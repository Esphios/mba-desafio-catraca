# F06 | FDD: API pública de parceiros

Status: planejado. Wave W5. Fonte: PRD e HLD; ADRs propostos. Este FDD não atesta código existente.

## Objetivo, provides e consumes
As três rotas /api/partner, autenticação por chave, tradução de DTOs e erros do domínio.

F03: catálogo público; F04: compra/consulta.

## Limites de escrita
partner/, tests/partner; no modifications to ledger or catalog.

## Design detalhado
`partner/` owns fixed no-trailing-slash routes with string path params, exact key guard before parsing and resource lookup. No redirects from canonical URL. Validate JSON object, required fields and card/email before calling reserve; map errors exact. Content type application/json required for purchase. Do not serialize extra fields or secret; use safe JSON error responses. GET events uses catalog DTO, converts ISO timestamp and cents; GET ticket permits both channels. Concurrency runner uses real HTTP and distinct requests. No Django CSRF exemption beyond key-authenticated routes. Handle malformed IDs as unavailable/not found after key and payload validation. Do not add authentication requirement not in fixed contract.

## Dependências e integração
F03, F04. Consumir interfaces do HLD, não importar views de outras features. Em caso de interface insuficiente, registrar bloqueio e pedir amendment; não criar cópia de regra. Contratos externos e códigos do brief têm precedência. Dependências cross-feature: X09, X10; ver contrato.

## Critérios locais e casos de falha
- A21 (API,R02,R05): GET events com chave retorna array de publicados, id/name/startsAt/priceCents/availableSeats com tipos exatos; cancelados/drafts excluídos.
- A22 (API,R06,R07): POST compra responde 202 com ticketId/code/status pending; após chave, precedência 422 invalid_request, 404 event_not_available, 409 sold_out.
- A23 (API,R09,R13): GET ticket consulta ambos os canais e retorna ticketId/code/eventId/status/checkedIn booleano; desconhecido 404 ticket_not_found; todas as rotas sem chave ou chave errada 401 unauthorized.
- A24 (R07,API): Em duas rodadas HTTP reais, cada evento novo de capacidade 5 recebe 30 POST simultâneos com cartão 0001: 5×202 e 25×409, sem 5xx; depois 5 confirmados.

## Testabilidade e segurança
Usar fixtures mínimas isoladas; relógio injetável para lógica, modo padrão para prazo real. Validar entradas e falhas além de happy path. Nenhum dado real, nenhuma modificação de contrato para mascarar falha. Evidência independente no contrato.

## Rollback e evolução
Em falha, manter branch sem merge e corrigir com novo commit. Mudanças de schema após F01 exigem migração revisada, teste fresh/upgrade e coordenação. Não desfazer migração de dados em ambiente de usuário sem backup; neste MVP usar ambiente descartável de teste. Regressão final obrigatória após última integração.
