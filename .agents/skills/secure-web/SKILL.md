---
name: secure-web
description: Implementar identidade, páginas e autorização sem vazamento.
---

# secure-web

## Quando usar
Implementar identidade, páginas e autorização sem vazamento.

## Entradas
F02/F05/F07, security design, HLD.

## Procedimento
1. Usar sessão Django e CSRF em POST, guards por papel e owner, hash de senha.
2. Validar formulário server-side e escapar template; nunca confiar no ator enviado.
3. Testar papéis, URL direta, POST forjado, CSRF, logout e isolamento por ID.
4. Para compra, usar reserve e tratar SoldOut; para operação usar serviço autorizado.

## Saída e gate
A06–A08, A18–A20, A28 e cross pertinentes com browser real.

## Regras
Ler AGENTS.md. Não inventar resultado, não copiar implementação de referência. Registrar bloqueios e respeitar ownership, contrato e avaliação independente.
