# W0 | revisão independente de arquitetura e governança

**Veredito: PASS** — arquitetura e evidência documental da ratificação, no escopo desta revisão. Este parecer isolado não comprova a segunda sessão exigida pelo checklist e não autoriza, sozinho, a transição de estado ou o despacho de F01.

## Identidade, contexto e isolamento

- Sessão canônica: `/root/w0_fresh_architecture`; coordenador: `/root`.
- Recebi briefing específico de avaliação independente, sem transcrição do coordenador; contexto novo conforme o despacho. Não disponho de metadados internos para provar criptograficamente a configuração de fork.
- Checkout exclusivo de revisão, CWD `C:\Users\eduar\AppData\Local\Temp\catraca-w0-architecture-32410078`, detached HEAD `b8db254568d6d359ae8261245814c365c97dbea6`; `git symbolic-ref -q HEAD` exit 1, `git status --porcelain=v1` vazio antes e depois dos gates. Nenhuma alteração no checkout ou index.
- Este relatório é escrito somente no repositório principal, após a avaliação; handoff ao coordenador por mensagem de conclusão com caminho e SHA-256.

## Fontes e acessos

Consultei `AGENTS.md`, `tasks.md`, as skills locais `independent-evaluation`, `architecture-review`, `schema-review` e `transaction-safety`, `proposal.md`, `design.md`, `docs/prd/PRD.md`, `requirements-matrix.md`, `state/project-state.json`, `docs/interfaces/internal.md`, `docs/architecture/{version-manifest,transactions,diagrams,research,security}.md`, ADR-001 a ADR-009 e README, `docs/validation/normative-lock.json`, `docs/validation/w0-audit/{AMENDMENT-001,APPROVAL-CHECKLIST,CORRECTIONS}.md`, registros textuais dos runs 0245, 0931 e 0938 e seus manifestos de hashes, além de histórico e diff Git. Artefatos Mermaid binários foram inventariados, não inspecionados visualmente nesta sessão; a inspeção registrada no run 0931 é evidência anterior, não observação própria.

## Evidência observada

- `git merge-base --is-ancestor` para `eff1b20 → 1905960 → 0af4039 → b8db254`: três exits 0. `git show 1905960` confirma commit explícito de ratificação: atualização da trava, registro de aprovação, proposal/design/manifesto aprovados e ADR-001–009 `accepted`. O diff posterior inclui os registros aditivos de G0 e atestações; o estado segue `baseline=proposed`, `baselineCommit=null`, `currentWave=0`, release e F01–F07 planejados.
- `Get-FileHash -Algorithm SHA256` confere com a trava e amendment: PRD `5f2764b10fab3da8027d1d423aa1b9abba270bf96812b86a16bb4c89ee0d9fec`; OpenAPI `141992b6ba262e96b55bdba8dc7bb541110b6a7174a7b448a9a6d778720e0a00`; traceability `42a0c0233a29f29fccaee5a793c70c035c5bb1fb86ddfbc3a7b5c4eabe50d7ad`. Os quatro hashes das atestações 0938 conferem com seu README.
- Manifesto especifica pins e digests por arquitetura; run 0931 registra smoke amd64 de Python, PostgreSQL, Playwright e Mermaid, validação OpenAPI e render de 10 fontes Mermaid. W1 ainda deve materializar lockfile transitivo e imagens e repetir smoke; não refiz a consulta de registries ou renderização nesta sessão.
- O amendment e o run 0931 registram aprovação explícita do proprietário; esta sessão teve acesso ao registro no checkout, não à mensagem original ou prova independente de sua autenticidade.
- Atestações 0938 reconhecem que os quatro revisores anteriores compartilharam worktree e não puderam provar fork vazio. Não os conto como prova conclusiva do item 6. Esta sessão é uma das duas sessões novas solicitadas; a outra e seu handoff precisam ser verificados pelo coordenador antes do commit separado de estado.

## Gates executados neste checkout

Python host 3.12.10; comandos abaixo executados novamente no SHA indicado:

| Comando | Exit | Resultado |
| --- | --- | --- |
| `python scripts/validate_docs.py` | 0 | 7 features, 37 critérios locais, 16 cruzados, 6 de processo |
| `python scripts/verify_model.py` | 0 | 4.290 estados, 36.558 transições; negativo oversell rejeitado |
| `python scripts/test_baseline.py` | 0 | negativos da baseline detectados |
| `python scripts/validate_evidence.py` | 0 | estrutura e histórico para fase; sem inferir autenticidade/PR |
| `python scripts/validate_evidence.py --release` | 1 | somente F01–F07 incompletas, evidências de merge/PR ausentes e estado de release incompleto |
| `python docs/validation/w0-audit/reproduce_mutations.py` | 0 | 0/7 mutantes inválidos aceitos |
| `git diff --check` | 0 | sem erros no worktree |

Uma tentativa inicial de `Get-FileHash` com expansão de chaves no PowerShell resultou em erro de parser; foi repetida com `Get-ChildItem` e os quatro hashes conferidos.

## Julgamento arquitetural e limites

O HLD usa domínio compartilhado e ledger único entre canais. O protocolo documenta lock Event → Ticket → PaymentJob, contagem em nova instrução após aquisição, reserva e job no mesmo commit, preço histórico, estados terminais e projeções em snapshot único. `create_event` é exceção justificada por inexistência de linha; FK única garante no máximo um job e a totalidade depende de `reserve`. A prova de capacidade é condicional a todos os escritores seguirem o protocolo; não prova SQL arbitrário, liveness, deadlines ou implementação. Constraints, migrations, corridas reais, timings, segurança, browser e integração ainda exigem os testes do produto previstos; o modelo abstrato não os substitui.

O G0 documental e seus limites estão coerentes com os resultados frescos e registros existentes. Não identifiquei bloqueio arquitetural para o commit separado de estado **após** confirmação independente da segunda sessão nova e dos demais pareceres necessários. O registro 0931 indica `baselineCommit=19059603b450981630477dac3732acfdc8fe9d1d`; o coordenador deve preservar F01–F07 planned e verificar todas as condições do checklist antes de qualquer transição. Este relatório não declara PASS integrado ou release.
