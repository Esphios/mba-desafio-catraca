---
name: release-validation
description: Exercer produto integrado e entrega. Use quando a tarefa da wave exigir esta responsabilidade.
---

# release-validation

## When to use
Exercer produto integrado e entrega. Leia AGENTS.md e tarefas da feature primeiro.

## Inputs
main clean clone, full evaluator flow. Confirme SHA, fase e ownership.

## Procedure
Rodar scale=1; executar 18 passos + X14–X16; sem fixtures; conferir painel/receita/timing/API; comparar relatórios/history/PRs, README; run gates/down/up; corrigir via PR se falha.

## Validation
TEST-P01–P06 e todos A/X; validate_evidence --release.

## Output and guardrails
Release report com SHA e evidência, nunca inventar sucesso. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
