# Tasks | backlog executável por agentes

Todos os itens começam abertos. O coordenador é o único escritor do estado global. Não iniciar consumidor antes do provider estar na main com local PASS e interface congelada. Aprovado local não equivale a concluído.

## W0 | design gate

- [ ] T-W0-01: produto revisa R01–R13, API, limites, casos ambíguos e escopo; skill `prd-design`. Validar PRD, matriz e contrato OpenAPI.
- [ ] T-W0-02: arquiteto revisa HLD/FDD, ADRs, diagramas, versões, lock order e harness; skills `architecture-review`, `schema-review`, `transaction-safety`. Rodar `python3 scripts/validate_docs.py` e `python3 scripts/verify_model.py`; revisar hipóteses.
- [ ] T-W0-03: inicializar repositório novo, escolher ferramenta de agentes, validar compatibilidade Docker/Compose e WSL, resolver e registrar versões/digests verificados (lockfile e imagens são entrega W1), validar G0 completo e sessões isoladas, registrar SHA baseline e aprovação explícita do produto; skill `wave-orchestration`.

## Backlog de implementação

### W1 / F01 | Ambiente reproduzível e persistência

| Tarefa | Entrega | Skills | Testes / gate | Predecessor |
| --- | --- | --- | --- | --- |
| T-F01-01 | Materializar os pins aprovados na W0 em runtime, Dockerfile, Compose, lockfile, estrutura de comandos e lint; implementar health inicial. | harness-engineering, schema-review, feature-implementation | TEST-A03 | W0 |
| T-F01-02 | Criar user custom e models/schema, constraints, índices e migrations; rodar testes de integridade. | harness-engineering, schema-review, feature-implementation | TEST-A05 | T-F01-01 |
| T-F01-03 | Implementar bootstrap, seed e scripts de subida/descida/gates; validar clone limpo. | harness-engineering, schema-review, feature-implementation | TEST-A01, TEST-A02, TEST-A04 | T-F01-02 |
| T-F01-04 | Verificar fail-closed do harness, isolamento e documentação; fornecer interface e avaliação. | harness-engineering, schema-review, feature-implementation | TEST-A01, TEST-A02, TEST-A03, TEST-A04, TEST-A05, TEST-A29, TEST-A37 | T-F01-03 |

### W2 / F02 | Identidade e fronteiras de acesso

| Tarefa | Entrega | Skills | Testes / gate | Predecessor |
| --- | --- | --- | --- | --- |
| T-F02-01 | Implementar cadastro, login e logout com Django; validação de e-mail e senha. | secure-boundaries, feature-implementation | TEST-A06 | F01 |
| T-F02-02 | Expor Actor/guards e predicado de dono; comportamento de erros e redirects. | secure-boundaries, feature-implementation | TEST-A07, TEST-A08 | T-F02-01 |
| T-F02-03 | Testar CSRF, role escalation, session replay, ownership por fixture, sanitização. | secure-boundaries, feature-implementation | TEST-A30 | T-F02-02 |
| T-F02-04 | Validar seed em ambiente real e congelar contrato de acesso. | secure-boundaries, feature-implementation | TEST-A06, TEST-A07, TEST-A08, TEST-A30, TEST-X01 | T-F02-03 |

### W3 / F03 | Administração e catálogo de eventos

| Tarefa | Entrega | Skills | Testes / gate | Predecessor |
| --- | --- | --- | --- | --- |
| T-F03-01 | Implementar DTO, validação e persistência de draft, formulário de edição. | transaction-safety, secure-boundaries, feature-implementation | TEST-A09 | F01, F02 |
| T-F03-02 | Implementar lock, edição/publicação e consultas de ocupação; casos limite e estado terminal. | transaction-safety, secure-boundaries, feature-implementation | TEST-A11, TEST-A12, TEST-A31 | T-F03-01 |
| T-F03-03 | Implementar páginas de gestão e slot operacional; integração com identidade. | transaction-safety, secure-boundaries, feature-implementation | TEST-A10 | T-F03-02 |
| T-F03-04 | Executar testes de estado, data, dono e DB; fixar interface para F04/F05/F06/F07. | transaction-safety, secure-boundaries, feature-implementation | TEST-A09, TEST-A10, TEST-A11, TEST-A12, TEST-A31, TEST-X02, TEST-X03 | T-F03-03 |

### W4 / F04 | Livro de ingressos e liquidação simulada

| Tarefa | Entrega | Skills | Testes / gate | Predecessor |
| --- | --- | --- | --- | --- |
| T-F04-01 | Criar Buyer/Ticket DTO, validador de cartão, classificação de gateway e código. | transaction-safety, payment-simulation, feature-implementation | TEST-A17 | F01, F03 |
| T-F04-02 | Implementar reserve atômico, savepoint de colisão e rollback ticket/job; stress. | transaction-safety, payment-simulation, feature-implementation | TEST-A13, TEST-A14, TEST-A32 | T-F04-01 |
| T-F04-03 | Implementar worker durável, due_at, restart e proteção de terminal; timing real. | transaction-safety, payment-simulation, feature-implementation | TEST-A15, TEST-A16, TEST-A33 | T-F04-02 |
| T-F04-04 | Executar concorrência, corrida preço/capacidade e avaliação de interfaces. | transaction-safety, payment-simulation, feature-implementation | TEST-A13, TEST-A14, TEST-A15, TEST-A16, TEST-A17, TEST-A32, TEST-A33, TEST-X04, TEST-X05 | T-F04-03 |

### W5 / F05 | Jornada de participante

| Tarefa | Entrega | Skills | Testes / gate | Predecessor |
| --- | --- | --- | --- | --- |
| T-F05-01 | Implementar catálogo público e detalhe com estados vazio/lotado. | secure-boundaries, browser-validation, feature-implementation | TEST-A18 | F02, F03, F04 |
| T-F05-02 | Implementar compra, mapeamento de erros e Meus ingressos por identidade. | secure-boundaries, browser-validation, feature-implementation | TEST-A19, TEST-A20 | T-F05-01 |
| T-F05-03 | Testar fluxo browser, negativos, titularidade, CSRF e status. | secure-boundaries, browser-validation, feature-implementation | lint, unitário específico e teste negativo | T-F05-02 |
| T-F05-04 | Avaliar dependências anteriores; entregar handoff sem modificar F06/F07. | secure-boundaries, browser-validation, feature-implementation | TEST-A18, TEST-A19, TEST-A20, TEST-X06, TEST-X07, TEST-X08 | T-F05-03 |

### W5 / F06 | Integração comercial por API

| Tarefa | Entrega | Skills | Testes / gate | Predecessor |
| --- | --- | --- | --- | --- |
| T-F06-01 | Implementar guard e serialização; tratamento explícito do parser e erros. | partner-api-contract, concurrency-validation, feature-implementation | lint, unitário específico e teste negativo | F03, F04 |
| T-F06-02 | Ligar três rotas ao catálogo/ledger; OpenAPI e fixtures. | partner-api-contract, concurrency-validation, feature-implementation | TEST-A21, TEST-A22, TEST-A23 | T-F06-01 |
| T-F06-03 | Validar auth/precedência, malformed JSON, carga e consultas. | partner-api-contract, concurrency-validation, feature-implementation | TEST-A24, TEST-A34 | T-F06-02 |
| T-F06-04 | Avaliar local e preparar testes de canais mistos para integração. | partner-api-contract, concurrency-validation, feature-implementation | TEST-A21, TEST-A22, TEST-A23, TEST-A24, TEST-A34, TEST-X09, TEST-X10 | T-F06-03 |

### W5 / F07 | Operação do evento e apuração

| Tarefa | Entrega | Skills | Testes / gate | Predecessor |
| --- | --- | --- | --- | --- |
| T-F07-01 | Implementar decisão de check-in e escrita única; formulário/POST com autorização. | transaction-safety, secure-boundaries, concurrency-validation, feature-implementation | TEST-A25 | F02, F03, F04 |
| T-F07-02 | Implementar cancelamento terminal e testes gateway tardio + corrida. | transaction-safety, secure-boundaries, concurrency-validation, feature-implementation | TEST-A26 | T-F07-01 |
| T-F07-03 | Construir painel agregado e integrar partial; validar snapshot e números. | transaction-safety, secure-boundaries, concurrency-validation, feature-implementation | TEST-A27, TEST-A28, TEST-A35 | T-F07-02 |
| T-F07-04 | Rodar concorrência adversarial e avaliação local; integrar X14/X15 posteriormente. | transaction-safety, secure-boundaries, concurrency-validation, feature-implementation | TEST-A25, TEST-A26, TEST-A27, TEST-A28, TEST-A35, TEST-A36, TEST-X11, TEST-X12, TEST-X13 | T-F07-03 |

## W5 | paralelismo comprovável

- [ ] T-W5-00: congelar interfaces e schema F01–F04. Criar 3 branches/worktrees no mesmo SHA; nomes e portas distintas. Skill `wave-orchestration`; validar worktrees e Compose configs.
- [ ] T-W5-01: iniciar implementadores F05, F06 e F07 simultaneamente; primeiro commit útil de cada PR antes de finalizar os demais; gravar fatos reais, não manipular datas.
- [ ] T-W5-02: avaliar cada branch com contrato local e contexto novo. F07 usa overrides dos hooks precriados para A28 sem editar wiring; após seu local PASS/merge, o coordenador troca os defaults em commit separado, repete A28 e registra o SHA antes de X14/X15. PENDING_INTEGRATION permitido somente para itens integrados. Corrigir FAIL com novo relatório, sem editar o anterior. Integrar um PR por vez e executar regressão; alterações de interfaces exigem reavaliação.

## W6 | integração e entrega

- [ ] T-W6-01: verificar merges, sobreposição de commits e handoffs; conferir estado `merged_local` e evidências; skill `wave-orchestration`.
- [ ] T-W6-02: rodar TEST-X14, TEST-X15, TEST-X16 e fluxo 1–17 no clone limpo da main, gateway padrão; skills `independent-evaluation`, `release-validation`. Avaliar novamente F06/F07 com todos os itens e F05 se alterada ou se regressão X14/X16 indicar falha; registrar relatório novo. Regressão falha bloqueia release, abrir PR corretivo.
- [ ] T-W6-03: validar TEST-P01–P06 e passo 18; gerar relatório final, atualizar README/state, validar evidências e histórico, rodar gates final. Skill `release-validation`.

## Estimativa e decisões
O brief prevê 8–12 h somando trabalho humano/agentes; não é SLA. Reserve ~1h W0, 2h fundação/identidade, 2–3h catálogo/ledger, 2–3h wave paralela, 1–2h integração. Se tempo curto, reduzir itens opcionais (telemetria extra), nunca requisitos obrigatórios.

## Definition of Done
Cada etapa tem testes e commit; feature tem contrato local aprovado por agente independente e PR mergeado; `completed` somente quando todos os itens aplicáveis, inclusive integrados, tiverem evidência real. Release exige todos completos, gates reais, histórico de relatórios e fluxo de 18 passos.
