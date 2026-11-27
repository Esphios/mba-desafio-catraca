---
name: independent-evaluation
description: Julgar contrato sem viés de implementação. Use quando a tarefa da wave exigir esta responsabilidade.
---

# independent-evaluation

## When to use
Julgar contrato sem viés de implementação. Leia AGENTS.md e tarefas da feature primeiro.

## Inputs
clean SHA, contract, report template. Confirme SHA, fase e ownership.

## Procedure
Sessão nova; confirmar metadados; executar cada item; observar resultado, timing real e efeitos; evidência por item; pending só na fase explícita; gerar Markdown/JSON novos; não editar código nem contrato.

## Validation
validate_evidence em fase correta; FAIL/BLOCKED impede aprovação.

## Output and guardrails
Relatório imutável, conclusão factual. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
