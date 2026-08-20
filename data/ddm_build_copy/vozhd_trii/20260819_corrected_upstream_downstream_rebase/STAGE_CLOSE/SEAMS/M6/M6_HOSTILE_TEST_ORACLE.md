# M6 — Hostile test oracle

**Contract:** `M6_V3_TO_V2_ACTOR_SAFE_EXPRESSION_SEAM@1.0.0`  
**Mode:** contract-level adversarial adjudication; no production implementation executed.

| ID | Hostile case | Required result | Adjudication |
|---|---|---|---|
| M6-H01 | Current verified envelope + current verified full-access BELIEF entry. | Exact claim may enter V2 under BELIEF permission only. | PASS |
| M6-H02 | Same entry but envelope source memory hash changed after `as_of`. | STALE; zero positive semantics; no transcript fallback. | PASS |
| M6-H03 | Envelope/entry/replay hash mismatch. | Integrity failure; zero positive semantics; no heuristic repair. | PASS |
| M6-H04 | Exact `DENY_FIRST_PERSON_CLAIM` decision. | Control-only denial; no hidden claim recovery. | PASS |
| M6-H05 | Exact `DEFER_MISSING_AUTHORITY` decision. | Control-only defer; system missing authority does not become actor uncertainty/nonknowledge. | PASS |
| M6-H06 | Partial accessibility lists components C1,C3. | Only C1,C3 may enter V2; whole claim and C2 remain inaccessible. | PASS |
| M6-H07 | V2 joins two permitted entries to infer a third unlisted claim. | `BLOCKED_HIDDEN_CLAIM_JOIN`. | PASS |
| M6-H08 | Entry permission is BELIEF; V2/render plan says KNOWLEDGE. | Permission-class substitution blocked/repaired; no escalation. | PASS |
| M6-H09 | Objective relationship truth differs from actor-perceived view. | Actor-perceived accessible view only. | PASS |
| M6-H10 | Opaque provenance points to V558 structural truth and renderer dereferences it. | Denied; audit-only ref cannot influence behavior. | PASS |
| M6-H11 | PSEPF is provided directly to prompt/persona selection. | Denied upstream-prior behavioral source. | PASS |
| M6-H12 | PSEPF is wrapped in a summary/cache/embedding and used for salience. | Denied indirect bypass; representation change grants no authority. | PASS |
| M6-H13 | Old transcript contains a claim that current V3 has withdrawn. | Transcript cannot restore current access. | PASS |
| M6-H14 | Previous rendered text says “I know X” but no current positive entry for X exists. | No current permission; rendered text is not V3 truth. | PASS |
| M6-H15 | External event decision REJECT. | Zero occurrence, zero V3 mutation, zero event/causal-session cursor advance. | PASS |
| M6-H16 | External event decision DEFER or INVALID. | Same zero-mutation/cursor behavior. | PASS |
| M6-H17 | External event decision ADMIT. | Exactly one admitted occurrence only; no automatic memory/knowledge/belief/relationship effect. | PASS |
| M6-H18 | Identical exact replay inputs are reordered in file/enumeration order. | Same semantic identities and receiver decision. | PASS |
| M6-H19 | Requested claim absent from a current verified nonempty envelope. | No inferred stance, denial, uncertainty, nonknowledge or permission. | PASS |
| M6-H20 | Current verified envelope has zero positive entries. | Valid empty; no filler/persona fabrication. | PASS |
| M6-H21 | V2 phenomenology selects one of three allowed claims due lawful current salience. | Allowed if salience authority is separate and only narrows selection. | PASS |
| M6-H22 | V2 salience machinery invents a structural explanation absent from envelope. | Forbidden semantic widening. | PASS |
| M6-H23 | Opaque provenance ID/hash is made model-visible without dereference. | Forbidden; provenance remains non-model-visible. | PASS |
| M6-H24 | Receiver actor differs from envelope actor. | Integrity failure; zero positive semantics. | PASS |
| M6-H25 | ADP-017 hash/version differs from accepted literal. | Integrity failure; no latest/semver fallback. | PASS |
| M6-H26 | Receiver causal time precedes envelope `as_of_causal_time`. | Integrity failure. | PASS |
| M6-H27 | No governed actor stance exists and system data are missing. | No fabricated `NONKNOWLEDGE`/`UNCERTAINTY`. | PASS |
| M6-H28 | V2 receives full GeneratedPersonRecord and infers answer not present in positive entries. | Forbidden; actor-safe envelope is sole positive semantic lane. | PASS |
| M6-H29 | Analyst `MISRECOGNITION_SUPPORTED` exists but actor has no meta-knowledge entry. | Analyst truth remains excluded. | PASS |
| M6-H30 | Raw `ReplayReceipt` is used as renderer/persona authority. | Forbidden; replay/audit only. | PASS |
| M6-H31 | V557/V558 locator metadata changes while actor-safe envelope semantics remain fixed. | No behavioral semantic change. | PASS |
| M6-H32 | Same actor-safe entry is expressed with different lawful register/wording. | Allowed variability if semantic claim/scope/permission do not widen. | PASS |

## Aggregate invariants

```text
CURRENT_VERIFIED_ACTOR_SAFE_ENTRY_ONLY
STALE_OR_INTEGRITY_FAILURE -> ZERO_POSITIVE_SEMANTICS
DENY_DEFER -> CONTROL_ONLY
SYSTEM_UNKNOWN != ACTOR_UNCERTAINTY_OR_NONKNOWLEDGE
PARTIAL_ACCESS -> EXACT_COMPONENT_ALLOWLIST_ONLY
V2_OUTPUT ⊆ V3_ALLOWED_SEMANTICS
PERMISSION_CLASS_IMMUTABLE_AT_SEAM
NO_HIDDEN_CLAIM_JOIN
ACTOR_PERCEIVED_RELATIONSHIP_VIEW_ONLY
OPAQUE_PROVENANCE -> AUDIT_ONLY_NONBEHAVIORAL
RAW_OR_INDIRECT_UPSTREAM_PRIOR -> DENY
SESSION_TRANSCRIPT != V3_ACCESS_AUTHORITY
REJECT_DEFER_INVALID -> ZERO_V3_MUTATION
ADMIT != AUTOMATIC_DOWNSTREAM_ACTOR_EFFECT
REPLAY_IS_EXACT_AND_FAIL_CLOSED
ALLOWLIST_CEILING != COMPLETE_PHENOMENOLOGY_OR_UTTERANCE_PLAN
```
