# Harness: operação e gates

## Contract of commands (implement in F01)

`bash bin/up`: resolve root independent of cwd; validate Docker daemon/Compose and env values; configure project/port; build pinned images; start DB, wait health, run bootstrap migrate+seed, start web/worker, wait readiness within explicit timeout; verify HTTP from host using Node LTS or container. No .env copy, sudo, manual setup, payment secret. Return nonzero on failure with service diagnostics; no success banner before readiness. On failed startup clean only resources created by current invocation when safe, preserve prior demo volume. `bash bin/down`: down project with --remove-orphans; verify no running service/host listener started by this project; preserve volume unless explicit destructive command outside default. `bash bin/gates [--feature Fxx|--release]`: isolated fresh project and data, never reconfigure or tear down demo; use temp project name unique per invocation, dynamic available port, trap cleanup on success/failure/INT/TERM, return original failure or cleanup failure. Git history checks on host (not shallow). Test runner uses container image; bind code readonly where possible. `bash bin/flow`: run public evaluator flow against separate real-scale stack, browser + HTTP; release only, cannot skip any required step.

## Defaults and readiness

CAT_PROJECT=catraca-demo; CAT_PORT=8080; WEB/API=http://127.0.0.1:8080; CAT_PROFILE=demo; CAT_GATEWAY_SCALE=1; CAT_PARTNER_KEY=local-passgate-26; CAT_SECRET local only. Use loopback mapping. `CAT_PROJECT` and `CAT_PORT` must differ per worktree; no fixed container_name, no shared DB volume. Test profile may accelerate only named non-timing suites. Reject CAT_GATEWAY_SCALE !=1 for demo/release. Health checks DB reachable, migration complete, worker heartbeat fresh. On worker crash readiness must become unhealthy; restart completes outstanding job. Bootstrap seed idempotent: use normalized unique email, validate roles of seed identities, never reset unrelated accounts or events. Seed fixed synthetic credentials per README. Timeouts defined in scripts, stdout concise diagnostics; logs redacted.

## Gate matrix

| Gate | Phase                  | Checks                                                                                  | Failure action                           |
| ---- | ---------------------- | --------------------------------------------------------------------------------------- | ---------------------------------------- |
| G0   | W0/every PR            | validate_docs, OpenAPI, model oracle, links, render Mermaid in container                | no implementation if design inconsistent |
| G1   | all                    | image build, Ruff check/format, Django check, lockfile, migrate fresh/upgrade, no drift | fix build/schema                         |
| G2   | all                    | unit test named cases, no zero tests/skips                                              | fix logic                                |
| G3   | all                    | PG real, integration, guard, rollback, concurrency, job                                 | fix implementation                       |
| G4   | from relevant adapters | API shape/auth, browser, 30/5 bursts, default timing                                    | fail contract                            |
| G5   | each feature           | local evaluator report; later integrated report if required                             | new commit/new evaluation                |
| G6   | after merge/release    | X14–X16, flow 1–18, README/state/report history, PR overlap                             | block release                            |

Implementation gates are not yet present; F01 implements. G0 runs included scripts now; `python3 scripts/test_baseline.py` and `python3 docs/validation/w0-audit/reproduce_mutations.py` must also pass. Gate phase distinctions: baseline permits planned features/no reports; candidate local checks only available feature IDs and provider contracts, but not empty suite or hidden skip. Release requires all A/X/P, reports and state complete. Run docs check separately from actual product gates to avoid mislabel. Validate evidence script checks structure/history only; independent evaluator must verify semantic truth. Timing runs use scale=1 and real worker; measure from creation + observed request, poll <=200ms, no timeout extension to mask failure. Run timing suite without competing stress. Real HTTP load uses multiple threads/processes; validate status bodies, ticket IDs/code uniqueness, DB counts. For mutation proof intentionally break one test in temp copy; gate must fail and clean up. Restore before PR.

## Operational troubleshooting

Registry unreachable: log image, network cause; retry build after network available. Port occupied: fail or choose CAT_PORT explicitly, no killing foreign process. DB health failure: inspect own compose logs; preserve volume. Bootstrap failure: inspect migration/seed output; no schema reset automatically. Worker lag: check heartbeat, pending jobs due, DB contention and lock wait; do not increase required gateway deadline. Gate failure: preserve test output and run targeted tests in isolated profile. Cleanup failure: identify project and residual containers, no global prune. macOS: ensure Docker Compose works with supported engine and arch; WSL: run all commands inside distro. Do not claim platform compatibility before smoke evidence.

## Limite entre W0 e W1

W0 aprova manifesto de versões/digests verificados e reproduz G0 em containers de ferramentas, sem Dockerfile, lockfile da aplicação, Compose ou código de produto. W1 materializa pins e prova build, smoke, grants e compatibilidade real; não declarar compatibilidade da aplicação antes dessa execução. Validar Docker/Compose/WSL e arquiteturas prometidas na W0 com containers de ferramenta; repetir com stack real em W1. A19 exige captura do pending real no browser; perda da janela de observação não autoriza PASS. A14: dez rodadas DB; A24: duas HTTP; executar ambas.
