# W0 | Procedimento de aprovação e registro

O procedimento foi executado sobre o commit ratificado
`19059603b450981630477dac3732acfdc8fe9d1d`. A aprovação humana explícita ocorreu
em 2026-11-27; o G0 passou e está registrado em
`runs/20261127T0931-0300-ratification-g0/`. W1 só começa após revisão independente
deste registro e commit separado de `state/project-state.json`.

1. Produto: fornecer brief normativo original ou registrar confirmação explícita de que PRD, OpenAPI, matriz e contratos são a fonte autorizada. Validar R01–R13, fluxo 1–18, escopo, mensagens e faixas de tempo. Confirmar as decisões propostas de normalização, cap de corpo, ownership e permissões de banco.
2. Arquitetura: revisar `AMENDMENT-001.md`, ADRs e `docs/architecture/version-manifest.md`; confirmar patches e hashes/digests de Python 3.12, Django 5.2 LTS, psycopg, PostgreSQL 17, Gunicorn, Ruff, Playwright/browser, ferramenta OpenAPI 3.1 e Mermaid. Guardar versão exata, origem, digest por arquitetura, resolução de dependências e comandos reais. Não usar `latest`. W1 materializa lockfile da aplicação e imagens com esses pins; nenhuma aplicação deve ser criada na W0.
3. Ambiente: em máquina Linux/macOS suportada e WSL quando aplicável, comprovar Docker Engine, Compose, Git, arquitetura e execução real de containers de ferramenta com pins. Registrar saída de `docker version`, `docker compose version`, `git --version`, `uname -a`; guardar resultado de smoke e versão Python dentro do container. Não confundir smoke de ferramenta com smoke da aplicação.
4. Reproduzir G0 sob Python 3.12: executar `scripts/validate_docs.py`, `scripts/verify_model.py`, `scripts/test_baseline.py`, `scripts/validate_evidence.py` e `docs/validation/w0-audit/reproduce_mutations.py`; registrar saída/exit de cada comando. Os testes Git requerem Git completo, inclusive dentro do container. `validate_evidence.py --release` deve falhar em W0. Usar um clone limpo com histórico completo, não somente ZIP extraído sem Git.
5. Executar validador formal OpenAPI 3.1 sobre `docs/interfaces/partner.openapi.json` (por exemplo CLI openapi-spec-validator em versão pinada e verificada); renderizar cada fence Mermaid de `design.md`, `docs/prd/PRD.md` e demais Markdown usando CLI Mermaid em imagem pinada. Guardar versões, comandos, exit codes e SVGs/inspeção visual. Não substituir por hash ou contagem de rotas.
6. Demonstrar separação de contexto com duas sessões reais novas da ferramenta de agentes escolhida, sem repassar transcrição entre elas. Registrar identidade, configuração de worktree, acessos e procedimento de handoff com evidência; sem inventar sessão/feature de teste. Avaliador de feature só após candidato verdadeiro.
7. Produto e arquitetura aprovam explicitamente o pacote corrigido e o manifesto de versões. Coordenador registra decisões, evidências anteriores e aceite em commit real; revisar mudanças normativas e preservar critérios. Após gate G0 integral, registrar SHA completo desse commit em `state/project-state.json`, `baseline=approved`, `currentWave=1`; manter todas as features planned até despacho F01. Commitar alteração de estado separadamente. Nenhum campo deve ser preenchido com aprovação fictícia.

## Legado: retomada do pacote de auditoria importado

As instruções abaixo descrevem somente o ZIP/bundle histórico que originou esta
árvore; não são o procedimento para o repositório vivo atual. Para auditar o estado
atual, use clone completo do remoto e o SHA candidato. No pacote legado, extraia o
ZIP e execute no diretório extraído:

```bash
git clone catraca-design.bundle catraca
a=$(git -C catraca rev-parse HEAD)
git -C catraca log --oneline
git -C catraca status --short
printf '%s\n' "$a"
```

O remoto `origin` desse clone aponta ao bundle local, não a GitHub. Criar/conectar remoto público somente com autorização e seguir o fluxo real de PRs; nenhuma entrega/PR externo foi produzido nesta revisão.
