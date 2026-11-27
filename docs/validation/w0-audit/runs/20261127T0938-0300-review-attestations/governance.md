Authored by session: /root/w0_amend_governance

# Atestação de revisão independente W0

## 1. Identidade e papel

- Identidade canônica observável da sessão: `/root/w0_amend_governance`.
- Papel exercido: revisão independente de governança, harness documental e processo de ratificação W0.
- Coordenador remetente: sessão canônica `/root`.
- Natureza da atuação: estritamente somente leitura; não editei arquivos, não alterei Git, não gerei commit e não simulei aprovação humana.
- Não consigo confirmar um UUID interno adicional da sessão, identidade de modelo, configuração de serviço ou mecanismo criptográfico de isolamento. Não os invento.

## 2. Contexto recebido e isolamento

Esta foi uma sessão de agente separada da sessão do coordenador, identificada pelo caminho canônico acima. Recebi:

- As instruções do repositório e o `AGENTS.md` fornecido pelo usuário.
- O pedido inicial para revisar governança/harness W0.
- O SHA inicial `afe39c1b410c9a00aea601cf2c3b434def8c457a`.
- Posteriormente, pedidos específicos para avaliar:
  - o candidato `93b5b1c52d9efc33c74fe4e163c37e81d877fbf4`;
  - o delta final e tree `eff1b20cb50ae73313e8245d11a6a068fbda9bd5`.
- A informação de que a evidência ainda não rastreada seria commitada aditivamente após o parecer.

A sessão foi separada operacionalmente da coordenação, mas não posso atestar que tenha sido criada com um mecanismo de “fresh context” sem histórico herdado. Recebi contexto de conversa, instruções e mensagens do coordenador. Portanto, não afirmo isolamento integral conforme o padrão mais forte exigido para futuros avaliadores de feature.

Não recebi nem examinei código de produto implementado, pois o pacote permanece pré-implementação. Também não recebi uma aprovação humana antecipada.

## 3. Ambiente observado

- Diretório de trabalho:
  `D:\Docs\Workspace\mba-ia-workspace\desafios\catraca-greenfield`
- Worktree observado: worktree principal compartilhado; não usei worktree independente.
- Branch observada: `main`.
- Primeiro candidato observado:
  `93b5b1c52d9efc33c74fe4e163c37e81d877fbf4`.
- Candidato final observado:
  `eff1b20cb50ae73313e8245d11a6a068fbda9bd5`.
- Ambos os candidatos tinham como pai observado:
  `afe39c1b410c9a00aea601cf2c3b434def8c457a`.
- Assim, `eff1b20…` é uma reescrita/substituição do candidato anterior, não seu descendente. O delta foi comparado diretamente entre os dois trees.
- Em ambos os momentos, o worktree continha o diretório não rastreado:
  `docs/validation/w0-audit/runs/20261127T0245-0300-amendment/`.
- Não atribuo a criação desse diretório a esta sessão. Ele já estava presente quando observei os candidatos.
- Os arquivos rastreados não apresentavam diff local durante as verificações.

## 4. Skills e referências consultadas

Li integralmente:

- `AGENTS.md`
- `.agents/skills/harness-engineering/SKILL.md`
- `.agents/skills/independent-evaluation/SKILL.md`
- `.agents/skills/release-validation/SKILL.md`

Também consultei, entre outros:

- `proposal.md`
- `design.md`
- `docs/prd/PRD.md`
- `requirements-matrix.md`
- `tasks.md`
- `state/project-state.json`
- `docs/validation/normative-lock.json`
- `docs/validation/baseline-validation.md`
- `docs/validation/evaluator-flow.md`
- `docs/validation/harness.md`
- `docs/validation/release-contract.md`
- `docs/validation/test-catalog.md`
- `docs/validation/traceability.json`
- Todos os registros textuais, scripts e manifestos sob `docs/validation/w0-audit/`
- `scripts/validate_docs.py`
- `scripts/test_baseline.py`
- `scripts/validate_evidence.py`
- `docs/validation/w0-audit/reproduce_mutations.py`
- `docs/validation/w0-audit/AMENDMENT-001.md`
- `docs/validation/w0-audit/APPROVAL-CHECKLIST.md`
- `docs/architecture/version-manifest.md`
- Interfaces e contratos afetados pelo amendment, principalmente:
  - `docs/interfaces/internal.md`
  - `docs/interfaces/partner.openapi.json`
  - contratos/specs/plans de F01, F04, F06 e F07.

Os PNGs e SVGs foram inventariados, mas não realizei uma inspeção visual independente completa de todos eles. Não assumo como minha a inspeção visual registrada pelo coordenador.

## 5. Comandos realmente executados

Os comandos foram executados em PowerShell e usados somente para leitura ou validação. Para execuções Python, configurei `PYTHONDONTWRITEBYTECODE=1`.

### Inventário e Git

Executei variações dos seguintes comandos:

```powershell
git status --short
git rev-parse HEAD
git log --oneline --decorate
git log --format=...
git show --stat --oneline <sha>
git show --name-status <sha>
git show -s --format=... <sha>
git diff --name-status <sha1>..<sha2>
git diff --stat <sha1>..<sha2>
git diff --check <sha1>..<sha2>
git diff --word-diff=plain <sha1>..<sha2> -- <arquivos>
git log --all --diff-filter=D --name-status -- docs/validation/w0-audit
rg --files ...
rg -n ...
Get-Content -Raw ...
Get-FileHash -Algorithm SHA256 ...
```

Resultados relevantes:

- `93b5b1…` e depois `eff1b20…` foram confirmados como HEAD nos respectivos momentos.
- Não havia alteração local em arquivos rastreados.
- O run de evidência permanecia não rastreado.
- Não encontrei deleção de relatórios históricos.
- O delta final passou `git diff --check`.
- `state/project-state.json` permaneceu:
  - `baseline=proposed`;
  - `baselineCommit=null`;
  - `currentWave=0`;
  - `releaseStatus=planned`;
  - F01–F07 `planned`.
- `normative-lock.json` permaneceu inalterado e com os hashes anteriores, preservando comportamento fail-closed antes da ratificação.

### Validações executadas diretamente no candidato `93b5b1…`

Executei:

```powershell
python scripts/validate_docs.py
python scripts/verify_model.py
python scripts/validate_evidence.py
```

Resultados:

- `validate_docs.py`: exit 1, exclusivamente pelos drifts de PRD, OpenAPI e traceability contra o lock antigo.
- `verify_model.py`: exit 0, com 4.290 estados, 36.558 transições e mutante artificial de oversell rejeitado.
- `validate_evidence.py`: exit 1, propagando os mesmos três drifts normativos.

Não executei diretamente, nesse SHA, todo o G0 relatado no diretório não rastreado. Li o relatório e o log produzidos por outra sessão, mas distingui essa evidência das minhas próprias execuções.

### Validações no candidato final `eff1b20…`

No tree final, executei verificações de:

- SHA e branch;
- status do worktree;
- delta completo `93b5b1… → eff1b20…`;
- `git diff --check`;
- conteúdo final do amendment, manifesto e checklist;
- consistência textual de UUID, código, cap de body e wiring;
- hashes SHA-256 dos três artefatos primários;
- preservação de lock, state e registros históricos.

Hashes observados e compatíveis com `AMENDMENT-001.md`:

```text
docs/prd/PRD.md
5f2764b10fab3da8027d1d423aa1b9abba270bf96812b86a16bb4c89ee0d9fec

docs/interfaces/partner.openapi.json
141992b6ba262e96b55bdba8dc7bb541110b6a7174a7b448a9a6d778720e0a00

docs/validation/traceability.json
42a0c0233a29f29fccaee5a793c70c035c5bb1fb86ddfbc3a7b5c4eabe50d7ad
```

Não executei o G0 integral diretamente em `eff1b20…`. Isso permanece obrigação do processo após a atualização explícita do lock. Também não executei testes de produto, browser, concorrência ou release.

## 6. Achados que bloquearam `93b5b1…`

O primeiro parecer foi **BLOCK para ratificação** pelos seguintes motivos:

1. A evidência nova estava fora do Git, sem proveniência e imutabilidade commitadas.
2. O lock antigo fazia `validate_docs.py` e `validate_evidence.py` falharem pelos três artefatos primários.
3. O G0 verde descrito havia ocorrido somente numa cópia efêmera com hashes candidatos, e não no SHA limpo ratificado.
4. Faltava aprovação humana explícita de produto e arquitetura.
5. Amendment, manifesto, PRD, design e ADRs continuavam corretamente como candidatos/propostos.
6. O texto inicial tratava um conjunto amplo de documentos como fonte normativa sem distinguir claramente o que seria primário e byte-locked do que seria derivado.
7. O manifesto apontava como proveniência principal um run histórico realizado em outro SHA, fora da ancestralidade do squash atual.
8. O checklist ainda apresentava o procedimento de ZIP/bundle histórico sem distingui-lo claramente do repositório vivo.
9. A evidência não rastreada ainda não satisfazia, como artefato imutável, todos os requisitos de proveniência, hashes e registro ambiental.
10. As revisões frescas anteriores documentadas no amendment não haviam produzido análise válida naquele momento.

Também registrei que nenhum desses bloqueios autorizava marcar o estado como aprovado ou iniciar W1.

## 7. Verificação das correções em `eff1b20…`

Revisei diretamente o delta entre os dois trees.

### Autoridade primária e derivada

O amendment final passou a declarar:

- PRD, OpenAPI e traceability como três fontes primárias protegidas por hash;
- matriz, contracts, test catalog, HLD/ADRs e interfaces como refinamentos normativos derivados;
- proibição de alteração desses derivados sem amendment e revisão, mesmo não sendo byte-locked;
- preservação de R01–R13, das três rotas e dos critérios A/X/P.

Considerei essa separação clara e compatível com o escopo atual do lock.

### Proveniência

O manifesto final deixou de atribuir o SHA atual ao run histórico de 2026-11-26 e passou a declarar explicitamente:

- o run de `20261127T0245-0300-amendment` como local esperado para a evidência do candidato;
- o run de `20261126T2114-0300` como histórico, incapaz de provar o SHA atual.

Os manifests de Playwright e Mermaid também passaram a distinguir digests por arquitetura.

Entretanto, o conteúdo não rastreado do run ainda registrava:

```text
tested_commit=93b5b1c52d9efc33c74fe4e163c37e81d877fbf4
```

Por isso, determinei que ele deveria ser regenerado para `eff1b20…` antes de ser commitado ou apresentado como evidência desse SHA.

### Checklist legado

O título foi alterado para “Legado: retomada do pacote de auditoria importado”, declarando que:

- ZIP/bundle descrevem apenas o pacote histórico;
- não são o procedimento do repositório vivo;
- o estado atual deve ser auditado por clone completo e SHA candidato.

Considerei corrigida a ambiguidade.

### Lock, estado e histórico

Confirmei:

- `normative-lock.json` preservado, sem regeneração prematura;
- `state/project-state.json` preservado em `proposed/null/wave0`;
- nenhuma feature avançada;
- nenhum relatório histórico removido;
- somente `AMENDMENT-001.md` foi adicionado e o checklist foi atualizado dentro da área histórica de auditoria;
- os relatórios antigos continuaram imutáveis.

### Correções contratuais adicionais

O delta final tornou explícitos e rastreados:

- UUIDs e código `[A-Z0-9]{12}`;
- tratamento de UUID malformado;
- body autenticado com limite inclusivo de 16.384 bytes e rejeição a partir de 16.385;
- ausência de `maxLength: 254` incorreto no valor bruto do e-mail antes de strip/casefold;
- manifests por arquitetura;
- ownership e wiring settings-driven entre F01, F03, F07 e coordenação.

Não identifiquei redução de R01–R13, rotas fixas ou critérios A/X/P nesse delta.

## 8. Veredito final

Veredito sobre `eff1b20cb50ae73313e8245d11a6a068fbda9bd5`:

**PASS para apresentar o pacote documental à aprovação humana.**

Esse PASS possui escopo restrito:

- confirma que os bloqueios documentais revisados no primeiro candidato foram adequadamente tratados no delta final;
- não é aprovação humana;
- não é ratificação da baseline;
- não é PASS de G0 pós-lock;
- não é avaliação de feature;
- não é release;
- não autoriza W1.

Condição operacional obrigatória antes de anexar ou commitar a evidência:

- regenerar o run para o tree `eff1b20…`;
- registrar o SHA correto;
- não reutilizar outputs de `93b5b1…` como prova de `eff1b20…`;
- commitar a evidência de forma aditiva.

Após aprovação humana, ainda são necessários:

1. commit explícito de ratificação do `normative-lock.json`;
2. G0 integral no SHA limpo ratificado;
3. evidência aditiva e imutável desse G0;
4. commit separado de estado apontando `baselineCommit` para o SHA aprovado;
5. manutenção de todas as features como `planned` até o despacho formal de F01.

## 9. Limites da atestação

Não consigo confirmar:

- que a aprovação humana ocorreu;
- que produto e arquitetura aceitaram o pacote;
- que a evidência não rastreada será efetivamente regenerada;
- que os digests externos foram verificados por mim diretamente nos registries;
- que todos os SVGs/PNGs foram visualmente inspecionados por esta sessão;
- que houve duas sessões completamente isoladas conforme o padrão forte do checklist;
- que o G0 integral passou em `eff1b20…`;
- qualquer comportamento de produto, pois não há implementação;
- compatibilidade real de runtime, concorrência, browser, Linux/macOS/arm64 ou release.

Esses itens não foram inferidos nem declarados como PASS.

## 10. Handoff ao coordenador

O handoff foi feito por mensagens diretas à sessão canônica `/root`, contendo:

- o BLOCK inicial para ratificação de `93b5b1…`;
- os bloqueadores por severidade e a sequência segura de correção;
- o PASS restrito do tree `eff1b20…` para apresentação humana;
- a ressalva de que a evidência ainda apontava para `93b5b1…`;
- a proibição explícita de iniciar W1 antes de aprovação, lock, G0 e state separados.

Esta atestação completa é devolvida no chat ao coordenador para registro aditivo. Nenhum arquivo foi criado ou alterado por esta sessão.
