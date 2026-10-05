# 00 — HQ213 V556 FINAL HOSTILE REREVIEW — independent review — R1

**Role:** independent hostile reviewer. No implementation. No repair. No merge. No self-adoption.
**Branch:** `agent/reviewer-pyat-hq213-v556-final-rereview-r1`
**Review tip:** `f459efc897965bc1e57b48659028c661c816ba3f` (verified equal to the pushed review branch before work)
**Candidate:** `agent/rabochii-pyat-hq211-v556-unbounded-gate-repair-r1 @ e4d7e6f7352e60da9de956c7875293fca141d371`
**Repair base (my HQ210 review's candidate):** `3a2dcafe024b2556af1df909deb5452841e45b7c`
**Prior hostile review:** `46bf1ac246f51d7499bccf56e41add78779e00ad` (mine)
**Architecture of record:** `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/recalibration/TD_R03_V556/RESULT.md`

## DISPOSITION

`V556_BOUNDED_REPAIR_PARTIAL__NAMED_DEFECT`

**All four blocking repairs and all four required low-severity repairs I named in HQ210 are genuinely closed at machinery level.** I re-ran every one of my original escape routes and they now refuse. I drove five hand-built bypass routes that skip the helper constructors entirely and all five refuse. The semantic-`UNBOUNDED` gate holds through arbitrary nesting, through arrays, and through the binding validator. The valid-empty ceiling for the interaction and attractor families is now a machinery fact enforced at two independent surfaces. The participant-role ceiling is a genuine positive allowlist that refuses twelve novel labels I invented beyond the ten witnesses. The M3 and M2 seams are byte-identical. The positive topology core still evaluates SUPPORTED through the unmodified seam. The court grew 35→54 and the aggregate is **111/111**, which I reproduced.

Four bounded defects remain, and I am naming them rather than waving the repair through:

1. **The class↔family coherence check is only enforced on the author path, and its court test is vacuous.** `07_FINAL_DISPOSITION`-class claims in the repair narrative say "every class now names the family that authorizes it", which is true of the *map*. But a hand-built `GovernedRule` carrying a consistently rehashed contract whose class belongs to a different family **registers**: I registered two of them. The check lives only in `author_governed_rule`, never in `V556RuleMaterialRegistry.build`, so it is bypassed by the very hand-built-rule route the commission told me to attack.
2. **`test_schema_class_must_be_the_class_authorized_by_its_family` is vacuous** and its docstring claims the opposite of what it does. It asserts a map entry equals itself; it never attempts to bind a mismatched class and never expects a refusal. This is the same class of self-referential constant the prior court was criticised for — I flagged it in HQ210 as finding CRT-1 and the replacement reintroduced it.
3. **`test_w10_court_does_not_prove_itself_from_production_vocabulary` is self-referential by construction**: it dodges its own scan by string-concatenating the banned identifiers (`"BLOCKED" + "_STRONG_NOUNS"`), so it can never catch what it exists to catch. It is strictly worse than no test, because it reads as a guard.
4. **`test_payload_participant_helper_is_declared_a_court_helper_not_seam_enforcement` asserts a substring** (`"court" in doc and "not" in doc`) rather than the factual claim. The factual half — the seam does not reference the helper — is genuinely asserted and I confirmed it holds (zero references in the M3 source).

None of the four reintroduces a leak, and the fix is a small documentary/implementation consolidation. But two of them are *false proofs sitting in the court*, which is exactly what this lineage keeps having to repair, so they cannot be accepted silently.

## 1. What was run and verified

Environment: independent venv `/tmp/hq210venv`, CPython 3.11.3, pytest 9.1.1, read-only imports from a worktree at the exact candidate SHA. Probe scripts outside the repository.

### 1.1 Change set and blast radius — verified

```
git diff --name-status 3a2dcafe024b2556af1df909deb5452841e45b7c e4d7e6f7352e60da9de956c7875293fca141d371 -- rawlsing_next/
M  rawlsing_next/pre553_v556_positive_substrate.py
M  rawlsing_next/tests/test_pre553_v556_positive_substrate_court.py
```

Exactly two files, zero seam edits, matching the candidate's claim. Additionally:
- repository-wide search for importers of the changed module outside itself and its court: **zero**
- the M3 seam source contains **zero** references to `pre553_v556_positive_substrate`; M2 likewise

So the change is a pure leaf.

### 1.2 Seam byte-identity — verified

```
git hash-object rawlsing_next/m3_v556_higher_order_structural.py => 9a4b26b214686364a43d108dabf0d57dac0ed3b2
git hash-object rawlsing_next/m2_v555_atomic_route.py           => deef8a60613635a10faf7d89cd8cdf0c3b8a0710
```

The M3 blob `9a4b26b2…` is **exactly** the blob the HQ205 and HQ210 reviews recorded as the adopted seam. Neither seam file appears in the change set.

### 1.3 Court surface — independently reproduced

| Suite | Candidate claim | Independently observed |
|---|---|---|
| repaired focused court | 54 | **54 passed** |
| M3 court (unmodified) | 29 | **29 passed** |
| M2/V555 court (unmodified) | 28 | **28 passed** |
| **aggregate** | **111** | **111 passed** |

I also independently established the two baselines the candidate reasons from:

- **Old court against the unrepaired module** (`3a2dcafe0`): **92 passed** — `35 + 29 + 28`. So the pre-repair surface is green *and blind*, exactly as claimed.
- **New court against the unrepaired module**: **15 failed, 39 passed**. The 15 failures are the discriminating witnesses, and they are precisely the ones an implementer would expect: `w1, w1b, w2, w3, w4, w5, w5b, w6` plus `actor_semantic_participant_labels`, `participant_role_allowlist_is_the_ceiling_not_a_blacklist`, `binding_ref_object_id_is_checked_at_authoring`, `actor_named_schema_classes_are_withdrawn`, `schema_class_must_be_the_class_authorized_by_its_family`, `illustrative_labels_are_snapshot_only`, `payload_participant_helper_is_declared_a_court_helper`.

**The candidate's discriminating/preservation split is independently confirmed, not merely repeated.** `w3b, w7, w8, w9, w10` pass against both modules and are correctly labelled preservation-only / anti-vacuity witnesses. I verified the old court's one removed test (`test_blocked_nouns_are_quoted_from_adopted_law_not_invented`) is the constant assertion I flagged in HQ210, and that all 34 other old tests survive into the new court.

## 2. Attack 1 — the HQ210 escape routes, re-run: **ALL CLOSED**

| Route | HQ210 (unrepaired) | HQ213 (candidate) |
|---|---|---|
| UNBOUNDED string leaf carrying `DOMINATION` | SUPPORTED, object payload `{"k": "DOMINATION"}` | **refused** at authoring |
| UNBOUNDED exact_ref kind carrying `HEGEMONY` | SUPPORTED | **refused** at authoring |
| numeric magnitude `"0.87"` on a string leaf | SUPPORTED | **refused** at authoring |
| generic authoring of `V556_INTERACTION_RELATION` | authored → `GOVERNED_RULES_PRESENT` | **refused** at authoring and at registry build |
| generic authoring of `V556_ATTRACTOR_PREREQUISITE` | authored | **refused** at authoring and at registry build |
| ten actor/person-semantic role witnesses | 10 accepted, 0 refused | **0 accepted, 10 refused** |

Two of these are worth stating precisely, because the failure mode was subtle and the fix is correctly placed.

**The root cause was in the substrate, not the seam.** M3 constrains a string or kind value *only when the declaration is closed* (`m3:655-660`, `m3:667-669`) and copies the payload verbatim into the positive object (`m3:931`). The substrate was handing M3 an `UNBOUNDED` declaration and claiming closed governance in prose. The repair therefore belongs in the substrate, and the seam stays byte-identical — which it does.

**Closing the declaration closes the value route.** I verified the second-order effect directly: with a closed enum, M3 now enforces the enum at *evaluation* time. Probe D1 — a schema declaring `("PERMITTED_A","PERMITTED_B")` — yields `SUPPORTED` for `PERMITTED_A` and `RESULT_SCHEMA_NONCONFORMING` for `DOMINATION`. Probe D2 — a declared list of digit strings `("0.87","1.0")` — yields `SUPPORTED` for the declared `0.87` and `RESULT_SCHEMA_NONCONFORMING` for an undeclared `3.14159`. So the gate is not merely syntactic: an undeclared magnitude can no longer reach a positive object.

## 3. Attack 2 — bypass routes that skip the helper constructors: **ALL CLOSED**

The commission asked me to prove the gate runs before any positive-object assembly. I drove every bypass the commission named, plus a deep-nesting variant:

| Bypass | Result |
|---|---|
| hand-authored schema mapping with `allowed_values_or_unbounded_marker: "UNBOUNDED"` (never touches `_node_string`) | **refused** — `$.root.k declares an UNBOUNDED semantic string value leaf` |
| hand-authored mapping with an UNBOUNDED exact-ref kind list | **refused** |
| hand-built `ResultContractBinding` carrying an UNBOUNDED schema, passed straight to `validate_result_contract_binding` | **refused** — the validator walks the schema |
| hand-built `GovernedRule` naming `V556_INTERACTION_RELATION`, straight to `V556RuleMaterialRegistry.build` | **refused** |
| hand-built `GovernedRule` naming role `CIVIC_ASSOCIATION`, straight to registry build | **refused** |
| UNBOUNDED leaf buried six object levels deep | **refused** — `$.root.lvl5.lvl4.lvl3.lvl2.lvl1.lvl0 …` |
| UNBOUNDED semantic string as an **array item** | **refused** |

The gate genuinely runs on the node *mapping* rather than only inside the constructors, so hand-authoring cannot evade it, and it runs in every entry point (`author_closed_result_schema` → `author_result_contract_binding` → `validate_result_contract_binding` → `author_governed_rule` → registry build). Note also that `GovernedRule` is the only constructible carrier in the module (`__all__` exposes no request dataclass), and the registry re-validates it, so there is no unprotected constructor to slip past.

## 4. Attack 3 — semantic vs structural `UNBOUNDED`: **SEPARATION HELD**

This was the repair's sharpest risk — over-closing and losing lawful structural cardinality. It did not happen:

- semantic **string** leaf: `UNBOUNDED` refused; an omitted list refused; `None` refused
- semantic **exact_ref** kind leaf: same
- **array** `max_items_or_unbounded_marker`: `"UNBOUNDED"` **still allowed** where commissioned, and it cannot carry a semantic value or kind — the item node is validated recursively, so an UNBOUNDED semantic leaf inside an UNBOUNDED array is refused while the array itself remains lawful

Verified directly: `_node_array(_node_string("OBJECTIVE_TEXT_LABEL", ("X",)), min_items=1, max_items="UNBOUNDED")` authors successfully; the same array with an UNBOUNDED string item is refused (`$.root.items[] declares an UNBOUNDED semantic string value leaf`).

## 5. Attack 4 — authorable family set at both surfaces: **ENFORCED**

`TRANCHE_LOCAL_AUTHORABLE_FAMILIES = ("V556_TOPOLOGY",)`, and the complement is named (`V556_ATTRACTOR_PREREQUISITE`, `V556_INTERACTION_RELATION`).

- `V556_TOPOLOGY` → authors, registers, and evaluates SUPPORTED through the unmodified seam (witness w7 re-run green)
- `V556_INTERACTION_RELATION` → refused at `author_governed_rule` **and** independently at `V556RuleMaterialRegistry.build`; a hand-built rule is refused too
- `V556_ATTRACTOR_PREREQUISITE` → same

The valid-empty claim is therefore a **machinery ceiling**, not an accident of the shipped instance. That is exactly what my HQ210 finding F-3 demanded, and it is honestly labelled as tranche-local rather than timeless.

## 6. Attack 5 — role ceiling is an allowlist, not blacklist theatre: **TOTAL OVER ITS COMPLEMENT**

`TRANCHE_LOCAL_FAMILY_PARTICIPANT_ROLE_MAP` is `{V556_TOPOLOGY: (STRUCTURAL_ENDPOINT_A, STRUCTURAL_ENDPOINT_B)}` — derived only from the roles the canary already used, with nothing invented.

I tested twelve novel labels **beyond** the ten HQ210 witnesses, deliberately including the kind of innocuous social-science vocabulary a blacklist would miss:

```
CIVIC_ASSOCIATION, COLLECTIVE_IDENTITY, SOCIAL_TRUST, GROUP_COHESION,
MEMBER_ALLEGIANCE, NORMATIVE_COMMITMENT, CULTURAL_ORIENTATION,
POLITICAL_IDENTIFICATION, RELIGIOUS_AFFILIATION, ETHNIC_SELF_LABEL,
STRUCTURAL_ENDPOINT_C, ENDPOINT_A
→ 0 of 12 accepted
```

The blacklist survives as defence in depth, but it is no longer what makes the claim true: an unlisted label is refused *by construction*, whether or not it looks actor-semantic. That is the correct shape for this ceiling.

## 7. Attacks 6 and 7 — seam identity and no new ontology: **PASS**

- M3 and M2 byte-identical (§1.2), and neither seam references the substrate.
- No new semantic family, no new relation kind, `AUTHORIZED_INTERACTION_RELATION_KINDS` still `()`, no attractor population, no scalar pressure field, no actor implementation. The public surface (`__all__`) contains no new authority-bearing callable; the repair is additive only in tranche-local ceiling constants and their snapshot exposure.
- The schema-class set **shrank**: `OBJECTIVE_ACTOR_POSITION` and `OBJECTIVE_ACTOR_OPPORTUNITY` are withdrawn, which is a reduction consistent with the actor-role ceiling.

## 8. Attack 8 — court authenticity: **STRONG EXCEPT TWO FALSE PROOFS**

The court is substantially better than the one I reviewed. It is not self-referential on the properties that matter: the hostile literals are written independently in the court file, `_HQ211_BLOCKED_NOUNS` deliberately omits `"FIELD"` (an over-broad production token) to show the list is not read back, and the refusal assertions expect specific messages per route. The discriminating/preservation split is honest — the candidate volunteered that five of its own witnesses also pass against the unrepaired module, and I confirmed that split independently.

Two defects, both named in §10.

## 9. Attack 9 — the low-severity repairs: **3 OF 4 VERIFIED, 1 DORMANT**

| Claimed repair | Verdict |
|---|---|
| `binding_ref.object_id` consistency at authoring | **VERIFIED** — the check exists and fires; court test genuinely drives a relabelled ref and expects the refusal |
| actor-named schema classes withdrawn + class→family linkage | **PARTIALLY VERIFIED** — the withdrawal is real (two classes gone); the linkage is enforced **only on the author path** and its court test is vacuous (§10 D-1, D-2) |
| deep-freeze of hand-built `ResultContractBinding` | **VERIFIED** — `author_governed_rule` now stores `_freeze(result_contract.binding)`; in-place mutation of top-level and nested keys raises (`AttributeError` on the `MappingProxyType`, which is the correct frozen behaviour; the court expects `TypeError` and passes) |
| truthful documentary/helper classification of the payload validator | **VERIFIED (implementation) / WEAK (test)** — the docstring now says court/helper and "NOT wired into the M3 seam", and I confirmed the seam contains zero references to it. The court's assertion of that is a substring check (§10 D-4) |

## 10. Named defects

### D-1 (defects the "no dormant gap" claim) — class↔family linkage is not enforced on the registry path

`author_governed_rule` contains:

```
if TRANCHE_LOCAL_ADMITTED_SCHEMA_CLASS_FAMILY_MAP.get(bound_class) != family:
    raise SubstrateAuthoringError("... class and family must agree")
```

`V556RuleMaterialRegistry.build` contains no equivalent. So a hand-built `GovernedRule` whose rule body and contract are **consistently rehashed** carries an arbitrary admitted class into `GOVERNED_RULES_PRESENT`. I registered two such rules:

```
class=OBJECTIVE_MEASUREMENT   -> REGISTERED
class=OBJECTIVE_WORLD_STATUS  -> REGISTERED
```

In this tranche the gap is **dormant**: all three admitted classes map to `V556_TOPOLOGY`, the only authorable family, so no mismatched pair can be constructed. It becomes live the moment a second family is opened or the class map grows — exactly the "widening requires a governed authority" step the ceiling note anticipates. Recommended minimal repair: move (or duplicate) the check into `V556RuleMaterialRegistry.build`, immediately after `validate_result_contract_binding(r.result_contract)`, reading the class from `r.result_contract["result_schema"]["semantic_class"]`, and add a court witness that constructs a genuinely mismatched pair (which requires temporarily adding a test-only family entry, or asserting the check by monkeypatching the map).

### D-2 (false proof) — `test_schema_class_must_be_the_class_authorized_by_its_family` is vacuous

The test's docstring says *"Repair 7: a class/family mismatch is refused."* The body authors a coherent `OBJECTIVE_WORLD_STATUS` binding and then asserts:

```
assert S.TRANCHE_LOCAL_ADMITTED_SCHEMA_CLASS_FAMILY_MAP["OBJECTIVE_WORLD_STATUS"] == "V556_TOPOLOGY"
```

It never binds a mismatched class to a family, never calls `author_governed_rule` with an incoherent pair, and never expects a refusal. It asserts a dictionary entry equals itself. Its own comment concedes the point (*"the only authorable family is V556_TOPOLOGY, so this asserts the linkage is consulted"*) — asserting a map entry is not evidence that a check consults it. This is the same defect class as the old court's `noun in BLOCKED_STRONG_NOUNS`, which this repair removed elsewhere. Note the test *passes against the unrepaired module too* only in the sense that it is in the failing set for import reasons; as an assertion it is unfalsifiable.

### D-3 (false proof) — `test_w10` is self-referential by construction

The test parses its own module's AST for `BLOCKED_STRONG_NOUNS`, `_FORBIDDEN_PARTICIPANT_ROLE_TOKENS`, `_FORBIDDEN_PERSON_STATE_ROLES`, then dodges its own scan by writing the banned names as concatenations:

```
banned = {"BLOCKED" + "_STRONG_NOUNS", "_FORBIDDEN" + "_PARTICIPANT_ROLE_TOKENS", ...}
```

Because the identifiers are assembled at runtime, the AST will never contain them as names, so the primary assertion is true by construction and can never fail. It is strictly worse than omitting the test, because it presents as a guard against exactly the self-referential pattern the court is trying to avoid. The honest version is either a documented manual check or an external lint, not a test that cannot fail.

### D-4 (weak witness) — the helper-classification test asserts substrings

`assert "court" in doc.lower() and "not" in doc.lower()` is satisfied by almost any docstring containing those substrings. The other half of the same test — `assert "validate_payload_against_participants" not in inspect.getsource(seam)` — is a genuine, falsifiable claim and I confirmed it holds. Recommend keeping that half and replacing the substring half with an assertion on an explicit classification constant (e.g. a module-level `PAYLOAD_VALIDATOR_CLASSIFICATION = "COURT_HELPER_NOT_SEAM_ENFORCEMENT"`) so the claim is machine-checkable.

### D-5 (informational) — environment and baseline classification

The candidate discloses that no pytest existed on the host, that it installed pytest 9.1.1 into an isolated throwaway venv with `--break-system-packages`, and that only 4 of 157 test files are materialized under the commissioned sparse scope, so it explicitly does **not** claim a full-suite baseline. It supplies a structural substitute instead: two changed files, zero production importers, seam contains zero references to the substrate, seam byte-identical — all four of which **I verified independently**. This is the correct discipline and I neither upgrade nor dispute it. My own 111/111 reproduction is likewise an independent mechanical check in a disclosed environment, not a governed certification.

## 11. What is sustained (do not discard)

- Every HQ210 blocking finding is closed, verified by re-running the original probes.
- Every bypass route the commission named is closed, including deep nesting and array items.
- Semantic `UNBOUNDED` is closed while lawful structural cardinality `UNBOUNDED` survives.
- The valid-empty ceiling for both empty families is now machinery, enforced at two independent surfaces.
- The participant-role ceiling is a real allowlist, total over its complement, verified against twelve novel labels.
- The class set shrank (two actor-named classes withdrawn).
- `binding_ref.object_id` is checked at authoring; hand-built bindings are frozen at rule authoring.
- The M3/M2 seams are byte-identical and contain zero substrate references; the change is a pure leaf with zero production importers.
- The positive topology core still evaluates SUPPORTED through the unmodified seam (w7 re-run green).
- The court is substantially non-self-referential, and the candidate honestly self-reported which of its own witnesses are non-discriminating — I confirmed that split independently.
- 111/111 reproduces; the 15-failure discriminating set against the unrepaired module reproduces; the old 92/92 baseline reproduces.

## 12. Bound on this review

No raw source, no locator discovery, no warrant, no live C4, no C7, no actor/person implementation, no attractor population, no new V556 semantics, no implementation edits, no repair, no merge, no self-adoption. All probes were read-only imports from a worktree at the exact candidate SHA; probe scripts were written outside the repository. I modified no implementation file. The only artifacts are these five return files.

## 13. Answer to the commission, plainly

`accept_for_hq_adoption = false`, on four named and bounded defects — two of which are false proofs sitting in the court rather than leaks.
`escape_routes_closed = true` (all six HQ210 routes plus every commissioned bypass).
`authorable_family_ceiling_enforced_at_both_surfaces = true`.
`role_ceiling_is_allowlist_based = true` (0 of 12 novel labels accepted).
`seam_byte_identical = true`. `new_ontology_introduced = false`.
`court_surface = 111/111 reproduced; 15 discriminating witnesses confirmed against the unrepaired module`.
`smallest_blocking_repair = D-1 + D-2` (duplicate the class/family check into the registry build and replace the vacuous test with a real one), with D-3 and D-4 as court-honesty repairs.
`V556 remains unadopted.`
