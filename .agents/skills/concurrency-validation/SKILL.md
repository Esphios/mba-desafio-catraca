---
name: concurrency-validation
description: Provar corridas e testar sensibilidade. Use quando a tarefa da wave exigir esta responsabilidade.
---

# concurrency-validation

## When to use
Provar corridas e testar sensibilidade. Leia AGENTS.md e tarefas da feature primeiro.

## Inputs
transactions, PostgreSQL, HTTP probe. Confirme SHA, fase e ownership.

## Procedure
Usar conexões e processos distintos; barrier, fresh event, approved cards; registrar histograma e DB final; forçar ordens de lock; simular bypass em cópia temporária e provar fail; restaurar; medir default deadlines.

## Validation
TEST-A14,A24,A33,A35,A36,X16; 10 DB rounds e 2 HTTP.

## Output and guardrails
Resultados reais e invariantes, sem afirmar prova absoluta por teste. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
