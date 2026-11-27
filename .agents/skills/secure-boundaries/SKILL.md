---
name: secure-boundaries
description: Implementar autenticação, autorização e input safety. Use quando a tarefa da wave exigir esta responsabilidade.
---

# secure-boundaries

## When to use
Implementar autenticação, autorização e input safety. Leia AGENTS.md e tarefas da feature primeiro.

## Inputs
security, web/internal contracts. Confirme SHA, fase e ownership.

## Procedure
Derivar Actor da sessão; guards e ownership em GET/POST; CSRF e safe redirects; nunca usar papel/owner externo; verificar cross-account e logs; API key não sessão.

## Validation
TEST-A07,A08,A17,A30,X11,A28.

## Output and guardrails
Guard e testes negativos; não desabilitar CSRF globalmente. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
