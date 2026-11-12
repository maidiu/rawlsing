# SOROK D01 Agent A relay — receipt-deletion and actual-owner verify

**Task:** `D01` — exact-reuse positive-development producer and sourcefree boundary.
**Programme:** #939 / PR #938 at `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Branch:** `codex/sorok-duel-d01-a-relay-d02-20261112-r1`; start `acfcb72f49102cd2fdc7d165b1d5a8e2b5b60f5d`.
**B return examined:** `0e0bb07ec8091fd34c6e47fff493a9ce39c9893d`; B code cut `141372a9095f901c48fc06d03301c4dda66befec`.
**A counterstrike code cut:** `a3ead75aad5a40a0c96224f8f747e9c48b6f085f`.
**D02 code cut:** `76547199c20f29f63c0e0e43b13a12cdecb3d47a`.
**Ceiling:** `SOURCEFREE_S2_CANDIDATE_PENDING_B`; no native science, actor/human rights, protected merge or independent acceptance.

## 1. B's valid findings and improvements — conceded

1. **B-D01-1 is real.** A's cold boundary checked row hashes/head/config but did not call `PsycheStore.verify()`. A chain-consistent rewrite of a non-head record was accepted and consumed. B's `verify()` call at the cold/live boundary and record-to-receipt binding are genuine improvements. I reproduced B's defect and preserve the repair.
2. **B-D01-2 is real enough.** A's claim that an identical actual-P2 event differential was impossible was too strong. The same-path, same-seed deterministic re-creation reproduces identical P2 event hashes; B's `test_d01_owner_differential.py` demonstrates a real owner-level changed-value differential. I accept it with B's stated boundary: it is a deterministic replay, not a live fork.
3. **B-D01-3 is real.** A's missing-config guard had no verified recovery even when the exact config was provable. B's anchor-proved recovery and empty-store recovery are useful. I did not find a legitimate pending-only state that should bypass the refusal.
4. **B-D01-4 is real at A's cut.** A's provenance anchor lived only in `d01_reuse.open_cold_owner`; a direct `P3Owner` reopen bypassed it. Moving the anchor into `P3Owner.__init__` is correct.
5. **B-D01-5 is a real validator gap.** A's fixed-key scanner did not reject unknown affirmative keys. B's exact response mode is a valid strengthening.
6. **B-D01-6 is correct.** A's pin table listed engine `engine.py`/`model_cycle.py` as if they were in `producer_identity()`; they are not part of `p3_owner._code_pins()`. The pin table in this relay corrects that.
7. **B's fsync and recovery work** are preserved. I did not revert or weaken the exact-code binding.

## 2. B's incomplete repair — new defect and evidence

**B's `verify()` record-to-receipt binding is one-way.** It proved every surviving record row appears in its operation receipt, but did not prove every receipt record appears in the rows. Therefore a record can be **deleted**, the remaining chain and head recomputed consistently, and the receipt left intact. B's `verify()` returns `True`; a later consumer sees fewer records.

Direct reproduction before the repair (current merged code):

```text
before: 2 records, head count 2
delete first row; rewrite second previous_chain/chain_hash and p3_meta head/count
PsycheStore.verify() -> True
head -> count 1
later records -> [private_check] only
```

The config anchor still passes because it uses the receipt's durable `psyche_after`; only the row chain changed. B's docs cover a record rewrite (B-D01-1) but not a chain-consistent deletion. This is a consequential retention defect, not a hash nit: the missing record is still in the operation receipt and the completed result.

**Repair implemented in `p3/state_store.py`:** `verify()` now compares the full canonical record list for each operation against the rows committed by that operation. A missing receipt record, an extra row, or a chain-consistent replacement refuses `JOURNAL_INTEGRITY:RECORD_RECEIPT_MISMATCH`. A focused test is `WORKER_RETURNS/SOROK-DUEL-D01-R1/tests/test_d01_a_relay_repairs.py`.

**Actual-owner closure:** `P3Owner.__init__` now calls `self.store.verify()` before the config anchor and closes the store on failure. B explicitly left this as a cost decision; I made the correctness call because the actual owner, not only the D01 loader, must refuse a chain-consistent deletion. The test constructs `P3Owner` directly on the tampered store and expects the refusal. Cost is one bounded full store scan per owner construction; measured D01/A relay suite 15 passed in 91.73s and P3 regression 77 passed/1 skipped in 55.29s, so no observed regression.

## 3. B's other statements: refuted, bounded or incomplete

- **Not refuted:** B's same-path differential is a legitimate actual-owner value proof; it is not a live fork. The limitation is stated, not hidden.
- **Not refuted:** B's exact response validator rejects unknown affirmative keys; I retain it. It still does not check the `rule` descriptor values, so a store-level response substitution with the exact key set remains a narrow attack surface; the P3 owner computes the response and the receipt binds it, so I did not spend this round on a scanner arms race.
- **Incomplete:** B's `verify()` receipt binding (above).
- **Incomplete:** B's anchor/pending boundary. A pending-only store with no completed operation cannot be anchored to a complete config; B refuses recovery, which is safe but leaves the exact candidate unproven. I did not invent a migration. This remains a documented hold.
- **Accepted boundary:** B's "full Byzantine state-root rewrite is outside this local consistency boundary" is correct. The new deletion test does not rewrite receipts/results and is inside the boundary.

## 4. Regressions, negative controls and cold receipts

Commands run from the worktree at `a3ead75a` / `76547199`:

```sh
python3 -B -m pytest -vv -p no:cacheprovider WORKER_RETURNS/SOROK-DUEL-D01-R1/tests/
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_state_store.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_rules.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_projections.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_goal_residuals.py
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DUEL-D02-R1/tests/
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_household.py \
  WORKER_RETURNS/SOROK-DUEL-C01-R1/test_c01_supporting_actor.py
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_p2_owner.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py
```

Observed:

| Suite | Result | Evidence |
|---|---|---|
| D01 all (A + B + relay test) | **15 passed in 91.73s** | `evidence/d01_a_relay_all_pytest.log` |
| P3 owner/store/rules/projections/goal-residual | **77 passed, 1 skipped in 55.29s** | `evidence/p3_a_relay_regression_pytest.log` |
| D02 selector + composition | **6 passed in 125.48s** | `SOROK-DUEL-D02-R1/evidence/d02_all_pytest.log` |
| B01 household + C01 supporting actor | **13 passed in 63.86s** | `SOROK-DUEL-D02-R1/evidence/composition_b01_c01_pytest.log` |
| P2 owner + P6 house | **13 passed in 147.75s** | `SOROK-DUEL-D02-R1/evidence/composition_p2_p6_pytest.log` |

The D01 relay test covers: non-head rewrite refusal (B), chain-consistent record/receipt divergence (B), live-owner terminal-consumer tamper refusal (B), config recovery/exact-byte restore (B), exact response claim keys (B), source severance (B), and the new chain-consistent **deletion** refusal (A).

## 5. Unfulfilled requirements

- D02 is only the dependency-independent read-only selector; B02 calendar/as-of is **NOT BUILT** and C01 is still under its own B counterstrike. D02 is marked `IN_PROGRESS_PREREQUISITE_HELD`, not complete.
- No D03/D04/D05, no parent-authored act/utterance, no dated household period, no multicycle duration, no P6/root-to-live, no J1/J2/J3/J4.
- No native CAN/ADP/Pyat, actor/human/source rights, C12 issuance, production or protected merge.
- Old-code P3 roots created at A/B cuts refuse under the current code pins. This is an exact hold; I did not weaken pins or rewrite old roots.
- Full P3 vertical matrix and full estate were not rerun. The selected suites above are the bounded evidence.

## 6. Exact source identities at this return

| Path | SHA-256 |
|---|---|
| `p3/p3_owner.py` | `81be18dae3c4c5d9d79f68ee7146be13055a24c4b63bb54019b8ce9d3931b44b` |
| `p3/state_store.py` | `fc878ce928d9aca305166bfd1b24f4f5c31923b9479f6d47ac4a0bd54402589a` |
| `p3/situated_context.py` (D02) | `f978c02ab002a6a55e3fa6f42aab9beaa11a7b1a4fc33975f93bc03f5aee6035` |
| `tests/test_d01_a_relay_repairs.py` | `f674d6cb04d7e440bcad6f4c9a79b148e051f1256a3c9aa9d67ab4bbe392052f` |
| B1 `bfirst.py` (unchanged) | `478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3` |

## 7. Strongest remaining attack surfaces

- **Pending-only config:** a store with a pending operation and no completed anchor; B refuses recovery; direct `P3Owner` with an existing tampered config can still choose future plans. I did not invent a migration. Attack this with an exact crash window and a safer candidate-proof design.
- **Exact response rule values:** the exact schema checks keys/hash but not that `rule` equals `response_rule`. A receipt-consistent substitution is narrowly possible at the store level. Decide whether D03 needs the value check or a stronger response provenance.
- **Full scan cost:** `P3Owner` now verifies the whole store on construction. Measure larger roots before using this in a tight loop; if too costly, propose a targeted committed-receipt digest without weakening deletion detection.
- **Byzantine rewrite:** receipts/results/records rewritten consistently remain outside the local anchor. Do not call the boundary authenticated.
- **B's record semantic check:** exact two-parent/ID/payload/mode assumptions are D01-specific; D04 must add an additive selector rather than silently widening this one.

## 8. Challenge to the same B

Break the deletion repair or the actual-owner closure with a **non-Byzantine** state that is still legitimate: a pending-only crash with a provable exact config, a receipt-consistent operation with zero/multiple records, or a store construction where full verify is unacceptable but a targeted anchor can still prove the exact config and record set. If the full verify is too costly, propose a targeted receipt/record digest that detects deletion without a full scan. Then attack the D02 selector's material/actor-access split: make objective household availability leak into Nadia's admissible options without actor position/perception, or make an observed relation appear eligible after it is no longer co-present.
