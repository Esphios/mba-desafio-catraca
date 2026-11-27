---
name: partner-api-contract
description: Preservar contrato de parceiro. Use quando a tarefa da wave exigir esta responsabilidade.
---

# partner-api-contract

## When to use
Preservar contrato de parceiro. Leia AGENTS.md e tarefas da feature primeiro.

## Inputs
OpenAPI, PRD, ledger ports. Confirme SHA, fase e ownership.

## Procedure
Autenticar antes de parser; conferir JSON errors e precedence; retornar campos exatos; key compare, UUID inválido not found; evitar redirect e PII; testar malformed body e cross-channel.

## Validation
TEST-A21–A24,A34,X09,X10,X16.

## Output and guardrails
API e contract tests; não adicionar requisito de conta web. Se faltar pré-requisito, registre bloqueio, não fabrique evidência. Não substituir regra normativa por conveniência.
