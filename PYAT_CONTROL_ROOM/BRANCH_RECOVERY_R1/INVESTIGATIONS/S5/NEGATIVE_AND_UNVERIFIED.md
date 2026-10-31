# S5 NEGATIVE, INVALID, HELD AND UNVERIFIED REGISTER

**Return branch:** `agent/pyat-rabochii-845-s5-function-investigation-20261030-r1`  
**PRE-MAIN compared:** `750548ddbb9b4392a16ce93097b856f349e16182` (`integration/pre-main-reconciliation-r1`)  
**Rule:** a negative is retained even when a later repair exists. A later repair does not retroactively make the reviewed negative true of the later blob unless the exact blob was re-reviewed and the finding was closed.

---

## 1. Known reviewer negative cases

### 1.1 F7 temporal comparability — HQ213 to HQ248

| ID | Negative | Status / evidence |
|---|---|---|
| `F-DIR-01` | Required authorities were presence-only; a positive directional claim could be minted with fabricated refs. | HQ213 blocking finding; repaired in later temporal blobs, but final applicability remains bounded by HQ240/HQ232. |
| `F-DIR-02` | `TEMPORAL_COMPARABILITY` resolved without operation or governed-use scope. | HQ213 blocking finding; later repairs added scope checks. |
| `F-CARD-01` | Exact cardinality 2 for anchors was not enforced. | HQ213 blocking finding; repaired in later blobs. |
| `F-REASON-01` | `AUTHORITY_HASH_MISMATCH` / `AUTHORITY_SCOPE_MISMATCH` unreachable as reasons. | HQ213 major finding; repaired in later blobs. |
| `F-PRIOR-01` | Prior-F7 state map inert. | HQ213 major finding; later repair claims participation. |
| `F-RCPT-01` | Closed receipt omitted required fields and renamed `delta`. | HQ213 major finding; later receipt expanded; still not issuer-authenticated per HQ240. |
| `F-PROV-01` | Provenance did not carry all authority resolutions / operation identity / projection rule. | HQ213 major finding; later repair partially addressed. |
| `F-DELTA-01` | Delta was caller-minted, not bound to an authorized difference operation. | HQ213 major finding; later repair derives exact difference. |
| `F-REQ-01` | `comparability_requirements_ref` optional and unused. | HQ213 major finding; later repair made it required. |
| `F-ORDER-01` | No-basis + higher-precedence failure raised instead of applying precedence. | HQ213 medium finding; later adjudication changed behavior. |
| `F-XU-01` | Cross-universe law gated on caller boolean. | HQ213 medium finding; later repair derives from refs. |
| `F-COURT-01..05` | Vacuous or weak court tests (public-object/state-family, receipt, prior map, decorative authority fixture). | HQ213 medium findings; later courts claim repair, not re-run here. |
| `F-BACKFILL-01` | Self-referential backfill guard. | HQ213 low finding; later repair consults live frozen surface. |
| `F-NONE-01` | Missing registry produced `AttributeError` rather than typed refusal. | HQ213 low finding; later repair claims typed refusal. |
| `F7-RR-04B` | Returned owner decision did not prove the exact F7 request. | HQ220/HQ224; later repair claims closure for concrete owner. |
| `F7-RR-04C` | Hostile `SourceRelationResolver` subclass could counterfeit owner adjudication. | HQ224 blocker; later outer-dispatch repair. |
| `F7-RR-04D` | Exact resolver instance could shadow internal owner dispatch. | HQ226 blocker; later non-virtual dispatch repair. |
| `F7-RR-04F` | Live authenticated owner state exposed and post-construction replaceable. | HQ228 blocker; `_load_owner_state` returned the live state. |
| `F7-RR-04G` | Lexical custody ledger cell is caller-rebindable; transplant forges a positive. | HQ232 reproduced; HQ236 reproduced a narrower attack. **Still OPEN.** |
| `HQ240-DEFECT-F7-P07-ALIAS-TCB-001` | F7 producer binds `_authenticated_source_relation_decide` as a writable module global; alias replacement yields a positive bypass. | HQ240 adoption blocker; **no HQ T1 decision found.** |
| `HQ240-DEFECT-F7-TERMINAL-RELIANCE-002` | `TemporalRelationReceipt` is content-addressed but not issuer-authenticated; terminal reliance not inventoried. | HQ240 adoption blocker; **open.** |
| `HQ245-D1` | Stage A constructor out-of-bounds read; list/tuple subclass `__len__` lies reach the C loop; deterministic SIGSEGV. | HQ245 blocking finding; repaired later, inherited by Stage B. |
| `HQ246-B1..B4` | Stage B inherited OOB; malformed `PyObject_Call`; `PyErr_Fetch` NULL traceback; non-str replay field crash. | HQ246 blocking findings. |
| `HQ246-P1` | Positive decision parity failure: hardcoded effective scope/directionality. | HQ246 blocking finding; later R2 repair. |
| `HQ246-T1` | Trusted callables/classes caller-selected with no provenance; attacker classes seal and return attacker relation. | HQ246 blocking trust finding. |
| `HQ247-OPEN-001` | Stage B `decide()` leaks ~12–15 allocated blocks per call. | HQ247/HQ248 open named blocker. |
| `HQ248_TRANSITIVE_HELPER_GLOBALS_TCB_JURISDICTION` | Transitive helper globals TCB jurisdiction not proved/approved. | HQ248 `PROPOSAL_ONLY`; Stage B quarantined; production native ingress false. |

### 1.2 C3 / physical representation

| ID | Negative | Status / evidence |
|---|---|---|
| C3-02 `CHANGES_REQUIRED` | D02 item()-unwrapped timezone-aware datetime/time was swallowed and stringified; two independent reasons not acceptable. | HQ126 C3-02 independent integration review; C3-03 bounded correction then d3d8. |
| C3-03 execution | Static repair `PASS_AT_DECLARED_GRAIN`; execution qualification `BLOCKED_EXECUTION_CAPABILITY` (GitHub-hosted runner not assigned). | HQ126 C3-03 review. |
| C3 final execution rerun | HQ130 did **not** re-run the integration head; no lawful reviewer runtime available. Prior HQ-admitted qualification was 55/55. | HQ130 final disposition; this lane did not re-run it. |
| C3 adoption boundary | C3 approved source-free at declared grain only; it does not certify survey semantics, raw-source authority, full F1–F8, or PRE-V3→V3 actor implementation. | HQ130; OPS-01/04. |

### 1.3 R9 broker/session/binding

| ID | Negative | Status / evidence |
|---|---|---|
| HQ197 byte cap | `reader_bytes` cap could not fire because no `check(reader_bytes=…)` call existed; broker candidate partial. | HQ197 review; repaired by HQ197/HQ198 successors. |
| HQ201 binding defects | Route-pass applicability, retry-zero second attempt, completion before postconditions, discarded pyreadstat dependency injection. | HQ201 review; hardened candidate `deea4054…` repaired them. |
| HQ202 R9 ceiling | Accepted source-free at broker/session/binding grain only; source-dependent issuance, locator/approval, host preflight, cross-process uniqueness remain separate. | HQ202 disposition. |
| Current decoder conflict | R9 branch decoder `b406d45fae41…` routes through broker/session and D02, but drops current `_SourceSnapshot` read-only/stable/TOCTOU custody present in PRE-MAIN `8732e34d0ea3…`. | This lane's function/import comparison. Do not drop current custody. |

### 1.4 EE14 / G1 / source science

| ID | Negative | Status / evidence |
|---|---|---|
| HQ251 T1 serving custody | Existing T0 API route feasible, but T1 serving custody and exact selected-use grant unproved; no adapter authorized. | HQ251 R01 independent review. |
| HQ256 N02 HOLD | Competent EE14 issuer and exact selected use not established; all operative issuer/adoption/service/permission fields null/placeholder. | HQ256 N02; **HOLD**, not an empirical negative. |
| HQ261 T01 | G01 producer-origin defect affirmed; universal impossibility argument not proved; conditionally implementable service-owner custody boundary, not adopted. | HQ261 T01 independent review. |
| HQ254 S01 | LiTS I second-family candidate is **not admitted**; no world consumer proved; source meanings are retrospective appraisal/satisfaction, not measured institutional change. | HQ254 S01. |
| HQ260 S01 | Warrant not issuable: exact P1/Q301 role preimage and positive structural-use permission missing; source-specific science does not imply structural authority. | HQ260 S01. |
| C1 historical witness preimages | Four requested historical preimages cannot be reconstructed lawfully without guessing identity-bearing inputs. | HQ180/HQ181 C1-00 R5 disposition; preimage-specification failure, not hash mismatch. |

---

## 2. Invalid / trash-with-grounds functions (11)

All are in `rawlsing_next/pre553_source_relations.py` and are part of the blocked lexical sealed-owner attempt (`8053d30d306a…`, earlier `d9fb2c48ff6f…`). Reproduced grounds: RR-04F live-state exposure, RR-04G writable closure cell, HQ236 narrower coordinated substitution.

- `_authenticate_owner_custody_anchor`
- `_custody_relations_fingerprint`
- `_decide_from_owner_state`
- `_make_authenticated_decision_entrypoint`
- `_make_owner_state_store`
- `_make_sealed_source_relation_owner`
- `_owner_state_resolve_exact`
- `_relation_decision_replay_identity`
- `_resolve_exact_owner_snapshot`
- `_validate_positive_from_owner_state`
- `validate_relation_decision_replay_identity`

Do not integrate these as-is. The current PRE-MAIN `SourceRelationResolver` (blob `5b67e3f98a5faf95a6c82700af2346fef6e306a5`) remains the owner. The two refactor helpers `_relation_object_key_from_relation` and `_validate_relation_replay_identity` are classed `NEEDS_ADAPTATION`, not invalid.

---

## 3. Held unique-useful functions (20)

All are pure/helper-level functions of `pre553_temporal_comparability.py` final blob `6f6b462b1cde…`. No in-function defect was established by this lane, but the module is under an unresolved authority/TCB hold and was not adopted:

`AuthorityResolutionRecord.as_material`, `TemporalRelationReceipt.as_material`, `TemporalRelationReceipt.replay_identity`, `_bind_ref_to_material`, `_canonical_zero`, `_exact_difference`, `_exact_number`, `_exact_sign`, `_frozen_backfill_targets`, `_known_snapshots`, `_request_field_names`, `_require_authority_ref`, `_require_authority_tuple`, `_require_ref`, `_require_ref_tuple`, `_scope_is_adopted_unrestricted`, `_select_reason`, `_validate_kind_ceiling_pairing`, `_validate_receipt_cross_field_law`, `temporal_backfill_refused`.

Hold reasons: HQ232 RR-04G open in P07 custody; HQ240 writable module-global alias; HQ240 non-issuer-authenticated terminal receipt; HQ248 native ingress still proposal-only/quarantined.

---

## 4. Needs-adaptation functions (101)

### 4.1 F7/P07 boundary

`compare_temporal_anchors`, `resolve_required_authority`, `_relation_decision_defect`, `_temporal_evidence_identity_scope`, `_scope_covers_exact_ref_set`, `_scope_covers_governed_use`, `_scope_covers_universe`.

Grounds: dependency on blocked/absent `authenticated_source_relation_decision`; writable module-global alias; receipt issuer authentication; RR-04G. Current PRE-MAIN source_relations has no sealed entrypoint.

### 4.2 Physical decoder / R9 broker integration

`_decode`, `decode_sav`, `decode_dta`, `decode_in_session`, `_governed_source_sha`, `_build_variables`, `PhysicalSourceIncidence.iter_batches`, `PhysicalSourceIncidence.iter_batches.emit`, `PhysicalSourceIncidence.source_access_receipt`, `PhysicalSourceIncidence.selected_ordinals`, `PhysicalSourceIncidence.close_source_access`, `PhysicalSourceIncidence.__enter__`, `PhysicalSourceIncidence.__exit__`.

Grounds: b406 routes through broker/session but omits current `_SourceSnapshot` read-only/stable/TOCTOU custody; D02/D01 accepted C3 functions must be ported into the current decoder rather than replacing it wholesale.

### 4.3 Source-relation refactor helpers

`_relation_object_key_from_relation`, `_validate_relation_replay_identity`.

Grounds: useful decompositions of current resolver logic, but currently coupled to the invalid sealed-owner wrapper; extract only after the owner boundary is re-architected.

### 4.4 N10E owner-authentic lifecycle repairs (15)

`AnalyticalDependencyRegistry.assert_lifecycle_coverage_is_owned`, `AnalyticalDependencyRegistry.unreachable_determinants`, `AnalyticalProductRegistration.assert_complete_determinant_classification`, `AnalyticalProductRegistration.assert_no_unowned_determinant_claimed_covered`, `AnalyticalProductRegistration.unclassified_determinants`, `AnalyticalProductRegistration.unreachable_determinants`, `DeterminantOwnerEvidence.__post_init__`, `ExactDeterminantOwnership.__post_init__`, `ExactDeterminantOwnership.is_reachable`, `_assert_replacement_family`, `_authority_refs_at_path`, `_authority_snapshot_identity_material`, `_material_path`, `_owner_relation_path_allowed`, `assert_authority_snapshot_body_matches_ref`.

Grounds: these are real HQ225 repairs, but HQ226 finds authority overreach in the actual model-rule lifecycle: the runner seeds `AuthorityMaintenanceExecutor` with an unauthenticated model-authority snapshot, and the consumed model-rule identity is not represented/owner-authenticated in the dependency graph. The current PRE-MAIN accepted C1-03R blobs (`47e65aad5e0a…`) remain the accepted baseline; these N10E repairs require adaptation and a new authority court, not wholesale adoption.

---

### 4.5 Native P07 Stage A/B C functions (64)

Static C extraction found 64 meaningful functions across `rawlsing_next/_p07_native_owner_stage_a.c` and `_p07_native_owner_stage_b.c`. All are `UNIQUE_USEFUL_NEEDS_ADAPTATION` at the family level; early constructor variants are `INVALID/TRASH_WITH_GROUNDS` at variant level.

Variant-level `INVALID/TRASH_WITH_GROUNDS` additionally appears on the early `StageAOwner_init`/`StageBOwner_init` C blobs; the family row is `NEEDS_ADAPTATION` because later variants repaired the constructor. Known grounds: HQ245-D1 constructor OOB/SIGSEGV (`StageAOwner_init`/`StageBOwner_init` early blobs); HQ246-B1 inherited OOB; B2 malformed `PyObject_Call`; B3 `PyErr_Fetch` NULL traceback; B4 non-str replay crash; P1 positive parity failure; T1 caller-selected trusted callables; HQ247 open `decide()` leak; HQ248 Stage B quarantined, production native ingress false. ABI is CPython 3.11 C extension; no build/import/ABI/hostile run was performed by this lane.

### 4.6 Dispatcher JS — no needs-adaptation function

The adopted dispatcher current blob is `2db72c887b032622e09da6a5bd7723f7fb7055ee`; HQ193 adoption; HQ192 `ACCEPT_UNATTENDED_WITH_BOUNDED_RESIDUAL_LIMITATIONS`; HQ190 supervised base only. The 40 JS functions are `EXACT_ALREADY_IN_PREMAIN` at current; older HQ190 variants are `SUPERSEDED_BETTER`. Residual limitations (seatbelt/egress/sandbox context) are retained and not re-run.

## 5. Unverified branches and evidence gaps

### 5.1 No return or linked review evidence (25)

All 25 are **ancestors of PRE-MAIN** (`merge-base == tip`), so they carry no unique S5 content; their lack of a return document is an evidence gap, not a missing code delta.

`agent/reviewer-pyat-hq207-hc-r1`; `agent/reviewer-pyat-hq213-c1-current-dag-r1`; `agent/reviewer-pyat-hq218-hd-f8-authentication-final-rereview-r1`; `agent/vozhd-pyat-hq123-j2i-fanin-r1`; `agent/vozhd-pyat-hq124-six-stage-completion-adoption-r1`; `agent/vozhd-pyat-hq250-astra-d1d3-intake-and-frontier-r1`; `agent/vozhd-pyat-hq251-partial-s01-s02-intake-r1`; `agent/vozhd-pyat-hq252-s03-evs-return-intake-r1`; `agent/vozhd-pyat-hq253-r01-r02-intake-first-productive-test-r1`; `agent/vozhd-pyat-hq254-parallel-t0-and-empirical-frontier-r1`; `agent/vozhd-pyat-hq255-five-returns-and-routed-next-wave-r1`; `agent/vozhd-pyat-hq256-r01-n01-intake-parallel-r1`; `agent/vozhd-pyat-hq257-p02-n02-intake-r1`; `agent/vozhd-pyat-hq258-two-returns-binder-reviewed-evs-xlsx-r1`; `agent/vozhd-pyat-hq259-g2-adoption-and-evs-method-r1`; `agent/vozhd-pyat-hq260-selected-service-and-empirical-frontier-r1`; `agent/vozhd-pyat-hq261-four-hq260-returns-trust-and-empirical-r1`; `agent/vozhd-pyat-hq262-g3-adoption-g1-ghana-lits-r1`; `agent/vozhd-pyat-hqd125-ddm-functional-conservation-r1`; `integration/staging-pyat-hq263-return-intake-r1`; `integration/staging-pyat-hq265-fixture-reground-r1`; `integration/staging-pyat-hq266-query-parity-r1`; `integration/staging-pyat-hq268-independence-d1-d2-r1`; `integration/staging-pyat-hq269-e01-g1-fanin-and-qualification-r1`; `integration/staging-pyat-hq270-triple-return-science-g1-service-r1`.

### 5.2 Linked-review-only or control-room-only evidence

- `7` branches have only linked independent/integration review evidence, no branch-own return: HQ215 V556, HQ222 C5, HQ226 V555 (2 branches), HQ130 C3 integration, HQ264 G01 repair, HQ267 G01 hostile.
- `2` branches have control-room documentary delivery only: `agent/reviewer-pyat-hq202-r2` (commission only) and `codex/prev3-terminal-backward-audit-r1` (Astra delivery, `DOCUMENTARY_DELIVERY__NOT_HQ_ADOPTION`).
- `8` branches have fallback return documents with non-`00_*` names; they are indexed as fallback evidence, not as formal `00_RETURN.md`.

### 5.3 Missing or null disposition metadata

Several linked review documents expose a verdict only in prose or in a differently named JSON. Where `disposition` is `null` in `BRANCH_DISPOSITIONS.jsonl`, the full document path is retained; the null is not an acceptance. No disposition was inferred from a branch name.

### 5.4 Refs not in the S5 roster

Review documents and quoted return text sometimes name predecessor/candidate branches outside the S5 roster. Those names are evidence provenance only. They were not borrowed into the S5 roster, not classified, and not used as a substitute for S5 rows.

---

## 6. Method limitations and exact unknowns

- **Tests run: NONE.** No branch executable, test, import of branch code, pyreadstat read, raw survey read, response execution or model invocation was performed.
- **No fresh runtime proof.** All test counts are reviewer-claimed prior evidence, not re-executed here.
- **No semantic equivalence claim.** Exact equivalence means identical Git blob, identical Python AST, or identical lexical/body hash for the C/JS extraction at one path. Structural/no-identifier matches are candidate locators only.
- **No hash inversion or fixture guessing.** Historical preimages were not reconstructed; C1-00 R5 preimage-specification failure is retained.
- **No source or Sorok issuance.** Source scientific merit and Sorok actor permission are separate; neither is granted here.
- **No N9–N12 completion.** N9, N10E, N10W, N11, N12 remain `PROPOSED_NOT_COMMISSIONED` in the PRE-MAIN atlas.
- **PRE-MAIN may move.** The final comparison used `750548ddbb9b4392a16ce93097b856f349e16182`; a later PRE-MAIN head must be re-checked before any integration.
- **Tip date is not creation date.** Branch names and tip dates were not used as equivalence evidence.
- **Fixed function court.** `343` rows cover functions with at least one non-identical variant (239 Python, 40 adopted-dispatcher JS, 64 native C). Functions identical in every variant are enumerated in branch rows as `EXACT_ALREADY_IN_PREMAIN`; they are not duplicated as disputed court rows.

---

## 7. Exact `TESTS_NOT_RUN` reminder

`rawlsing_next/tests/test_closed35_g01_sav_numeric_representation_authority.py`, `test_closed35_d01_declared_encoding_admission.py`, `test_closed35_d02_opaque_datetime_carrier.py`, `test_current_gt2_structural_context.py`, `test_pre553_source_access_broker_court.py`, `test_pre553_source_session_court.py`, `test_pre553_execution_binding_court.py`, `test_pre553_temporal_comparability.py`, `test_pre553_source_relations.py`, the native Stage A/B build/import/ABI/hostile courts, the dispatcher Node harnesses, and every required regression court were **not run**.

Independent I2/I3 hostile adjudication at the exact SHAs in `FUNCTION_COURT.jsonl` is required before any integration decision.
