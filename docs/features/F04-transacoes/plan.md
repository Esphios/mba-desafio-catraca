# F04 | Plano de implementação

Prerequisitos: baseline aprovada, dependências F01, F03 mergeadas; branch `feat/f04-transacoes`; ler spec, contrato, guidelines, skills e estado.

## T-F04-01 | Etapa 1

- [ ] Implementar Buyer/TicketDTO tipados, validação, classificação do gateway e geração de código.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A17`: Casos 15/17 dígitos, letras, Unicode, espaços, e-mail inválido; assert contagem zero e inspeção DB/logs. Esperado: Cartão diferente de 16 dígitos ASCII falha antes de criar ingresso; e-mail malformado na compra de parceiro falha; PAN não persiste nem aparece em logs.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Validadores puros, todos finais de cartão, geração de código e entradas inválidas; teste de ausência de efeitos após implementação da reserva na etapa 2.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F04-02 | Etapa 2

- [ ] Implementar reserva atômica, lock seguido de contagem, snapshot e job durável; testar falha e colisão.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A13`: Invocar reserve e consultar DB; medir tempo <2s em ambiente local estável; rollback injetado não deixa ticket/job; colisão de código tratada. Esperado: Uma compra válida retorna ingresso pending com ID/código únicos e job gravado na mesma transação, sem aguardar gateway; reserva já ocupa vaga.
  - `TEST-A14`: TransactionTestCase com barreira de threads/conexões distintas e PostgreSQL real; consultar ocupação, jobs e erros; repetir 10 vezes como robustez. Esperado: Quando lotação esgota, não cria ingresso/job; 30 reservas concorrentes sobre capacidade 5 dão exatamente 5 sucessos/25 sold_out, em duas rodadas novas.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Rollback injetado ao gravar job, preço e código; stress com PostgreSQL e conexões distintas.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F04-03 | Etapa 3

- [ ] Implementar loop de finalização, proteção terminal, recuperação após reinício e consultas de ingressos.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A15`: Testes unitários de mapeamento e integração com relógio real: polling, timestamps, ocupação; não acelerar teste de prazo. Esperado: Gateway padrão confirma 0001 e recusa 0002/outros em 2–5s; confirma 0003 e recusa 0004 em 30–40s; recusa libera uma vaga.
  - `TEST-A16`: Testar preço antes/depois, aplicar resultado duas vezes e fixtures cancelled/refunded; parar/reiniciar worker com job pendente e verificar efeito único. Esperado: Snapshot de preço é capturado sob lock; finalize só altera pending de evento publicado; resultado duplicado/tardio não revive terminal; job sobrevive reinício.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Finalização idempotente e timing padrão, job persistente após restart e estado terminal.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F04-04 | Etapa 4

- [ ] Executar stress concorrente, timing real e corridas edição/reserva; congelar interfaces e registrar base SHA para W5.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A13`: Invocar reserve e consultar DB; medir tempo <2s em ambiente local estável; rollback injetado não deixa ticket/job; colisão de código tratada. Esperado: Uma compra válida retorna ingresso pending com ID/código únicos e job gravado na mesma transação, sem aguardar gateway; reserva já ocupa vaga.
  - `TEST-A14`: TransactionTestCase com barreira de threads/conexões distintas e PostgreSQL real; consultar ocupação, jobs e erros; repetir 10 vezes como robustez. Esperado: Quando lotação esgota, não cria ingresso/job; 30 reservas concorrentes sobre capacidade 5 dão exatamente 5 sucessos/25 sold_out, em duas rodadas novas.
  - `TEST-A15`: Testes unitários de mapeamento e integração com relógio real: polling, timestamps, ocupação; não acelerar teste de prazo. Esperado: Gateway padrão confirma 0001 e recusa 0002/outros em 2–5s; confirma 0003 e recusa 0004 em 30–40s; recusa libera uma vaga.
  - `TEST-A16`: Testar preço antes/depois, aplicar resultado duas vezes e fixtures cancelled/refunded; parar/reiniciar worker com job pendente e verificar efeito único. Esperado: Snapshot de preço é capturado sob lock; finalize só altera pending de evento publicado; resultado duplicado/tardio não revive terminal; job sobrevive reinício.
  - `TEST-A17`: Casos 15/17 dígitos, letras, Unicode, espaços, e-mail inválido; assert contagem zero e inspeção DB/logs. Esperado: Cartão diferente de 16 dígitos ASCII falha antes de criar ingresso; e-mail malformado na compra de parceiro falha; PAN não persiste nem aparece em logs.
  - `TEST-X04`: Comprar slow, reiniciar worker antes de due; obter status final uma vez. Esperado: Worker do Compose consome job persistido após reinício sem chave real.
  - `TEST-X05`: Corrida compra × redução e compra × preço; conferir invariantes e snapshots. Esperado: Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## Handoff

- [ ] Testes unitários, integração e contratos locais verdes no SHA indicado.
- [ ] Nada fora da ownership; atualizar docs e registrar dependências.
- [ ] Entregar SHA e comandos à sessão nova de avaliação; não entregar veredito pronto.
- [ ] Após aprovação independente e PR mergeado, coordenador atualiza estado.
