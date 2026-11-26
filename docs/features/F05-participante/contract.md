# F05 | Contrato de avaliação

Versão 0.1 proposta. Avaliar SHA exato em checkout limpo, Docker/Compose v2, Git, porta/projeto isolados; usar PostgreSQL real. Instalar nada no host além dos pré-requisitos do brief. Rodar `./bin/up`, `./bin/gates F05` quando implementados e executar verificações específicas abaixo. Se comando não existir ou efeito não puder ser reproduzido, FAIL/ BLOCKED, nunca PASS. Em F01, gates inicial não pressupõe features futuras. Fixtures de estados futuros são permitidas para dependências ainda não implementadas, somente em DB de teste e indicadas no relatório. Não substituir provas HTTP/UI finais por fixtures.

## Itens obrigatórios locais

| Item | Critério | Procedimento e evidência | Resultado esperado |
|---|---|---|---|
| C-F05-A18 | A18 (R02,R05,R07) | Browser: draft/publicado/cancelled, capacidade 1 pendente e tentativa direta sem vaga. | Vitrine exibe só publicados não cancelados, inclusive esgotados com texto exato Ingressos esgotados; tentativa concorrente recebe mesma mensagem. |
| C-F05-A19 | A19 (R06,R08,R09) | Playwright: cadastro, login, compra, tela pending e polling/reload até confirmed; conferir código em DB ou via F06 após integração. | Participante cria conta, compra pela vitrine, vê evento/status/código em Meus ingressos; pending imediato e confirmado em até 5s para 0001. |
| C-F05-A20 | A20 (R09,R13) | Fixtures dos cinco estados; duas contas; ingresso partner com mesmo e-mail não aparece; POST anônimo sem efeito. | Meus ingressos filtra por participant_id autenticado, não por e-mail, e mostra todos os cinco rótulos; visitante não compra. |

## Cross-feature (dependências anteriores)

| Item | Critério | Procedimento e evidência | Esperado |
|---|---|---|---|
| C-F05-X06 | X06 (F02→F05) | Dois browsers com sessões distintas; compra e acesso cruzado. | Sessão define dono do ingresso; anônimo e outra conta não veem compra pessoal. |
| C-F05-X07 | X07 (F03→F05) | Criar draft, publicar, reservar até lotar, cancelar fixture; recarregar catálogo. | Publicar/lotar/cancelar reflete na vitrine sem cache obsoleto. |
| C-F05-X08 | X08 (F04→F05) | Comprar 0004, observar lotação, após 45s ver declined e vaga. | Compra web usa reserve e worker; pendente ocupa e recusa libera na vitrine. |

## Veredito

PASS somente se todo item aplicável tem evidência real e satisfaz o resultado esperado. FAIL se divergente; BLOCKED se não reproduzível. Para itens W6, relatório isolado identifica explicitamente `not_applicable_until_integration`; o relatório mais recente após W6 cobre também esses itens. Guardar relatório em `reports/<UTC>-<shortSHA>.md` (novo arquivo; não alterar). Registrar data UTC, SHA completo, ferramenta/modelo, sessão independente, comandos, saída, artefatos, veredito individual e resumo. Usar template em docs/agents.
