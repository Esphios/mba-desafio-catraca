---
name: independent-evaluator
description: Avaliar contrato com contexto separado e evidência append-only.
---

# independent-evaluator

## Quando usar
Avaliar contrato com contexto separado e evidência append-only.

## Entradas
SHA, contrato, PRD, harness, template de relatório.

## Procedimento
1. Verificar independência da sessão, checkout limpo e ambiente isolado.
2. Executar cada item, sem corrigir código; coletar evidências e negativos.
3. Registrar PASS/FAIL/BLOCKED por item e relatório novo com data/SHA/ferramenta/modelo.
4. Derrubar ambiente, entregar relatório ao coordenador; nova avaliação após correção.

## Saída e gate
Relatório real, imutável, sem N/A obrigatório final; veredito baseado em observação.

## Regras
Ler AGENTS.md. Não inventar resultado, não copiar implementação de referência. Registrar bloqueios e respeitar ownership, contrato e avaliação independente.
