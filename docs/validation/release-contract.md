# Contrato de release | W6

Pré-requisito: main integrada, clean clone, real scale, histórico completo e PRs públicos. Todos os itens locais e integrados aprovados; fluxo sem skip.

## C-RELEASE-P01 (P01)

main final, clone completo com histórico Git, PRs acessíveis e ambiente padrão.

Executar validate_docs e revisar DAG, regras, escopo e cada critério.

PASS: PRD >=5 features, fornece/consome, DAG e waves; todas R01–R13 citadas, cada aresta coberta.

Teste: TEST-P01.

## C-RELEASE-P02 (P02)

main final, clone completo com histórico Git, PRs acessíveis e ambiente padrão.

Inspecionar todos os FDD, planos, contratos e mapeamentos; validar existência dos testes.

PASS: Spec, plano e contrato por feature, todos os critérios e cross-feature mapeados.

Teste: TEST-P02.

## C-RELEASE-P03 (P03)

main final, clone completo com histórico Git, PRs acessíveis e ambiente padrão.

Rodar validate_evidence --release e conferir evidência original, SHA, sessão, modelo e imutabilidade.

PASS: Para cada feature há relatório novo e imutável, com data UTC, SHA completo, ferramenta, modelo, identidade de sessão e evidência por item; último relatório integrado aprova tudo aplicável.

Teste: TEST-P03.

## C-RELEASE-P04 (P04)

main final, clone completo com histórico Git, PRs acessíveis e ambiente padrão.

Cruzar state, relatórios mais recentes, SHAs e PRs; confirmar todos os status.

PASS: Estado final aponta ao último relatório aprovado, commit implementado e PR de cada feature; nenhum concluído sem integração verificada.

Teste: TEST-P04.

## C-RELEASE-P05 (P05)

main final, clone completo com histórico Git, PRs acessíveis e ambiente padrão.

Abrir PRs da wave, conferir merge e lista de commits; testar sobreposição estrita para cada par.

PASS: Pelo menos uma wave paralela via PRs mergeados; primeiro commit de cada PR anterior ao último de todos os demais.

Teste: TEST-P05.

## C-RELEASE-P06 (P06)

main final, clone completo com histórico Git, PRs acessíveis e ambiente padrão.

Clonar main em pasta vazia, rodar os 18 passos, conferir README e repo público.

PASS: Repo público único, main com README completo; fluxo externo 1–18 aprovado em clone limpo.

Teste: TEST-P06.

## Blocking condition
Qualquer falha de 1–18 ou X14–X16, falta de relatório independente, histórico alterado, estado ou PR ausente impede release. Validador estrutural não comprova verdade de evidência; revisar manualmente outputs.
