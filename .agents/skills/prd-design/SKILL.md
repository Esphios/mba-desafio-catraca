---
name: prd-design
description: Revisar produto e rastreabilidade antes de implementação. Use quando a tarefa da wave exigir esta responsabilidade.
---

# prd-design

## When to use
Revisar produto e rastreabilidade antes de implementação. Leia AGENTS.md e tarefas da feature primeiro.

## Inputs
brief, PRD, matriz, traceability.json. Confirme SHA, fase e ownership.

## Procedure
Conferir R01–R13 e contrato fixo; separar regra obrigatória de decisão; conferir todo Provides/Consumes e cada aresta; identificar aceite que depende de sibling e classificar integrated; atualizar matriz/contrato/plan/test catalog juntos; submeter W0.

## Validation
validate_docs + revisão humana dos cenários e API; nenhum requisito sem teste.

## Output and guardrails
PRD/matriz e decisão de kickoff; não alterar brief. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
