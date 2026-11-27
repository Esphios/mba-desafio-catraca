# Security design and threat model

Local MVP, synthetic data only. Assets: user identities/sessions, event ownership, ticket codes, sales integrity, partner key, payment simulation input, reports. Trust boundaries: anonymous browser, session browser, API key client, web/worker, DB, agent/Git. Never log raw card, key, password, cookie or email. Never ask for real card. TLS not in local scope; bind host port to loopback by default.

| Threat | Control | Evidence |
| --- | --- | --- |
| role escalation in signup | role assigned server-side, whitelist fields, DB enum | TEST-A30 |
| IDOR | actor+owner filter for GET/POST, generic 404, no payload owner | TEST-A07,X03,X11,A28 |
| session replay/fixation | Django session rotation/logout flush, HttpOnly/SameSite; safe next URL | TEST-A30 |
| CSRF | middleware/forms + token, API-only exemption with key auth | TEST-A30,A34 |
| input injection/XSS | ORM bind params, autoescape, reject malformed data, no safe untrusted HTML | TEST-A09,A17,A34; adversarial escaped markup |
| card/secret leakage | simulator uses suffix transiently, logs allowlist; no body logging | TEST-A17 |
| API enumeration | fixed contract allows lookup across channels with valid key; no PII; opaque UUID | TEST-A23 |
| unauthorized API request parse | key guard before reading body; 16 KiB body cap after key guard (422), no redirects | TEST-A34 |
| overbooking / replay result | DB guard, atomic job, terminal check | TEST-A14,A33,A36 |
| tampering with reports | append-only files, SHA + Git history, separate context | TEST-A37,P03 |

Password validator minimum eight characters for local baseline, framework hash algorithm, no plaintext. Normalize email consistently; database uniqueness protects concurrent signup. Session/partner secret default demo-only; README includes synthetic credentials, never production keys. Compare key constant time; configure key in env override, no accidental print. CSRF error generic. Do not disable framework security globally. Web pages cache-control no-store on authenticated views. No debug trace in demo. Query parameter next must be same-host safe; no open redirect. Use mandatory separate runtime and migration roles: runtime web/worker has only necessary DML, no ownership/DDL/CREATEROLE; bootstrap uses migration credentials for schema and seed; don't expose PostgreSQL host port. Backup/production hardening out of scope. Test code and evidence redact sensitive data; dependency lockfile and review. Residual: local HTTP, no brute-force rate limiting, key grants cross-channel ticket lookup as mandated; no production claim.
