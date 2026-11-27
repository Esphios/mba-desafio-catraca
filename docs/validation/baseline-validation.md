# Validação da baseline documental

## Resultado reproduzível antes da implementação

Executado em ambiente de elaboração com Python 3.13 e Git. A versão alvo do projeto é Python 3.12; o gate de W0 deve reproduzir a execução na imagem alvo. Não há aplicação ou ambiente Docker implementado neste pacote.

| Comando                               | Resultado observado                                                                                                                                                                                   |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `python scripts/validate_docs.py`     | PASS: 7 features, 37 critérios locais, 16 cross-feature, 6 critérios de processo.                                                                                                                     |
| `python scripts/validate_evidence.py` | PASS: estrutura inicial sem relatórios e sem aprovações fictícias.                                                                                                                                    |
| `python scripts/test_baseline.py`     | PASS: rejeitou CSV divergente, release incompleto, estado aprovado sem relatório, mesma sessão e adulterações locais e commitadas de relatório. Fixture sintética descartada em diretório temporário. |
| `python scripts/verify_model.py`      | PASS: 4.290 estados abstratos e 36.558 transições; contraexemplo artificial de sobrelotação rejeitado.                                                                                                |
| `python -m py_compile scripts/*.py`   | PASS: sintaxe dos scripts auxiliares.                                                                                                                                                                 |

O modelo assume transições serializadas. Não prova que o PostgreSQL ou a implementação futura efetivamente serializam operações; os testes em banco real são indispensáveis. O gate de evidências não comprova a autenticidade do conteúdo nem a independência efetiva da sessão; é necessário conferir os artefatos e o histórico de trabalho. O modo `--release` deve falhar nesta baseline.

## Pendente até a implementação

- Resolver e fixar versões patch, construir imagens, executar migrations e seed em Linux/macOS.
- Implementar e executar testes por feature, testes de integração com banco real, probes HTTP/browser e fluxo final em escala real.
- Validar visualmente/renderizar diagramas Mermaid e verificar o OpenAPI com ferramenta apropriada.
- Produzir relatórios independentes reais, integrar PRs e comprovar sobreposição temporal.
- Verificar todos os critérios de entrega em clone limpo da main.

Não há relatório de avaliação de feature neste documento; trata-se apenas de um registro da validação estrutural anterior ao código.
