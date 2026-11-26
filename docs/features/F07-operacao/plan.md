# F07 | Plano de implementação

Prerequisitos: baseline aprovada, dependências F02, F03, F04 mergeadas; branch `feat/f07-operacao`; ler spec, contrato, guidelines, skills e estado.

## T-F07-01 | Etapa 1

- [ ] Implementar check-in com lock do evento, precedência e mensagem exatas; adicionar formulário à gestão.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A25`: Fixtures código inválido/outro evento, cancelado, pending/declined/refunded, confirmado já usado e novo; corrida com duas sessões do dono. Esperado: Check-in aplica exatamente as cinco mensagens na ordem definida; só confirmed não utilizado recebe checkedIn=true; dois check-ins concorrentes liberam uma entrada.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Matriz R10 completa e duas tentativas de check-in concorrentes; autorização e mensagem exata.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F07-02 | Etapa 2

- [ ] Implementar cancelamento atômico e proteção de estado terminal; verificar gateway tardio, corridas e edição negada.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A26`: Criar slow 0003 + fast 0001, cancelar antes de 30s; medir <=10s, aguardar >=45s, repetir cancelamento e testar ações; corrida cancelamento/reserva/finalização. Esperado: Cancelar publicado é irreversível; na mesma transação confirmed→refunded e pending→cancelled, sem alteração de declined; gateway posterior não modifica; edit/publish/compra rejeitados.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Corridas cancelamento/reserva e finalize, timer lento real, cancelamento repetido e edição negada.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F07-03 | Etapa 3

- [ ] Implementar agregação do painel e seção de ações/métricas; testar preço histórico e ingresso utilizado estornado.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A27`: Fixture 10000+10000+15000 confirmados, 1 check-in, recusado e estornado; conferir receita 35000 e todas as contagens; após cancelar comparar zeros e estornos. Esperado: Painel mostra seis métricas com snapshots de preço e ambos os canais; check-ins somente confirmed; cancelado tem receita/vagas/confirmados/pendentes/check-ins zero.
  - `TEST-A28`: Browser A/B/P/visitante, POST forjado de B, verificar nenhum dado nem alteração; abrir gestão de A e executar ações. Esperado: Check-in, cancelar e painel ficam na URL de gestão de cada evento; todas as ações exigem dono inclusive requisição direta.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Painel 35000 centavos, check-in e estorno, sem vazamento, URL única.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F07-04 | Etapa 4

- [ ] Executar avaliação independente A25–A28 e X11–X13; após W5 executar X14–X16.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A25`: Fixtures código inválido/outro evento, cancelado, pending/declined/refunded, confirmado já usado e novo; corrida com duas sessões do dono. Esperado: Check-in aplica exatamente as cinco mensagens na ordem definida; só confirmed não utilizado recebe checkedIn=true; dois check-ins concorrentes liberam uma entrada.
  - `TEST-A26`: Criar slow 0003 + fast 0001, cancelar antes de 30s; medir <=10s, aguardar >=45s, repetir cancelamento e testar ações; corrida cancelamento/reserva/finalização. Esperado: Cancelar publicado é irreversível; na mesma transação confirmed→refunded e pending→cancelled, sem alteração de declined; gateway posterior não modifica; edit/publish/compra rejeitados.
  - `TEST-A27`: Fixture 10000+10000+15000 confirmados, 1 check-in, recusado e estornado; conferir receita 35000 e todas as contagens; após cancelar comparar zeros e estornos. Esperado: Painel mostra seis métricas com snapshots de preço e ambos os canais; check-ins somente confirmed; cancelado tem receita/vagas/confirmados/pendentes/check-ins zero.
  - `TEST-A28`: Browser A/B/P/visitante, POST forjado de B, verificar nenhum dado nem alteração; abrir gestão de A e executar ações. Esperado: Check-in, cancelar e painel ficam na URL de gestão de cada evento; todas as ações exigem dono inclusive requisição direta.
  - `TEST-X11`: B tenta check-in e cancelamento de A, sem efeito e sem informação. Esperado: Todas as ações operacionais respeitam guarda de dono.
  - `TEST-X12`: Cancelar publicado e tentar editar e republicar via POST; consultar catálogo. Esperado: Cancelamento bloqueia publicação/edição e integra gestão em URL existente.
  - `TEST-X13`: Combinar slow, fast, check-in, cancelar e esperar resultado tardio. Esperado: Check-in/painel/cancelamento compartilham status, lock e preço; gateway tardio não revive.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## Handoff

- [ ] Testes unitários, integração e contratos locais verdes no SHA indicado.
- [ ] Nada fora da ownership; atualizar docs e registrar dependências.
- [ ] Entregar SHA e comandos à sessão nova de avaliação; não entregar veredito pronto.
- [ ] Após aprovação independente e PR mergeado, coordenador atualiza estado.
