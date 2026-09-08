# OBL059 R6 — FRESH INDEPENDENT REVIEW EVIDENCE R1

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r6-independent-review-r1`

Exact start:
`e4a42d77abfd6191025d4505ef9550700dd04e25`

Campaign authority consumed prospectively:
`2d0c274c28fdb16de5fbb731a90059184982d841`

Campaign tree:
`8f1c70c91ce9b94666005599e4ac3e01ea15847f`

Frozen R6 candidate reviewed:
`5ca7380bd17b3dec271fe5a8c6bf22656f55b647`

Candidate executable blob:
`9514781522388d314dca8f71b088e243a6e84820`

Known producer evidence:
`a21f7ba53a8f9e58a983b8f5c678ef66d1ad207a`
run `34250997854`
producer court `80 passed, 313 subtests passed`; protocol `20 passed`

## Independent freeze identities

Independent matrix/evidence execution commit:
`8485e68b7fbe85ce618f4a24db9cc990b9c69695`

Matrix blob:
`1cfc964819fd99bab9cbb42d84599af56cf37063`

Independent test blob:
`7c911b8d8327d7ef9edd9b29903aef8bd71dfbb3`

Governed wrapper blob:
`5f4cdbb5bd2ee0ccec0bf5a8afacb691b016cfa2`

Court-spec blob:
`009b879b16ff59f8add2c6a67ff4bb192647cf8a`

The matrix was frozen before governed execution. No candidate file was modified.

## Governed execution

Workflow:
`Rabochii Governed Bounded Court`

Run:
`34254885825`

Run conclusion:
`failure`

Job:
`102158038828`

Protocol self-test:
`20 passed in 0.06s`

Court-spec validation:
`PASS`

Independent review court:
`1 failed, 15 passed, 141 subtests passed in 0.19s`

Artifact:
`10067444579`

Artifact name:
`rabochii-court-receipt-34254885825`

Artifact size:
`618 bytes`

Artifact ZIP SHA-256:
`52ebf84202663b26cabf0b259a270ad746608dd5582a6f83aa2e41745463f4a1`

Execution-only PR:
`#299`

PR disposition:
`CLOSED_UNMERGED`

PR synthetic merge identity:
`d617329e781017873f1cc5d78d9fb144ea35258f`

## Semantic review result

`FAIL__OBL059_R6_INDEPENDENT_REVIEW__CUSTOM_MAPPING_PACKET_TRAVERSAL_ESCAPES_NEGATIVE_RECEIPT`

Smallest exact blocker:
`BLOCKER__OBL059_R6_CUSTOM_MAPPING_PACKET_CAN_ESCAPE_VIA_CALLER_CONTROLLED_KEYS_BEFORE_NEGATIVE_RECEIPT`

The failing case used a custom `collections.abc.Mapping` packet whose backing data contained the exact oversized malformed `actor_id` case. R6 checks `type(packet) is not dict` and delegates it to R5; R5 delegates to R4; R4 delegates to R3. R3 then executes `deepcopy(dict(packet))`. Constructing that dict invokes the packet's caller-defined `keys()` method, which raised `RuntimeError("packet-keys-must-not-run")`. The exception escaped instead of returning the required deterministic negative receipt.

This establishes that the R6 stable-integer repair itself closes the mutable runtime-setting gap for exact dict packets, but the public Mapping input path can still depend on caller-defined traversal before malformed-input receipt construction becomes total.

All other frozen-matrix families passed, including stable-threshold neighbors, direct proof that unsafe exact integers do not reach inherited evaluation, in-flight `0 -> minimum` setting changes, setting-invariant proofs, diagnostic correctness, oversized integers at all five required bindings, nested exact built-ins/cycles/shared/depth forms, exact-int subclasses and adjacent primitive cases, custom malformed values, concurrent evaluations/settings, ordinary semantic controls, and deliberate unrelated programmer-error visibility.

## Separation / current effect

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT = 1`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

`FROZEN_R6_CANDIDATE_MODIFIED = NO`

`PROJECT_CURRENT_POSITIVE_APPLICABILITY_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`ENCOUNTER_CREATED = NO`

`AUTHORITY_INDEX_MUTATED = NO`

`SUB_VOZHD_E_ADOPTION_CLAIMED = NO`

`HQ_ADOPTION_CLAIMED = NO`

`OBL061 = HARD_BLOCKED`
