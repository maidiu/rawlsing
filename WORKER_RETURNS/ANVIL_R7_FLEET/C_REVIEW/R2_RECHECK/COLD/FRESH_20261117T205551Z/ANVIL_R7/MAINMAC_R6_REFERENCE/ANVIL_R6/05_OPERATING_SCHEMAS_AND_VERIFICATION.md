# 05 — One executable vocabulary, stages, outputs, verification and limits

## Source of truth

`contracts/policy.json` is the only verdict/grade enumeration used by R6 stage validators; it also defines physical metrics, workloads, lawful source-claim facets, graph domains and allowed transitions. `contracts/source_registry.json` is an exact cut/ID inheritance register, not a current-live source authority; its 118 IDs are 29 K1 + 26 PYAT-PC +14 P4R +10 SEAM B +8 SEAM S +8 ANVIL L +7 T +16 terminal. All 26 remain NOT_ADOPTED; 14 remain HELD. `contracts/boundaries.json` fixes T1–T7. Every other source is evidence or explanation, never an override layer.

`ANVIL_R6_PLAN_1`: H0 policy digest, immutable A0/B0 SHAs, selected decision scope, frozen material cells `(id, workload, dimension, metric, decision_id, source/runner/negative/first-consumer, both reversers)` and challenged exclusions; SHA-256 computed over sorted compact JSON excluding `freeze_digest`. `phase=BEFORE_FIRST_RESULT`. Any v2 must pass `amend` with parent plan and substantive B pre-result discovery. **Freezing a file cannot prove when the freeze happened**: actual commits/time/host evidence are examined by C.

`ANVIL_R6_MEASUREMENTS_1`: exact freeze digest; one row for each material cell, matching fixture hash and runner identity; A/B statuses `MEASURED`, `MODELED`, or `UNRUN_HELD`; measured nonnegative [low,high] and independently reviewable source/run/receipt evidence. The validator rejects A-only or missing raw identity from an unqualified ready selection.

`ANVIL_R6_SPINE_1`: source/policy sha256, exact cell comparator digest, `author_proposed_grade` from enumerated outcomes, selected A/B/UNDECIDED, raw evidence registry, provenance-specific source claims, whole-domain nodes/edges and five named routes with proper endpoints, all 118 original identities and protected 29/26/14 counts, material physical decisions each tied to comparison evidence and actual first consumer, positive/denied/restored source/semantic witnesses, truthful handoffs and real evidence-backed product delta. `builder_cold_start=PENDING_INDEPENDENT_C`. All other independent C/H1 claims are separate external frozen receipts.

`ANVIL_R6_STAGE_1`: `stage=H0|A0|B0|A1|B1|P15|P2|C|H1`; the exact `verdict` strings are enumerated in `contracts/policy.json`. The required per-stage fields and terminal truth table are in `tools/r6.py check_stage`. At P2 product deltas have only `PROPOSED_*` or `NO_NEW_PRODUCT_ADVANCE` grades; independent C/H1 alone may use verified product-advance grades. No `A_PROVED_AT_SCOPE` alias or other inherited R5 name. The complete return can have separate scientific, native, engineering and currentness conclusions, never a single magical `PASS`.

## CLI

```
python3 tools/r6.py check-plan FROZEN_PLAN.json
python3 tools/r6.py amend PLAN_v1.json PLAN_v2.json
python3 tools/r6.py compare FROZEN_PLAN.json ACTUAL_MEASUREMENTS.json
python3 tools/r6.py check-claim ONE_CLAIM.json
python3 tools/r6.py check-graph SPINE.json
python3 tools/r6.py check-handoff ONE_CARD.json
python3 tools/r6.py check-stage H0 H0.json
python3 tools/r6.py check-stage P15 P15.json
python3 tools/r6.py check-stage C C.json
python3 tools/r6.py check-stage H1 H1.json
python3 tools/r6.py check-spine SPINE.json PLAN.json MEASUREMENTS.json
python3 tools/r6.py render SPINE.json DERIVED/
python3 tools/r6.py check-render DERIVED/
python3 tools/test_r6.py
python3 tools/preflight.py
```

CLI exit 0 = **necessary structural/typed contract conditions met on supplied input**, not evidence a GitHub commit exists, the source was allowed, a real run occurred, a third party independently witnessed it, or that structural science is right. CLI exit 2 = RED defect in representation. Reviewer must check actual run/owner/cold source semantics, especially numeric intervals and `independent_checked` which a worker can type without proving independence.

## Six deterministic outputs

`DESIGN_DECISION.md`; `GLOBAL_ARCHITECTURE.json`; `DOWNSTREAM_BUILD_HANDOFF.jsonl`; `REQUIREMENT_CONSERVATION.jsonl` (118 exact inherited IDs, no false 118 builds); `EVIDENCE_AND_FALSIFIERS.tsv`; `OPERATIONAL_HANDOFF.md`, plus `RENDER_SHA256.json`. One changed SPINE implies regenerate and recheck all outputs. Don't manually edit a generated decision document and leave the source spine unchanged.

## Quality verification required before sending prompts

- Source R5 archive and PYAT HQ handoff exact uploaded SHA-256 noted in `evidence_frozen/input_hashes.json`; repo dynamic heads recut at H0.
- Syntax/static self-tests and adversarial mutation tests pass using actual `tools/r6.py`, not a mocked duplicate.
- No missing/broken source registry, unresolved launch-stage synonym, stale post-review acceptance in author P2, unknown C builder grade, fake H1 grant, new 26 adoptions or deleted 14 held obligations.
- Missing frozen digest, one metric for seven shapes, six excluded families, unrun rival, unqualified scientific original value, false WORLD_TO_ACTOR, forged product delta, placeholder READY handoff, disconnected global decision and nontransitively repaired architecture must not receive a ready verdict.
- A positive metadata sentence “the instrument omitted ancestry” is permitted while the forbidden respondent inference “the person lacks Lebanese ancestry” is rejected.
- A `SOURCE_STATIC`/synthetic sourcefree example remains at its exact stated grade; native/external grants are never simulation outputs.

## Responsible claim ceiling

All rendered decisions remain **author proposals**. C is actually independent only on real owner/host evidence; its cold builder may be specification-credible without executing real code. H1 receives only with real protected integration, CAS, paired CURRENT_PROGRESS and competent owner. Published GitHub issue/PR is NOT a launched worker. If current sources, session, rights, independent review or active edit lease cannot be established, state precise hold while lawful sourcefree work continues. The user's principal priorities remain controlling; don't let validator details replace product goals.
