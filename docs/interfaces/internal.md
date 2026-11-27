# Internal interface registry (normative design)

All types conceptual Python dataclasses/enums, immutable at boundary. Implementation can refine names only via amendment. No HTTP objects in domain. `Actor(id, role, email)` created by identity; no role from client. `WebBuyer(participant_id, email)` constructed from Actor; `PartnerBuyer(email)` constructed after key guard. `EventEdit(name, venue, starts_at, capacity, price_cents)`. `PublicEvent(id, name, venue, starts_at, price_cents, available_seats)`. `TicketView(id, event_id, event_name, code, status, checked_in, price_cents)` internal only; serialize allowlist. `ManagementView(event fields, metrics, controls)` one snapshot.

| Port | Owner | Inputs / return | Errors / transaction |
| --- | --- | --- | --- |
| normalize_email | F01 (shared canonical routine); F02 consumes | str -> canonical str | invalid; no DB |
| require_participant / require_organizer | F02 | authenticated session -> Actor | unauthenticated, wrong_role |
| event_guard | F03 | event id, optional organizer Actor -> locked event context | not_found; atomic owner; caller must finish within context; lock first |
| occupied_count | F03 | event id -> count of pending + confirmed | within guard for writes; read after guard |
| create_event | F03 | Actor, EventEdit -> event | invalid_input; atomic |
| edit_event | F03 | Actor, id, EventEdit -> event | not_found, event_closed, invalid_input, capacity_below_occupied; guard |
| publish_event | F03 | Actor, id -> event | not_found, event_closed; guard |
| public_catalog / public_detail | F03 | optional event id -> PublicEvent list/item | no drafts/cancelled; single statement |
| reserve | F04 | event_id, Buyer, card string -> immutable pending TicketView | invalid_request, event_not_available, sold_out; guard and commit before return |
| read_ticket | F04 | id -> TicketView or None | no ownership restriction here; adapter selects authorization |
| list_participant_tickets | F04 | Actor participant -> list TicketView | filters by actor.id; no email link |
| resolve_due | F04 | job id -> applied/ignored/not_due | event→ticket→job order; commit terminal effect and job |
| admit | F07 | Actor organizer, event id, code -> enum/message | owner check before ticket lookup; guard |
| cancel_event | F07 | Actor organizer, event id -> terminal result | not_found, not_cancellable; guard |
| basic_management_snapshot | F03 | Actor organizer, event id -> basic management DTO | owner scoped, no fake metrics; replaced via composition root |
| management_snapshot | F07 | Actor organizer, event id -> ManagementView | owner scoped single query; no stale DTO; composition root injects it into F03 shell after integration |

Error precedence for API is external contract; domain errors are typed and adapters translate, never catch all as sold_out. `event_guard` accepts no untrusted owner identity. F04/F07 must not call each other in cycles: both use F03 guard and shared transition enum; F07 cancellation may use F04 shared transition helper for bulk update, no direct writes outside guard. Web UI is a consumer; no models mutated from templates, admin, signals or HTTP handlers. Ownership of config/url wiring fixed by coordinator; F07 receives partial slot and named URL include; no direct import from sibling modules.

## Schema change handoff
Migration and model changes require coordinator PR or explicit ownership transfer, re-run fresh + upgrade + dependent contracts. Freeze before W5. All ports and names referenced here are proposed, no implementation claim.

## Management view extension
F03 owns the stable management route and render shell. Before F07, the composition root supplies a basic owner-scoped snapshot provider. F07 registers a replacement provider via the composition root; it returns the full event data and metrics from a single query. The shell must render all critical fields from that DTO, not fetch the event separately. F03 must not import F07. The coordinator owns this single wiring change; placeholder does not simulate operations or report metrics.

## Ownership exato e convenções W0 (propostos)

- F01 cria `app/accounts/models.py`, `app/accounts/migrations/`, `app/accounts/email_policy.py`, `app/coredata/`, `app/catraca_platform/`, `app/config/`, `bin/`, `app/worker/main.py` (heartbeat inicial). F02 recebe `app/accounts/` exceto model, migrations e email_policy congelados; alterações nesses três exigem PR do coordenador. F04 recebe `app/worker/main.py` e demais `app/worker/` por handoff explícito de F01; mantém contrato de heartbeat e entrypoint. F03 possui `app/catalog/` e provider inicial; F07 possui `app/operations/` e provider final. Coordenador possui `app/config/urls.py`, `app/config/management_provider.py`, `app/templates/base.html` e mudanças de schema após F01; registra a troca de provider sem import de F07 por F03. F05/F06/F07 escrevem apenas módulos e templates próprios.
- `normalize_email`: strip de whitespace externo, casefold Unicode completo, validação Django de endereço canônico; rejeitar vazio, formato inválido e comprimento canônico >254 caracteres. Mesma rotina desde F01 para seed, signup, login e e-mail do comprador parceiro; não associar parceiro a conta. Banco armazena valor canônico com UNIQUE e collation determinística `C`; nenhuma escrita de usuário contorna a rotina. Testar variantes ASCII/Unicode (incluindo expansão por casefold), concorrência e seed. Não confiar em lower do DB como equivalente a casefold. Migrações/fixtures passam pela rotina ou comprovam canonicidade. Não afirmar que SQL arbitrário normaliza Unicode.
- `PartnerBuyer(email)` é discriminado pelo tipo; credencial única é validada pelo adapter, não armazenada nem enviada ao ledger. Campos extras JSON permanecem ignorados. Duplicidade de chave HTTP deve ser rejeitada antes de qualquer coalescência destrutiva; validar no ingresso HTTP real, não só no Django test client. Se servidor/proxy perder multiplicidade, ajustar ingresso em F01/F06 por amendment, não aceitar silenciosamente.
- Role bootstrap possui objetos/migrations; runtime sem superuser, CREATEDB, CREATEROLE ou ownership; grants de CONNECT, USAGE e DML estritamente necessários (incluindo sequências quando usadas). Remover CREATE público no schema de aplicação; credenciais de bootstrap indisponíveis a web/worker; testar DDL negado e DML permitido em F01. Role de testes isolada pode criar banco/migrar, nunca usada pela demo.
