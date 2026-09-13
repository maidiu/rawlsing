# E07 — governed return

Status: **BLOCKED — independent degraded qualification found a replay/provenance collision in the exact D07 bounded-evidence runtime; no repair authority exercised**

Terminal:

`PREV3_BOUNDED_EVIDENCE_INDEPENDENT_DEGRADED_QUALIFICATION_R1__BLOCKED__REPLAY_PROVENANCE_COLLISION`

Commission: `PREV3_BOUNDED_EVIDENCE_INDEPENDENT_DEGRADED_QUALIFICATION_R1_ONLY`

Branch: `agent/rabochii-prev3-w3-e07-bounded-evidence-independent-qualification-r1`

Commission tip: `b6fb9daa95ff82984ac49728e3b50f1164035464`

Inherited D07 return head: `12e83fa226cb200cc4de38812d89c5c3b71ea42e`

HQ fan-in authority: `018ef13413b24a3bc131fd0c769d37b832854135`

Library/external evidence: `NO`.

## Clean rerun of exact D07 identities

The exact D07 production/test files were reconstructed in an isolated work directory and Git-blob verified before execution:

- `rawlsing_next/objective_consumer_bounded_evidence.py` — `9738399d5e454808235a91b10a2d473cdd851d97`
- `rawlsing_next/tests/d07_bounded_loss_harness.py` — `74a393f11d986e89a21d192495dc1bf985ace0e4`
- `rawlsing_next/tests/test_objective_consumer_bounded_evidence_d07.py` — `4e4c47e006f29137deeba05499a9eab2c03396e2`

Clean-process executions:

1. `python -m pytest -q rawlsing_next/tests/test_objective_consumer_bounded_evidence_d07.py`
   - observed: `3 passed in 0.06s`
2. `python rawlsing_next/tests/d07_bounded_loss_harness.py`
   - observed: `PASS`, `12 PASS / 0 FAIL`

The inherited self-court therefore reproduces exactly.

## Independent degraded/loss qualification

Independent executable court: `02_INDEPENDENT_HOSTILE_QUALIFICATION.py`.

Observed: **5 PASS / 2 FAIL / 7 total**, process exit `1`.

The two failures are one exact replay/provenance blocker expressed at both currently applicable policies:

- `E07-H02` / OC01: change only the unavailable required input's `omission_reason` from `RISK_SET_UNAVAILABLE` to `SOURCE_SCOPE_UNAVAILABLE`. The resulting receipts have the **same `receipt_hash` and identical `as_dict()` serialization**.
- `E07-H03` / OC02: change only the selected empirical input's exact `authority_refs` from `AUTH-1` to `AUTH-2`. The resulting receipts again have the **same `receipt_hash` and identical `as_dict()` serialization**.

The D07 `Receipt`/receipt-hash projection carries selected producer refs, missing/omitted IDs, refusal strings, and relation-authority refs, but it does not carry the unavailable input's `omission_reason` or ordinary selected-input `authority_refs`. Consequently two materially different evidence/provenance states are replay-indistinguishable.

This violates the adopted C08/HQ law that omissions/refusals and exact producer/**authority** dependencies remain provenance-bearing and replayable. It also defeats tamper-sensitive replay at OC02 because changing the exact governing input-authority ref is invisible to the receipt identity.

## Other independently exercised boundaries

At the tested exact D07 grain:

- source-local evidence does not satisfy a population claim — PASS;
- explicit renormalization request refuses — PASS;
- all-unavailable is not positive completion — PASS;
- unrelated lawful selected evidence remains visible when a required local premise is lost — PASS;
- OC03/OC04/OC05 remain explicit `NOT_YET_APPLICABLE` and cannot be synthetically executed — PASS.

The clean D07 rerun additionally reproduced its missing-as-unavailable, missing relation-authority/backfill, separately typed non-empirical model-prior, and no-renormalization cases.

## Exact blocker and disposition

Smallest proved blocker:

`E07_BLOCKER__D07_RECEIPT_REPLAY_COLLISION__OMISSION_REASON_AND_SELECTED_INPUT_AUTHORITY_REFS_NOT_PROVENANCE_BEARING`

No production repair is authorized by this commission, so E07 does not alter the D07 runtime or either current consumer seam.

`GATE-DEGRADED-QUALIFIED = NOT_ISSUED`

Required successor is a competent repair/requalification that makes omission/refusal reason and exact selected-input authority dependencies receipt-bearing/hash-bearing, then reruns D07 plus the independent E07 court. No OC03/OC04/OC05 promotion is implied.

## Return artifacts / exact test identities

- `00_RETURN.md`
- `01_INDEPENDENT_DEGRADED_LOSS_MATRIX.tsv`
- `02_INDEPENDENT_HOSTILE_QUALIFICATION.py`
- `03_TEST_RESULTS.txt`

Independent court source SHA-256 before commit: `d80e5ded33e7bbfc281d23cc8961054ce726ee9fff736292a7654a7c94fe210b`.

Successor gate requested by commission: `GATE-DEGRADED-QUALIFIED`; disposition: **withheld on exact blocker above**.
