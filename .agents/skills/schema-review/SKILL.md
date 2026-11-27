---
name: schema-review
description: Projetar e validar modelo relacional. Use quando a tarefa da wave exigir esta responsabilidade.
---

# schema-review

## When to use
Projetar e validar modelo relacional. Leia AGENTS.md e tarefas da feature primeiro.

## Inputs
logical model, migration, DB real. Confirme SHA, fase e ownership.

## Procedure
Criar custom User antes de migrations; aplicar FKs e CHECKs locais, unique code/email/job, indexes; não usar clock em CHECK; testar fresh e upgrade; validar union web/partner; revisar plano de queries.

## Validation
TEST-A05,A11,A32; migrate e no drift.

## Output and guardrails
Migration revisada; sem bypass de locks. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
