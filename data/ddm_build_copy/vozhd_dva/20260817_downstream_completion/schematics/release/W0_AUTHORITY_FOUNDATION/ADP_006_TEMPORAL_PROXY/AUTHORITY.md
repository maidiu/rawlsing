# ADP-006 — Runtime Temporal-Proxy Eligibility Authority

**Authority cell:** W0-02 / ADP-006  
**RA-R00 blocker:** `MUST-006`  
**Authority ID:** `RA-MUST-006-TEMPORAL-PROXY-ELIGIBILITY`  
**Authority version:** `1.0.0`  
**Status:** `AUTHORITY_CREATED`  
**Whole-machine architecture:** CLOSED; unchanged  
**Production implementation:** NOT PERFORMED  
**Historical archive:** NOT AUTHORIZED / NOT USED

---

## 1. Bounded holding

This authority answers one question only:

> When may an already-authorized temporal observation be used by the accepted `ContextResolver` as `LATEST_PRIOR_OBSERVATION_PROXY` or `EARLIEST_POST_QUERY_PROXY`, and when must proxy resolution fail closed?

It does **not** redesign temporal selection precedence. The already-binding order remains:

`DIRECT_TEMPORAL_SUPPORT`
`→ authorized LATEST_PRIOR_OBSERVATION_PROXY`
`→ authorized EARLIEST_POST_QUERY_PROXY`
`→ NO_LAWFUL_TEMPORAL_ANCHOR`.

It does **not** create V557 runtime-use permission. Producer permission and V557 runtime-use governance remain separate, monotone prerequisites. It does not alter V553 evidence time, create temporal intervals, interpolate, select a nearest wave, generate actor history, or turn a structural prior into a remembered/lived event.

### First-release authority conclusion

Only canonical V553 `TEMPORAL_OBSERVATION` objects are temporal proxy anchors in the first release. Downstream V554/V555/V556 objects may depend on a lawfully resolved temporal observation, but are never independently “proxied as objects.” Their own producer conditions, exact temporal dependency refs, item-use authority and generated-binding requirements remain in force.

Two proxy rules are authorized:

1. `ADP006-R001-LATEST-PRIOR-STRUCTURAL-CONTEXT` version `1.0.0`;
2. `ADP006-R002-EARLIEST-POST-PRECOVERAGE` version `1.0.0`.

Both use an explicit first-release lag policy of `NO_NUMERIC_CAP_EXPLICIT`. This is deliberate: the accepted evidence does not govern a universal numeric year cutoff, and the runtime-prior architecture explicitly rejects a hardcoded universal fidelity cutoff. Every proxy lag remains mandatory, signed, visible and fidelity-bearing. An explicit no-cap token is not a claim of equal historical fidelity and does not widen producer/V557 permission.

**Authority verdict:** `PASS`.

---

## 2. Ownership and exact consumers

### Semantic owner

`RA-MUST-006-TEMPORAL-PROXY-ELIGIBILITY` is a cross-boundary runtime eligibility authority for the accepted V557/V558→V3 path. It creates no producer semantic family.

### Exact direct consumers

- **V557-P2** — records/binds the applicable proxy-eligibility rule reference or explicit missing/denied eligibility on the runtime-authorized object record. This does not replace `CAN-003` item-use governance.
- **V558-P3** — evaluates proxy eligibility while applying the already-bound resolver precedence/tie law.
- **V558-P4** — emits exact `SelectionRecord`, fidelity and refresh metadata for the resulting resolution.

### Indirect consumer

- **V3** receives only the resulting `ResolvedStructuralContext` and selection/provenance receipts. V3 cannot override this registry or independently proxy raw producer objects.

### Explicit non-consumers

V553, V554, V555, V556 and V2 do not execute this authority. V553 remains evidence-time authority. V2 never receives temporal-proxy authority as causal evidence.

---

## 3. Authority inputs and admissible epistemic classes

Eligibility evaluation may use only immutable, exact, repository-resident material whose producer identity/hash and runtime publication authority have already passed the accepted V557/V558 contracts.

Required inputs where applicable:

- exact V553 `TEMPORAL_KEY` identity;
- exact candidate V553 `TEMPORAL_OBSERVATION` ID/hash;
- producer evidence/support time and declared granularity;
- exact V553 temporal relation/limit/negative-authority refs relevant to the candidate/use;
- exact producer causal-use permission;
- separate V557 item-use state under `CAN-003`;
- native geographic/structural scope and exact semantic resolution key;
- query time and declared granularity;
- accepted resolver `query_purpose` category;
- accepted resolver Phase-A / Phase-B / life-course-refresh role where applicable;
- this authority ID/version and matched rule ID/version.

Eligible anchor epistemic material is producer-owned temporal/structural prior authority. `GENERATED_RUNTIME_FACT` may appear only as caller-supplied binding/query criteria under the accepted resolver contract; it is never a proxy anchor. `RENDERED_EXPRESSION` is never an input to proxy eligibility.

---

## 4. Eligible object-class matrix

| Object class | Prior proxy anchor? | Forward proxy anchor? | Ruling |
|---|---:|---:|---|
| V553 `TEMPORAL_OBSERVATION` with exact lawful value/status/lineage | YES under R001 | YES under R002 precoverage rule | Sole first-release proxy-anchor class |
| V553 `TEMPORAL_KEY` | NO | NO | Resolution/grouping identity only |
| V553 `TEMPORAL_RELATION` | NO | NO | Preserved explanatory/constraint metadata; never a value anchor |
| V553 `TEMPORAL_LIMIT / NEGATIVE_AUTHORITY` | NO | NO | Constrains/blocks use; never a substitute observation |
| V552 structural fact | NO independent proxy | NO independent proxy | Reached through exact selected V553 observation lineage; cannot bypass V553 time |
| V554 affordance / applicability condition | NO | NO | May become applicable only through lawful temporal dependency resolution plus its own conditions |
| V555 route / route condition | NO | NO | Immutable structural possibility; temporal prerequisites resolve through exact V553 refs |
| V556 F1/F2 | NO | NO | Existing governed topology only; resolver may activate/defer/exclude, never proxy the topology itself |
| static position/stratum/geography/Horizon/AH reference objects | NO | NO | Not temporal measurements |
| producer negative/valid-empty/integrity objects | NO | NO | State/constraint authority, not temporal anchors |
| generated runtime facts / actor history | FORBIDDEN | FORBIDDEN | V3-owned generated truth; never proxy evidence |
| rendered expression/session material | FORBIDDEN | FORBIDDEN | Noncausal presentation material |

### Dependent-object closure law

A V554/V555/V556 object with one or more required temporal dependencies is eligible for downstream applicability only when every required temporal dependency has a lawful resolution under the accepted resolver contract and the dependent object's own producer conditions/permissions remain satisfied.

If any indispensable temporal dependency returns no lawful anchor, the dependent object is deferred/excluded under its accepted condition semantics. The resolver may not “proxy the route,” “proxy the interaction,” or “proxy the topology” as a shortcut.

---

## 5. Query-purpose and phase matrix

The phase categories below are the already-accepted **resolver generation/context roles** from TD-R04. They do not create or anticipate the separate W0 `ADP-008` V3 developmental-phase taxonomy. Any later, more detailed V3 developmental phase may narrow applicability but cannot widen this authority.

| Query purpose | Resolver role | Latest-prior | Earliest-post | Law |
|---|---|---:|---:|---|
| `STRUCTURAL_CONTEXT_PHASE_A` | environmental / position-generation context | YES | YES only while semantic key is precoverage | Ordinary generation/genealogy environmental context |
| `STRUCTURAL_CONTEXT_PHASE_B` | position-bound structural context | YES | YES only while semantic key is precoverage | Generated bindings may activate objects; bindings do not widen proxy eligibility |
| `STRUCTURAL_CONTEXT_REFRESH` | prospective life-course structural re-resolution | YES | YES only while semantic key remains precoverage | After at-or-before coverage exists, ordinary forward proxy is ineligible |
| `REPLAY_AUDIT_EXPLANATION` | deterministic replay/audit of a prior resolution | REPLAY ONLY | REPLAY ONLY | May reproduce an originally lawful decision; cannot create a new proxy decision |
| V3 actor-history generation as a substitute for missing structural context | any | NO | NO | Proxy is structural context, not lived event generation |
| biography/memory/personality/Enneagram inference | any | NO | NO | Forbidden temporal laundering |
| V2 rendering/session/conversation convenience | any | NO | NO | Presentation purpose cannot create structural authority |
| unspecified/ad-hoc/debug/query convenience | any | NO | NO | Missing recognized purpose fails closed |

### Genealogy

Parent, partner, child and recursive-generation subjects receive no special widening. They use the same Phase-A, Phase-B and refresh eligibility rules as any other generated subject.

### Birth specialization

When an eligible earliest-post precoverage selection occurs for a birth-initialization query, `EARLIEST_POST_BIRTH_ANCHOR` may be emitted as a reporting specialization tag. It remains `EARLIEST_POST_QUERY_PROXY` for precedence, eligibility and evidence-time semantics.

---

## 6. Rule registry

### R001 — latest prior structural context

**Rule ID:** `ADP006-R001-LATEST-PRIOR-STRUCTURAL-CONTEXT`  
**Version:** `1.0.0`

Eligibility requires all of:

1. candidate is an exact V553 `TEMPORAL_OBSERVATION` for the same governed semantic resolution key;
2. candidate evidence/support reference time is strictly earlier than query time under compatible declared granularity;
3. no lawful direct-support candidate was selected under the already-binding precedence law;
4. query purpose is `STRUCTURAL_CONTEXT_PHASE_A`, `STRUCTURAL_CONTEXT_PHASE_B`, or `STRUCTURAL_CONTEXT_REFRESH`;
5. candidate producer permission permits the requested structural-context use;
6. V557 item-use governance independently permits that use;
7. no applicable producer negative/limit authority blocks proxy/carry use;
8. object identity/hash/reference closure and temporal granularity are valid.

**Lag policy:** `NO_NUMERIC_CAP_EXPLICIT`.

R001 does not assert persistence from the observation time to query time. A selected prior proxy remains an approximation with `historical_observation_at_query_time=false`.

### R002 — earliest post-query precoverage context

**Rule ID:** `ADP006-R002-EARLIEST-POST-PRECOVERAGE`  
**Version:** `1.0.0`

Eligibility requires all of:

1. candidate is an exact V553 `TEMPORAL_OBSERVATION` for the same governed semantic resolution key;
2. candidate evidence/support reference time is strictly later than query time under compatible declared granularity;
3. no lawful direct-support candidate exists/was selected;
4. no lawful latest-prior candidate exists for that semantic key at that query time;
5. the semantic key is genuinely `PRECOVERAGE_AT_QUERY_TIME`: there is no lawful at-or-before temporal anchor after permission/negative/eligibility filtering;
6. query purpose is `STRUCTURAL_CONTEXT_PHASE_A`, `STRUCTURAL_CONTEXT_PHASE_B`, or `STRUCTURAL_CONTEXT_REFRESH`;
7. candidate producer permission permits the requested structural-context use;
8. V557 item-use governance independently permits that use;
9. no applicable producer negative/limit authority blocks forward proxy use;
10. object identity/hash/reference closure and temporal granularity are valid.

**Lag policy:** `NO_NUMERIC_CAP_EXPLICIT`.

R002 is a precoverage fallback only. Once a lawful direct or prior anchor exists for the semantic key, ordinary forward proxying is not eligible. Chronological closeness never overrides this rule.

---

## 7. Lag law

### 7.1 First-release maximum lag

No governed evidence inspected supports a universal numeric lag ceiling, and accepted runtime architecture explicitly permits an explicit no-cap token. The first-release rules therefore bind:

`maximum_lag_policy = NO_NUMERIC_CAP_EXPLICIT`.

This means:

- no arbitrary year threshold is invented;
- only a real exact V553 observation can anchor a proxy;
- same semantic key/native authority/permission/negative rules remain mandatory;
- the full lag is always reported;
- large lag lowers descriptive historical fidelity but does not become a hidden semantic denial threshold;
- a later finite cap requires a new authority version and therefore a new bound resolver/repository policy identity.

### 7.2 Signed lag

Canonical convention:

`signed_lag = selected_anchor_reference_time - query_time`

in the query's deterministically normalized declared time unit/granularity.

- prior proxy: signed lag `< 0`;
- forward proxy: signed lag `> 0`;
- direct support: signed lag `0` only where the selected producer support truly contains query time.

Always record `absolute_lag = abs(signed_lag)`.

If evidence time and query time cannot be deterministically compared at a compatible governed granularity, the candidate is ineligible with `TEMPORAL_GRANULARITY_INCOMPATIBLE`. The resolver may not coerce the units or invent an interval.

### 7.3 Fidelity

`NO_NUMERIC_CAP_EXPLICIT` is not a fidelity claim. `CoverageFidelityProfile` must expose proxy counts and signed/absolute lag distributions. No fidelity score or threshold may retroactively change producer evidence time or silently authorize/deny proxy use.

---

## 8. Negative authority and permission precedence

This section defines **eligibility filtering**, not a new resolver temporal-mode precedence.

For each candidate:

1. **Integrity first.** Hash/reference/version/identity corruption is `INTEGRITY_FAILURE`, not a semantic no-anchor fact.
2. **Producer permission first-class.** A producer denial or non-applicable requested use cannot be widened by ADP-006.
3. **V557 use governance remains separate.** `CAN-003` may narrow/deny use. ADP-006 cannot widen it.
4. **Producer negative/limit authority controls its declared affected use.** If exact V553/upstream negative authority explicitly blocks temporal proxy/carry/use for the candidate/key, the candidate is ineligible.
5. **Absence/noncomparability/missing authoritative value is not an anchor.** Unknown is not zero. Observed zero remains a valid observation when otherwise authorized.
6. **Generic negative metadata is not silently upgraded.** A relation/noncomparability record that does not govern proxy use remains preserved explanatory/negative context; this authority does not invent a new blocking scope for it.
7. **Eligibility rule must match exactly.** Missing rule, mismatched object class, purpose or direction means no proxy permission.
8. If no candidate survives the already-binding resolution procedure, the final temporal result is `NO_LAWFUL_TEMPORAL_ANCHOR` with the specific rejection/authority reasons recorded.

A denied observation does not automatically deny every other observation for the same key unless the producer negative authority is explicitly key/use scoped. Conversely, key/use-level denial cannot be bypassed by choosing a different observation.

---

## 9. Equal-rank, tie and multiplicity law

The existing AEX-004 tie law remains controlling; ADP-006 does not create a new ordering heuristic.

- Exact storage duplicates with the same authoritative object ID **and** authoritative hash may deduplicate.
- Lexicographic/stable ID ordering is serialization only.
- For a singular semantic resolution key, two or more nonidentical equal-rank candidates with no governed distinguishing precedence produce `AMBIGUOUS_EQUAL_RANK_AUTHORITY`; no winner is active.
- A complete tied set may be returned only when the producer/reference contract explicitly makes equal-rank multiplicity lawful for that resolution operation. The entire set must be preserved in canonical stable order.
- Distinct simultaneous pressure keys are separate semantic resolution keys and must not be converted into a “tie” merely because their times match.

The proxy registry cannot authorize “pick one arbitrarily.”

---

## 10. `historical_observation_at_query_time` semantics

This flag answers only whether producer-governed temporal support exists **at the query time**.

- `DIRECT_TEMPORAL_SUPPORT` → `true`, only when exact producer support contains query time at the declared granularity.
- `LATEST_PRIOR_OBSERVATION_PROXY` → `false`.
- `EARLIEST_POST_QUERY_PROXY` / `EARLIEST_POST_BIRTH_ANCHOR` → `false`.
- no selected temporal anchor / integrity failure → `null` / not applicable.

A prior proxy never becomes direct support because it is nearby. A future proxy never becomes historical observation at query time because it is useful for generation.

---

## 11. SelectionRecord obligations

Every candidate considered for a temporal semantic key, whether selected, rejected, deferred or ambiguous, must produce/reach a deterministic `SelectionRecord` containing at minimum:

- repository bundle ID;
- ContextQuery ID/hash;
- resolver policy version;
- ADP-006 authority ID/version/hash;
- matched proxy rule ID/version or explicit `NO_MATCHING_PROXY_RULE`;
- semantic resolution key;
- candidate logical collection/object class;
- exact authoritative object ID/hash and V553 observation/key refs;
- producer permission state;
- separate V557 item-use state;
- query purpose and resolver Phase-A/Phase-B/refresh role;
- query time and granularity;
- producer evidence/support start/end and selected observation/reference time;
- temporal resolution mode and birth-specialization tag if applicable;
- signed lag, absolute lag and lag unit;
- lag policy and `lag_ceiling_status` (`NO_NUMERIC_CAP_EXPLICIT` in v1 rules);
- `historical_observation_at_query_time`;
- `future_evidence_used_as_proxy` boolean;
- exact negative/limit refs and filtering outcome;
- tie group/rank/multiplicity outcome;
- caller-supplied generated-binding refs used as selection criteria, if any;
- selection/rejection/deferment/fail-closed reason;
- provenance refs;
- deterministic SelectionRecord hash.

For any future proxy, the record must additionally make machine-explicit:

- `future_evidence_used_as_proxy = true`;
- `historical_observation_at_query_time = false`;
- `lived_history_claim = false`;
- any future-dependent explanatory metadata is noncausal/explanatory unless separately authorized for causal use at query time.

---

## 12. Fail-closed states

The authority recognizes at minimum these distinct outcomes/reasons:

- `PROXY_ELIGIBLE_LATEST_PRIOR`;
- `PROXY_ELIGIBLE_EARLIEST_POST_PRECOVERAGE`;
- `PROXY_OBJECT_CLASS_NOT_AUTHORIZED`;
- `PROXY_QUERY_PURPOSE_NOT_AUTHORIZED`;
- `PROXY_DIRECTION_NOT_AUTHORIZED`;
- `PROXY_ELIGIBILITY_RULE_MISSING`;
- `PROXY_BLOCKED_BY_PRODUCER_PERMISSION`;
- `PROXY_BLOCKED_BY_V557_ITEM_USE`;
- `PROXY_BLOCKED_BY_NEGATIVE_AUTHORITY`;
- `CANDIDATE_NOT_AUTHORITATIVE_OBSERVATION`;
- `TEMPORAL_GRANULARITY_INCOMPATIBLE`;
- `AMBIGUOUS_EQUAL_RANK_AUTHORITY`;
- `DEPENDENT_TEMPORAL_PREREQUISITE_UNRESOLVED`;
- `NO_LAWFUL_TEMPORAL_ANCHOR`;
- `INTEGRITY_FAILURE`.

`NO_LAWFUL_TEMPORAL_ANCHOR` must not erase the more specific candidate rejection reasons in the SelectionRecord ledger.

---

## 13. Forbidden proxy laundering

The following are forbidden irrespective of convenience:

1. rewriting V553 evidence/support time to query time;
2. treating prior proxy as producer-declared persistence or direct support;
3. treating future proxy as evidence that existed at the earlier query time;
4. turning future proxy into childhood exposure, parent belief, memory, biography, event or route traversal;
5. converting V553 point observation into an interval without producer interval authority;
6. interpolation, linear or otherwise, absent separate explicit authority;
7. nearest-wave selection;
8. choosing future because it is numerically closer than the lawful prior;
9. using mutable `latest`, filesystem order, lexicographic object ID or arbitrary tie-breaking as semantic precedence;
10. proxying V554/V555/V556 objects wholesale instead of resolving their exact temporal dependencies;
11. using geography, generated position, query purpose or developmental convenience to widen producer/V557 permission;
12. treating absence/noncomparability as zero/neutral;
13. allowing V2/session/render data to create or modify proxy eligibility;
14. allowing V3 to mutate an old resolver receipt after later evidence or later generated bindings appear.

---

## 14. Versioning, provenance and replay

### Authority identity

Registry authority:

`RA-MUST-006-TEMPORAL-PROXY-ELIGIBILITY@1.0.0`.

Rule identities:

- `ADP006-R001-LATEST-PRIOR-STRUCTURAL-CONTEXT@1.0.0`;
- `ADP006-R002-EARLIEST-POST-PRECOVERAGE@1.0.0`.

### Version-change law

Any change to eligible object classes, recognized query purposes, prior/forward permission, precoverage condition, lag policy, negative-use treatment or multiplicity declaration requires a new authority/rule version. A changed bound authority version produces a new policy/repository identity under the accepted V557/V558 immutability law. Old bundles and SelectionRecords remain replayable under their original authority version.

### Provenance

V557-P2 records exact proxy rule refs on item authorization records. V558 repository/policy manifests bind the registry ID/version/content hash. SelectionRecords retain the exact rule and producer object IDs/hashes used. No runtime component may load an unversioned mutable proxy rule.

### Replay

For the same immutable repository bundle, query, generated bindings, resolver policy, ADP-006 registry version and item-use state, eligibility and resulting temporal selection must be deterministic. Later observations or policy versions never rewrite an earlier receipt; they create a new bundle/query resolution.

---

## 15. Hostile fixtures

The implementation acceptance harness for this authority must include at least:

1. **Direct support bypasses proxy authority:** exact producer support contains query time → `DIRECT_TEMPORAL_SUPPORT`; no proxy permission needed; historical flag true.
2. **Ordinary prior:** observation 1985, query 1988, structural Phase A → R001 eligible, signed lag `-3`, historical flag false.
3. **Earlier-born precoverage parent:** first observation 1990, birth/query 1961 → R002 eligible if all permissions pass; signed lag `+29`; tag `EARLIEST_POST_BIRTH_ANCHOR`; no-cap token recorded; historical flag false; lived-history claim false.
4. **Forbidden purpose:** same 1961 candidate requested for V2 biography/rendering → no proxy permission / no lawful anchor.
5. **Prior beats closer future:** 1985 prior and 1990 future at 1988 → prior lane wins under existing precedence even if future is closer; no nearest-wave behavior.
6. **No matching eligibility rule:** otherwise usable observation but no matching rule ref/purpose/class → proxy rejected and no lawful anchor if no direct support.
7. **Large lag is visible, not silently normalized:** a 40-year eligible precoverage lag remains signed/absolute in fidelity metadata under `NO_NUMERIC_CAP_EXPLICIT`; no claim of equal fidelity.
8. **Ambiguous equal rank:** two nonidentical same-rank observations for singular key → `AMBIGUOUS_EQUAL_RANK_AUTHORITY`; no active winner.
9. **Lawful set-valued tie:** exact producer/reference contract declares set-valued multiplicity → return complete tied set in stable serialization order.
10. **True duplicate:** same authoritative ID+hash duplicated in storage → deduplicate without semantic loss.
11. **Point-as-interval attack:** point observation at 1994 queried at 1995 is not direct support; proxy eligibility is evaluated instead.
12. **Permission laundering attack:** producer or V557 item-use denial + matching ADP-006 rule → remains denied; ADP-006 cannot widen.
13. **Observed zero:** exact authorized zero observation remains a candidate; zero is not missing.
14. **Negative authority:** exact negative/limit authority whose affected use blocks proxying → candidate rejected even if chronologically best.
15. **Dependent route with two temporal prerequisites:** one resolves, one returns no anchor → route remains unresolved/deferred; resolver may not proxy the route wholesale.
16. **Future-proxy-to-memory attack:** future structural proxy offered as V3 childhood exposure/memory → reject; proxy receipt is structural context only.
17. **Phase-B rebinding:** new generated position may expose additional conditioned objects but cannot rewrite evidence time or widen proxy permissions; same key/time/candidate set reproduces same anchor.
18. **Mutated evidence identity:** same semantic ID with changed evidence time/hash under unchanged bundle identity → integrity failure, never silent reselection.

---

## 16. Present-terrain disposition

Current checked-in V553 code still contains interpolation/aggregate machinery and repository-discovery conveniences from the superseded implementation path. Those surfaces are non-authoritative for this decision. Current V558+ code is governance/readiness review terrain rather than the accepted standalone repository/resolver implementation and contains no canonical ADP-006 rule registry.

Therefore no current interpolation, readiness score, mutable latest-path behavior, global status or legacy runtime-graft behavior is promoted into proxy authority.

---

## 17. Consumer-release sufficiency

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT`

Meaning: this authority is sufficient to discharge **MUST-006** as a semantic dependency for its named consumers. It does **not** independently release V557-P2, V558-P3 or V558-P4, which remain gated by their other accepted CAN/EXT/implementation dependencies and Vozhd adjudication.

No production implementation is released by this result.

---

## 18. Final authority statement

### THIS AUTHORITY CREATES

- a versioned, fail-closed eligibility registry for prior and earliest-post temporal proxies;
- an exact first-release proxy anchor class: V553 `TEMPORAL_OBSERVATION`;
- purpose/phase restrictions;
- independent prior/forward permission;
- explicit precoverage-only forward eligibility;
- explicit no-numeric-cap lag semantics with mandatory signed lag/fidelity reporting;
- negative/permission filtering and existing tie-law integration;
- SelectionRecord/replay/provenance obligations;
- hostile anti-laundering fixtures.

### THIS AUTHORITY DOES NOT CREATE

- resolver precedence;
- V557 runtime-use permission;
- V553 evidence time or validity intervals;
- interpolation or nearest-wave fallback;
- actor history, memory, biography or developmental events;
- new V554/V555/V556 semantic families;
- V3 developmental-phase taxonomy;
- any numeric historical-fidelity threshold.

**`ADP_006_TEMPORAL_PROXY_AUTHORITY = PASS`**
