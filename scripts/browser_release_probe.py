#!/usr/bin/env python3
"""Planned black-box acceptance probe, steps 2–16; requires completed app + Playwright.
Run against a fresh, disposable local demo with default gateway delays. Never uses DB writes.
"""
import argparse
import concurrent.futures
import datetime as dt
import json
import threading
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from zoneinfo import ZoneInfo
from playwright.sync_api import sync_playwright, expect

CARDS={'fast_ok':'4000000000000001','fast_no':'4000000000000002','slow_ok':'4000000000000003','slow_no':'4000000000000004'}
SEED={'A':('gestao.a@example.test','LocalA-2026!'),'B':('gestao.b@example.test','LocalB-2026!'),'P':('pessoa@example.test','LocalP-2026!')}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None

def run(args):
    web=args.web.rstrip('/');api=args.api.rstrip('/')+'/api/partner';nonce=uuid.uuid4().hex[:10]
    out=Path(args.evidence);out.mkdir(parents=True,exist_ok=False)
    evidence=[]
    def record(step,message,**fields):
        item={'step':step,'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'result':message,**fields}
        evidence.append(item);(out/'observations.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2));print(f'{step}: {message}',flush=True)
    def http(path,method='GET',body=None,key=args.key,raw=None):
        headers={'Accept':'application/json'}
        if key is not None:headers['X-Api-Key']=key
        if body is not None or raw is not None:headers['Content-Type']='application/json'
        data=raw if raw is not None else json.dumps(body).encode() if body is not None else None
        request=urllib.request.Request(api+path,data=data,headers=headers,method=method)
        opener=urllib.request.build_opener(NoRedirect())
        try:
            with opener.open(request,timeout=15) as response: code,payload=response.status,response.read()
        except urllib.error.HTTPError as exc:code,payload=exc.code,exc.read()
        return code,json.loads(payload)
    def catalog():
        code,items=http('/events');assert code==200 and isinstance(items,list),(code,items)
        for x in items:
            assert set(x)=={'id','name','startsAt','priceCents','availableSeats'},x
            assert type(x['priceCents']) is int and type(x['availableSeats']) is int,x
        return {x['id']:x for x in items}
    def buy(eid,card,email=None):
        start=time.monotonic();code,data=http(f'/events/{eid}/purchases','POST',{'buyerEmail':email or f'partner-{uuid.uuid4().hex[:12]}@example.test','cardNumber':card})
        assert code==202 and set(data)=={'ticketId','code','status'} and data['status']=='pending',(code,data)
        return start,data
    def ticket(tid):
        code,data=http(f'/tickets/{tid}');assert code==200 and set(data)=={'ticketId','code','eventId','status','checkedIn'},(code,data)
        assert data['ticketId']==tid and type(data['checkedIn']) is bool,data
        return data
    def wait_ticket(tid,want,deadline):
        while time.monotonic()<=deadline:
            data=ticket(tid)
            if data['status']==want:
                assert time.monotonic()<=deadline,(tid,'observed too late');return data
            time.sleep(.1)
        raise AssertionError(f'{tid}: expected {want}, last {ticket(tid)}')
    def wait_until(start,seconds):time.sleep(max(0,start+seconds-time.monotonic()))
    def login(page,who):
        page.goto(web+'/conta/entrar/');email,pw=SEED[who];page.get_by_label('E-mail',exact=True).fill(email);page.get_by_label('Senha',exact=True).fill(pw);page.get_by_role('button',name='Entrar',exact=True).click()
    def form(page,name,cap,price,date):
        for label,value in [('Nome',name),('Início',date),('Local','Sala de teste'),('Lotação',str(cap)),('Preço',price)]:page.get_by_label(label,exact=True).fill(value)
    future=(dt.datetime.now(ZoneInfo('America/Sao_Paulo'))+dt.timedelta(days=32)).replace(hour=19,minute=30,second=0,microsecond=0).strftime('%Y-%m-%dT%H:%M')
    past=(dt.datetime.now(ZoneInfo('America/Sao_Paulo'))-dt.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
    def create(page,tag,cap,price,publish=False):
        name=f'{tag}-{nonce}';page.goto(web+'/gestao/eventos/novo/');form(page,name,cap,price,future);page.get_by_role('button',name='Criar evento',exact=True).click();expect(page.get_by_test_id('event-management')).to_be_visible();url=page.url
        eid=url.rstrip('/').split('/')[-1];assert eid and eid!='novo'
        if publish:page.get_by_role('button',name='Publicar',exact=True).click()
        return name,eid,url
    def panel(page,url,expected):
        page.goto(url)
        for field,val in zip(['confirmed','pending','checkins','available','revenue','refunded'],expected):expect(page.get_by_test_id('metric-'+field)).to_have_text(str(val),timeout=3000)
    def admission(page,url,code,msg):
        page.goto(url);page.get_by_label('Código do ingresso',exact=True).fill(code);page.get_by_role('button',name='Validar entrada',exact=True).click();expect(page.get_by_test_id('admission-result')).to_have_text(msg)
    def denied(page,url,name):
        response=page.goto(url);assert response is not None
        assert response.status in (403,404) or '/conta/entrar/' in page.url,(response.status,page.url)
        assert page.get_by_text(name,exact=True).count()==0 and page.get_by_test_id('event-management').count()==0
    def screenshot(page,label):page.screenshot(path=str(out/f'{label}.png'),full_page=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        contexts=[]
        def newpage():
            ctx=browser.new_context();contexts.append(ctx);return ctx.new_page()
        a,b,participant,anonymous,seed_p=[newpage() for _ in range(5)]
        try:
            login(a,'A');login(b,'B');login(seed_p,'P')
            name,e1,url=create(a,'E1',2,'100,00');anonymous.goto(web+'/');assert anonymous.get_by_text(name,exact=True).count()==0 and e1 not in catalog();record(2,'draft hidden',event=e1)
            a.goto(web+'/gestao/eventos/novo/');badname=f'Invalid-{nonce}';form(a,badname,2,'10,00',past);a.get_by_role('button',name='Criar evento',exact=True).click();assert a.get_by_test_id('event-management').count()==0;a.goto(web+'/gestao/eventos/');assert a.get_by_text(badname,exact=True).count()==0;record(3,'past rejected')
            a.goto(url);a.get_by_role('button',name='Publicar',exact=True).click();assert catalog()[e1]['availableSeats']==2 and catalog()[e1]['priceCents']==10000;anonymous.goto(web+'/');expect(anonymous.get_by_text(name,exact=True)).to_be_visible();record(4,'published')
            participant.goto(web+'/conta/cadastro/');participant.get_by_label('Nome',exact=True).fill('Pessoa teste');participant.get_by_label('E-mail',exact=True).fill(f'person-{nonce}@example.test');participant.get_by_label('Senha',exact=True).fill('LocalTest-2026!');participant.get_by_role('button',name='Criar conta',exact=True).click();participant.goto(web+f'/eventos/{e1}/');participant.get_by_label('Número do cartão',exact=True).fill(CARDS['fast_ok']);start=time.monotonic();participant.get_by_role('button',name='Comprar',exact=True).click();expect(participant.get_by_test_id('ticket-status')).to_have_text('pendente',timeout=1500);c1=participant.get_by_test_id('ticket-code').inner_text().strip();assert c1
            while time.monotonic()<start+5:
                participant.reload();status=participant.get_by_test_id('ticket-status').inner_text().strip()
                if status=='confirmado':break
                time.sleep(.1)
            else:raise AssertionError('web ticket not confirmed within 5s')
            assert time.monotonic()<=start+5;expect(participant.get_by_text(name,exact=True)).to_be_visible();screenshot(participant,'05-ticket');record(5,'web pending and confirmed',code=c1)
            t2_at,t2=buy(e1,CARDS['slow_no']);assert catalog()[e1]['availableSeats']==0;record(6,'partner pending consumes last seat',ticket=t2['ticketId'])
            assert http(f'/events/{e1}/purchases','POST',{'buyerEmail':'full@example.test','cardNumber':CARDS['fast_ok']})==(409,{'error':'sold_out'});participant.goto(web+f'/eventos/{e1}/');expect(participant.get_by_text('Ingressos esgotados',exact=True)).to_be_visible();assert time.monotonic()<t2_at+30;record(7,'sold out before slow decline')
            wait_until(t2_at,45);assert ticket(t2['ticketId'])['status']=='declined' and catalog()[e1]['availableSeats']==1;t3_at,t3=buy(e1,CARDS['fast_ok']);wait_ticket(t3['ticketId'],'confirmed',t3_at+5);record(8,'decline freed seat')
            a.goto(url);form(a,name,1,'100,00',future);a.get_by_role('button',name='Salvar',exact=True).click();assert catalog()[e1]['availableSeats']==0;a.goto(url);expect(a.get_by_label('Lotação',exact=True)).to_have_value('2');form(a,name,3,'150,00',future);a.get_by_role('button',name='Salvar',exact=True).click();assert catalog()[e1]['priceCents']==15000 and catalog()[e1]['availableSeats']==1;t4_at,t4=buy(e1,CARDS['fast_ok']);wait_ticket(t4['ticketId'],'confirmed',t4_at+5);panel(a,url,(3,0,0,0,'R$ 350,00',0));screenshot(a,'09-panel');record(9,'historical revenue correct')
            admission(a,url,c1,'Entrada liberada');admission(a,url,c1,'Ingresso já utilizado');admission(a,url,t2['code'],'Ingresso não confirmado');admission(a,url,'ZZZZZZZZ','Ingresso inválido para este evento');panel(a,url,(3,0,1,0,'R$ 350,00',0));record(10,'check-in cases')
            b.goto(web+'/gestao/eventos/');assert b.get_by_text(name,exact=True).count()==0;denied(b,url,name);denied(seed_p,url,name);denied(anonymous,url,name);_,e2,_=create(b,'E2',1,'20,00',True);t_at,t=buy(e2,CARDS['fast_ok']);wait_ticket(t['ticketId'],'confirmed',t_at+5);admission(a,url,t['code'],'Ingresso inválido para este evento');record(11,'owner isolation and foreign code')
            name3,e3,url3=create(a,'E3',5,'50,00',True);t5_at,t5=buy(e3,CARDS['slow_ok']);t6_at,t6=buy(e3,CARDS['fast_ok']);wait_ticket(t6['ticketId'],'confirmed',t6_at+5);assert ticket(t5['ticketId'])['status']=='pending';a.goto(url3);cancel_at=time.monotonic();assert cancel_at<t5_at+30;a.get_by_role('button',name='Cancelar evento',exact=True).click();assert time.monotonic()<t5_at+30;record(12,'cancel submitted before slow payment')
            assert e3 not in catalog();anonymous.goto(web+'/');assert anonymous.get_by_text(name3,exact=True).count()==0;assert http(f'/events/{e3}/purchases','POST',{'buyerEmail':'late@example.test','cardNumber':CARDS['fast_ok']})==(404,{'error':'event_not_available'});wait_ticket(t5['ticketId'],'cancelled',cancel_at+10);wait_ticket(t6['ticketId'],'refunded',cancel_at+10);a.goto(url3);assert a.get_by_role('button',name='Salvar',exact=True).count()==0;record(13,'cancel propagated')
            wait_until(t5_at,45);assert ticket(t5['ticketId'])['status']=='cancelled' and ticket(t6['ticketId'])['status']=='refunded';expect(a.get_by_text('Evento cancelado',exact=True)).to_be_visible();panel(a,url3,(0,0,0,0,'R$ 0,00',1));screenshot(a,'14-cancelled');record(14,'late result ignored')
            for tag in ('E4','E5'):
                _,eid,manage=create(a,tag,5,'10,00',True);barrier=threading.Barrier(30,timeout=15)
                def burst(i):
                    barrier.wait();started=time.monotonic();result=http(f'/events/{eid}/purchases','POST',{'buyerEmail':f'load-{tag}-{nonce}-{i}@example.test','cardNumber':CARDS['fast_ok']});return started,result
                with concurrent.futures.ThreadPoolExecutor(max_workers=30) as pool:results=list(pool.map(burst,range(30)))
                accepted=[x for _,(status,x) in results if status==202];rejected=[x for _,(status,x) in results if status==409];assert len(accepted)==5 and len(rejected)==25 and all(x=={'error':'sold_out'} for x in rejected)
                assert all(set(x)=={'ticketId','code','status'} and x['status']=='pending' for x in accepted);assert len({x['ticketId'] for x in accepted})==len({x['code'] for x in accepted})==5
                deadline=min(started for started,_ in results)+10
                for x in accepted:wait_ticket(x['ticketId'],'confirmed',deadline)
                panel(a,manage,(5,0,0,0,'R$ 50,00',0));assert time.monotonic()<=deadline;record(15,'concurrency verified',event=eid,accepted=5,sold_out=25)
            absent=str(uuid.uuid4());paths=[('/events','GET',None),(f'/events/{absent}/purchases','POST',b'{'),(f'/tickets/{absent}','GET',None)]
            for key in (None,args.key+'-wrong'):
                for path,method,raw in paths:assert http(path,method,key=key,raw=raw)==(401,{'error':'unauthorized'})
            assert http(f'/events/{absent}/purchases','POST',raw=b'{')==(422,{'error':'invalid_request'});assert http(f'/events/{absent}/purchases','POST',{'buyerEmail':'bad@example.test','cardNumber':'123'})==(422,{'error':'invalid_request'});assert http(f'/tickets/{absent}')==(404,{'error':'ticket_not_found'});record(16,'API negative cases')
        except Exception as exc:
            record('failure',type(exc).__name__,detail=str(exc));raise
        finally:
            for ctx in contexts:ctx.close()
            browser.close()
    print('PASS steps 2–16 only. Steps 1, 17–18 and X14–X16 require separate evidence.')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--web',required=True);p.add_argument('--api',required=True);p.add_argument('--key',required=True);p.add_argument('--evidence',required=True,help='New empty output path (must not exist)');run(p.parse_args())
if __name__=='__main__':main()
