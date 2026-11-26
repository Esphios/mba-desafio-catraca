# F02 | FDD: Identidade e autorização

Status: planejado. Wave W2. Fonte: PRD e HLD; ADRs propostos. Este FDD não atesta código existente.

## Objetivo, provides e consumes
Cadastro/login/logout, sessão, funções require_participant e require_owner, identidade dos usuários da seed.

F01: schema, seed e ambiente.

## Limites de escrita
identity/, identity templates/tests; register routes through F01 seam; no event mutations.

## Design detalhado
`identity/` owns authentication and guards. Reuse account from F01, no second user model or migrations unless coordinated. Form validates name/email/password and normalizes email; handle uniqueness violation safely. Login authenticates by email with framework hash; generic error, session rotation, validate local next. Logout POST invalidates session. `require_owner` compares immutable account id; read query scopes owner_id, write rechecks under lock. Test role field injection and unauthorized data on both HTML and POST; F03 adds event routes, so F02 validates guards with real model fixtures and test-only views, X03 later exercises actual route. Do not expose organizer self-signup. Partner key remains F06.

## Dependências e integração
F01. Consumir interfaces do HLD, não importar views de outras features. Em caso de interface insuficiente, registrar bloqueio e pedir amendment; não criar cópia de regra. Contratos externos e códigos do brief têm precedência. Dependências cross-feature: X01; ver contrato.

## Critérios locais e casos de falha
- A06 (R13): Cadastro público cria somente participante, e-mail normalizado único; senha armazenada como hash; login válido e logout invalidam sessão; erro genérico em credenciais inválidas.
- A07 (R13): Visitante e participante não acessam rotas de gestão; B não lê nem modifica eventos de A, incluindo URL direta e POST forjado.
- A08 (R09,R13): Participante só tem acesso aos próprios recursos; parceiro não cria sessão web nem vincula conta pelo e-mail.

## Testabilidade e segurança
Usar fixtures mínimas isoladas; relógio injetável para lógica, modo padrão para prazo real. Validar entradas e falhas além de happy path. Nenhum dado real, nenhuma modificação de contrato para mascarar falha. Evidência independente no contrato.

## Rollback e evolução
Em falha, manter branch sem merge e corrigir com novo commit. Mudanças de schema após F01 exigem migração revisada, teste fresh/upgrade e coordenação. Não desfazer migração de dados em ambiente de usuário sem backup; neste MVP usar ambiente descartável de teste. Regressão final obrigatória após última integração.
