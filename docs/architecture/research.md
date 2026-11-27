# Deep research: questions, evidence and decision gates

## Phase 1: alternatives

| Problem | Options | Selection rationale |
| --- | --- | --- |
| Capacity safety | in-memory mutex; serializable+retry; materialized occupied counter; event lock + fresh count | Mutex fails across processes; serializable needs retry handling; counter risks drift; event lock simple and provable for MVP |
| Async payment | sleep in HTTP; background thread; external broker; persisted DB job | Sleep violates R06, thread loses state, broker extra operations; same DB transaction keeps reservation/job atomic |
| UI/auth | SPA+API; custom auth; Django templates/session | Built-in CSRF, auth, forms and minimal tooling reduce attack surface and contracts |
| Cancel propagation | eventual job per ticket; synchronous atomic bulk update | Small event MVP can update all in commit; avoids partial state and new sales during cancellation |
| Metrics | counters by channel; cached projection; direct aggregate | Aggregate same snapshot preserves R12; no drift/invalidation |
| Agent evaluation | implementer self-test; isolated evaluator; final integrated run | Independent evaluator with observable evidence and release gate catches cross-feature regressions |

## Phase 2: official technical grounding

- PostgreSQL 17 explicit locking: https://www.postgresql.org/docs/17/explicit-locking.html ; row locks conflict until transaction end, consistent acquisition order reduces deadlocks. Applied to event→ticket→job.
- PostgreSQL 17 consistency checks: https://www.postgresql.org/docs/17/applevel-consistency.html ; use READ COMMITTED when relying on explicit locks and fresh reads. Applied to post-lock count; no mixed snapshot in dashboard.
- PostgreSQL 17 isolation: https://www.postgresql.org/docs/17/transaction-iso.html ; per-command snapshots at READ COMMITTED. Applied to single-statement read projections.
- Django 5.2 transactions: https://docs.djangoproject.com/en/5.2/topics/db/transactions/ ; atomic/savepoint and commit semantics. ORM locking: https://docs.djangoproject.com/en/5.2/ref/models/querysets/#select-for-update ; evaluate within transaction, TransactionTestCase for lock proof.
- Django 5.2 security: https://docs.djangoproject.com/en/5.2/topics/security/ ; session, CSRF, escaping, ORM parameters. Applied to security design.
- Docker startup order: https://docs.docker.com/compose/how-tos/startup-order/ ; service_healthy and service_completed_successfully. Applied to bootstrap lifecycle.
- Playwright Python: https://playwright.dev/python/docs/locators and https://playwright.dev/python/docs/test-assertions ; semantic locators and retrying assertions. Applied to browser evidence with explicit deadlines.

## Hypotheses to test, not results
H1: event row lock handles 30 requests across connections with no oversell or 5xx. H2: delay 3/34s plus polling meets 5/40s deadlines in evaluator environment. H3: worker restart recovers durable jobs. H4: compose works from clean clone on Linux/macOS without manual prep. H5: separate branches can integrate without schema changes after freeze. Use gates and record measured values. If disproved, revise ADR and contracts before implementation changes; never weaken brief. No production benchmark performed.
