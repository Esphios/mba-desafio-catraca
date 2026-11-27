# AI design | roles, state and evidence protocol

## Roles

Product owner approves W0 and requirement changes. Coordinator owns DAG, shared files, state, worktrees, merges and release. Implementer owns one branch and tests, cannot write evaluation reports. Evaluator uses fresh session/context with exact SHA and contract, does not receive implementer transcript or self-verdict and never fixes code. Integrator resolves conflicts, runs regressions and asks a fresh evaluator for affected contracts. One person may coordinate multiple sessions; independent means distinct context, not necessarily different vendor/model. Do not claim independence if it cannot be demonstrated.

## State machine

`planned → implementing → ready_for_review → local_pass → merged_local → completed`. Failure from review/local_pass/merged_local returns `needs_fix`; new commit and new report, then repeat. Only coordinator writes state; implementer submits handoff. `local_pass` permits merge but not completion while integration items pending. For features with no integrated items, completion after merge and coordinator confirms no regressions. For F06/F07, rerun contract in integrated environment with all items PASS, then complete. A regression reopens affected features, including F05 if X14/X16 fails due to its behavior; release state not complete until main passes.

## Handoff rules

Start consumer only when required provider is merged with local PASS and interface version frozen. Coordinator reads state and applicable PRD sections, sends immutable base SHA and ownership boundaries to one fresh implementer per feature. Reuse that implementer for sequential tasks and fixes while available. Worktrees each have separate compose project/port. Start commits useful and early; record actual GitHub timestamps, do not synthesize overlap. Parallel W5 features consume frozen F01–F04, not each other; their real cross-channel/operation behavior is evaluated in W6.

## Execution checkpoints
- For each task, preserve a material commit on the feature branch and a concise handoff with full SHA, changed paths, test commands/exits and next task. The coordinator independently checks the actual Git repository, commit, ancestry, branch reference and material diff before advancing. Do not require a new agent merely to check Git or run deterministic scripts.
- A missing commit or environment mismatch blocks advancement. Recover existing work first; if the session cannot resume, start a replacement from the last verified checkpoint, preserving actual authorship and session IDs. Do not loop on redispatch or rewrite active history.
- Formal independent evaluation is per feature plus any additional evaluation required by the contract or concrete critical risk. A failed formal evaluation requires a fresh evaluator on the corrected candidate and a new report. Preserve all existing report, evidence and merge rules. Do not record final candidate or approval before the required evidence exists.
- Update global state only for relevant transitions and required session metadata; do not generate commits merely to repeat progress messages.

## Evaluation

Checkout clean exact implementation SHA; record full SHA, actual model/tool, UTC date, session identifier (local pseudonymous ID), phase, base SHA and commands. Local contract items evaluated with actual providers; future sibling items marked PENDING_INTEGRATION, never PASS. Fixture may prove a provider interface but not absent consumer. Each item PASS/FAIL/BLOCKED/PENDING_INTEGRATION (pending only for integrated in local phase). Missing evidence = FAIL or BLOCKED; local verdict pass only all local pass. Integrated verdict requires all items PASS. Evaluate with default simulator for timing and real DB; never accept code inspection as sole proof of runtime. Record raw/redacted command output, HTTP and screenshot path; keep log artifacts with unique names; test result tied to SHA. Report JSON for machine validation and Markdown for human review; same facts and all items. New report per run; commit once, no edits or deletions. `git log -- path` and hash check. Evaluator can write report files only; coordinator commits and updates state. No manufactured dates, PRs, logs or screenshots.

## Integration and final gate

Merge local-approved PR one at a time, preserving GitHub commit history. Rebase/merge conflicts require fresh gate and evaluation if behavior changed; avoid squash of historical report changes that obscures commits, preserve one creation commit per report. After all W5 PRs merge, run X14/15/16 and full flow from clean main, create integrated reports for assigned features. If one fails, block release, identify owner, fix in PR, re-run affected contract and full regression. Final evidence lists PR links, overlap calculation, last reports, state and actual release SHA. Documentation-only evidence commit does not imply tested new behavior; confirm product diff unchanged and rerun gates on final main.

## Relações verificáveis de estado

Em W0, `baseline=proposed`, `baselineCommit=null`, `currentWave=0`, todas as features planned. Após aprovação explícita e G0 completo, o coordenador registra `baseline=approved`, SHA completo do commit aprovado e `currentWave=1` em commit posterior. O SHA deve ser ancestral de HEAD. Avançar wave somente depois de merge local aprovado de todas as anteriores; regressão reabre feature já entregue sem liberar consumidores novos. Em `local_pass`, o relatório local avalia exatamente `implementationCommit` e corresponde a `implementerSession`; `mergedCommit` deve conter esse commit (merge preservando ancestralidade, não squash/rebase que descarte SHA avaliado). Se houver rebase, reavaliar SHA resultante antes do merge. Em integração, SHA avaliado é descendente de todos os merges; preservar PASS local do candidato e registrar nova sessão. SHA de avaliação, criação dos relatórios e merge/release devem estar no histórico pertinente. Relatórios anteriores podem referir outros candidatos; não os reescrever. IDs de sessão de avaliador não se reutilizam. A validação automatizada não confirma isolamento real, veracidade dos artefatos, aprovação humana ou PRs externos.
