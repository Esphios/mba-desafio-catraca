# Transações e invariantes: desenho verificável

## 1. Modelo formal
Para evento e, O(e)=|tickets pending ou confirmed|; C(e)=capacity; A(e)=0 se cancelled, senão C−O. Invariantes em todos os commits válidos: 0≤O≤C; evento cancelled implica O=0; status terminal não tem saída; código único; ticket tem job único; preço congelado; checked_in_at somente atribuído na primeira admissão de confirmed. Receitas e contagens derivam dos tickets, não de eventos de pagamento ou contadores de canal. A exclusão do catálogo depende exclusivamente de status published.

## 2. Linearização e lock order
READ COMMITTED. Todas as mutações de um evento usam `transaction.atomic()` e `SELECT ... FOR UPDATE` na linha Event, antes de tocar Ticket/PaymentJob. Django `select_for_update()` só avaliado dentro da transação; consultas ORM preguiçosas precisam ser materializadas. Não combinar leitura de ocupação na mesma query do lock: snapshot anterior à espera pode estar velho. Recontar em comando subsequente. Ordem: Event → Ticket (ordem estável por ID se vários) → PaymentJob. Worker descobre candidatos sem lock, nunca segura lock de job enquanto tenta adquirir evento. A leitura de código inválido procura somente no evento alvo, sem lock de evento alheio. Transações curtas, sem espera ou HTTP. Linearização em commit; resposta de sucesso só depois dele. Erros conhecidos de transação abortada permitem retry limitado com backoff; não repetir commit incerto.

## 3. Operações em pseudocódigo

```text
RESERVE(event_id, buyer, card):
  validate buyer/card; outcome = classify(card[-4:]); discard card
  ATOMIC:
    event = lock(event_id)
    require event exists and published
    occupied = count tickets pending or confirmed   # new SQL statement
    require occupied < capacity
    ticket = insert pending(snapshot price, unique code, buyer)
    insert durable job(ticket, outcome, clock_timestamp + delay)
  return immutable pending DTO

EDIT(actor, event_id, fields):
  ATOMIC:
    event = lock_owned(event_id, actor)
    require not cancelled; validate fields with current clock
    require new capacity >= count occupied after lock
    update fields (never ticket price)

RESOLVE(job_id):
  lookup immutable event_id without locks
  ATOMIC:
    event = lock(event_id)
    ticket = read/lock associated ticket; job = read/lock job
    if job not queued or now < due_at: no effect
    else if event published and ticket pending:
      transition to confirmed or declined; mark job done
    else: mark job ignored

CANCEL(actor, event_id):
  ATOMIC:
    event = lock_owned(event_id, actor); require published
    mark event cancelled
    bulk update confirmed -> refunded, pending -> cancelled
    preserve checked_in_at, declined, prices
  return committed result

ADMIT(actor,event_id,code):
  ATOMIC:
    event = lock_owned(event_id,actor)
    ticket = lookup within event by normalized code
    if missing: invalid
    elif event cancelled: cancelled
    elif ticket status != confirmed: not_confirmed
    elif checked_in_at present: used
    else: set checked_in_at once; allowed
```

Reserve locks only one event. Every mutation of capacity/price/status/ticket/check-in uses same event guard. Unique code global across events; retry savepoint handles collision without dropping event lock; no retry generic constraint. Job and ticket transaction atomic. Cancellation leaves queued jobs to be marked ignored by worker after due; state of ticket never changes thereafter. Deadline proof is empirical; same-commit cancellation meets semantics but must be measured <=10s.

## 4. Decision table for R10
| First true condition | Message | Mutation |
| --- | --- | --- |
| ticket absent or belongs elsewhere | Ingresso inválido para este evento | none |
| event cancelled | Evento cancelado | none |
| ticket not confirmed | Ingresso não confirmado | none |
| checked_in_at set | Ingresso já utilizado | none |
| otherwise | Entrada liberada | set timestamp |

Unauthorized actor is rejected before these business conditions. UI may show cancellation instead of input; direct action still checks invalid first. Refund retains historical used flag, dashboard counts only currently confirmed check-ins.

## 5. Simulator deadlines and failure modes
| Card suffix | Result | Planned delay | Required observation |
| --- | --- | --- | --- |
| 0001 | approved | 3 s | 2–5 s |
| 0002 | declined | 3 s | 2–5 s |
| 0003 | approved | 34 s | 30–40 s |
| 0004 | declined | 34 s | 30–40 s |
| other | declined | 3 s | 2–5 s |

Deterministic values within intervals reserve scheduling margin. Use DB time to calculate due after reservation lock, timestamp created/changed for measurement; worker never resolves early. Poll idle ~100ms, bounded batch 32; process independent transactions; no multi-event locks. If high queue lag, measure and tune worker concurrency and polling, never extend required deadlines. Default scale 1, accelerated only explicit test profile; real-time tests use normal scale. Worker crash before commit rolls back; after commit job terminal. If worker is offline beyond due, recovery is eventual, not a claim of deadline during outage. Health reflects outage.

## 6. Proof of capacity (conditional on protocol)
Base: new event capacity>=1 and O=0. All writers of an event serialize under same row lock; re-read state after acquiring it. Reserve increments only if O<C; approval leaves O; decline decrements; edit sets C'≥O; cancellation sets O=0 and blocks new reservations; check-in leaves O unchanged. Rollbacks do not change committed state. Induction across commits proves 0≤O≤C for service paths, assuming no direct bypass. This does not prove liveness, timing, correct implementation or arbitrary SQL writes. Avoid unprotected count triggers and `max(0, ...)` that hide invalid states. Test negative: mutate test implementation to bypass lock and use barrier to force two stale reads; test must catch oversell. Restore mutation, rerun. Never commit mutant.

## 7. Concurrency matrix
| Pair | Legal outcome | Forbidden |
| --- | --- | --- |
| two reserves, last seat | exactly one accepted | two accepted |
| reserve vs lower capacity | edit first: reserve may fail; reserve first: edit may fail | O>C |
| reserve vs price change | old or new snapshot depending on order | ticket later rewritten |
| reserve vs cancel | accepted before cancel becomes terminal; later reserve 404 | pending after cancel |
| approve vs cancel | approval first refunded; cancel first cancelled | confirmed after cancel |
| decline vs cancel | declined first remains; cancel first cancelled | declined after cancel-first |
| admit vs admit | allowed then used | two successes |
| admit vs cancel | allowed first then refund; cancel first no entry | entry after cancel |
| resolve vs resolve | one applied, one no-op | duplicate transition |
| read snapshot vs edit/cancel | one committed full snapshot | mixed old capacity/new ticket counts |

Test with TransactionTestCase or live server and independent DB connections, actual barriers, event fresh each round. Use lock acquisition test hooks ONLY in tests; don't test concurrency with mocks or one shared connection. Capture result histograms, final DB and timestamps; test both orderings, repeated stress + public HTTP 30/5 twice. Test across two processes/worker replicas. Use query inspection to ensure no stale counts after wait. No direct DB fixtures in release journey.
