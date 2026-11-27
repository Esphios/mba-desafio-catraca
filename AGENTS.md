# AGENTS.md | contrato de trabalho

Projeto greenfield, documentação pré-implementação. Comece por proposal.md, design.md, docs/prd/PRD.md, requirements-matrix.md, tasks.md e state/project-state.json. Depois leia spec/plan/contract da feature, interfaces consumidas e skills indicadas em tasks. A fonte normativa é o brief e os contratos rastreados. Nenhuma implementação existe neste pacote.

## Comandos
Planejamento: `python3 scripts/validate_docs.py`, `python3 scripts/verify_model.py`, `python3 scripts/test_baseline.py`, `python3 docs/validation/w0-audit/reproduce_mutations.py`; host sem Python: `docker run --rm -v "$PWD:/work:ro" -w /work python:3.12-slim python scripts/validate_docs.py` (idem verify_model). Após F01: `bash bin/up`, `bash bin/down`, `bash bin/gates`; candidato `bash bin/gates --feature Fxx`; release `bash bin/gates --release`, `bash bin/flow`. `python3 scripts/validate_evidence.py --release` requer Git e histórico real. Não confundir docs check com testes do produto. Default simulator, no payment key.

## Invioláveis
- R01–R13 e API fixa; web/API partilham ledger. Todos os writes de evento sob event→ticket→job; preço histórico; nenhum status terminal revive; read snapshot único. Não modificar modelos, contratos ou código compartilhado fora de ownership.
- Auth server-side/owner em todas as rotas; CSRF no web; key antes de parse na API; não logar dados sensíveis.
- Providers aprovados/mergeados antes de consumidores. Wave paralela por worktrees; Compose project e porta distintos.
- Implementer testa, não avalia. Evaluator fresh context, SHA limpo e relatório novo, sem edição histórica. Local PASS não equivale a integrated PASS. Não inventar evidência.
- Coordenador escreve state; cada etapa tem teste, commit e handoff. Gate falho impede merge/release. Não alterar teste para esconder defeito.

## Mapa
PRD em docs/prd, FDDs/plan/contracts em docs/features, arquitetura/ADRs em docs/architecture, API/UI/internal em docs/interfaces, skills em .agents/skills, avaliação em docs/agents, testes/traceability/flow em docs/validation, scripts auxiliares em scripts, estado em state. README registra comandos/credenciais/PRs reais. Veja engineering-guidelines para padrões. Se ferramenta lê outro arquivo, apontar para este, sem regras conflitantes.

A trava `docs/validation/normative-lock.json` protege as fontes normativas desta revisão contra alterações acidentais. Não regenerar para fazer gate passar; mudança normativa exige amendment, revisão humana e commit explícito. Em W0 consulte `docs/validation/w0-audit/CORRECTIONS.md` e `docs/validation/w0-audit/APPROVAL-CHECKLIST.md`; nenhum PASS estrutural autoriza iniciar W1.
