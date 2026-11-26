---
name: transactional-domain
description: Preservar capacidade, estados, preço e efeitos sob concorrência.
---

# transactional-domain

## Quando usar
Preservar capacidade, estados, preço e efeitos sob concorrência.

## Entradas
F03/F04/F07, transactions.md, ADR-002–005.

## Procedimento
1. Identificar todos os escritores; exigir atomic e lock event primeiro; count em query posterior.
2. Revalidar estado sob lock; manter ticket+job e cancelamento atômicos.
3. Testar transições inválidas, rollback, colisão, corrida e restart com PostgreSQL real.
4. Provar 30×5 em duas rodadas, executar stress e teste de pagamento tardio.

## Saída e gate
Invariantes e corridas verificadas; nenhum estado terminal revivido.

## Regras
Ler AGENTS.md. Não inventar resultado, não copiar implementação de referência. Registrar bloqueios e respeitar ownership, contrato e avaliação independente.
