#!/usr/bin/env python3
"""Independent small-state oracle: explore serialized business transitions; not application code."""
from dataclasses import dataclass, replace
from collections import deque

@dataclass(frozen=True)
class Ticket:
    status: str
    cents: int
    used: bool = False

@dataclass(frozen=True)
class Event:
    status: str = 'draft'
    capacity: int = 1
    cents: int = 100
    tickets: tuple[Ticket,...] = ()

def metrics(s):
    confirmed=[t for t in s.tickets if t.status=='confirmed']
    pending=sum(t.status=='pending' for t in s.tickets)
    return (len(confirmed),pending,sum(t.used for t in confirmed),0 if s.status=='cancelled' else s.capacity-len(confirmed)-pending,sum(t.cents for t in confirmed),sum(t.status=='refunded' for t in s.tickets))

def invariant(s):
    c,p,k,a,r,refund=metrics(s)
    assert 0<=c+p<=s.capacity
    assert 0<=k<=c and a>=0 and r>=0
    if s.status=='cancelled': assert (c,p,k,a,r)==(0,0,0,0,0)
    assert all(t.cents>0 for t in s.tickets)

def update(s,i,t): return replace(s,tickets=s.tickets[:i]+(t,)+s.tickets[i+1:])

def successors(s):
    c,p,*_=metrics(s)
    if s.status=='draft': yield 'publish',replace(s,status='published')
    if s.status!='cancelled':
        for cap in (1,2,3):
            if cap>=c+p: yield 'edit-capacity',replace(s,capacity=cap)
        for price in (100,150): yield 'edit-price',replace(s,cents=price)
    if s.status=='published':
        if c+p<s.capacity and len(s.tickets)<3:
            yield 'reserve',replace(s,tickets=s.tickets+(Ticket('pending',s.cents),))
        yield 'cancel',replace(s,status='cancelled',tickets=tuple(replace(t,status={'pending':'cancelled','confirmed':'refunded'}.get(t.status,t.status)) for t in s.tickets))
    for i,t in enumerate(s.tickets):
        if s.status=='published' and t.status=='pending':
            yield 'approve',update(s,i,replace(t,status='confirmed'))
            yield 'decline',update(s,i,replace(t,status='declined'))
        else: yield 'late-or-duplicate-payment',s
        if s.status=='published' and t.status=='confirmed' and not t.used:
            yield 'check-in',update(s,i,replace(t,used=True))
        else: yield 'reject-check-in',s

def transition_invariant(old,new):
    invariant(new)
    for a,b in zip(old.tickets,new.tickets):
        assert a.cents==b.cents
        assert not a.used or b.used
        if a.status in {'declined','cancelled','refunded'}: assert a.status==b.status
    if old.status=='cancelled': assert old==new

def main():
    start=Event(); q=deque([start]); visited={start}; transitions=0
    while q:
        s=q.popleft();invariant(s)
        for action,n in successors(s):
            transition_invariant(s,n);transitions+=1
            if n not in visited: visited.add(n);q.append(n)
    # Known fixed public dashboard oracle plus history after cancellation.
    sample=Event('published',3,150,(Ticket('confirmed',100,True),Ticket('confirmed',100),Ticket('confirmed',150),Ticket('declined',100)))
    assert metrics(sample)==(3,0,1,0,350,0)
    cancel=next(x for a,x in successors(sample) if a=='cancel')
    assert metrics(cancel)==(0,0,0,0,0,3)
    # Negative: a hypothetical bypass overbooks cap1, must violate invariant.
    try: invariant(Event('published',1,100,(Ticket('pending',100),Ticket('pending',100))))
    except AssertionError: pass
    else: raise AssertionError('oracle failed to reject oversell')
    print(f'PASS abstract model: {len(visited)} states, {transitions} transitions; oversell negative rejected.')
    print('Bounded model assumes serialized transitions; not a database/concurrency or product test.')
if __name__=='__main__': main()
