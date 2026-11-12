# SOROK D01 Agent B handoff — durable record custody and exact-owner reuse

**Task:** `D01` — Exact-reuse positive-development producer selection and sourcefree native-rule boundary.
**Programme:** #939 / PR #938 at `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Opponent frozen artifact:** A at `82d310b4e09774e04f883fe7386c2f53cb2ac23e` (`codex/sorok-duel-d01-a-20261112-r1`).
**Author branch:** `codex/sorok-duel-d01-b-20261112-r1`.
**Protected base:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.
**B code cut:** `141372a9095f901c48fc06d03301c4dda66befec`.
**Final artifact:** the branch HEAD commit containing this handoff and the B impact records. No remote or protected push was made.
**Ceiling:** `SOURCEFREE_S2_CANDIDATE_PENDING_A`; no independent receiving, native science, actor/human authority or protected merge is claimed.

## 0. Independent reconstruction before reading A

Performed from the five frozen programme sources plus the #911 crosswalk before opening A's handoff or diff.

D01 must:

- select an **existing** positive-development producer at its actual current code, not invent a rule, owner, store or scheduler. The available producer is `p3.p3_owner.P3Owner` composed over `p3.state_store.PsycheStore`, with the frozen B1-derived `p3.test_rules` formation rule (`TEST_ONLY_P3_B1_SCOPED_MEDIATOR_CREATE`) and the actual `P2Owner`/S47 world;
- prove that **one admitted sourcefree record** with the exact current owner/source/root/actor/branch identity survives durably, and that a **later actual P3 consumer** reads it through the existing rule/readset path with a scoped actor output;
- refuse a **test interpreter or narrative-only memory** presented as a CAN/ADP durable issue, and refuse malformed root/branch/record identity;
- make **cold no-record** change or refuse the same-root computation, and make **source severance** refuse or change it, with exact restoration;
- remain `SOURCEFREE_S2_ONLY`: no native CAN/ADP/Pyat, no production, no actor/human rights, no protected merge.

The terminal consumer is the actual later `P3Owner.realize` / `test_rules.evaluate_event` response and its readset/actor projection, not a narrative report. The relevant existing code is `p3_owner._effect` → `PsycheStore.query`/`commit_effects` → `test_rules.evaluate_event`, with `P2Owner` remaining the sole world writer and B1 loaded read-only. D01 does not require B01+, P6, a CG-A bridge, or any of #915/#917/#924/#928; those are unmerged and were not adopted. The full Library conceptual/operational sources remain NOT_INSPECTED locally; no contents are asserted from them.

## 1. Exact artifact and provenance

Changed implementation paths and exact SHA-256 at the B code cut:

| Path | SHA-256 |
|---|---|
| `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/p3_owner.py` | `64000995182bfe3232576773eac0cf6c88fd3846e133303615b7f6c04068b458` |
| `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/state_store.py` | `d5bba50bfa7d2724b21a6b912f31179b588e69db41a9defa4f3d91b1c2ad416e` |
| `WORKER_RETURNS/SOROK-DUEL-D01-R1/d01_reuse.py` | `5700063d8d8d6349f1cca8e5dd64e684672540759dd9cb47eaaf710b28859c1f` |
| `WORKER_RETURNS/SOROK-DUEL-D01-R1/tests/test_d01_owner_differential.py` | `12b956978b3c79aff1253569ea9c0492e40041de4ce66e5cc83606949e6db136` |
| `WORKER_RETURNS/SOROK-DUEL-D01-R1/tests/test_d01_retention_repairs.py` | `19bcf830a29f3c0991df20855997dda1523d2b7cf4f881ff70542f08467a8328` |
| `p3/test_rules.py` (unchanged) | `27272cd43c26b6aa114ee65c97ca07eb56accecbd440841c29696b98e203b4b4` |
| `p3/projections.py` (unchanged) | `ca405dda778191537ce38b0b63ff6b6ba8104dcd1ea676d6b458d454b362005b` |
| `p3/compression.py` (unchanged) | `49df70d60cbc3b37ec3e484c5a7c64e14ac174faafe8fcaa02e5428c583be4f4` |
| engine `contracts.py` (unchanged) | `9aabbc9f14c55234b5c3612dcc3a7e8165d835e06ea2cc5f72af98d5e6472f2d` |
| engine `p2_owner.py` (unchanged) | `fd98a757a102faae78b5b9e520cf7ce07d518d5f62942bea3279b696a13401d0` |
| B1 `probe/vendor/B1/bfirst.py` (unchanged) | `478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3` |

A's handoff table also lists engine `engine.py` and `model_cycle.py` as if they were in `producer_identity()` code pins. They are **not** in `p3_owner._code_pins()`, and the D01 proof calls `P3Owner.realize` directly rather than `BatchEngine`. The actual pin set is the seven files above plus B1. This is a correction of A's documentary claim, not a weakening of a pin.

Execution commands (from the worktree root; `PYTHONDONTWRITEBYTECODE=1` and `python3 -B` used to avoid bytecode):

```sh
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DUEL-D01-R1/tests/
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_state_store.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_rules.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_projections.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_goal_residuals.py
python3 -B -m pytest -q -p no:cacheprovider \
  'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_primary_actual_formation_read_later_and_no_mediator_control' \
  'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_h_cold_reopen_idempotent_replay_and_source_restore' \
  'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_h_real_process_crash_after_base_before_psych_commit'
```

Receipts: D01 suite **14 passed** (`evidence/d01_b_all_pytest.log`, 83.45 s); P3 owner/store/rules/projections/goal-residual **77 passed, 1 skipped** (`evidence/p3_b_regression_pytest.log`, 52.52 s); P3 primary + cold + real crash **3 passed** (`evidence/p3_b_primary_cold_crash_pytest.log`, 486.09 s). The A-HEAD defect reproduction and the B fixed-boundary reproduction are in `evidence/D01_B_DEFECT_A_HEAD_TAMPER.txt` and `evidence/D01_B_FIXED_TAMPER.txt`.

Write scope used: `SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/`, `.../tests/` was read only, and `SOROK-DUEL-D01-R1/`. No P6 `situated.py`, CG-A branch, shared `CURRENT_PROGRESS`, workflow, Pyat, global configuration or other pair path was modified. A's handoff and evidence logs are preserved.

## 2. A's genuine strengths, independently verified

- **Producer selection is correct.** `P3Owner` + `PsycheStore` + the frozen B1-derived formation rule is the actual existing positive-development producer. A did not invent a second owner, store, rule or scheduler. The extra `d01_reuse` loader is warranted: it opens from durable config rather than caller memory, validates exact source/registry/rule identity, and binds the later consumer's response to the formation record hashes.
- **The positive cold path works.** A's `test_cold_reopen_later_consumer_reads_exact_owner_held_record` does form a record, close, reopen from `p3_owner_config.json` + `p3_psyche.sqlite3`, read the exact hashes, realize a later RECRUIT event, and show the formation hashes in the response streams and the P3 readset with the head unchanged. The actor surface remains `MISSING_RULE`. I reproduced this.
- **The retention guard is correct in its narrow path.** A missing owner config with an existing store refusing `P3_CONFIG_MISSING_WITH_EXISTING_STORE` prevents silent regeneration of plan provenance. I did not find a legitimate no-anchor pending state that should bypass that guard; my recovery accepts only a config proven by a completed operation (or an empty store).
- **A's config-substitution anchor works for the tested case.** A recomputes the last completed operation's `after.state_hash` from the durable base after-state, psychology head and loaded `config_hash`, and refuses a substituted unused plan. This is a real improvement over a self-hashed config file.
- **A's controls are real.** Narrative-only accessible prose yields no records and `MISSING_RULE`; B1 severance refuses before the head changes; exact restoration resumes; direct store binding mismatch refuses; the cold no-record case returns `inspect_alone` with a zero head. The native/durable/first-person boundary is honest.
- **A's rejected alternatives are sound.** A new P3 owner/kernel, reusing the unmerged CG-A P6 bridge, direct `PsycheStore` writes, and the owner-level two-session comparison were correctly rejected on scope/ABI grounds (the last for the wrong reason, below).
- **A's proof boundaries are honest:** rule-level value isolation was identified as weaker than an owner-level test rather than overclaimed; native science remains held.

## 3. Defects established with exact evidence

### B-D01-1 — Cold boundary accepts a rewritten non-head record and the later consumer consumes it

A's `open_cold_owner` validated each row's own record hash, the head pointer and the config anchor, but never called `PsycheStore.verify()`. `query` validates row content hashes but not the record chain. A two-record store therefore permits the first record's `payload.mode` to be changed with `record_json`/`hash` recomputed while the second record and head remain untouched:

- `evidence/D01_B_DEFECT_A_HEAD_TAMPER.txt`, run against A's exact frozen HEAD `82d310b4e` in an isolated worktree, shows `cold open ACCEPTED`, `post modes ['private_check', 'private_check']`, and `later accepted, modes ['private_check', 'private_check']` after a `joint_check` record was rewritten.
- `PsycheStore.verify()` refuses that same store (`JOURNAL_INTEGRITY:RECORD_CHAIN_HASH`), so the durable integrity owner already had the evidence; the D01 boundary did not ask it.
- `evidence/D01_B_FIXED_TAMPER.txt` shows B's boundary refusing the same scenario at cold open.
- B's regression test is `test_cold_open_refuses_rewritten_nonhead_record`; the live-owner terminal-consumer version is `test_live_owner_terminal_consumer_refuses_record_chain_tamper`.

This defeats D01's "exact current owner/source identity survives" and the malformed-record negative without requiring a full state-root rewrite: the config, operation receipts and head are untouched.

### B-D01-2 — A's "owner-level identical-event changed value is impossible" claim is false for a deterministic same-path replay

A's D01-A2 says two separately started P2 sessions do not reproduce identical event hashes and therefore the rule-level comparison is the only isolator. That is true for starts at **different** paths (the P2 material includes path-bound journal state; I measured different base state hashes). It is false for a same-path, same-seed deterministic re-creation of the actual fixture: the base snapshot and both P2 event hashes are identical, while only the frozen P3 history outcome differs.

`tests/test_d01_owner_differential.py` proves:

- `base_before` equal across the two runs;
- formation event hash equal and later event hash/`event_ref` equal;
- formation records and the later response modes are `joint_check` vs `private_check`;
- record hashes differ and each later readset contains its own record, not the other's;
- the store head is one record after the later event (no fabrication).

This is an actual-owner, identical-P2-event value differential. It is stronger than A's direct `evaluate_event` fixture. It is a controlled deterministic replay, not a live fork; that boundary is stated below.

### B-D01-3 — A missing config over a nonempty store is unrecoverable even when the exact config is provable

A's guard correctly refuses silent regeneration, but `_check_or_write_config` did not fsync the config file or directory. A power loss or backup restore can therefore leave the SQLite store durable and the config absent. A holds no verified recovery even when the exact original config document is available. A's own section 5 challenge asked for this migration. B's `recover_missing_config` accepts a candidate only when the last completed operation's durable `after.state_hash` proves its `config_hash`, or when the store is genuinely empty (no operations, no records). It refuses a pending-only unanchored store. Tested in `test_recovery_accepts_only_durable_provenance_and_restores_exact_bytes`, `test_recovery_empty_store_is_unambiguous`, and `test_recovery_preserves_verified_pending_operation`.

### B-D01-4 — A's provenance anchor lived only in the extra loader, not in the actual P3Owner

A direct `P3Owner(...)` reopen with a rewritten config file and matching caller arguments bypassed `d01_reuse.open_cold_owner`; the actual owner did not check the last completed operation. A's handoff says "Cold config is anchored to the last completed operation provenance" without that qualification. B moved the anchor into `P3Owner.__init__` (after store open; store closed on failure) so the actual owner enforces it. Tested by the direct `P3_CONFIG_PROVENANCE_MISMATCH` case in `test_recovery_accepts_only_durable_provenance_and_restores_exact_bytes`.

### B-D01-5 — The response claim scanner accepted unknown affirmative keys

`validate_sourcefree_response` blocked fixed key names/values; `{"can_008":"ACQUIRED"}` and a stream key `native_memory` passed. This is a validator gap rather than the actual rule-generated durable path, but A listed it as an attack surface. B added an exact D01 response mode used by `later_consumer`: exact top-level/rule/stream key sets, response hash, status/grade, and forbidden-claim recursion. Tested by `test_exact_response_refuses_unknown_affirmative_claim_key`.

### B-D01-6 — A's documentary pin table overstates `producer_identity()`

A lists engine `engine.py` and `model_cycle.py` in the "selected producer identity (current code pins)" table. They are not in `_code_pins()` and are not executed by the D01 later-consumer proof. Corrected here; no pin was weakened.

## 4. Corrections implemented

- **`p3/p3_owner.py`**
  - Added `verify_completed_config(store, config_hash)`: the config hash anchored through `PsycheStore.latest_completed()` to the last COMPLETE operation's durable base after-state and psychology head.
  - `P3Owner.__init__` now runs that anchor after opening the store and closes the store on failure. The actual owner, not only the D01 wrapper, enforces config provenance.
  - The normal config write now fsyncs the temporary file and the containing directory before/after `os.replace`.
- **`p3/state_store.py`**
  - Added `latest_completed()`: targeted last COMPLETE operation, so the per-construction anchor is one row rather than a full completed list.
  - `verify()` now binds every record row to the committing operation's effect receipt (`record_id`, `hash`, canonical body) in addition to the record chain and head. A chain-consistent record rewrite that leaves the receipt intact is refused.
  - A's `completed()` listing is preserved.
- **`SOROK-DUEL-D01-R1/d01_reuse.py`**
  - `open_cold_owner` now preflights the real store: refuses pending, runs full `verify()`, runs the D01 config anchor before constructing the owner, then constructs and re-checks the actual owner. `D01_COLD_CONFIG_PROVENANCE_MISMATCH` is preserved.
  - `read_sourcefree_records` checks the B1/registry source, verifies the store, and validates exact record identity: exactly two causal parents `[event, history]`, recomputed record ID from root/actor/branch/event/history/rule, exact payload keys, static origin/access values, and the B1 `mode_for` expected mode for the actual history row.
  - `later_consumer` verifies the store before the later realization and uses the exact response validator.
  - `validate_sourcefree_response(..., exact=True)` is the D01 exact mode: exact top-level/rule/stream keys, sealed hash, status/grade, and claim recursion. The default remains A-compatible for generic callers.
  - `recover_missing_config` adds the root-locked, fsynced, anchor-verified recovery described above.
  - `load_cold_config`/`_validate_config_body` share the config-body checks.
- **Tests** (new, in the D01 return): actual-owner differential, non-head record tamper, chain-consistent record/receipt divergence, live terminal-consumer tamper, exact recovery/exact-byte restore, tampered-candidate refusal, empty-store recovery, pending-operation recovery, direct P3Owner anchor, clean severed-source refusal, exact response claim-key refusal.
- No new owner, scheduler, store, world writer or rule; no P2/P6/CG-A edits; no native claim.

## 5. Proof of improvement and preservation

- **D01 suite:** 14 passed in 83.45 s (`evidence/d01_b_all_pytest.log`). This includes A's five original tests unchanged; they pass.
- **P3 regression subset:** 77 passed, 1 skipped in 52.52 s (`evidence/p3_b_regression_pytest.log`).
- **P3 primary formation/no-mediator control + cold replay/source restore + real crash recovery:** 3 passed in 486.09 s (`evidence/p3_b_primary_cold_crash_pytest.log`).
- **A-HEAD versus B differential:** `evidence/D01_B_DEFECT_A_HEAD_TAMPER.txt` (A accepted and consumed the rewritten record) versus `evidence/D01_B_FIXED_TAMPER.txt` (B refused at cold open with `JOURNAL_INTEGRITY:RECORD_CHAIN_HASH`).
- **Preservation:** A's five D01 tests, the P3 state-store/rules/projections/owner/goal-residual suites, the P3 primary formation→later/no-mediator control, the cold replay/source-restore test and the real subprocess crash recovery all pass. The store head is unchanged by the later RECRUIT event; no record is fabricated; `MISSING_RULE`/`NOT_ISSUED_BY_P3_RULE`/TEST_ONLY remain.
- **Measured costs:** D01 83.45 s; P3 subset 52.52 s; P3 vertical 486.09 s. The cold boundary and later consumer now pay a full `verify()` scan; `latest_completed()` is one targeted row. Token/USD is `UNKNOWN`; only wall-clock test times were measured.
- **Exact-code transition:** the changed `p3_owner.py`/`state_store.py` SHA-256 values are part of every fresh config's `code_pins`. Stores written under A's cut will refuse under B's code (`D01_COLD_CODE_IDENTITY` or `P3_CONFIG_FILE_MISMATCH`). This is the intended exact-code binding, not a silent acceptance; HQ must rebuild or explicitly re-pin at B/D composition. The shared `INTEGRATION_CONTRACT.md` is outside the writer lease and still lists only the base `PsycheStore` API; `completed()`, `latest_completed()`, `verify_completed_config`, `recover_missing_config` and the exact response mode need later contract reconciliation.

## 6. Challenges refuted, conceded, or bounded

- **Refuted:** A's claim that an actual-owner identical-P2-event value test is impossible. Same-path/seed re-creation reproduces the exact P2 event identity; A's negative result came from different paths.
- **Refuted as sufficient:** A's loader-only anchor. The actual `P3Owner` is the terminal consumer and now enforces the anchor.
- **Refuted as sufficient:** A's record-by-record hash checks. They do not establish the chain or the record-to-operation binding; a non-head rewrite passed A's boundary.
- **Conceded:** A's config anchor is a real and useful repair; B preserves and centralizes it.
- **Conceded:** A's rejection of a new owner/kernel, CG-A bridge reuse, direct store writes, and native claims is correct for this packet.
- **Bounded:** A's "full state-root rewrite is outside the boundary" is accepted. B's defect is a record-only rewrite with intact head/config/receipts, which the boundary can and does catch; a Byzantine writer that rewrites every receipt, result and record consistently remains outside this local consistency boundary.
- **Conceded:** A's rule-level value test remains valid; B does not remove it. B adds a stronger actual-owner differential rather than claiming the rule test is false.
- **Bounded:** A's "two separate starts" observation is true for different fixture paths; B's differential uses the same root path deliberately and states that it is a deterministic replay, not a live fork.
- **Own attack announced and refuted:** I first suspected `P3_CONFIG_MISSING_WITH_EXISTING_STORE` was over-strict and should simply regenerate the config from caller arguments. Enumerating the writer's crash windows did not produce a legitimate unproven state; silently regenerating plan provenance would weaken the retention boundary. The correct repair is B's verified recovery (anchor-proved or empty store), not a relaxation of A's guard. A's guard stands.
- **Own attack announced and refuted:** I considered replacing `d01_reuse` with direct `P3Owner` calls as simpler. That loses the durable-config cold open, the exact selected-record/history/mode checks, the later-consumer readset proof and the exact response boundary. The extra loader is warranted at this scope; B strengthened it rather than deleting it.

## 7. New attack surfaces introduced or exposed

- `open_cold_owner`, `read_sourcefree_records` and `later_consumer` now perform a full `verify()` scan. For a large durable store this is O(records + operations) at the D01 proof boundary, not the normal P3 hot path. Measure before using this boundary in a tight loop.
- `P3Owner.__init__` adds one targeted `latest_completed()` read. If a consumer opens owners very frequently, measure the added row read; it is not a full scan.
- The empty-store recovery path accepts any structurally valid candidate whose source/binding matches the empty store's meta. There is no durable computation to reinterpret, but an operator with write access to an empty state root can choose the future P3 config. Confirm that this is the desired fresh-sidecar policy.
- The exact response validator is D01-specific. D03/D04 must add an explicit response schema rather than silently widening or bypassing `exact=True`.
- The semantic record check recomputes B1 `mode_for`; if B1 is severed or changed, `read_sourcefree_records` now refuses `P3_B1_SOURCE_SEVERED`/registry mismatch. Do not cache the mode across source changes.
- `verify()` now relies on the operation receipt's `records` list matching the rows. A future store normalization change must update both sides; a wholly rewritten state root remains outside the local anchor.
- The new config fsync is best-effort for the directory; filesystems that ignore directory fsync can still lose the rename under a crash, which is exactly why verified recovery exists.
- The differential is a same-path deterministic replay. If HQ requires a live fork of one root, C12/branch machinery outside D01's lease is needed.

## 8. Surviving disagreements and material questions

- **Same-path replay vs live fork.** I claim identical P2 root/state/event hashes and a single controlled P3 history difference make the differential an actual-owner changed-value proof. A true one-root fork would be stronger but is not available in this lease. The evidence is explicit about the method.
- **Full scan in the owner constructor.** I added the config anchor to `P3Owner.__init__` but not `store.verify()` there, to avoid a full scan on every construction. The D01 boundary scans. If HQ requires every actual owner construction to verify the full record chain, that is a cost/ABI decision; I did not silently make it.
- **Shared contract reconciliation.** `INTEGRATION_CONTRACT.md` is outside the lease. The additive methods and the exact response mode must be reconciled by HQ before D02–D05 rely on them; they are not claimed as received.
- **Code-pin transition.** B's code cut invalidates A-cut stores by design. Is a pinned old-code read/migration path required, or should HQ rebuild test fixtures at the new cut? I did not weaken `code_pins` to make old stores open.
- **Recovery candidate provenance.** The exact config hash is only recoverable from a candidate document; unused plans are covered by that hash, so reconstructing the full config from used-operation receipts alone is impossible. The anchor proves the candidate rather than trusting it. If an authenticated config backup/controller store exists, it should be the source.
- **Pending policy.** `open_cold_owner` remains read-only and pending-refusing; `recover_missing_config` can restore a verified config while a pending operation remains, allowing `P3Owner`'s own recovery path. Whether the cold reader itself should expose a pending recovery entry is a D02/D04 interface choice.
- Native CAN/ADP/Pyat, human/actor rights, production and protected merge remain held. No claim is made that D01 completes CG-D or any J cell.

## 9. Challenge to Agent A

1. **Break the differential.** Show that the same-path/seed replay is not an identical world on a consequential hidden dimension (path-bound material, clock, journal, or P3 state other than the intended history). If it is invalid, produce a true forked-root identical-event comparison within the D01/available lease and show the later response difference.
2. **Break the record-to-receipt binding.** Construct a record tamper that passes both `PsycheStore.verify()` and the `P3Owner`/D01 anchor without rewriting the whole state root; repair the boundary if you can.
3. **Break the semantic record check.** Find a legitimate selected-rule record that my exact parent/ID/payload/mode check falsely refuses (multiple histories, empty selectors, a different but valid mode, a future rule version). Either fix the selector or prove D01 must not read it.
4. **Attack recovery.** Find a missing-config state with a completed anchor where the exact candidate is legitimate but my recovery refuses, or an empty-store candidate that should be refused. Provide the exact state transition and a safer recovery.
5. **Attack the pending boundary.** Decide whether `open_cold_owner` should continue refusing pending while `recover_missing_config` allows a verified pending config, or whether the cold boundary must itself recover the pending operation. Demonstrate the crash window.
6. **Attack the code-pin transition.** Propose a precise B/D reconciliation for A-cut stores that preserves exact source identity; do not solve it by weakening `code_pins`.
7. **Use it.** Implement D02's situated-field readset on this boundary and show a changed material/actor fact changing the actual later consumer, without claiming D01 is the whole CG-D or J join.

## 10. Limits

- `SOURCEFREE_S2_ONLY` engineering; no native CAN-008/010/011, ADP-016/017/019, Pyat, C9/O15 native, actor/human or rights issuance; no production or protected merge.
- D02–D05 are unimplemented. No P6, B01+, CG-A bridge, multi-actor parent, dated household or generated root is added.
- The positive proof is the actual sourcefree formation record retained in the actual `PsycheStore` and read by a later actual `P3Owner.realize` after cold reopen from durable config. The differential is a deterministic same-path replay with an identical P2 event identity, not a live fork.
- The boundary is a local consistency anchor, not a Byzantine authenticated root. A writer that rewrites the config, store records, operation receipts and results consistently is outside it.
- Token/USD cost is `UNKNOWN`; pytest wall times and the A-HEAD defect probe are the measured evidence.
