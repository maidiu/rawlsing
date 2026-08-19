# M2 — V554 -> V555 hostile seam oracle

**Oracle:** `M2_V554_V555_ATOMIC_ROUTE_HOSTILE_ORACLE@1.0.0`  
**Accepted inputs:** SCR554 `b5d745ac70c833324c8be0addf6c08ad72372263`; SCR555 `49a9ce7cd830eb670cf1f9d381d4d33e56ddf682`.  
**Production implementation:** not authorized.

| ID | hostile case | required result |
|---|---|---|
| M2-H01 | V555 receives exact canonical SCR554 F1 with state `ELIGIBLE`, exact B1 whose `f1_id_or_null` matches it, and `allowed_v555_structural_use=true` | route may proceed to the governed V555 route-rule gate; F1 is the sole upstream semantic participant |
| M2-H02 | B1 is present but F1 is absent/null | no V555 route; B1 cannot reconstruct F1 |
| M2-H03 | F1 is present but B1 is missing, mismatched, hash-invalid, or `allowed_v555_structural_use=false` | no positive V555 route; fail closed at seam |
| M2-H04 | Two canonical F1s have identical visible source/channel/receiver bindings but different canonical `F1_id` | they cannot collapse; if each is independently lawful, they seed distinct V555 route identities because field 1 differs |
| M2-H05 | Direct admission and V553 object are duplicate physical paths for one `SIG-001` semantic support | SCR554 emits at most one canonical F1; V553 path is provenance/reference-only; V555 route multiplicity remains one |
| M2-H06 | Multiple same-kind alias/reissue physical refs resolve to one canonical basis | one canonical F1; aliases remain provenance; no route multiplication |
| M2-H07 | Direct and V553 candidates overlap but full material equivalence cannot resolve | upstream `EQUIVALENCE_UNKNOWN`/K07-compatible fail-closed; no F1 reaches V555 |
| M2-H08 | One exact invocation contains mixed/unresolved required V554 authority snapshots differing in rule version/hash with no governed precedence | upstream `NONASSERTABLE_UNKNOWN_OR_CONFLICTING_STATIC_AUTHORITY` / K07; zero positive F1; version/hash difference alone cannot manufacture route multiplicity |
| M2-H09 | Two rule-version/hash identities are already governed as separate exact semantic authorities or separate exact invocations | their canonical F1 identities may differ; M2 preserves them without treating unresolved authority as resolved |
| M2-H10 | V555 is given a `StructuralEmpiricalAdmission` but no canonical F1/B1 | reject; no route reconstruction |
| M2-H11 | V555 is given a V553 temporal object/label but no canonical F1/B1 | reject; V553 cannot bypass V554 route eligibility |
| M2-H12 | V555 is given a legacy V554 seed/readiness ID or current implementation slot label | reject; legacy identifier cannot stand in for canonical F1/B1 |
| M2-H13 | Exact inherited SCR554 F2 IDs accompany a valid route | preserve exact references only; V555 does not re-evaluate or rename them |
| M2-H14 | Consumer asks V555 to copy an inherited F2 into the route-born predicate registry | reject; route-born registry remains independently governed and currently `VALID_EMPTY` count 0 |
| M2-H15 | B1 contains different sorted F2 IDs but the same exact F1 | B1 identity/replay may differ as governed; V555 route semantic identity remains keyed by F1 plus the six V555 fields, not by B1/F2 |
| M2-H16 | B1 is added as an eighth route tuple member | reject contract mutation; frozen route tuple remains seven fields |
| M2-H17 | F2 ID is added as a route tuple member | reject contract mutation; inherited applicability is not V555 route identity |
| M2-H18 | Route identity omits exact F1 ref and keeps only source/channel/receiver | reject; two different F1s could collapse |
| M2-H19 | Route identity replaces exact F1 ref with proposition label/text | reject; label reconstruction is forbidden |
| M2-H20 | F1 content-derived identity or SCR554 authority bundle cannot be dereferenced exactly during replay | fail closed; no latest/fuzzy/default repair |
| M2-H21 | Same exact SCR554 contract/rule/signature/authority bundle and same V555 route inputs arrive in different row/file order | identical F1/B1 and identical seven-field V555 route identity/result |
| M2-H22 | Rejected duplicate V553 provenance is added/removed around a lawful direct F1 | canonical F1 and V555 route identity unchanged |
| M2-H23 | Applicable K05/K08/K09 hard block crosses B1 with `allowed_v555_structural_use=false` | no V555 route; negative cannot be evaded by reconstructing F1 from ancestry |
| M2-H24 | K01-K03 deferred F2 accompanies positive F1/B1 allowed for structural use | route may exist structurally; V555 preserves F2 refs but never asserts runtime satisfaction |
| M2-H25 | V555 route-born predicate registry is empty | lawful `VALID_EMPTY`; no filler predicate/effect |
| M2-H26 | Additional mediation hop is attempted inside one F1-derived route | reject; each additional hop is another atomic V555 route |
| M2-H27 | Physical fusion proposal proves rowset parity only | insufficient; must prove exact F1/B1, seven-field route identity, typed states, reference closure, permissions, consumers and replay equality |
| M2-H28 | M1 later changes SCR554 basis/dedup/F1/B1/authority contract hash materially | this M2 receipt becomes stale; re-run M2 against new exact SCR554 head/blob before whole-machine closure |

## HQ authority-snapshot guard

The critical ordering is inherited verbatim from accepted SCR554:

1. `STATIC_AUTHORITY_COMPLETENESS` runs before duplicate equivalence and before F1 emission.
2. `unknown/conflicting required authority without governed precedence -> K07/nonassertable`.
3. Only after authority is exact may duplicate equivalence and the conjunctive F1 court run.

Therefore **different rule version/hash values do not themselves authorize a second positive F1 inside one mixed/unresolved exact invocation**. The identity-sensitive SCR554 cases for changed semantic authority apply only after the authority relation is itself governed/resolved.

## Required invariants

1. `EXACT_V554_F1_REF` means the accepted canonical SCR554 `F1_id`, not an admission, V553 object, legacy seed or label.
2. Exactly one `ELIGIBLE` canonical F1 participates in one V555 route.
3. Exact B1 must prove the same F1 and `allowed_v555_structural_use=true`; B1 is not a route semantic participant.
4. Different canonical F1 IDs cannot collapse merely because the other six route fields coincide.
5. Duplicate physical provenance contributes at most one canonical F1 and therefore at most one corresponding route input.
6. F2 stays V554-owned exact-reference-only.
7. V555 route-born predicate authority remains independent and may lawfully be empty.
8. The frozen route identity remains exactly seven ordered fields beginning with the exact F1 ref.
9. Replay remains bound to exact SCR554 contract/rule/signature/authority/reference closure.
10. Any material later SCR554 change invalidates this checksum until rechecked.
