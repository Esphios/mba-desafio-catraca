# Evaluation report template (not an actual report)

Create `reports/<UTC compact timestamp>-<short SHA>-<local|integrated>.md` and same basename `.json`. Use actual values, no placeholder in committed report. Markdown includes:

- Feature, phase, date UTC ISO 8601, full tested commit SHA, branch, tool, model, evaluator session ID, implementer session ID, clean checkout confirmation.
- Environment: compose project/port, gateway scale, DB, commands, cleanup and exit codes.
- Each contract item: ID, expected, steps, observed, evidence paths/command output, PASS/FAIL/BLOCKED/PENDING_INTEGRATION. Pending only integrated item in local report. For PASS include nonempty observed evidence, not just a test name.
- Overall PASS only if all applicable items PASS; no unresolved blocker. For local report state explicit pending integration IDs. No edited historical report.

Machine JSON uses `feature`, `phase`, `date`, `commit`, `tool`, `model`, `evaluatorSession`, `implementerSession`, `clean`, `verdict`, `items` array of `{id, verdict, evidence}`. Evidence is text with observed result and/or relative artifact paths; Markdown sibling is human record. Store actual evidence alongside in unique directory when needed. Template itself is not in reports. `validate_evidence.py` checks structural metadata, contract IDs and Git history, not authenticity; coordinator inspects semantic correspondence and actual independent context.

**Formato verificável:** incluir no Markdown exatamente um bloco cercado `json` com o conteúdo integral do JSON irmão (sem modificar os valores). Além do bloco, registrar a narrativa de ambiente, comandos, resultados e evidências por item. Campo opcional `artifacts` no JSON: objeto de caminhos relativos à raiz, dentro de reports da própria feature, para SHA-256 hexadecimal do conteúdo de cada arquivo externo usado como evidência. Incluir todos os arquivos citados; se a evidência for integralmente textual, pode omitir `artifacts`. Commitar JSON, Markdown e artefatos juntos, uma única vez. Não guardar segredos. O coordenador confere também o texto narrativo e se toda referência está no manifesto; a igualdade do bloco não autentica a narrativa.

State `latestEvaluation` stores the relative JSON report path; the sibling Markdown remains mandatory. `releaseStatus` is set by coordinator only after full release verification.
