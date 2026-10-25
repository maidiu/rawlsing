# R95-R06V R4 qualification, residual limits and non-blockers

Verdict: **ACCEPT_SCOPED_LOCAL**. No blocking R4 boundary defect was found in
the authorized sourcefree grain. The four named repairs hold under independent
replay and successor controls; retained limitations are stated below.

## Verified corrections

1. **Pinned P41 owner.** `_pinned_p41_runtime` materializes the fixed Git packet
   `f27d1101048638bba395143a48efb7ef00bfcda4`; `_validate_pinned_runtime`
   compares a deterministic tree SHA256 excluding bytecode; `_execute_p41_world`
   purges `bootstrap`/`p41_service`/`fixture`/`readthrough`/`product`, imports
   the pinned owner, and checks imported `bootstrap`/`p41_service` files under
   the pinned root. Forged caller runtime refuses `UNTRUSTED_P41_RUNTIME`;
   preloaded fake owner modules are purged and do not mint receipts.
2. **Trusted execution context.** The private
   `configure_trusted_execution_context` executes the actual accepted
   coordinator, checks original/learned/step, and registers an opaque handle.
   The public request cannot supply its own verifier/original/runtime authority.
   Missing/forged handle, forged coordinator original, and same-context step/
   learned substitutions refuse; genuine positive restores with the same view
   hash. S1/S3 and the R4 step/learned/handle controls pass.
3. **CONTEXT held.** All public wrappers return
   `CONTEXT_STRUCTURAL_AUTHORITY_HELD` for CONTEXT fields, including a plausible
   real-type admission. No competent FF issuer is configured; generic FF use
   remains unqualified. Direct synthetic STRUCTURAL positive remains.
4. **Temporal actual payload.** Equal actual routes/N10E/N10W with distinct
   clocks/hashes refuses `R05_TEMPORAL_PAIR_NOT_CONSUMED`; the declared
   synthetic pair positive changes actual routes, and cold/current/as-of/
   revocation/severance/restore remain.

Cross-unit label-only pooling remains `CROSS_UNIT_LINKED_QUERY_UNAVAILABLE`
across all three public wrappers. Two real fields change the same actual
consumer assertion.

## Residual limits (not R4 blockers)

- Sourcefree TEST_ONLY local trusted host only; no source respondent access.
- The opaque execution handle is a private local registration, not a
  cryptographic/R09 issuer. A caller able to execute arbitrary host code can
  configure its own trusted context; the commission explicitly excludes that
  deliberate private-host/context-factory replacement from the public subject
  boundary. The public request itself cannot select its own original/verifier.
- No competent FF issuer is configured; CONTEXT structural use is honestly HELD
  and generic FF remains unqualified. This is the authorized response, not a
  demand for new scientific issuance.
- Original F7 measured waves, original 35/1890/F6/F8, source/science, F5/F6/F7
  issuance, CI/prod, N11/N12, Sorok and J52/W52 remain held/NOT_REACHED.
- The temporal pair is declared synthetic modeled-rule software evidence, not
  original F7 measured-wave issuance; no original scientific claim follows.
- Scope is the authorized sourcefree grain; no universal/source-qualified
  completion or production adoption is claimed.

## Non-blocking observations

- The `R05ActualExecution.trusted_context` field remains present but unused; the
  effective authority is the registered `execution_handle` and module-private
  context. Supplying a different `trusted_context` object does not change the
  authenticated context.
- Author R4 code retains the two authorized R06 paths only; accepted bodies are
  unchanged. No new R09/signer/service was added.

No candidate repair or self-adoption was performed by the reviewer.
