# OBL059 POSITIVE_APPLICABILITY — R10 FRESH DISTINCT INDEPENDENT REVIEW EVIDENCE R1

## Exact identities

Repository:
`maidiu/rawlsing`

Reviewer branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r10-independent-review-r1`

Exact review start:
`0c9e18cb63a03791c8c9ce4deeb57422ddea5a76`

Campaign authority:
`b948aed197506905f4b5f1cab20a92e3ce6949b9`

Campaign tree:
`bc11426ddcf8078bfabc1ac59a889bedd1d1f6b1`

Frozen R10 target:
`77f80b15d35236d13899df0992943cfc20a08485`

Producer governed evidence consumed as prior context only:
`c9d2ecd1869992881aca35660dcb24f65b7760d7`

Producer run/job:
`34281370576` / `102246653893`

Independent review matrix/evidence freeze:
`1a4101f78d6cdb5509b21baa939aa5890e37e4f5`

Independent matrix blob:
`723c484580d4c8eb35ea97b095da1ac46b3fd587`

Independent test blob:
`fe83b8ce371575fc8c60831a191dd87856623fd7`

Governed wrapper blob:
`ac9d2393a0d952a0bf98c7b37587cc098a6c5d6e`

Court-spec blob:
`2df32881fdde948730b8c94f027cd83b7e647c73`

## Governed execution

Workflow:
`Rabochii Governed Bounded Court`

Run:
`34284731914`

Job:
`102257552577`

Protocol self-test:
`20 passed in 0.07s`

Court-spec validation:
`PASS`

Independent review court:
`5 failed, 16 passed, 76 subtests passed in 0.55s`

Workflow conclusion:
`failure`

Artifact:
`10079002491`

Artifact name:
`rabochii-court-receipt-34284731914`

Artifact ZIP SHA-256:
`a66eac9b1dae4b6cea0c05222ffc7f00152436307305da67afa54bfc995bdecf`

Execution-only PR:
`#327`

PR disposition:
`CLOSED_UNMERGED`

PR synthetic merge identity:
`14b2d9cf1df9e6593b433660bb4a59e9f85ed2b1`

## Independent finding

The fresh matrix found one semantic-preservation blocker, reproduced independently at every consumed custom-Mapping node.

The review used `collections.ChainMap(data, {})` with `data` equal to the exact-dict positive control for the node under test. Each ChainMap was stable: its observable Mapping key/value view was the same as the exact dict, and no mutation callback or timing dependency was present.

Frozen R10 returned a negative result at all five positions instead of preserving the exact-dict positive result:

- opportunity -> `OPPORTUNITY_BINDING_MISSING_OR_MALFORMED`;
- top-level evidence -> `EVIDENCE_MISSING_OR_MALFORMED`;
- subject classification -> structural-classification missing result;
- actor activation -> actor-activation missing result;
- developmental phase -> developmental-phase missing result.

The reason is the R10 entry-view acquisition boundary: it requires one directly discoverable dict backing for a custom Mapping. A ChainMap stores a stable composed view in its `maps` sequence rather than one directly discoverable backing dict. R10 therefore treats the view as unavailable and invalidates the node, even though the Mapping itself is stable, lawful, and exact-dict-equivalent at the semantic interface.

The R10 commission explicitly requires stable lawful custom Mapping carriers at every consumed node to preserve exact-dict-equivalent meaning. Failing closed is lawful when a coherent view truly cannot be established, but it cannot replace that preservation requirement for a stable Mapping whose coherent semantic view is well-defined and deterministic.

## Smallest blocker

`BLOCKER__OBL059_R10_STABLE_COMPOSED_MAPPING_EQUIVALENCE_REJECTED_BY_SINGLE_BACKING_DICT_REQUIREMENT`

R10's coherent-entry-view mechanism is therefore not general enough to satisfy both required properties simultaneously: coherent isolation and stable lawful Mapping semantic preservation.

## Passing independent findings

The same frozen matrix independently confirmed the rest of the commissioned boundary:

- all ordered negative-to-positive internal mutation directions across the five consumed nodes remain governed by the entry view;
- reverse positive-to-negative child-local mutation directions do not rewrite the entry result;
- parent-slot and component-slot replacement during validation do not rewrite the captured entry semantics;
- outer custom Mapping plus nested custom Mapping composition remains coherent for supported carriers;
- shared/aliased custom carriers retain one-validation identity behavior;
- deterministic fail-closed behavior holds when an entry view genuinely cannot be established;
- actually invoked `keys()` and indexing failures return deterministic field-specific negative receipts;
- cyclic backing content on the commissioned negative path remains total and JSON-safe;
- stable mapping-proxy controls preserve exact-dict positive semantics;
- oversized exact integers at all five required bindings remain total under supported integer-conversion settings;
- nested custom-carrier oversized integers remain deterministic and JSON-safe;
- identical oversized nested inputs have stable proofs and distinct values remain distinguishable;
- wrong scope, wrong authority, stale evidence and adjacent narrative/routing fields remain negative;
- unrelated deliberate implementation errors after successful preparation remain visible;
- repeated and concurrent exact-dict evaluations remain deterministic;
- exact R10 revision identity and every no-current-effect flag remain intact.

The independently confirmed R9 oversized-integer repair therefore remains closed. The terminal FAIL is solely required by the stable composed-Mapping equivalence blocker above.

## Separation

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R10_CANDIDATE = 1`

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

## No-current-effect attestation

`PROJECT_CURRENT_POSITIVE_APPLICABILITY_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`ACTOR_CREATED_OR_ACTIVATED = NO`

`ADP008_PHASE_TRANSITION_EXECUTED = NO`

`ADP019_OCCURRENCE_ADMITTED = NO`

`CAUSAL_USE_PERMISSION_OWNED = NO`

`CONTACT_WITNESS_INDEPENDENCE_OWNED = NO`

`ENCOUNTER_CREATED = NO`

`AUTHORITY_INDEX_MUTATED = NO`

`SUB_VOZHD_E_ADOPTION_CLAIMED = NO`

`HQ_ADOPTION_CLAIMED = NO`

`OBL061 = HARD_BLOCKED`
