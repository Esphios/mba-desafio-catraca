---
name: implement-feature
description: Executar FDD/plano/contrato em uma branch, entregar handoff sem autoavaliar.
---

# implement-feature

## Quando usar
Executar FDD/plano/contrato em uma branch, entregar handoff sem autoavaliar.

## Entradas
Feature, base SHA, tasks, spec, plan, contract, guidelines.

## Procedimento
1. Verificar dependências e ownership; criar worktree se instruído.
2. Implementar etapa mínima e testes rastreáveis; executar gate da etapa, corrigir antes de seguir.
3. Executar contrato local como pré-check, sem declarar avaliação independente.
4. Commit, registrar SHA e handoff; deixar avaliação para contexto novo.

## Saída e gate
Código e testes no SHA, sem alteração de contrato não aprovada; handoff.

## Regras
Ler AGENTS.md. Não inventar resultado, não copiar implementação de referência. Registrar bloqueios e respeitar ownership, contrato e avaliação independente.
