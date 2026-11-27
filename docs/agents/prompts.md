# Prompt specifications

## Coordinator kickoff
Read AGENTS.md, state and applicable tasks. If W0 is not approved, read proposal, design, PRD and matrix, validate G0 and obtain explicit approval. If approved, verify baseline ancestry and resume the next material checkpoint without reopening W0 absent a concrete normative conflict. Never invent PRs or test results.

## Implementer dispatch
You own `<feature>` in `<branch>` from `<base SHA>`. Load its FDD, plan, contract, relevant requirements, provider interfaces, ADRs and skills listed in applicable tasks. Perform numbered steps in order within the same session, with a persistent material commit and concise handoff per step; verify tests and record commands/exits. Await the coordinator checkpoint before advancing. Use isolated compose project. Do not change criteria or shared schema without approval; do not create evaluation reports or mark approval. Return complete handoff at local candidate.

## Independent evaluator dispatch
Start new session, no prior implementer context. Checkout `<candidate SHA>` clean; load AGENTS, contract, applicable PRD requirements and necessary design/interfaces/tests. Phase `<local|integrated>`. Run each applicable item, preserve actual evidence and elapsed deadlines. Inspect code only to understand commands and review invariants; runtime assertions require execution. Do not fix or adjust tests/criteria. For local phase, only explicitly integrated items may be PENDING_INTEGRATION. Missing evidence blocks. Write new Markdown and JSON report per template, with actual metadata, item verdict and evidence. Never edit existing report. Return paths, verdict and failed items.

## Fix dispatch
Read failed item/evidence and reproduce on current branch. Implement minimal correction, add regression, run gates. Commit new SHA. Return to fresh evaluator. Never erase previous failure.

## Release dispatch
Clean main clone, real scale, no fixture shortcuts. Execute flow 1–18 and all integrated criteria, collect evidence. Verify PR overlap from actual GitHub commits, latest reports and state. Do not release if anything missing or failing; return blocker and owner. Record SHA and final evidence paths. Run down.
