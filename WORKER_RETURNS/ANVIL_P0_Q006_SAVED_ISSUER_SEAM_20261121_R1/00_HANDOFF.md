# Q006 saved-stream typed issuance — authority-binding correction

## Status

`AUTHORITY_BINDING_CORRECTED__MISSING_RESOLVER_RED_GREEN__OPERATION_TO_QUERY_BUILDER_ABSENT__Q103_SOURCE_HELD`

Isolated candidate only. No q103 original-wave issuance, new source scheme or
scientific authority is claimed.

## RED witness — missing resolver

`red_missing_resolver.py` was run against the prior candidate
`520094c79c25efaabed2db6c02150f2912091721` with
`effective_current=None`. The positive sourcefree call completed with
`SUPPORTED`; the absent decision-level check did not block it. See
`RED_MISSING_RESOLVER.out`.

## Correction

`rawlsing_next/pre553_anvil_stream_issuance.py` now requires
`decision_verifier: Callable[[HeldStreamIssuanceDecision], bool]`; there is no
optional check and no `lambda: True` default in the adapter. It calls the exact
held-decision verifier before validation, immediately before native execution,
after native execution, and at final output. It also validates the held
source/release/universe/replay roots, source identity, exact question binding,
query target, denominator, response-state semantics, operation authority and
current estate.

`HeldStreamIssuanceDecision` now carries the externally held denominator and
response-semantics refs. No source semantics are inferred from saved metadata.

## Retained refusals

The sourcefree proof refuses:

- forged/stale decision under the expected verifier;
- missing verifier;
- wrong source/release/universe/replay/question;
- wrong operation;
- missing/stale authority;
- raw outcome outside the approved domain;
- denied current authority;
- revocation during execution and at final output.

## Operation-to-query construction — exact first fault

The existing exact saved-stream consumer still requires caller-supplied
`EmpiricalPredicate` and `EmpiricalQuerySpec`. No production operation-to-query
builder exists for a verified ANVIL stream:

- `pre553_governed_query_issuer_v2` builds only from a
  `GovernedFrontierCompilation` and is explicitly `TEST_ONLY_SOURCEFREE`;
- `pre553_native_workload_binding.build_projection_catalog` is a test-only
  fixture builder and does not consume a verified saved stream;
- q103's 97/98/99 and asked/eligible source decision is absent, so constructing
  its operation/query would require source/schema authority not present here.

The candidate therefore freezes the valid authority-binding correction at the
adapter and leaves operation-to-query construction as an exact owner seam. It
does not invent a new source scheme, full R03 compiler or second evaluator.

### Required owner terrain

- **R03 / saved-release issuer owner**: production operation-to-query/predicate
  construction from the exact held operation and verified stream scope.
- **SRC04 QSM/source/risk owner**: q103 97/98/99, system missingness, and
  asked/eligible denominator (or narrower recorded-responses-only scope).

## Sourcefree proof

`proof_typed_issuance.py` / `TYPED_ISSUANCE.out`:

- positive: `SUPPORTED`, denominator 2, cells `0`/`1`, exact
  `PRE553_I03_QUERY_REPLAY`;
- nonanswer: `UNRESOLVED`, explicitly approved;
- roots unchanged, stream release retained;
- exact verifier mandatory and called before/after/output;
- all negatives above refused.

## Pins

- #1084 issuer: `357a0fbf...`
- #1205 asked-eligible: `c5efdbdf...`
- #1185 bridge: `3eee662d...`
- prior candidate: `520094c79...`
- q103 return: `4a3599065...`

No original source, original q103 data, saved-estate rebuild/modification,
protected refs, G5 claim, issue posts or original-wave I03 was used.
