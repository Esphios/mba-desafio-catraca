# F07 | FDD: Operação de evento: check-in, cancelamento e painel

Status: planejado. Wave W5. Fonte: PRD e HLD; ADRs propostos. Este FDD não atesta código existente.

## Objetivo, provides e consumes
Ações de gestão, cancelamento atômico, check-in serializado, painel coerente com todos os estados e canais.

F02: dono; F03: página/lock/estado; F04: ingressos, preço e job.

## Limites de escrita
operations/, templates/operations/, tests/operations; consume F03 template include, do not edit shared shell unless integration coordinator approves.

## Design detalhado
`operations/` owns management extension. Check-in loads actor event with lock, lookup code and test R10 order; timestamp only on success, preserve status. Cancel uses same lock and one atomic update of event and pending/confirmed tickets, preserves history and job queued; repeated attempt no new effect. Panel uses one aggregate query with status-filtered counts and sum of snapshots; avoid join multiplication, show zero and BRL format. Page uses F03 extension include; POSTs verify owner and CSRF. The cancellation fixture can use core reserve without API/F05 when evaluated on isolated branch; full UI/API cross-channel proofs must be run after W5 merge. Test real late gateway and concurrency; cancelled UI hides field with message; direct POST still follows R10 precedence. Never add second state source.

## Dependências e integração
F02, F03, F04. Consumir interfaces do HLD, não importar views de outras features. Em caso de interface insuficiente, registrar bloqueio e pedir amendment; não criar cópia de regra. Contratos externos e códigos do brief têm precedência. Dependências cross-feature: X11, X12, X13; ver contrato.

## Critérios locais e casos de falha
- A25 (R10): Check-in aplica exatamente as cinco mensagens na ordem definida; só confirmed não utilizado recebe checkedIn=true; dois check-ins concorrentes liberam uma entrada.
- A26 (R11): Cancelar publicado é irreversível; na mesma transação confirmed→refunded e pending→cancelled, sem alteração de declined; gateway posterior não modifica; edit/publish/compra rejeitados.
- A27 (R05,R12): Painel mostra seis métricas com snapshots de preço e ambos os canais; check-ins somente confirmed; cancelado tem receita/vagas/confirmados/pendentes/check-ins zero.
- A28 (R04,R13): Check-in, cancelar e painel ficam na URL de gestão de cada evento; todas as ações exigem dono inclusive requisição direta.

## Testabilidade e segurança
Usar fixtures mínimas isoladas; relógio injetável para lógica, modo padrão para prazo real. Validar entradas e falhas além de happy path. Nenhum dado real, nenhuma modificação de contrato para mascarar falha. Evidência independente no contrato.

## Rollback e evolução
Em falha, manter branch sem merge e corrigir com novo commit. Mudanças de schema após F01 exigem migração revisada, teste fresh/upgrade e coordenação. Não desfazer migração de dados em ambiente de usuário sem backup; neste MVP usar ambiente descartável de teste. Regressão final obrigatória após última integração.
