# Catraca | desenvolvimento local

Fundação Django/PostgreSQL do MVP Catraca. O ambiente local usa somente o
simulador de pagamento; nenhuma chave ou integração externa é necessária.

## Como rodar

Pré-requisitos: Docker/Compose e Git. No Windows, execute dentro do WSL com o
repositório no filesystem Linux. Não é preciso copiar .env nem instalar Python.

    bash bin/up
    bash bin/down
    bash bin/gates
    bash bin/gates --feature F01
    bash bin/gates --release

bin/up constrói a imagem pinada, sobe o banco sem publicar sua porta, executa
migrations e seed uma vez e espera web/worker prontos. bin/down remove os
serviços e listeners do projeto, preservando o volume. Uma nova subida conserva
os dados e não duplica a seed. bin/gates usa projeto, porta e volume descartáveis,
executa lint, aplica migrações em PostgreSQL, verifica o schema, roda os testes
reais e os validadores documentais e limpa seus recursos em sucesso, falha ou
interrupção. `--feature F01` também valida as evidências do candidato.
`--release` exige estado, relatórios e histórico completos para release.
Use um clone com histórico Git completo.

Para worktrees paralelos, escolha projeto e porta exclusivos:

    CAT_PROJECT=catraca-f01 CAT_PORT=18083 bash bin/up
    CAT_PROJECT=catraca-f01 CAT_PORT=18083 bash bin/down

## Endereços e defaults

- WEB e API: http://127.0.0.1:8080
- Readiness: http://127.0.0.1:8080/health/ready
- Liveness: http://127.0.0.1:8080/health/live
- CAT_PROJECT=catraca-demo
- CAT_PORT=8080
- CAT_PROFILE=demo
- CAT_GATEWAY_SCALE=1
- CAT_PARTNER_KEY=local-passgate-26

CAT_PORT altera a porta. O perfil demo exige escala 1. CAT_SECRET tem um valor
padrão de desenvolvimento local. A API futura começa em /api/partner.

## Credenciais de seed sintéticas

| Papel         | E-mail                | Senha        |
| ------------- | --------------------- | ------------ |
| Organizador A | gestao.a@example.test | LocalA-2026! |
| Organizador B | gestao.b@example.test | LocalB-2026! |
| Participante  | pessoa@example.test   | LocalP-2026! |

X-Api-Key: local-passgate-26. Apenas demo local, nunca reutilizar em produção.
A seed roda somente em perfis demo/test, usa hash Django, é idempotente pelo
e-mail canônico e preserva contas que não pertencem a ela.

## Mapa dos artefatos

- [Proposal](proposal.md), [Design/HLD](design.md), [Matriz](requirements-matrix.md) e [Tasks](tasks.md).
- [PRD](docs/prd/PRD.md), [ADRs](docs/architecture/adrs/README.md), [interfaces](docs/interfaces/internal.md), [OpenAPI](docs/interfaces/partner.openapi.json) e [contrato web](docs/interfaces/web.md).
- [Manifesto de versões W0](docs/architecture/version-manifest.md) e [guidelines](docs/engineering-guidelines.md).
- Features, spec/plan/contract/reports em docs/features/.
- [Gates](docs/validation/harness.md), [catálogo de testes](docs/validation/test-catalog.md), [fluxo de avaliação](docs/validation/evaluator-flow.md) e [release contract](docs/validation/release-contract.md).
- [AGENTS](AGENTS.md), [skills](.agents/skills/README.md), [workflow](docs/agents/workflow.md) e [state](state/project-state.json).

## Estado e próximos contratos

F01 fornece ambiente, schema, seed, clock e worker de heartbeat. O worker desta
etapa não consome jobs; F04 preservará o entrypoint e acrescentará liquidação
durável. F02 implementará login das contas seed. Os probes partner/browser
dependem das features posteriores e não substituem os gates por feature.

- `accounts.email_policy.normalize_email(value)` retorna o e-mail canônico.
- `catraca_platform.clock.clock_now()` devolve um datetime UTC com fuso. O
  clock de prazos persistidos será obtido do PostgreSQL sob o lock do evento.
- `tests.fixtures.fixture_factory(scenario, **overrides)` cria dados sintéticos
  isolados para `organizer`, `participant` e `event`, exclusivamente em testes.
- `worker.main.worker_command(worker_id, stop)` atualiza o heartbeat até receber
  o sinal de parada. Compose executa `python -m worker.main`.
- `config.management_provider` resolve os settings `MANAGEMENT_PROVIDER`,
  `MANAGEMENT_PARTIAL` e `MANAGEMENT_OPERATIONS_URLCONF`. O provider padrão
  referencia `catalog.management.basic_management_snapshot`, a ser entregue
  na F03. O partial é um caminho de template exposto por atributo Python e o
  URLconf é um módulo. F03 renderiza o partial quando configurado e monta os
  padrões de operações na URL de gestão. Ambos começam vazios.

W5 executa F05/F06/F07 em branches paralelas. Links, SHAs e sobreposição de PRs
somente serão registrados pelo coordenador quando existirem de fato.
