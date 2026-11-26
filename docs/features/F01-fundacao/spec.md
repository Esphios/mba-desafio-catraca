# F01 | FDD: Harness e persistência

Status: planejado. Wave W1. Fonte: PRD e HLD; ADRs propostos. Este FDD não atesta código existente.

## Objetivo, provides e consumes
Ambiente Compose, schema compartilhado, clock, runner, dados de demonstração e interfaces de registro de rotas.

Nenhuma feature anterior.

## Limites de escrita
Container, schema, configuration, tooling and only initial shared files. No app domain features.

## Design detalhado
`compose.yaml`, `Dockerfile`, `bin/`, `config/`, `catraca_platform/`, shared models and migrations. Schema from HLD must be defined before any dependent feature. Create custom account model first, then event/ticket/job. Model constraints and enum labels fixed. Seed command uses stable normalized emails, update_or_create or get_or_create with explicit role verification; no reset of business records. Do not create event fixtures in production seed; tests create fresh events. Health checks DB and worker heartbeat. Compose worker skeleton runs idle until F04. Initial route stubs for later features must not pretend to implement business behavior. The baseline URL registry includes each feature URL module only when present or empty placeholder. Document per-worktree port/project and test DB cleanup.

## Dependências e integração
Nenhuma. Consumir interfaces do HLD, não importar views de outras features. Em caso de interface insuficiente, registrar bloqueio e pedir amendment; não criar cópia de regra. Contratos externos e códigos do brief têm precedência. Dependências cross-feature: nenhuma; ver contrato.

## Critérios locais e casos de falha
- A01 (H01): Clone limpo: ./bin/up constrói, migra, semeia e espera web/worker/DB prontos; /health/ready retorna 200 sem configuração manual.
- A02 (H02): ./bin/down encerra todos os containers e portas iniciados; nova subida conserva dados e seed não duplica contas.
- A03 (H03): ./bin/gates falha com teste quebrado, executa testes reais e lint, usa DB isolado e passa com testes válidos.
- A04 (H04): AGENTS.md e README contêm comandos, endereços, credenciais de seed, mapa; modo padrão não exige gateway real.
- A05 (R05,R09): Schema possui FKs, unicidade de código, restrições de status, lotação e preço; migrações reexecutáveis.

## Testabilidade e segurança
Usar fixtures mínimas isoladas; relógio injetável para lógica, modo padrão para prazo real. Validar entradas e falhas além de happy path. Nenhum dado real, nenhuma modificação de contrato para mascarar falha. Evidência independente no contrato.

## Rollback e evolução
Em falha, manter branch sem merge e corrigir com novo commit. Mudanças de schema após F01 exigem migração revisada, teste fresh/upgrade e coordenação. Não desfazer migração de dados em ambiente de usuário sem backup; neste MVP usar ambiente descartável de teste. Regressão final obrigatória após última integração.
