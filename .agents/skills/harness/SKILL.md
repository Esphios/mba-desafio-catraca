---
name: harness
description: Construir ambiente autocontido, seed, gates e isolamento.
---

# harness

## Quando usar
Construir ambiente autocontido, seed, gates e isolamento.

## Entradas
F01, HLD, harness, guidelines.

## Procedimento
1. Fixar versões e scripts portáveis; Docker/Compose healthchecks e migração one-shot.
2. Seed idempotente; DB real isolado por projeto; worker e web prontos.
3. Provar clone limpo, down, restart e gate que falha de verdade.
4. Capturar stdout e exit code, eliminar segredos, registrar comandos no README.

## Saída e gate
A01–A05 e X01, nenhum serviço residual, testes reais e DB isolado.

## Regras
Ler AGENTS.md. Não inventar resultado, não copiar implementação de referência. Registrar bloqueios e respeitar ownership, contrato e avaliação independente.
