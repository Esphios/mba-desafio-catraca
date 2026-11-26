---
name: partner-contract
description: Implementar e verificar API fixa sem divergência de DTO/erros.
---

# partner-contract

## Quando usar
Implementar e verificar API fixa sem divergência de DTO/erros.

## Entradas
F06, design seção 7, contrato e probe.

## Procedimento
1. Autenticar antes de parser; validar JSON e campos antes de lookup; converter erro por precedência.
2. Usar DTO catalog e reserve/consulta ledger; sem regras duplicadas.
3. Testar shapes exatos, ausência/chave inválida, IDs inválidos e todos os status.
4. Executar probe em dois eventos novos e comprovar 5/25; consultar aceitos após gateway.

## Saída e gate
A21–A24, X09–X10; X15–X16 no integrado.

## Regras
Ler AGENTS.md. Não inventar resultado, não copiar implementação de referência. Registrar bloqueios e respeitar ownership, contrato e avaliação independente.
