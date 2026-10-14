# HQ299 G12 — actual S-GI1 direct generalization — executed return

**Terminal:** `G12_SGI1_ORIGINAL_24_OF_24__98_OF_98_REPLAYED__GI2_57_PREDICATES_53_PASS__3_NOT_REACHED_AUTHORITY_GAP__1_NOT_REACHED_FIXTURE_SCHEMA_GAP__ZERO_MODEL_SOURCE_ACTOR_CALLS__NO_ADOPTION`.

## 1. Custody

- Repository `maidiu/rawlsing` (private). Branch `agent/rabochii-sorok-r3-hq299-g12-sgi1-direct-generalization-r1`.
- **Exact sealed worker startup:** `3c0270d2b3e09a82459269b42ddc73032caf9b6d` (commission-creation commit; direct remote branch read confirmed before work). HQ299 parent `5c59fb409d5f08312c19b936738eb4410dbd4f26` is ancestry, not the worker startup.
- Commission read in full: `WORKER_COMMISSIONS/SOROK-R3-HQ299-G12-SGI1-DIRECT-GENERALIZATION-R1/00_COMMISSION.md`; Sorok `00_READ_ME_FIRST` / `00B` / `00C` (incl. §5A `LOCAL_DOMINANT`) / `00D` and `HQ299_SIX_RETURN_INTAKE_AND_INDEPENDENT_COURT_ORDER_R1.md` at `5c59fb409…`.
- Role: independent source-free genealogy implementation scientist. NOT GI2 surrogate author, NOT S-GI1 author, NOT ADP issuer, NOT reviewer/adopter, NOT V3 actor.
- Write terrain: `WORKER_RETURNS/SOROK-R3-HQ299-G12-SGI1-DIRECT-GENERALIZATION-R1/` only. No accepted owner module, commission, PRE-MAIN or CURRENT file touched.
- Predecessor material read at exact commits: S-GI1 original `27ca1f2792a5213064c0b5ea2e27b89e8acce0c3`; GI2 surrogate `aa4d845736ff6208a988a3e70cb9f74e3104633e`; G11 `0cb708bbfe522a6c6e359f36d99835d180d5a84d`; SG authority packet `a12d01c5f7d7ddad8be92c58afc97141b672dba0`.

## 2. Environment (00C §5A LOCAL_DOMINANT honoured)

Authorized OpenCode Go local session, single canonical Git object store, governed sparse worktree. Python 3.11.3 / pytest 9.1.1 / git 2.39.1 verified. **True S-GI1 closure staged and blob-verified**: 34 objects (14 lab modules + `run_k11.py` + 11 frozen LLM proposal records + 8 reference outputs) at `27ca1f279…`, Git blob SHA-1 with NUL `blob <len>\0` preimages — `staging/sigi1_staging_manifest.json`. Executed imports recorded per module (`02_EXECUTION_RECEIPTS.json#sgi1_module_provenance`), e.g. `construction.py` `8bc7c1a5d8d9…`, `pipeline.py` `cf91c99b90e4…` (matching GI2's documentary pins exactly). Runtime mirror `repro/sigi1_run/` copied byte-identically before execution. Sanitized passport: `environment_passport_delta.json`. No warm-browser fallback was taken (no surviving S-GI1 Browser closure existed; the commission already routes this import-heavy grade to LOCAL).

## 3. Original S-GI1 24-case / 98-predicate suite — EXECUTED

Command (exact historical entrypoint, zero model calls):
`SGI1_MODEL=0 SGI1_REUSE_RECORDS=1 python3 01_LAB_IMPLEMENTATION/run_k11.py` (cwd `repro/sigi1_run/01_LAB_IMPLEMENTATION`).

| Item | Result |
|---|---|
| Grade | `K11_LAB_PASS_AT_DECLARED_GRAIN` |
| Cases | **24 / 24** at expected status (11 `K11_CASE_PASS`, 13 `K11_CASE_INVARIANT_HELD`), `cases_failed: []` |
| Atomic predicates | **98 / 98** |
| Suite fingerprints vs original | **identical** (0 mismatched fields over the full fingerprint tree) |
| Wall | 0.135 s (frozen-record replay) |
| Model calls this run | **0** (the `model_status: AUTOMATED_LLM_PROPOSAL_EXECUTED` label inside `k11_summary.json` belongs to the frozen historical records' acquisition; per-case `model_calls: 0`) |

## 4. GI2 12 held-out families / 57 predicates on ACTUAL S-GI1 — EXECUTED

Independently frozen **before** any adapter code: `01_FROZEN_GI2_EXPECTATION_LEDGER.json` (families sha256 `5b3339d5e28205032e44bd4e614b03e94de8a09bb90a0c66710b9efcf5f948ca`, matching GI2's declared preimage). The GI2 oracle strings are preserved verbatim; **no surrogate code (`forward_lab.py`) was executed** — all 57 predicates ran through `gi2/sgi1_bridge.py` onto S-GI1's real `run_pipeline` / `construct_second_parent` / `DadHistoryBuilder` / `forward_replay_to_endpoint` / `heldout_independent_probes` / `build_causal_graph`.

Command: `python3 -m pytest gi2/test_gi2_on_sgi1.py -q --junitxml=repro/gi2_57.junit.xml` → **57 executed**.

| Verdict | Count | Meaning |
|---|---:|---|
| PASS | **53** | S-GI1 reproduced the frozen expectation (exact name or declared typed-equivalent mapping) |
| NOT_REACHED_AUTHORITY_GAP | **3** | semantics genuinely absent from the owner |
| NOT_REACHED_FIXTURE_SCHEMA_GAP | **1** | owner fixture schema differs |
| RED | 0 | — |

### 4.1 Family status matrix (S-GI1 observed vs GI2 expected)

| Family | GI2 expected | S-GI1 observed | attempts | verdict |
|---|---|---|---:|---|
| HW01 two fathers, same endpoint | COMMITTED | COMMITTED | 1 | PASS |
| HW02 older-child mother | COMMITTED | COMMITTED | 1 | PASS (family) / see 4.2 |
| HW03 mobility | COMMITTED | COMMITTED | 1 | PASS |
| HW04 world route closed | WORLD_ROUTE_UNAVAILABLE | WORLD_ROUTE_UNAVAILABLE | 0 | PASS (declared map: `SCENARIO_INFEASIBLE`/`SCENARIOS_VALID_EMPTY`) |
| HW05 N9 unavailable | WORLD_EVIDENCE_UNKNOWN | WORLD_EVIDENCE_UNKNOWN | 0 | PASS (declared map: `NOT_EXECUTED_AUTHORITY_HOLD`) |
| HW06 N9 stale as-of | WORLD_EVIDENCE_STALE | WORLD_EVIDENCE_UNKNOWN | 0 | **NOT_REACHED_AUTHORITY_GAP** |
| HW07 endpoint shift | HISTORY_SEARCH_EXHAUSTED | HISTORY_SEARCH_EXHAUSTED | 4 | PASS |
| HW08 retry success third | COMMITTED | COMMITTED | 3 (`[FAIL,FAIL,PASS]`) | PASS |
| HW09 retry all fail | HISTORY_SEARCH_EXHAUSTED | HISTORY_SEARCH_EXHAUSTED | 4 | PASS |
| HW10 child-future-dependent | FUTURE_CHILD_INFORMATION_LEAK | HISTORY_SEARCH_EXHAUSTED | 1 | **NOT_REACHED_AUTHORITY_GAP** |
| HW11 unconventional | COMMITTED | COMMITTED | 1 | PASS |
| HW12 no dyad bridge | COMMITTED | COMMITTED | 1 | PASS (joint_dyad_evidence false, population_posterior NOT_ESTIMABLE) |

### 4.2 The four typed gaps (flagged, not patched)

1. **HW06 `WORLD_EVIDENCE_STALE` (×1 predicate):** S-GI1's synthetic world premise has **no N9 evidence-custody layer and no as-of/staleness model**; a STALE-vs-UNKNOWN distinction is inexpressible without new accepted semantics. The refusal-before-attempt invariant still holds via the owner's generic `NOT_EXECUTED_AUTHORITY_HOLD` (0 attempts, no filler facts, distinct from zero-probability).
2. **HW10 leak status + 0 attempts (×2 predicates):** S-GI1's `FutureChildPartitionGuard` audits only mother-anchor visible field names; a **declared future-required endpoint has no pre-attempt refusal channel**. Expressed as an owner endpoint predicate, the requirement was refused by `forward_replay_to_endpoint` (no future content was ever read), but the terminal is `HISTORY_SEARCH_EXHAUSTED`, not `FUTURE_CHILD_INFORMATION_LEAK`. Adversarial counterexample retained.
3. **HW02 older-child exact fields (×1 predicate):** GI2 asserts 3 events of kind `OLDER_CHILD*` with `hours_per_week=22`/`prior_link=PRIOR_PARTNER`; S-GI1's older-child fixture **M2** carries `CHILD_GENERATED`/`RELATIONSHIP_CHANGE`/`CARE_ROUTINE`/`HOUSEHOLD_STATE` with different payloads. The semantic invariant (older-child history immutable under focal genealogy — mother checkpoint hash stable) is satisfied; the exact-field schema is a fixture gap.

### 4.3 Declared interface adaptations (frozen before execution; no semantic repair)

- status-name back-map: `SCENARIO_INFEASIBLE`/`SCENARIOS_VALID_EMPTY`→`WORLD_ROUTE_UNAVAILABLE`; `NOT_EXECUTED_AUTHORITY_HOLD`→`WORLD_EVIDENCE_UNKNOWN` (HW06 deliberately **not** mapped to STALE).
- mother `M1`→S-GI1 fixture `M2`; route/place names per frozen ledger.
- `fail_first` schedules realised through S-GI1's own endpoint-mismatch mechanism (`construct_second_parent` + seed-derived endpoint predicates) — the same declared-intervention class as S-GI1's own `endpoint_place_override`; no surrogate scheduling code.
- relation-view asymmetry realised via the owner's `force_mom_affectionate_dad_unknown` intervention (default S-GI1 states are independent but equal-valued; `reciprocity_inferred=False` throughout).
- `two_dag_oracle` attaches label `BAD_PARENT_ORDER` to S-GI1's real `causal_endpoint_to_childhood_edges` detections (name mapping only).

## 5. Interface findings (S-GI1 owner defects, not repaired here)

1. `run_pipeline(extra_llm_candidates=...)` is a **dead parameter** (declared, never read).
2. `run_pipeline` exposes **no candidate endpoint-predicate channel** (`required_state_predicates` fixed to availability+place) — partial-failure schedules must go through `construct_second_parent` directly.
3. No N9 evidence-custody/as-of semantics (gap 1 above).
4. No future-requirement pre-attempt gate (gap 2 above).
5. Older-child fixture schema divergence (gap 3 above).

## 6. Adversarial counterexamples retained

- `test_bad_reverse_edge_detected`: forged causal parent order **detected** by S-GI1's temporal-inversion check (the strongest hostile in the 57).
- `test_endpoint_change_does_not_mutate_mother`: endpoint shift + 4 new seeds → mother checkpoint hash invariant, `HISTORY_SEARCH_EXHAUSTED`, zero mutation.
- HW10: a future-required endpoint is refused by replay (no future read) yet cannot be labeled a leak pre-attempt — recorded as a gap, not glossed.

## 7. Cost and calls

- Model calls **0**; original-source reads **0**; actor/V3 invocations **0**; survey bytes **0**.
- K11 wall 0.135 s (frozen replay); GI2 57-predicate suite 0.37 s; staged bundle 34 objects (~0.4 MB source + records).
- Cash/quota: `UNKNOWN` (no new billable call made; OpenCode Go shared quota).

## 8. Grade, ceilings and non-claims

- **Claimed grade:** `SOURCEFREE_PINNED_IMPORTED_OWNER_DIRECT_GENERALIZATION_EVIDENCE` — the actual original S-GI1 implementation passes its declared 24/98 suite at this read cut with byte-identical suite fingerprints, and satisfies **53/57** independently frozen GI2 held-out predicates, with 4 precisely typed gaps.
- **NOT claimed:** semantic adoption of any genealogy rule; ADP015/020 issuance; conception/birth biological authority; population posterior or original-source calibration; V3 person generation/wake; N11/N12 readiness; physical weld; product release; that the GI2 surrogate was a substitute (it was never executed here).
- `ADP015/020_ISSUANCE=NONE; NEW_SELECT_WEIGHTS=NONE; CONCEPTION_BIRTH_OWNER_AUTHORITY=HOLD; ORIGINAL_SOURCE_RIGHTS=NONE; ACTOR_MODEL_AUTHORITY=NONE; CANONICAL_ADOPTION=NONE; V3_WAKE=NONE`.
- Risk: the two authority gaps (staleness custody, future-requirement gate) are exactly where GI2's held-out design is *stricter* than the owner; treating 53/57 as full generalization would overclaim. Independent review (03 §1) required before any acceptance.

## 9. Changed paths and remote verification

Changed paths (only): `WORKER_RETURNS/SOROK-R3-HQ299-G12-SGI1-DIRECT-GENERALIZATION-R1/` — `00_RETURN.md`, `01_FROZEN_GI2_EXPECTATION_LEDGER.json`, `02_EXECUTION_RECEIPTS.json`, `03_REVIEW_AND_OWNER_ACTION_REGISTER.md`, `environment_passport_delta.json`, `conftest.py`, `gi2/` (bridge, tests, frozen families), `staging/` (stage script, manifest, blob-verified S-GI1 closure), `repro/` (battery script, runtime mirror outputs, stdout, JUnit), `outputs/` (verdict ledger).

Branch pushed (assigned branch only); exact remote HEAD verified by direct `git ls-remote origin agent/rabochii-sorok-r3-hq299-g12-sgi1-direct-generalization-r1` after publication and reported in the completion message (a commit cannot self-reference its own future SHA).

TERMINAL: `G12_SGI1_ORIGINAL_24_OF_24__98_OF_98_REPLAYED__GI2_57_PREDICATES_53_PASS__3_NOT_REACHED_AUTHORITY_GAP__1_NOT_REACHED_FIXTURE_SCHEMA_GAP__ZERO_MODEL_SOURCE_ACTOR_CALLS__NO_ADOPTION`.
