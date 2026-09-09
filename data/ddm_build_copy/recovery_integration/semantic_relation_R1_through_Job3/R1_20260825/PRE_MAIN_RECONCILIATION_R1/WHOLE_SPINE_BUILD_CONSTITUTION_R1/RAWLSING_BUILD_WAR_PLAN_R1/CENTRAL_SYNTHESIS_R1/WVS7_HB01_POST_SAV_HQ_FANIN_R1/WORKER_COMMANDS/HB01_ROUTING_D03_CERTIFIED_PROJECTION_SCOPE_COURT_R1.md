# RABOCHII — HB01 ROUTING / D03 CERTIFIED-PROJECTION SCOPE COURT R1

Repository: `maidiu/rawlsing`

Branch:
`agent/rabochii-vozhd-hb01-routing-d03-certified-projection-scope-r1`

Exact starting PRE-MAIN:
`ae5f002b2232a49968ebf3472f25a257fca54717`

Authority inputs:
- accepted WVS7 routing/risk law: `a07f449221256e0c52cffd3f85812d30c0f047fc`
- accepted C11 ownership bridge: `a06f2bced8677453cf77fec5e622cb334a9810a5`
- historical postbatch HQ package: `efca0824b87415b9a99991b989eb0c8334cdcd9d`
- current post-SAV W join consumed by HQ: `155ae2d1416b89f9a0035ca0cc284183ed069224`
- D03/D12 exact source-backed return: `e404bc097f48a09265f1aec06e3d011a892f69c4`

Mission grain:
`HB01_ROUTING_D03_CERTIFIED_PROJECTION_SCOPE_DISPOSITION_ONLY`

Do NOT touch or decode the SAV.

## Exact universe to adjudicate

Documentary routing unresolved cells:
- D01: 63
- D02: 65
- D04: 13
- D05: 4
- D06: 4
- D07: 1
- D08: 5
- D09: 5
- D10: 62
Total: 222 / 585

D03 person-position targets:
`Q276,Q276A,Q277,Q277A,Q278,Q278A,Q280,Q282,Q283`

## Required question

For every unresolved target/rule-family projection, determine from accepted current ownership / projection authority whether that projection is actually required inside the HB01-certified WVS7 projection.

Court outcomes are HQ-scope decisions, NOT respondent routing states:

1. `IN_SCOPE__POSITIVE_ROUTING_RESOLUTION_REQUIRED`
   - the projection remains part of the certified WVS7 surface;
   - any unresolved determinant remains exactly `ROUTING_UNKNOWN`;
   - the court must identify the exact missing authority grain that a later recovery worker would need.

2. `OUT_OF_SCOPE__EXPLICIT_CERTIFIED_PROJECTION_REMOVAL_SUPPORTED`
   - accepted ownership/current projection authority positively supports omitting this entire target/rule-family projection from the certified WVS7 surface;
   - respondent `ROUTING_UNKNOWN` values are NOT relabeled negative or inapplicable.

3. `SCOPE_AUTHORITY_UNRESOLVED__FAIL_CLOSED`
   - the court cannot prove either inclusion necessity or lawful exclusion from accepted authority;
   - return this exact blocker rather than inventing scope.

## Accepted routing-law invariants

- unresolved determinant => `ROUTING_UNKNOWN`;
- UNKNOWN is never converted to denominator complement;
- explicit negative/inapplicable routing is lawful only where an accepted deterministic negative branch exists;
- observed child missingness, response incidence, frequencies and populated-row complements are forbidden determinant inputs;
- person-position eligibility requires accepted positive presence determinant if the projection remains in scope.

## Prohibitions

- no documentary recovery archaeology in this court;
- no SAV work;
- no new D11 universe work;
- no cross-country inference;
- no target exclusion merely because documentary recovery would be inconvenient;
- no conversion of routing UNKNOWN into NOT_ELIGIBLE/INAPPLICABLE;
- no C05-R2A, full GSR07, HB05, HB06, HB07 or C09.

## Required artifacts

Freeze:
- one exact row per unresolved documentary cell with target/rule family, country/scope, current unresolved state, certified-projection scope disposition, authority refs, and rationale;
- one exact row per nine D03 targets with the same disposition logic;
- summary counts by disposition;
- exact list of positive-recovery grains still required after lawful scope removals;
- exact list of projections lawfully removed from the certified scope;
- explicit unresolved scope-authority blockers, if any;
- deterministic machine-readable court result.

PASS terminal:
`HB01_ROUTING_D03_CERTIFIED_PROJECTION_SCOPE_COURT_COMPLETE__REQUIRED_AND_REMOVED_PROJECTIONS_FROZEN`

BLOCKER terminal:
`HB01_ROUTING_D03_CERTIFIED_PROJECTION_SCOPE_COURT__EXACT_SCOPE_AUTHORITY_BLOCKER_PROVED`

Return to VOZHD/HQ. Do not claim HB01 closure.
