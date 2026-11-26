# F06 | Contrato de avaliação

Versão 0.1 proposta. Avaliar SHA exato em checkout limpo, Docker/Compose v2, Git, porta/projeto isolados; usar PostgreSQL real. Instalar nada no host além dos pré-requisitos do brief. Rodar `./bin/up`, `./bin/gates F06` quando implementados e executar verificações específicas abaixo. Se comando não existir ou efeito não puder ser reproduzido, FAIL/ BLOCKED, nunca PASS. Em F01, gates inicial não pressupõe features futuras. Fixtures de estados futuros são permitidas para dependências ainda não implementadas, somente em DB de teste e indicadas no relatório. Não substituir provas HTTP/UI finais por fixtures.

## Itens obrigatórios locais

| Item | Critério | Procedimento e evidência | Resultado esperado |
|---|---|---|---|
| C-F06-A21 | A21 (API,R02,R05) | HTTP GET com fixtures dos estados; comparar shape e valores; esgotado permanece com 0. | GET events com chave retorna array de publicados, id/name/startsAt/priceCents/availableSeats com tipos exatos; cancelados/drafts excluídos. |
| C-F06-A22 | A22 (API,R06,R07) | Tabela HTTP: JSON inválido e evento inexistente ->422; inválido e esgotado ->422; válido draft/cancelled/inexistente ->404; lotado ->409; válido ->202. | POST compra responde 202 com ticketId/code/status pending; após chave, precedência 422 invalid_request, 404 event_not_available, 409 sold_out. |
| C-F06-A23 | A23 (API,R09,R13) | HTTP em três rotas × sem/errada e com payload inválido; consulta fixtures web/partner e inexistente; checar JSON exato. | GET ticket consulta ambos os canais e retorna ticketId/code/eventId/status/checkedIn booleano; desconhecido 404 ticket_not_found; todas as rotas sem chave ou chave errada 401 unauthorized. |
| C-F06-A24 | A24 (R07,API) | Runner HTTP com barreira, 30 conexões, validar corpo e IDs únicos, consultar cada aceito e availableSeats=0; usar novo evento por rodada. | Em duas rodadas HTTP reais, cada evento novo de capacidade 5 recebe 30 POST simultâneos com cartão 0001: 5×202 e 25×409, sem 5xx; depois 5 confirmados. |

## Cross-feature (dependências anteriores)

| Item | Critério | Procedimento e evidência | Esperado |
|---|---|---|---|
| C-F06-X09 | X09 (F03→F06) | GET antes/depois publicação, edição e cancelamento fixture. | API usa catálogo e centavos/ocupação canônicos; edição preço/capacidade reflete na listagem. |
| C-F06-X10 | X10 (F04→F06) | POST simultâneo e GET ticket, comparar dados de ledger. | API usa mesmo reserve/consulta: carga, códigos e estados, inclusive ticket web fixture. |

## Itens de integração pós-wave (W6)

Não bloquear aprovação isolada com itens ainda indisponíveis; estes são obrigatórios no gate de release integrado e avaliados novamente por sessão independente depois dos merges. Não registrar PASS antecipado.

| Item | Critério | Procedimento | Esperado |
|---|---|---|---|
| C-F06-X16 | X16 (F05→F06) | Corrida web e API com capacidade 1; um sucesso, outro esgotado; testar isolamento pelo e-mail. | Integração final: canais disputam mesma última vaga; consulta partner aceita ticket web e compra partner não entra em conta web. |

## Veredito

PASS somente se todo item aplicável tem evidência real e satisfaz o resultado esperado. FAIL se divergente; BLOCKED se não reproduzível. Para itens W6, relatório isolado identifica explicitamente `not_applicable_until_integration`; o relatório mais recente após W6 cobre também esses itens. Guardar relatório em `reports/<UTC>-<shortSHA>.md` (novo arquivo; não alterar). Registrar data UTC, SHA completo, ferramenta/modelo, sessão independente, comandos, saída, artefatos, veredito individual e resumo. Usar template em docs/agents.
