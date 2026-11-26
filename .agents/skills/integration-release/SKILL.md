---
name: integration-release
description: Executar fluxo público completo e gate de entrega.
---

# integration-release

## Quando usar
Executar fluxo público completo e gate de entrega.

## Entradas
main SHA, evaluator-flow.md, release-contract, README.

## Procedimento
1. Clone limpo, modo padrão, seed; iniciar serviços com um comando.
2. Rodar passos 1–17, X14–X16, real timing e duas rodadas concorrentes.
3. Conferir P01–P06, imutabilidade/estado e sobreposição de PRs.
4. Salvar relatório, bloquear release em falha; após correções repetir integralmente.

## Saída e gate
Fluxo inteiro verde, SHA e evidências reais, release sem regressão.

## Regras
Ler AGENTS.md. Não inventar resultado, não copiar implementação de referência. Registrar bloqueios e respeitar ownership, contrato e avaliação independente.
