# Fluxo de avaliação integrado | roteiro executável por agente

Pré-condições: main integrada, clone novo, ambiente padrão sem gateway real, browser e cliente HTTP; seed do README. Registrar WEB/API, chave (não incluir segredo no relatório), SHA, data e IDs/códigos E1–E5/T2–T6/C1–C6; usar data relativa (mês seguinte). Executar passos em ordem; o agente pode automatizar por Playwright + HTTP, mas não modificar DB para obter resultados nesse fluxo. Cronometrar passos 6–8 e 12–14. Repetir fluxo após correções em ambiente novo. O roteiro detalha o fluxo público do brief em formato de oráculo.

| Passo | Ação | Resultado e evidência |
|---|---|---|
| 1 | Clone vazio; up do README | Página responde, 3 contas seed e serviços saudáveis; log e SHA (A01) |
| 2 | A cria E1 cap 2 preço 10000 futuro como draft; deslogar; GET partner/events | E1 ausente ambos (A10,A21) |
| 3 | A tenta data ontem | rejeição sem criar (A09) |
| 4 | A publica E1; guardar ID | aparece web/API, 2 vagas, 10000 centavos (A10,X09) |
| 5 | cadastrar participante novo e comprar E1 final 0001 | Meus ingressos pending imediatamente e confirmed <=5s; C1 anotado (A19) |
| 6 | POST partner E1 final 0004, T2/C2 | 202 pending; vagas 0 (A22) |
| 7 | Antes de 30s de T2, tentar compra E1 final 0001 e recarregar vitrine | 409 sold_out, Ingressos esgotados (A18,A22) |
| 8 | Aos 45s de T2, consultar | declined, 1 vaga; comprar T3 0001 e confirmar <=5s (A15) |
| 9 | A reduz cap 1 (nega), aumenta para 3 e preço 15000; comprar T4 0001, confirmar | painel confirmados 3, pendentes 0, check-ins 0, vagas 0, receita R$ 350,00, estornados 0 (A11,A27) |
| 10 | Check-in C1, repetir, C2, ZZZZZZZZ; copiar URL | Entrada liberada; Ingresso já utilizado; Ingresso não confirmado; Ingresso inválido para este evento; painel check-ins 1 (A25) |
| 11 | B não vê E1 nem URL; B cria/publica E2 cap 1 preço 2000, compra C3 pela API; participante seed e anônimo tentam URL; A usa C3 no E1 | nenhum dado de E1 nas sessões indevidas; C3 inválido para E1 (A07,A28) |
| 12 | A cria/publica E3 cap 5 preço 5000; comprar T5 0003 e T6 0001; esperar T6 confirmed; cancelar antes dos 30s de T5 | cancelamento efetivo (A26) |
| 13 | Consultar catálogo, API, compra, tickets e gestão E3 | fora dos dois canais; POST 404 event_not_available; T6 refunded, T5 cancelled <=10s; edição negada (X12,X15) |
| 14 | Após 45s de T5, consultar e tentar check-in C6 | T5 segue cancelled; Evento cancelado; painel confirmados/pendentes/check-ins/vagas/receita zero, estornados 1 (A26,A27) |
| 15 | E4 e E5 novos, cap 5 preço 1000; 30 POST simultâneos 0001 em cada | por evento 5×202, 25×409, sem outros; painel 5 confirmados e 0 vagas <=10s (A24) |
| 16 | 3 rotas sem key e errada; compra cartão 123; ticket inexistente | 401 unauthorized nas 6; 422 invalid_request; 404 ticket_not_found (A23) |
| 17 | gates, down, checar porta/containers, up e login seed | exit 0, nenhum serviço residual, seed repetível (A02,A03) |
| 18 | Inspecionar README, PRD, FDD/plan/contract, relatórios, state, AGENTS e PRs | todos P01–P06; verificar cada report via git log, timestamps de PRs e SHA; sem arquivo fake |

## Oráculos adicionais obrigatórios do design

X14: compra web aparece no painel e permite check-in; após cancelar, Meus ingressos mostra refunded. X15: compra partner entra no painel, check-in reflete `checkedIn`, cancelamento remove catálogo/estorna. X16: capacidade 1, web e API simultâneas com barrier, uma aceitação, outra esgotada; ticket web consultável na API, ticket partner de mesmo e-mail não aparece em Meus ingressos. A25: POST direto em evento cancelado com código inexistente deve respeitar prioridade de inválido; UI pode mostrar Evento cancelado no lugar do campo. Confirmar preço histórico e check-ins filtrados após estorno. A26: corrida cancelamento × finalize/reserve/check-in em ambiente de teste; verificar nenhuma entrada após cancelamento. A23: body e códigos exatos, precedência chave→payload→evento→lotação, sem redirect.

## Captura de evidência

Para cada passo: data UTC, IDs, status HTTP/JSON redigido, screenshot UI, resultado, tempo monotônico quando aplicável. Para fluxo de carga registrar histogramas e IDs dos 5 aceitos. Para processo, `git log --format='%h %ad' --date=iso -- <report>` deve apontar um commit por relatório criado. Consultar PRs reais e lista de commits, não só timestamps locais. Se fluxo falhar, relatar e bloquear entrega.
