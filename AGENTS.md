# AGENTS.md | instruções de execução

Este é um projeto greenfield. Não buscar, copiar ou adaptar a implementação do repositório de referência. O brief é normativo. O pacote inicial contém apenas design e ferramentas auxiliares; não afirmar que o produto existe ou que gates passaram quando não executados.

## Leitura obrigatória

1. `README.md`, `proposal.md`, `docs/prd/PRD.md`, `design.md`, `requirements-matrix.md`, `tasks.md` e `state/project-state.json`.
2. Para sua feature, `docs/features/Fxx-*/spec.md`, `plan.md`, `contract.md`, ADRs relevantes e `docs/engineering-guidelines.md`.
3. Carregar skills locais em `.agents/skills/`; seguir `docs/agents/workflow.md` para handoff/isolamento. Claude Code pode usar `CLAUDE.md`; as skills são também instruções textuais portáveis, não dependência de marketplace.

## Comandos

- `./bin/up` (F01 implementará): build, migrate, seed, readiness.
- `./bin/down`: parar todos os serviços do projeto sem apagar dados por padrão.
- `./bin/gates [Fxx]`: lint, documentação e testes, com DB isolado; sem argumento executa tudo.
- `python3 scripts/validate_docs.py` ou container Python descrito no README: disponível já no pacote.
- `scripts/partner_probe.py`: executável via Python somente após API implementada; ver `docs/validation/harness.md`.

## Regras inegociáveis

- Implementador nunca é avaliador. Novo contexto e SHA fixado para avaliar. Sem inventar evidência, sem alterar relatórios commitados.
- Não mudar contrato para passar teste. Se ambíguo, registrar proposta e obter aprovação do coordenador; atualizar critérios, matriz e consumidores antes de código.
- Toda mutação de evento/ticket segue lock de evento e ordem event→ticket→job. Não implementar compras separadas por canal.
- Não usar SQLite para prova concorrente; não persistir cartão. Não usar dados/segredos reais.
- Usar branches por feature e limites de escrita; migrations compartilhadas com coordenador. Antes de W5, congelar interfaces.
- Testar falhas, estados terminais, segurança e integração. Sem skips para requisitos obrigatórios. Gates retornam não zero em falha.
- Não usar `git push --force`, reescrever histórico de relatórios ou editar branches alheias. Não fazer deploy.
- Estado inicial planejado; coordenador atualiza status e links com fatos verificados. Leia os artefatos referenciados no README para mapa completo.
