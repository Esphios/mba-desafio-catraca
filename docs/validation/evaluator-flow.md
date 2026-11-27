# Fluxo público de avaliação | release em main

Pré-condições: clone limpo main, gateway escala 1, browser real e cliente HTTP; use contas seed e datas relativas ao próximo mês. Não inserir fixtures por SQL neste fluxo. Registrar commit, relógio monotônico, E1–E5, T2–T6 e códigos, saída HTTP e screenshot da UI. Não seguir redirects em API. Cada passo obrigatório; falha bloqueia release.

| Passo | Procedimento | Oráculo |
| --- | --- | --- |
| 1 | Clonar em pasta vazia; comando de subida README | web pronta, seed carregada, sem setup |
| 2 | A cria E1 cap 2 preço R$100 futuro, deixa draft; sair; vitrine e GET events | E1 ausente em ambos |
| 3 | A tenta criar com data ontem | rejeitado, nenhum evento criado |
| 4 | A publica E1 e captura ID pela API | E1 nos dois canais; availableSeats=2, priceCents=10000 |
| 5 | cadastrar participante novo, comprar E1 final 0001, abrir Meus ingressos | pendente imediato, confirmado em até 5s; evento, código C1 |
| 6 | POST partner E1 final 0004, guardar T2/C2 e timestamp | 202 pending; availableSeats=0 |
| 7 | antes de 30s desde T2, tentar outra compra 0001 e abrir vitrine | 409 sold_out; Ingressos esgotados |
| 8 | aos 45s desde T2, GET ticket; depois comprar T3 final 0001 | T2 declined, vaga 1; T3 confirmed até 5s |
| 9 | A tenta cap 1 (nega), altera para 3 e preço 15000; compra T4 0001 e espera confirmar | painel 3 confirmados, 0 pendentes, 0 check-ins, 0 vagas, R$350,00, 0 estornados |
| 10 | check-in C1, repetir C1, C2, ZZZZZZZZ; copiar URL | Entrada liberada; Ingresso já utilizado; Ingresso não confirmado; Ingresso inválido para este evento; painel check-ins 1 |
| 11 | B tenta lista/URL de E1; cria E2 cap 1 R$20 publicado, compra C3 pela API; participante seed e deslogado tentam URL; A tenta C3 em E1 | nenhum dado E1 para B/P/anônimo; C3 inválido para E1 |
| 12 | A cria E3 cap5 R$50 publicado; compra T5 0003 e T6 0001; espera T6 confirmed, cancela antes de 30s de T5 | T5 ainda pending ao cancelar; T6 confirmed antes |
| 13 | consultar catálogo e API; POST compra E3; GET T5/T6; abrir gestão e tentar editar | E3 ausente; POST 404 event_not_available; T6 refunded, T5 cancelled ≤10s; edição negada |
| 14 | aguardar até 45s de T5; consultar e tentar check-in C6 | T5 segue cancelled; Evento cancelado; painel 0/0/0/0/R$0,00/1 |
| 15 | E4 e E5 novos cap5 R$10; para cada um disparar 30 POST simultâneos final 0001 | por evento 5×202, 25×409 sold_out; até 10s painel 5 confirmed, 0 vagas |
| 16 | três rotas sem chave e com chave errada, POST card 123, GET ticket inexistente | seis 401 unauthorized; 422 invalid_request; 404 ticket_not_found |
| 17 | gates; down; verificar portas e containers; up novamente | gates exit 0, nenhuma porta/serviço do projeto ativo após down, seed funciona na nova subida |
| 18 | revisar PRD/contratos/relatórios/state/AGENTS/README e PRs paralelos | rastreabilidade integral, relatórios novos e imutáveis, todas features completas, repo público e PRs mergeados com overlap |

## Comandos de apoio
```bash
export WEB=http://127.0.0.1:8080 API=http://127.0.0.1:8080 KEY=local-passgate-26
curl -sS -H "X-Api-Key: $KEY" "$API/api/partner/events"
# E1 deve vir do produto, não inventar ID
curl -sS -i -X POST "$API/api/partner/events/$E1/purchases" \
  -H "X-Api-Key: $KEY" -H 'Content-Type: application/json' \
  -d '{"buyerEmail":"evaluator@example.test","cardNumber":"4000000000000004"}'
curl -sS -H "X-Api-Key: $KEY" "$API/api/partner/tickets/$T2"
# E4/E5 frescos, cap5, publicados; probe usa HTTP real
python3 scripts/partner_probe.py --base "$API" --key "$KEY" --events "$E4" "$E5"
```
Probe verifica rajadas e shape/precedência, não substitui painel/browser ou todos os tempos. Use container para Python se necessário. Não execute em eventos já usados.

## Cenários integrados extras
TEST-X14: compra web, confirmação, painel, check-in, cancelamento, status estornado em Meus ingressos e ausência do catálogo. TEST-X15: compra parceiro conta na lotação/painel, check-in atualiza checkedIn, cancelamento bloqueia compra e estorna mantendo GET ticket. TEST-X16: disputa web/API pela última vaga (cap1), um sucesso e um sold_out, ticket web consultável na API, ticket parceiro com e-mail igual não aparece na conta web. TEST-A35/A36 em ambiente isolado com DB real, não confundir com fluxo público. TEST-A34 chave antes de JSON inválido; teste as duas condições juntas.

## Evidência
Para cada passo: timestamp e SHA, ação/entrada, resultado esperado e observado, HTTP status/body sanitizado, screenshot ou logs, duração quando aplicável. Reprovar se não houver evidência. P05: comparar GitHub PR commit lists, primeiro_i < último_j para todos i≠j na wave; links no README. P03: verificar git log de cada relatório e ausência de modificações; conferir metadados e itens. Se houve correção, novo PR e fluxo completo em clone novo; não reutilizar resultados do SHA anterior.

## Probe browser planejado
`python3 scripts/browser_release_probe.py --web "$WEB" --api "$API" --key "$KEY" --evidence artifacts/flow-unique` automatiza passos 2–16 com Playwright Python e Chromium (instalados no container de testes na F01). Depende dos labels/test IDs definidos em docs/interfaces/web.md. Use somente ambiente local descartável no modo padrão. Ele não substitui passos 1, 17, 18, X14–X16, POSTs forjados e demais testes adversariais. F01/F05/F06/F07 devem integrar e ajustar ao contrato de UI na implementação; não ajustar oráculos para aceitar falha. O script foi validado sintaticamente, não executado contra aplicação inexistente.
