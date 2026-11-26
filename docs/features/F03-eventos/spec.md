# F03 | FDD: Ciclo de publicação e catálogo

Status: planejado. Wave W3. Fonte: PRD e HLD; ADRs propostos. Este FDD não atesta código existente.

## Objetivo, provides e consumes
CRUD limitado de evento, publicação, página de gestão /organizer/events/{id}/, consulta pública, lock e leitura canônica de ocupação.

F01: schema e clock; F02: identidade e autorização.

## Limites de escrita
catalog/, catalog templates, tests; only F03 owns management shell. Shared DTO interface changes via ADR.

## Design detalhado
`catalog/` owns event lifecycle and query DTO. Use form Decimal parse for price, timezone-aware starts_at, capacity integer; reject past/now both create and edit. Use event lock for edit/publish; count pending/confirmed by second query after lock. Public list only state published; include 0 seats; use one aggregate query. Create own events from actor ID not form field. Management route shows edit/publish, placeholder include `operations/panel.html` with empty fallback owned by F07; no business operation implemented here. Provide typed locked_event, occupied and available to F04. Test using direct ticket fixtures only to emulate ledger state, not as real purchases.

## Dependências e integração
F01, F02. Consumir interfaces do HLD, não importar views de outras features. Em caso de interface insuficiente, registrar bloqueio e pedir amendment; não criar cópia de regra. Contratos externos e códigos do brief têm precedência. Dependências cross-feature: X02, X03; ver contrato.

## Critérios locais e casos de falha
- A09 (R01): Nome/local não vazios; lotação inteira >=1; preço em centavos >0; início estritamente futuro em criar e editar, inclusive requisição direta.
- A10 (R02,R04): Evento nasce draft; publicar torna visível a consulta pública; gestão tem URL estável e lista apenas próprios eventos.
- A11 (R03,R05): Editar sob lock do evento; capacidade abaixo de pending+confirmed é rejeitada; igual/acima aceita; preço novo não altera snapshot de ingressos.
- A12 (R11): Evento cancelled não pode ser alterado/republicado; catálogo e disponibilidade pública o excluem.

## Testabilidade e segurança
Usar fixtures mínimas isoladas; relógio injetável para lógica, modo padrão para prazo real. Validar entradas e falhas além de happy path. Nenhum dado real, nenhuma modificação de contrato para mascarar falha. Evidência independente no contrato.

## Rollback e evolução
Em falha, manter branch sem merge e corrigir com novo commit. Mudanças de schema após F01 exigem migração revisada, teste fresh/upgrade e coordenação. Não desfazer migração de dados em ambiente de usuário sem backup; neste MVP usar ambiente descartável de teste. Regressão final obrigatória após última integração.
