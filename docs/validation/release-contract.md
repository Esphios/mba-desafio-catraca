# Contrato de release | W6

Pré-requisito: main integrada, clone novo, delays padrão, Docker/Git; avaliação independente. Não aceitar relatórios locais como substituto do fluxo.

## C-RELEASE-P01

PRD >=5 features, fornece/consome, DAG e waves; todas R01–R13 citadas, cada aresta coberta. Evidência: TEST-P01; verificar no fluxo, arquivos e histórico.

## C-RELEASE-P02

Spec, plano e contrato por feature, todos os critérios e cross-feature mapeados. Evidência: TEST-P02; verificar no fluxo, arquivos e histórico.

## C-RELEASE-P03

Cada feature aprovada em avaliação independente; relatório imutável com data, SHA, ferramenta, modelo, evidência por item. Evidência: TEST-P03; verificar no fluxo, arquivos e histórico.

## C-RELEASE-P04

Estado final bate com relatórios existentes e mais recentes; sem status concluído sem aprovação. Evidência: TEST-P04; verificar no fluxo, arquivos e histórico.

## C-RELEASE-P05

Pelo menos uma wave paralela via PRs mergeados; primeiro commit de cada PR anterior ao último de todos os demais. Evidência: TEST-P05; verificar no fluxo, arquivos e histórico.

## C-RELEASE-P06

Repo público único, main com README completo; fluxo externo 1–18 aprovado em clone limpo. Evidência: TEST-P06; verificar no fluxo, arquivos e histórico.

Incluir relatório do fluxo integrado 1–18, erros e regressões. Todos P01–P06 e X14–X16 devem passar.
