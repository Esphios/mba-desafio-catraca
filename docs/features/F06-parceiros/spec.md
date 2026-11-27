# F06 | FDD: Integração comercial por API

Status: proposto · Wave W5 · Fonte normativa: PRD e design.

## Resultado e interfaces

Provides: As três rotas /api/partner, autenticação por chave, tradução de DTOs e erros do domínio.

Consumes: F03: catálogo público; F04: compra/consulta.

Ownership: partner API. Não alterar módulos de outras features sem amendment.

## Low-level design

As três rotas fixas não usam trailing slash. Middleware/guard de chave precede parse de corpo, validação de evento e capacidade. `X-Api-Key` é única credencial, comparada em tempo constante a valor local configurado; rejeitar ausente, duplicado ou inválido. Chave não vira sessão. JSON object com buyerEmail e cardNumber strings; `Content-Type: application/json` (parâmetro charset permitido); parse malformado, tipos errados ou cartão fora de 16 dígitos ASCII → 422. Campos extras ignorados, não conferem papel nem associação de conta. Para POST, chave → payload → existência/publicação → disponibilidade. Nenhuma falha esperada responde HTML/redirect. Tratar UUID malformado como evento/ticket inexistente, depois das validações anteriores.

**Serialização:** GET events retorna array de exatamente id/name/startsAt/priceCents/availableSeats; ISO 8601 com offset ou Z; inclui publicados lotados. POST 202 exatamente ticketId/code/status pending; GET ticket 200 exatamente ticketId/code/eventId/status/checkedIn (booleano); consulta de qualquer canal sem buyerEmail/valor. API de parceiro pode consultar ticket web mesmo se não vendeu; é regra explícita.

**Segurança:** isentar CSRF só do namespace da API sem autenticação por cookie; não aplicar CSRF exemption a web; nunca logar body/chave. Body cap de 16 KiB (16.384 bytes) no adapter, após autenticação; exceder retorna 422 invalid_request, inclusive evento ausente ou lotado; limitar leitura a cap+1, sem parse do excedente, erros internos 500 genérico (não mascarar como sold_out).

**Testes:** contrato OpenAPI em `docs/interfaces/partner.openapi.json`; JSON exato, precedência cruzada, duas rodadas HTTP reais 30/5 e carga mista no integrado; client sem seguir redirect. Não assumir status terminal antes do gateway. F06 não precisa F05 para verificar leitura de fixture web; X16 exige compra web real.

## Critérios e limites
| ID | Fase | Aceite |
| --- | --- | --- |
| A21 | local | GET events com chave retorna array de publicados, id/name/startsAt/priceCents/availableSeats com tipos exatos; cancelados/drafts excluídos. |
| A22 | local | POST compra responde 202 com ticketId/code/status pending; após chave, precedência 422 invalid_request, 404 event_not_available, 409 sold_out. |
| A23 | local | GET ticket consulta ambos os canais e retorna ticketId/code/eventId/status/checkedIn booleano; desconhecido 404 ticket_not_found; todas as rotas sem chave ou chave errada 401 unauthorized. |
| A24 | local | Em duas rodadas HTTP reais, cada evento novo de capacidade 5 recebe 30 POST simultâneos com cartão 0001: 5×202 e 25×409, sem 5xx; depois 5 confirmados. |
| A34 | local | Autorização antecede leitura/parse do corpo; JSON inválido, null, array, tipo errado, cartão Unicode e e-mail inválido respondem 422 após chave válida; precedência vale em eventos ausentes e esgotados. |
| X09 | local | A listagem de parceiros reflete publicação, preço e capacidade de F03; fixtures draft/cancelled ficam fora. Cancelamento real será validado em X15. |
| X10 | local | API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture. |
| X16 | integrated | Integração final: canais disputam mesma última vaga; consulta partner aceita ticket web e compra partner não entra em conta web. |

## Evolução e rollback
Mudança de contrato exige ADR/amendment aprovado e reavaliação de consumidores. Em falha de implementação, corrigir em commit novo; não alterar migrations aplicadas nem relatórios. No MVP local usar ambiente de testes descartável para rollback de schema; não apagar volume de demonstração.
