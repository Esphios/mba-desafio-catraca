# F06 | Plano de implementação

Entrada: baseline W0 aprovada, dependências F03, F04 integradas e aprovadas, branch exclusiva. Skills: partner-api-contract, concurrency-validation, feature-implementation.

## T-F06-01

**Entrega:** Implementar guard e serialização; tratamento explícito do parser e erros.

**Validação:** lint, checks do framework e testes já implementados; fase 1 não exige endpoints futuros.
- Criar teste unitário ou de integração para a entrega desta etapa; provar caminho negativo e resultado observado antes da próxima etapa.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F06-02

**Entrega:** Ligar três rotas ao catálogo/ledger; OpenAPI e fixtures.

**Validação:** lint, checks do framework e testes já implementados; fase 2 não exige endpoints futuros.
- `TEST-A21` (A21): GET /api/partner/events; verificar set de campos, tipos, timestamps e vagas. Resultado: 200 array; publicados inclusive esgotados; sem dados de owner/PII; disponibilidade derivada.
- `TEST-A22` (A22): POST válido; em seguida combinar erro de chave, payload inválido, evento indisponível e falta de vaga. Resultado: 202 pending exato; 401→422→404→409 na precedência; erros sem efeitos.
- `TEST-A23` (A23): GET ambos os tickets e ID ausente; executar as três rotas sem chave e com chave inválida. Resultado: 200 exatamente ticketId/code/eventId/status/checkedIn booleano; 404 ticket_not_found; 401 unauthorized em 6 combinações.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F06-03

**Entrega:** Validar auth/precedência, malformed JSON, carga e consultas.

**Validação:** lint, checks do framework e testes já implementados; fase 3 não exige endpoints futuros.
- `TEST-A24` (A24): Disparar 30 POSTs com final 0001 por evento usando barreira; verificar payloads, cinco IDs/códigos únicos, disponibilidade e confirmações até 10s. Resultado: Por rodada 5×202, 25×409 sold_out, nenhum outro status; cinco confirmed e 0 vagas.
- `TEST-A34` (A34): Enviar JSON truncado, null, array, e-mail ruim, cartão Unicode e numérico, content-type incorreto, corpo com chave ausente. Resultado: 401 antes de parse; 422 para payload inválido autenticado mesmo com evento inexistente/lotado; sem redirect/500.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F06-04

**Entrega:** Avaliar local e preparar testes de canais mistos para integração.

**Validação:** lint, checks do framework e testes já implementados; fase 4 não exige endpoints futuros.
- `TEST-A21` (A21): GET /api/partner/events; verificar set de campos, tipos, timestamps e vagas. Resultado: 200 array; publicados inclusive esgotados; sem dados de owner/PII; disponibilidade derivada.
- `TEST-A22` (A22): POST válido; em seguida combinar erro de chave, payload inválido, evento indisponível e falta de vaga. Resultado: 202 pending exato; 401→422→404→409 na precedência; erros sem efeitos.
- `TEST-A23` (A23): GET ambos os tickets e ID ausente; executar as três rotas sem chave e com chave inválida. Resultado: 200 exatamente ticketId/code/eventId/status/checkedIn booleano; 404 ticket_not_found; 401 unauthorized em 6 combinações.
- `TEST-A24` (A24): Disparar 30 POSTs com final 0001 por evento usando barreira; verificar payloads, cinco IDs/códigos únicos, disponibilidade e confirmações até 10s. Resultado: Por rodada 5×202, 25×409 sold_out, nenhum outro status; cinco confirmed e 0 vagas.
- `TEST-A34` (A34): Enviar JSON truncado, null, array, e-mail ruim, cartão Unicode e numérico, content-type incorreto, corpo com chave ausente. Resultado: 401 antes de parse; 422 para payload inválido autenticado mesmo com evento inexistente/lotado; sem redirect/500.
- `TEST-X09` (X09): GET antes/depois publicação, edição e cancelamento fixture. Resultado: A listagem de parceiros reflete publicação, preço e capacidade de F03; fixtures draft/cancelled ficam fora. Cancelamento real será validado em X15.
- `TEST-X10` (X10): POST simultâneo e GET ticket, comparar dados de ledger. Resultado: API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## Integração posterior
- X16 / TEST-X16: Corrida web e API com capacidade 1; um sucesso, outro esgotado; testar isolamento pelo e-mail.

## Handoff
Entregar SHA limpo, base SHA, interfaces, comandos, logs redigidos e desvios. Avaliador novo, sem histórico de conversa, julga apenas contrato e evidência. Coordenador integra após local PASS; relatório final da feature exige também itens integrados, se houver.
