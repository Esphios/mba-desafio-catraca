# Catraca | baseline de design

Este pacote inicia um repositório novo. Contém documentação, skills e ferramentas auxiliares; não é aplicação pronta. Todos os estados estão planejados. Primeiro W0, depois execução em waves conforme tasks.md.

## Como rodar (agora)

Docker/Compose e Git no host; Node LTS disponível, Python opcional. Para validar baseline sem Python local:

```bash
docker run --rm -v "$PWD:/work:ro" -w /work python:3.12-slim python scripts/validate_docs.py
docker run --rm -v "$PWD:/work:ro" -w /work python:3.12-slim python scripts/verify_model.py
```

Com Python 3.12 local, executar diretamente. Para verificar o gate de evidências e seus testes negativos, usar `python scripts/validate_evidence.py` e `python scripts/test_baseline.py` (Git disponível no host). Ver [validação da baseline](docs/validation/baseline-validation.md). O modelo é oráculo independente de regras, não aplicação. O probe HTTP só após API existir. F01 implementará `bash bin/up`, `bash bin/down`, `bash bin/gates` e `bash bin/flow` (último em W6). Nenhum destes comandos de produto existe ainda; substituir esta nota no README de entrega somente após testes reais. Pré-requisitos finais Linux/macOS + Docker Compose + Git; Windows WSL. Não exigir cópia .env ou instalação adicional.

## Endereços planejados

WEB e API http://127.0.0.1:8080; CAT_PORT pode alterar. API começa em /api/partner; readiness /health/ready. CAT_PROJECT=catraca-demo; CAT_PROFILE=demo; CAT_GATEWAY_SCALE=1. Sem serviço de pagamento externo.

## Credenciais de seed propostas (sintéticas, F01 implementará)

| Papel         | E-mail                | Senha        |
| ------------- | --------------------- | ------------ |
| Organizador A | gestao.a@example.test | LocalA-2026! |
| Organizador B | gestao.b@example.test | LocalB-2026! |
| Participante  | pessoa@example.test   | LocalP-2026! |

X-Api-Key: `local-passgate-26`. Apenas demo local, nunca reutilizar em produção. Verificar login e seed repetida quando implementados.

## Mapa dos artefatos

- [Proposal](proposal.md), [Design/HLD](design.md), [Matriz](requirements-matrix.md) e [Tasks](tasks.md).
- [PRD](docs/prd/PRD.md), [ADRs](docs/architecture/adrs/README.md), [interfaces](docs/interfaces/internal.md), [OpenAPI](docs/interfaces/partner.openapi.json), [contrato web](docs/interfaces/web.md).
- Features, spec/plan/contract/reports: `docs/features/`; cada diretório contém contrato e pasta vazia de relatórios.
- [Gates](docs/validation/harness.md), [catálogo de testes](docs/validation/test-catalog.md), [fluxo de avaliação](docs/validation/evaluator-flow.md), [release contract](docs/validation/release-contract.md).
- [AGENTS](AGENTS.md), [skills](.agents/skills/README.md), [workflow](docs/agents/workflow.md), [state](state/project-state.json), [guidelines](docs/engineering-guidelines.md).

## PRs da wave paralela

W5 F05/F06/F07; links, SHAs e sobreposição ainda não existem. Coordenador preenche somente com PRs reais mergeados. W6 verifica primeiro commit de cada PR anterior ao último dos demais.

## Decisões

Django + PostgreSQL para simplificar auth, CSRF, migrations e transações. R07 garantida por lock por evento e count após lock; prova condicional e testes de concorrência. Gateway: job persistido junto com ticket, worker separado, estado terminal protegido. Avaliação: sessão nova distinta do implementador, contrato por item, relatório append-only e integração final. Ver design/ADRs. Versões patch, configuração final e plataformas devem ser aprovadas em W0 e verificadas no harness.

## Probes após implementação

`scripts/partner_probe.py` verifica duas rajadas de carga e contrato HTTP; `scripts/browser_release_probe.py` automatiza passos 2–16 e captura screenshots/JSON. Ambos dependem da aplicação futura; o segundo também de Playwright Python + Chromium no container de testes. Ver o roteiro de avaliação. Scripts auxiliares não substituem testes por feature e fluxo final.
