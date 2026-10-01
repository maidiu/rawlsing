# PYAT C1-02 — WITNESS PAIRING-GROUND-TRUTH REACHABILITY REPAIR — R1

Status: ISSUED__NARROW_ACCEPTANCE_BLOCKER_REPAIR

**LAUNCH IN: OpenCode — Space Bunny Free**

Repository:
`maidiu/rawlsing`

Branch:
`agent/opencode-pyat-hq143-c1-02-witness-pairing-repair-r1`

Exact branch base:
`6e0f7b438089a542c9949b604cd55cbb3eaf8b2b`

Accepted C1-01 baseline:
`5fafb499d53dddadaf8a7b4fd46506e91a09d270`

Corrected C1-02 code-under-test previously reviewed:
`795bd0814980b06174119a766a3f3940a2842385`

Independent review return:
`c9ed2fe49d032b9313c3d24227a08fd9ca3aff89`

Blocking finding:
`C1-02-REVIEW-BLOCK-WITNESS-PAIR-001`

Read first:
- `WORKER_RETURNS/PYAT-C1-02-CORRECTION-INDEPENDENT-REVIEW-R1/05_FINAL_DISPOSITION.json`
- `WORKER_RETURNS/PYAT-C1-02-CORRECTION-INDEPENDENT-REVIEW-R1/03_OWNER_FIX_AND_REGRESSION_AUDIT.json`
- original C1-02 commission:
  `WORKER_RETURNS/PYAT-C1-02-HIGHER-ORDER-RECURSIVE-R1/00_COMMISSION.md`

## Governing adjudication

The independent review accepted the corrected C1-02 implementation everywhere except one narrow generalized witness-law defect.

The multi-conditioner `_verify_witness` path currently performs structural/hash/ref verification, but the per-conditioner pairing-ground-truth semantic checks:

- pairing subject ref matches the frozen subject preimage ref;
- pairing predicate-leaf ref matches the frozen producer leaf ref;
- pairing required semantic ref matches the subject semantic ref;
- pairing required exact value matches the subject exact value;

are indented after an unconditional `raise` inside the `if not match_found:` branch.

They are therefore unreachable on every successful verification path.

A malicious or corrupted pairing-ground-truth relation can be made internally hash-consistent by recomputing its pairing ref and enclosing witness ref while still lying about the relation between the unchanged subject/binding and producer leaf. The current verifier can accept that false semantic relation.

This is acceptance-blocking.

## Exact mission

Repair only:

`C1-02-REVIEW-BLOCK-WITNESS-PAIR-001`

Do not redesign C1-02.

Make the four per-conditioner pairing-ground-truth comparisons reachable on the successful multi-conditioner verification path.

Add a hostile court proving that a pairing-ground-truth relation which is:

- structurally valid;
- hash-consistent;
- freshly re-content-addressed;
- enclosed in a freshly re-content-addressed witness;
- paired with otherwise valid consumer binding, subject preimage and producer leaf;

but **semantically false** is rejected before evidence construction and before consumer invocation.

The hostile must not merely corrupt a hash or ref and then rely on the existing hash-integrity checks. It must specifically demonstrate semantic falsity behind internally valid recomputed identities.

## Required semantic hostiles

At least one hostile must mutate one of:
- `required_semantic_ref`
- `required_exact_value`

while recomputing:
- pairing-ground-truth ref/hash;
- witness identity/ref/hash;
- every directly dependent frozen identity needed to keep the supplied witness structurally self-consistent.

The actual consumer binding, subject preimage truth and producer leaf truth must remain unchanged.

Expected result:

`ConditionValueRelationMismatch`

before:
- possibility evidence construction;
- consumer invocation.

If naturally cheap, exercise both a false semantic-ref and false exact-value relation. One decisive hostile is sufficient if it proves the blocker exactly.

## Preserve accepted review findings

The independent reviewer already accepted:
- AT08–AT13 substantive corrected courts;
- AT10 underpowered-state non-trigger at this grain;
- AT11 exact-frontier coverage distinction without adaptive unvisited requirement;
- all three earlier owner fixes;
- C1-01 regression preservation;
- wider-regression attribution;
- execution provenance;
- authority ceiling.

Do not reopen or rewrite those findings unless this repair produces a counterexample.

## Write allowlist

You may edit only:

1. `rawlsing_next/pre553_analytical_composition.py`
2. `rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py`
3. optional `rawlsing_next/tests/c1_at08_at13_fixture.py` only if required to construct the hash-consistent false relation
4. `WORKER_RETURNS/PYAT-C1-02-WITNESS-PAIRING-REPAIR-R1/**`

Do not modify:
- the prior corrected C1-02 return directory;
- the independent review return directory;
- generic C1 packet files;
- any upstream empirical/discovery/recursive/consumer owner;
- HQ/control files.

## Test sequence

During development, run the smallest targeted hostile court first.

Before return, run the complete commissioned C1-02 six-file court:

`rawlsing_next/tests/test_pre553_analytical_composition.py`
`rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py`
`rawlsing_next/tests/test_pre553_empirical_query.py`
`rawlsing_next/tests/test_pre553_discovery_exact.py`
`rawlsing_next/tests/test_pre553_recursive_handoff.py`
`rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py`

Required result:
- no regression from the previously accepted 105/105 court;
- plus the new hostile(s), so the total should increase accordingly.

If the test count does not increase, explain why.

Also verify:
- all original 31 higher-order tests remain present;
- all 30 test names cited by the corrected matrix still exist;
- C1-01 legacy analytical court remains green.

A new broad 27-minute wider regression sweep is not required unless the repair changes more than the exact verifier/test terrain or produces evidence of wider breakage. The prior exact three-tree attribution is retained unless contradicted.

## Required return

Write only:

`WORKER_RETURNS/PYAT-C1-02-WITNESS-PAIRING-REPAIR-R1/**`

Required:
- `00_RETURN.md`
- `01_BLOCKER_REPRODUCTION.json`
- `02_REPAIR_AND_HOSTILE_AUDIT.json`
- `03_EXECUTION_RECEIPT.json`
- `04_FINAL_DISPOSITION.json`
- `FINAL_COURT.txt`

The return must state:
- exact pre-repair unreachable-control-flow defect;
- exact source lines/logic repaired;
- exact hostile construction;
- which semantic relation was false;
- which identities were recomputed to keep the hostile structurally valid;
- exact rejection point;
- evidence that evidence construction/consumer invocation did not occur.

## Allowed dispositions

- `PASS_BLOCKER_REPAIRED__NARROW_INDEPENDENT_REREVIEW_REQUIRED`
- `FAIL_BLOCKER_REPAIR`
- `COUNTEREXAMPLE_REQUIRES_C1_02_REOPEN`
- `EXISTING_OWNER_CHANGE_REQUIRED`
- `AUTHORITY_GAP`

Do not self-adopt.

## Absolute prohibitions

No raw survey files.
No Candidate A/B/C.
No measured P2X.
No real-source C11.
No C4.
No C1-03 implementation.
No new semantic/comparability/model authority.
No V3 actor/person implementation.
No modification of Kimi's preserved branch.
No modification of the prior corrected return or independent review artifacts.

## Git completion

When finished:
1. verify diff from `6e0f7b438089a542c9949b604cd55cbb3eaf8b2b` stays inside the allowlist;
2. commit all completed work;
3. push exactly this assigned branch;
4. report:
   - final SHA;
   - disposition;
   - terminal token;
   - changed files;
   - final test counts.

Terminal:

`C1_02_WITNESS_PAIRING_REPAIR_RETURNED__HQ_ADJUDICATION_REQUIRED`
