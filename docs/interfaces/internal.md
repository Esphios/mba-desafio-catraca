# Internal interface registry (normative design)

All types conceptual Python dataclasses/enums, immutable at boundary. Implementation can refine names only via amendment. No HTTP objects in domain. `Actor(id, role, email)` created by identity; no role from client. `WebBuyer(participant_id, email)` constructed from Actor; `PartnerBuyer(email)` constructed after key guard and canonicalized at the F04 reserve boundary. `EventEdit(name, venue, starts_at, capacity, price_cents)`. `PublicEvent(id, name, venue, starts_at, price_cents, available_seats)`. `TicketView(id, event_id, event_name, code, status, checked_in, price_cents)` internal only; serialize allowlist. `BasicManagementView(id, owner_id, name, venue, starts_at, capacity, price_cents, status, controls)` contains no metrics. `ManagementView(event fields, metrics, controls)` is one snapshot.

| Port | Owner | Inputs / return | Errors / transaction |
| --- | --- | --- | --- |
| normalize_email | F01; F02 and F04 consume | str -> canonical str | invalid/too_long; no DB; F04 applies it to PartnerBuyer before lock |
| clock_now | F01 | no input -> aware UTC datetime | injectable in unit/DB tests; persistent deadlines use DB clock after lock |
| fixture_factory | F01 test support | named scenario + overrides -> isolated synthetic objects | never evidence by itself; no production/debug endpoint |
| worker_command | F01 entrypoint, handed to F04 | settings + stop signal -> loop exit code | F01 heartbeat-only; F04 preserves command/readiness and adds durable job consumption |
| require_participant / require_organizer | F02 | authenticated session -> Actor | unauthenticated, wrong_role |
| owner_predicate | F02 | Actor, resource owner id -> boolean | pure/server-side; resource owner performs generic not_found mapping |
| event_guard | F03 | event id, optional organizer Actor -> locked event context | not_found; atomic owner; only F03 loads/locks Event; caller finishes inside context |
| occupied_count | F03 | event id -> count of pending + confirmed | within guard for writes; read after guard |
| create_event | F03 | Actor, EventEdit -> event | invalid_input; atomic |
| edit_event | F03 | Actor, id, EventEdit -> event | not_found, event_closed, invalid_input, capacity_below_occupied; guard |
| publish_event | F03 | Actor, id -> event | not_found, event_closed; guard |
| public_catalog / public_detail | F03 | optional event id -> PublicEvent list/item | no drafts/cancelled; single statement |
| reserve | F04 | event_id, Buyer, card string -> immutable pending TicketView | invalid_request, event_not_available, sold_out; guard and commit before return |
| read_ticket | F04 | id -> TicketView or None | no ownership restriction here; adapter selects authorization |
| list_participant_tickets | F04 | Actor participant -> list TicketView | filters by actor.id; no email link |
| resolve_due | F04 | job id -> applied/ignored/not_due | event→ticket→job order; commit terminal effect and job |
| transition_ticket | F04 | locked ticket, allowed transition -> changed/noop | shared enum/table; terminal cannot revive; F07 consumes only inside event_guard |
| admit | F07 | Actor organizer, event id, code -> enum/message | owner check before ticket lookup; guard |
| cancel_event | F07 | Actor organizer, event id -> terminal result | not_found, not_cancellable; guard |
| basic_management_snapshot | F03 | Actor organizer, event id -> BasicManagementView | owner scoped, one statement, no fake metrics; replaced via composition root |
| management_snapshot | F07 | Actor organizer, event id -> ManagementView | owner scoped single query; no stale DTO; composition root injects it into F03 shell after integration |

Error precedence for API is external contract; domain errors are typed and adapters translate, never catch all as sold_out. `event_guard` accepts no untrusted owner identity. F04/F07 must not call each other in cycles: both use F03 guard; F07 may consume the F04 transition port inside the guard, never write around it. Web UI is a consumer; no models mutated from templates, admin, signals or HTTP handlers. Ownership of config/url wiring and base layout is fixed by coordinator; F03 owns the module-local management shell/slot, F07 receives the partial slot and named URL include; no direct import from sibling modules.

## Schema change handoff
Migration and model changes require coordinator PR or explicit ownership transfer, re-run fresh + upgrade + dependent contracts. Freeze before W5. All ports and names referenced here are proposed, no implementation claim.

## Management view extension
F01 precria no composition root um hook configurável por dotted paths para provider, partial e URLconf de operações; o default aponta para o snapshot básico e slot vazio de F03. F03 owns the stable management route and render shell. F07 implementa provider, partial e URLconf somente em `app/operations/`; no gate local, settings de teste apontam os hooks reais para esses componentes e exercitam a URL HTTP completa, sem mock, stub ou edição de arquivo compartilhado. Depois do local PASS/merge, o coordenador troca os defaults no único commit de wiring, roda A28 novamente e só então permite X14/X15. O provider F07 retorna dados completos e métricas em uma instrução; o shell renderiza o DTO sem buscar Event separadamente. F03 não importa F07, e o placeholder nunca simula operações nem métricas.

## Ownership exato e convenções W0 (propostos)

- F01 cria `app/accounts/models.py`, `app/accounts/migrations/`, `app/accounts/email_policy.py`, `app/coredata/`, `app/catraca_platform/`, `app/config/`, `bin/`, `app/worker/main.py` (heartbeat inicial), inclusive hooks settings-driven de gestão. F02 recebe `app/accounts/` exceto model, migrations e email_policy congelados; alterações nesses três exigem PR do coordenador. F04 recebe `app/worker/main.py` e demais `app/worker/` por handoff explícito de F01; mantém contrato de heartbeat e entrypoint. F03 possui `app/catalog/` e provider inicial; F07 possui `app/operations/`, provider, partial e URLconf finais. Coordenador possui `app/config/urls.py`, `app/config/management_provider.py`, `app/templates/base.html` e mudanças de schema após F01; após local PASS de F07, registra a troca dos defaults em commit de wiring separado e repete A28 antes dos integrados. F05/F06/F07 escrevem apenas módulos e templates próprios; settings override no teste local usa os mesmos componentes reais de F07 e não transfere ownership.
- `normalize_email`: strip de whitespace externo, casefold Unicode completo, validação Django de endereço canônico; rejeitar vazio, formato inválido e comprimento canônico >254 caracteres. Mesma rotina desde F01 para seed, signup e login; F04 a aplica ao `PartnerBuyer` antes de abrir `event_guard`, portanto F06 não importa F01. Parceiro nunca é associado a conta. Banco armazena valor canônico com UNIQUE e collation determinística `C`; nenhuma escrita de usuário contorna a rotina. Testar variantes ASCII/Unicode (incluindo expansão por casefold), concorrência e seed. Não confiar em lower do DB como equivalente a casefold. Migrações/fixtures passam pela rotina ou comprovam canonicidade. Não afirmar que SQL arbitrário normaliza Unicode.
- `PartnerBuyer(email)` é discriminado pelo tipo; credencial única é validada pelo adapter, não armazenada nem enviada ao ledger. Campos extras JSON permanecem ignorados. Duplicidade de chave HTTP deve ser rejeitada antes de qualquer coalescência destrutiva; validar no ingresso HTTP real, não só no Django test client. Se servidor/proxy perder multiplicidade, ajustar ingresso em F01/F06 por amendment, não aceitar silenciosamente.
- Role bootstrap possui objetos/migrations; runtime sem superuser, CREATEDB, CREATEROLE ou ownership; grants de CONNECT, USAGE e DML estritamente necessários (incluindo sequências quando usadas). Remover CREATE público no schema de aplicação; credenciais de bootstrap indisponíveis a web/worker; testar DDL negado e DML permitido em F01. Role de testes isolada pode criar banco/migrar, nunca usada pela demo.
