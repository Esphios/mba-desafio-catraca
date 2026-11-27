# Prompt specifications

## Coordinator kickoff
Read AGENTS.md, proposal, design, PRD, matrix, tasks and state. Review assumptions, validate G0, identify ambiguity and request approval on decisions only. Do not write product code before W0. Produce approved baseline SHA, dependency plan and next feature. Never invent external PRs or test results.

## Implementer dispatch
You own `<feature>` in `<branch>` from `<base SHA>`. Load its FDD, plan, contract, all provider interface docs and skills listed in tasks. Perform only its numbered steps. Verify tests at each step and record actual commands/exits. Use isolated compose project. Do not change criteria or shared schema without coordinator approval; do not create reports or mark approval. Return handoff with SHA, tests, limitations, touched paths, contract changes. Stop after local candidate.

## Independent evaluator dispatch
Start new session, no prior implementer context. Checkout `<candidate SHA>` clean; load AGENTS, PRD, contract and necessary design/interfaces. Phase `<local|integrated>`. Run each applicable item, preserve actual evidence and elapsed deadlines. Inspect code only to understand commands and review invariants; runtime assertions require execution. Do not fix or adjust tests/criteria. For local phase, only explicitly integrated items may be PENDING_INTEGRATION. Missing evidence blocks. Write new Markdown and JSON report per template, with actual metadata, item verdict and evidence. Never edit existing report. Return paths, verdict and failed items.

## Fix dispatch
Read failed item/evidence and reproduce on current branch. Implement minimal correction, add regression, run gates. Commit new SHA. Return to fresh evaluator. Never erase previous failure.

## Release dispatch
Clean main clone, real scale, no fixture shortcuts. Execute flow 1–18 and all integrated criteria, collect evidence. Verify PR overlap from actual GitHub commits, latest reports and state. Do not release if anything missing or failing; return blocker and owner. Record SHA and final evidence paths. Run down.
