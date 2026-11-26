# F03 | Contrato de avaliação

Versão 0.1 proposta. Avaliar SHA exato em checkout limpo, Docker/Compose v2, Git, porta/projeto isolados; usar PostgreSQL real. Instalar nada no host além dos pré-requisitos do brief. Rodar `./bin/up`, `./bin/gates F03` quando implementados e executar verificações específicas abaixo. Se comando não existir ou efeito não puder ser reproduzido, FAIL/ BLOCKED, nunca PASS. Em F01, gates inicial não pressupõe features futuras. Fixtures de estados futuros são permitidas para dependências ainda não implementadas, somente em DB de teste e indicadas no relatório. Não substituir provas HTTP/UI finais por fixtures.

## Itens obrigatórios locais

| Item | Critério | Procedimento e evidência | Resultado esperado |
|---|---|---|---|
| C-F03-A09 | A09 (R01) | Tabela de casos com agora, passado, futuro, 0, -1, 1.5, preço zero e campos vazios; checar persistência. | Nome/local não vazios; lotação inteira >=1; preço em centavos >0; início estritamente futuro em criar e editar, inclusive requisição direta. |
| C-F03-A10 | A10 (R02,R04) | Criar E1, consultar catálogo antes/depois e abrir URL de gestão com dono. | Evento nasce draft; publicar torna visível a consulta pública; gestão tem URL estável e lista apenas próprios eventos. |
| C-F03-A11 | A11 (R03,R05) | Fixtures de dois ingressos ocupando; reduzir para 1 rejeita, 2/3 aceitam; snapshot histórico inalterado. | Editar sob lock do evento; capacidade abaixo de pending+confirmed é rejeitada; igual/acima aceita; preço novo não altera snapshot de ingressos. |
| C-F03-A12 | A12 (R11) | Fixture de estado cancelled; POST edição/publicação e leitura pública; negar sem mutação. | Evento cancelled não pode ser alterado/republicado; catálogo e disponibilidade pública o excluem. |

## Cross-feature (dependências anteriores)

| Item | Critério | Procedimento e evidência | Esperado |
|---|---|---|---|
| C-F03-X02 | X02 (F01→F03) | DB limpo migrado; criar evento futuro e rejeitar ontem. | Migração e clock da fundação permitem criação e rejeição de data vencida. |
| C-F03-X03 | X03 (F02→F03) | Browser e POST direto B contra E1 de A; ausência de dados, estado intacto. | URL de gestão e listagem usam dono da sessão; B não pode editar/publicar A. |

## Veredito

PASS somente se todo item aplicável tem evidência real e satisfaz o resultado esperado. FAIL se divergente; BLOCKED se não reproduzível. Para itens W6, relatório isolado identifica explicitamente `not_applicable_until_integration`; o relatório mais recente após W6 cobre também esses itens. Guardar relatório em `reports/<UTC>-<shortSHA>.md` (novo arquivo; não alterar). Registrar data UTC, SHA completo, ferramenta/modelo, sessão independente, comandos, saída, artefatos, veredito individual e resumo. Usar template em docs/agents.
