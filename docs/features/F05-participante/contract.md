# F05 | Contrato de avaliação

Versão 2 proposta. Ambiente: checkout limpo do SHA, Docker/Compose e Git; `bash bin/up` e `bash bin/gates --feature F05` após implementados. Banco PostgreSQL real, dados sintéticos, projeto/porta exclusivos, gateway padrão para itens de tempo. O avaliador cria relatório novo sem alterar código.

## Fase LOCAL (antes do merge)

### C-F05-A18 (A18)

Preparação: E1 draft, E2 publicado com vaga, E3 publicado lotado, E4 cancelado fixture.

Procedimento: Visitar vitrine anonimamente e detalhe E3; forjar POST quando vaga termina.

PASS somente se: Só E2/E3 listados; mensagem Ingressos esgotados no detalhe ou tentativa; sem venda adicional.

Teste: `TEST-A18`. Evidência: Browser: draft/publicado/cancelled, capacidade 1 pendente e tentativa direta sem vaga.

### C-F05-A19 (A19)

Preparação: Browser participante novo e evento publicado disponível.

Procedimento: Cadastrar, comprar 0001, abrir Meus ingressos imediatamente e recarregar até 5s.

PASS somente se: Evento e código visíveis, pendente inicialmente, confirmado até deadline; sem esperar gateway no POST.

Teste: `TEST-A19`. Evidência: Playwright: cadastro, login, compra, tela pending e polling/reload até confirmed; conferir código em DB ou via F06 após integração.

### C-F05-A20 (A20)

Preparação: Fixtures de cinco status para P, ticket de outro participante e parceiro com mesmo e-mail.

Procedimento: Abrir Meus ingressos, trocar sessão, tentar URL/ID forjado e compra anônima.

PASS somente se: Só tickets do ID da sessão; cinco rótulos exatos; parceiro não aparece; visitante não compra.

Teste: `TEST-A20`. Evidência: Fixtures dos cinco estados; duas contas; ingresso partner com mesmo e-mail não aparece; POST anônimo sem efeito.

### C-F05-X06 (X06)

Preparação: Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.

Procedimento: Dois browsers com sessões distintas; compra e acesso cruzado.

PASS somente se: Sessão define dono do ingresso; anônimo e outra conta não veem compra pessoal.

Teste: `TEST-X06`. Evidência: Dois browsers com sessões distintas; compra e acesso cruzado.

### C-F05-X07 (X07)

Preparação: Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.

Procedimento: Criar draft, publicar, reservar até lotar, cancelar fixture; recarregar catálogo.

PASS somente se: A publicação e as vagas calculadas por F03 chegam à vitrine; draft/cancelled não são exibidos, inclusive fixture cancelada. A ação real de cancelar é validada em X14.

Teste: `TEST-X07`. Evidência: Criar draft, publicar, reservar até lotar, cancelar fixture; recarregar catálogo.

### C-F05-X08 (X08)

Preparação: Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.

Procedimento: Comprar 0004, observar lotação, após 45s ver declined e vaga.

PASS somente se: Compra web usa reserve e worker; pendente ocupa e recusa libera na vitrine.

Teste: `TEST-X08`. Evidência: Comprar 0004, observar lotação, após 45s ver declined e vaga.

## Fase INTEGRATED (após merge da wave)

Itens desta fase são explicitamente PENDING_INTEGRATION no relatório local; não contar como PASS e não exigir feature irmã no checkout isolado. Relatório integrado deve incluir todos os itens anteriores e os seguintes, sem pendências.

Nenhum item exclusivo desta fase; o último relatório local permanece válido se nenhum comportamento foi alterado, sem dispensar regressão de release.

## Mapeamento explícito

| Critério | Item      | Teste    | Fase  |
| -------- | --------- | -------- | ----- |
| A18      | C-F05-A18 | TEST-A18 | local |
| A19      | C-F05-A19 | TEST-A19 | local |
| A20      | C-F05-A20 | TEST-A20 | local |
| X06      | C-F05-X06 | TEST-X06 | local |
| X07      | C-F05-X07 | TEST-X07 | local |
| X08      | C-F05-X08 | TEST-X08 | local |

Qualquer item aplicável sem evidência = FAIL. Fixture deve ser declarada; não usar fixture para substituir efeito real no integrado.
