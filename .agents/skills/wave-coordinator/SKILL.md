---
name: wave-coordinator
description: Orquestrar DAG, PRs, worktrees, tracking e integração.
---

# wave-coordinator

## Quando usar
Orquestrar DAG, PRs, worktrees, tracking e integração.

## Entradas
PRD, tasks, state, workflow, contratos.

## Procedimento
1. Confirmar baseline e dependências mergeadas; isolar worktrees/portas.
2. Iniciar W5 simultânea, preservar commits genuínos e PRs; não alterar timestamps.
3. Revisar ownership e relatórios; merges sequenciais e regressão.
4. Atualizar estado com paths e SHA reais, provar sobreposição, preencher README.

## Saída e gate
P03–P06 e dependências verificadas; main íntegra.

## Regras
Ler AGENTS.md. Não inventar resultado, não copiar implementação de referência. Registrar bloqueios e respeitar ownership, contrato e avaliação independente.
