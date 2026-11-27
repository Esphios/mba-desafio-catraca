# Web UI functional contract

Simple accessible HTML; no JavaScript required beyond optional convenience. Server rendered forms with CSRF, labels, validation errors and PRG. Prefer roles/names in browser tests, stable data-testid only when needed. Never render secret values or full card. No extra pages demanded beyond journeys.

| Method/path | Actor | Expected behavior |
| --- | --- | --- |
| GET / | any | public published catalog, sold-out shown |
| GET /eventos/<id>/ | any | published detail or 404 |
| POST /eventos/<id>/comprar/ | participant | reserve one; redirect to tickets, or 422/409/404 with message |
| GET/POST /conta/cadastro/ | anonymous | signup participant; invalid input no account |
| GET/POST /conta/entrar/ | anonymous | login; safe local return |
| POST /conta/sair/ | authenticated | invalidate session, redirect |
| GET /meus-ingressos/ | participant | only own, event/status/code |
| GET /gestao/eventos/ | organizer | own events only |
| GET/POST /gestao/eventos/novo/ | organizer | draft form/create |
| GET /gestao/eventos/<id>/ | owner | edit/publish/check-in/cancel/panel in one URL |
| POST /gestao/eventos/<id>/editar/ | owner | validate, edit or error |
| POST /gestao/eventos/<id>/publicar/ | owner | publish draft or no-op published |
| POST /gestao/eventos/<id>/entrada/ | owner | R10 message, redirect/re-render; exact precedence |
| POST /gestao/eventos/<id>/cancelar/ | owner | cancel published; terminal |

Anonymous GET protected -> login; anonymous protected POST -> 403 without mutation; public signup/login POST are exceptions; wrong role -> 403; missing/not-owned -> generic 404; invalid CSRF -> 403; no unauthorized mutation. UI status codes outside fixed partner API are design choices. A cancel page hides the edit/publish/check-in controls, shows `Evento cancelado`; direct POST cannot bypass guards. Use one snapshot for event/panel critical state.

## UI names and selectors
- Form labels Nome, E-mail, Senha; event Nome, Início, Local, Lotação, Preço; purchase Número do cartão; check-in Código do ingresso.
- Buttons Criar conta, Entrar, Sair, Criar evento, Salvar, Publicar, Comprar, Validar entrada, Cancelar evento.
- Ticket rows `ticket-list`, `ticket-status`, `ticket-code`; catalog `event-card`, `sold-out`; management `event-management`, `event-state`, `admission-result`, `metric-confirmed`, `metric-pending`, `metric-checkins`, `metric-available`, `metric-revenue`, `metric-refunded`.
- Exact labels and messages defined in PRD/transaction protocol. Render BRL `R$ 350,00`, decimal input accepts `100,00` or `100.00`, no thousands separators (document helper). Tests should capture actual UI, not only service return.

`event-management` identifica o contêiner autorizado da gestão; erros de criação não incluem esse contêiner. `metric-*` deve conter exclusivamente o valor textual (rótulo separado); `ticket-status` e `ticket-code` contêm valor de um ingresso por elemento. A página pós-compra mostra Meus ingressos diretamente, com a conta de teste recém-criada tendo um único ticket. Após recusar redução da lotação, reabrir gestão mostra valor persistido anterior. Em evento cancelado, o texto exato `Evento cancelado` aparece no lugar do campo. Estes detalhes tornam o probe browser reproduzível sem depender de aparência.
