# F07 | Contrato de avaliação

Versão 2 proposta. Ambiente: checkout limpo do SHA, Docker/Compose e Git; `bash bin/up` e `bash bin/gates --feature F07` após implementados. Banco PostgreSQL real, dados sintéticos, projeto/porta exclusivos, gateway padrão para itens de tempo. O avaliador cria relatório novo sem alterar código.

## Fase LOCAL (antes do merge)

### C-F07-A25 (A25)

Preparação: Ingresso de outro evento, código inexistente, pending, declined, confirmed livre/usado, cancelado.

Procedimento: Executar tabela de decisão e 10 POSTs concorrentes para código livre; em cancelado testar POST com inválido e próprio.

PASS somente se: Mensagens R10 em ordem; exatamente uma entrada liberada; nenhum efeito nos demais; timestamp original preservado.

Teste: `TEST-A25`. Evidência: Fixtures código inválido/outro evento, cancelado, pending/declined/refunded, confirmado já usado e novo; corrida com duas sessões do dono.

### C-F07-A26 (A26)

Preparação: Evento publicado, ticket confirmado e slow pending + declined; relógio real.

Procedimento: Cancelar antes de 30s; consultar estados em até 10s, novamente após 45s; forjar edição/republicação; tentar cancelar draft e repetir cancelamento.

PASS somente se: Evento terminal; confirmed refunded, pending cancelled, declined intacto; nenhum ingresso reativado; ações inválidas negadas.

Teste: `TEST-A26`. Evidência: Criar slow 0003 + fast 0001, cancelar antes de 30s; medir <=10s, aguardar >=45s, repetir cancelamento e testar ações; corrida cancelamento/reserva/finalização.

### C-F07-A27 (A27)

Preparação: Ingressos mistos de dois canais com preço 10000,10000,15000 confirmados e um declined; um já utilizado.

Procedimento: Abrir painel, comparar ao oráculo; cancelar; recarregar.

PASS somente se: Antes 3/0/1/0/35000/0 (cap 3), depois 0/0/0/0/0/3; soma por preço congelado.

Teste: `TEST-A27`. Evidência: Fixture 10000+10000+15000 confirmados, 1 check-in, recusado e estornado; conferir receita 35000 e todas as contagens; após cancelar comparar zeros e estornos.

### C-F07-A28 (A28)

Preparação: A, B, P, anônimo; E de A com ticket.

Procedimento: Acessar URL e enviar check-in/cancelamento em cada sessão; conferir HTML e banco.

PASS somente se: A tem gestão completa; B, P, anônimo não leem nem alteram; resposta sem dados de A.

Teste: `TEST-A28`. Evidência: Browser A/B/P/visitante, POST forjado de B, verificar nenhum dado nem alteração; abrir gestão de A e executar ações.

### C-F07-A35 (A35)

Preparação: Dois estados válidos de evento/tickets em transações; consultas simultâneas.

Procedimento: Usar barreira para alterar capacity e status durante leituras; comparar cada resultado a snapshots completos.

PASS somente se: Sem mistura de dados de commits distintos, sem clamp escondendo ocupação inválida; painel sempre deriva do mesmo snapshot.

Teste: `TEST-A35`. Evidência: Forçar alternância de snapshots e comparar cada resultado a estados completos permitidos; verificar ausência de clamp de contagem negativa.

### C-F07-A36 (A36)

Preparação: Evento publicado cap 1 ou 2; conexões separadas; ticket pending/confirmed.

Procedimento: Forçar as duas ordens de lock em cada par: reserva×cancelar, finalize×cancelar, checkin×cancelar.

PASS somente se: Somente resultados serializáveis; no final 0 pending/confirmed, nenhum check-in liberado se cancelar ganhou; sem deadlock/5xx.

Teste: `TEST-A36`. Evidência: Barreiras e locks controlados em ambas as ordens; comparar sequência de commits e estado terminal.

### C-F07-X11 (X11)

Preparação: Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.

Procedimento: B tenta check-in e cancelamento de A, sem efeito e sem informação.

PASS somente se: Todas as ações operacionais respeitam guarda de dono.

Teste: `TEST-X11`. Evidência: B tenta check-in e cancelamento de A, sem efeito e sem informação.

### C-F07-X12 (X12)

Preparação: Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.

Procedimento: Cancelar publicado e tentar editar e republicar via POST; consultar catálogo.

PASS somente se: Cancelamento bloqueia publicação/edição e integra gestão em URL existente.

Teste: `TEST-X12`. Evidência: Cancelar publicado e tentar editar e republicar via POST; consultar catálogo.

### C-F07-X13 (X13)

Preparação: Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.

Procedimento: Combinar slow, fast, check-in, cancelar e esperar resultado tardio.

PASS somente se: Check-in/painel/cancelamento compartilham status, lock e preço; gateway tardio não revive.

Teste: `TEST-X13`. Evidência: Combinar slow, fast, check-in, cancelar e esperar resultado tardio.

## Fase INTEGRATED (após merge da wave)

Itens desta fase são explicitamente PENDING_INTEGRATION no relatório local; não contar como PASS e não exigir feature irmã no checkout isolado. Relatório integrado deve incluir todos os itens anteriores e os seguintes, sem pendências.

### C-F07-X14 (X14)

Preparação: Checkout integrado contendo ambas as features; realizar ações reais via UI/API, sem editar DB.

Procedimento: Fluxo browser: comprar, confirmar, validar código, cancelar, recarregar ambos.

PASS somente se: Com UI e operações integradas, uma compra web confirmada incrementa painel, permite check-in e, após cancelamento, some do catálogo e vira estornada em Meus ingressos.

Teste: `TEST-X14`. Evidência: Fluxo browser: comprar, confirmar, validar código, cancelar, recarregar ambos.

### C-F07-X15 (X15)

Preparação: Checkout integrado contendo ambas as features; realizar ações reais via UI/API, sem editar DB.

Procedimento: HTTP+browser: compra, consultar checkedIn, cancelar, verificar 404 e estorno.

PASS somente se: Com API e operações integradas, ingresso de parceiro conta na lotação e painel, permite check-in e consulta checkedIn; cancelar remove evento da lista, bloqueia POST, estorna e conserva consulta do ticket.

Teste: `TEST-X15`. Evidência: HTTP+browser: compra, consultar checkedIn, cancelar, verificar 404 e estorno.

## Mapeamento explícito

| Critério | Item      | Teste    | Fase       |
| -------- | --------- | -------- | ---------- |
| A25      | C-F07-A25 | TEST-A25 | local      |
| A26      | C-F07-A26 | TEST-A26 | local      |
| A27      | C-F07-A27 | TEST-A27 | local      |
| A28      | C-F07-A28 | TEST-A28 | local      |
| A35      | C-F07-A35 | TEST-A35 | local      |
| A36      | C-F07-A36 | TEST-A36 | local      |
| X11      | C-F07-X11 | TEST-X11 | local      |
| X12      | C-F07-X12 | TEST-X12 | local      |
| X13      | C-F07-X13 | TEST-X13 | local      |
| X14      | C-F07-X14 | TEST-X14 | integrated |
| X15      | C-F07-X15 | TEST-X15 | integrated |

Qualquer item aplicável sem evidência = FAIL. Fixture deve ser declarada; não usar fixture para substituir efeito real no integrado.
