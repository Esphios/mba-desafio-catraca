---
name: browser-validation
description: Validar comportamento UI real. Use quando a tarefa da wave exigir esta responsabilidade.
---

# browser-validation

## When to use
Validar comportamento UI real. Leia AGENTS.md e tarefas da feature primeiro.

## Inputs
web contract, Playwright, fixture factory. Confirme SHA, fase e ownership.

## Procedure
Usar roles/labels e test IDs estáveis; contas isoladas; navegar signup/login/compra/tickets; capturar mensagens e screenshots; recarregar sem polling infinito; testar IDOR e CSRF; nenhum DB edit no release.

## Validation
TEST-A18–A20,X06–X08,X14 e fluxo 1–14.

## Output and guardrails
Browser suite e evidência redigida. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
