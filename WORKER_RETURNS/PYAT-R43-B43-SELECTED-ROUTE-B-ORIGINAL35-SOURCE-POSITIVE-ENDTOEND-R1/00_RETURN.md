# B43 - selected Route B original-source production feeder and truthful source-positive status

**Role:** bounded source-to-product implementation integrator. NOT HQ, not source/scientific
issuer, not N11 adopter. **No current source+host+purpose or U/E_pre grant exists in the
evidence, so B43 does NOT fabricate measured original results.** It delivers the complete
executable feeder, the WG0L provenance repairs, the independent all35 frontier, and the
exact competent-owner decision docket. N11 stays NOT_READY; original measured occupancy
stays 0.

Branch `agent/rabochii-pyat-r43-b43-selected-b-original35-real-source-production-r1` from
exact startup `556dd7e2bf67e2bc0b1772d18880ef0dfaa819e3` (HEAD verified). J42's live
worktree was not touched; U43 has not returned.

## What actually runs

`python3 -m b43.cli assemble`:
- verifies the declared estate matrix and the WG0P4 fixture frontier at exact Git preimages;
- freezes the all35 source-execution frontier (35 waves, 0 executed, expected operation
  count null WITH CAUSE, no raw source permitted);
- proves the real selected-B owner call contract
  (`rawlsing_next.pre553_route_b_production.execute_route_b_production`);
- runs the issuer-bound admission control;
- re-runs the returned A42 v2 assessor with the B43 receipt and emits v3 artifacts;
- writes the source-owner decision docket (35 rows) and the A42 source-grade delta.

`python3 -m b43.cli replay` reproduces the artifacts deterministically.

## WG0L's three REDs closed in a new admission adapter

WG0L `bec9a128922e4e431ce2ed862aa7802c902813ed` proved that a copied plan can change
`BoundSpec.source_edition` or `native_item_ids` while the registered contract is unchanged
and still serve `SUPPORTED`, and a changed `release_tag` reaches native I03 as a `KeyError`.

`b43/admission.py` compares the plan's consumed descriptor fields against an
**issuer-controlled** contract before any native execution and refuses early with typed
`B43AdmissionDenied` codes:
`B43_ADMISSION_BOUND_SOURCE_EDITION_MISMATCH`,
`B43_ADMISSION_BOUND_NATIVE_ITEM_IDS_MISMATCH`,
`B43_ADMISSION_BOUND_RELEASE_TAG_MISMATCH` / `UNBOUND_RELEASE_TAG`,
`B43_ADMISSION_UNREGISTERED_OPERATION`.
No forged descriptor reaches I03/Batch or a consumer.

## Grant gate (no fabricated measured output)

`b43/feeder.py` refuses to proceed without an exact current grant covering source + host +
purpose + scientific operation + edition. Without it the result is
`SOURCE_EXECUTION_PENDING_OWNER` with `measured_output = None` and
`raw_source_read = False`. `guard_raw_source_read` raises on any raw SAV/DTA path without a
covering grant. A granted-but-streamless call returns `SOURCE_STREAM_NOT_SUPPLIED`, never a
value. A granted call with a stream invokes the real selected-B owner.

## Frozen all35 frontier and decision docket

- 35 declared waves; every wave `PENDING_COMPETENT_SOURCE_HOST_PURPOSE_AND_U_E_PRE`,
  `raw_source_permitted = false`, `executed_original_operations = 0`.
- `expected_original_operations = null` with cause: U43's prospective frontier has not
  returned and no competent U/E_pre was issued.
- WG0P4 fixture frontier recorded as **3 PRODUCED / 16 HELD / 6 INADMISSIBLE**, 5 native
  items, grade `SOURCEFREE_FIXTURE_METHOD_PROOF__NOT_ORIGINAL` (does not count toward
  original occupancy).
- `b43_source_owner_decision_docket.json`: 35 rows of the exact competent decisions needed
  per wave plus the global C11/U43/issuer prerequisites.

## A42 re-run (truthful)

- `b43_a42_v2_estate_acceptance_manifest.json`, `b43_a42_v2_f1_f8_acceptance_matrix.json`,
  `b43_a42_v2_final_maturity_adjudication.md` re-generated from A42 `843175b0...`.
- **original measured occupancy 0 / 1,890; no new original occupied cells; N11_NOT_READY.**
- `b43_a42_source_grade_delta.json` shows `new_original_measured_cells = 0` and
  `source_positive_state = SOURCE_EXECUTION_PENDING_OWNER`.

## Proof

- 16 native tests pass; cold replay byte-stable.
- Shared proof gate: four edges `baseline PASS -> TARGET_ASSERTION_FAILED -> restored`:
  forged edition, forged native item ids, forged release tag, and all35 no-drop.
- Controls: no-grant pending, revoked/expired/wrong-purpose/wrong-edition grant refusal,
  raw-source guard, no fabricated streamless value, real owner call shape.

## Explicit limits

- No raw SAV/DTA was read; no respondent-level material is in this return.
- U43 frontier absent; J42 returned locally but **not published**, so not ingested.
- The historical EE-P2R6M four-question C11 snapshot remains an **optional** bounded parity
  oracle and was not rehydrated (no current source grant and no material consumer change
  required it). `OPTIONAL_NOT_RUN`.
- No source/model/FF/F6/EE12/actor/N11/N12 right is issued.
