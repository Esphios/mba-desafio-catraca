---
name: wave-orchestration
description: Planejar e integrar branches paralelas. Use quando a tarefa da wave exigir esta responsabilidade.
---

# wave-orchestration

## When to use
Planejar e integrar branches paralelas. Leia AGENTS.md e tarefas da feature primeiro.

## Inputs
PRD graph, state, handoffs. Confirme SHA, fase e ownership.

## Procedure
Confirmar provider merged+local PASS e interface congelada; criar worktrees/ports; W1–W4 sequenciais, um implementador por feature; W5 despachar F05/F06/F07 simultaneamente. Reutilizar implementador nas tasks e correções; conferir cada commit material, referência persistente e testes antes de avançar. Avaliar por sessão distinta conforme contrato; merge serial com gates; reavaliar quando exigido; coletar GitHub PR overlap real. Usar Git/scripts diretamente; recuperar checkpoint antes de redespachar.

## Validation
TEST-P01,P04,P05; G5/G6.

## Output and guardrails
State e histórico verificável; sem backdate. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
