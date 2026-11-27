# W0 | avaliação final independente de governança

**Veredito: PASS para a transição de estado descrita abaixo**, limitado à governança documental W0. Este parecer não é aprovação de feature, integração ou release.

## Identidade, escopo e isolamento

- Avaliador: sessão canônica `/root/w0_final_governance`, delegada pelo coordenador `/root`; ferramenta Codex. Não disponho de identificador interno de infraestrutura ou modelo exato verificável.
- Avaliação em 2026-11-27, America/Sao_Paulo; checkout exclusivo `C:\Users\eduar\AppData\Local\Temp\catraca-w0-final-governance-1194c18`.
- HEAD avaliado: `1194c18c2e8b6864d319c08b66f9fd770a5fb488`, detached (`git symbolic-ref -q HEAD`, exit 1). `git status --short` vazio antes e depois dos gates. Nenhuma edição no checkout avaliado; este relatório é autoral e gravado separadamente no workspace principal.
- Recebi briefing próprio e as instruções de projeto; não disponho de prova interna criptográfica da configuração de fork ou de autenticidade das sessões anteriores. Não fui implementador nem aprovador humano.
- Julgamento solicitado: permitir ao coordenador, em commit de estado separado, definir `baseline=approved`, `baselineCommit=19059603b450981630477dac3732acfdc8fe9d1d`, `currentWave=1`, mantendo F01–F07 `planned`. O estado examinado ainda está `proposed`, commit nulo, wave 0, release planned e todas as features planned.

## Evidência e julgamento

- O commit explícito de ratificação `19059603b450981630477dac3732acfdc8fe9d1d` é ancestral do HEAD (`git merge-base --is-ancestor`, exit 0). O histórico subsequente registra G0 em `0af4039`, atestações em `b8db254` e sessões novas em `1194c18`. O diff posterior à ratificação altera o checklist e acrescenta evidência; não modifica fontes primárias ou estado. `git diff --check 19059603b450981630477dac3732acfdc8fe9d1d HEAD` exit 0.
- Os SHA-256 calculados das fontes correspondem ao amendment e ao lock ratificado: PRD `5f2764b10fab3da8027d1d423aa1b9abba270bf96812b86a16bb4c89ee0d9fec`; OpenAPI `141992b6ba262e96b55bdba8dc7bb541110b6a7174a7b448a9a6d778720e0a00`; traceability `42a0c0233a29f29fccaee5a793c70c035c5bb1fb86ddfbc3a7b5c4eabe50d7ad`. O lock prova correspondência de bytes, não autenticidade ou completude semântica.
- `AMENDMENT-001.md` registra aprovação explícita do proprietário em 2026-11-27 pela mensagem `Aprovo o AMENDMENT-001`, incluindo pacote e manifesto. Examinei o registro versionado, não a mensagem original; não posso autenticar sua origem independentemente. O brief original é declarado irrecuperável; fidelidade a ele não é verificável. As fontes ratificadas são a autoridade registrada para esta revisão.
- O run `20261127T0931-0300-ratification-g0` identifica o SHA de ratificação e registra G0, Python 3.12, Docker/Compose/WSL, smoke das imagens amd64 pinadas, OpenAPI formal e renderização/inspeção Mermaid. O manifesto lista pins e digests por arquitetura; W1 ainda deve materializar dependências transitivas e imagens e repetir smoke. Estas verificações ambientais e visuais são evidência prévia; não foram repetidas por mim.
- As quatro atestações autorais do run 0938 descrevem seus papéis, acesso ao worktree compartilhado e limites do fork; seus hashes conferem com o README. Seus PASS são limitados à apresentação do candidato, sem pretensão de comprovar isolamento forte. O manifesto 0945 registra duas chamadas com `fork_turns=none` e worktrees exclusivos no SHA `b8db254568d6d359ae8261245814c365c97dbea6`. Os pareceres autorais de produto e arquitetura declaram sessão, isolamento observado, gates e handoff, e ambos dão PASS no próprio escopo; cada um reconhece que não consegue provar criptograficamente o fork. Hashes dos pareceres: produto `2b0430d22fc200aaa8de9c1d0ddbd1f3adc01929da3d14d201c352f400566137`, arquitetura `df1a527138843bf44a924b5661df2dc467f8b9a68eaa7d14dbfba9f9eff6b122`. A evidência disponível sustenta as duas sessões exigidas pelo checklist, sujeita aos limites declarados.
- Consultei AGENTS.md, proposal, design, PRD, matriz, tasks, state, amendment, correções, checklist, lock, manifesto de versões, logs e pareceres W0, incluindo runs 0245, 0931, 0938 e 0945; apliquei `.agents/skills/independent-evaluation/SKILL.md`. O PRD ainda ostenta o cabeçalho histórico “proposta, aguardando aprovação W0”; o amendment e o checklist registram ratificação posterior. Corrigir esse texto protegido exige processo normativo próprio, não regeneração casual do lock.

## Reprodução própria

PowerShell, Python 3.12.10, `PYTHONDONTWRITEBYTECODE=1`, no checkout indicado:

| Comando | Exit | Resultado observado |
| --- | ---: | --- |
| `git status --short` | 0 | vazio antes e depois |
| `git rev-parse HEAD` | 0 | `1194c18c2e8b6864d319c08b66f9fd770a5fb488` |
| `python scripts/validate_docs.py` | 0 | 7 features, 37 critérios locais, 16 cross e 6 de processo |
| `python scripts/verify_model.py` | 0 | 4.290 estados, 36.558 transições; negativo oversell rejeitado |
| `python scripts/test_baseline.py` | 0 | testes negativos da baseline detectados |
| `python scripts/validate_evidence.py` | 0 | estrutura e histórico válidos para a fase |
| `python docs/validation/w0-audit/reproduce_mutations.py` | 0 | 0/7 mutantes inválidos aceitos |
| `python scripts/validate_evidence.py --release` | 1 | F01–F07 incompletas, merge/PR ausentes e estado de release incompleto; nenhuma outra falha emitida |

O modelo assume transições serializadas; os gates documentais não provam banco real, concorrência, segurança, browser ou comportamento da aplicação. O validador de evidência não autentica autores nem prova PRs reais. Não existe implementação avaliada neste parecer.

## Handoff

O coordenador pode registrar a transição especificada em commit separado, preservando `releaseStatus=planned` e F01–F07 `planned`; verificar o diff e o gate de evidência na fase adequada após o commit. Só então seguir o procedimento de despacho F01. Preservar relatórios históricos e o lock; qualquer alteração normativa segue amendment e revisão. Este PASS não substitui os gates de implementação, avaliação independente de feature, integração ou release.
