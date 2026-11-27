# F04 | FDD: Livro de ingressos e liquidação simulada

Status: proposto · Wave W4 · Fonte normativa: PRD e design.

## Resultado e interfaces

Provides: Serviço reserve, resolve_due, consulta de ingresso, job persistente e regras transacionais de venda.

Consumes: F01: DB/worker/clock; F03: evento bloqueável e ocupação.

Ownership: ledger, worker. Não alterar módulos de outras features sem amendment.

## Low-level design

O ledger é único serviço autorizado para criar ingresso; adapters não fazem INSERT. `reserve(event_id, buyer, card_number)` aceita união discriminada WebBuyer(participant_id, email da sessão) ou PartnerBuyer(email). Entrada é validada antes de adquirir lock. No mesmo `transaction.atomic()`: bloquear evento; reavaliar published; contar ocupação em outra instrução; capturar preço; gerar código global de 12 caracteres alfanuméricos com CSPRNG e constraint UNIQUE; criar ticket pending + job. Erro de colisão usa atomic aninhado/savepoint e até 4 novas tentativas; só retry da constraint de código. Retorno DTO é snapshot pending pós-commit. Erro de commit não é sucesso. Não retry de POST em resultado ambíguo.

**Gateway:** classifica último grupo de 4 apenas em memória e descarta PAN; job guarda outcome, due_at, status, ticket FK única, processed_at. Delay determinístico 3s/34s no modo padrão, dentro das faixas; clock do DB depois do lock para agendar (não timestamp de início de transação). Worker descobre IDs vencidos sem lock, em lote limitado; cada job é transação própria, lock Event → Ticket → PaymentJob, sempre nessa ordem; consulta novamente due_at, estado e ticket. Se pending e published, aplica approved→confirmed ou declined; caso contrário marca ignored sem efeito. Jobs done/ignored são terminais. Dois workers podem selecionar mesmo job: segundo observa estado e sai. Processar por due_at, lote 32; espera idle 100ms, backoff limitado em falha; não processar job antes de vencer. Logs estruturados sem PAN, chave ou e-mail.

**Falha e recuperação:** crash antes do commit não cria metade da compra; crash após commit antes do retorno pode deixar compra válida (idempotência do POST não faz parte do brief). Crash de worker antes de commit mantém job disponível; depois do commit efeito único. Não usar fila em memória, sleep em request ou lock de job antes de event. Implementar teste de lock order e erro transitório (SQLSTATE 40P01/40001) com retry limitado somente de transação totalmente abortada. Se resultado incerto não repetir compra.

**Robustez:** A14 exige no mínimo duas rodadas; executar dez rodadas DB novas conforme TEST-A14, mais cap 1/2. A24 permanece duas rodadas HTTP independentes. Nenhuma rodada substitui outra.

**Handoff:** DTOs imutáveis, error enum, `reserve`, `read_ticket`, `list_participant_tickets`, `resolve_due`, helper de transição. F07 pode alterar tickets apenas dentro de event_guard, usando convenção e máquina de estados compartilhadas.

## Critérios e limites
| ID | Fase | Aceite |
| --- | --- | --- |
| A13 | local | Uma compra válida retorna ingresso pending com ID/código únicos e job gravado na mesma transação, sem aguardar gateway; reserva já ocupa vaga. |
| A14 | local | Quando lotação esgota, não cria ingresso/job; 30 reservas concorrentes sobre capacidade 5 dão exatamente 5 sucessos/25 sold_out, em duas rodadas novas. |
| A15 | local | Gateway padrão confirma 0001 e recusa 0002/outros em 2–5s; confirma 0003 e recusa 0004 em 30–40s; recusa libera uma vaga. |
| A16 | local | Snapshot de preço é capturado sob lock; finalize só altera pending de evento publicado; resultado duplicado/tardio não revive terminal; job sobrevive reinício. |
| A17 | local | Cartão diferente de 16 dígitos ASCII falha antes de criar ingresso; e-mail malformado na compra de parceiro falha; PAN não persiste nem aparece em logs. |
| A32 | local | Falha ao criar job reverte reserva; colisão de código usa savepoint e retry limitado; conflitos inesperados não viram sold_out. |
| A33 | local | Worker concorrente obedece event→ticket→job e revalida estado/vencimento; nenhuma espera de gateway ou lock global; transação abortada é retomável. |
| X04 | local | Worker do Compose consome job persistido após reinício sem chave real. |
| X05 | local | Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação. |

## Evolução e rollback
Mudança de contrato exige ADR/amendment aprovado e reavaliação de consumidores. Em falha de implementação, corrigir em commit novo; não alterar migrations aplicadas nem relatórios. No MVP local usar ambiente de testes descartável para rollback de schema; não apagar volume de demonstração.
