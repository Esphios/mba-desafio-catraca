# F03 | FDD: Administração e catálogo de eventos

Status: proposto · Wave W3 · Fonte normativa: PRD e design.

## Resultado e interfaces

Provides: CRUD limitado de evento, publicação, página de gestão /gestao/eventos/<id>/, consulta pública, lock e leitura canônica de ocupação.

Consumes: F01: schema e clock; F02: identidade e autorização.

Ownership: catalog, organizer event views. Não alterar módulos de outras features sem amendment.

## Low-level design

O domínio de catálogo é o ponto de entrada para criação/edição/publicação e consultas. O modelo `Event` tem ID UUID, owner_id imutável, status, nome/local, starts_at, capacity e price_cents. Parser de moeda usa Decimal; não arredondar silenciosamente terceira casa. Em criação e edição, validar instante UTC estritamente futuro; na edição fazê-lo após lock. Nome e local trim e não vazios. Capacidade >=1 e <=2^31−1; preço positivo em centavos <=2^63−1, com validação de limite da API interoperável (até 2^53−1 centavos, decisão W0). IDs públicos são strings UUID.

**Transações:** `event_guard` abre atomic, seleciona linha por ID/owner e adquire lock; consulta de ocupação em instrução subsequente. Edição usa pending+confirmed; preço/lotação alterados juntos. Publicação draft→published, published→published é no-op, cancelled rejeita. Consulta pública usa uma query com subquery/aggregate e filtro published; sem cache. Publicado no passado não é automaticamente removido (brief não define fechamento).

**UI:** `/gestao/eventos/`, `/gestao/eventos/novo/`, `/gestao/eventos/<id>/`, POST `/editar/`, `/publicar/` sob mesma URL base. F03 cria layout e slot de operações via partial que F07 possui; não usar stub que retorna aprovação. F07 substitui partial; registro de URL central com includes isolados aprovado antes da wave paralela.

**Handoff:** DTO `PublicEvent`, `EventEdit`, `event_guard`, `occupied_count`, `catalog` e `basic_management_snapshot` (F03, provider inicial sem métricas; F07 fornece `management_snapshot`). Fixtures de tickets podem existir para teste de redução, mas não atestam compra real.

## Critérios e limites
| ID | Fase | Aceite |
| --- | --- | --- |
| A09 | local | Nome/local não vazios; lotação inteira >=1; preço em centavos >0; início estritamente futuro em criar e editar, inclusive requisição direta. |
| A10 | local | Evento nasce draft; publicar torna visível a consulta pública; gestão tem URL estável e lista apenas próprios eventos. |
| A11 | local | Editar sob lock do evento; capacidade abaixo de pending+confirmed é rejeitada; igual/acima aceita; preço novo não altera snapshot de ingressos. |
| A12 | local | Evento cancelled não pode ser alterado/republicado; catálogo e disponibilidade pública o excluem. |
| A31 | local | Edição revalida a data no instante da escrita e não aceita frações de vaga, centavos fracionários ou valores fora dos limites documentados; nenhuma escrita parcial. |
| X02 | local | Migração e clock da fundação permitem criação e rejeição de data vencida. |
| X03 | local | URL de gestão e listagem usam dono da sessão; B não pode editar/publicar A. |

## Evolução e rollback
Mudança de contrato exige ADR/amendment aprovado e reavaliação de consumidores. Em falha de implementação, corrigir em commit novo; não alterar migrations aplicadas nem relatórios. No MVP local usar ambiente de testes descartável para rollback de schema; não apagar volume de demonstração.
