# Método e governança da documentação

A especificação normativa é o brief Catraca: R01–R13, contrato de API e fluxo de avaliação. Os nomes, mensagens exatas e identificadores que fazem parte do contrato são mantidos para interoperabilidade. Decisões técnicas são propostas novas, sujeitas a W0. Referências técnicas oficiais estão em architecture/research.md.

O módulo Design Docs orienta a classificação de documentos: PRD e proposal (produto), HLD/FDD/LLD e ADRs (design), diagramas C4/Mermaid, Engineering Guidelines (processo), harness/testes/AI design (operação e agentes). Para greenfield, a sequência é brief → PRD → research/alternativas → HLD/ADRs → FDD + contrato/plano → matriz/tasks → implementação → avaliação → auditoria. O fluxo de análise de codebase é adaptado para design pré-código. Não confundir estrutura planejada com estado existente.

Limites: não há aplicação, migrations, containers, PRs ou relatórios reais neste pacote. Verificadores e oráculo de modelo são executáveis; os testes de produto especificados devem ser implementados por feature. Probe HTTP é utilizável depois que API existir. Nenhuma afirmação de sucesso funcional sem execução no SHA real. Aprovar escolhas em W0 e atualizar design após desvios autorizados, preservando histórico.
