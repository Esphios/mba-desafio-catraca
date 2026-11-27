# F04 | Plano de implementação

Entrada: baseline W0 aprovada, dependências F01, F03 integradas e aprovadas, branch exclusiva. Skills: transaction-safety, payment-simulation, feature-implementation.

## T-F04-01

**Entrega:** Criar Buyer/Ticket DTO, validador de cartão, classificação de gateway e código.

**Validação:** lint, checks do framework e testes já implementados; fase 1 não exige endpoints futuros.
- `TEST-A17` (A17): Enviar cartão com 15/17 dígitos, letras, Unicode, espaços, tipo numérico; e-mail inválido; procurar número de teste em DB/logs. Resultado: Sem ticket/job para entradas inválidas; PAN não salvo nem refletido.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F04-02

**Entrega:** Implementar reserve atômico, savepoint de colisão e rollback ticket/job; stress.

**Validação:** lint, checks do framework e testes já implementados; fase 2 não exige endpoints futuros.
- `TEST-A13` (A13): Reservar web e parceiro; capturar DTO imediato, recontar tickets e jobs; comparar preço/código. Resultado: Um ticket pending e um job por chamada; código distinto; 0 vagas após duas; não aguarda pagamento.
- `TEST-A14` (A14): Barreira de início, usar cartões de aprovação; conferir resultados e contagem DB; rodar também cap 1 com 2 concorrentes. Resultado: Exatamente 5/25 em todas as rodadas, 1/1 no limite; nenhuma exceção inesperada nem job órfão.
- `TEST-A32` (A32): Forçar colisão uma vez e permanente; injetar falha ao criar job; verificar tickets/jobs antes/depois. Resultado: Colisão transitória resolve com novo código; permanente/falha reverte tudo, não retorna sold_out.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F04-03

**Entrega:** Implementar worker durável, due_at, restart e proteção de terminal; timing real.

**Validação:** lint, checks do framework e testes já implementados; fase 3 não exige endpoints futuros.
- `TEST-A15` (A15): Comprar cada final 0001/0002/0003/0004/9999; consultar pending e resultado até deadline; medir intervalo created→resolved, recarregar vagas. Resultado: Aprovação/recusa corretas; 2–5 s e 30–40 s; recusa libera exatamente uma vaga; nenhum terminal antecipado.
- `TEST-A16` (A16): Comprar antes/depois da edição; reiniciar worker antes de due; executar resolução novamente; tentar aplicar a fixture terminal. Resultado: Preço histórico intacto; job recuperado; só uma transição; terminal nunca muda.
- `TEST-A33` (A33): Ambos descobrem o mesmo ID; um rollback; outro conclui; repetir job terminal; testar evento diferente. Resultado: Um efeito, sem deadlock; retry só de transação abortada; eventos independentes não bloqueiam entre si.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F04-04

**Entrega:** Executar concorrência, corrida preço/capacidade e avaliação de interfaces.

**Validação:** lint, checks do framework e testes já implementados; fase 4 não exige endpoints futuros.
- `TEST-A13` (A13): Reservar web e parceiro; capturar DTO imediato, recontar tickets e jobs; comparar preço/código. Resultado: Um ticket pending e um job por chamada; código distinto; 0 vagas após duas; não aguarda pagamento.
- `TEST-A14` (A14): Barreira de início, usar cartões de aprovação; conferir resultados e contagem DB; rodar também cap 1 com 2 concorrentes. Resultado: Exatamente 5/25 em todas as rodadas, 1/1 no limite; nenhuma exceção inesperada nem job órfão.
- `TEST-A15` (A15): Comprar cada final 0001/0002/0003/0004/9999; consultar pending e resultado até deadline; medir intervalo created→resolved, recarregar vagas. Resultado: Aprovação/recusa corretas; 2–5 s e 30–40 s; recusa libera exatamente uma vaga; nenhum terminal antecipado.
- `TEST-A16` (A16): Comprar antes/depois da edição; reiniciar worker antes de due; executar resolução novamente; tentar aplicar a fixture terminal. Resultado: Preço histórico intacto; job recuperado; só uma transição; terminal nunca muda.
- `TEST-A17` (A17): Enviar cartão com 15/17 dígitos, letras, Unicode, espaços, tipo numérico; e-mail inválido; procurar número de teste em DB/logs. Resultado: Sem ticket/job para entradas inválidas; PAN não salvo nem refletido.
- `TEST-A32` (A32): Forçar colisão uma vez e permanente; injetar falha ao criar job; verificar tickets/jobs antes/depois. Resultado: Colisão transitória resolve com novo código; permanente/falha reverte tudo, não retorna sold_out.
- `TEST-A33` (A33): Ambos descobrem o mesmo ID; um rollback; outro conclui; repetir job terminal; testar evento diferente. Resultado: Um efeito, sem deadlock; retry só de transação abortada; eventos independentes não bloqueiam entre si.
- `TEST-X04` (X04): Comprar slow, reiniciar worker antes de due; obter status final uma vez. Resultado: Worker do Compose consome job persistido após reinício sem chave real.
- `TEST-X05` (X05): Corrida compra × redução e compra × preço; conferir invariantes e snapshots. Resultado: Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## Integração posterior
Não há item exclusivo de integração atribuído a esta feature; regressão global é obrigatória.

## Handoff
Entregar SHA limpo, base SHA, interfaces, comandos, logs redigidos e desvios. Avaliador novo, sem histórico de conversa, julga apenas contrato e evidência. Coordenador integra após local PASS; relatório final da feature exige também itens integrados, se houver.
