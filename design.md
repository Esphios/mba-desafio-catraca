# Design | HLD do Catraca

Estado: proposto. FDDs em `docs/features/`; este HLD define interfaces e invariantes comuns. A matriz de requisitos indica quem testa cada decisão.

## 1. Contexto, qualidade e fronteiras

Produto local multiusuário, sem serviço externo real. Web HTML server-rendered e JSON de parceiros no mesmo serviço HTTP. Aplicação modular Django; banco PostgreSQL único, worker executa o simulador via tabela de jobs. Navegador não escreve banco diretamente. Chave de parceiro não é sessão; sessão web não substitui chave. Sem cache de vagas ou contagens. O tempo de relógio deve vir de clock injetável em testes e timezone-aware no produto.

| Componente | Responsabilidade | Não faz |
|---|---|---|
| identity | contas, sessões, papéis, guarda de acesso | venda, cálculo de vaga |
| catalog | evento, publicação, gestão base, catálogo, lock e consulta de ocupação | criar ticket |
| ledger | reserva, código, job e resolução de pagamento | montar HTML ou HTTP |
| storefront | páginas públicas e participante, adaptador de compra | calcular vagas isoladamente |
| partner | autenticar chave e mapear contrato JSON | criar ticket direto pelo ORM |
| operations | check-in, cancelamento, métricas, formulários de gestão | duplicar reserva ou gateway |
| platform | configuração, schema e migrações, health, runner | inventar regras de negócio |

## 2. Stack proposta

Python 3.12, Django 5.2 LTS, psycopg 3, PostgreSQL 17, Gunicorn com 4 workers gthread × 8 threads (32 requests simultâneas, ajustar se medição exigir), templates Django, CSS simples, pytest-django ou runner Django (preferência: runner Django + unittest), Playwright em container para browser, Ruff para lint, Node apenas opcional para validação local. Compose v2. Fixar versões de patch, imagens e dependências verificadas na F01, com lockfile/hash e suporte Linux/macOS arm64/amd64. Não impor Python/Playwright ao host. Banco e worker não expõem porta externa. Apenas 127.0.0.1:8080. Não usar runserver na carga concorrente. Não há escolha de versão patch inventada neste documento.

## 3. Modelo persistente

| Tabela lógica | Campos/constraints |
|---|---|
| account | id UUID PK; name; email normalizado unique; password hash Django; role participant/organizer; ativo; timestamps. Custom User desde migração inicial. |
| event | id UUID PK; owner_id FK account PROTECT; name/location; starts_at timestamptz; capacity integer CHECK >=1; price_cents bigint CHECK >0; state draft/published/cancelled CHECK; cancelled_at nullable; created/updated_at. |
| ticket | id UUID PK; event_id FK PROTECT; participant_id FK nullable; buyer_email; channel web/partner; code unique global (8 caracteres alfanuméricos maiúsculos com CSPRNG); status CHECK enum; price_cents bigint positivo; checked_in_at nullable; created_at, status_changed_at. CHECK: web exige participante, partner exige null; não exigir checked_in_at null em refunded. |
| payment_job | ticket_id unique FK PROTECT; outcome approved/declined; due_at timestamptz; state queued/done/ignored; completed_at; created_at. Nenhum PAN, CVV ou cartão parcial armazenado. |
| django_session | sessão padrão server-side; expiração, rotação e invalidação via Django. |

Índices: event(owner_id,state), event(state,starts_at), ticket(event_id,status), ticket(participant_id,created_at), payment_job(state,due_at). Código unique global, reintentar colisão via savepoint (máximo 5) sem quebrar atomicidade. Usar bigint e Decimal para conversão reais→centavos; rejeitar >2 casas, limites de representação inválidos, bool e floats ambiguamente arredondados. A capacidade não será mantida em contador duplicado. Horário futuro é validação de comando, não CHECK baseado em now(). Sem exclusão física de evento/ticket no MVP.

## 4. Máquinas de estado

Evento: draft → published → cancelled. Cancelled terminal; published pode ser editado se início informado futuro e lotação válida. Repetir publicação de published é no-op/erro de domínio sem efeito; cancelar só published, repetição retorna estado terminal/erro sem nova transição. Nenhuma reversão de cancelled. Não inventar estado de evento expirado.

| Ticket API | Rótulo UI | Ocupa? | Transições permitidas |
|---|---|---|---|
| pending | pendente | sim | confirmed, declined, cancelled |
| confirmed | confirmado | sim | refunded |
| declined | recusado | não | nenhuma |
| cancelled | cancelado | não | nenhuma |
| refunded | estornado | não | nenhuma |

`checkedIn` é booleano derivado de `checked_in_at != null`, independente de status; estorno preserva histórico de entrada, mas painel ignora check-ins não confirmed. Código sempre consultável; parceiro pode consultar todo ticket com a chave. Ticket web é associado ao ID autenticado, jamais por igualdade de e-mail. Partner não cria ou vincula conta.

## 5. Interfaces internas (congelar antes de W5)

Python, assinaturas ilustrativas, não código implementado. DTOs imutáveis; erros tipados e adaptados no limite HTTP. Definir tipos reais em módulos indicados; mudanças de contrato exigem ADR ou amendment, revisão de consumidores e tests.

| Provedor / módulo | Operação / resultado |
|---|---|
| identity/access.py | `require_participant(request) -> Account`; `require_organizer(request) -> Account`; `require_owner(actor,event) -> None` (404 para outro dono) |
| catalog/services.py | `create_event(actor, fields) -> EventDTO`; `edit_event(actor,id,fields)`; `publish_event(actor,id)`; `get_owned_event(actor,id)` |
| catalog/queries.py | `public_events() -> list[EventSaleDTO]`; `public_event(id)`; `occupied(event_id) -> int`; `available(event, occupied) -> int` |
| catalog/locking.py | `locked_event(event_id) -> Event` exige transaction.atomic ativa, lock exclusivo e objeto atualizado; não abre/fecha transação do chamador |
| ledger/services.py | `reserve(event_id, buyer, card_number) -> TicketDTO` (validar entrada, depois estado, depois vaga); `finalize_payment(ticket_id)`; `find_ticket(id)`; `participant_tickets(participant_id)` |
| operations/services.py | `check_in(actor,event_id,code) -> CheckInResult`; `cancel_event(actor,event_id) -> EventDTO`; `dashboard(actor,event_id) -> DashboardDTO` |

EventSaleDTO: id, name, starts_at, location, price_cents, available_seats; TicketDTO: id, code, event_id, status, checked_in, price_cents, participant_id, event_name; Buyer: channel, email, participant_id nullable; DashboardDTO: confirmed, pending, checkins, available, revenue_cents, refunded. Nenhum DTO externo recebe senha, PAN, dados de terceiros ou detalhes do job. Erros: InvalidRequest, EventNotAvailable, SoldOut, TicketNotFound, Forbidden/NotFound, InvalidTransition, ValidationError. Request validation deve preservar precedência externa. Passar ator explícito a operações privadas; não confiar em owner_id enviado.

## 6. Protocolo de concorrência e pagamento

Detalhamento normativo em `docs/architecture/transactions.md`. Cada operação que modifica evento, estado de ticket ou check-in adquire primeiro lock do evento em transação curta. Isolamento READ COMMITTED; contagem após lock em segunda consulta SQL. Ordem de lock event → ticket(s) → job(s). Nenhum sleep/rede enquanto segura lock. Operações distintas podem ocorrer em eventos distintos. Vitrine/API são consultas derivadas; a reserva sempre revalida sob lock. Cancelamento é transação única com status do evento e transições dos ingressos, de modo que os prazos do brief são satisfeitos sem fila de reembolso. Jobs que chegam depois são ignorados e finalizados sem reescrever estado terminal.

## 7. Contrato de parceiro (fixo do brief)

Autenticar primeiro em todas as rotas com `X-Api-Key`, comparar em tempo constante; falta/inválida → 401 `{"error":"unauthorized"}`. JSON UTF-8, sem redirects em rotas válidas. Todas as IDs string. `GET /api/partner/events` → 200 array de objetos `{id,name,startsAt,priceCents,availableSeats}`; ISO 8601 com offset/Z; número inteiro para centavos/vagas. Inclui publicado esgotado (0). Não inclui draft/cancelled.

`POST /api/partner/events/{eventId}/purchases`, JSON `{"buyerEmail":"comprador@example.com","cardNumber":"4000000000000001"}` → 202 `{"ticketId":"<uuid>","code":"<codigo>","status":"pending"}`. Exigir e-mail válido e cartão string de 16 dígitos ASCII; JSON inválido/campos ausentes/tipos inválidos → 422 `{"error":"invalid_request"}` mesmo que evento inexistente ou esgotado. Depois, evento inexistente/draft/cancelled → 404 `{"error":"event_not_available"}`; depois, sem vaga → 409 `{"error":"sold_out"}`. Não tratar UUID malformado como 500: mapear ao erro de recurso inexistente após validar corpo. Evitar rota Django com conversor UUID que retorna 404 antes da chave/validação; capturar segmento string. CSRF dispensado apenas nessas rotas autenticadas por chave, não no restante.

`GET /api/partner/tickets/{ticketId}` → 200 `{"ticketId":"<uuid>","code":"<codigo>","eventId":"<uuid>","status":"confirmed","checkedIn":false}` (status qualquer dos cinco). Desconhecido → 404 `{"error":"ticket_not_found"}`. Sem campos adicionais nos DTOs fixos. Sem HTML em erros contratados. A documentação OpenAPI futura poderá derivar desta tabela; não alterar URLs/JSON.

## 8. UX e rotas web

| Método / rota proposta | Permissão e efeito |
|---|---|
| GET / | pública; vitrine com nome/data/local/preço, vagas e esgotado |
| GET/POST /signup/ | pública, somente participant; form nome/email/senha |
| GET/POST /login/ | autenticação; redirect por papel |
| POST /logout/ | sessão; CSRF e invalidação |
| GET /events/{id}/ | pública se à venda; detalhes e compra unitária |
| POST /events/{id}/purchase/ | participant; cartão; sucesso redireciona Meus ingressos (303), erro sem ticket |
| GET /my-tickets/ | participant; evento, status em português, código; reload suficiente |
| GET /organizer/events/ | organizer; somente próprios eventos |
| GET/POST /organizer/events/new/ | organizer; criar draft e redirect gestão |
| GET /organizer/events/{id}/ | owner; detalhes e seções de edição, publicação, cancelamento, check-in, painel |
| POST /organizer/events/{id}/edit/ | owner; validação e lock |
| POST /organizer/events/{id}/publish/ | owner; transição |
| POST /organizer/events/{id}/cancel/ | owner; ação irrevogável com confirmação visual |
| POST /organizer/events/{id}/check-in/ | owner; mensagem exata, redirect para gestão ou render |

Layout mínimo sem SPA; labels acessíveis, inputs de data e hora, lotação, preço, senha e cartão. Não oferecer link de gestão de outro usuário. Renderizar estado de venda atualizado a cada GET. Página de gestão deve manter URL estável; F03 cria template base com slots independentes `ops_actions`, `checkin`, `metrics` ou include `operations/panel.html` placeholder sob ownership F07 (reservar um ponto único sem edição por F05/F06). Em cancelado, exibir painel e mensagem "Evento cancelado" no lugar do campo, ocultar edição/publicação; servidor rejeita POST mesmo escondido.

## 9. Check-in e painel

Após autenticação e dono, dentro de lock do evento, procurar código por igualdade exata normalizada (trim e uppercase, escolha local). A ordem de R10 é obrigatória:

1. Inexistente ou de outro evento: `Ingresso inválido para este evento`.
2. Evento cancelado: `Evento cancelado`.
3. Status diferente de confirmed: `Ingresso não confirmado`.
4. checked_in_at já preenchido: `Ingresso já utilizado`.
5. Preencher checked_in_at e retornar `Entrada liberada`.

Nunca confundir check-in com status. A consulta do painel usa uma única instrução SQL de agregação filtrada, unida ao evento para snapshot coerente. `confirmed=COUNT(status=confirmed)`, `pending=COUNT(pending)`, `checkins=COUNT(confirmed AND checked_in_at IS NOT NULL)`, `available=0 se cancelled senão capacity-confirmed-pending`, `revenue_cents=COALESCE(SUM(price_cents WHERE confirmed),0)`, `refunded=COUNT(refunded)`. Exibir rótulos Confirmados, Pendentes, Check-ins, Vagas disponíveis, Receita, Estornados. Valor BRL com 2 decimais. Sem agregação global de outros eventos.

## 10. Deployment e falhas

Compose: postgres saudável → migrate-seed one-shot → web e worker; `up` espera readiness incluindo worker ativo (heartbeat no DB ou probe equivalente), `down` remove containers e redes do projeto, conserva volume; gates com projeto e volume separados e cleanup em trap. Logs estruturados com IDs de evento/ticket, operação e latência, sem payload sensível. Falha transacional retorna erro sem sucesso fictício. Worker busca jobs vencidos sem bloquear evento antes da hora, revalida e finaliza transacionalmente; reinício reprocessa jobs queued. Não marcar done antes do commit. Monitorar atraso real; nenhuma garantia de prazo sob desligamento ou infraestrutura indisponível, mas recuperar após reinício.

## 11. Verificação e evolução

ADRs e diagrama vinculados a este HLD. Manter cada implementação, teste, doc e contrato na mesma mudança. A regra mais restritiva prevalece: brief → PRD/contrato externo → HLD/ADR aprovados → FDD/plano → código. Divergência bloqueia merge e exige resolução explícita. Ver `requirements-matrix.md`, `docs/validation/`, `tasks.md`.
