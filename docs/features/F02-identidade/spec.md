# F02 | FDD: Identidade e fronteiras de acesso

Status: proposto · Wave W2 · Fonte normativa: PRD e design.

## Resultado e interfaces

Provides: Cadastro/login/logout, sessão, funções require_participant e require_organizer + predicado de dono, identidade dos usuários da seed.

Consumes: F01: schema, seed e ambiente.

Ownership: identity, web account. Não alterar módulos de outras features sem amendment.

## Low-level design

Use autenticação por sessão Django com backend por e-mail normalizado (strip seguido de casefold conforme registro de interfaces), hash padrão com validators; tabela do usuário possui UNIQUE sobre o e-mail canônico. O formulário público não aceita papel, is_staff ou owner_id. A seed é o único caminho para organizador. `require_organizer` e `require_participant` retornam Actor imutável; visitante redireciona apenas no GET da UI, mutação sem sessão não tem efeito. F02 fornece somente o `owner_predicate(actor, resource_owner_id)` puro; não carrega nem bloqueia Event. F03 aplica esse predicado dentro de `event_guard`, incluindo owner no lookup/lock. A view nunca usa owner de formulário. Organizador alheio e ID ausente são indistinguíveis (404 genérico); papel errado 403. Revalidar Actor em cada comando de escrita.

**Rotas:** `/conta/cadastro/`, `/conta/entrar/`, `/conta/sair/` (POST com CSRF), retorno local via `url_has_allowed_host_and_scheme`; `/gestao/eventos/` exige organizador. Sessão server-side, cookie HttpOnly/SameSite=Lax, Secure somente TLS (ambiente local HTTP); CSRF em todos POSTs de browser. API com chave usa guarda própria, sem cookie auth. A sessão é rotacionada no login e invalidada no logout.

**Testes:** validação dos papéis pode usar fixture e handler de teste em F02; não inserir endpoints de debug no produto. F03/F07 fazem testes HTTP reais para cada rota de gestão. Testar XSS com texto de nome, HTML escapado; ausência de PAN ou senha em erro/log.

**Handoff:** `Actor`, guards de papel, `owner_predicate`, normalização para contas e credenciais seed. Lookup/lock de recurso pertence à feature dona do recurso; nunca confiar em IDs externos como identidade.

## Critérios e limites
| ID | Fase | Aceite |
| --- | --- | --- |
| A06 | local | Cadastro público cria somente participante, e-mail normalizado único; senha armazenada como hash; login válido e logout invalidam sessão; erro genérico em credenciais inválidas. |
| A07 | local | Guarda de papel e predicado de dono são aplicados em todos os recursos de gestão; no contrato local, validar com fixtures e endpoints de teste; as rotas reais são validadas em X03 e X11. |
| A08 | local | O serviço de identidade identifica participante por ID de sessão, não por e-mail ou parâmetro; parceiro não é uma identidade web. Titularidade real de ingressos é validada em X06/X16. |
| A30 | local | Cadastro ignora papel recebido; sessão é rotacionada no login e invalidada no logout; mutações web exigem CSRF e redirecionamento local seguro. |
| X01 | local | Após up com seed, A/B/P autenticam; duas execuções da seed não duplicam contas. |

## Evolução e rollback
Mudança de contrato exige ADR/amendment aprovado e reavaliação de consumidores. Em falha de implementação, corrigir em commit novo; não alterar migrations aplicadas nem relatórios. No MVP local usar ambiente de testes descartável para rollback de schema; não apagar volume de demonstração.
