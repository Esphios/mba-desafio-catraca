# AI Design Doc | orquestração de agentes

## Papéis e contextos

| Papel | Entradas | Saídas | Proibições |
|---|---|---|---|
| PRD writer / arquiteto | brief, design docs do curso | proposal, PRD, HLD, ADR, matriz, FDD | inventar requisitos ou usar código da referência |
| Coordenador | baseline, estado, DAG, PRs | alocação de waves, conflitos, tracking | autoaprovar, falsificar tempo/commit |
| Implementador | spec/plano/contrato, dependências, guidelines | código, testes, commit e handoff | editar contrato para mascarar falha; avaliar próprio trabalho |
| Avaliador | SHA, contrato, brief, ambiente limpo | relatório novo com evidência | editar implementação; confiar no relato do implementador |
| Integrador de release | main integrada, fluxo, PRs | relatório final, regressões e veredito P | aceitar relatório local como prova de release |

Sessões distintas, não compartilhar histórico do implementador com avaliador. Ferramentas podem ser Codex, Claude Code, Gemini CLI ou Cursor conforme o brief. Modelo pode ser igual se contexto for independente; registrar nome real de ferramenta/modelo, não assumir. Handoff informa SHA, feature, caminho de contrato e comando, sem resumo persuasivo. Avaliador pode criar testes temporários em checkout descartável, mas não alterar código avaliado. Relatório é commit posterior que referencia SHA testado; resultados vinculados ao commit, não à sessão.

## Máquina de estados

planned → implementing → ready_for_evaluation → evaluating → approved → merged_pending_integration (se houver itens W6) → completed. FAIL/BLOCKED → needs_fix → implementing. Nunca saltar avaliação. Após mudança de comportamento reavaliar itens afetados em novo relatório. O coordenador é único escritor de `state/project-state.json`; preencher branch, implementationCommit, latestEvaluation, pr, mergedCommit; finaliza só após merge e integração quando necessária. Estado não substitui relatório. Atualize após cada handoff.

## Processo por wave

1. Coordenador confere dependências e contratos; inicializa branch baseada em main aprovada, registra SHA e ownership.
2. Implementador executa plano, testes por etapa, gates locais; commit. Envia handoff objetivo.
3. Avaliador abre nova sessão e checkout detached do SHA; lê contrato e brief; executa verificações sem usar banco da implementação. Para FAIL/BLOCKED, evidência e passos de repro; não corrige.
4. Coordenador recebe relatório, cria commit novo com ele, registra no estado. Implementador corrige na branch; outra avaliação em contexto vazio e novo relatório. Não editar anterior.
5. PR revisado e merge; roda gate de regressão para features integradas. Se falhar, corrigir por PR e reavaliar. W5 branches F05/F06/F07 trabalham simultaneamente sobre a mesma base F04 aprovada; contratos de integração X14–X16 ficam para W6. Depois, avaliações atualizadas F06/F07 contra main, sem N/A no último relatório.
6. W6 clone limpo, fluxo integral com delays padrão, todos os P. Atualizar README, links e estado; repetir gates após commits de documentação, verificar relatório aponta para commit avaliado cujo código é idêntico ao final (se só docs mudaram, registrar diff).

## Isolamento de ambientes

Cada worktree tem `COMPOSE_PROJECT_NAME=catraca-fXX` e `WEB_PORT` exclusivo; gates usam sufixo -test e volume separado. Não usar `docker system prune` ou `down -v` genérico. Avaliador usa `git worktree add --detach <diretorio> <SHA>`, project exclusivo, remove somente seus recursos. Para evidência de paralelismo, consultar lista de commits de cada PR mergeado via GitHub, registrar min/max timestamps reais e verificar primeiro de cada < último de todos os outros. Não depender de branches sobreviventes; não fabricar commits vazios/backdate.

## Controle de mudanças

Mudança requerida do brief não pode ser aprovada como exceção. Para escolha técnica: escrever amendment (problema, alternativas, critérios atingidos, dependentes, testes); coordenador aprova e atualiza PRD se necessário, design/ADR, FDD/contratos/matriz e consumidor antes de implementação. Bloquear branch que altera interface sem concordância. Documentação pode ser regenerada após análise real de código conforme módulo do curso, mas relatórios são append-only. Use `scripts/validate_docs.py` em toda mudança documental.
