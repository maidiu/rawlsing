# ALTERNATIVE AND COUNTEREXAMPLE — strongest rival design, and the case that most threatens mine

## 1. The strongest alternative I rejected

**Residual-manifest S1.** Instead of a per-row locator for all 118 identities, store one manifest: `{path → sha256, git_blob}` for the three K3 TSVs, SEAM/25, SEAM/26, ANVIL/15, `02`, `03`, plus a `census` array of the 118 ids. S1 passes if the manifest hashes match and the census has 118 entries. The decision then reconciles the census.

**Why it is genuinely attractive.**
- ~40 fewer lines of gate code; one artefact per source file.
- Impossible to "hallucinate a row hash", because rows are not individually asserted.
- Deterministic and trivially auditable by anyone who can run `shasum`.

**Why I rejected it — the decisive counterexample.**
Take the real `SEAM_25.md` bytes. Delete the single table row `B-10`. Recompute the file hash. Under residual-manifest S1 with a matching rebuilt manifest, **every check still passes** and the census still has 118 ids if the id list is copied from `03_FROZEN_SOURCE_CUTS.json`. The identity is then a *name without a body*: the decision can map `B-10` to "preserved" using a sentence about something else, and nothing notices.

This is not hypothetical: it is exactly required negative test #3 ("missing row/blob or **B10** RED"). The per-row locator catches it (`HISTORY:ID_SET_DRIFT:SEAM_B` plus `ROW_NOT_IN_SOURCE`); the manifest design cannot, unless it re-introduces per-row hashes — at which point it *is* my design with fewer checks.

**Second rival: "hash the whole SPINE and trust it".** Rejected for the reason in `GROK_PROOF.md` §3 and §8: two parties hashing the same bytes proves agreement, not source truth, and the SPINE was never produced.

## 2. The strongest counterexample against my own design

**The fluent-but-wrong disposition.** My S3 anti-boilerplate rule requires only ≥2 distinctive token overlap between `candidate_specific_effect` and the located `source_semantics`. A decision author can write:

> For `K1-CAP-03` the selected candidate **preserves respondent reuse** by keeping a **partial** incidence route, so the current first reader returns the same conditional.

This shares `respondent`, `reuse`, `partial` with the K3 row, passes the token floor, and can still be **substantively false** (e.g. the candidate actually collapses occurrence identity). My gate returns `PASS_LOCAL_INTEGRATED_DECISION_PENDING_C`.

**Consequence I accept.** The gate is a *floor against silence and copy-paste*, not a semantic referee. The only defence against a fluent wrong claim is independent C reading the actual code and the actual source rows — which is why C's `boundary_court` requires positive/negative/restore and why the six projections expose every row for cold reading (`COVERAGE_TO_DECISION.tsv`).

**A second self-counterexample, on C.** My `boundary_court` accepts `SOURCE_STATIC_CONSERVED` for `positive`/`negative`/`restore` with `evidence_grade: DOCUMENTARY`. That is honest but weak: seven documentary triples can coexist with a candidate that has never executed anything. I did **not** make `ACTUAL_PROVED_AT_SCOPE` mandatory, because that would reintroduce a false block for `FUTURE_NONPRECLUSION` boundaries that legitimately have no executor yet. The brake is that `C_CONDITIONALLY_ADMIT_DESIGN` still requires an **executed** current builder card; a purely documentary C can only return `C_HOLD_EXACT`.

## 3. What would reverse my design choice

1. **A real, complete R5 P2 `SPINE.json` is produced** with byte-verified provenance for all 118 rows. Then the legacy transfer path becomes the cheaper primary route and my inventory becomes its verification layer — my design survives but is no longer the first-choice entry.
2. **K3 re-issues the 118 with per-row canonical URIs** (e.g. content-addressed SWHIDs). Then `origin.path+selector` should be replaced by the canonical identifier and the row-hash machinery becomes redundant.
3. **The owners declare that terminal identities are not stable across cuts.** If F1–F8 etc. are intentionally re-issued per campaign, then binding them to fixed excerpts (as `D3A_TERMINAL_ORIGINS.json` does) is wrong and they should be bound to an owner-issued registry instead.

## 4. Cheapest thing that would falsify my central claim

Run the two suites against a deliberately **empty** `identity_dispositions` array: my gate must return RED with `IDENTITY_UNIVERSE_INCOMPLETE` for all eight groups. Then run it with **all 118 rows filled by the single sentence** `"Preserved by the selected candidate"`: my gate must return RED with `IDENTITY_EFFECT_NOT_GROUNDED_IN_ORIGIN` for all 118. Both are already covered by `Decision.test_one_missing_historical_decision_in_complete_53_is_red` and `Decision.test_boilerplate_identity_effect_is_red`.
