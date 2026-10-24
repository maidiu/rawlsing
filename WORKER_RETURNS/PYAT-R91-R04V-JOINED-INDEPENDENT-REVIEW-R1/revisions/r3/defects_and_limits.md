# R91-R04V R3 defects and limits — ACCEPT_SCOPED_LOCAL

Verdict: **ACCEPT_SCOPED_LOCAL**. The sole R2 defect is fixed: completed unary
outputs restore as actual native `QueryExecutionResult` objects with equal
`query_ref`, facts and release refs; completed governed discovery restores as a
frozen checked `RetainedDiscoveryResultView` with equal evaluated-frontier,
replay, fact/receipt and executed predicate/query identities. The same
consumers work, mutation of the checked discovery view raises
`FrozenInstanceError`, and all prior fixed-pin/partial-cold/manifest/no-rerun
positives remain.

## Fixed R2 defect

- Unary checkpoint output material now includes exact `query_ref`, fact
  preimages, `source_scope_mode` and release refs; restore reconstructs actual
  `QueryExecutionResult` objects.
- Discovery output material now includes contract/authority/grammar/
  evaluated-frontier/replay, coverage/counts, receipt preimages, fact refs/facts,
  executed predicate/query refs and valid-empty; restore reconstructs the frozen
  `RetainedDiscoveryResultView` with ordering/closure checks.
- Mutable facts-only `SimpleNamespace` output views are gone for the output
  payload. Discovery result remains inside a `SimpleNamespace` container, but
  its `native_result` is the frozen checked view; this is a non-blocking
  container note, not a mutable authority/output object.
- Output material is validated against the original external checkpoint pin and
  native closure before release.

## Independent evidence

- Author R3 focused suite: 6 passed, 0 failed/error/skip.
- Retained R03 suite: 16 passed, 0 failed/error/skip.
- Reviewer successor probes: 5 passed (actual unary `QueryExecutionResult`
  identity; governed frozen discovery identity; mutation refusal; external pin
  forgery refusal/genuine restore; real partial multi-unit fresh-process resume
  with no completed rerun).
- Prior R2 positives retained: actual governed capture, external original pin,
  original manifest, real partial multi-unit cold resume, completed-unit
  no-rerun, pending native execution, current grant/source recheck.
- U43 exact; native/R03 owners and R04.byte decoder unchanged; two authorized
  code paths only.

## Residual limits / not reached

- Sourcefree TEST_ONLY local trusted host only; no source respondent access.
- Both pin and candidate replaced by a different trusted host is the R61AV
  excluded boundary.
- No new global durable exactly-once/anti-fork, cryptographic issuer/R09/R05
  requirement is claimed.
- R05/original science/CI/prod/N11/N12/Sorok/J52/W52 remain NOT_REACHED.
- No candidate repair, self-adoption or production merge.

## Minimal missing function

None for the commissioned R3 scope.
