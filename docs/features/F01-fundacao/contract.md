# F01 | Contrato de avaliação

Versão 0.1 proposta. Avaliar SHA exato em checkout limpo, Docker/Compose v2, Git, porta/projeto isolados; usar PostgreSQL real. Instalar nada no host além dos pré-requisitos do brief. Rodar `./bin/up`, `./bin/gates F01` quando implementados e executar verificações específicas abaixo. Se comando não existir ou efeito não puder ser reproduzido, FAIL/ BLOCKED, nunca PASS. Em F01, gates inicial não pressupõe features futuras. Fixtures de estados futuros são permitidas para dependências ainda não implementadas, somente em DB de teste e indicadas no relatório. Não substituir provas HTTP/UI finais por fixtures.

## Itens obrigatórios locais

| Item | Critério | Procedimento e evidência | Resultado esperado |
|---|---|---|---|
| C-F01-A01 | A01 (H01) | Clonar SHA em pasta temporária; executar up; verificar HTTP e compose ps. | Clone limpo: ./bin/up constrói, migra, semeia e espera web/worker/DB prontos; /health/ready retorna 200 sem configuração manual. |
| C-F01-A02 | A02 (H02) | Executar up, seed duas vezes, down, provar porta fechada e ps vazio, up novamente; comparar IDs e autenticação após F02. | ./bin/down encerra todos os containers e portas iniciados; nova subida conserva dados e seed não duplica contas. |
| C-F01-A03 | A03 (H03) | Executar gates e injetar falha em cópia descartável; capturar códigos de saída. | ./bin/gates falha com teste quebrado, executa testes reais e lint, usa DB isolado e passa com testes válidos. |
| C-F01-A04 | A04 (H04) | Inspeção dos arquivos, ambiente sem .env e sem credenciais externas. | AGENTS.md e README contêm comandos, endereços, credenciais de seed, mapa; modo padrão não exige gateway real. |
| C-F01-A05 | A05 (R05,R09) | Aplicar migração em DB vazio e reexecutar; tentar inserir status inválido, código duplicado, capacidade zero e FK órfã; todas rejeitadas. | Schema possui FKs, unicidade de código, restrições de status, lotação e preço; migrações reexecutáveis. |

## Cross-feature (dependências anteriores)

| Item | Critério | Procedimento e evidência | Esperado |
|---|---|---|---|
| Não aplicável | Nenhum | ; | ; |

## Veredito

PASS somente se todo item aplicável tem evidência real e satisfaz o resultado esperado. FAIL se divergente; BLOCKED se não reproduzível. Para itens W6, relatório isolado identifica explicitamente `not_applicable_until_integration`; o relatório mais recente após W6 cobre também esses itens. Guardar relatório em `reports/<UTC>-<shortSHA>.md` (novo arquivo; não alterar). Registrar data UTC, SHA completo, ferramenta/modelo, sessão independente, comandos, saída, artefatos, veredito individual e resumo. Usar template em docs/agents.
