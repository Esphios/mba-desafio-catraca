# W0 | revisão independente de produto e rastreabilidade

- Sessão canônica: `/root/w0_fresh_product`; papel: avaliação independente de produto, não implementador nem aprovador humano.
- Data: 2026-11-27, aproximadamente 12:46 UTC. Ferramenta: Codex; modelo e identificador opaco de infraestrutura não disponíveis a esta sessão.
- Contexto: sessão delegada nova, conforme briefing recebido, sem transcrição do coordenador; baseei o parecer no briefing e no checkout. Não possuo evidência interna que prove criptograficamente o modo exato de fork ou a ausência de contexto herdado.
- Worktree e cwd de revisão: `C:\Users\eduar\AppData\Local\Temp\catraca-w0-product-32410078`; HEAD detached `b8db254568d6d359ae8261245814c365c97dbea6`; `git symbolic-ref -q HEAD` exit 1; `git status --porcelain=v1` vazio antes e depois dos comandos. A revisão não editou esse worktree.

## Acessos

Lidos: `AGENTS.md`, `tasks.md`, `.agents/skills/independent-evaluation/SKILL.md`, `.agents/skills/prd-design/SKILL.md`, `proposal.md`, `design.md`, `docs/prd/PRD.md`, `requirements-matrix.md`, `state/project-state.json`, `docs/validation/w0-audit/AMENDMENT-001.md`, `APPROVAL-CHECKLIST.md`, `runs/20261127T0245-0300-amendment/REPORT.md`, `runs/20261127T0931-0300-ratification-g0/REPORT.md` e `commands.log`, todos os arquivos de `runs/20261127T0938-0300-review-attestations/`, `docs/validation/normative-lock.json`, `docs/validation/traceability.json`, `docs/interfaces/partner.openapi.json` e `docs/architecture/version-manifest.md`. Os caminhos abreviados de runs e checklist são relativos a `docs/validation/w0-audit/`.

## Execução própria

Python 3.12.10 no worktree acima:

| Comando | Exit | Resultado observado |
| --- | --- | --- |
| `python scripts/validate_docs.py` | 0 | 7 features, 37 critérios locais, 16 cross e 6 de processo |
| `python scripts/verify_model.py` | 0 | 4.290 estados, 36.558 transições; negativo de oversell rejeitado |
| `python scripts/test_baseline.py` | 0 | testes negativos da baseline detectados |
| `python scripts/validate_evidence.py` | 0 | estrutura/histórico válidos para a fase |
| `python scripts/validate_evidence.py --release` | 1 | F01–F07 incompletas, sem evidência de merge/PR; estado de release incompleto, sem outras falhas relatadas |
| `python docs/validation/w0-audit/reproduce_mutations.py` | 0 | 7/7 mutações inválidas detectadas |

Busca adicional com `rg` terminou exit 1 por glob Windows inválido; seus resultados parciais não são prova de cobertura. `git merge-base --is-ancestor 19059603b450981630477dac3732acfdc8fe9d1d HEAD` retornou 0; o diff subsequente compreende checklist e evidências de revisão/G0, sem alteração das três fontes primárias.

`Get-FileHash -Algorithm SHA256`, comparado com amendment e lock:

- PRD: `5f2764b10fab3da8027d1d423aa1b9abba270bf96812b86a16bb4c89ee0d9fec`.
- OpenAPI: `141992b6ba262e96b55bdba8dc7bb541110b6a7174a7b448a9a6d778720e0a00`.
- Traceability: `42a0c0233a29f29fccaee5a793c70c035c5bb1fb86ddfbc3a7b5c4eabe50d7ad`.

## Achados e decisão

R01–R13 constam do PRD e estão associados a critérios/testes na matriz; o gate confirma sua cobertura estrutural e as 16 relações cross-feature. O escopo preserva canal único de ledger, ocupação pending+confirmed, preço histórico, cancelamento terminal, autorização por dono e painel coerente. Os critérios X14–X16 exigem integração, não presumem comportamento de siblings na avaliação local.

O OpenAPI contém as três rotas previstas; prevê UUID, código de 12 caracteres, estados, chave antes da leitura do body, limite inclusivo de 16.384 bytes e precedência de erros. A21–A24/A34 e X09/X10/X15/X16 conectam esses pontos a testes. A coerência inspecionada é documental; não validei uma implementação.

O amendment registra que o brief original é irrecuperável e que o proprietário aprovou explicitamente `Aprovo o AMENDMENT-001` em 2026-11-27. Trata-se de registro no repositório, não de verificação independente da mensagem original. A fidelidade histórica ao brief indisponível não pode ser comprovada; o parecer usa as fontes ratificadas como autoridade declarada. O cabeçalho do PRD ainda diz “proposta, aguardando aprovação W0”, embora amendment/checklist registrem ratificação: ressalva editorial no artefato protegido, a resolver somente mediante processo normativo, sem alterar a trava para fazer gate passar.

O G0 registrado foi executado no commit de ratificação `19059603b450981630477dac3732acfdc8fe9d1d`, ancestral do checkout. Seu relatório registra OpenAPI formal, Mermaid e ambiente; não repeti essas verificações nesta sessão. As atestações anteriores declaram limite de isolamento e o checklist exige duas sessões novas separadas. Esta sessão constitui um parecer de produto; não comprova por si só a segunda sessão independente nem aprovação de arquitetura ou todos os pré-requisitos do coordenador.

O dossiê e as verificações observadas sustentam o commit separado de estado do ponto de vista de produto, condicionado à conclusão satisfatória da outra sessão independente e à revisão integral do G0 pelo coordenador. O estado atual permanece `proposed`, baselineCommit nulo, wave 0 e F01–F07 planned. Não autoriza despacho F01 antes do commit de estado e das condições restantes. Nenhum teste de runtime, concorrência, browser ou release foi executado; o modelo abstrato não prova banco real.

## Handoff

Coordenador: conferir a segunda avaliação e o dossiê completo; se aprovados, registrar em commit separado `baselineCommit=19059603b450981630477dac3732acfdc8fe9d1d`, `baseline=approved`, `currentWave=1`, mantendo features planned. Preserve os registros históricos e trate a ressalva de status do PRD pelo procedimento normativo aplicável. Esta sessão não alterou index, estado nem commits.

Veredito único: **PASS** — escopo de produto e rastreabilidade W0, sujeito às condições expressas para a transição de estado.
