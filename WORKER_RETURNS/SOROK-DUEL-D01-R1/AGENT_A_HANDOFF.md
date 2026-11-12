# SOROK D01 Agent A handoff — exact P3 reuse and sourcefree boundary

**Task:** `D01` — Exact-reuse positive-development producer selection and sourcefree native-rule boundary.
**Programme:** #939 / PR #938 at `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Author branch:** `codex/sorok-duel-d01-a-20261112-r1`.
**Protected base:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.
**Author ceiling:** `SOURCEFREE_S2_CANDIDATE_PENDING_B`; no independent receiving, native science, actor/human authority or protected merge is claimed.

## 1. Exact artifact

Author implementation code cut: `ed8add689631a796a4177bdb9aa98452d946e7c5`.
The exact immutable per-file SHA-256 identities are listed below; later commits on this branch only add/update the handoff and impact records.

Changed implementation paths:

| Path | Change |
|---|---|
| `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/p3_owner.py` | Fail-closed retention invariant in `P3Owner._check_or_write_config`: a missing owner config with an existing `p3_psyche.sqlite3` now refuses instead of silently regenerating plan provenance. |
| `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/state_store.py` | Additive read-only `PsycheStore.completed()` listing COMPLETE operations in durable sequence order for the D01 provenance anchor. |
| `WORKER_RETURNS/SOROK-DUEL-D01-R1/d01_reuse.py` | Read-only D01 reuse boundary: durable-config cold open, exact producer identity, sourcefree record validation, later P3 consumer validation. No new owner, scheduler, rule, store or world writer. |
| `WORKER_RETURNS/SOROK-DUEL-D01-R1/tests/test_d01_reuse.py` | Five discriminating tests. |
| `WORKER_RETURNS/SOROK-DUEL-D01-R1/evidence/*.log` | Captured pytest receipts. |

Execution commands (run from the worktree root, `python3 -B` so no bytecode is written):

```sh
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DUEL-D01-R1/tests/test_d01_reuse.py
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_state_store.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_rules.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_projections.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_goal_residuals.py
python3 -B -m pytest -q -p no:cacheprovider \
  'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_primary_actual_formation_read_later_and_no_mediator_control' \
  'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_h_cold_reopen_idempotent_replay_and_source_restore'
```

Observed receipts:

- D01 suite: **5 passed in 24.00 s** (`evidence/d01_reuse_pytest_vv.log`; latest rerun 5 passed in 23.78 s in `evidence/d01_reuse_pytest.log`).
- P3 owner/store/rules/projections/goal-residual suite: **77 passed, 1 skipped in 50.15 s** (`evidence/p3_regression_pytest.log`).
- P3 primary formation→later-response/no-mediator control plus cold replay/source restore: **2 passed in 446.66 s** (`evidence/p3_primary_cold_pytest.log`).

The selected producer identity (current code pins) is exposed by `d01_reuse.producer_identity()` and freezes these actual sources:

| Source | SHA-256 at this branch |
|---|---|
| `p3/p3_owner.py` (post-repair) | `ee2d0826a3680ce54a9031f8ce8316c58da2f4590d1a9efbc2d17b4ede210583` |
| `p3/state_store.py` (post-repair) | `95ca65edf9e9c541b01224aa9fb977fee2c575b717de3d15d3a0a2412fd8ecf2` |
| `p3/test_rules.py` | `27272cd43c26b6aa114ee65c97ca07eb56accecbd440841c29696b98e203b4b4` |
| `p3/projections.py` | `ca405dda778191537ce38b0b63ff6b6ba8104dcd1ea676d6b458d454b362005b` |
| engine `contracts.py` | `9aabbc9f14c55234b5c3612dcc3a7e8165d835e06ea2cc5f72af98d5e6472f2d` |
| engine `p2_owner.py` | `fd98a757a102faae78b5b9e520cf7ce07d518d5f62942bea3279b696a13401d0` |
| engine `engine.py` | `ba6caa74b2c57e567dbefa57571bc931bac8e4e5108bf844efe2966754ae9586` |
| engine `model_cycle.py` | `af83f8f1a3d31c4281dc2550e07fa0e5c31304cfd3fb1bc9538f674c95f46df5` |
| B1 `probe/vendor/B1/bfirst.py` | `478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3` |

Pre-repair `p3_owner.py` SHA-256 was `e735ada798533a8f568739e823767bb2e2b4272c3c03d84dc2cd47f73cf65df1`; the two added lines are the retention guard.

## 2. Governing contract

- D01 must select the existing P3 positive-development producer and prove one admitted sourcefree record with exact current owner/source identity survives, and a later P3 consumer reads it.
- The terminal consumer in the packet is the actual later P3 owner/readset and scoped actor output, not a narrative report.
- The negative court must reject a test interpreter or narrative-only memory being claimed as a CAN/ADP durable issue, and reject malformed root/branch acceptance.
- Cold/no-record and source-severance must refuse or change the same-root computation; exact restore must be tested.
- Grade is `SOURCEFREE_S2_ONLY`; native CAN/ADP/Pyat, actor/human rights and protected merge remain held.
- Exclusive writer scope used: `SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/`, `.../tests/` and `SOROK-DUEL-D01-R1/`. P6 `situated.py`, CG-A candidate branches, shared guides, workflows and other pair paths were not modified.
- The unmerged CG-A chain `8248711fb` → `384d4a4a` → `0213c844` → `37c5842e` was inspected through git. It is **not protected-accepted** here. Its P3/P6 bridge is not duplicated or modified.

## 3. Strongest achieved result

**Actual producer → first consumer.** `d01_reuse` opens the actual `P3Owner` over an actual `P2Owner`, realizes the selected B1-derived formation rule, reads the committed `V3MS_MEDIATOR` records, closes the owner, reopens the same durable root from `p3_owner_config.json` plus `p3_psyche.sqlite3`, and realizes a later `RECRUIT` event. The later response's streams carry the exact formation record hashes and the P3 result readset contains them; the store head stays at two records and no new record is fabricated. The actor surface remains the existing sourcefree projection with `memory_formation: MISSING_RULE`.

**Cold no-record control.** A cold-open owner with zero records realizes the later event as `inspect_alone`; the head remains zero. This is distinct from the formation case.

**Changed-value dependence.** Because two separately started actual P2 sessions do not reproduce identical event hashes, value dependence is isolated at the exact rule boundary that `P3Owner._effect` invokes: two histories differing only in `recognized_plan` vs `imposed_plan` produce records with the same event hash but different `payload.mode` (`joint_check` vs `private_check`) and different record IDs/hashes; the later response consumes exactly those values. This is the actual B1 `mode_for` rule, not a narrative interpreter. The owner-level cold test proves the same rule/store/readset path is the actual later consumer.

**Negative court.** Tests establish:

- narrative-only `accessible` prose with no actor access yields `HELD`, no records and `memory_formation: MISSING_RULE`;
- `production_guard()` remains `DENY_ZERO_EFFECT` / `ZERO_POSITIVE_REGISTRY`;
- `validate_sourcefree_response` refuses affirmative native-rule, first-person and durable-transition claims;
- a wrong store binding refuses with `STORE_REOPEN_BINDING_MISMATCH`;
- tampered config root and branch refuse at the cold base identity check;
- exact original config bytes restore the exact head and record hashes;
- missing/altered B1 source refuses with `P3_B1_SOURCE_SEVERED` before the store head changes; exact restore resumes the later consumer.

## 4. Own hostile findings and repairs

**Finding D01-A1 (repaired).** Before this branch, deleting `p3_owner_config.json` while `p3_psyche.sqlite3` held two records and constructing `P3Owner` with a substituted plan silently re-created the config, retained the two-record head, and changed the same-root computation: the later consumer returned `inspect_alone` with no record. I reproduced this directly before editing. The config file is part of the exact plan/provenance identity; silent regeneration over a nonempty store is retention corruption. The repair makes `_check_or_write_config` refuse `P3_CONFIG_MISSING_WITH_EXISTING_STORE`. Exact config restoration then resumes with the exact head and hashes. The D01 test exercises both the direct `P3Owner` refusal and the D01 cold-open refusal.

**Finding D01-A2 (limitation made explicit).** Two separately started P2 sessions do not produce the same event hash, so a two-session owner-level “changed value” comparison would be confounded by the P2 event. I did not use that weaker comparison. I used the exact rule with an identical event hash for value isolation, and the actual owner for the cold first-consumer proof. This is a proof-boundary choice, not a claim that the rule-level test is a second actual P2 session.

**Finding D01-A3 (scope).** The CG-A cold-later test already exercised P3 cold retention, but it re-supplied the source/history/plans from an in-memory `VerticalCase`. It did not cold-open from the durable config. D01 adds the durable-config loader and refuses missing config/store at that boundary. It does not duplicate or modify the CG-A P6 bridge.

**Finding D01-A4 (repaired).** A config file is only self-hashed. Before the provenance anchor, an attacker or accidental editor could alter an unused plan (for example the later counterpart), recompute the plan hash and `config_hash`, and the cold loader would accept the substituted plan while retaining the two-record store head; the later consumer then returned `inspect_alone`. I reproduced this directly. The repair adds `PsycheStore.completed()` and recomputes the last completed operation's `after.state_hash` from its durable P2 after-state, durable psychology head and the loaded `config_hash`. A config whose hash was not the one used at the last completed operation now refuses `D01_COLD_CONFIG_PROVENANCE_MISMATCH`. The test also exercises exact config restore. This is a durable consistency anchor, not a cryptographic signature; a writer with full rewrite authority over the entire state root is outside the boundary.

## 5. Unresolved challenges

- No native CAN-008/010/011, ADP-016/017/019, Pyat, C9/O15 native or human issuance; everything here is TEST_ONLY sourcefree engineering.
- D02–D05 remain unimplemented: no situated-field projection, no CAN-008 immediate-vs-durable acquisition, no target acquire/inhibit/reinforce/hold, no prospective performed consumer.
- No multi-actor, independent mother, dated material household or P6 bridge is added.
- The actual P2 fixture is a controlled workshop; its event identity is nondeterministic across separate starts. Do not generalize the value test beyond the exact rule boundary.
- The D01 cold loader freezes absolute-path code pins through the existing `P3Owner._code_pins()`. Exact-worktree cold reopen works; a moved/copied worktree is expected to refuse until its config is regenerated. This is consistent with the existing owner, but it is a portability limit.
- The full P3 vertical matrix (all A–H cases) and full 115-test P3 suite were not rerun. Targeted owner/store/rules/projections/goal-residual tests and the two decisive vertical tests were run. B3A/BP2P4J/HQ300/M01/C9RI were inspected through the actual E1 reconnaissance and the current tree, but were not re-executed; they are rejected as D01 drop-in producers on exact ABI grounds, not declared scientifically inferior.
- `PsycheStore.completed()` is an additive read-only method documented in the module and this handoff. The shared P3 `INTEGRATION_CONTRACT.md` is outside this lease and still lists only the original API; HQ should reconcile that shared contract if D02–D05 rely on the additive listing. No silent scope crossing was made.
- Token/USD cost is `UNKNOWN`; only wall-clock test times are measured.

## 6. Likely attack surfaces

- **Config reset semantics:** find a legitimate P3 crash/reset transition where a missing config with an existing store is the only recoverable state. If one exists, provide a safe migration that preserves exact plan provenance; do not silently weaken the new refusal.
- **Claim scanner:** construct a nested response/record shape that carries an affirmative native/ADP/first-person claim past `_walk_claims`; if it passes, repair the scanner and add the negative.
- **Cold first-consumer:** find a way to demonstrate actual-owner changed-value dependence with identical P2 event identity across two cold sessions; if P2 can be made deterministic, replace the rule-level isolation with the stronger owner-level proof.
- **Producer selection:** show a current exact-ABI producer other than B1/P3Owner that is a better drop-in for D01 without a new owner or scheduler.
- **`read_sourcefree_records` breadth:** the exact `V3MS_MEDIATOR`/formation-rule selection is intentional for D01; check whether D04 needs a compatible additive selector without weakening D01's exactness.
- **Guard ordering:** verify the new refusal occurs before any P2/P3 effect and does not mask a more specific corruption diagnosis.
- **Store rewrite authority:** the provenance anchor detects a substituted config against the last durable completion, but a writer that recomputes the operation/result/receipt hashes could defeat it. If the commission needs Byzantine state-root tamper evidence, that requires an external authenticated root, not another local hash.
- **Pending-operation cold state:** the D01 cold loader refuses any pending operation (`D01_COLD_OPERATION_PENDING`); verify this is the desired consumer behavior versus P3's own recovery path, which needs the exact original proposal/expected state.

## 7. Rejected alternatives

- **New P3 owner/kernel:** rejected; the existing `P3Owner` + `PsycheStore` + B1-derived `test_rules` already implement the sourcefree producer/readset. D01 adds only a read-only reuse/consumer boundary and a retention invariant.
- **Reuse the CG-A P6 bridge:** rejected; it is unmerged, not protected-accepted, outside D01's packet, and P6 `situated.py` is explicitly outside this writer scope.
- **B3A/HQ300/M01/BP2P4J as producer:** rejected for D01 on exact ABI: they are not drop-in current `DevelopmentOwner` writers (in-memory or separate product/bridge), as recorded by the actual E1 reconnaissance. They were not silently reclassified or declared native.
- **Direct `PsycheStore` writes as the later consumer:** rejected; it bypasses the P3 owner plan/rule/event/authority validation. D01 reads and realizes only through `P3Owner`.
- **Owner-level two-session value comparison:** rejected as confounded by nondeterministic P2 event identity; the rule-level identical-event comparison is the defensible isolator.
- **Treating the test interpreter/provider or narrative prose as a durable psychological issue:** rejected; the provider is transport only, records come from the frozen sourcefree rule, and the response boundary is checked for native/first-person/durable claims.

## 8. Proof boundaries

- This is `SOURCEFREE_S2_ONLY` engineering. It does not establish native psychological science, human validity, actor rights, source rights, or a protected merge.
- The positive proof is an actual sourcefree formation record retained in the actual `PsycheStore` and read by a later actual `P3Owner.realize` path at the same root/actor/branch after cold reopen from durable config.
- The changed-value proof is at the exact rule boundary with an identical event hash; it is not a second actual P2 session.
- The negative proofs are refusal/absence/changed-computation controls at the D01 boundary, not claims about untested native rules.
- No claim is made that D01 completes CG-D or the whole programme; D02–D05 and the material/parent/P6 joins remain separate.
- The `P3Owner`/`PsycheStore` repairs are retention-integrity fixes: a missing config with an existing store refuses, and cold config is anchored to the last completed operation's durable provenance. They are not rule, science or authority changes.
- The provenance anchor is a local consistency check, not an authenticated signature; full state-root rewrite authority is not defeated.

## Hardest concrete challenge for the same B

Take the pre-repair reproduction in section 4 and try to make the repaired boundary both exact and recoverable: find a genuine interrupted cold state (config absent, store present) that a legitimate operator or crash recovery must repair, and implement a migration that re-establishes the exact original config/provenance from authoritative receipts rather than from caller-supplied plans. If no such state is legitimate, prove that by enumerating the writer’s actual crash windows. In parallel, try to build an actual-owner, identical-P2-event value test; if P2 cannot be frozen, demonstrate why and keep the rule-level isolation honestly bounded.
