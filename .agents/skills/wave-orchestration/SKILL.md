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
Confirmar provider merged+local PASS; criar worktrees/ports; despachar agentes simultâneos; commits úteis; avaliar por sessão distinta; merge serial com gates; reavaliar após mudanças; coletar GitHub PR overlap real.

## Validation
TEST-P01,P04,P05; G5/G6.

## Output and guardrails
State e histórico verificável; sem backdate. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
