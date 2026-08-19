# M3 — hostile test oracle

**Contract:** `M3_V555_V556_HIGHER_ORDER_STRUCTURAL_EXACT_SEAM_CONTRACT@1.0.0`  
**Required passing token:** `M3_ACCEPTED__SCR556_EXACT_CONTRACT_CLOSED`  
**Production implementation:** not authorized

A case passes only when the exact identity/reference/state behavior below is preserved. Labels, convenient locators, current implementation rows, or downstream readiness cannot substitute for the accepted producer identity.

## A. Final SCR556 M3 fixtures

| ID | Hostile case | Required result |
|---|---|---|
| M3-01 | Import SCR555 participant identity | `SCR555_ACCEPTED_CANONICAL_ROUTE_IDENTITY_REF` resolves exactly to the accepted seven-field V555 route tuple or an exact verifiable address thereof; no new route ID. |
| M3-02 | Same visible labels/channel/receiver, different accepted V555 route identities | Preserve distinct participants exactly. No label collapse. |
| M3-03 | Break or hash-mismatch one accepted V555 participant ref | `UNRESOLVABLE_PARTICIPANT`; no look-alike reconstruction or latest repair. |
| M3-04 | Feed every accepted V555 route state through participant eligibility | Only `ROUTE_CANDIDATE_AUTHORIZED` may proceed as positive route-bearing eligibility; no V556 reownership/rename of upstream states. |
| M3-05 | Round-trip participant through V556 reference serialization/dereference | Exact producer-owned V555 identity is preserved; no V556 re-ID. |

## B. M2-bound route identity attacks

| ID | Hostile case | Required result |
|---|---|---|
| H-M3-006 | V555 tuple element 1 is supplied as a label/look-alike rather than M2-bound canonical SCR554 F1 ID | Participant cannot validate; fail closed. |
| H-M3-007 | B1 is appended as an eighth V555 route-identity member | Reject. B1 is M2 permission/reference/replay boundary, not a route identity field. |
| H-M3-008 | Inherited V554 F2 ID/payload is appended to V555 route identity | Reject. F2 remains V554-owned exact-reference-only context. |
| H-M3-009 | A locator/hash claims route equality but dereference yields any seven-field tuple mismatch | Fail closed; locator/hash convenience never overrides tuple inequality. |
| H-M3-010 | Different canonical SCR554 F1 IDs with otherwise identical V555 route fields | Different V555 routes and therefore distinct V556 participants. |
| H-M3-011 | Same exact seven-field tuple arrives through duplicate physical rows/aliases | Same V555 route identity; duplicate physical rows cannot create extra distinct routes. |

## C. Route reconstruction and bypass attacks

| ID | Hostile case | Required result |
|---|---|---|
| H-M3-012 | Only `run_id`, slot ID/name/channel and endpoint labels survive; canonical route ref is absent | `UNRESOLVABLE_PARTICIPANT`; no reconstruction. |
| H-M3-013 | StructuralEmpiricalAdmission supplied directly as V556 participant | Reject semantic bypass. |
| H-M3-014 | V553 temporal object supplied directly as V556 participant | Reject semantic bypass. |
| H-M3-015 | Canonical V554 F1/B1 supplied without the complete V555 route identity | Reject as V556 participant; F1 is only field 1 inside the complete V555 route. |
| H-M3-016 | Legacy V555/V556 seed or readiness row offered as route identity | Reject. |
| H-M3-017 | Repository locator exists but cannot deterministically dereference exact V555 identity/closure | `UNRESOLVABLE_PARTICIPANT`; repository presence is not identity authority. |
| H-M3-018 | V556 mints a local base-edge ID by normalizing route components | Reject duplicate/reidentified base edge. |

## D. Upstream route-state attacks

| ID | Hostile case | Required result |
|---|---|---|
| H-M3-019 | `VALID_EMPTY` offered as positive route participant | No positive V556 participation; preserve upstream state. |
| H-M3-020 | `V554_STRUCTURAL_USE_DENIED` offered with surviving labels/locator | No positive participation; no repair from visible route fields. |
| H-M3-021 | `NO_GOVERNED_ROUTE_AUTHORITY` or `ROUTE_BLOCKED_BY_GOVERNED_RULE` offered as participant | No positive participation. |
| H-M3-022 | `ROUTE_STATIC_AUTHORITY_MISSING` or `ROUTE_IDENTITY_UNRESOLVED` offered | No positive participation; resolution failure remains fail-closed. |
| H-M3-023 | `CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE` offered | No positive participation; integrity failure is not a V556 supported relation. |
| H-M3-024 | `DEFERRED_RUNTIME_BINDING_REFERENCED_ONLY` is asserted satisfied by V556 | Reject. It remains inherited V554-owned exact-reference-only F2 context. |
| H-M3-025 | `ROUTE_CANDIDATE_AUTHORIZED` copied/renamed directly into V556 `SUPPORTED` | Reject. Route authorization is eligibility only; exact V556 rule evaluation over 2..n participants is still required. |

## E. Cardinality / role / order / multiplicity attacks

| ID | Hostile case | Required result |
|---|---|---|
| H-M3-026 | One exact V555 route supplied to a higher-order V556 rule | `INVALID_PARTICIPANT_SET`; no positive V556 semantic. |
| H-M3-027 | Same canonical route duplicated twice to fake two distinct routes | Does not satisfy distinct-route floor; invalid participant set. |
| H-M3-028 | Same route repeated where rule does not explicitly permit reuse | `INVALID_PARTICIPANT_SET`. |
| H-M3-029 | Rule permits same-route reuse but occurrence-specific V555 route IDs are minted | Reject. Occurrence metadata is V556-owned; V555 identity remains unchanged. |
| H-M3-030 | Required participant role missing/unknown | `INVALID_PARTICIPANT_SET`. |
| H-M3-031 | Ordered rule has missing/duplicate invalid ordinal | `INVALID_PARTICIPANT_SET`. |
| H-M3-032 | V556 participant ordinal is used to reverse `SOURCE -> MEDIATION_LOCUS -> RECEIVER` inside a route | Reject. Higher-order participant order cannot mutate internal V555 route order. |
| H-M3-033 | Ordered rule A,B is replayed as B,A while all else is held fixed | Treat according to exact ordered rule: changed semantic candidate/identity or invalid; never silently canonicalize to A,B. |
| H-M3-034 | Unordered/symmetric rule receives same exact participant bindings in different file/input/storage order | Same canonical V556 identity and typed outcome. |

## F. Source composition / noninference attacks

| ID | Hostile case | Required result |
|---|---|---|
| H-M3-035 | Cross-source participants, no operation-specific composition authority | `UNKNOWN_AUTHORITY`; no positive cross-source semantic. |
| H-M3-036 | Exact composition authority says noncomparable | `NONCOMPARABLE`. |
| H-M3-037 | Exact composition authority denies operation | `DENIED`. |
| H-M3-038 | Applicable exact composition authorities conflict without precedence | `CONFLICTING_AUTHORITY`. |
| H-M3-039 | Shared receiver/endpoint alone | No relation without exact V556 rule authority. |
| H-M3-040 | Shared source/channel labels alone | No relation/equivalence without exact V556 rule authority. |
| H-M3-041 | Shared time/geography/stratum alone | No relation. |
| H-M3-042 | Storage/file/index adjacency or co-resolution alone | No relation. |
| H-M3-043 | Provenance graph reaches common ancestor but no composition authority exists | No positive composition; provenance is interpretation/origin reachability only. |

## G. V556 rule / typed-outcome attacks

| ID | Hostile case | Required result |
|---|---|---|
| H-M3-044 | Exact immutable V556 rule, admissible exact participants, all required authorities, governed positive relation | `SUPPORTED`; object names exact rule authority and participant bindings. |
| H-M3-045 | Exact rule lawfully evaluates to empty/none | `VALID_EMPTY`; do not convert to missing output, denial, or unknown authority. |
| H-M3-046 | Rule authority missing, mutable-latest, hash-mismatched or label-selected | `UNKNOWN_AUTHORITY`; no positive semantic. |
| H-M3-047 | Two exact applicable rule authorities conflict without exact precedence | `CONFLICTING_AUTHORITY`. |
| H-M3-048 | V556 topology references an unresolved required V556 relation object | Fail closed; no topology repair from adjacency/labels. |
| H-M3-049 | Missing positive output is interpreted as `VALID_EMPTY` | Reject. Missing positive output carries no implicit semantic result. |

## H. Higher-order ceiling / no-filler attacks

| ID | Hostile case | Required result |
|---|---|---|
| H-M3-050 | Proposed structural path adds another source/channel/receiver hop but tries to encode it only as V556 topology | Reject; additional atomic hop requires another V555 route. |
| H-M3-051 | No exact V556 higher-order meaning required; system emits one wrapper per V555 route | Fail no-filler law; required result is `ZERO_V556_OBJECTS`. |
| H-M3-052 | V555 route is otherwise directly publishable and no V556 transform is required | Preserve direct V555 -> V557 path subject to producer ceiling and V557 governance. |
| H-M3-053 | `ROUTE_CANDIDATE_AUTHORIZED` is treated as V557 publication permission | Reject. Route state is not publication permission. |
| H-M3-054 | V556 widens producer/V557 permission | Reject; permission may not be widened. |

## I. Replay / authority freshness attacks

| ID | Hostile case | Required result |
|---|---|---|
| H-M3-055 | Same exact M2/SCR555/SCR556 authority pins, same participants/rule/composition refs/payload/state, different run/timestamp/storage order | Identical semantic replay except where exact rule declares participant order semantic. |
| H-M3-056 | V556 rule authority hash changes | Old semantic object cannot silently replay as identical; no latest repair. |
| H-M3-057 | Exact V555 participant reference changes while visible labels remain same | V556 semantic identity/participant binding must reflect the changed producer identity. |
| H-M3-058 | Current M2 branch administrative reassignment commit is substituted for the accepted semantic package pin | Reject as semantic authority substitution; accepted M2 semantic head/blobs remain the pins. |
| H-M3-059 | M1 is claimed to have changed SCR554 materially, but exact accepted M1 still pins the same SCR554 head used by M2 | Do not manufacture staleness; M2/M3 remain fresh on current evidence. |
| H-M3-060 | A future higher authority materially changes SCR554 and M2 is reclassified stale | M3 becomes transitively stale; re-adjudicate M2 then recheck M3 before whole-machine closure. |

## Acceptance checksum

M3 passes only if all of the following are simultaneously true:

1. exact V555 participant identity is the frozen seven-field tuple with M2-bound canonical SCR554 F1 as field 1;
2. V556 never re-IDs or reconstructs it;
3. every governed evaluation has 2..n exact route occurrences and at least two distinct canonical routes;
4. roles/order/cardinality/multiplicity are V556-rule-declared;
5. only `ROUTE_CANDIDATE_AUTHORIZED` is positive route-bearing upstream eligibility;
6. source composition remains `NONE_BY_DEFAULT` absent exact positive authority;
7. all eight V556 typed states remain distinct and fail closed;
8. no upstream object/legacy seed/repository locator bypasses V555;
9. no filler V556 object is required for direct V555 publication;
10. replay binds exact accepted M2/SCR555/SCR556 authority and reference closure.

Passing token:

`M3_ACCEPTED__SCR556_EXACT_CONTRACT_CLOSED`
