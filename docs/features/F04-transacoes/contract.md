# F04 | Contrato de avaliação

Versão 2 proposta. Ambiente: checkout limpo do SHA, Docker/Compose e Git; `bash bin/up` e `bash bin/gates --feature F04` após implementados. Banco PostgreSQL real, dados sintéticos, projeto/porta exclusivos, gateway padrão para itens de tempo. O avaliador cria relatório novo sem alterar código.

## Fase LOCAL (antes do merge)

### C-F04-A13 (A13)

Preparação: E publicado cap 2 sem tickets; relógio de teste e worker pausado para conferir commit.

Procedimento: Reservar web e parceiro; capturar DTO imediato, recontar tickets e jobs; comparar preço/código.

PASS somente se: Um ticket pending e um job por chamada; código distinto; 0 vagas após duas; não aguarda pagamento.

Teste: `TEST-A13`. Evidência: Invocar reserve e consultar DB; medir tempo <2s em ambiente local estável; rollback injetado não deixa ticket/job; colisão de código tratada.

### C-F04-A14 (A14)

Preparação: PostgreSQL real, 10 eventos novos cap 5 e 30 clientes em conexões distintas.

Procedimento: Barreira de início, usar cartões de aprovação; conferir resultados e contagem DB; rodar também cap 1 com 2 concorrentes.

PASS somente se: Exatamente 5/25 em todas as rodadas, 1/1 no limite; nenhuma exceção inesperada nem job órfão.

Teste: `TEST-A14`. Evidência: TransactionTestCase com barreira de threads/conexões distintas e PostgreSQL real; consultar ocupação, jobs e erros; repetir 10 vezes como robustez.

### C-F04-A15 (A15)

Preparação: 5 eventos ou vagas independentes; worker padrão ativo; relógio monotônico + timestamps DB.

Procedimento: Comprar cada final 0001/0002/0003/0004/9999; consultar pending e resultado até deadline; medir intervalo created→resolved, recarregar vagas.

PASS somente se: Aprovação/recusa corretas; 2–5 s e 30–40 s; recusa libera exatamente uma vaga; nenhum terminal antecipado.

Teste: `TEST-A15`. Evidência: Testes unitários de mapeamento e integração com relógio real: polling, timestamps, ocupação; não acelerar teste de prazo.

### C-F04-A16 (A16)

Preparação: Ticket slow e fixtures terminais; dois preços sucessivos.

Procedimento: Comprar antes/depois da edição; reiniciar worker antes de due; executar resolução novamente; tentar aplicar a fixture terminal.

PASS somente se: Preço histórico intacto; job recuperado; só uma transição; terminal nunca muda.

Teste: `TEST-A16`. Evidência: Testar preço antes/depois, aplicar resultado duas vezes e fixtures cancelled/refunded; parar/reiniciar worker com job pendente e verificar efeito único.

### C-F04-A17 (A17)

Preparação: E publicado com vaga; DB e captura sanitizada de log.

Procedimento: Enviar cartão com 15/17 dígitos, letras, Unicode, espaços, tipo numérico; e-mail inválido; procurar número de teste em DB/logs.

PASS somente se: Sem ticket/job para entradas inválidas; PAN não salvo nem refletido.

Teste: `TEST-A17`. Evidência: Casos 15/17 dígitos, letras, Unicode, espaços, e-mail inválido; assert contagem zero e inspeção DB/logs.

### C-F04-A32 (A32)

Preparação: Code generator injetável e DB transacional; evento com vagas.

Procedimento: Forçar colisão uma vez e permanente; injetar falha ao criar job; verificar tickets/jobs antes/depois.

PASS somente se: Colisão transitória resolve com novo código; permanente/falha reverte tudo, não retorna sold_out.

Teste: `TEST-A32`. Evidência: Forçar colisões e exceção entre INSERTs; contar tickets/jobs, inspecionar status HTTP em teste integrado.

### C-F04-A33 (A33)

Preparação: Job vencido, dois workers independentes; lock de evento controlado.

Procedimento: Ambos descobrem o mesmo ID; um rollback; outro conclui; repetir job terminal; testar evento diferente.

PASS somente se: Um efeito, sem deadlock; retry só de transação abortada; eventos independentes não bloqueiam entre si.

Teste: `TEST-A33`. Evidência: Duas conexões/processos, job selecionado duas vezes, lock hold/release, abortar uma execução, confirmar efeito único.

### C-F04-X04 (X04)

Preparação: Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.

Procedimento: Comprar slow, reiniciar worker antes de due; obter status final uma vez.

PASS somente se: Worker do Compose consome job persistido após reinício sem chave real.

Teste: `TEST-X04`. Evidência: Comprar slow, reiniciar worker antes de due; obter status final uma vez.

### C-F04-X05 (X05)

Preparação: Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.

Procedimento: Corrida compra × redução e compra × preço; conferir invariantes e snapshots.

PASS somente se: Reserve usa mesmo lock de editar; draft/cancelled recusam, alteração de capacidade não gera sobrelotação.

Teste: `TEST-X05`. Evidência: Corrida compra × redução e compra × preço; conferir invariantes e snapshots.

## Fase INTEGRATED (após merge da wave)

Itens desta fase são explicitamente PENDING_INTEGRATION no relatório local; não contar como PASS e não exigir feature irmã no checkout isolado. Relatório integrado deve incluir todos os itens anteriores e os seguintes, sem pendências.

Nenhum item exclusivo desta fase; o último relatório local permanece válido se nenhum comportamento foi alterado, sem dispensar regressão de release.

## Mapeamento explícito

| Critério | Item      | Teste    | Fase  |
| -------- | --------- | -------- | ----- |
| A13      | C-F04-A13 | TEST-A13 | local |
| A14      | C-F04-A14 | TEST-A14 | local |
| A15      | C-F04-A15 | TEST-A15 | local |
| A16      | C-F04-A16 | TEST-A16 | local |
| A17      | C-F04-A17 | TEST-A17 | local |
| A32      | C-F04-A32 | TEST-A32 | local |
| A33      | C-F04-A33 | TEST-A33 | local |
| X04      | C-F04-X04 | TEST-X04 | local |
| X05      | C-F04-X05 | TEST-X05 | local |

Qualquer item aplicável sem evidência = FAIL. Fixture deve ser declarada; não usar fixture para substituir efeito real no integrado.
