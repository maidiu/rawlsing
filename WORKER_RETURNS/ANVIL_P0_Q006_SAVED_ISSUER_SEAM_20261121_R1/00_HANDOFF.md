# Q006 recorded-response operation — candidate

## Status

`RECORDED_ONLY_NATIVE_SOURCEFREE_SEVEN_CODE_DENOM7_GREEN__REAL_TOKEN_UNWRAP_FIXED__PRIVATE_OPERATION_ARTIFACT_PRESENT`

One focused old-code continuation only. No protected/shared refs, original data,
original q103 run, issue post or G5 claim.

## Actual constructor

`rawlsing_next/pre553_anvil_stream_recorded.py`

`HeldRecordedOperation` is the externally held q103 decision binding. It carries:

- owner-decision SHA-256;
- exact source/release/universe/replay roots and native question;
- authorized operation and allowed raw codes;
- exact source/routing/query authority refs;
- distinct recorded risk, routing-rule, member-set replay, predicate replay,
  query replay, measure and response-semantics refs.

`build_recorded_operation` constructs the existing `EmpiricalPredicate` and
`EmpiricalQuerySpec` with `make_empirical_predicate` and `EmpiricalQuerySpec`
directly from that operation. It does not consume a prebuilt query/predicate,
does not use the TEST_ONLY `_query_for_bundle`, and does not create scientific
authority.

It resolves the verified saved scalar occurrences from the stored R5
`raw_typed` lane using `R5TypedValueCodec`; it never calls `str()` on an
undecoded raw object. The real projected native wrapper
`{"$raw_physical_value":{"token":...}}` is unwrapped strictly through the
codec. Missing token refs are integrity failures, not system missing; invalid
wrappers and nonintegral tokens are refused or preserved as unknown rather
than counted as missing. Recorded membership is established only from the held
allowed raw codes. A stored system-missing event and a genuinely absent event
are distinguished and excluded separately from the denominator. Unknown codes
and duplicate occurrences refuse.

## Narrow native admission

`pre553_direct_estate_i03.DirectEstateI03Session` accepts an internal
`RecordedRoutingPlan` from `_make_recorded_routing_plan`; there is no
public raw-tuple override. The plan is keyed by exact
`(respondent,target,risk)` and is not scanned per respondent. The normal path
is unchanged and ordinary `ROUTING_UNKNOWN` still refuses.

The projection supplies ephemeral `RoutingEligibilityFact` rows with a distinct
recorded risk ref and member-set replay commitment. A scoped observation view
maps each stored R5 scalar to a transformed counted event; the original event
ref is retained in dependency provenance, and the transform commitment is in
the query/replay identity (`recorded_transform_ref`). The transformed event
binds the materialized source authority and its authority closure is checked
before the native index, so an original stored event authority cannot surface
as a late historical-authority failure. Stored Parquet, locators, authority and
stream refs are not modified.

The existing native I03 evaluator performs all counting; there is no second
evaluator or manual count.

## Sourcefree proof

`proof_recorded_operation.py` / `RECORDED_OPERATION.out`:

- owner decision SHA-256 `e3de52e...` verified;
- stored shape: `97`/`98` DK, `99` substantive, one stored system-missing
  event, one separate absent event;
- codes `1,2,3,4,97,98,99`;
- seven disjoint native cells, each support 1;
- denominator exactly **7**;
- system-missing and absent each exactly **1**, excluded separately;
- ordinary token unwrap `97`, system-missing token `None`, nonintegral token
  `1.5`, and invalid wrapper refusal are separately exercised;
- native state `SUPPORTED`;
- exact repeat replay equal;
- stream release retained;
- wrong source/release, missing authority, duplicate code, unknown code and
  denied verifier refusals.

This is a sourcefree q103-shaped fixture, not an original SRC04 run.

## Private MainMac harness contract

`run_recorded_q103_private.py` is the actual private read harness. It verifies
the owner decision SHA, re-reads the held R2 decision at current checks, uses
exact stream roots, loads the concrete private operation artifact, builds the
same recorded operation and executes the existing native I03 evaluator.

Its private output now retains `typed_state`, `p02_failure_state`,
`execution_detail`, uncertainty state, cells, replay ref and release refs. A
native `UNAVAILABLE` is never reported as accepted positive counts:
`positive_counts_accepted` is false unless the fact is `SUPPORTED` with a
positive denominator and at least one cell. Stdout is sanitized and contains no
counts; private output is mode 0600.

```bash
PYTHONPATH=/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/REMONT_Q006_ISSUER \
python3 /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/REMONT_Q006_ISSUER/WORKER_RETURNS/ANVIL_P0_Q006_SAVED_ISSUER_SEAM_20261121_R1/q006_materialize.py \
  --owner-decision "$PRIVATE/q006_q103_owner_decision.json" \
  --r2-decision "$PRIVATE/r2_typed_user_decision_private.json" \
  --q006-dir "$PRIVATE/q006_q103_execution" \
  --question-ref "<full exact q103 custody ref>" \
  --output "$PRIVATE/q006_q103_execution/q006_q103_operation.json"

PYTHONPATH=/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/REMONT_Q006_ISSUER \
python3 /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/REMONT_Q006_ISSUER/WORKER_RETURNS/ANVIL_P0_Q006_SAVED_ISSUER_SEAM_20261121_R1/run_recorded_q103_private.py \
  --owner-decision "$PRIVATE/q006_q103_owner_decision.json" \
  --r2-decision "$PRIVATE/r2_typed_user_decision_private.json" \
  --operation-json "$PRIVATE/q006_q103_execution/q006_q103_operation.json" \
  --stream-root "$SRC04_STREAM_ROOT" \
  --release-path "$SRC04_RELEASE_PATH"
```

The operation JSON is the exact held `HeldRecordedOperation` material:
source/root/question/operation, authorities, recorded risk/routing/member-set
refs, measure/response-semantics/domain refs, replay roots and transform ref.
It is materialized only from the owner decision, held R2 decision and q006
inputs; no source metadata is inferred. `validate_operation_authorities` runs
the same positive-authority checks against the canonical universe mapping
before the stream/index stage.

The controller's concrete private operation artifact is now present at the
safe q006 path, mode 0600, SHA-256
`fa0582562c3ccd57194d3fb4f375693d61eb725cfe3efc10261940be5f9afdf3`. It carries
the full exact q103 question ref (`NATIVE_QUESTION|urn:...7f5834521c9c4a400580|7f5834...`)
and the held owner/R2 binding. `q006_materialize.py` can regenerate it when the
controller supplies `--question-ref`; the local author sidecar only had the
object ID, which is the recorded materializer fault. No hash was fabricated.

The original SRC04 execution remains explicitly not run until the controller
checks the candidate and private authority.

## Preserved boundaries

- no asked risk synthesized from recorded rows;
- no stored event/locator/Parquet mutation;
- no TEST_ONLY R03 path or new source scheme;
- no full compiler or second evaluator;
- original q103 data, raw SAV, protected refs, G5 and issue posts untouched.

Pins: #1084 `357a0fbf...`, #1205 `c5efdbdf...`, #1185 `3eee662d...`, q103
`4a3599065...`.

## Held source-universe DEFER — exact first fault

The actual cheap probe shows:

- operation-only registry: `exact historical authority unavailable; no fallback permitted`
- with the stored snapshot: `EmpiricalUniverse authority closure contains nonpositive exact snapshot`

The sole attached source snapshot is `SOURCE_SEMANTICS_TOPOLOGY` with
`decision_state=DEFER` and scope `EXACT_SOURCE_CODEBOOK_AND_H48_EVIDENCE_ONLY`.
The consuming stage is `execute_empirical_query` preflight
`_validate_public_object_authorities` on `EmpiricalUniverse`, before `indices_for`.

No existing route promotes that historical snapshot:

- `resolve_exact_runtime_authority` returns only adopted historical snapshots
- `authorize_i03_operation_successor` requires a positive `PREDICATE_GRAMMAR`
- `AuthorityRegistry.resolve_exact` has no fallback

No implementation or relabel was made. The exact missing native interface is an
adopted source-universe/source-semantics successor resolver bound to the
historical DEFER snapshot, exact source/release/universe/replay roots and the
q103 recorded-only operation. The smallest owner decision is to issue/adopt one
current positive source-universe successor for that exact scope.

## Scoped historical DEFER universe use

`RecordedUniverseUse` is attached only to the recorded-operation plan and is
consulted at the native `index.universe` authorization points in
`_pre553_query_eval`, not at the early query-only fitness block. Ordinary
universe validation remains strict; historical DEFER is never rewritten.

The sourcefree full native proof is `UNIVERSE_USE.out`: `SUPPORTED`, repeat
replay equal, both historical and positive identities retained, missing/wrong
history/wrong query negatives refused. `REAL_UNIVERSE_USE.out` is a real
metadata-only preflight over the stored DEFER and issued owner decision:
`PASS`, no respondent bodies read, no index built, no private IDs published.
