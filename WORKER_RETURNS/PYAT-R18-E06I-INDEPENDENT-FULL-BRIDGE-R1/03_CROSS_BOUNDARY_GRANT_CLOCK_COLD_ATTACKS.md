# E06I — cross-boundary grant / clock / cache / cold attack log

Reviewer-authored. Every row was physically executed by the independent court in
`tests/test_e06i_independent_court.py` (48 cases) plus the reviewer observation
run (`repro/observe_court.py`). No author assertion is reused as independent
evidence; the author's 40-case suite was executed separately as **regression
grade only**.

Machine-readable results: `observations/e06i_independent_court.xml`,
`observations/e06i_independent_court.stdout`, `02_EXECUTED_ORIGINAL_OWNER_AND_BOTH_CLIENTS.json`,
`01_PRECOMMITTED_JOINED_NATIVE_ORACLE.json`.

## 0. What was reconstructed before any assertion

* Candidate `agent/userdirect-pyat-20261016-r17-e06-e04e05-native-bridge-r1`
  @ `f9c52113de38caececc450f0e54c980f64ed3981`; bridge SHA256
  `182818d96f27a853d02bcc977c1a143ef395498fb4cabca89f9c7c85e2dcec0e`.
* Native closure independently re-staged and re-verified from Git objects
  (`repro/verify_source_closure.py`): **402/402** entries match their
  NUL-header Git blob and SHA256; the **401**-object E05S closure @
  `f524f60781e2e7e72278d04d6377fb1da877698a` is reproduced byte-for-byte; the
  separately imported E04T owner @ `79cb8244a5291218bde17142b93fc2419eade396`
  (blob `2fdae6e07d…`) is exact; the five nonempirical E04T `product/` modules
  (`__init__`, `service`, `world`, `nonparent`, `scenario`) are byte-identical
  to the E05S-staged originals — no owner patch, no shadow replacement of
  `product.empirical` (blob `475feb9f9a…`).
* Observed physical import identities: `e04t_empirical` ←
  `runtime/owners/e04t_empirical.py` (E04T `79cb8244`), `product.empirical` ←
  `runtime/product/empirical.py` (`9c96f201`, blob `475feb9f9a`), E05R ←
  `runtime/e05_n9_selected_world_adapter.py` (`84485d32`); the two provider
  classes are distinct. **34** native modules imported in the observation run.
* Independent numerical oracle derived from the raw native source rows
  (`e03.synthetic_world_rows()`) **before** the court ran, and frozen in
  `01_PRECOMMITTED_JOINED_NATIVE_ORACLE.json`.

## 1. Positive current-grant joined path (not refusal-only)

| Probe | Observed |
| --- | --- |
| `A01` prepare/read on the exact candidate | `SELECTED_WORLD_VALUES_SERVED`; consumers exactly `NONPARENT_OPTIONS → OPTIONS_AND_SOURCE_SUPPORT_PRODUCED` and `CONCEPTION_SCENARIO_PROPOSALS → FINITE_PROPOSALS_EVALUATED`; both materials carry the same `snapshot_hash`; native readset `TWO_VALUES_READ_TEST_ONLY` |
| `A02` independent oracle vs executed | forward **18/32 → 10/16 → 6/8**, minority **14/32 → 6/16 → 2/8**, reverse **18/29**, Y0→1 **19/32 → 11/16 → 7/8**, support-loss early **12/24, 4/8**, terminal denominator **0** with `ZERO_SUPPORT` |
| `A03` two native field units | GSS **2,388,192/3,288,063** (subtypes sum 2,388,192, `GHANA_RURAL`, pub 2022-02-24) and NCA **23,414,527** (`GHANA_NATIONAL`, pub 2022-07-08); distinct units/geographies/source families; `pooling/person_exposure/model_use` all False |
| `A04` clocks | current `training_access=False`, `exit_cost=8`; historical `True/2`; empirical steps identical across clocks |
| observation run | real frames for `ingest_c11_source_release`, `execute_empirical_query`, `provide_empirical_possibility_slice`, `compose_positioned_subject_possibility`, `evaluate_positioned_subject_possibility`, `resolve_v558`, `materialize/validate_resolved_structural_context`, `_authorize_cached_use`, `consume`, `evaluate`, `serve`, `accept`; **58** respondent identities / **232** C11 events reconstructed from the accepted release; **60** compositions with the same concrete C1 evidence object reaching F8; both original client functions observed on the identical snapshot object |

## 2. Source-current grant withdrawal / restoration / reissue

| ID | Attack | Observed | Disposition |
| --- | --- | --- | --- |
| `B01` | warm positive, then remove the exact query authority from the attached registry; re-read same prepared request | `DEPENDENT_EMPIRICAL_USE_REFUSED`, `fresh_empirical_use_authorized=False`, `empirical_values=None`, **both** warm clients deny with `fresh_receipt=False`; E05R partial has no cells / no evidence; structural + native readset unchanged from the positive read | PASS |
| `B02` | repeat the withdrawn read (cache now cold after the refusal path) | no cells / no evidence; state is a typed partial, never `SELECTED_WORLD_VALUES_SERVED`; `fresh_empirical_use_authorized` never True | PASS (see residual R2) |
| `B03` | brand-new bridge whose query grant was never attached | no positive cells/evidence | PASS |
| `B04` | warm bridge, withdraw, then a **different empirical condition key** (cold cache key) — the naive "only cache hits are checked" bypass | no positive cells/evidence | PASS |
| `B05` | restore only the exact legitimate fixture grants, same acceptance | `SELECTED_WORLD_VALUES_SERVED`, same acceptance, receipt byte-equal to the original positive receipt | PASS |
| `B06` | does the refusal auto-issue / renew authority? | world source authorities, qauth and registry entry count unchanged | PASS |
| `B07` | old receipt as grant | `archive()` is `archival_only=True`, `fresh_use_authorized=False` in both states | PASS |
| `B08` | same-label successor grant (new version/content hash), foreign issuer, same-ref DENY, warm **and** cold | warm: refusal envelope or no-values partial; cold: no positive values; same-ref forged content raises an integrity `ValueError` | PASS |
| `B09` | same ref, `governed_operations=['FOREIGN']` — warm **and** cold | warm raises `CURRENT_NATIVE_QUERY_GRANT_CONTENT_MISMATCH` (integrity, never laundered to UNAVAILABLE); cold raises the same before any values | PASS |
| `B10` | a source-release authority put in `DENY` | no positive cells/evidence | PASS |
| `B11` | one source-release authority removed from the registry | no positive cells/evidence | PASS |

Key structural fact: the E04T owner authenticates the **currently attached**
registry on the cached-use path *and* the native composition re-validates the
query/source authority content on the cold path. Withdrawing the grant therefore
blocks values on both paths; restoring the exact grant restores the identical
receipt under the same acceptance.

## 3. Cache identity, issuer identity and mixed provenance

| ID | Attack | Observed | Disposition |
| --- | --- | --- | --- |
| `C01` | inject a prior-process public cache projection into a fresh bridge before its first `prepare` | `ValueError UNATTESTED_NATIVE_CACHE_ENTRY` | PASS |
| `C02` | mutate a warm cache entry and recompute its `content_hash` | `ValueError NATIVE_OWNER_CACHE_PROJECTION_MISMATCH` propagates as an integrity error; **not** turned into the grant-loss envelope | PASS |
| `C03` | replace a warm entry with a projection from a different source binding | `NATIVE_OWNER_CACHE_PROJECTION_MISMATCH` | PASS |
| `C04` | prepared handoff read by a different bridge instance | `E06_FOREIGN_PREPARED_HANDOFF` | PASS |
| `D01` | `release_ref` replaced after a valid acceptance | `ValueError` (binding/source changed), no values | PASS |
| `D02` | same release ref, foreign release object | `ACCEPTED_NATIVE_SOURCE_REPLACED` | PASS |
| `D03` | risk ref / permission root / model rule / coordinate ref mutated | `ValueError`, no values | PASS |
| `D04` | supplied consumer material with a tampered native field readset / foreign partial snapshot | `N9SelectedWorldRefusal CONSUMER_MATERIAL_NOT_EXACT_ORIGINAL_OUTPUT` | PASS |
| `D04b` | supplied **exact** original consumer material | accepted and reproduces the identical receipt | PASS |
| `D05` | one native role revoked in the adapter registry | typed partial; exactly one value removed; dependency readset, structural values, empirical steps and consumers unchanged | PASS |
| `D06` | explicit `adapter.invalidate(role)` | refusal reason `SOURCE_REVOKED`, distinct from rekey (`UNKNOWN_EXACT_FIELD_REF`) and publication (`NOT_PUBLISHED_AT_SELECTED_ASOF`); old receipt invalidated for fresh use while retained | PASS |

## 4. Historical publication clocks

| ID | Attack | Observed | Disposition |
| --- | --- | --- | --- |
| `E01` | `published_asof` precedes the empirical source publication | **no prewarm**: provider cache `{}`, `_accepted {}`, trace `[]`; `empirical_steps == []`; `empirical_state == UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK`; NCA refusal `NOT_PUBLISHED_AT_SELECTED_ASOF` | PASS |
| `E02` | clock denial followed by a current request on the same bridge | full positive current path (denial neither poisons nor pre-grants) | PASS |
| `E03` | serve a different clock's request against an existing acceptance/snapshot | `N9SelectedWorldRefusal`, no receipt | PASS |
| `E04` | arbitrary clock whose `published_asof` precedes the source publication | no prewarm, empirical `UNAVAILABLE` | PASS |

## 5. Cold restarts and stale permission

| ID | Attack | Observed | Disposition |
| --- | --- | --- | --- |
| `H01` | two fresh cold OS processes replay a persisted **restored** current-grant ledger | distinct PIDs, bit-identical serialized results, result receipt equals the original positive receipt, foreign projection rejected `UNATTESTED_NATIVE_CACHE_ENTRY`, real native `ingest_c11_source_release` frames present | PASS |
| `H02` | two fresh cold OS processes replay a persisted **withdrawn** ledger (stale permission) | distinct PIDs, bit-identical, no positive cells/evidence, foreign projection rejected | PASS |

Ledgers: `observations/e06i_cold_restored_ledger.json`,
`observations/e06i_cold_withdrawn_ledger.json`; per-process outputs
`observations/e06i_cold_{restored,withdrawn}_{0,1}.json`.

## 6. No installer / factory downgrade

| ID | Attack | Observed |
| --- | --- | --- |
| `F01` | after a valid E05 acceptance, replace `adapter.service` with the original `GenericSelectedWorldService` (E04R factory) | `E06_PINNED_E04T_PROVIDER_SUBSTITUTED` |
| `F02` | replace `service.provider` with `product.empirical.GenericProgressiveProvider` | `E06_PINNED_E04T_PROVIDER_SUBSTITUTED` |
| `F03` | mutate the live catalog records in place | `ValueError`, no positive service |
| `F04` | construct without literal `enabled=True` | `BridgeDisabled` before any native evidence |
| `G01` | imported producer identity | exact E04T owner file + Git blob; `product.empirical` distinct |
| `G02` | installation/issuance | `installed_OC05` is `NOT_YET_APPLICABLE` with `consumer_seam=None`; `issued_N5N6`/`issued_EE13`/`operative_N9`/`operative_OC05`/`new_issuer` all False |
| `G03` | frozen-contract immutability | SHA256 equals `01_FREEZE_SHA256.txt` and equals the pre-image at freeze commit `14f247b75` |

## 7. Bounded residuals (no value-bearing bypass found)

* **R1 — same-ref forged grant is an integrity error, not a typed refusal.** A
  same-ref query authority whose semantic content differs makes the E04T owner
  raise `ValueError CURRENT_NATIVE_QUERY_GRANT_CONTENT_MISMATCH`; the bridge
  propagates it. This is correct (an integrity error is never laundered into
  UNAVAILABLE), but callers must distinguish it from the grant-loss envelope.
  No values are produced.
* **R2 — refusal-state label depends on cache warmth.** The first withdrawn read
  returns `DEPENDENT_EMPIRICAL_USE_REFUSED`; a repeat after the refusal path has
  emptied the transient cache returns `TYPED_PARTIAL_SELECTED_WORLD` with
  `fresh_empirical_use_authorized` absent rather than `False`. Both are
  value-free refusals and neither serves a receipt; the label/reporting is
  inconsistent across warm and cold cache states.
* **R3 — process-wide runtime-authority fallback.** `AuthorityRegistry.resolve_exact`
  falls back to `current_runtime_authorities()` when an exact ref is absent. No
  runtime authority set is bound anywhere in this court, and the bridge never
  binds one, so withdrawal is enforced by the attached registry here. A future
  installing/operative court must confirm that no ambient runtime authority set
  can resurrect a withdrawn grant.
* **R4 — fixture revocation is not durable distributed revocation.** Fixture
  grants and process-local caches are not external signatures; this court does
  not test a real registry service or cross-machine revocation.
* **R5 — sourcefree grain.** All products are synthetic. No original
  SAV/DTA/PDF, U/E source, N5/N6, EE13/EE14, operative N9/OC05/N10W, N11/N12,
  canonical/CURRENT mutation, or actor/model use occurs or is authorized.
