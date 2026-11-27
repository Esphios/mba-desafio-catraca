# Proposal | Catraca

Status: aprovado na ratificação W0 de 2026-11-27.

## Contexto

Catraca é uma bilheteria local de MVP para pequenos eventos. O risco dominante é a inconsistência entre interfaces, reserva concorrente, pagamento assíncrono e operação do evento. O projeto deve demonstrar desenvolvimento agentic com avaliação independente, não somente funcionalidades isoladas.

## Proposta de valor

Visitantes descobrem eventos; participantes compram uma unidade e acompanham seu código; organizadores controlam publicação, lotação, entrada e cancelamento; parceiros vendem pela API fixa. O sucesso é medido no fluxo completo com compras reais simuladas e concorrência.

## Escopo e fronteiras

R01–R13, três endpoints, seed, Docker, comandos de lifecycle/gates, PRD/FDD/plan/contract, relatórios imutáveis, estado e PRs paralelos. Fora de escopo: gateway real, deploy, notificações, app móvel, assentos, compra múltipla, transferência, cancelamento individual e atualização em tempo real.

## Decisões propostas

Django 5.2 LTS e PostgreSQL 17 em Docker, templates server-side, worker durável na mesma base, uma lógica de domínio para web/API, locks por evento e leitura consistente. Sem Redis/broker/frontend SPA; observabilidade básica por logs e health, sem stack de monitoramento obrigatória. O stack foi escolhido por robustez de autenticação/CSRF, migrations e transações nativas e baixo custo operacional.

## Alternativas

Aplicação SPA + API ou microserviços aumentariam contratos, deploy local e pontos de falha; mutex de processo não prova concorrência multirréplica; fila em memória perde pagamentos. O monólito modular com worker separado mantém o domínio centralizado e facilita isolamento de testes.

## Critérios de sucesso

Todas as regras rastreadas; dois eventos cap 5 com 30 POSTs concorrentes cada, exatamente 5/25; cancelamento terminal dentro do prazo; painel com receita histórica correta; nenhuma leitura/escrita cruzada; ambiente reproduzível; todos os contratos aprovados de forma independente; main final passa fluxo de 18 passos.

## Riscos e mitigação

| Risco                    | Impacto               | Mitigação                                          | Prova            |
| ------------------------ | --------------------- | -------------------------------------------------- | ---------------- |
| Race de venda/edição     | sobrevenda            | lock por evento + count após lock                  | TEST-A14,X05,A36 |
| Gateway tardio           | revive cancelado      | estado terminal + recheck sob lock                 | TEST-A16,A26     |
| Worker indisponível      | pagamento perdido     | job persistente, readiness e restart               | TEST-A33,X04     |
| Snapshot misto           | painel inconsistente  | single statement                                   | TEST-A35         |
| Identidade forjada       | vazamento             | guards e ownership no serviço                      | TEST-A07,A30,X11 |
| Avaliação autoindulgente | falso verde           | sessão nova, relatório imutável, gate de evidência | TEST-P03,A37     |
| Wave irmã não integrada  | reprovação artificial | contrato local e integrado distintos               | TEST-X14–X16     |
| Flakiness temporal       | prazo falso           | margem e relógio monotônico, modo padrão           | TEST-A15,A24     |

## Aprovação requerida

O proprietário aprova stack, convenção UTC/BRL, limites técnicos de entrada, delays determinísticos, escopo da telemetria e distribuição de features. As regras do brief e o contrato fixo não são negociáveis.
