---
name: prd-and-traceability
description: Produzir ou revisar PRD e matriz sem inventar requisitos.
---

# prd-and-traceability

## Quando usar
Produzir ou revisar PRD e matriz sem inventar requisitos.

## Entradas
Brief, PRD, proposal, traceability.json, matriz, contratos.

## Procedimento
1. Separar regra normativa de escolha técnica e fora de escopo.
2. Atribuir ID estável, critério observável e evidência negativa quando pertinente.
3. Mapear cada regra a A/X/P; cada aresta do DAG a um X; cada critério a item, teste, tarefa.
4. Atualizar documentos e manifesto juntos; executar checker; revisão humana verifica semântica.

## Saída e gate
PRD/matriz coerentes, nenhuma regra/aresta órfã, sem status fictício.

## Regras
Ler AGENTS.md. Não inventar resultado, não copiar implementação de referência. Registrar bloqueios e respeitar ownership, contrato e avaliação independente.
