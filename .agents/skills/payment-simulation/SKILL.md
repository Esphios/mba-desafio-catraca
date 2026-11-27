---
name: payment-simulation
description: Implementar gateway durável e deadlines. Use quando a tarefa da wave exigir esta responsabilidade.
---

# payment-simulation

## When to use
Implementar gateway durável e deadlines. Leia AGENTS.md e tarefas da feature primeiro.

## Inputs
gateway table, ledger, worker spec. Confirme SHA, fase e ownership.

## Procedure
Validar ASCII 16; classificar só em memória; due_at DB clock após lock; persistir job com ticket; resolver candidato sob ordem comum; confirmar idempotência/restart; medir real scale e fila lag.

## Validation
TEST-A13,A15,A16,A33,X04.

## Output and guardrails
Worker e testes; sem PAN, nenhuma chave real. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
