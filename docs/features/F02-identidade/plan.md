# F02 | Plano de implementação

Entrada: baseline W0 aprovada, dependências F01 integradas e aprovadas, branch exclusiva. Skills: secure-boundaries, feature-implementation.

## T-F02-01

**Entrega:** Implementar cadastro, login e logout com Django; validação de e-mail e senha.

**Validação:** lint, checks do framework e testes já implementados; fase 1 não exige endpoints futuros.
- `TEST-A06` (A06): Cadastrar, repetir e-mail com caixa distinta, login incorreto/correto, logout; consultar hash sem registrá-lo. Resultado: Participante único; senha não em claro; sessão só após sucesso; logout invalida cookie anterior.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F02-02

**Entrega:** Expor Actor/guards e predicado de dono; comportamento de erros e redirects.

**Validação:** lint, checks do framework e testes já implementados; fase 2 não exige endpoints futuros.
- `TEST-A07` (A07): Exercitar guardas com IDs de A e B; forjar proprietário no payload; comparar resultados e dados. Resultado: Anônimo redirecionado no GET, participante 403, B recebe 404 genérico ao acessar A; nenhuma mutação.
- `TEST-A08` (A08): Forjar ID de participante no request/contexto, tentar autenticar por chave; validar identidade retornada. Resultado: ID da sessão é autoridade exclusiva; chave não cria sessão; login por e-mail continua conta distinta.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F02-03

**Entrega:** Testar CSRF, role escalation, session replay, ownership por fixture, sanitização.

**Validação:** lint, checks do framework e testes já implementados; fase 3 não exige endpoints futuros.
- `TEST-A30` (A30): Enviar role=organizer, token CSRF ausente, next=//host e variações, reutilizar cookie após logout. Resultado: Conta participante, mutação proibida sem CSRF, apenas redirect interno, sessão anterior inválida.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## T-F02-04

**Entrega:** Validar seed em ambiente real e congelar contrato de acesso.

**Validação:** lint, checks do framework e testes já implementados; fase 4 não exige endpoints futuros.
- `TEST-A06` (A06): Cadastrar, repetir e-mail com caixa distinta, login incorreto/correto, logout; consultar hash sem registrá-lo. Resultado: Participante único; senha não em claro; sessão só após sucesso; logout invalida cookie anterior.
- `TEST-A07` (A07): Exercitar guardas com IDs de A e B; forjar proprietário no payload; comparar resultados e dados. Resultado: Anônimo redirecionado no GET, participante 403, B recebe 404 genérico ao acessar A; nenhuma mutação.
- `TEST-A08` (A08): Forjar ID de participante no request/contexto, tentar autenticar por chave; validar identidade retornada. Resultado: ID da sessão é autoridade exclusiva; chave não cria sessão; login por e-mail continua conta distinta.
- `TEST-A30` (A30): Enviar role=organizer, token CSRF ausente, next=//host e variações, reutilizar cookie após logout. Resultado: Conta participante, mutação proibida sem CSRF, apenas redirect interno, sessão anterior inválida.
- `TEST-X01` (X01): Subir ambiente limpo, login das três contas, comparar IDs após reseed. Resultado: Após up com seed, A/B/P autenticam; duas execuções da seed não duplicam contas.

**Saída:** commit útil, resultado do gate, limitações e arquivos modificados. Sem evidência de teste não avançar.

## Integração posterior
Não há item exclusivo de integração atribuído a esta feature; regressão global é obrigatória.

## Handoff
Entregar SHA limpo, base SHA, interfaces, comandos, logs redigidos e desvios. Avaliador novo, sem histórico de conversa, julga apenas contrato e evidência. Coordenador integra após local PASS; relatório final da feature exige também itens integrados, se houver.
