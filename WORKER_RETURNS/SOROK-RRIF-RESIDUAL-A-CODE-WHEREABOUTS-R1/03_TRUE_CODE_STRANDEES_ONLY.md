# TRUE CODE STRANDEES ONLY — 18 branch records in 9 material families

Definition used here: material source code that is **not** present in current PREMAIN, **not**
proved replaced by an accepted scoped cut, and **not** carried/executed by a later worker branch.
Documentation, source atlases, test-only review evidence and predecessor cuts are excluded.

These are code-location findings, not authority verdicts. Nothing here authorizes a new person,
world, native rule, merge, or PREMAIN change.

## Priority 1 — product-relevant writer/transport/custody code

### S1. Sorok C0R3 two-owner transport and C10 receiver

- Branch: `agent/rabochii-sorok-20261019-c0r3-c0x-endtoend-transport-repair-r1`
  (`SOROK294-007`, HIGH, tip `a0f7ab5ff9323a1db8a4c6c3b365283b0969de46`).
- Material code: `candidate/upstream/c0p_two_contract_port.py`,
  `candidate/c0x_world_receiver.py`, `product/nonparent.py`, `product/scenario.py`.
- Functions: `TwoContractReceipt`, `TwoContractPort.select`, `_source_value_refs`,
  `consume_nonparent`, `consume_conception_proposals`, `_world_receipt`,
  `_possibility_receipt`, `_require_snapshot`.
- Why stranded: C0X row 6 is the earlier RED/predecessor (its `c0p_stage_runtime.py` utility is
  carried into Pyat C0P/C0R2), but the C0R3 port/receiver itself is not in R2, I1, F0, RA-D,
  current PREMAIN, or any later Sorok consumer found.
- Owner question: is this the intended Sorok C0/C10 transport, or retired?
- Evidence: exact C0R3 blob `4bb56a5143...`; C0X stage utility `4c86b911...` appears in
  C0P/C0R2.

### S2. OUT14 version/state multiwriter integrity repair

- Branch: `agent/rabochii-sorok-v2-hq322-out14-multiwriter-integrity-repair-r1`
  (`SOROK294-089`, HIGH, tip `a77f0f8e45ee...`).
- Material code: OUT12 candidate `multiwriter_journal.py` plus
  `test_out14_integrity.py`; version/state sealing, typed unreadable-version refusal,
  acknowledged-ledger prefix preservation, CAS/lock races, SIGKILL/exit separation.
- Why stranded: OUT12 `c2fb389300b8...` is the executed predecessor. OUT14 is implemented but
  its own new court was **collection ERROR / NOT_RUN** (`ModuleNotFoundError: outbox_prototype`),
  and no later branch carries it. It is not an accepted repair.
- Do not claim OUT14 green. The 28/28 SR outbox execution below is separate code.

### S3. SR occurrence/outbox execution candidate

- Branch: `agent/rabochii-sorok-r3-hq298-sr-outbox-execution-r1`
  (`SOROK294-053`, HIGH, tip `8da45605c267...`).
- Material code: `outbox_prototype.py`, binding occurrence/outbox execution path, 28-case
  falsifier matrix.
- Why stranded: executed **28/28 PASS** in its own return and preserves distinct
  occurrence/emission/delivery/perception states, but is not carried by OUT12/OUT14, R2, I1, F0,
  RA-D or current PREMAIN.
- Relation: do not merge with OUT14; the writer/CAS concerns overlap but the code is different.

### S4. OC6 custody input-contract repair

- Branch: `agent/rabochii-sorok-r3-hq313-oc6-native-input-contract-repair-r1`
  (`SOROK294-069`, MEDIUM, tip `873ce1c749fb...`).
- Material code: repair of `repro/custody_protocol.py` / `repro/adjudicate.py` entrypoints:
  `_normalized_duplicate_aliases`, `_well_formed_allowed`, bounded `_CONFUSABLE_FOLD` (30
  homoglyphs), typed signature/role/holder checks, `validate_capsule_fields`.
- Why stranded: OC6 closes **47 of 49** new OC5E REDs and **7 of 7** OC5 predictions
  (601 PASS / 21 RED at author grain), but the later OC5 branch used the older OC4 blob
  `af2b7e943018...` and preserved 49 REDs. OC6's repair is not in OC5, R2, current PREMAIN, or
  any later branch found.
- This is the highest-value missed custody repair in the 97. It is TEST_ONLY and still has
  two malformed-input residuals and the external-anchor HOLD.

### S5. C07P cross-process custody journal

- Branch: `agent/rabochii-sorok-r3-hq317-c07p-crossprocess-custody-r1`
  (`SOROK294-073`, HIGH, tip `805d0a071db7...`).
- Material code: `repro/c07_journal.py`, public-API replay, temp-fsync-rename-fsync journal,
  real Process A/B handoff, real SIGKILL crash points.
- Why stranded: the branch reports **30/30** and a genuine fresh-interpreter restore, plus typed
  `C07_DEPENDENCY_TS` / `C07_DEPENDENCY_REVOKE` holds and the explicit whole-journal rollback
  ceiling. No later carrier or product consumer found.
- It depends on OC6's blob `4c185c18...`; do not assert a production custody anchor.

### S6. Pyat C0P / C0R2 generic native port

- Branch: `agent/rabochii-sorok-v2-hq323-c0r2-git-backed-repair-r1`
  (`SOROK294-090`, HIGH, tip `55d2daa4bab4...`).
- Material code: `repro/c0p_two_contract_port.py` final facade, `WorldReceipt` and
  `PossibilityReceipt` two-contract envelopes, imported-runtime resolution, CAS/stale-version
  repair.
- Why stranded: C0R2 reports **50/50** after repair and **47/50 + 3 RED** baseline, but it is a
  Pyat native-port test candidate. C0P row 55 is its predecessor. No Sorok product consumer
  found.
- Do not call this Sorok product adoption or a Pyat semantic change.

## Priority 2 — developmental/native experiments

### S7. V2 B-first final developmental code

- `agent/rabochii-sorok-v2-hq329-b3-coupled-interpretation-prototype-r1`
  (`SOROK294-097`, HIGH, `47b46a85b9eb...`): `developmental_loop.py`, `integration.py`,
  `process_b3.py`, `custody.py`, `mutation_audit_b3.py`; B2-fixed x M2 six-stage loop.
- `agent/rabochii-sorok-v2-hq330-m4-m2-source-preimage-repair-r1`
  (`SOROK294-098`, LOW, `858bc2d91b1d...`): M4/M2 source-preimage repair.
- `agent/experimental-sorok-m2-preimage-custody-r1`
  (`SOROK294-238`, HIGH, `e8f375e9feae...`): `m2_patch/kernel.py` and relation-preimage probe,
  91 PASS cited, three residual relation-readset REDs preserved.
- Why stranded: B1/P1/B2/B2R1/M1/M2 are predecessors or are consumed inside this lineage, but
  the final B3/M4/experimental-M2 code has no later carrier and no product consumer. The
  experimental M2 is an authoritative later variant of M2 but is not the same as M2R3/M2R4.

### S8. Onecall C0R scheduler (worker-only carrier exists; no production consumer)

- Final code: `agent/userdirect-sorok-20261018-onecall-c0r-authority-causality-repair-r1`
  (`SOROK294-252`, HIGH, `98fdbdf0794d...`), `onecall_c0.py` (blob `76bd3a6e...`).
- The C0RI branch `5abd3c5d243c...` (`SOROK294-253`, HIGH) is an independent post-author court
  and contains/executes the repaired scheduler, so the exact code is **not** lost. C0 row 76 and
  C0F row 77 are predecessors.
- Why it still needs an owner: C0RI is a test court, not a production consumer. No R2/I1/F0/
  RA-D/PREMAIN consumer was found.
- This is listed separately from strict strandees because a later worker branch does carry the
  code.

## Priority 3 — research/experiment code with no product carrier

### S9. CLR causal courts

- `agent/rabochii-sorok-20261018-clr2-ownerlicensed-publication-r1`
  (`SOROK294-003`, MEDIUM, `a1c5b1b0...`): `court.py` (blob `6415054c...`),
  `world_intersection.py`, `run_research.py`.
- `agent/rabochii-sorok-20261018-clr3-recursive-canon-causal-court-r1`
  (`SOROK294-004`, MEDIUM, `4076dcc7...`): `recursive_court.py` plus preserved CLR2 court.
- Functions: `intervene`, `add`, `behavior`, `rehash`, `replace_event`, `threshold_variant`,
  `FutureChildPartitionGuard.assert_clean`, recursive formation/canon checks.
- No later carrier. Research/science only; the CLR2 and CLR3 shared court blob is not proof of
  two independent runtime capabilities.

### S10. RFA-06C2 renderer screen

- Branch: `agent/rabochii-sorok-r15-rfa06c2-quote-smoke-gate-repair-r1`
  (`SOROK294-046`, MEDIUM, `06e5cadac551...`).
- Material code: `anthropic_cross_model_screen_r2/quote_invariant.py`,
  `referent_admission.py`, `smoke_custody.py`, plus the final screen/custody harness.
- RFA-06C row 28 is its predecessor. No later carrier; it is an offline/API experimental
  renderer-feasibility screen, not a Sorok product runtime.

### S11. Final R3 causal/genealogy courts

| Record | Bridge | Priority | Final material code | Why no carrier |
|---|---|---|---|---|
| K3/K5 world-conditioned causal court | `SOROK294-047` | HIGH | causal-cell predicates and sourcefree court | final executed court; no later branch |
| SM owner-effect stub/court | `SOROK294-052` | MEDIUM | `owner_effect_stub_TEST_ONLY.py` | unique owner-effect test stub |
| G12 direct SGI1 generalization | `SOROK294-054` | MEDIUM | G12/SGI1 heldout and 57-predicate court | consumes SGI1; no later carrier |
| Behavioral assay R2 reconstruction | `SOROK294-055` | MEDIUM | `assay/experiment.py` + frozen LAB2 protocol | final assay; no product consumer |
| MS3 serial provenance repair | `SOROK294-075` | HIGH | `candidate/ms1_serial.py`, `ms3_native_custody.py` | 169/171 + 47 author; MS4 still required |
| G13/K11 sourcefree lab repair | `SOROK294-081` | MEDIUM | K11 lab mechanism and `finish_packet.py` | final K11 lab court |

These are genuine test-only science/engineering evidence. They should not be converted into a
new person/world build. They need an owner decision only if the relevant science lane is resumed.

## Strandee summary

- 18 strict branch records in nine material families (S2 and S3 are two subitems of the same
  OUT/writer family). S8 is the separate onecall worker-only carrier and is not counted in the 18.
- 9 HIGH, 8 MEDIUM, 1 LOW_ENTRYPOINT_ONLY at strict branch-record level.
- The largest product-relevant unfinished items are C0R3, OUT14/SR, OC6/C07P and C0R2.
- The largest research-only items are CLR, RFA-06C2, K3/K5, G12 and MS3.
- All are sourcefree/test-only unless explicitly described otherwise; none is native authority,
  none is current PREMAIN, and none is an adopted repair.
