# F06 | Contrato de avaliação

Versão 2 proposta. Ambiente: checkout limpo do SHA, Docker/Compose e Git; `bash bin/up` e `bash bin/gates --feature F06` após implementados. Banco PostgreSQL real, dados sintéticos, projeto/porta exclusivos, gateway padrão para itens de tempo. O avaliador cria relatório novo sem alterar código.

## Fase LOCAL (antes do merge)

### C-F06-A21 (A21)

Preparação: Eventos draft, published, lotado e cancelled; chave válida.

Procedimento: GET /api/partner/events; validar cada item contra o schema OpenAPI, inclusive UUID, timestamp e limites numéricos.

PASS somente se: 200 array conforme OpenAPI; publicados inclusive esgotados; sem dados de owner/PII; disponibilidade derivada.

Teste: `TEST-A21`. Evidência: HTTP GET com fixtures dos estados; validar cada item contra o OpenAPI, inclusive UUID/timestamp/limites; esgotado permanece com 0.

### C-F06-A22 (A22)

Preparação: E disponível, draft, inexistente, esgotado, cancelado fixture.

Procedimento: POST válido; em seguida combinar erro de chave, payload inválido, evento indisponível e falta de vaga.

PASS somente se: 202 pending exato; 401→422→404→409 na precedência; erros sem efeitos.

Teste: `TEST-A22`. Evidência: Tabela HTTP: JSON inválido e evento inexistente ->422; inválido e esgotado ->422; válido draft/cancelled/inexistente ->404; lotado ->409; válido ->202.

### C-F06-A23 (A23)

Preparação: Ticket web fixture e parceiro; ID inexistente; chaves válidas e inválidas.

Procedimento: GET ambos os tickets, ID UUID ausente e UUID malformado; validar respostas 200 contra OpenAPI; executar as três rotas sem chave e com chave inválida.

PASS somente se: 200 com IDs UUID, código ^[A-Z0-9]{12}$ e demais campos exatos; ausente/malformado dá 404 ticket_not_found; 401 unauthorized em 6 combinações.

Teste: `TEST-A23`. Evidência: HTTP em três rotas × sem/errada; consultar fixtures web/partner, UUID inexistente e malformado; validar respostas 200 contra OpenAPI.

### C-F06-A24 (A24)

Preparação: Dois eventos novos, cap 5, preço 1000, gateway padrão, web concorrente.

Procedimento: Disparar 30 POSTs com final 0001 por evento usando barreira; verificar payloads, cinco IDs/códigos únicos, disponibilidade e confirmações até 10s.

PASS somente se: Por rodada 5×202, 25×409 sold_out, nenhum outro status; cinco confirmed e 0 vagas.

Teste: `TEST-A24`. Evidência: Runner HTTP com barreira, 30 conexões, validar corpo e IDs únicos, consultar cada aceito e availableSeats=0; usar novo evento por rodada.

### C-F06-A34 (A34)

Preparação: Chave válida/errada, evento ausente e esgotado.

Procedimento: Enviar chave ausente/duplicada/errada com body sentinela; com chave válida enviar JSON válido de exatamente 16.384 bytes, o mesmo com 16.385 bytes, JSON truncado/null/array, e-mail canônico inválido/>254, cartão Unicode/numérico e content-type incorreto.

PASS somente se: 401 sem ler/parsear body para chave ausente/duplicada/errada; 16.384 bytes alcança o domínio; 16.385 bytes e payload inválido autenticado dão 422 mesmo com evento inexistente/lotado; sem efeito, redirect ou 500.

Teste: `TEST-A34`. Evidência: HTTP bruto registrando multiplicidade da chave e bytes efetivamente lidos para 16.384/16.385; conferir resposta exata, ordem das guardas e ausência de efeitos.

### C-F06-X09 (X09)

Preparação: Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.

Procedimento: GET antes/depois publicação, edição e cancelamento fixture.

PASS somente se: A listagem de parceiros reflete publicação, preço e capacidade de F03; fixtures draft/cancelled ficam fora. Cancelamento real será validado em X15.

Teste: `TEST-X09`. Evidência: GET antes/depois publicação, edição e cancelamento fixture.

### C-F06-X10 (X10)

Preparação: Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.

Procedimento: POST simultâneo e GET ticket, comparar dados de ledger.

PASS somente se: API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture.

Teste: `TEST-X10`. Evidência: POST simultâneo e GET ticket, comparar dados de ledger.

## Fase INTEGRATED (após merge da wave)

Itens desta fase são explicitamente PENDING_INTEGRATION no relatório local; não contar como PASS e não exigir feature irmã no checkout isolado. Relatório integrado deve incluir todos os itens anteriores e os seguintes, sem pendências.

### C-F06-X16 (X16)

Preparação: Checkout integrado contendo ambas as features; realizar ações reais via UI/API, sem editar DB.

Procedimento: Corrida web e API com capacidade 1; um sucesso, outro esgotado; testar isolamento pelo e-mail.

PASS somente se: Integração final: canais disputam mesma última vaga; consulta partner aceita ticket web e compra partner não entra em conta web.

Teste: `TEST-X16`. Evidência: Corrida web e API com capacidade 1; um sucesso, outro esgotado; testar isolamento pelo e-mail.

## Mapeamento explícito

| Critério | Item      | Teste    | Fase       |
| -------- | --------- | -------- | ---------- |
| A21      | C-F06-A21 | TEST-A21 | local      |
| A22      | C-F06-A22 | TEST-A22 | local      |
| A23      | C-F06-A23 | TEST-A23 | local      |
| A24      | C-F06-A24 | TEST-A24 | local      |
| A34      | C-F06-A34 | TEST-A34 | local      |
| X09      | C-F06-X09 | TEST-X09 | local      |
| X10      | C-F06-X10 | TEST-X10 | local      |
| X16      | C-F06-X16 | TEST-X16 | integrated |

Qualquer item aplicável sem evidência = FAIL. Fixture deve ser declarada; não usar fixture para substituir efeito real no integrado.
