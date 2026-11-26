# F02 | Contrato de avaliação

Versão 0.1 proposta. Avaliar SHA exato em checkout limpo, Docker/Compose v2, Git, porta/projeto isolados; usar PostgreSQL real. Instalar nada no host além dos pré-requisitos do brief. Rodar `./bin/up`, `./bin/gates F02` quando implementados e executar verificações específicas abaixo. Se comando não existir ou efeito não puder ser reproduzido, FAIL/ BLOCKED, nunca PASS. Em F01, gates inicial não pressupõe features futuras. Fixtures de estados futuros são permitidas para dependências ainda não implementadas, somente em DB de teste e indicadas no relatório. Não substituir provas HTTP/UI finais por fixtures.

## Itens obrigatórios locais

| Item | Critério | Procedimento e evidência | Resultado esperado |
|---|---|---|---|
| C-F02-A06 | A06 (R13) | Browser: cadastro/login/logout; POST com role=organizer; consulta DB somente para verificar hash e papel. | Cadastro público cria somente participante, e-mail normalizado único; senha armazenada como hash; login válido e logout invalidam sessão; erro genérico em credenciais inválidas. |
| C-F02-A07 | A07 (R13) | Sessões independentes A/B/P/anônima; fixture de evento A; assert HTTP 404 para B, ausência de nome/dados e nenhuma mutação; 403 ou redirect para demais. | Visitante e participante não acessam rotas de gestão; B não lê nem modifica eventos de A, incluindo URL direta e POST forjado. |
| C-F02-A08 | A08 (R09,R13) | Testar guarda de participante com duas contas e recurso fixture; tentar usar X-Api-Key em rota web; negar. | Participante só tem acesso aos próprios recursos; parceiro não cria sessão web nem vincula conta pelo e-mail. |

## Cross-feature (dependências anteriores)

| Item | Critério | Procedimento e evidência | Esperado |
|---|---|---|---|
| C-F02-X01 | X01 (F01→F02) | Subir ambiente limpo, login das três contas, comparar IDs após reseed. | Após up com seed, A/B/P autenticam; duas execuções da seed não duplicam contas. |

## Veredito

PASS somente se todo item aplicável tem evidência real e satisfaz o resultado esperado. FAIL se divergente; BLOCKED se não reproduzível. Para itens W6, relatório isolado identifica explicitamente `not_applicable_until_integration`; o relatório mais recente após W6 cobre também esses itens. Guardar relatório em `reports/<UTC>-<shortSHA>.md` (novo arquivo; não alterar). Registrar data UTC, SHA completo, ferramenta/modelo, sessão independente, comandos, saída, artefatos, veredito individual e resumo. Usar template em docs/agents.
