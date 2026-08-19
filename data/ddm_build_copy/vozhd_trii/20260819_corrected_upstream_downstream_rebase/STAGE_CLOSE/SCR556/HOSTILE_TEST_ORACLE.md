# SCR556 — HOSTILE TEST ORACLE

**Contract:** `SCR556_V556_INTERACTION_TOPOLOGY_EXACT_CONTRACT / scr556.v1`  
**Current disposition:** `SCR556_WAITING_ONLY_FOR_EXACT_FINAL_SEAM`

A fixture passes only when the exact typed outcome and identity/reference behavior below are deterministic. A convenient positive row, an empty dataframe, or a downstream blocker is not a substitute for the required semantic result.

## A. Participant / base-edge attacks

| ID | Hostile input | Required result |
|---|---|---|
| H01 | One exact V555 route supplied to a 2..n V556 rule | `INVALID_PARTICIPANT_SET`; no positive V556 object. |
| H02 | Two routes share endpoint | No relation unless exact V556 rule establishes it. |
| H03 | Two routes share time | No relation unless exact V556 rule establishes it. |
| H04 | Two routes share geography | No relation unless exact V556 rule establishes it. |
| H05 | Two routes share stratum | No relation unless exact V556 rule establishes it. |
| H06 | Two routes are adjacent in one file/table | No relation unless exact V556 rule establishes it. |
| H07 | Two routes co-resolve in one context | No relation unless exact V556 rule establishes it. |
| H08 | Two routes share provenance ancestor | No relation and no source-composition permission unless separately authorized. |
| H09 | Same labels/channels but different exact V555 route identities | Remain distinct participants. No label collapse. |
| H10 | Ordered rule receives participant order A,B then B,A | Order-sensitive semantic identity/result changes as the exact rule requires. |
| H11 | Unordered/symmetric rule receives same participants in different input/file order | Same canonical participant binding and replay identity. |
| H12 | Same V555 route appears twice where rule forbids same-route reuse | `INVALID_PARTICIPANT_SET`. |
| H13 | Same route reused under a rule that explicitly permits it but one occurrence lacks distinct role/multiplicity binding | `INVALID_PARTICIPANT_SET`. |
| H14 | Required participant role absent or unknown | `INVALID_PARTICIPANT_SET`. |
| H15 | Ordered rule has missing/duplicate invalid ordinal | `INVALID_PARTICIPANT_SET`. |
| H16 | Exact V555 participant ref missing or hash-mismatched | `UNRESOLVABLE_PARTICIPANT`; no reconstruction. |
| H17 | Current implementation `run_id + slot_name` offered as canonical route identity | Reject as non-authoritative; positive V556 semantics forbidden. |
| H18 | V556 attempts to mint local base-edge identity equivalent to V555 route | Fail: duplicate/reidentified base edge forbidden. |

## B. Rule-authority attacks

| ID | Hostile input | Required result |
|---|---|---|
| H19 | Rule authority missing | `UNKNOWN_AUTHORITY`; no positive object. |
| H20 | Rule selected by unversioned `latest` | `UNKNOWN_AUTHORITY`; no positive object. |
| H21 | Rule ID/version present but content hash mismatched | `UNKNOWN_AUTHORITY`; no positive object. |
| H22 | Rule selected by human-readable label similarity | Reject; no positive object. |
| H23 | Rule omits role/order/cardinality/multiplicity policy needed by evaluation | `UNKNOWN_AUTHORITY` or fail-closed rule invalidity; never infer defaults. |
| H24 | Two exact applicable rule authorities conflict with no exact precedence | `CONFLICTING_AUTHORITY`. |

## C. Source-composition attacks

| ID | Hostile input | Required result |
|---|---|---|
| H25 | Cross-source participants, no composition authority | `UNKNOWN_AUTHORITY`; no positive cross-source semantic. |
| H26 | Composition authority covers only some source universes/participants | `UNKNOWN_AUTHORITY`; no partial synthetic composition. |
| H27 | Composition authority exists for another operation/rule | `UNKNOWN_AUTHORITY`; no authority borrowing. |
| H28 | Exact authority says sources are noncomparable | `NONCOMPARABLE`. |
| H29 | Exact authority denies composition | `DENIED`. |
| H30 | Applicable composition authorities conflict and no exact precedence exists | `CONFLICTING_AUTHORITY`. |
| H31 | Provenance graph proves all source origins reachable but no composition authority exists | Still `UNKNOWN_AUTHORITY`; provenance is not composition permission. |

## D. Positive / valid-empty / topology attacks

| ID | Hostile input | Required result |
|---|---|---|
| H32 | Exact rule, valid participants, all authorities, governed positive relation | `SUPPORTED`; object names exact rule authority and all exact V555 participant bindings. |
| H33 | Exact rule lawfully evaluated and relation/topology/prerequisite is empty | `VALID_EMPTY`; distinguish from missing authority and missing output. |
| H34 | Same attractor label, different exact prerequisite participant sets | Distinct semantic identity/result as governed; labels cannot collapse prerequisite graphs. |
| H35 | Prerequisite supplied only as string `requires_v555_mediated_history` with no exact 2..n participant graph/rule authority | Not sufficient for positive exact V556 prerequisite semantics. |
| H36 | Topology references a V556 relation object that cannot be exactly resolved | Fail closed; no topology repair from labels/adjacency. |
| H37 | Interpretation-critical negative/valid-empty state removed before publication | Fail closure/replay oracle. |

## E. No-filler / publication attacks

| ID | Hostile input | Required result |
|---|---|---|
| H38 | V555 route is runtime-authorized but no higher-order V556 rule is required | `ZERO_V556_OBJECTS`; V555 direct V557 proposal remains lawful. |
| H39 | System creates one V556 wrapper per V555 route solely to preserve stage order | Fail no-filler law. |
| H40 | `ready_for_v557 = true` used as publication/use permission | Fail; readiness is not V557 permission. |
| H41 | V556 object attempts to widen producer permission on V557 handoff | Fail; V557 permission must remain within producer ceiling. |
| H42 | V556 object or attractor is consumed as actor psyche/identity/belief/voice | Fail semantic-authority boundary. |
| H43 | Raw StructuralEmpiricalAdmission or V554 look-alike fields enter V556 without exact V555 participant identity | Reject bypass. |

## F. Replay / identity attacks

| ID | Hostile input | Required result |
|---|---|---|
| H44 | Identical immutable authorities, participants, composition refs and semantic payload replay under different `run_id`/timestamp | Same semantic identity and typed state. |
| H45 | Only file/storage/resolver order changes for an unordered rule | Same semantic identity and state. |
| H46 | A semantic rule authority hash changes | Old object does not replay as identical; no `latest` repair. |
| H47 | Participant route ref changes while labels remain same | Semantic identity must reflect the changed exact participant. |

## G. M3 final-seam fixtures

These fixtures cannot be signed until SCR555 is accepted. They are the **only** unresolved SCR556 adjudication tests.

| ID | Required M3 fixture | Pass condition |
|---|---|---|
| M3-01 | Import accepted SCR555 canonical route identity/reference contract | `SCR555_ACCEPTED_CANONICAL_ROUTE_IDENTITY_REF` is bound by exact import, not renaming/reconstruction. |
| M3-02 | Same labels, different accepted SCR555 route identities | V556 preserves distinct participant identity exactly. |
| M3-03 | Break/hash-mismatch one accepted SCR555 route reference | `UNRESOLVABLE_PARTICIPANT`; no look-alike repair. |
| M3-04 | Feed each accepted SCR555 typed route state into V556 eligibility seam | Eligibility/rejection matches the accepted SCR555 mapping exactly; V556 invents no route-state policy. |
| M3-05 | Serialize/dereference participant through V556 and compare to SCR555 producer identity | Producer route identity is byte/exact-reference preserved; no V556 route re-ID. |

## Oracle disposition

All H01-H47 semantics are closed by SCR556 local authority. M3-01 through M3-05 await only the accepted SCR555 exact route contract.

Current token: `SCR556_WAITING_ONLY_FOR_EXACT_FINAL_SEAM`.
