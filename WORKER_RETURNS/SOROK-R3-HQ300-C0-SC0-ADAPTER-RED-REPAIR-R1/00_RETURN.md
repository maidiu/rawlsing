# HQ300 C0 — SC0 value-bearing adapter RED repair + pinned PE/C1/N10E connection

**Terminal:** `HQ300_C0_RC0_12_REDS_REPAIRED__13_PRESERVED__K9_8_K10_28_RETAINED__RC0_25_OF_25__PINNED_PE_C1_N10E_CONNECTED_CALL_TRACE__N10E_C1_56_PE_21_GREEN__NO_ADOPTION__NO_N9_N10W_ISSUANCE__NO_WAKE`.

## 1. Custody

- Repository `maidiu/rawlsing` (private). Branch `agent/rabochii-sorok-r3-hq300-c0-sc0-adapter-red-repair-r1`.
- **Exact sealed worker startup:** `74d85639f54deebf38eac6b334034c417cf5831d` (commission-creation commit; verified by direct remote branch read before writes). HQ300 parent `28d791df05b4d24ebe48b4298101af6951035a36` is ancestry only.
- Commission read in full: `WORKER_COMMISSIONS/SOROK-R3-HQ300-C0-SC0-ADAPTER-RED-REPAIR-R1/00_COMMISSION.md`; Sorok `00_READ_ME_FIRST` / `00B` / `00C` (§3A, §5A) / `00D` and `HQ300_HQ299_SIX_RETURN_ADJUDICATION_INTAKE_R1.md` at the HQ300 parent.
- Frozen inputs read at exact cuts: HQ298 SC0 candidate `b15dbbc4f07ae79e9ffb71e88e91e3b28b35da59`; **RC0 independent court `86bd2a54687b40401f7c4247607bd1873c585619`** (01 expectations, 02 per-case, 03 nine PE REDs, 05 owner actions); SC0 oracles at `241d35fa…`; PE2 `b94f0f98…`/`b497f8571…`; earlier K9R `f515188e…`, K9E `e61a26ce…` (read for provenance only).
- Role: bounded sourcefree implementer. NOT HQ, NOT acceptance reviewer, NOT issuer. Write terrain: `WORKER_RETURNS/SOROK-R3-HQ300-C0-SC0-ADAPTER-RED-REPAIR-R1/` only. Model/host unchanged per dispatch (OpenCode MiMo-V2.6 Pro); no harness or environment switch.

## 2. What was frozen before any change

`01_FROZEN_RC0_EXPECTATIONS_AND_REDS.json` (sha256 `8eda5d91…`) records, **before candidate edits**: RC0's 25 cases with their original statuses (**12 RED / 13 PASS**), the 10 independent invariants, all oracle sha256s (RC0 expectations `c9abb1c6…` declared/verified; K9 `9ccb66f9…`, K10 `e78b3ee9…`, envelope `610ac870…`), and the no-waiver rule. RC0's test source is staged byte-identical and executed unchanged.

## 3. The 12 RC0 REDs — all repaired (RC0 source unchanged)

| RC0 case | RC0 | HQ300 | Repair |
|---|---|---|---|
| `test_adapter_denied_world_read…[ProviderA/B]` | RED | **PASS** | `adapter._fail_closed_entry` refuses `DENIED_USE` before any value/consumer emission (revoked **or absent** WORLD_READ) |
| `test_foreign_demand_cannot_be_labelled_complete[ProviderA/B]` | RED | **PASS** | `validate_demand_closure`: demand-relative source closure; foreign scope → `PARTIAL_DEFERRED`, `is_demand_complete=false` |
| `test_knowledge_asof_cannot_consume_future_publication[ProviderA/B]` | RED | **PASS** | `validate_knowledge_clock`: KNOWLEDGE_AS_OF may not consume a later publication without declared prior knowledge |
| `test_matching_issuer_string_cannot_authorize_foreign…[scope-A/B]` | RED | **PASS** | grant `scope` dereferenced to the source-closure binding |
| `test_matching_issuer_string_cannot_authorize_foreign…[target-A/B]` | RED | **PASS** | `binds.target`/`reverse_target` dereferenced to the request target |
| `test_direct_receipts_satisfy_original_frozen_envelope_schema` | RED | **PASS** | **true serializer** `port/envelope.py` emits exactly the pinned draft-2020-12 fields (0 jsonschema errors on both receipts) |
| `test_full_original_negative_state_distinctions_survive` | RED | **PASS** | complete **12-state** negative algebra with original codes (`DENIED_USE` not `DENIED`; + `NO_CURRENT`, `PROXY_MODELLED`, `UNKNOWN_UNOBSERVED_GAP`, `UNBOUND_RUNTIME_BINDING`) |

All **13** prior PASSes preserved unchanged (value intervention, issuer-string variant, H1/F1/F2/H3 + dual H2 refresh, changed-binding guard, independent provider equality, six frozen mutation classes).

## 4. Preserved suites and the new connection evidence

| Suite | Result |
|---|---|
| Candidate K9 8 + K10 28 (frozen expected classes loaded from oracles) | **36/36 PASS** |
| RC0 frozen independent 25 (byte-identical reviewer source) | **25/25 PASS** |
| **Connection oracle** (`port/test_connection.py`) | **6/6 PASS** |
| Pinned N10E 43 + C1 13 | **56/56 PASS** |
| Pinned PE author 21 | **21/21 PASS** |

**Actual sourcefree call path into pinned PE/C1/N10E (the seam RC0 found dead):**
`TwoContractAdapter.run()` now executes `provide_empirical_possibility_slice` (pinned N10E) → `compose_positioned_subject_possibility` (pinned C1) and the PE seam `serve_generic_world_situated_possibility` (pinned PE), with a nest-safe real call counter (`sys.setprofile`, no monkeypatch). Observed during run (ProviderA trace, `outputs/connection_trace_ProviderA.json`): modules touched `{PE, C1, N10E}`, 5764 call events including `provide_empirical_possibility_slice ×1`, `compose_positioned_subject_possibility ×2`, `serve_generic_world_situated_possibility ×1`. The served support (54/60 / 6/60 / n=60) is the **producer-computed** geometry; the adversarial control shows a static-hint-only lane raises `INTEGRITY_FAILURE` — static hints cannot satisfy the connection oracle.

## 5. Repairs at law level (what changed and why)

1. **Permission fail-closed** — the adapter entry refuses revoked/absent `WORLD_READ` before any consumer emission (RC0 counterexample 1 closed; the explicit `revoked_use` method remains as a second gate).
2. **Demand-relative closure** — `selection_state` is computed from the demand-vs-closure binding, never self-labelled COMPLETE; the candidate owns the partial-selection gate (`assert_complete_claim` → `PARTIAL_DEFERRED`), so K10_21 is a real candidate gate (RC0 counterexample 2 closed).
3. **Knowledge-as-of ordering** — a new law (`validate_knowledge_clock`) forbids lookahead: publication > knowledge cut refuses unless a separately bound prior-knowledge declaration exists. The frozen oracle baseline's own 2009-as-of/2010-publication pair is internally inconsistent; the candidate fixture's `as_of` is corrected **2009→2011** (disclosed in `02_EXECUTION_RECEIPTS.json#fixture_correction_disclosure`; the frozen oracle FILES remain byte-identical and the 2009/2010 pair is retained as the hostile lookahead case). (RC0 counterexample 3 closed.)
4. **Reversal dereference + independent issuance** — grants must bind `direction: REVERSE`, `reverse_target`, `reverse_risk_set`, `reverse_numerator`, `reverse_denominator`; scope/target/direction each dereference exactly; the reverse slice is computed **only from the grant's bindings** and carries its own issuance ref (`independently_issued=true`, `computed_from_forward=false` verified by recomputation, not a metadata flag). (RC0 counterexample 4 closed.)
5. **12-state negative algebra + true serializer** — the serializer emits `ScopedStatus` objects with the pinned 15-code enum; the code layer keeps its own Python constants (separate true serializer vs code enums). (RC0 counterexample 5 closed.)
6. **Facade lineage** — `round_trip_two_contracts` now binds and verifies consumer values/effects lineage (digests + value keys) and rejects silent discard (RC0's checker-scope limit closed).
7. **K10_21 candidate gate** — the partial-selection refusal is produced by the candidate, not the test body.

## 6. Honest limits and non-claims

- **Sourcefree fixture grade only.** The world remains an invented fixture; the empirical lane is computed through pinned producers over their own synthetic rows. No operative N9/N10W service, no model-use grant, no adoption, no canonical/PRE-MAIN/production change, no survey bytes, no V3/wake/weld/release, zero model or actor calls.
- The envelope requires non-null `model_authority_ref`/`use_grant_ref`; the serializer supplies **TEST_ONLY** refs (`fx:model-authority:test-only`). These are fixture-grade placeholders, **not** issuers; the reviewer is asked to adjudicate this single point (03 §4).
- RC0's nine PE REDs remain adjudicated as RC0 recorded (1 validation defect + 5 cross-owner dependencies + 3 reviewer-expectation problems); this repair does not alter PE and does not waive those integration obligations.
- `source_claim_grade`: `SOURCEFREE_REPAIRED_ADAPTER_CANDIDATE_WITH_PINNED_PRODUCER_CONNECTION`. Not an operative owner runtime, not original-source calibration, not N11/N12 readiness.

## 7. Evidence map

| Deliverable | Path |
|---|---|
| Frozen RC0 inputs + 12 RED register | `01_FROZEN_RC0_EXPECTATIONS_AND_REDS.json` |
| Execution receipts (per-suite counts, repair matrix, call trace, fixture disclosure) | `02_EXECUTION_RECEIPTS.json` |
| Independent I2 review request + hostile acceptance matrix + owner blockers | `03_REVIEW_REQUEST.md` |
| Repaired candidate | `port/` (`envelope.py` serializer, `pinned_producer.py` connection, `adapter.py` entry gates, providers, laws, consumers) |
| Staged frozen inputs (29 blob-verified objects) | `staging/` + `staging/staging_manifest.json` |
| Battery + JUnit/stdout + call traces | `repro/run_hq300_battery.sh`, `repro/*.junit.xml`, `repro/*.log`, `outputs/connection_trace_*.json` |
| Environment passport | `environment_passport_delta.json` |

Commands: `bash repro/run_hq300_battery.sh` (five suites, JUnit retained). RC0's 25 run from `staging/rc0/test_rc0_hostile.py` **byte-identical**.

## 8. Changed paths and remote verification

Changed paths (only): `WORKER_RETURNS/SOROK-R3-HQ300-C0-SC0-ADAPTER-RED-REPAIR-R1/` — the four documents above, `environment_passport_delta.json`, `conftest.py`, `port/` (12 modules), `staging/` (script + manifest + 29 pinned objects + RC0 runtime copy), `repro/` (battery, JUnit, logs), `outputs/` (connection traces, verdict ledgers).

Branch pushed (assigned branch only); exact remote HEAD verified by direct `git ls-remote origin agent/rabochii-sorok-r3-hq300-c0-sc0-adapter-red-repair-r1` after publication and reported in the completion message (a commit cannot self-reference its own future SHA). No self-adoption.

TERMINAL: `HQ300_C0_RC0_12_REDS_REPAIRED__13_PRESERVED__K9_8_K10_28_RETAINED__RC0_25_OF_25__PINNED_PE_C1_N10E_CONNECTED_CALL_TRACE__N10E_C1_56_PE_21_GREEN__NO_ADOPTION__NO_N9_N10W_ISSUANCE__NO_WAKE`.
