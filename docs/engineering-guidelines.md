# Engineering Guidelines

## Princípios e stack

Python 3.12 + Django 5.2 LTS + psycopg + PostgreSQL 17; Gunicorn, Ruff, Playwright. Fixar patches e hashes em lockfile, imagens e browsers no container; atualizar via PR com gates. Desenvolvimento Windows somente WSL (repo no filesystem Linux, não em /mnt/c). Não exigir Make, curl, Python, jq ou browser no host. Bash e Docker Compose; documentação em pt-BR, identificadores e código em inglês. Preferir domínio explícito, typed dataclasses, enums, funções pequenas e composição; evitar abstrações sem consumidores.

## Domínio e persistência

- Controllers traduzem entrada/saída; serviços detêm invariantes; DTOs não vazam modelos nem PAN. Não duplicar lógica por canal. Todas as mutações de evento/ingresso usam event_guard e transação curta, READ COMMITTED; nenhuma query de ocupação antes do lock. Ordem Event→Ticket→Job. Não confiar em mutex de processo, count trigger sem lock, clamp de disponibilidade ou query de dashboard em múltiplos snapshots.
- Models e migrations em coredata, custom User em accounts; após merge, migrations imutáveis, alterações novas. Índices e constraints justificadas; fixtures só em testes. Evitar signals/admin bulk update que contornem serviços. Querysets avaliados dentro de atomic quando bloqueio necessário. Rollback testado. JSON numérico exato, Decimal para moeda, UTC para DB.
- Input validation server-side, role e ownership em serviço; secrets demo only; CSRF em browser; API guard antes do parser. Escapar HTML; não logar corpo, cookie ou cartão.

## Testes e qualidade

Test names/tags contêm TEST-ID; caso Given/When/Then, oracle não usa mesma função em teste de integração (calcular independentemente). Unit pure; DB real via TransactionTestCase e conexões independentes; HTTP sem redirect; browser semantic locators; concorrência com barrier; teste timing real sem timeout inflado. Nenhuma suite vazia considerada sucesso. Cobrir negativos, rollback, restart, erro precedence, race orders. Não usar fixtures para fluxo final. Flake é defeito a investigar, não aumentar retries; logs preservados. Mutation negativa de lock e gate comprova sensibilidade da suíte. Evidência real por item.

## Git e colaboração

Uma feature/branch/worktree; commits pequenos com intenção e teste, sem commits artificiais ou datas alteradas. Não reformatação massiva de módulos alheios. Changes de shared files exigem coordenação. PR descreve critério, teste, riscos, migrações, links; avaliador distinto da sessão implementadora. Merge serial após aprovação local, reexecutar gates e avaliar mudanças de contrato. Sem editar relatórios existentes. Coordenador atualiza estado global. Não remover falhas do histórico.

## Checklist pré-commit

- [ ] Critérios e tarefas rastreados, arquivos dentro de ownership.
- [ ] Lint/format/check e migrations sem drift.
- [ ] Testes positivos e negativos executados, saída preservada.
- [ ] Sem segredo/PAN/dados reais, logs redigidos.
- [ ] Revisar transações/locks, autorização e efeitos cruzados quando aplicável.
- [ ] README/contrato atualizado se mudança autorizada; ADR quando decisão estrutural.
- [ ] Não marcar PASS ou completed por autoavaliação.

## Manutenção documental

Brief > PRD > design e ADRs > FDD/contract > plan/tasks > implementação. Se divergência, bloquear e submeter amendment, nunca alterar o requisito para acomodar código. JSON de rastreabilidade gera matriz; revisar semântica além de validação mecânica. Diagramas representam design, revalidar após mudança. Relatórios e evidências são históricos, não documentos vivos. Registrar desvios aprovados e reavaliar dependentes.
