Authored by session: /root/w0_amend_product

# Atestação de revisão independente W0

## 1. Identidade e papel

- Identidade canônica disponível: `/root/w0_amend_product`.
- Papel: revisor independente de produto e rastreabilidade, somente leitura.
- Escopo: candidato inicial `93b5b1c52d9efc33c74fe4e163c37e81d877fbf4` e delta final `eff1b20cb50ae73313e8245d11a6a068fbda9bd5`.
- Não atuei como implementador, coordenador, aprovador humano ou avaliador de feature.
- Não editei arquivos, não atualizei estado, não alterei a trava normativa e não fiz commits.

Não tenho acesso a um identificador opaco adicional da sessão, nem consigo confirmar pelo runtime o nome exato do modelo, configuração de sampling, horário de criação ou identidade de infraestrutura. Não invento esses metadados.

## 2. Contexto e isolamento

Fui executado em um contexto delegado separado, identificado pelo caminho canônico acima. Recebi:

- as instruções do `AGENTS.md` fornecidas na conversa;
- a solicitação do coordenador para revisão independente e somente leitura;
- os SHAs candidatos;
- a exigência de usar a skill `prd-design`;
- os pedidos posteriores para revisar o delta corrigido e produzir esta atestação.

Li integralmente o `AGENTS.md` do repositório e `.agents/skills/prd-design/SKILL.md`.

Não recebi uma transcrição de implementação nem evidência de execução de produto. Não consigo provar criptograficamente que o contexto era “fresh” ou que nenhuma informação foi herdada pelo mecanismo de delegação. Posso afirmar apenas que atuei como subagente separado, não participei da edição e baseei o parecer nos arquivos e comandos observados diretamente.

## 3. Ambiente observado

- CWD/worktree: `D:\Docs\Workspace\mba-ia-workspace\desafios\catraca-greenfield`
- Branch observada: `main`
- Primeiro candidato observado: `93b5b1c52d9efc33c74fe4e163c37e81d877fbf4`
- Candidato final observado: `eff1b20cb50ae73313e8245d11a6a068fbda9bd5`
- Nos dois momentos, os arquivos rastreados estavam iguais ao respectivo `HEAD`.
- Havia um diretório não rastreado:
  `docs/validation/w0-audit/runs/20261127T0245-0300-amendment/`
- Não usei esse diretório não rastreado como parte normativa do candidato.

O candidato final é um commit refeito diretamente sobre `afe39c1b410c9a00aea601cf2c3b434def8c457a`; portanto, a revisão do delta `93b5b1c..eff1b20` comparou dois candidatos irmãos, não uma relação de ancestralidade entre eles.

## 4. Arquivos principais acessados

Entre os arquivos lidos ou comparados:

- `AGENTS.md`
- `.agents/skills/prd-design/SKILL.md`
- `proposal.md`
- `design.md`
- `docs/prd/PRD.md`
- `requirements-matrix.md`
- `requirements-matrix.csv`
- `docs/validation/traceability.json`
- `docs/validation/test-catalog.md`
- `docs/validation/normative-lock.json`
- `docs/validation/w0-audit/AMENDMENT-001.md`
- `docs/validation/w0-audit/APPROVAL-CHECKLIST.md`
- `docs/validation/w0-audit/CORRECTIONS.md`
- `tasks.md`
- `state/project-state.json`
- `docs/interfaces/internal.md`
- `docs/interfaces/partner.openapi.json`
- specs, plans e contratos relevantes de F01, F04 e F06
- documentação de arquitetura e transações afetada pelo amendment.

## 5. Comandos e verificações realmente executados

Executei, em PowerShell, comandos de leitura e comparação equivalentes a:

- `git rev-parse HEAD`
- `git status --short`
- `git show -s --format=... <sha>`
- `git show --stat <sha>`
- `git diff --stat 93b5b1c..eff1b20`
- `git diff --unified=...` sobre os artefatos normativos e contratos alterados
- `git diff --quiet HEAD --`
- `Get-Content -Raw` nos arquivos listados
- `Get-FileHash ... -Algorithm SHA256`
- `rg` para localizar requisitos, formatos, limites, critérios e testes
- `ConvertFrom-Json` sobre `traceability.json`
- `Import-Csv` sobre `requirements-matrix.csv`
- comparações programáticas entre traceability, matriz CSV e catálogo.

Também executei:

```text
python scripts/validate_docs.py
python scripts/test_validate_docs_parser.py
python scripts/verify_model.py
```

Resultados no candidato final:

- `validate_docs.py`: falhou somente pelos três drifts esperados da trava normativa antiga:
  - `docs/prd/PRD.md`
  - `docs/interfaces/partner.openapi.json`
  - `docs/validation/traceability.json`
- `test_validate_docs_parser.py`: 2 testes executados, todos passaram.
- `verify_model.py`: PASS, com 4.290 estados e 36.558 transições; mutante de oversell rejeitado.
- A comparação própria encontrou 59 itens de rastreabilidade, 123 linhas de matriz e nenhum ID de teste ausente ou extra.
- As 16 arestas cross-feature permaneceram alinhadas com o DAG.
- R01–R13 e a regra API continuaram cobertas.
- Os hashes do candidato final conferiram exatamente com os hashes informativos do `AMENDMENT-001`:
  - PRD: `5f2764b10fab3da8027d1d423aa1b9abba270bf96812b86a16bb4c89ee0d9fec`
  - OpenAPI: `141992b6ba262e96b55bdba8dc7bb541110b6a7174a7b448a9a6d778720e0a00`
  - traceability: `42a0c0233a29f29fccaee5a793c70c035c5bb1fb86ddfbc3a7b5c4eabe50d7ad`

## 6. Achados que bloquearam `93b5b1c`

Meu primeiro veredito foi `BLOCK` para ratificação por três motivos:

1. UUID e código de ingresso haviam se tornado decisões normativas, mas os testes não provavam suficientemente:

   - IDs UUID;
   - código exatamente `[A-Z0-9]{12}`;
   - rejeição de códigos curtos, longos, minúsculos ou não alfanuméricos;
   - tratamento de UUID malformado.

2. O limite de body de 16 KiB não tinha um oráculo inequívoco de borda:

   - não estava explicitamente provado que 16.384 bytes seriam aceitos pelo limitador;
   - não estava explicitamente provado que 16.385 bytes seriam rejeitados.

3. O OpenAPI aplicava `maxLength: 254` ao e-mail bruto, enquanto a decisão normativa limitava o e-mail canônico após `strip` e Unicode `casefold`. Isso criava ambiguidade contratual.

Não encontrei redução de R01–R13, das três rotas fixas, dos status HTTP ou da precedência de erros.

## 7. Verificação das correções em `eff1b20`

Confirmei no delta que as correções foram propagadas coordenadamente.

### UUID e código

- A05 passou a exigir schema com código `[A-Z0-9]{12}`.
- TEST-A05 e contrato F01 passaram a testar código duplicado, curto, longo, minúsculo e não alfanumérico.
- A13 passou a exigir ID UUID e código válido.
- TEST-A13 e contrato F04 passaram a validar UUID e `^[A-Z0-9]{12}$`.
- A21 passou a validar itens da listagem contra o OpenAPI, incluindo UUID, timestamp e limites numéricos.
- A23 passou a validar IDs UUID, código exato e UUID malformado → 404.
- PRD, traceability, matrizes Markdown/CSV, catálogo, specs, plans e contracts foram atualizados de forma consistente.

### Limite de body

A34 e seus artefatos coordenados passaram a exigir:

- JSON válido com exatamente 16.384 bytes alcançando o domínio;
- corpo de 16.385 bytes retornando `422 invalid_request`;
- registro dos bytes efetivamente lidos;
- preservação da precedência da chave antes da leitura do body.

O OpenAPI passou a documentar explicitamente o limite inclusivo.

### E-mail canônico

- O `maxLength: 254` foi removido do valor bruto no OpenAPI.
- O OpenAPI passou a explicar que o limite de 254 se aplica ao valor após `strip` e Unicode `casefold`.
- A17 continua testando canonicidade, expansão por casefold, inválido e comprimento canônico superior a 254.
- A34 mantém a cobertura HTTP para e-mail canônico inválido.

## 8. Veredito final

**PASS para apresentar o candidato `eff1b20cb50ae73313e8245d11a6a068fbda9bd5` à aprovação humana de produto e arquitetura.**

Esse PASS significa apenas que os bloqueios de produto/rastreabilidade identificados na primeira revisão foram corrigidos de forma coordenada e que não observei perda de R01–R13 ou do contrato fixo da API.

Não significa:

- aprovação humana do amendment;
- baseline aprovada;
- autorização para atualizar `state/project-state.json`;
- autorização para iniciar W1;
- PASS de runtime, concorrência, segurança ou release;
- validação independente de Docker, pins, digests, Mermaid, OpenAPI formal ou plataformas;
- prova de implementação, pois nenhuma aplicação existe neste pacote.

O candidato ainda mantém corretamente o gate documental em fail-closed enquanto `normative-lock.json` aponta para a baseline antiga. Após aprovação humana, ainda é necessário um commit explícito de ratificação da trava, seguido de G0 em SHA limpo. Só depois deve ocorrer o commit separado de estado previsto no procedimento.

## 9. Handoff

O handoff foi feito diretamente ao coordenador `/root` por mensagem no canal de colaboração, contendo:

- SHA observado;
- resultado dos comandos;
- bloqueios do primeiro candidato;
- confirmação das correções no candidato final;
- veredito `PASS` limitado à apresentação para aprovação humana;
- ressalva explícita de que W1 não estava autorizada.

Esta atestação é entregue integralmente no chat para registro aditivo. Nenhum arquivo histórico ou normativo foi criado ou alterado por esta sessão.
