# Q006 recorded-response operation — candidate

## Status

`RECORDED_ONLY_OPERATION_CONSTRUCTOR_IMPLEMENTED__SOURCEFREE_NATIVE_SEVEN_CODE_GREEN__Q103_ORIGINAL_NOT_RUN`

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
undecoded raw object. Recorded membership is established only from the held
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
the query/replay identity (`recorded_transform_ref`). Stored Parquet, locators,
authority and stream refs are not modified.

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
- native state `SUPPORTED`;
- exact repeat replay equal;
- stream release retained;
- wrong source/release, missing authority, duplicate code, unknown code and
  denied verifier refusals.

This is a sourcefree q103-shaped fixture, not an original SRC04 run.

## Private MainMac harness contract

`run_recorded_q103_private.py` is the actual private read harness. It verifies
the owner decision SHA, uses exact stream roots/current binding, loads an exact
operation JSON containing the typed authority/ref preimages, builds the same
recorded operation and executes the existing native I03 evaluator.

```bash
PYTHONPATH=/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/REMONT_Q006_ISSUER \
python3 /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/REMONT_Q006_ISSUER/WORKER_RETURNS/ANVIL_P0_Q006_SAVED_ISSUER_SEAM_20261121_R1/run_recorded_q103_private.py \
  --owner-decision "$PRIVATE/q006_q103_owner_decision.json" \
  --operation-json "$PRIVATE/q006_q103_operation.json" \
  --stream-root "$SRC04_STREAM_ROOT" \
  --release-path "$SRC04_RELEASE_PATH"
```

The operation JSON is the exact held `HeldRecordedOperation` material:
source/root/question/operation, authorities, recorded risk/routing/member-set
refs, measure/response-semantics/domain refs, replay roots and transform ref.
It is not produced by this author from metadata.

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
