---
name: harness-engineering
description: Construir ambiente e gates reproduzíveis. Use quando a tarefa da wave exigir esta responsabilidade.
---

# harness-engineering

## When to use
Construir ambiente e gates reproduzíveis. Leia AGENTS.md e tarefas da feature primeiro.

## Inputs
harness spec, Docker, lockfile. Confirme SHA, fase e ownership.

## Procedure
Validar prereqs reais; boot one-shot migrate/seed; health DB/web/worker; separar projects/ports; run gates com cleanup e exit propagation; repetir down/up; inject failure; document defaults.

## Validation
TEST-A01–A05,A29,A37; prova clone limpo e gate negativo.

## Output and guardrails
bin scripts, compose, CI e logs; não limpar projetos alheios. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
