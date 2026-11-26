---
name: architecture-review
description: Definir ou revisar HLD/FDD, ADRs e diagramas em greenfield.
---

# architecture-review

## Quando usar
Definir ou revisar HLD/FDD, ADRs e diagramas em greenfield.

## Entradas
proposal, PRD, design, ADR, pesquisa, FDDs.

## Procedimento
1. Identificar fronteiras, invariantes, interfaces, estados e requisitos não funcionais.
2. Pesquisar fontes oficiais em duas fases: alternativas e aprofundamento; registrar versões e lacunas.
3. Avaliar trade-offs, ADR para decisões relevantes, diagramas C4/Mermaid sem classes inventadas.
4. Validar lock/atomicidade, falhas, segurança e interfaces; depois do código confrontar arquitetura com implementação.

## Saída e gate
HLD/FDD/ADRs e diagramas consistentes; hipóteses mensuráveis; gate documental.

## Regras
Ler AGENTS.md. Não inventar resultado, não copiar implementação de referência. Registrar bloqueios e respeitar ownership, contrato e avaliação independente.
