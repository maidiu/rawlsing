# SOROK #1008 — Agent A final counter, shared A→B→A lineage

Disposition: C04_FIRST_CONSUMER_CUSTODY_REPAIR_CANDIDATE / ISOLATED_PROBE_PASS / FULL_J1_P6_NOT_RUN / G2_PARENT_VOLITION_HELD / G5_NOT_STARTED.

This is one final descendant of the same sourcefree C03/C04 implementation. It is NOT G5 acceptance or a native scientific grant.

## 1. Immutable provenance and changed files

- Original contract: issue #1008; frozen C03/C04 and C01/C02/B01–B05/E01 task packets at 227ce149fc7864c83c179a7d3ecaef2b92c5bdab.
- A initial author HEAD: 0ba01215936df0b28027afe6f1596e6e610dacf7, draft PR #1015.
- B exact frozen HEAD: fa91ccc09fea4ef0b646f437c6d2b05aed04af2a, draft PR #1017. Verified to be a six-commit fast-forward descendant of A.
- Final A branch: agent/sorok-c03-c04-a-final-counter-20261113-r1, created directly from B's immutable HEAD. Final immutable HEAD is the branch/PR SHA as finally reverified after this documentary commit.
- Scope: existing WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_speech.py plus newly authorized narrow tests and documentation under WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/.
- No changes to C03 prospectives, B02/B04/B05, world writer, D02/D03/P3, J1, MCR law, #939 fleet or protected PRE-MAIN. No simultaneous shared-file writer was asserted.

## 2. Governing contract reconstructed

SOROK's original PROGRAMMA, canonical 00_READ_ME_FIRST and PROGRAMMA_SOROK/00_PROGRAMMA_SOROK front door; MCR-lite at protected 6a5c12f04323d74001f9632063ec907f4fc4468e; frozen original task register at 227ce149fc7864c83c179a7d3ecaef2b92c5bdab; provisional UM-SOROK R1/R2 at f5c43c80675f2556e1287bf55d25052d11e8746e (interpretive only). Original literal SOROK_PRODUCT_CONTROL_ROOM/READ_FIRST.md is missing; the existing first-read is 00_READ_ME_FIRST.md.

G1 requires independent parent identity/history, parent/household money and actor-access boundaries. G2 requires actual C03 mother-owned choice/attempt/refusal through the competent owner, separate C04 public speech, actual P6 Nadia-qualified hearing and D03 uptake. G3 actual hostile contrasts; G4 cold/replay/conservation; G5 separate nonauthor receiving. Feasibility never entails willingness; sourcefree tests never issue native psychological or human authority.

Informed by PR #996 source derivation (return fb061dec16c8386b9caa1b5ea75ec7645aff88a7, tested code cut c724d1a89626f3e177acd004c0be20029dc7ade4), actual C01/C02 owner, J1 ABI/adapter, B02/B04/B05, P6/D03, and BP4 world make_event blob 5c4a309d376ce2bedce6a8a7e4f09768131f4d46.

## 3. B's valid victories — preserved

B correctly demonstrated that A compared a stored event hash with an event-reported hash, but failed to recompute the original BP4 content hash and event ID. Changing location, summary, observable or sequence with stale ID/hash could fool the earlier per-field checks and contaminate outward projection. BP4 source confirms make_event uses event_id = prefix + digest(base) and hash = digest(event). B's _verify_world_event_seal remains unmodified and continues to run at parent replay/self-read and both child readers. B's hostile tests are preserved.

I found no demonstrated false B accusation. B did NOT claim full repo execution. Its isolated probe is meaningful only at its explicitly bounded grade; no authentic BP4 fork/migration counterexample has been demonstrated that would justify weakening its seal.

## 4. Independently discovered consequential B-era defects

**FINAL-01: confused two-key lookup.** _utterance_by_event_or_operation used OR for event_id and operation_id. When one selector was correct and the other nonexistent, it silently selected a speech occurrence that the caller had explicitly not selected. read_child_experience then overwrote the caller's event_id with the matched body event_id. P6 child_speech_experience also accepts two selectors; the event self-hash seal cannot detect this semantic misbinding because the chosen event itself is genuine.

**FINAL-02: direct child perception promotion/erasure.** B added event seals to read_child_uptake, but the direct reader still did not check its stored admission-time child_perception_channel or embedded C04 utterance receipt against actual C12 parent/child perceptions. A historically admitted child speech receipt missing at read time returned NOT_PERCEIVED instead of a severance refusal. A newly forged child speech perception for a historically NOT_PERCEIVED utterance could return PERCEIVED. Missing parent own-speech receipt, duplicated child receipts and inconsistent episode root/branch likewise escaped direct child receipt checks.

These were not resolved merely because the higher read_child_experience path sometimes caught inconsistencies: read_child_uptake is directly callable and is itself part of the intended first-consumer custody.

## 5. Actual fixes on top of B, not replacement

- Require BOTH selectors to identify the same C12 utterance if both supplied; reject malformed or empty selectors. Single valid selectors still work.
- In direct read_child_uptake, bind current root/branch, parent/child identity, event ID/hash, speaker, decision and operation to the stored C04 admission episode and its embedded exact C04 receipt. Verify speech text, event decision_id, original utterance_source, clock and B's complete BP4 event seal.
- Require exactly one parent own_speech C12 receipt and zero or one child speech receipt consistent with the **admission-time** channel. Fail closed on missing originally admitted hearing, a forged later hearing, duplicated perceptions, or inconsistent embedded receipt. Historical NOT_PERCEIVED stays NOT_PERCEIVED when authentic. Current physical co-presence never rewrites historical hearing.
- No event writer, new ledger, speculative mother choice, persona store, or retrospective memory authority introduced. C03 sourcefree alternatives remain exactly as A originally wrote; B's stronger seal is retained.

Full-repo test module committed at WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_first_consumer_identity.py. Tests target the real J1 fixture and normal P6: matching event/operation, unknown/mismatched and cross-spliced selector, genuine unheard, missing witnessed child receipt, forged child receipt, missing parent receipt, duplicated receipt, forged episode branch and altered embedded hearing receipt, restoration after injected mutations. These tests remain NOT_RUN against the complete checkout in this environment.

## 6. Actual isolated negative evidence, exact commands

A separately executed local synthetic source-equivalent probe (NOT imported project code):
  python /mnt/data/c04_agent_a_final_isolated_probe.py
Script SHA-256: a3f4d38dce5fc7a623fece2871149d2f2b99b54825c159a3ed0ca0ef1d609911
Observed: EXIT=0, elapsed 1.29s, max RSS 96016 KB.
Two B-era OR lookup acceptances refused under the new conjunctive policy. Missing witnessed receipt, forged unheard receipt, missing parent receipt and duplicate receipt refused. Original witnessed, unheard and matching lookup preserved. Raw stdout/economics in evidence/ISOLATED_C04_SELECTOR_RECEIPT_20261113.txt.

This probe is **not an actual full-repo RED→GREEN**; it models the selected algorithms and fake C12 store. No J1/P6/P3/D03 runtime pass, cold fork, B05 rent/currency lock proof, full-system resource measurements, provider charges or independent receiving established. Private repository not locally mounted and git ls-remote failed DNS; GitHub connector provided source inspection and branch writes. Full project tests to execute in a complete exact checkout:

    python -m pytest -q WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_first_consumer_identity.py
    python -m pytest -q WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/test_c04_custody.py
    python -m pytest -q WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/test_c03_prospectives.py
    python -m pytest -q WORKER_RETURNS/SOROK-E01-J1-995-R1/test_j1_three_head_join.py
    python -m pytest -q WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/A_RETURN_R3/test_c03_c04_consumer.py

The 221 PASS / 1 SKIP from PR #996 is an inherited author report, NOT rerun by A or B.

## 7. Self-adversarial limitations and rejected approaches

- Stronger receipt checking could fail closed on a genuinely owner-migrated cold/fork record. Neither A nor B has tested actual cold/fork in this host; a genuine source owner must demonstrate any legitimate reidentification before introducing a precise exception. A/B original event/branch/alias fidelity is preserved.
- Sourcefree C04 legacy writer still accepts caller-supplied public text and hidden reason. An as_actor=parent_id parameter is not an authenticated actor session principal. New seals prove event/receipt coherence, not independently produced speech.
- C03 old caller-directed purchase rule remains test-only and experimental; C03 alternative reader is a menu, not mother-owned selection. G2 ACTUAL_PARENT_SELECTOR_AND_LANGUAGE remains HOLD. I considered hard-coded preference priorities and refused to manufacture a dominant psychological motive.
- These are read-side repairs, so they do not authorize P2/B04 double-spend/rent/writer changes; all claimed no-duplication/cold equivalence remain TEST_REQUIRED, not PASS.
- Self-hashes cannot prevent privileged coherent rewriting of event, episode and C12 evidence; that is source custody and append-owner authority, not a local hash-check promise.

## 8. Full exact G1–G5

| Gate | Final A status |
|---|---|
| G1 mother/person/world | PARTIAL_SOURCE_GROUNDED |
| G2 mother-selected/performed act, expression, P6/D03 | HOLD_PARENT_SELECTOR_AND_LANGUAGE_OWNER |
| G3 hostile first-consumer | ISOLATED_NEGATIVE_PASS; ACTUAL_J1_P6_TESTS_NOT_RUN |
| G4 conservation/cold/economics | SOURCE_DIFF_ONLY; COLD_RUNTIME_NOT_RUN; PROBE_RSS_ONLY |
| G5 independent nonauthor receiving | NOT_STARTED |

Engineering: SOURCEFREE_C04_REPAIR_CANDIDATE; scientific: NATIVE_RULE_A_T_NOCHANGE_MEMORY_HELD; authority: NO_NEW_PARENT_SOURCE_OR_HUMAN_GRANT. No protected merge. No #939 fleet restart.

Strongest next attack: Run the complete committed and inherited J1/P6 suites and true cold fork with exact source cut; demonstrate whether a legitimate historical branch/alias or receipt behaves differently, repair only that actual causal defect. Then address the real missing G2 source-owned mother activity/selection and independent expression under same material affordances and different constituted histories, without fabricating new volition. One further exchange only if a reproduced material contract breach warrants it.

A FINAL STOP. G5 remains separate.
