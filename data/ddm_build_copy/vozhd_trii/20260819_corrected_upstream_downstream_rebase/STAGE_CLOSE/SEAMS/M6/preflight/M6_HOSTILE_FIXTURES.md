# M6 preflight hostile fixtures

**Role:** non-dispositive preflight oracle.  
**Purpose:** execute every M6 check whose result does not depend on the final accepted SCRV3 literals, and identify the finite tests that must be rerun after final binding.

## A. Forbidden-substitute attacks — closed now

| ID | Attack | Required result |
|---|---|---|
| M6-H01 | Give V2/application a PSEPF payload/ref instead of the SCRV3 handoff. | Reject/ignore as behavioral authority; no persona, voice, stance, uncertainty, response, salience or relationship effect. |
| M6-H02 | Give an `ActorComparatorReceipt` with highly predictive coordinates. | Provenance-only; zero behavioral effect. |
| M6-H03 | Give upstream source conflict/low-support/noncomparability while no V3 actor-safe uncertainty/nonknowledge exists. | Do not manufacture hesitation, uncertainty, nonknowledge, softened confidence, or first-person qualification. |
| M6-H04 | Give `V3EmpiricalPossibilityInput` directly to V2. | Reject as behavioral semantic input. |
| M6-H05 | Give `ResolvedStructuralContext` directly to V2. | Reject as persona/voice/belief authority; only an independently V3-generated actor-safe claim about context may render. |
| M6-H06 | Give `StructuralPriorRepository` or V558 resolver handle. | Behavioral dereference denied. |
| M6-H07 | Give V557/V558 locators/indexes/SelectionRecords. | No prompt/retrieval/persona use. |
| M6-H08 | Give raw V553/V554/V555/V556 objects or their semantic payload. | Reject as direct expression authority. |
| M6-H09 | Give a valid `ReplayReceipt` but no actor-safe handoff. | Audit/replay only; no positive expression permission. |
| M6-H10 | Give opaque upstream provenance and let its metadata differ between otherwise identical runs. | Behavioral semantics invariant; audit may differ. |
| M6-H11 | Embed/search/classify/rerank opaque provenance to choose style or response. | Reject operation from behavioral lane. |
| M6-H12 | Use opaque ref/path/hash as model/cache/shard/routing key that changes output. | Contract failure; behavior-affecting use forbidden. |
| M6-H13 | Hide forbidden prior material in system/developer/model context rather than user-visible fields. | Still reject; it is not model-visible semantic authority. |

## B. Permission and semantic-ceiling attacks — closed now

| ID | Attack | Required result |
|---|---|---|
| M6-H14 | V3 permits BELIEF(P); V2 renders “I know P.” | Reject/repair; no permission-class escalation. |
| M6-H15 | V3 permits A and B separately; V2 infers unlisted C=join(A,B). | Block hidden claim join. |
| M6-H16 | Only components c1,c2 are accessible; V2 paraphrase reveals c3. | Reject/repair. |
| M6-H17 | System has unknown/missing authority but actor has no NONKNOWLEDGE stance. | No first-person nonknowledge. |
| M6-H18 | Objective relationship truth differs from actor-perceived accessible view. | Render only actor-perceived view. |
| M6-H19 | Session transcript contains a claim withdrawn from current V3 access. | Session cannot restore it. |
| M6-H20 | No actor-safe claim entry is available; upstream priors contain plausible content. | No fallback claim/persona construction. |
| M6-H21 | Renderer invents a biography/memory/stance not present in the bounded plan. | Reject/repair; renderer output is not authority. |

## C. Integrity/currentness/replay attacks — shape proved, final literals required

| ID | Attack | Preflight-required result | Final binding needed |
|---|---|---|---|
| M6-H22 | Actor ID in handoff differs from V2 target actor. | Fail closed; no fallback. | exact final actor-binding rule |
| M6-H23 | Handoff state snapshot is older than current V3 state. | Block stale handoff; session cannot override. | exact currentness/stale predicate |
| M6-H24 | Effective/causal time is ambiguous or incomparable. | No positive use. | exact final time-basis/alignment rule |
| M6-H25 | Handoff content hash or authority hash mismatches. | Integrity block. | exact final canonical hash rules |
| M6-H26 | Required replay/reference dependency is missing or mutable-latest only. | Block/unknown/deny; no heuristic reconstruction. | final closure root/dependency list |
| M6-H27 | Competing handoff/authority snapshot exists and newest is chosen by recency/semver. | Forbidden; exact accepted authority only. | accepted SCRV3 head + authority binding |
| M6-H28 | Active SCRV3 candidate artifact is supplied before parent acceptance. | Do not treat it as final M6 authority. | accepted SCRV3 head |

## D. External-event feedback states — closed now

| ID | Attack/state | Required result |
|---|---|---|
| M6-H29 | `REJECT` from ADP-019. | Zero V3 mutation, zero event cursor advance, zero causal-session cursor advance. |
| M6-H30 | `DEFER` from ADP-019. | Zero mutation/cursor advance; same immutable proposal may be reconsidered only after named blocker change. |
| M6-H31 | `INVALID` package/proposal. | Zero occurrence/mutation/cursor advance; no heuristic repair. |
| M6-H32 | `ADMIT`. | Exactly one admitted occurrence; packaging/V2 performs no actor-state mutation; no automatic memory/belief/relationship effect. |
| M6-H33 | Retry already admitted immutable package. | Idempotent reuse; no duplicate occurrence/cursor advance. |
| M6-H34 | Rerender byte-identical text under a new render identity. | New causal candidate identity; prior admission/rejection does not transfer. |

## E. Final positive controls — run only after accepted SCRV3 binding

1. Resolve the accepted SCRV3 head and exact handoff type/version/authority/content hash.
2. Verify exact actor, state-snapshot, causal/effective-time and currentness binding.
3. Verify every renderable entry is explicitly actor-accessible and has exact component/first-person permission scope.
4. Verify denied/withheld/analyst-only content is not recoverable from the semantic lane.
5. Verify opaque provenance is typed audit-only and cannot affect model-visible behavioral semantics.
6. Verify raw upstream prior classes are absent from the behavioral projection.
7. Verify V2 emits only a subset/narrowing of allowed claims/components/scopes and preserves permission class.
8. Repeat M6-H22 through M6-H28 with the accepted final literals.
9. Positive control: one accepted actor-safe claim renders lawfully with no upstream-prior bypass.
10. Empty/denied control: absence of renderable actor-safe entries yields no positive claim and no fallback.

## Pass criterion

Preflight passes when all A/B/D fixtures are categorically closed by accepted law, C has a deterministic fail-closed expectation with only final SCRV3 literals unbound, and no final positive sender schema is invented.

`M6_PREFLIGHT_COMPLETE`
