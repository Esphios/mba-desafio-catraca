---
name: architecture-review
description: Revisar HLD/FDD/ADR e diagramas. Use quando a tarefa da wave exigir esta responsabilidade.
---

# architecture-review

## When to use
Revisar HLD/FDD/ADR e diagramas. Leia AGENTS.md e tarefas da feature primeiro.

## Inputs
design, FDDs, research, ADRs, internal ports. Confirme SHA, fase e ownership.

## Procedure
Mapear responsabilidades e dependências; testar hipóteses de snapshots e ordem de locks; comparar alternativas; revisar configurações, segurança e recursos; validar diagramas Mermaid e preparar ADR para mudanças.

## Validation
G0, render Mermaid, revisão da prova condicional e do contrato.

## Output and guardrails
Design/ADR aprovado ou bloqueio explícito. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
