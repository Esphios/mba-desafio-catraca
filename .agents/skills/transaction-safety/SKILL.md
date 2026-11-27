---
name: transaction-safety
description: Implementar invariantes e locks reais. Use quando a tarefa da wave exigir esta responsabilidade.
---

# transaction-safety

## When to use
Implementar invariantes e locks reais. Leia AGENTS.md e tarefas da feature primeiro.

## Inputs
transactions, schema, interface registry. Confirme SHA, fase e ownership.

## Procedure
Adquirir event first dentro de atomic; recontar após lock; manter preço/job no commit; revalidar estado; evitar I/O e sleep; usar savepoints para colisão; teste rollback e duas ordens de corrida; review queries do painel.

## Validation
TEST-A14,A32,A33,A35,A36,X05.

## Output and guardrails
Prova condicional + evidência PostgreSQL real; sem mutex de processo. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
