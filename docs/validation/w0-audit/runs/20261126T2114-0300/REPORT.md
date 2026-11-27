# W0 | Retomada técnica em 2026-11-26

**Veredito: BLOCKED.** Este registro é evidência de retomada e diagnóstico no SHA
`b159b3d70f6bdef6775589528d1b247fb09407aa`; não é aprovação de produto,
aprovação de arquitetura nem avaliação de feature. W1 não foi iniciada e
`state/project-state.json` permanece `baseline=proposed`, `baselineCommit=null`,
`currentWave=0`.

## Proveniência e isolamento

- A leitura começou enquanto o repositório estava em `66fa620163754bad1a720c3c7cbe0c126906673c`.
  O HEAD avançou concorrentemente para `b159b3d70f6bdef6775589528d1b247fb09407aa`
  por ação externa a esta coordenação. Após o avanço, todas as revisões foram
  reconciliadas no SHA final e a árvore estava limpa antes das mudanças desta retomada.
- Cinco contextos novos, sem histórico herdado, executaram revisões somente leitura:
  `w0_product_traceability`, `w0_architecture`, `w0_features_interfaces`,
  `w0_validation_governance` e `w0_git_environment`. Nenhum deles editou arquivos
  ou se apresentou como avaliador de feature.
- O coordenador leu os documentos obrigatórios, as 14 skills locais, arquitetura,
  ADRs, interfaces, governança e spec/plan/contract de F01–F07.

## Git e ambiente observado

| Item | Resultado |
| --- | --- |
| Branch / upstream | `main`, um commit à frente de `origin/main` |
| Worktrees | apenas o worktree atual |
| Remoto | `https://github.com/Esphios/mba-desafio-catraca.git` |
| Git | `2.52.0.windows.1` |
| Python host | `3.12.10` (`python` e `python3`); launcher `py` aponta para 3.14 ausente |
| Docker | cliente `29.9.2 windows/amd64`; daemon recuperado como `29.9.2 linux/amd64` |
| Compose | `v5.6.1` |
| WSL | `2.6.3.0`, Ubuntu WSL2, kernel `6.6.87.2`, `x86_64` |
| Node | `24.12.0` |

O Docker Desktop estava instalado, mas o daemon não estava ativo. Ele foi iniciado
e respondeu ao smoke Linux. Isso prova o ambiente WSL/amd64 desta máquina, não
compatibilidade do produto inexistente, macOS ou execução arm64.

## Comandos G0 e resultados reais

| Comando | Exit | Resultado observado |
| --- | ---: | --- |
| `python scripts/test_validate_docs_parser.py` | 0 | 1 teste passou |
| `python scripts/validate_docs.py` | 1 | drift normativo em PRD e traceability |
| `python scripts/verify_model.py` | 0 | 4.290 estados, 36.558 transições; mutante de oversell rejeitado |
| `python scripts/test_baseline.py` | 1 | aborta porque a baseline sem mutação já falha |
| `python scripts/validate_evidence.py` | 1 | propaga os dois drifts normativos |
| `python scripts/validate_evidence.py --release` | 1 | drifts + F01–F07 incompletas + ausência de merge/PR + release state incompleto |
| `python docs/validation/w0-audit/reproduce_mutations.py` | 1 | aborta porque a baseline sem mutação já falha |
| `python -m compileall -q scripts docs/validation/w0-audit/reproduce_mutations.py` | 0 | sintaxe compilada |

O modo release falhou como esperado em W0, mas o resultado também contém o drift
anterior; não é uma prova isolada do gate de release.

## Causa raiz do gate documental

1. `normative-lock.json` foi criado no mesmo commit do PRD e traceability, porém os
   hashes registrados nunca correspondem ao conteúdo commitado atual:

   | Artefato | SHA-256 registrado | SHA-256 real |
   | --- | --- | --- |
   | `docs/prd/PRD.md` | `fde12c0a9f0e8a77ec3871735bc5465be79257beb371db095e9ee2b1234aa405` | `19569faf6b4d02aac619134d656909371d7654ad879ef865f5c9eab88504a1f2` |
   | `docs/validation/traceability.json` | `c756958bd2d41c621a00f7f8b0df6730140a1f87ab5c679d2f445f8439f630b2` | `74f79c4afe563693544db1a13f162f39ec527b837891f525ebd3fdaacdf1e812` |
   | `docs/interfaces/partner.openapi.json` | `22d03f15dd60133f7d46e271e5f9fad2ff812d0f1b826c29797fea58f6845d6d` | igual ao registrado |

2. O parser do PRD exigia exatamente `| A01 |`, mas o Markdown usa alinhamento
   `| A01      |`. Um teste focal foi escrito e observado falhando antes da correção.
   A correção aceita whitespace de alinhamento e removeu apenas o falso
   `PRD acceptance/rules mismatch`; os dois drifts reais continuam bloqueando o gate.

Nenhum hash normativo foi regenerado e nenhum conteúdo protegido foi alterado.

## OpenAPI e Mermaid

- `openapi-spec-validator 0.7.2`, em `python:3.12.12-slim-bookworm`, validou
  explicitamente schema 3.1: `partner.openapi.json: OK`. Duas tentativas anteriores
  falharam por invocação/quoting da ferramenta e não foram contabilizadas como validação.
- `mermaid-cli 11.12.0`, imagem
  `ghcr.io/mermaid-js/mermaid-cli/mermaid-cli:11.12.0`
  (`sha256:bad64c9d9ad917c8dfbe9d9e9c162b96f6615ff019b37058638d16eb27ce7783`),
  renderizou 10/10 fences. SVG e PNG foram inspecionados visualmente; todos estavam
  legíveis e sem erro de renderização. Os arquivos estão em `mermaid/` e os hashes
  dos SVGs em `sha256.txt`.

## Manifesto de versões candidato — requer aprovação

Estas versões foram resolvidas em 2026-11-26 e são apenas candidatas para W0; W1 é
quem materializa lockfile e imagens.

| Dependência | Candidato | SHA-256 wheel linux/amd64 | SHA-256 wheel linux/arm64 |
| --- | --- | --- | --- |
| Python image | `3.12.16-slim-bookworm` | manifest `1475c4f5b6bcb7d35e57661d6f5d7429ec4041275633c15f2b49350ac898276d` | manifest `209c477b2d5268b578d813ae5a4668682b55252a5b32ad1148dd49e937119101` |
| Django LTS | `5.2.19` | `5965d974a5218a2b68a11dd1276434707f23886525c23f0598eccedaf4f4ca00` | igual (wheel universal) |
| psycopg | `3.3.9` | `d2d7d04a1ce6dab4f5b27316bea3b52585cafa2f2d631e5b09dd69823f5c26f6` | igual (wheel universal; modo binary ainda deve ser decidido) |
| Gunicorn | `27.0.1` | `378b26b9a38adcf4592f28828233c1716acc55e833ea06bf48719782efaa0d10` | igual (wheel universal) |
| Ruff | `0.17.6` | `aa3b08254a732acba246891089a152c47c5733dc36b8ecb76ce8602f8326e5e4` | `435241c61af5909a022f76219d3d1bf24730dc1bf0acabb5ddf4b569ab3cbb30` |
| Playwright Python | `1.65.2` | `58932d35f56767ab7ebcdd3d4a733bfb3e62a1a5bc43c08e28b9fa9b3e61cf33` | `dd3e54b6a926fc6510f272797eec0707dc34ae04d564e74a7056c4a813e53270` |
| OpenAPI validator | `0.7.2` | `4bbdc0894ec85f1d1bea1d6d9c8b2c3c8d7ccaa13577ef40da9c006c9fd0eb60` | igual (wheel universal) |
| PostgreSQL image | `17.12-bookworm` | manifest `c7a16500f728a9c09731e772f228ee7a29615585e8019772f05b620522f62d03` | manifest `f3f92abad8b8105cb7e2bb5d76433640025be3221ce9758ba0ebcf0e115a73a9` |

Índices multi-arch candidatos:

- Python: `sha256:44cf1793efa7c7a476bb0f2cff81443f4a072c90c1cb127e2924933daa3e8c64`.
- PostgreSQL: `sha256:1eff563f6c868b9b433566e9f3cf6e5c79fbd3b95bf70ec7277d376cdbfc50d7`.
- Playwright image `v1.65.2-noble`:
  `sha256:38dd67fc654b56b3cba611e4c8eb71cd33750e1cd29eea2a5dc00b484817a75f`.

Ainda falta decidir a forma de empacotamento psycopg, resolver todas as dependências
transitivas com hashes e executar o smoke arm64 real; portanto este quadro não é um
lockfile aprovado.

## Bloqueios consolidados

1. O brief normativo original não está no repositório. Produto precisa fornecê-lo ou
   confirmar explicitamente PRD/OpenAPI/matriz/contratos como fonte autorizada.
2. A trava normativa diverge de PRD/traceability. Resolver por amendment e revisão
   humana; não regenerar automaticamente.
3. Permanecem decisões de produto/arquitetura: normalização e-mail, cap de body,
   limites numéricos, ownership/ports, DDL/DML, pins e ADRs ainda `proposed`.
4. Há conflitos de contrato a resolver: dependência F01→F06 para normalização,
   guards F02/F03, nomes de catálogo, ports compartilhados incompletos, detalhes
   OpenAPI e ownership do shell.
5. A evidência W0 histórica cita `30cc99ab...`, objeto ausente neste grafo Git; não
   pode provar o SHA atual.
6. Falta aprovação humana explícita do pacote e do manifesto. Sem isso, não registrar
   `baselineCommit`, não avançar `currentWave` e não iniciar F01.

## Próxima ação autorizada

Submeter este diagnóstico e as decisões consolidadas a produto/arquitetura. Após
amendment revisado e aprovação explícita, reproduzir todo G0 no novo SHA limpo,
commitá-lo como baseline aprovada e atualizar o estado em commit separado.
