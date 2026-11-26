# F04 | Contrato de avaliação

Versão 0.1 proposta. Avaliar SHA exato em checkout limpo, Docker/Compose v2, Git, porta/projeto isolados; usar PostgreSQL real. Instalar nada no host além dos pré-requisitos do brief. Rodar `./bin/up`, `./bin/gates F04` quando implementados e executar verificações específicas abaixo. Se comando não existir ou efeito não puder ser reproduzido, FAIL/ BLOCKED, nunca PASS. Em F01, gates inicial não pressupõe features futuras. Fixtures de estados futuros são permitidas para dependências ainda não implementadas, somente em DB de teste e indicadas no relatório. Não substituir provas HTTP/UI finais por fixtures.

## Itens obrigatórios locais

| Item | Critério | Procedimento e evidência | Resultado esperado |
|---|---|---|---|
| C-F04-A13 | A13 (R05,R06,R09) | Invocar reserve e consultar DB; medir tempo <2s em ambiente local estável; rollback injetado não deixa ticket/job; colisão de código tratada. | Uma compra válida retorna ingresso pending com ID/código únicos e job gravado na mesma transação, sem aguardar gateway; reserva já ocupa vaga. |
| C-F04-A14 | A14 (R07) | TransactionTestCase com barreira de threads/conexões distintas e PostgreSQL real; consultar ocupação, jobs e erros; repetir 10 vezes como robustez. | Quando lotação esgota, não cria ingresso/job; 30 reservas concorrentes sobre capacidade 5 dão exatamente 5 sucessos/25 sold_out, em duas rodadas novas. |
| C-F04-A15 | A15 (R08) | Testes unitários de mapeamento e integração com relógio real: polling, timestamps, ocupação; não acelerar teste de prazo. | Gateway padrão confirma 0001 e recusa 0002/outros em 2–5s; confirma 0003 e recusa 0004 em 30–40s; recusa libera uma vaga. |
| C-F04-A16 | A16 (R03,R11) | Testar preço antes/depois, aplicar resultado duas vezes e fixtures cancelled/refunded; parar/reiniciar worker com job pendente e verificar efeito único. | Snapshot de preço é capturado sob lock; finalize só altera pending de evento publicado; resultado duplicado/tardio não revive terminal; job sobrevive reinício. |
| C-F04-A17 | A17 (R06) | Casos 15/17 dígitos, letras, Unicode, espaços, e-mail inválido; assert contagem zero e inspeção DB/logs. | Cartão diferente de 16 dígitos ASCII falha antes de criar ingresso; e-mail malformado na compra de parceiro falha; PAN não persiste nem aparece em logs. |

## Cross-feature (dependências anteriores)

| Item | Critério | Procedimento e evidência | Esperado |
|---|---|---|---|
| C-F04-X04 | X04 (F01→F04) | Comprar slow, reiniciar worker antes de due; obter status final uma vez. | Worker do Compose consome job persistido após reinício sem chave real. |
| C-F04-X05 | X05 (F03→F04) | Corrida compra × redução e compra × preço; conferir invariantes e snapshots. | Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação. |

## Veredito

PASS somente se todo item aplicável tem evidência real e satisfaz o resultado esperado. FAIL se divergente; BLOCKED se não reproduzível. Para itens W6, relatório isolado identifica explicitamente `not_applicable_until_integration`; o relatório mais recente após W6 cobre também esses itens. Guardar relatório em `reports/<UTC>-<shortSHA>.md` (novo arquivo; não alterar). Registrar data UTC, SHA completo, ferramenta/modelo, sessão independente, comandos, saída, artefatos, veredito individual e resumo. Usar template em docs/agents.
