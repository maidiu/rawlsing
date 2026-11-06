# B07 / Court B — FIABC/LiTS exact 3-failure, two-blob and owner matrix

**Source cut:** `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`. **CI evidence:** [Rabochii governed bounded court run 41999468763](https://github.com/maidiu/rawlsing/actions/runs/41999468763) / job `127150756725`, 2026-11-05, `144 passed, 3 failed in 53.01s`, exit code 1. This is a previously executed CI result inspected by B07, **not** a B07 S2 test. The separately scoped [canonical guide integrity run](https://github.com/maidiu/rawlsing/actions/runs/41999468495) succeeded. The protected PRE-MAIN merge [8ffec40](https://github.com/maidiu/rawlsing/commit/8ffec40a6924848a49f95950aa9ce28c27ee3ec1) explicitly did not repin or waive the three historical negatives.

## Exact frozen tests and observed failure rows

| # | Exact test node / assertion | Historical expected Git blob | Current protected Git blob | What it checks | Source of frozen expectation / owner |
| --- | --- | --- | --- | --- | --- |
| F1 | `rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py::RuntimePackagingRebindTests::test_lits_authority_overlay_v2_pins_integrated_normalized_sourcebacked_scope`; line 181 | `f808dfcd2008cc71e9203de3cadf1abe14223974` | `64555ce46807b815c6e26cb46b35622c73efe5ab` | `rawlsing_next/_pre553_query_eval.py` must equal `source_free_successor_components` value in [LiTS runtime authority overlay v2](https://github.com/maidiu/rawlsing/blob/8ffec40a6924848a49f95950aa9ce28c27ee3ec1/rawlsing_next/runtime/ee_p2x/03_LITS_RUNTIME_AUTHORITY_OVERLAY_BINDING.json) | FIABC W3/I04 LiTS runtime packaging/authority overlay; qualified original LiTS/FIABC proof and I03 succession owner |
| F2 | `rawlsing_next/tests/test_fiabc_final_preflight_fanin.py::test_live_candidate_c_and_packaging_bind_final_hq_state`; line 160 | `47893688ed455ced2c2f2311ad0aead6fb5bf2d2` | `c2451b1b9d54b9588455022e0d6625083bb955d2` | Current `rawlsing_next/pre553_candidate_c_production_binding.py` compared to `C_BINDER_BLOB` historical literal | FIABC final T2→T5 packaging/preflight author, Candidate-C policy/owner and qualified sourcefree succession receiver |
| F3 | `rawlsing_next/tests/test_fiabc_final_preflight_fanin.py::test_t5_contract_binds_final_successor_and_lits_current_law`; line 194 | `47893688ed455ced2c2f2311ad0aead6fb5bf2d2` | `c2451b1b9d54b9588455022e0d6625083bb955d2` | Current binder compared to `T5.preservation_anchors.t2_current_binding.candidate_c_module.blob` | Original [T5 six-cell court contract](https://github.com/maidiu/rawlsing/blob/8ffec40a6924848a49f95950aa9ce28c27ee3ec1/WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json); original qualified FIABC/HQ proof-custody owner |

**Supporting test blobs:** [W3/I04 test](https://github.com/maidiu/rawlsing/blob/8ffec40a6924848a49f95950aa9ce28c27ee3ec1/rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py) Git blob `fea5a0457062ce639f42d75c470ec89a9dbea531`; [T5 preflight test](https://github.com/maidiu/rawlsing/blob/8ffec40a6924848a49f95950aa9ce28c27ee3ec1/rawlsing_next/tests/test_fiabc_final_preflight_fanin.py) blob `d9a6c263bf44d86994cb562e835efffe7734c6f0`. LiTS overlay blob `e9117e7757ceb81e32c133730632c8d20c5cb24e`; T5 contract blob `839141fa41dde455b59501380f90e81f2b6f3ea3`.

**Count interpretation:** 3 failing assertions; only 2 differing live source paths; **1 repeated Candidate-C expected blob**. F2 and F3 are two distinct preservation contracts with the same literal, not evidence of two distinct binder regressions.

## Direct Git-blob lineage comparison — not inferred from hash inequality

The two historical expected Git blobs and two current protected Git blobs were read directly from Git objects and compared in this S0–S1 investigation; there is no claim of performing a native six-cell execution.

### F1: I03 evaluator, old 727 lines → current 728

Old `f808df...` to protected `64555ce...` includes:
- Introducing `dataclasses.replace` and `_select_respondent_events`, using `_EventRead` in typing.
- Replacing the prior full scan of `index.events_by_respondent[respondent.ref.key]` filtered through `_event_matches_target` with `_select_respondent_events(index, respondent.ref.key, component.target_ref, include_component=True, states=component.included_states)`.
- Replacing mutation of `index.runtime_authorities`, `index.runtime_repository` and `index.runtime_predicate_grammar_authority_ref` with a tuple of `replace(index, ...)` local to evaluation.

These are plausible **sourcefree efficiency and isolation repairs** (selector and bounded authority scope), not meaningless byte shuffling. Git history for this file includes September 22 LiTS repairs and later November 4 sealed-release topology and November 5 compact C11/Parquet operations. The independently accepted E1/E3 [PR #684](https://github.com/maidiu/rawlsing/pull/684) and P1/P1F1 [PR #686](https://github.com/maidiu/rawlsing/pull/686) demonstrate bounded sourcefree I03 and compact first-reader capital. However **neither passing sourcefree local fixture nor accepted P1 ABI scope automatically proves equivalence to the original FIABC six-cell LiTS/WVS contract**. Need exact same first-reader and full source-/risk-set-/denominator-/event-order parity negatives, with approved sourcefree inputs.

**F1 provisional class:** `OLDER_IMMUTABLE_PROVENANCE_EXPECTATION_CONFLICTS_WITH_LATER_SCOPED_ACCEPTED_CODE`. No observed failure in actual I03 query evaluation is established by this hash assertion. `REAL_REGRESSION_UNKNOWN` until qualified source-specific first-reader differential; `OWNER_REQUALIFICATION_REQUIRED`. Do not rewrite the frozen LiTS overlay: it accurately records its own historical source cut.

### F2 and F3: Candidate-C binder, old 414 lines → current 442

Old `478936...` to protected `c2451...` adds optional `common_semantic_result: tuple[C11Repository, Any] | None` across binder/wrappers. Default behavior still builds through `build_source_backed_c11_repository(source, projection, cache=None)`. When common semantic result is supplied, the new branch checks an exact tuple, repository instance, release reference, source SHA, `repository.resolve_release_exact(release_ref)`, and release **object identity**; it refuses a foreign/common result not represented by that repository. This provides a controlled way for physical Candidate C to consume common Candidate B-approved semantic C11 result while retaining Candidate-C policy, rather than inventing separate semantic truth.

Git history identifies [commit 818a17908dd0d8c16b8054da80beb765854ae92b](https://github.com/maidiu/rawlsing/commit/818a17908dd0d8c16b8054da80beb765854ae92b) (“FIABC RUN3: qualify source-free repair stack”, 2026-09-24) as source of this change, **after** T5’s Sept 21 frozen blob. The [RUN3 return](https://github.com/maidiu/rawlsing/blob/8ffec40a6924848a49f95950aa9ce28c27ee3ec1/WORKER_RETURNS/FIABC-RUN3-POSTMEASUREMENT-REPAIR-STACK-R1/00_RETURN.md) reports original repair suite 115/115, sourcefree successor 24 tests/28 subtests, preflight 11/11 and candidate processes/outputs 0/0; it explicitly says `HQ_PROMOTION_REQUIRED`. A later sourcefree test may be valid without rewriting the older T5 owner identity. **No measured P2X candidate run or original survey semantic/science grant follows.**

**F2/F3 provisional class:** `OLDER_T2_T5_PROOF_CUSTODY_PIN_VS_LATER_FIABC_RUN3_COMMON_TRUTH_REPAIR`; not `STILL_IDENTICAL`, not `PROVEN_BAD_CODE`, not `UNCONDITIONALLY_SAFE`. Old T5 is historically correct **about the old binder**. A future current-successor claim needs a distinct, qualified versioned identity/equivalence receipt.

## Immutable scientific/proof contracts that remain controlling

[Final T5 contract](https://github.com/maidiu/rawlsing/blob/8ffec40a6924848a49f95950aa9ce28c27ee3ec1/WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json):
- `RAWLSING_FIABC_T5_CURRENT_SIX_CELL_COURT_CONTRACT@1.0.0`, explicit `CURRENT_CONTROL_CONTRACT__NO_MEASURED_RESULT`.
- Six ordered cells: LiTS-I A/B/C, WVS7 A/B/C; candidate A/B/C frozen owners; Candidate C `SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS`. LiTS permits only bounded CACC1/CACC2 with exact fallback and no CACC3; WVS7 source-backed, no WVS-specific accelerator.
- Source/release/Lock2/oracle identities, LiTS cross-schema logical-candidate identity (50 logical candidates; native hash equality **not required**) and WVS7 current 46-candidate successor stream remain separately pinned.
- Full terminal is **I05 learned empirical product, exact semantic replay output identity, complete coverage and constituent I03 fact closure**. C11-only, partial I03 or a sourcefree preflight is NOT T5 full-terminal proof.
- `R35` convergence and T4 process/accounting/negative-state requirements are not waived; no measured 35-source/105-cell or original-source native status is inferred.

[LiTS overlay](https://github.com/maidiu/rawlsing/blob/8ffec40a6924848a49f95950aa9ce28c27ee3ec1/rawlsing_next/runtime/ee_p2x/03_LITS_RUNTIME_AUTHORITY_OVERLAY_BINDING.json) freezes the sourcefree successor dependency set and explicitly says `measured_p2x_authorized:false`. Its historical old `_pre553_query_eval.py` identity remains meaningful as an archival root. It should not be silently retconned to claim that it originally approved November’s replacement.

## Owner/acceptance court — four possible final outcomes

1. `STALE_PROVENANCE_EXPECTATION_CONFIRMED_WITH_VERSIONED_SUCCESSOR`: competent FIABC/T5 provenance owner endorses the later substitute against the exact sourcefree authority and first-consumer invariants; preserve original frozen overlay/T5, publish a **new** successor receipt with old→new code/event/owner binding, separately independently reviewed. Do not use this status before the comparative proof.
2. `IMPLEMENTATION_REGRESSION_CONFIRMED`: exact sourcefree differential/falsifier proves a real I03 denominator/role/event/candidate C11/semantic replay difference. Then repair smallest live source behavior under qualified code owner, with independent review; don't use a pin update to bury it.
3. `ACCEPTANCE_DISAGREEMENT`: both code behaviors can be exercised but the original T5/FIABC semantic owner rejects the proposed common C11 or compact replacement as preserving accepted meaning/scope. Qualified FIABC original scientific/meaning owner adjudicates; no engineering self-issuance.
4. `UNRESOLVED_AUTHORITY`: code tests plausible but historic proof owner unavailable, missing source rights, or no qualified independent six-cell comparator. Keep `3 RED` and request named owner/right, with current historical sourcefree capital still preserved.

**B07 current outcome:** #4 with strong concrete evidence favoring a *versioned successor provenance conflict* (not simple implementation break). No terminal accepted FIABC outcome determined by B07.

## Narrowest repair/first-reader package to request

- Recover exact frozen original source/owner contract and current accepted proof cuts. Evaluate F1 with original selector and compact selector using identical sourcefree event sequence, filter/component, respondent, risk set, denominator, typed missingness, replay and predicate authority; detect stale per-evaluation runtime binding vs current copy-on-evaluate. Require correct refusal on poisoned/foreign authority and invalid compact cache. A current SOURCEFREE qualified proof must expose actual I03→I05/R04/R05/P41 reader when that edge is claimed, not only a hash check.
- Evaluate F2/F3 with `common_semantic_result=None` and exact approved shared result; verify exact repository identity, source SHA, release/replay ID, Candidate C identity retained; counterfeit mismatched tuple/source or foreign release MUST refuse. Use the existing RUN3 preflight and frozen A/B/C owner; do not reimplement Candidate-C.
- Original FIABC proof owner issues either a scoped successor identity/equivalence contract or a precisely named implementation defect. Independent receiving review tests the specific assertion and fault; competent protected owner makes any CAS. **Never edit frozen historical T5 or overlay to force an apparent GREEN**. Historical RED remains until an accepted current-proof path exists.
