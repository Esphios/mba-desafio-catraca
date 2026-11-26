# F06 | Plano de implementação

Prerequisitos: baseline aprovada, dependências F03, F04 mergeadas; branch `feat/f06-parceiros`; ler spec, contrato, guidelines, skills e estado.

## T-F06-01 | Etapa 1

- [ ] Implementar guard de chave, serializadores, registro de rotas e mapeamento estável de erros.
- Validação: executar testes pertinentes ao componente; se falhar, corrigir antes de seguir. Na última etapa rodar contrato inteiro e gates; não marcar aprovado pelo próprio implementador.
- Gate mínimo desta etapa: Teste de unidade de guard e tradução de erros; a autenticação de todas as rotas é verificada na etapa 2.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F06-02 | Etapa 2

- [ ] Implementar eventos e compras via catálogo/ledger; implementar consulta de ingresso.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A21`: HTTP GET com fixtures dos estados; comparar shape e valores; esgotado permanece com 0. Esperado: GET events com chave retorna array de publicados, id/name/startsAt/priceCents/availableSeats com tipos exatos; cancelados/drafts excluídos.
  - `TEST-A22`: Tabela HTTP: JSON inválido e evento inexistente ->422; inválido e esgotado ->422; válido draft/cancelled/inexistente ->404; lotado ->409; válido ->202. Esperado: POST compra responde 202 com ticketId/code/status pending; após chave, precedência 422 invalid_request, 404 event_not_available, 409 sold_out.
  - `TEST-A23`: HTTP em três rotas × sem/errada e com payload inválido; consulta fixtures web/partner e inexistente; checar JSON exato. Esperado: GET ticket consulta ambos os canais e retorna ticketId/code/eventId/status/checkedIn booleano; desconhecido 404 ticket_not_found; todas as rotas sem chave ou chave errada 401 unauthorized.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: HTTP 200/202/401/404/409/422 com corpos exatos, precedência e ambos canais.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F06-03 | Etapa 3

- [ ] Executar testes de shape, precedência, autenticação, duas rodadas HTTP de 30 e consulta de fixture web.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A24`: Runner HTTP com barreira, 30 conexões, validar corpo e IDs únicos, consultar cada aceito e availableSeats=0; usar novo evento por rodada. Esperado: Em duas rodadas HTTP reais, cada evento novo de capacidade 5 recebe 30 POST simultâneos com cartão 0001: 5×202 e 25×409, sem 5xx; depois 5 confirmados.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Probe 30×5 em dois eventos, códigos únicos, consulta de confirmação e vaga 0.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F06-04 | Etapa 4

- [ ] Abrir PR e avaliar X09–X10; X15/X16 serão verificados após merge.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A21`: HTTP GET com fixtures dos estados; comparar shape e valores; esgotado permanece com 0. Esperado: GET events com chave retorna array de publicados, id/name/startsAt/priceCents/availableSeats com tipos exatos; cancelados/drafts excluídos.
  - `TEST-A22`: Tabela HTTP: JSON inválido e evento inexistente ->422; inválido e esgotado ->422; válido draft/cancelled/inexistente ->404; lotado ->409; válido ->202. Esperado: POST compra responde 202 com ticketId/code/status pending; após chave, precedência 422 invalid_request, 404 event_not_available, 409 sold_out.
  - `TEST-A23`: HTTP em três rotas × sem/errada e com payload inválido; consulta fixtures web/partner e inexistente; checar JSON exato. Esperado: GET ticket consulta ambos os canais e retorna ticketId/code/eventId/status/checkedIn booleano; desconhecido 404 ticket_not_found; todas as rotas sem chave ou chave errada 401 unauthorized.
  - `TEST-A24`: Runner HTTP com barreira, 30 conexões, validar corpo e IDs únicos, consultar cada aceito e availableSeats=0; usar novo evento por rodada. Esperado: Em duas rodadas HTTP reais, cada evento novo de capacidade 5 recebe 30 POST simultâneos com cartão 0001: 5×202 e 25×409, sem 5xx; depois 5 confirmados.
  - `TEST-X09`: GET antes/depois publicação, edição e cancelamento fixture. Esperado: API usa catálogo e centavos/ocupação canônicos; edição preço/capacidade reflete na listagem.
  - `TEST-X10`: POST simultâneo e GET ticket, comparar dados de ledger. Esperado: API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## Handoff

- [ ] Testes unitários, integração e contratos locais verdes no SHA indicado.
- [ ] Nada fora da ownership; atualizar docs e registrar dependências.
- [ ] Entregar SHA e comandos à sessão nova de avaliação; não entregar veredito pronto.
- [ ] Após aprovação independente e PR mergeado, coordenador atualiza estado.
