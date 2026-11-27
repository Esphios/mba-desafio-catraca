# F07 | FDD: Operação do evento e apuração

Status: proposto · Wave W5 · Fonte normativa: PRD e design.

## Resultado e interfaces

Provides: Ações de gestão, cancelamento atômico, check-in serializado, painel coerente com todos os estados e canais.

Consumes: F02: dono; F03: página/lock/estado; F04: ingressos, preço e job.

Ownership: operations, management partial. Não alterar módulos de outras features sem amendment.

## Low-level design

Operações de organizador compartilham a URL de gestão de F03. A view renderiza partial de métricas e ações; POST `/gestao/eventos/<id>/entrada/` e `/cancelar/` exigem Actor organizador, CSRF e ownership dentro da transação. Não basta esconder botão. Lock por evento primeiro. Check-in procura ticket pelo código e event_id, sem lock de outro evento; se inexistente ou outro, inválido. Depois checa cancelled, status confirmed, checked_in_at; se elegível grava timestamp único. UI em evento cancelado oculta campo e exibe Evento cancelado; POST direto mantém precedência do código.

**Cancelamento:** somente published→cancelled; atomicamente atualiza estado do evento, timestamps, todos confirmed→refunded e pending→cancelled. Declined permanece. Preservar checked_in_at para histórico; métrica check-ins conta apenas confirmed. Jobs pendentes podem continuar aguardando vencimento; worker os resolve como ignored. Nada de chamadas externas, sem varrer eventos alheios, sem retorno antes do commit. Repetir cancelamento retorna conflito genérico sem alterar dados.

**Painel:** single SQL/ORM statement que seleciona event.id, owner, state, capacity e agregados condicionais do mesmo snapshot. Uma consulta por página para campos críticos; não reutilizar evento de outra query para availability. Confirmados inclui utilizados, receita soma price_cents de confirmed, vagas 0 se cancelled; estornados count refunded. Não usar max(0, capacity−occupied): se negativo, sinalizar invariante violada e falhar gate. Sem contadores materializados.

**Integração:** F07 testa core com chamadas de ledger nas branches; X14/X15 só após merge das interfaces. API GET ticket deve continuar respondendo mesmo cancelado. Executar corridas em ambas as ordens (event lock controlado) para provar estados finais válidos.

## Critérios e limites
| ID | Fase | Aceite |
| --- | --- | --- |
| A25 | local | A decisão de check-in respeita a precedência R10 e somente um pedido concorrente pode marcar entrada; no evento cancelado, a página oculta o formulário, e POST direto mantém precedência. |
| A26 | local | Cancelar evento publicado é uma operação terminal; em até 10 s (baseline: no mesmo commit), pending passa a cancelled e confirmed a refunded; declined permanece; nenhuma resposta tardia reabre ingresso. Rejeitar edição e republicação por POST. |
| A27 | local | As seis métricas usam uma consulta coerente sobre evento e ingressos, sem contadores de canal; preço histórico apenas de confirmed. Cancelamento zera tudo exceto estornados. |
| A28 | local | Check-in, cancelar e painel ficam na URL de gestão de cada evento; todas as ações exigem dono inclusive requisição direta. |
| A35 | local | Leitura de gestão/painel usa snapshot único incluindo capacidade/status/owner e agregados; corridas de edição e cancelamento não produzem combinações impossíveis. |
| A36 | local | Corridas reserva/cancelamento, gateway/cancelamento e check-in/cancelamento terminam em estado serial válido, sem 5xx ou entrada após cancelamento. |
| X11 | local | Todas as ações operacionais respeitam guarda de dono. |
| X12 | local | Cancelamento bloqueia publicação/edição e integra gestão em URL existente. |
| X13 | local | Check-in/painel/cancelamento compartilham status, lock e preço; gateway tardio não revive. |
| X14 | integrated | Com UI e operações integradas, uma compra web confirmada incrementa painel, permite check-in e, após cancelamento, some do catálogo e vira estornada em Meus ingressos. |
| X15 | integrated | Com API e operações integradas, ingresso de parceiro conta na lotação e painel, permite check-in e consulta checkedIn; cancelar remove evento da lista, bloqueia POST, estorna e conserva consulta do ticket. |

## Evolução e rollback
Mudança de contrato exige ADR/amendment aprovado e reavaliação de consumidores. Em falha de implementação, corrigir em commit novo; não alterar migrations aplicadas nem relatórios. No MVP local usar ambiente de testes descartável para rollback de schema; não apagar volume de demonstração.
