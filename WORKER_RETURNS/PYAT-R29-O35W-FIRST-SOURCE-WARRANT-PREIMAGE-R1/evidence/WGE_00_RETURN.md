# PYAT HQ280 WGE — Pre-result expected work and real E2B consumer — RETURN

**Terminal:** `HQ280_WGE_VISIBLE_KEY_REPLAY_AND_PRE_RESULT_EXPECTATION_REVIEWED__EXISTING_E2B_CONTEXT_RUNTIME_MEASURED_OR_EXACT_HOLD__NO_SELF_ADOPTION`

**Authority:** HQD-2026-10-10-280; HQ WGD adjudication `43aeba547b27a2f5e58d734cc1ff9dfcfd0b6901`. Canonical `6a8c91d99dca1ae2fd3559ba3c11ee26649e3cd9`; semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` — neither mutated. Branch `agent/rabochii-pyat-hq280-wge-preoutcome-gt2-e2b-positive-r1`; sealed tip `d14fefd5e7e67cee5f73b4955746dfd8578c74c4` **verified** (commission commit recovered from the local git repository; branch not checked out locally).

**Required inputs verified:** `PYAT_HQ280_WGD_EXACT_OPERATION_AUTHORITY_BRIDGE_RETURN_R1.zip` SHA-256 `71de4492b69358fe1ee48e6eb2ac51d62ebb6110402dddd30ee734506a7ff0e3` — exact match; `PYAT_HQ280_WGC_CORRECTED_PERMISSION_SHAPED_LEDGER_RETURN_R1.zip` `8fa58dec…` — exact match. WGD originals untouched (read-only derived overlay).

**Execution substrate:** OpenCode / Step 5 Preview Free, local Mac, python 3.11.3; deterministic scripts under `repro/`. **No repo test-only file authored, no production edit, no raw SAV/DTA, no canonical/PRE-MAIN/.rabochii mutation, no new issuer/consumer/actor/world grant, no self-adoption.**

## 1. Correction 1 — typed-obligation key replay repaired (01)

Confirmed the HQ defect: **0/3,142** WGD typed-obligation keys replay from published fields; **3,142/3,142** replay only with the undisclosed `orientation=TYPED_OBLIGATION` substitution. Repair (read-only derived overlay, no WGD edit):

- **Exact original preimage published per row**, making every superseded key fully replayable (`all_superseded_keys_reproduced_from_disclosed_preimage: true`).
- **Declared successor rule** — `sha256(source|wave|impl_id|var|label|purpose|orientation|entry_class)[:32]` — a pure function of **published fields only**; successor preimage published per row; no hash-affecting material hidden in code.
- **Succession manifest** 3,142/3,142 old→corrected rows; successors unique, distinct from superseded, no collision with the 78,037 annotation keys; 78,037 annotations untouched; 8 directional + 11 fail-closed denial states preserved; **zero obligations schedulable**; all authorized keys still null.

## 2. Correction 2 — pre-result expectation vs actual product (02)

WGD's `ecb7411003a96966d703fc88a28d973b` is **RETIRED** (`REJECTED_AS_PRE_OUTCOME_EXPECTED_WORK_KEY`): it keyed on the produced `EmpiricalFact` hash (a false-positive T08). Replaced by a **PROPOSED pre-result-only expectation** `2ee8980a96a73351102c9b814f5d51464c2e7b2d1d625da6f3be8b3dc60e437a` whose published preimage (full 64-hex, material published in full) is verified by exact dependency-lineage audit to contain **no** fact hash, query/predicate/replay hash, C11 release hash, produced F1 object/content hash, FF profile hash, V557/V558 publication/repository/resolution key, observed numerator, batch membership or invocation receipt.

- Built from accepted pre-result authorities only: GT12-A source/risk/role/target-use/query issuers; the frozen C-to-D relation rule `cddf66e2…` (Q86B CONDITIONER → Q86A TARGET, IDENTITY_ONLY state order, NONE information loss); risk set `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`; RAW/F1-only/ALLOW_CONTEXT_ONLY/CONTEXT ceiling; the existing harness consumer; frozen canary/closure commits. No fabricated `AuthorityRef`.
- **Honest limits:** constructed 2026-10-11; does **not** claim to predate the historical GT2 execution; frozen before this fresh invocation, establishing prospective authority only; adoption is a competent HQ/issuer decision — `PROPOSED_CANDIDATE__REQUIRES_COMPETENT_HQ_OR_ISSUER_ADOPTION`.

## 3. Real E2B CONTEXT consumer execution — MEASURED (03)

Executed the **existing accepted owners only** on committed R4A bytes after verifying all four transport SHA-256s (`c2d008a9…/9c34860a…/9ab1b532…/2fa09161…`):

- **Exit code 0**, wall 18.3 s (load 3.6 s + run 13.6 s); real stdout/stderr, command, timestamps and SHA-256 retained; **deterministic across two runs** (identical terminal core).
- Typed terminal: relation `SUPPORTED` (conditioner `2fb3a626…` → target `67f036c0…`, domains incl. DK/NOT_ASKED/REFUSAL/MISSING, target domain `afb1ff07…`, risk `0484fa5c…`); admission `ADMITTED / EXACT_GT2_RELATION_ADMITTED_FOR_STRUCTURAL_MEDIATION_INPUT` (FF profile `1ffdfe53…`, owner FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER); M1 `ELIGIBLE` under `GT12_GT2_Q86B_CONDITIONAL_SUPPORT_Q86A_F1_CONTEXT_PUBLICATION@1`; **F1 `3530f08f…` (content `a008553d…`)** published F1-only (`V557PUB:2c7fb3f8…`, ALLOW_CONTEXT_ONLY); V558 repository `47594be9…`, resolution key `205f5049…` with CONTEXT permission subsets verified; V3 guard `DENY_ZERO_EFFECT / ZERO_POSITIVE_REGISTRY` with actor sentinel `GT12_E2B_NO_ACTOR_PROMOTION_SENTINEL`.
- **36-cell geometry proved separately from the fact** (V558 resolution returns identity+permission only): 36 native cells = 13 `OBSERVED_POSITIVE` + **23 `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET`**, raw numerators summing to 19,210 — independently agreeing with the HQ221/LR-C lineage.
- Execution class: **fresh execution of an existing retained product — not remeasurement, not new science.** Raw source bytes never opened.

## 4. Independent hostile results (04) — 9 executed PASS, 0 fail, 2 honestly UNEXECUTED

(a) typed key preimage replay; (b) expectation key invariant under an alternative result world while the product fact hash would differ; (c) no invocation-derived expected set; (d) own-`_dk` and invented exact routing remain held; (e) 592 held-science + 8 directional denials remain not-ready; (f) committed transport SHA pins + tampered payload detected; (g) **no false F1/B1 publication** (F1-only published; no B1/F2 in publication); (h) causal/review/V555/objective/actor use refused (V3 `DENY_ZERO_EFFECT`, CONTEXT ceiling); (i) source/permission substitution refused (producer fact/query match pinned constants; 5 exact authority refs). (j) cross-interpreter replay and (k) issuer adoption are `UNEXECUTED` — never graded PASS.

**No-drop classification:** one pre-result expectation vs one executed retained product (not the 78,037 documentary annotations); 0 omissions; status `PROPOSED_CANDIDATE_NO_DROP` because the expectation is not yet adopted.

## 5. Issuer scope and adoption holds (05)

Adoption of the pre-result expectation, per-operation issuer coverage for 78,036/78,037 annotations, all 3,142 obligation holds, the 564 temporal and 2,980 co-topic permutation holds, and current F1/B1 byte-custody remain **competent HQ/issuer decisions**. The existing E2B CONTEXT use is preserved and unchanged; WGE extends, revokes and re-derives nothing, and self-adopts nothing.

## 6. Package

**`/tmp/rawlsing_hq280_WGE/PYAT_HQ280_WGE_PREOUTCOME_GT2_E2B_POSITIVE_RETURN_R1.zip`** — non-sensitive final reports: `00_RETURN.md`, `01_TYPED_OBLIGATION_KEY_SUCCESSION.json` (+ 9 `01_SHARDS/`), `02_PRE_RESULT_EXPECTED_OPERATION_VS_ACTUAL_PRODUCT.json`, `03_GENUINE_E2B_RUNTIME_EXECUTION.json` + `03_runtime_stdout.log` / `03_runtime_stderr.log`, `04_INDEPENDENT_HOSTILE_TESTS.json`, `05_ISSUER_SCOPE_AND_ADOPTION_HOLDS.md`, `06_EVIDENCE_MANIFEST.json`, `repro/` scripts. No repo test-only file was authored, so nothing was pushed.

**Disposition:** both corrections completed, the existing E2B CONTEXT runtime **measured**, the pre-result expectation **proposed pending competent adoption**, all remaining authority explicitly held. No self-adoption.