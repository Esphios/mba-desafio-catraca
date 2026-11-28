# AGENTS.md | contrato de trabalho

A fonte normativa é o brief e os contratos rastreados. Consulte state/project-state.json e o trecho aplicável de tasks.md para identificar a fase. W0: leia proposal.md, design.md, PRD e matriz, conforme G0. Após baseline aprovada, não reabra W0 sem contradição normativa concreta ou mudança formalmente autorizada.

## Execução econômica
- Coordenador: leia estado, dependências e trechos normativos relevantes; use Git e scripts existentes para verificações determinísticas.
- Implementador: leia spec/plan/contract da feature, interfaces consumidas, requisitos/ADRs e skills aplicáveis. Consulte os demais documentos quando necessários, sem releitura integral por task.
- Avaliador: nova sessão independente por avaliação formal, SHA limpo, contrato, requisitos e testes aplicáveis; não receba o transcript nem o veredito do implementador.
- Um implementador por feature (sessão reutilizada enquanto disponível); commits materiais e testes por task, handoff conciso por etapa e completo ao fim da feature. Preserve revisões intermediárias obrigatórias. W1–W4 sequenciais; W5 mantém os três implementadores simultâneos exigidos. Sem delegação recursiva.
- Use os perfis de .codex/agents; Standard, modelo econômico para tarefas simples e modelo crítico quando a complexidade justificar. Não crie agentes para verificações determinísticas.
- Antes de avançar uma task, confirme o SHA completo e o diff no Git do projeto, ancestralidade e referência persistente no branch correto, e testes associados ao candidato. Se houver interrupção, preserve os commits e registre o próximo passo. Não aceite somente relatos; não repita despachos sem diagnosticar a causa. Não reescreva histórico durante a implementação.
- Somente o coordenador atualiza o estado global em transições relevantes. Despacho ou relato não é entrega. Não dispense registros e evidências obrigatórios. Siga docs/agents/workflow.md.

## Comandos
Planejamento: `python3 scripts/validate_docs.py`, `python3 scripts/verify_model.py`, `python3 scripts/test_baseline.py`, `python3 docs/validation/w0-audit/reproduce_mutations.py`; host sem Python: `docker run --rm -v "$PWD:/work:ro" -w /work python:3.12-slim python scripts/validate_docs.py` (idem verify_model). Após F01: `bash bin/up`, `bash bin/down`, `bash bin/gates`; candidato `bash bin/gates --feature Fxx`; release `bash bin/gates --release`, `bash bin/flow`. `python3 scripts/validate_evidence.py --release` requer Git e histórico real. Não confundir docs check com testes do produto. Default simulator, no payment key.

Runtime local usa CAT_PROJECT=catraca-demo, CAT_PORT=8080, CAT_PROFILE=demo e
CAT_GATEWAY_SCALE=1. Readiness em /health/ready. Contas sintéticas
gestao.a@example.test, gestao.b@example.test e pessoa@example.test têm senhas
no README. O banco não publica porta e bin/down preserva o volume.

## Invioláveis
- R01–R13 e API fixa; web/API partilham ledger. Todos os writes de evento sob event→ticket→job; preço histórico; nenhum status terminal revive; read snapshot único. Não modificar modelos, contratos ou código compartilhado fora de ownership.
- Auth server-side/owner em todas as rotas; CSRF no web; key antes de parse na API; não logar dados sensíveis.
- Providers aprovados/mergeados antes de consumidores. Wave paralela por worktrees; Compose project e porta distintos.
- Implementer testa, não avalia. Evaluator fresh context, SHA limpo e relatório novo, sem edição histórica. Local PASS não equivale a integrated PASS. Não inventar evidência.
- Coordenador escreve state; cada etapa tem teste, commit e handoff. Gate falho impede merge/release. Não alterar teste para esconder defeito.

## Mapa
PRD em docs/prd, FDDs/plan/contracts em docs/features, arquitetura/ADRs em docs/architecture, API/UI/internal em docs/interfaces, skills em .agents/skills, avaliação em docs/agents, testes/traceability/flow em docs/validation, scripts auxiliares em scripts, estado em state. README registra comandos/credenciais/PRs reais. Veja engineering-guidelines para padrões. Se ferramenta lê outro arquivo, apontar para este, sem regras conflitantes.

A trava `docs/validation/normative-lock.json` protege as fontes normativas desta revisão contra alterações acidentais. Não regenerar para fazer gate passar; mudança normativa exige amendment, revisão humana e commit explícito. Em W0 consulte `docs/validation/w0-audit/CORRECTIONS.md` e `docs/validation/w0-audit/APPROVAL-CHECKLIST.md`; nenhum PASS estrutural autoriza iniciar W1.
