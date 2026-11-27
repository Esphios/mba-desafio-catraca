# F07 | Plano de implementação

Entrada: baseline W0 aprovada, dependências F02, F03, F04 integradas e aprovadas, branch exclusiva. Skills: transaction-safety, secure-boundaries, concurrency-validation, feature-implementation.

## T-F07-01

**Entrega:** Implementar decisão de check-in e escrita única; formulário/POST com autorização.

**Validação:** lint, checks do framework e testes já implementados; fase 1 não exige endpoints futuros.
- `TEST-A25` (A25): Executar tabela de decisão e 10 POSTs concorrentes para código livre; em cancelado testar POST com inválido e próprio. Resultado: Mensagens R10 em ordem; exatamente uma entrada liberada; nenhum efeito nos demais; timestamp original preservado.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F07-02

**Entrega:** Implementar cancelamento terminal e testes gateway tardio + corrida.

**Validação:** lint, checks do framework e testes já implementados; fase 2 não exige endpoints futuros.
- `TEST-A26` (A26): Cancelar antes de 30s; consultar estados em até 10s, novamente após 45s; forjar edição/republicação; tentar cancelar draft e repetir cancelamento. Resultado: Evento terminal; confirmed refunded, pending cancelled, declined intacto; nenhum ingresso reativado; ações inválidas negadas.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F07-03

**Entrega:** Construir painel agregado, partial e URLconf no módulo F07; no gate local, ativá-los pelos hooks settings-driven precriados, sem editar wiring compartilhado.

**Validação:** lint, checks do framework e testes já implementados; fase 3 não exige endpoints futuros.
- `TEST-A27` (A27): Abrir painel, comparar ao oráculo; cancelar; recarregar. Resultado: Antes 3/0/1/0/35000/0 (cap 3), depois 0/0/0/0/0/3; soma por preço congelado.
- `TEST-A28` (A28): Com settings de teste apontando hooks aos componentes reais F07, acessar URL e enviar check-in/cancelamento em cada sessão; conferir HTML e banco. Resultado: A tem gestão completa; B, P, anônimo não leem nem alteram; resposta sem dados de A; nenhum arquivo compartilhado foi editado.
- `TEST-A35` (A35): Usar barreira para alterar capacity e status durante leituras; comparar cada resultado a snapshots completos. Resultado: Sem mistura de dados de commits distintos, sem clamp escondendo ocupação inválida; painel sempre deriva do mesmo snapshot.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F07-04

**Entrega:** Rodar concorrência adversarial e avaliação local; integrar X14/X15 posteriormente.

**Validação:** lint, checks do framework e testes já implementados; fase 4 não exige endpoints futuros.
- `TEST-A25` (A25): Executar tabela de decisão e 10 POSTs concorrentes para código livre; em cancelado testar POST com inválido e próprio. Resultado: Mensagens R10 em ordem; exatamente uma entrada liberada; nenhum efeito nos demais; timestamp original preservado.
- `TEST-A26` (A26): Cancelar antes de 30s; consultar estados em até 10s, novamente após 45s; forjar edição/republicação; tentar cancelar draft e repetir cancelamento. Resultado: Evento terminal; confirmed refunded, pending cancelled, declined intacto; nenhum ingresso reativado; ações inválidas negadas.
- `TEST-A27` (A27): Abrir painel, comparar ao oráculo; cancelar; recarregar. Resultado: Antes 3/0/1/0/35000/0 (cap 3), depois 0/0/0/0/0/3; soma por preço congelado.
- `TEST-A28` (A28): Acessar URL e enviar check-in/cancelamento em cada sessão; conferir HTML e banco. Resultado: A tem gestão completa; B, P, anônimo não leem nem alteram; resposta sem dados de A.
- `TEST-A35` (A35): Usar barreira para alterar capacity e status durante leituras; comparar cada resultado a snapshots completos. Resultado: Sem mistura de dados de commits distintos, sem clamp escondendo ocupação inválida; painel sempre deriva do mesmo snapshot.
- `TEST-A36` (A36): Forçar as duas ordens de lock em cada par: reserva×cancelar, finalize×cancelar, checkin×cancelar. Resultado: Somente resultados serializáveis; no final 0 pending/confirmed, nenhum check-in liberado se cancelar ganhou; sem deadlock/5xx.
- `TEST-X11` (X11): B tenta check-in e cancelamento de A, sem efeito e sem informação. Resultado: Todas as ações operacionais respeitam guarda de dono.
- `TEST-X12` (X12): Cancelar publicado e tentar editar e republicar via POST; consultar catálogo. Resultado: Cancelamento bloqueia publicação/edição e integra gestão em URL existente.
- `TEST-X13` (X13): Combinar slow, fast, check-in, cancelar e esperar resultado tardio. Resultado: Check-in/painel/cancelamento compartilham status, lock e preço; gateway tardio não revive.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## Integração posterior
- Após local PASS e merge, o coordenador troca os defaults do composition root em commit de wiring separado, repete TEST-A28 no checkout integrado e registra o SHA antes de X14/X15.
- X14 / TEST-X14: Fluxo browser: comprar, confirmar, validar código, cancelar, recarregar ambos.
- X15 / TEST-X15: HTTP+browser: compra, consultar checkedIn, cancelar, verificar 404 e estorno.

## Handoff
Entregar SHA limpo, base SHA, interfaces, comandos, logs redigidos e desvios. Avaliador novo, sem histórico de conversa, julga apenas contrato e evidência. Coordenador integra após local PASS; relatório final da feature exige também itens integrados, se houver.
