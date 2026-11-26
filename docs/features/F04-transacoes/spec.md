# F04 | FDD: Compra e processamento de pagamento

Status: planejado. Wave W4. Fonte: PRD e HLD; ADRs propostos. Este FDD não atesta código existente.

## Objetivo, provides e consumes
Serviço reserve, finalize_payment, consulta de ingresso, job persistente e regras transacionais de venda.

F01: DB/worker/clock; F03: evento bloqueável e ocupação.

## Limites de escrita
ledger/, worker command implementation, ledger tests; no edits to consumer modules. Coordinate F01 skeleton replacement only.

## Design detalhado
`ledger/` owns reservation and payment job resolution. Shared schema from F01, lock from F03. The same reserve entrypoint accepts typed Buyer web/partner; validate before transaction, map domain errors; web actor validated by F05. Store ticket and job together, snapshot cents, retry unique code collision in savepoint. Worker uses stable outcome/due_at, polls ~100ms, lock event first and recheck job and ticket before state change. No raw PAN saved. Query by participant id and ticket id, including event name. Expose immutable DTO and test fixtures; no public HTTP or web purchase route yet. Test default 3s/35s in real worker and injected clock for exhaustive branch tests. Implement atomic rollback and stress tests with separate DB connections.

## Dependências e integração
F01, F03. Consumir interfaces do HLD, não importar views de outras features. Em caso de interface insuficiente, registrar bloqueio e pedir amendment; não criar cópia de regra. Contratos externos e códigos do brief têm precedência. Dependências cross-feature: X04, X05; ver contrato.

## Critérios locais e casos de falha
- A13 (R05,R06,R09): Uma compra válida retorna ingresso pending com ID/código únicos e job gravado na mesma transação, sem aguardar gateway; reserva já ocupa vaga.
- A14 (R07): Quando lotação esgota, não cria ingresso/job; 30 reservas concorrentes sobre capacidade 5 dão exatamente 5 sucessos/25 sold_out, em duas rodadas novas.
- A15 (R08): Gateway padrão confirma 0001 e recusa 0002/outros em 2–5s; confirma 0003 e recusa 0004 em 30–40s; recusa libera uma vaga.
- A16 (R03,R11): Snapshot de preço é capturado sob lock; finalize só altera pending de evento publicado; resultado duplicado/tardio não revive terminal; job sobrevive reinício.
- A17 (R06): Cartão diferente de 16 dígitos ASCII falha antes de criar ingresso; e-mail malformado na compra de parceiro falha; PAN não persiste nem aparece em logs.

## Testabilidade e segurança
Usar fixtures mínimas isoladas; relógio injetável para lógica, modo padrão para prazo real. Validar entradas e falhas além de happy path. Nenhum dado real, nenhuma modificação de contrato para mascarar falha. Evidência independente no contrato.

## Rollback e evolução
Em falha, manter branch sem merge e corrigir com novo commit. Mudanças de schema após F01 exigem migração revisada, teste fresh/upgrade e coordenação. Não desfazer migração de dados em ambiente de usuário sem backup; neste MVP usar ambiente descartável de teste. Regressão final obrigatória após última integração.
