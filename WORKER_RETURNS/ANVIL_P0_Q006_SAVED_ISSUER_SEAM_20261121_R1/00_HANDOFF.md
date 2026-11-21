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

It resolves the verified saved scalar occurrences using the existing stream
decoder. Recorded membership is established only from the held allowed raw
codes. A respondent with no event is an explicit nonmember and is tallied as
physical missing, outside the native denominator. Unknown codes and duplicate
occurrences refuse.

## Narrow native admission

`pre553_direct_estate_i03.DirectEstateI03Session` accepts an optional
`recorded_routing` tuple. `execute_anvil_stream_i03` forwards it for this one
read. The normal path is unchanged and ordinary `ROUTING_UNKNOWN` still refuses.

The projection supplies ephemeral `RoutingEligibilityFact` rows with a distinct
recorded risk ref and member-set replay commitment. Original event refs are
retained in routing dependencies and native provenance. Stored Parquet,
locators, authority and stream refs are not modified.

The existing native I03 evaluator performs all counting; there is no second
evaluator or manual count.

## Sourcefree proof

`proof_recorded_operation.py` / `RECORDED_OPERATION.out`:

- owner decision SHA-256 `e3de52e...` verified;
- codes `1,2,3,4,97,98,99`;
- seven disjoint native cells, each support 1;
- denominator exactly **7**;
- one physical-missing occurrence excluded separately;
- native state `SUPPORTED`;
- exact repeat replay equal;
- stream release retained;
- wrong source/release, missing authority, duplicate code, unknown code and
  denied verifier refusals.

This is a sourcefree q103-shaped fixture, not an original SRC04 run.

## MainMac command

```bash
ANVIL_Q006_OWNER_DECISION=/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/evidence/P0_TWO_SAVED_WAVES_PRIVATE/q006_q103_owner_decision.json \
PYTHONPATH=/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/REMONT_Q006_ISSUER \
python3 /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/REMONT_Q006_ISSUER/WORKER_RETURNS/ANVIL_P0_Q006_SAVED_ISSUER_SEAM_20261121_R1/proof_recorded_operation.py
```

The original SRC04 execution remains explicitly not run until controller checks
the candidate and private authority.

## Preserved boundaries

- no asked risk synthesized from recorded rows;
- no stored event/locator/Parquet mutation;
- no TEST_ONLY R03 path or new source scheme;
- no full compiler or second evaluator;
- original q103 data, raw SAV, protected refs, G5 and issue posts untouched.

Pins: #1084 `357a0fbf...`, #1205 `c5efdbdf...`, #1185 `3eee662d...`, q103
`4a3599065...`.
