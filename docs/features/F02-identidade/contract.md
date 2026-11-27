# F02 | Contrato de avaliação

Versão 2 proposta. Ambiente: checkout limpo do SHA, Docker/Compose e Git; `bash bin/up` e `bash bin/gates --feature F02` após implementados. Banco PostgreSQL real, dados sintéticos, projeto/porta exclusivos, gateway padrão para itens de tempo. O avaliador cria relatório novo sem alterar código.

## Fase LOCAL (antes do merge)

### C-F02-A06 (A06)

Preparação: Browser sem sessão e contas seed.

Procedimento: Cadastrar, repetir e-mail com caixa distinta, login incorreto/correto, logout; consultar hash sem registrá-lo.

PASS somente se: Participante único; senha não em claro; sessão só após sucesso; logout invalida cookie anterior.

Teste: `TEST-A06`. Evidência: Browser: cadastro/login/logout; POST com role=organizer; consulta DB somente para verificar hash e papel.

### C-F02-A07 (A07)

Preparação: Fixtures de eventos A/B e atores anônimo/P/A/B.

Procedimento: Exercitar guardas com IDs de A e B; forjar proprietário no payload; comparar resultados e dados.

PASS somente se: Anônimo redirecionado no GET, participante 403, B recebe 404 genérico ao acessar A; nenhuma mutação.

Teste: `TEST-A07`. Evidência: Sessões independentes A/B/P/anônima; fixture de evento A; assert HTTP 404 para B, ausência de nome/dados e nenhuma mutação; 403 ou redirect para demais.

### C-F02-A08 (A08)

Preparação: Dois participantes com e-mails distintos e credencial de parceiro.

Procedimento: Forjar ID de participante no request/contexto, tentar autenticar por chave; validar identidade retornada.

PASS somente se: ID da sessão é autoridade exclusiva; chave não cria sessão; login por e-mail continua conta distinta.

Teste: `TEST-A08`. Evidência: Testar guarda de participante com duas contas e recurso fixture; tentar usar X-Api-Key em rota web; negar.

### C-F02-A30 (A30)

Preparação: Sessão anônima, formulários públicos e protegidos.

Procedimento: Enviar role=organizer, token CSRF ausente, next=//host e variações, reutilizar cookie após logout.

PASS somente se: Conta participante, mutação proibida sem CSRF, apenas redirect interno, sessão anterior inválida.

Teste: `TEST-A30`. Evidência: POST forjado, role=organizer, cookies antes/depois, token ausente e next externo; comparar banco.

### C-F02-X01 (X01)

Preparação: Checkout com providers e consumer disponíveis; fixtures isoladas e dados sintéticos.

Procedimento: Subir ambiente limpo, login das três contas, comparar IDs após reseed.

PASS somente se: Após up com seed, A/B/P autenticam; duas execuções da seed não duplicam contas.

Teste: `TEST-X01`. Evidência: Subir ambiente limpo, login das três contas, comparar IDs após reseed.

## Fase INTEGRATED (após merge da wave)

Itens desta fase são explicitamente PENDING_INTEGRATION no relatório local; não contar como PASS e não exigir feature irmã no checkout isolado. Relatório integrado deve incluir todos os itens anteriores e os seguintes, sem pendências.

Nenhum item exclusivo desta fase; o último relatório local permanece válido se nenhum comportamento foi alterado, sem dispensar regressão de release.

## Mapeamento explícito

| Critério | Item      | Teste    | Fase  |
| -------- | --------- | -------- | ----- |
| A06      | C-F02-A06 | TEST-A06 | local |
| A07      | C-F02-A07 | TEST-A07 | local |
| A08      | C-F02-A08 | TEST-A08 | local |
| A30      | C-F02-A30 | TEST-A30 | local |
| X01      | C-F02-X01 | TEST-X01 | local |

Qualquer item aplicável sem evidência = FAIL. Fixture deve ser declarada; não usar fixture para substituir efeito real no integrado.
