# F02 | Plano de implementação

Prerequisitos: baseline aprovada, dependências F01 mergeadas; branch `feat/f02-identidade`; ler spec, contrato, guidelines, skills e estado.

## T-F02-01 | Etapa 1

- [ ] Implementar formulário de cadastro, backend de autenticação quando necessário, rotas e templates de cadastro/login/logout.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A06`: Browser: cadastro/login/logout; POST com role=organizer; consulta DB somente para verificar hash e papel. Esperado: Cadastro público cria somente participante, e-mail normalizado único; senha armazenada como hash; login válido e logout invalidam sessão; erro genérico em credenciais inválidas.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Formulário rejeita e-mail inválido e role forjado; senha não é armazenada em claro; normalização de e-mail.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F02-02 | Etapa 2

- [ ] Definir guards de papel e dono, redirects, tratamento de erros e CSRF.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A07`: Sessões independentes A/B/P/anônima; fixture de evento A; assert HTTP 404 para B, ausência de nome/dados e nenhuma mutação; 403 ou redirect para demais. Esperado: Visitante e participante não acessam rotas de gestão; B não lê nem modifica eventos de A, incluindo URL direta e POST forjado.
  - `TEST-A08`: Testar guarda de participante com duas contas e recurso fixture; tentar usar X-Api-Key em rota web; negar. Esperado: Participante só tem acesso aos próprios recursos; parceiro não cria sessão web nem vincula conta pelo e-mail.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Gate mínimo desta etapa: Teste de guarda com A/B/participante/anônimo, CSRF real e sessão de login/logout.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F02-03 | Etapa 3

- [ ] Testar papéis, invalidação da sessão, unicidade/hash e acesso indevido a fixtures; revisar logs.
- Validação: executar testes pertinentes ao componente; se falhar, corrigir antes de seguir. Na última etapa rodar contrato inteiro e gates; não marcar aprovado pelo próprio implementador.
- Gate mínimo desta etapa: Browser com duas sessões e tentativa de acesso por ID; conferir X01 com seed.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## T-F02-04 | Etapa 4

- [ ] Verificar login da seed F01 e publicar contrato de autorização.
- Validação rastreável (executar quando a dependência do cenário estiver disponível; no gate final nenhum item aplicável pode faltar):
  - `TEST-A06`: Browser: cadastro/login/logout; POST com role=organizer; consulta DB somente para verificar hash e papel. Esperado: Cadastro público cria somente participante, e-mail normalizado único; senha armazenada como hash; login válido e logout invalidam sessão; erro genérico em credenciais inválidas.
  - `TEST-A07`: Sessões independentes A/B/P/anônima; fixture de evento A; assert HTTP 404 para B, ausência de nome/dados e nenhuma mutação; 403 ou redirect para demais. Esperado: Visitante e participante não acessam rotas de gestão; B não lê nem modifica eventos de A, incluindo URL direta e POST forjado.
  - `TEST-A08`: Testar guarda de participante com duas contas e recurso fixture; tentar usar X-Api-Key em rota web; negar. Esperado: Participante só tem acesso aos próprios recursos; parceiro não cria sessão web nem vincula conta pelo e-mail.
  - `TEST-X01`: Subir ambiente limpo, login das três contas, comparar IDs após reseed. Esperado: Após up com seed, A/B/P autenticam; duas execuções da seed não duplicam contas.
  - Rodar lint e testes já existentes da feature. Falha impede avançar.
- Evidência: código de saída, teste nomeado, SHA e arquivos modificados; registrar no handoff.

## Handoff

- [ ] Testes unitários, integração e contratos locais verdes no SHA indicado.
- [ ] Nada fora da ownership; atualizar docs e registrar dependências.
- [ ] Entregar SHA e comandos à sessão nova de avaliação; não entregar veredito pronto.
- [ ] Após aprovação independente e PR mergeado, coordenador atualiza estado.
