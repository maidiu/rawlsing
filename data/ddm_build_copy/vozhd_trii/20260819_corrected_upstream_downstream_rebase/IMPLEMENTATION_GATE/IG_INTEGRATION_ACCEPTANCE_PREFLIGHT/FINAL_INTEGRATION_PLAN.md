# IG-INTEGRATION — FINAL ACCEPTANCE / RECLOSURE PLAN

**Assignment:** `IG01-W08-INTEGRATION-ACCEPTANCE-PREFLIGHT-002`  
**Agent:** `IG_INTEGRATION_ACCEPTANCE_PREFLIGHT`  
**Class:** `INSPECTORATE`  
**Authority:** `NON_DISPOSITIVE_HOSTILE_INTEGRATION_PREFLIGHT_ONLY`  
**Mission branch:** `agent/vozhd-trii-ig-integration-acceptance-preflight`  
**Exact branch base:** `c7dfd69131d0909cd0e4a7bec223ba64ec5d6167`  
**Runtime writes:** `FORBIDDEN`  
**Semantic redesign:** `FORBIDDEN`

## Disposition

The final integration procedure is finite and dependency-correct. No semantic contradiction was found among accepted M1–M6, the accepted PSEPF zero-positive guard, and the frozen H01–H20/replay/noncollapse requirements.

The preflight itself can close now. **Final runtime integration cannot execute yet** because dispatch has not yet accepted an exact `IG_RENDER_BOUNDED_IMPLEMENTATION` return. The render implementation branch was visible with two in-scope files during inspection, but mutable branch state is not authority and is therefore not bound by this preflight.

This expected render wait is an exact future binding gate, not a request to redesign semantics and not a reason to invent a fallback.

## 1. Frozen cumulative M1→M6 spine

Final integration begins from the exact accepted cumulative M6 head:

`c7dfd69131d0909cd0e4a7bec223ba64ec5d6167`

The spine is linear:

`M1 e5f4871... -> M2 9357495... -> M3 f67c099... -> M4 83694e9... -> M5 b2d8636... -> M6 c7dfd69...`

Against production baseline `0777a34e50221bde6801dbaca26c058a7350c9e8`, M6 contains exactly twelve additive clean-sideline paths: six `rawlsing_next` runtime modules and their six tests. No legacy runtime file is modified by this spine.

The exact runtime import DAG is:

```text
M1 -> stdlib only
M2 -> M1
M3 -> M2
M4 -> M1 + M2 + M3
M5 -> M4
M6 -> M5 evidence types
```

This import DAG does **not** imply semantic permission inheritance. In particular:

- M4 may package only accepted structural producer semantics and rejects reverse-lane/actor/render classes.
- M5 structural eligibility is not actor-state mutation authority.
- M6 may inspect exact M5 evidence types only to reject direct behavioral use; there is no positive M5→M6 semantic edge.

Exact path/blob identities are frozen in `FINAL_INTEGRATION_BINDINGS.json`.

## 2. Accepted PSEPF sidecar — compose by exact content, not branch history

Accepted PSEPF head:

`dbed67bd83887afe310d9eeab827518d8cbf3a57`

It diverges historically from the cumulative M1–M6 branch at the production baseline. Its semantic contribution is exactly two files:

- `rawlsing_next/v3_psepf_zero_positive_guard.py` — blob `e0528d65215cb431196570c38bac4eae94217a1b`
- `rawlsing_next/tests/test_psepf_zero_positive_guard.py` — blob `21cfdee118d70d41def6ba654bbada5214cc1112`

Therefore final integration must **not merge the PSEPF branch wholesale**. It must materialize, recreate, or cherry-pick only these exact two file contents onto the accepted M6 tree and then verify:

1. both final blob identities equal the pins above;
2. no third path changed as a consequence of PSEPF composition;
3. the guard remains stdlib-only and does not import M1–M6 or legacy runtime;
4. the active positive transition registry remains exactly empty;
5. guarded empirical/structural/observer/analyst/provenance truth has zero actor/causal/RNG/scheduler effect absent a separately accepted exact owner.

A branch-history merge that introduces unrelated changes is a binding failure even if tests happen to pass.

## 3. Render binding — exact dispatch acceptance required

Accepted render **preflight** is pinned at:

`385651927ff74c0edf3bce55a5174dfc8e59951e`

with:

- preflight RESULT blob `7d391f25e65c6b32289d6659f27f3141ac377b7f`;
- M6→render binding requirements blob `56a1de6cb5bfb1d991ea92338a07ed994877cc92`;
- render hostile-fixture blob `14f74eda00add93b8f640ad8bac6f9b4b51c26c8`.

The implementation assignment allows only:

- `rawlsing_next/render_bounded_expression.py`
- `rawlsing_next/tests/test_render_bounded_expression.py`

At inspection time those two candidate paths were visible and path-disjoint from M1–M6 and PSEPF. Their candidate imports were M6-only. **They remain nonbinding evidence until dispatch accepts an exact return.**

Before final composition, the integration worker must re-read the render mailbox and require all of the following:

1. exact accepted return head;
2. exact return token `IG_RENDER_BOUNDED_IMPLEMENTATION_COMPLETE__READY_FOR_INTEGRATION`;
3. exact runtime/test path list;
4. exact runtime/test blob identities from that accepted head;
5. accepted head descends from exact M6 base `c7dfd69131d0909cd0e4a7bec223ba64ec5d6167`;
6. diff from M6 contains only the two authorized render paths;
7. render imports M6 by exact accepted runtime role and does not import M5/RSC/PSEPF/provenance/legacy runtime as a behavioral source;
8. render does not implement any blocked SPDM positive subpart.

Do not use branch-latest, file-name similarity, reflection, duck typing, mutable discovery, or the candidate blobs recorded during this preflight as a substitute for dispatch acceptance.

## 4. Final composition order

The safest final tree procedure is:

1. Create the final integration branch from exact M6 head `c7dfd69131d0909cd0e4a7bec223ba64ec5d6167`.
2. Verify the twelve M1–M6 paths against every blob in `FINAL_INTEGRATION_BINDINGS.json`.
3. Add the exact two accepted PSEPF files by immutable content identity; verify no unrelated changes.
4. Re-read dispatch and obtain the exact accepted render head/token/blobs.
5. Verify render's accepted diff against M6 and its import/authority closure.
6. Apply only the exact accepted render file contents to the integration tree if they are not already present by exact blob.
7. Prove final path uniqueness/noncollision across M1–M6, PSEPF, and render.
8. Run every accepted package-local test without modification.
9. Bind the frozen H01–H20 vectors to exact implementation surfaces and run the whole-machine cross-package hostile suite.
10. Run replay/noncollapse/path-law checks listed below.
11. Refuse acceptance if any negative fixture fails even if positive examples pass.
12. Produce the final integration acceptance/reclosure result; do not alter frozen semantics to make implementation pass.

## 5. Test execution order

Final integration must run at least:

1. `test_m1_temporal_v554_admission_dedup.py`
2. `test_m2_v555_atomic_route.py`
3. `test_m3_v556_higher_order_structural.py`
4. `test_m4_v557_v558_publication_repository.py`
5. `test_m5_runtime_rsc_peer_prior.py`
6. `test_m6_actor_safe_expression.py`
7. `test_psepf_zero_positive_guard.py`
8. exact accepted render test from the dispatch-accepted render return
9. a whole-machine integration acceptance harness mapping the frozen H01–H20 manifest to concrete accepted runtime surfaces.

This preflight does **not** create or authorize the executable whole-machine harness path. The final integration assignment must bind its exact path before writing it. Whatever path is chosen, the frozen H01–H20 IDs and expected verdicts may not change.

## 6. Whole-machine hostile requirements

The final harness must preserve all H01–H20 families from scaffold head `9fd7694049d8b6e79534c98cdd93a9f141302215`, including:

- temporal negative nonlaundering;
- duplicate support/route nonmultiplication;
- V555 identity and V556 participant identity preservation;
- role/order/cardinality/multiplicity integrity;
- item-wise V557/V558 permission monotonicity;
- provenance never becoming composition authority;
- RSC/PSEPF reverse-lane noncollapse;
- no prior-to-actor-state shortcut;
- independent structural/empirical currentness;
- prospective refresh without historical receipt rewriting;
- source disagreement not becoming actor uncertainty;
- actor-accessibility as sole positive M6 ingress;
- stale/deny/defer/integrity/session nonrestoration;
- no hidden joins or scope/permission widening;
- actor-safe ceiling not collapsed into complete person/phenomenology/rendering;
- lawful divergent lives plus deterministic exact-history replay;
- typed absence/valid-empty/denial/noncomparability/unknown/zero/defer/stale/integrity distinctions;
- no fabricated RSC;
- dispositive authority over feeder suggestions;
- no latest/fuzzy/nearest/network/LLM/random/default/session authority repair.

`WHOLE_MACHINE_HOSTILE_TEST_MATRIX.json` binds each family to its current accepted package-local evidence and the required final cross-package obligation.

## 7. Additional implementation path law

Final acceptance must also prove:

- exact twelve-file M1–M6 spine identity;
- exact two-file PSEPF sidecar identity;
- exact dispatch-accepted render path/blob identity;
- no legacy runtime imports;
- no runtime read of stage-close semantic artifacts as live data;
- no direct M5→M6 positive behavioral effect;
- PSEPF zero-positive registry cannot be bypassed by wrappers/aliases/metadata;
- render cannot consume M5/RSC/PSEPF/comparator/provenance via direct or indirect side channels;
- no session/transcript restoration;
- no hidden claim joins or permission/component/scope widening;
- deterministic replay at each declared owner grain;
- lawful render wording variability only when separately governed render/model/RNG receipts differ;
- no mutable-latest or heuristic reconstruction anywhere in integration.

## 8. SPDM gap is preserved and nonblocking

Positive SPDM subparts remain:

`BLOCKED_NAMED_AUTHORITY_REQUIRED`

This preflight found no authority that permits implementation of situated phenomenology, disclosure willingness/planning, salience, inhibition, affective foregrounding, interlocutor-specific openness, or psychological register selection.

Final integration must therefore prove two things simultaneously:

1. these positive semantics are **not** implemented, inferred, defaulted, guessed by a model, or recovered from actor-safe/RSC/PSEPF/session material;
2. their absence does **not** prevent independent acceptance of authority-complete M1–M6, PSEPF guard, and bounded render realization.

If a render operation actually requires one of these missing positive decisions, that operation returns `BLOCKED_NAMED_AUTHORITY_REQUIRED`; it is not silently filled.

## 9. Failure classification

- **Exact path/head/blob/import binding missing or mismatched:** return bounded exact-binding failure; do not guess.
- **Implementation violates a frozen semantic invariant:** return to the owning implementation package for repair under its existing authority; do not amend semantics here.
- **A genuine contradiction proves frozen semantics cannot be jointly satisfied:** return semantic conflict to HQ with the exact counterexample.
- **All exact bindings and hostile/replay/noncollapse tests pass:** final integration may return its separately authorized acceptance token.

## Preflight conclusion

The composition strategy is closed and testable. M1–M6 and PSEPF are exactly pinned and collision-free; render has a finite acceptance contract and two-path scope but still awaits dispatch acceptance of its exact runtime return. No semantic harmonization is warranted.

Preflight return:

`IG_INTEGRATION_ACCEPTANCE_PREFLIGHT_COMPLETE`
