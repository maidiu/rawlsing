# R95-R06V independent world-consumer failures and limits — REVISE

Verdict: **REVISE**. The authored actual R05->P41 path produces a real positive,
and the 10-test author suite passes. The R06 public wrapper does not authenticate
that actual consumer execution: it accepts caller-supplied/canned receipts,
accepts clock/hash-only temporal changes with identical real routes, accepts a
transport label without a linked indexed query, and accepts CONTEXT promotion
with an arbitrary FF ref. The full authorized R06 function is therefore not
qualified.

## Prioritized remaining failures

### 1. Actual P41/E04 consumer invocation is not authenticated (blocking)

`R05WorldConsumerRequest.consumer` is an arbitrary caller callable. The wrapper
calls it and validates only the returned receipt's self-hash, schema/providers,
R05 learned/M1/M2/evidence/N10E/N10W bindings and source/field values. A lambda
returning a copied/self-consistent receipt, with no actual P41/N9/N10W/E04
execution, is accepted as `R05_WORLD_SELECTED_VIEW`.

Reviewer probe H4:
`select_r05_world_view` accepted a canned callback returning the receipt; no
actual consumer identity/attestation is required. This is exactly the forbidden
"fixture callback returning canned values"/receipt echo, not an authenticated
actual R05->P41 dependency.

**Required:** configure/construct the actual P41/N9/N10W/E04 consumer inside the
R06 wrapper (or require a host-retained actual-execution receipt with owner
identity/attestation that cannot be synthesized by the subject); verify actual
call/values, not a caller-supplied mapping. If an indispensable P41 caller path
is outside the grant, return that exact path/invocation dependency.

### 2. Temporal dependence is clock/hash-only, not actual consumer values (blocking)

`select_r05_world_view` accepts a temporal pair when clocks are distinct and
receipt `content_hash` differs; it does not require the actual routes/N10W/
consumer values to change. Reviewer probe H1 set T1's `structural.routes` and
`n10w` equal to T0, recomputed the receipt hash, and the wrapper still returned
`temporal_changed=True`. This is a clock-label/hash-only change, explicitly
insufficient under the R2/R06 requirements.

**Required:** require the declared synthetic pair to change actual consumer
routes/values/N10W/structural assertion (identity-bearing comparison), while
still rejecting label/hash-only or identical receipts. Preserve the declared
synthetic modeled-rule semantics; do not invent F7 science.

### 3. Transport label is accepted without a linked indexed query (blocking)

The wrapper checks only `relation_transport_authorized` and matching
`relation_ref`; it does not verify that a lawful linked indexed cross-unit query
or transport index exists. Reviewer probe H2 used person/household fields with
an arbitrary relation ref and authorized flag, and the wrapper accepted the
view. The R95 grant's explicit critical hold is
`CROSS_UNIT_UNAVAILABLE_NO_POOLING`: a relation/transport grant alone does not
make an unlinked-unit query executable.

**Required:** validate actual linked indexed cross-unit execution/relation
evidence; otherwise return typed `UNAVAILABLE`/refusal. No pooling by label or
boolean.

### 4. Context promotion accepted with an arbitrary FF authority ref (blocking)

The wrapper checks `ff_structural_authority_ref is not None` for CONTEXT fields;
it does not validate the actual FF structural issue/authority. Reviewer probe H3
promoted a field to CONTEXT and supplied an arbitrary `ExactRef`, and the view
was accepted.

**Required:** validate the actual competent FF structural authority/issuance
context (or return typed unavailable/refusal); a non-null ref is not authority.

### 5. Two-field assertion change is not independently authenticated

The wrapper checks field IDs/values against receipt `n9.rules` and that the
field is in dependencies, but because the receipt/callback is untrusted and the
actual consumer is not invoked, a canned receipt with both fields and unchanged
routes can satisfy the wrapper. This is part of the same actual-consumer
authentication gap; two fields must change the same actual consumer assertion,
not just appear in a receipt/rules mapping.

## Retained positive evidence

- Author R06 R2 suite: 10/10 passed under the reviewer harness (165s).
- Reviewer independent actual-path positive: actual R05 learned
  `LEARNED_CONSUMER_EXACT_SUPPORTED` -> actual P41 N9/N10W/E04 receipt, routes
  `ELIGIBLE` -> `BLOCKED_BY_MODELED_RULE`, N10E content hash bound to the R05
  consumer result, coordinator original present.
- Authored cold replay and prior J42/R06 R1 positives remain preserved.
- U43/R03/R04/R05/R08/native/FF/temporal/J42/P41/E04 bodies unchanged; only the
  two authorized R06 code paths differ from original R06 base.
- No R05 extension, original science/F5/F6/F7/F8 issuance, CI/prod/N11/N12/
  Sorok/J52/W52 claim.

## Limits / NOT_REACHED

Sourcefree TEST_ONLY local trusted host only; no source respondent access.
Original F7 measured waves, original 35/1890/F6/F8, source/science, CI/prod,
N11/N12, Sorok and J52/W52 remain held/NOT_REACHED. No new trust service,
cryptographic issuer, R09 or global exactly-once requirement. No candidate
repair or self-adoption.
