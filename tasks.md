# Tasks | execução desde zero

Status: todas abertas. Marque caixas somente após evidência; mantenha critérios e estado sincronizados. Tarefas individuais estão também nos planos de feature. W0 aprova documentação; W1–W5 implementam; W6 integra e valida release.

## W0 | baseline documental

- [ ] T-W0-01: revisar brief, proposal, PRD, matriz, arquitetura/ADRs; skill `prd-and-traceability`; confirmar escolhas de design. Gate: `scripts/validate_docs.py`, revisão humana da semântica e cobertura do fluxo.
- [ ] T-W0-02: revisar HLD, FDD, protocolo concorrente, segurança, diagramas e limites de escrita; skill `architecture-review`; validar cada aresta e item contratual. Gate: renderizar diagramas e revisão de concorrência.
- [ ] T-W0-03: criar repo público novo, commit baseline, estabelecer branch protection se disponível; skill `wave-coordinator`. Não clonar solução de referência. Registrar SHA real.

## W1–W5 | implementação

Cada linha tem 4 etapas, com testes e skills; planos detalham execução. A validação de cada etapa usa testes relevantes antes da etapa seguinte, a última cobre todos os itens A/X aplicáveis. A ordem de implementação não é autorização para autoavaliar.

| Tarefa | Entrega | Skills | Validação | Dependência |
|---|---|---|---|---|
| T-F01-01 | Preparar repositório, fixar versões de containers e dependências, lint, runner e configuração; construir imagens para as arquiteturas suportadas. | harness, implement-feature | TEST-A03 + lint/build + unitários do componente | W0 |
| T-F01-02 | Definir schema de contas, eventos, ingressos e jobs, constraints, índices e migração inicial; usar PostgreSQL e estabelecer convenção de lock. | harness, implement-feature | TEST-A05 + unitários e integração de mudanças | T-F01-01 |
| T-F01-03 | Implementar seed, serviço one-shot de migração, heartbeat inicial do worker, readiness e scripts up/down/gates com ambiente de testes isolado. | harness, implement-feature | TEST-A01; TEST-A02; TEST-A04 + integração real e negativos | T-F01-02 |
| T-F01-04 | Comprovar clone limpo, seed repetível, down/up e gate negativo; registrar comandos e ambiente. | harness, implement-feature | A01, A02, A03, A04, A05 + X aplicáveis + avaliação independente | T-F01-03 |
| T-F02-01 | Implementar formulário de cadastro, backend de autenticação quando necessário, rotas e templates de cadastro/login/logout. | secure-web, implement-feature | TEST-A06 + lint/build + unitários do componente | F01 |
| T-F02-02 | Definir guards de papel e dono, redirects, tratamento de erros e CSRF. | secure-web, implement-feature | TEST-A07; TEST-A08 + unitários e integração de mudanças | T-F02-01 |
| T-F02-03 | Testar papéis, invalidação da sessão, unicidade/hash e acesso indevido a fixtures; revisar logs. | secure-web, implement-feature | integração real e negativos | T-F02-02 |
| T-F02-04 | Verificar login da seed F01 e publicar contrato de autorização. | secure-web, implement-feature | A06, A07, A08 + X aplicáveis + avaliação independente | T-F02-03 |
| T-F03-01 | Implementar validação e formulários de evento, conversão monetária, serviços e consultas por dono. | transactional-domain, implement-feature | TEST-A09 + lint/build + unitários do componente | F01, F02 |
| T-F03-02 | Implementar lock, consultas de ocupação, edição/publicação transacionais e DTO público. | transactional-domain, implement-feature | TEST-A11; TEST-A12 + unitários e integração de mudanças | T-F03-01 |
| T-F03-03 | Construir listagem e gestão do organizador e preparar ponto de extensão para operações. | transactional-domain, implement-feature | TEST-A10 + integração real e negativos | T-F03-02 |
| T-F03-04 | Executar testes de validação, estado, dono e lock; congelar DTO e interfaces para F04. | transactional-domain, implement-feature | A09, A10, A11, A12 + X aplicáveis + avaliação independente | T-F03-03 |
| T-F04-01 | Implementar Buyer/TicketDTO tipados, validação, classificação do gateway e geração de código. | transactional-domain, implement-feature | TEST-A17 + lint/build + unitários do componente | F01, F03 |
| T-F04-02 | Implementar reserva atômica, lock seguido de contagem, snapshot e job durável; testar falha e colisão. | transactional-domain, implement-feature | TEST-A13; TEST-A14 + unitários e integração de mudanças | T-F04-01 |
| T-F04-03 | Implementar loop de finalização, proteção terminal, recuperação após reinício e consultas de ingressos. | transactional-domain, implement-feature | TEST-A15; TEST-A16 + integração real e negativos | T-F04-02 |
| T-F04-04 | Executar stress concorrente, timing real e corridas edição/reserva; congelar interfaces e registrar base SHA para W5. | transactional-domain, implement-feature | A13, A14, A15, A16, A17 + X aplicáveis + avaliação independente | T-F04-03 |
| T-F05-01 | Implementar listagem pública, detalhes e estados de disponibilidade/vitrine vazia. | secure-web, implement-feature | TEST-A18 + lint/build + unitários do componente | F02, F03, F04 |
| T-F05-02 | Implementar formulário autenticado, mapeamento de erros, navegação e Meus ingressos. | secure-web, implement-feature | TEST-A19; TEST-A20 + unitários e integração de mudanças | T-F05-01 |
| T-F05-03 | Executar testes browser de pendente, confirmação, recusa, esgotamento, titularidade e CSRF. | secure-web, implement-feature | integração real e negativos | T-F05-02 |
| T-F05-04 | Abrir PR; avaliar X06–X08 localmente; reservar X14/X16 para gate integrado. | secure-web, implement-feature | A18, A19, A20 + X aplicáveis + avaliação independente | T-F05-03 |
| T-F06-01 | Implementar guard de chave, serializadores, registro de rotas e mapeamento estável de erros. | partner-contract, implement-feature | lint/build + unitários do componente | F03, F04 |
| T-F06-02 | Implementar eventos e compras via catálogo/ledger; implementar consulta de ingresso. | partner-contract, implement-feature | TEST-A21; TEST-A22; TEST-A23 + unitários e integração de mudanças | T-F06-01 |
| T-F06-03 | Executar testes de shape, precedência, autenticação, duas rodadas HTTP de 30 e consulta de fixture web. | partner-contract, implement-feature | TEST-A24 + integração real e negativos | T-F06-02 |
| T-F06-04 | Abrir PR e avaliar X09–X10; X15/X16 serão verificados após merge. | partner-contract, implement-feature | A21, A22, A23, A24 + X aplicáveis + avaliação independente | T-F06-03 |
| T-F07-01 | Implementar check-in com lock do evento, precedência e mensagem exatas; adicionar formulário à gestão. | transactional-domain, secure-web, implement-feature | TEST-A25 + lint/build + unitários do componente | F02, F03, F04 |
| T-F07-02 | Implementar cancelamento atômico e proteção de estado terminal; verificar gateway tardio, corridas e edição negada. | transactional-domain, secure-web, implement-feature | TEST-A26 + unitários e integração de mudanças | T-F07-01 |
| T-F07-03 | Implementar agregação do painel e seção de ações/métricas; testar preço histórico e ingresso utilizado estornado. | transactional-domain, secure-web, implement-feature | TEST-A27; TEST-A28 + integração real e negativos | T-F07-02 |
| T-F07-04 | Executar avaliação independente A25–A28 e X11–X13; após W5 executar X14–X16. | transactional-domain, secure-web, implement-feature | A25, A26, A27, A28 + X aplicáveis + avaliação independente | T-F07-03 |

## W5 | paralelismo obrigatório

- [ ] T-W5-00: todos F01–F04 aprovados e mergeados; congelar schema, DTO e registro de rotas. Coordenador registra base SHA e cria 3 worktrees, branches F05/F06/F07. Use `git worktree add -b feat/f05-participante ../catraca-f05 main` (repetir para demais branches), cada sessão usa Compose project e porta próprios. Não compartilhar banco.
- [ ] T-W5-01: iniciar pelo menos 2 implementadores simultaneamente e criar commits genuínos de início com mudanças úteis antes que qualquer outro finalize. Registrar início e SHA; não backdate. Para comprovação forte, todos os três PRs devem satisfazer sobreposição par a par.
- [ ] T-W5-02: executar contratos locais em sessões independentes; corrigir com relatórios novos. Integrar PRs um por vez; em conflito, coordenador resolve registrando decisão, pede avaliação das mudanças afetadas e roda regressão. Preservar histórico GitHub e links no README. Não usar merge sem aprovação.

## W6 | release

- [ ] T-W6-01: skill `wave-coordinator`, conferir merges reais, sobreposição de commits, atualizar estado com SHA e relatório mais recente de cada feature; não marcar concluído se faltam X14–X16.
- [ ] T-W6-02: skill `independent-evaluator` + `integration-release`; executar X14, X15, X16 e fluxo completo 1–17 em main via clone limpo com delays padrão. Avaliar novamente F06/F07 contra itens integrados, relatórios novos. Corrigir regressão via PR e repetir fluxo; registrar E1–E5 e evidências reais.
- [ ] T-W6-03: avaliar P01–P06 (fluxo 18 incluído), revisar README, docs, gates, status, links, imutabilidade de relatórios e ausência de segredos. Registrar relatório de release em `docs/validation/reports/` e atualizar README/state. Rodar gate final no SHA final após commits documentais.

## Definition of Done

Feature: contratos aplicáveis aprovados por avaliador separado, unit/integration/browser conforme feature, docs atualizados, PR mergeado, dependentes não quebrados. Release: todos A/X/P aprovados, resultados reais no SHA indicado, nenhuma regressão, ambiente local reprodutível, estado concluído coerente com relatórios e README, repo público. Nenhuma checklist verde artificial.
