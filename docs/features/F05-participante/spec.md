# F05 | FDD: Jornada de participante

Status: proposto · Wave W5 · Fonte normativa: PRD e design.

## Resultado e interfaces

Provides: Vitrine pública, compra autenticada e página de ingressos pessoais.

Consumes: F02: participante/sessão; F03: catálogo; F04: reserve e consulta.

Ownership: participant web. Não alterar módulos de outras features sem amendment.

## Low-level design

A vitrine é um adapter de leitura do catálogo; não recalcula disponibilidade. GET `/` e `/eventos/<id>/` exibem nome, local, data, preço e ação/estado de esgotado. GET é público; compra POST `/eventos/<id>/comprar/` exige participante e CSRF. O cartão é uma string transitória, não ecoada em erro. `reserve` recebe ID do Actor, email da sessão e cartão. Em sucesso PRG para `/meus-ingressos/` com mensagem de compra registrada; o status exibido vem da consulta real, não flash. Erro sold_out mostra `Ingressos esgotados`, evento indisponível 404 genérico. Formulário oculto se disponibilidade zero, mas POST sempre revalida.

**Meus ingressos:** consulta por participant_id; join com evento mesmo cancelado; status exato em português e código de cada ticket. Sem filtro por e-mail, sem ingressos de parceiro. A conta de organizador não compra pela vitrine; pode navegar como visitante. Anônimo pode visitar; a ação de navegação para login é GET, com retorno seguro ao detalhe. POST protegido sem sessão responde 403 sem escrita, mesmo com CSRF válido.

**Observação temporal de A19:** capturar pending real do primeiro GET pós-PRG, sem status fabricado, e confirmar até 5s desde created_at. Registrar timestamps DB e relógio monotônico; se o primeiro GET já for terminal, o caso não é PASS, investigar latência e repetir em ambiente isolado sem ocultar falha, sem atrasar worker nem estender prazo.

**Handoff:** seletores acessíveis por labels/role; `data-testid` estáveis `event-card`, `purchase-submit`, `ticket-list`, `ticket-status`, `ticket-code`, `sold-out`. Cobrir fluxos no browser real. Testes locais usam fixture cancelada para filtro; efeito de cancelamento executado pela gestão só no integrado X14.

## Critérios e limites
| ID | Fase | Aceite |
| --- | --- | --- |
| A18 | local | Vitrine exibe só publicados não cancelados, inclusive esgotados com texto exato Ingressos esgotados; tentativa concorrente recebe mesma mensagem. |
| A19 | local | Participante cria conta, compra pela vitrine, vê evento/status/código em Meus ingressos; pending imediato e confirmado em até 5s para 0001. |
| A20 | local | Meus ingressos filtra por participant_id autenticado, não por e-mail, e mostra todos os cinco rótulos; visitante não compra. |
| X06 | local | Sessão define dono do ingresso; anônimo e outra conta não veem compra pessoal. |
| X07 | local | A publicação e as vagas calculadas por F03 chegam à vitrine; draft/cancelled não são exibidos, inclusive fixture cancelada. A ação real de cancelar é validada em X14. |
| X08 | local | Compra web usa reserve e worker; pendente ocupa e recusa libera na vitrine. |

## Evolução e rollback
Mudança de contrato exige ADR/amendment aprovado e reavaliação de consumidores. Em falha de implementação, corrigir em commit novo; não alterar migrations aplicadas nem relatórios. No MVP local usar ambiente de testes descartável para rollback de schema; não apagar volume de demonstração.
