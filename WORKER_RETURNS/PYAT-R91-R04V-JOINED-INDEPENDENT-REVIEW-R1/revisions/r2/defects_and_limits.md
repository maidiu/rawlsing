# R91-R04V R2 remaining failure and limits — REVISE

Verdict: **REVISE**. R2 fixes the actual governed capture, external original
pin, original manifest retention and real partial multi-unit cold restart; the
reviewer independently proved the partial multi-unit fresh-process resume that
the author had only shown in-process. One remaining output-identity gap prevents
ACCEPT: completed native outputs are rehydrated as mutable facts-only
`SimpleNamespace` views, not actual native owner result objects or checked
immutable views carrying the original output identities.

## Remaining failure — completed native output identity is a mutable facts-only view (blocking)

**Contract:** R2 requires completed native output/fact OBJECT material or actual
usable owner representations/checked immutable views consumed by the SAME native
downstream assertion, not just refs or rawdict with advertised hashes. Exact
operation/job/receipt/fact identity must be preserved.

**Observed:** `_completed_entry_view` reconstructs a completed
`NativeWorkloadResult` with
`native_outputs=tuple(SimpleNamespace(facts=...))`. The original
`QueryExecutionResult` output object is not retained/reconstructed; its
`query_ref` and other output identity fields are absent. The view is a mutable
`types.SimpleNamespace`, not a checked immutable view. A same consumer expecting
the native output contract (`query_ref`, etc.) raises AttributeError; the
reviewer probe fails with
`'types.SimpleNamespace' object has no attribute 'query_ref'`.

For completed discovery, `_completed_entry_view` similarly reconstructs a
`SimpleNamespace(native_result=SimpleNamespace(...))` rather than an actual
owner result view; only facts/manifest are checked by the author tests.

**Required minimal function:** reconstruct actual native owner output objects
(`QueryExecutionResult` / actual discovery result) or a frozen checked view with
all identity-bearing output fields (query/evaluated-frontier/replay/fact
identities and associations), and validate it before releasing completed
cached facts. Facts-only mutable namespaces do not satisfy same-consumer output
identity.

## Fixed R2 requirements (retained)

- Actual R03 governed `NativeDiscoveryExecution` is captured/restored with exact
  facts and original manifest; source SHA supplied by the trusted host.
- Joined checkpoint requires a separately provisioned original pin; a
  self-rehashed forged checkpoint with altered receipt/output refs is rejected.
- Real partial multi-unit prefix capture/resume works; completed units are not
  rerun, pending units execute through the existing Batch path, and the
  reviewer independently proved the fresh-process partial resume (author had
  only in-process partial evidence).
- Original manifest is retained for completed workloads.
- Author focused 5/5; retained R03 16/16.
- U43 exact; R03/native owner bodies and R04.byte decoder unchanged; two
  authorized code paths only.

## Limits / not reached

Sourcefree TEST_ONLY local trusted host only; no source respondent access.
Both pin and candidate replaced by a different trusted host remains the R61AV
excluded boundary. No new global durable exactly-once/anti-fork, cryptographic
issuer/R09/R05 requirement is imposed. R05/original science/CI/prod/N11/N12/
Sorok/J52/W52 remain NOT_REACHED. No candidate repair or unauthorized
native-owner edit.
