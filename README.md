# Catraca | pacote de planejamento greenfield

**Estado:** especificação inicial, não produto executável. Nenhuma feature implementada ou avaliada. Não há PRs fictícios.

## Como iniciar agora

1. Extraia este pacote em diretório vazio, não dentro de um clone da solução de referência.
2. Leia `AGENTS.md`, `proposal.md`, `docs/prd/PRD.md`, `design.md` e `requirements-matrix.md`.
3. Revise ADRs propostos e aprove a baseline no primeiro commit. Inicialize um Git próprio (`git init -b main`).
4. Execute `python3 scripts/validate_docs.py` (Python 3 local opcional; alternativa: `docker run --rm -v "$PWD:/work:ro" -w /work python:3.12-slim python scripts/validate_docs.py`).
5. Inicie F01 conforme `tasks.md`, com uma sessão implementadora; outra sessão avalia o contrato. Só então avance a wave.

## Contrato do README final (preencher durante implementação)

| Item | Planejado | Estado |
|---|---|---|
| Requisitos | Linux/macOS ou WSL, Docker Engine + Compose v2, Git, Node LTS opcional | A validar |
| Subir | `./bin/up` | A implementar F01 |
| Derrubar | `./bin/down` | A implementar F01 |
| Gates | `./bin/gates` | A implementar F01, expandir por feature |
| Web/API | `http://localhost:8080` (ambos, API em `/api/partner`) | Planejado |
| Organizador A | `alice@catraca.test` / `DemoAlice!2026` | Seed planejada |
| Organizador B | `bruno@catraca.test` / `DemoBruno!2026` | Seed planejada |
| Participante | `participante@catraca.test` / `DemoPessoa!2026` | Seed planejada |
| Chave parceira | `catraca-local-partner-demo-v1` | Somente demonstração local |
| PRs paralelos | F05, F06, F07: registrar links reais após merge | Pendente |

Não use as credenciais de demonstração em serviços reais. Após F01, atualize este README com comandos confirmados e saída da subida. Antes da entrega, registre SHA final, links reais dos PRs e resultado do fluxo externo.

## Mapa dos artefatos

- `proposal.md`: escopo e proposta executiva.
- `docs/prd/PRD.md`: produto, regras, features, dependências, critérios locais e cruzados.
- `design.md`: HLD, fronteiras, modelo de dados, concorrência e contratos internos.
- `requirements-matrix.md` e `.csv`: rastreabilidade requisito → critério → contrato → teste → tarefa.
- `tasks.md`: waves, tarefas, skills, gates e entregáveis.
- `docs/features/F*/`: spec (FDD), plan, contract e espaço para relatórios reais.
- `docs/architecture/`: diagramas, protocolo transacional, segurança, ADRs e pesquisa técnica.
- `docs/engineering-guidelines.md`: regras de código, Git, testes e documentação.
- `docs/validation/`: catálogo de testes, fluxo integrado, avaliação e harness.
- `docs/agents/`: design do workflow agentic, prompts e templates de avaliação.
- `state/project-state.json`: estado verdadeiro, inicialmente `planned`.
- `AGENTS.md`, `CLAUDE.md`, `.agents/skills/`: instruções e skills portáveis.
- `scripts/validate_docs.py`: verificador executável dos artefatos. `scripts/partner_probe.py`: teste HTTP para ambiente implementado.

## Decisões previstas

Python 3.12/Django 5.2 LTS, PostgreSQL 17, templates HTML com formulários e worker persistente, todos em containers. Compra, edição, pagamento, check-in e cancelamento compartilham lock da linha de evento. Pagamento simulado por job transacional com vencimento, sem sleep em request. Avaliadores trabalham em sessão nova contra SHA fixado, não editam código nem relatórios antigos. Todas são decisões de projeto, sujeitas à aprovação da baseline e aos testes reais.
