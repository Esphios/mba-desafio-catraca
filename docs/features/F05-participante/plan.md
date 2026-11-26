# F05 | Plano de implementação

Prerequisitos: baseline aprovada, dependências F02, F03, F04 mergeadas; branch `feat/f05-participante`; ler spec, contrato, guidelines, skills e estado.

## T-F05-01 | Etapa 1

- [ ] Implementar listagem pública, detalhes e estados de disponibilidade/vitrine vazia.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A18`: Browser: draft/publicado/cancelled, capacidade 1 pendente e tentativa direta sem vaga. Esperado: Vitrine exibe só publicados não cancelados, inclusive esgotados com texto exato Ingressos esgotados; tentativa concorrente recebe mesma mensagem.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Catálogo por estado e disponibilidade; texto exato para evento lotado. Teste da tentativa POST após etapa 2.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F05-02 | Etapa 2

- [ ] Implementar formulário autenticado, mapeamento de erros, navegação e Meus ingressos.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A19`: Playwright: cadastro, login, compra, tela pending e polling/reload até confirmed; conferir código em DB ou via F06 após integração. Esperado: Participante cria conta, compra pela vitrine, vê evento/status/código em Meus ingressos; pending imediato e confirmado em até 5s para 0001.
  - `TEST-A20`: Fixtures dos cinco estados; duas contas; ingresso partner com mesmo e-mail não aparece; POST anônimo sem efeito. Esperado: Meus ingressos filtra por participant_id autenticado, não por e-mail, e mostra todos os cinco rótulos; visitante não compra.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Compra real, CSRF, erros de sessão e status/rótulos na lista pessoal.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F05-03 | Etapa 3

- [ ] Executar testes browser de pendente, confirmação, recusa, esgotamento, titularidade e CSRF.
- Validação: executar testes pertinentes ao componente; se falhar, corrigir antes de seguir. Na última etapa rodar contrato inteiro e gates; não marcar aprovado pelo próprio implementador.
- Gate mínimo desta etapa: Browser E1 pendente e confirmado, slow recusa, conta separada, POST stale e ausência de dados de outro participante.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F05-04 | Etapa 4

- [ ] Abrir PR; avaliar X06–X08 localmente; reservar X14/X16 para gate integrado.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A18`: Browser: draft/publicado/cancelled, capacidade 1 pendente e tentativa direta sem vaga. Esperado: Vitrine exibe só publicados não cancelados, inclusive esgotados com texto exato Ingressos esgotados; tentativa concorrente recebe mesma mensagem.
  - `TEST-A19`: Playwright: cadastro, login, compra, tela pending e polling/reload até confirmed; conferir código em DB ou via F06 após integração. Esperado: Participante cria conta, compra pela vitrine, vê evento/status/código em Meus ingressos; pending imediato e confirmado em até 5s para 0001.
  - `TEST-A20`: Fixtures dos cinco estados; duas contas; ingresso partner com mesmo e-mail não aparece; POST anônimo sem efeito. Esperado: Meus ingressos filtra por participant_id autenticado, não por e-mail, e mostra todos os cinco rótulos; visitante não compra.
  - `TEST-X06`: Dois browsers com sessões distintas; compra e acesso cruzado. Esperado: Sessão define dono do ingresso; anônimo e outra conta não veem compra pessoal.
  - `TEST-X07`: Criar draft, publicar, reservar até lotar, cancelar fixture; recarregar catálogo. Esperado: Publicar/lotar/cancelar reflete na vitrine sem cache obsoleto.
  - `TEST-X08`: Comprar 0004, observar lotação, após 45s ver declined e vaga. Esperado: Compra web usa reserve e worker; pendente ocupa e recusa libera na vitrine.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## Handoff

- [ ] Testes unitários, integração e contratos locais verdes no SHA indicado.
- [ ] Nada fora da ownership; atualizar docs e registrar dependências.
- [ ] Entregar SHA e comandos à sessão nova de avaliação; não entregar veredito pronto.
- [ ] Após aprovação independente e PR mergeado, coordenador atualiza estado.
