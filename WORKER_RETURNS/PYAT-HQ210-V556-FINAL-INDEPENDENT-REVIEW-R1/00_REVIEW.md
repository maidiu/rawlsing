# 00 — HQ210 V556 final hostile independent review — R1

**Role:** independent hostile reviewer. No implementation. No self-adoption. No merge. No candidate repair.
**Branch:** `agent/reviewer-pyat-hq210-v556-final-r1`
**Review tip:** `bb453566e96ab11bb6f54574c2e45962ec32a9e4` (verified equal to pushed `origin/agent/reviewer-pyat-hq210-v556-final-r1` before work)
**Commissioned startup base:** `7cc1ce20238e06e4b785b6a804cc885cd19d641a` (ancestor of the review tip; the tip is the review-setup commit carrying this commission)
**Candidate under review:** `agent/rabochii-pyat-hq206-v556-repair-r1 @ 3a2dcafe024b2556af1df909deb5452841e45b7c`
**Original repair startup:** `1be02e9505df56291f61e46a79b37e49e8afdf9b`
**Repair base (control):** `87268ffaa60ebd9119aa46dc3f664e12d632b4d5`
**Prior hostile review:** `5f3b799736eefbde56086b82287da80e20dbe890`
**Architecture of record:** `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/recalibration/TD_R03_V556/RESULT.md`

## DISPOSITION

`V556_REPAIR_PARTIAL__BOUNDED_REPAIR_REQUIRED`

**V556 remains unadopted.** The repair is a genuine and substantial improvement: seven of the prior review's ten findings are closed with behavioural, machinery-level evidence, the load-bearing change is a correct reduction (the inverted non-inference law is un-inverted), the adopted M3/M2 seam is byte-identical, and the positive core survives. But the commission's attack #2 — *"generic enum/exact-ref escape routes"* — was correctly anticipated and **is still open**: the authoring-time ontology gate validates only **declared** enum values and **declared** exact-ref kinds on **closed** leaves. A rule may declare a leaf `UNBOUNDED`, and then an arbitrary forbidden value reaches a positively evaluated V556 object with `M3DecisionState.SUPPORTED`. I reproduced this three ways. Two receipt claims are therefore false at the machinery level, and the interaction family — which the candidate correctly reasons must be lawfully `VALID_EMPTY` — is still authorable and positively evaluable through the generic path. All of it is bounded and documentary plus one narrow gate change.

## 1. What was actually run and verified

Environment: independent venv, CPython 3.11.3, pytest 9.1.1. Read-only imports of the candidate module; probe scripts outside the repository.

### 1.1 Change set and blast radius — verified

`git diff --name-status 87268ffaa 3a2dcafe0` is exactly:

```
A WORKER_COMMISSIONS/PYAT-HQ206-V556-ONTOLOGY-AUTHORING-REPAIR-R1/00_COMMISSION.md
A WORKER_RETURNS/PYAT-HQ206-V556-ONTOLOGY-AUTHORING-REPAIR-R1/00_RETURN.md ... 07_FINAL_DISPOSITION.json   (8 artifacts)
M rawlsing_next/pre553_v556_positive_substrate.py
M rawlsing_next/tests/test_pre553_v556_positive_substrate_court.py
```

Two files changed; nothing else created or touched in production. Verified independently.

### 1.2 Adopted seam byte-unchanged — verified

```
git diff --stat 1be02e95 3a2dcafe0 -- rawlsing_next/m3_v556_higher_order_structural.py rawlsing_next/m2_v555_atomic_route.py   => empty
git diff --stat 87268ffaa 3a2dcafe0 -- <same two files>                                                                     => empty
```

The candidate's claim "the adopted M3 seam was not modified" is **byte/commit verified true**.

### 1.3 Blast radius — verified zero

A repository-wide search for importers of `pre553_v556_positive_substrate` outside the module itself and its own court returns **zero** hits. No production module, test, or consumer imports it. Zero-new-regression-ID is therefore guaranteed by construction, independently of any suite run.

### 1.4 The 35 + 29 + 28 = 92 surface — independently reproduced

| Suite | Candidate claim | Independently observed |
|---|---|---|
| `rawlsing_next/tests/test_pre553_v556_positive_substrate_court.py` | 35 | **35 passed** |
| `rawlsing_next/tests/test_m3_v556_higher_order_structural.py` | 29 | **29 passed** |
| `rawlsing_next/tests/test_m2_v555_atomic_route.py` | 28 | **28 passed** |
| combined | 92 | **92 passed** |

Arithmetic reconciles: the prior review measured the focused court at 17, and 35 − 17 = 18. Both untouched courts (29, 28) reproduce the prior review's numbers exactly.

### 1.5 The full-suite regression claim — cannot be independently reproduced here; structurally sound anyway

The candidate records base 227 failed / 2293 passed / 53 errors / 280 failure-error IDs and after 227 / 2311 / 53 / 280, with `passed_delta: 18`.

I attempted the full `rawlsing_next/tests` suite (163 test files) in my own venv and could **not** reproduce the baseline: `223 failed, 2263 passed, 59 errors, 28 subtests passed`, stable across two runs and across the candidate's `PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` flags. The candidate's declared environment (`LOCAL_COURTS/qualification/r7-c4-source-free-venv`) **does not exist in this checkout**, and my plugin set differs.

**I do not silently relabel this.** The absolute regression counts are **not independently certified by this review**. What I *did* certify is stronger for the specific claim at issue: the change set is two files, one of which is a test file, and **no other module imports the changed module**. A zero-new-ID outcome is a structural consequence, not an empirical coincidence. The baseline's internal arithmetic is also self-consistent (`passed_delta 18` = `2293→2311`; `17→35`).

## 2. The seven repairs — independently attacked

### R1 — Authoring validation: **CLOSED**

Independently confirmed by reading the code at the candidate tip and by hostile probes:

- `author_closed_result_schema` (`:432-452`) validates the root through `_validate_authored_schema_node`.
- `author_result_contract_binding` (`:543-594`) validates the schema, **recomputes** `schema_ref` via `_expected_schema_ref` and requires exact equality (`:574-578`), then calls `validate_result_contract_binding` on its own output (`:593`).
- `author_governed_rule` (`:651-663`) re-validates the embedded contract, checks the ref kind, checks the ref `content_hash` commits to the binding, and checks the binding names the same rule id/version.
- `V556RuleMaterialRegistry.build` (`:727-762`) re-validates the frozen family, the embedded contract, family agreement, contract-ref agreement, and recomputes `rule_content_hash`.

I verified the hash mirroring matches the seam **exactly**, not approximately: M3 `_result_contract` builds `material` with `"contract_id": M3_CONTRACT_ID` re-inserted and hashes it (`m3…:729-745`); the substrate's `validate_result_contract_binding` reconstructs `{"contract_id": M3_CONTRACT_ID, **rest}` and hashes that (`:536-540`). M3 `_rule_body_material` excludes the authority triple; the registry recomputation excludes exactly `rule_content_hash`, `authority_id`, `authority_version`, `authority_content_hash` (`:747-752`). Both match.

The five implementation-discovered defects are real and the fixes are correct. In particular, the `contract_id` omission (defect 1/2) would have refused every lawful binding; the `_EXPECTED_BINDING_FIELDS` set (`:493-499`) is indeed M3's exact 13-field set (`m3…:64-69`), and `contract_id` is correctly excluded from the binding but re-inserted for both hashes. Defect 4 is verified at source: `_topology_schema` now pins `allowed_kinds` to `V555_FAMILY` (`:877-878`), the real `m2_v555_atomic_route.SEMANTIC_FAMILY`. Defect 5 is verified: cardinality is checked at `:834-841` before field binding at `:843-854`.

**One residual gap (low):** `author_governed_rule` validates `binding_ref["kind"]` and `binding_ref["content_hash"]` but never `binding_ref["object_id"]` (`:655-659`). M3 does validate the reconstructed object_id (`m3…:746-751`), so this fails closed at the seam, not at authoring. It is a completeness gap against R1's own "validate everything at authoring" goal.

### R2 — Ontology / role gating: **PARTIAL — the commission's escape route is open**

This is the material finding. `UNBOUNDED` is a first-class, documented sentinel for a leaf with no enum constraint (`:297-308`, `:311-320`). The gate runs on **declared** values only — `_node_string` refuses blocked nouns in `allowed` (`:305-306`), `_node_exact_ref` refuses them in `kinds` (`:425-426`) — and `_validate_authored_schema_node` repeats that check (`:412-413`, `:425-426`). When the sentinel is used, **no layer anywhere checks the value**: M3's `_validate_payload_node` accepts any string when `allowed == "UNBOUNDED"` (`m3…:658-660`) and any kind when `kinds == "UNBOUNDED"` (`m3…:667-669`), and the payload is copied verbatim into the positive object (`m3…:931`).

Three reproductions, all `M3DecisionState.SUPPORTED`, all reaching `res.v556_object`:

| Probe | Declaration | Payload | Result |
|---|---|---|---|
| P1 | `_node_string("OBJECTIVE_STRUCTURAL_RELATION", "UNBOUNDED")` | `{"relation_kind": "DOMINATION"}` | **SUPPORTED**; object payload `{"relation_kind": "DOMINATION"}` |
| P2/Q3 | `_node_exact_ref("OBJECTIVE_REFERENCE", "UNBOUNDED")` | `endpoint_a_ref.kind = "HEGEMONY"` | **SUPPORTED**; object payload carries `kind: HEGEMONY` |
| P4 | `_node_string("OBJECTIVE_MEASUREMENT", "UNBOUNDED")` | `{"pressure_magnitude": "0.87"}` | **SUPPORTED**; numeric magnitude carried as a string |

The negative control confirms the gate works when the leaf is closed: declaring the same value as an enum (`_node_string(..., ("DOMINATION",))`) is refused with *"names blocked strong noun 'DOMINATION'"*. The gate is therefore **syntactic against the declaration, not semantic against the material**.

Two receipt claims are false at the machinery level as a result:

- `01_REPAIR_MATRIX.json` R2 *after*: *"string enum values and exact-ref kinds are refused on blocked strong nouns; numeric scalar leaves (number and integer) are refused outright"* — true only for closed leaves. An `UNBOUNDED` string leaf emits a blocked strong noun, and an `UNBOUNDED` string leaf emits a numeric magnitude.
- `02_VOCABULARY_AUTHORITY_RECEIPT.json` `numeric_ceiling.consequence`: *"no numeric pressure magnitude, scalar coupling value or aggregate strength can be authored through any positive path"* — **false**; the string path carries it (P4).
- `00_RETURN.md` R2: *"the whole semantic class is blocked rather than the two labels the review happened to probe"* — the token list is not whole-class (see P5 below).

### R2b — Actor-semantic role labels: **PARTIAL**

The token test (`_FORBIDDEN_PARTICIPANT_ROLE_TOKENS`, `:187-191`) is real and behavioural; the court's four labels are refused. But ten of twelve further actor-semantic candidates I probed were **accepted** as participant roles:

```
accepted: SELF_MODEL, IDENTITY_COMMITMENT, INNER_STATE, SUBJECTIVE_MEANING,
          WORLDVIEW, TEMPERAMENT, STRUCTURAL_SELF, HABITUS, DISPOSITION, ORIENTATION
```

`HABITUS`, `DISPOSITION`, `ORIENTATION`, `TEMPERAMENT`, `WORLDVIEW` and `SELF_MODEL` are squarely actor/person-semantic. The receipt's justification — *"a token test refuses the whole semantic class rather than only the two labels the review happened to probe, so a new actor-semantic label cannot be coined around a fixed enum"* — overstates what a 17-token **substring** list achieves. This is a bounded gap: the declared class is broader than the delivered list. (Note also that substring matching over-blocks: `"FIELD"` also refuses `FIELDWORK`.)

### R3 — Interaction semantics: **REASONING CLOSED; the valid-empty claim is falsifiable**

The reasoning is **correct and independently verified at source**. TD_R03 `RESULT.md:154` is the non-inference law verbatim; `:181` is the §6 verdict verbatim; gates `:509` (G14) and `:497` (G02) exist. `PERMITTED_RELATION_KINDS` in the prior tranche was exactly the three forbidden premises, so the load-bearing change really is an un-inversion, not a scalar removal. `AUTHORIZED_INTERACTION_RELATION_KINDS = ()` is right. `interaction_relation_canary_rule()` refusing rather than minting a replacement kind is right. `PERMITTED_INCIDENCE_KINDS` (`:221-224`) does not collide with the non-inference law.

**However**, "V556_INTERACTION_RELATION is returned lawfully VALID_EMPTY" is a statement about the **canary**, not the machinery. `SUPPORTED_FAMILIES` is `tuple(sorted(V556_SEMANTIC_FAMILIES))` (`:74`), so the registry gate accepts all three families, and the rule author accepts any frozen family (`:623-626`). Probe P7 authors a `V556_INTERACTION_RELATION` rule through the generic path with an `UNBOUNDED` array of `UNBOUNDED` strings, registers it (`GOVERNED_RULES_PRESENT`, `populated_families == ["V556_INTERACTION_RELATION"]`) and evaluates it `SUPPORTED` with payload `{"coexisting_relations": ["COEXISTING_STRUCTURAL_INCIDENCE", "PARALLEL_STRUCTURAL_OCCURRENCE"]}` — the literal TD_R03 §5 forbidden premise names inside a positive object. A `V556_ATTRACTOR_PREREQUISITE` rule is equally authorable, which would falsify the sibling claim that the attractor family "remains unfilled".

The candidate's own `limits` say this weakly (*"V556_INTERACTION_RELATION and V556_ATTRACTOR_PREREQUISITE both remain lawfully empty"*); they are empty **in the shipped registry only**. The court's `test_interaction_family_is_lawfully_valid_empty` and `test_attractor_family_remains_unfilled` assert against `source_free_canary_registry()` — instance material — which is exactly the class of assertion the prior review criticised.

### R4 — Topology truthfulness: **CLOSED**

- Truthful dyadic maximum: `TOPOLOGY_CANARY_MAX_CARDINALITY = 2` (`:861`) used at `:912`; `source_free_canary_registry()`/`topology_canary_rule()` declare 2, and M3 refuses a third participant (`m3…:397-400`). Independently reproduced by the candidate's own `test_truthful_cardinality_is_enforced_by_the_seam_not_only_by_us`, which I re-ran green.
- `shared_structural_channel_ref` is gone: verified by reading `_topology_schema` (`:870-884`); the fields are exactly `endpoint_a_ref`, `endpoint_b_ref`, `incidence_kind`.
- Labelling: `TOPOLOGY_CANARY_SHAPE_LABEL` (`:860`) and `TOPOLOGY_CANARY_F2_CLAIM` (`:865-867`) are explicit. `snapshot()` exposes them.
- Payload binding: `validate_payload_against_participants` (`:812-854`) binds payload route refs to the governed participants' identifiers and now checks cardinality **before** field binding (`:834-841` before `:843-854`).
- No hidden F2 attractor-grain claim: confirmed.

**Two low residuals.** (a) `TOPOLOGY_CANARY_SHAPE_LABEL` and `TOPOLOGY_CANARY_F2_CLAIM` live in `snapshot()` only; the **rule, schema and contract material do not carry them** (`_topology_schema` passes no label; `topology_canary_rule` sets none). A recipient of the material alone cannot see that it is illustrative. The receipt claims *"the material declares itself…"* (`03_…json`), which is true of the substrate snapshot, not of the emitted material. (b) `validate_payload_against_participants` is **not called anywhere in production** — no other module imports the substrate, and the seam performs no route-binding join. It is a court-exercised helper, and the enforcement it claims does not happen on the evaluation path.

### R5 — Registry / tranche ceilings: **CLOSED**

Family enforcement at `build` is real (`:737-739`), exercised by a genuine distinct-key test. `TRANCHE_LOCAL_ONE_RULE_PER_FAMILY` plus note (`:112-117`) is named data and surfaced in `snapshot()` (`:802-803`). `TRANCHE_LOCAL_ADMITTED_ROLE_NARROWING` (`:88-106`) names exactly what M3 also admits, with no architectural-ceiling claim. `OBJECTIVE_ACTOR_INDEXED` is withdrawn with a stated reason (`:119-127`, `:559-562`). I confirmed the withdrawal is coherent: `ADMITTED_OBJECTIVE_ROLES` (`:89-98`) excludes `OBJECTIVE_ACTOR_INDEX`, so the mode could never be satisfied (`m3…:727-728`).

**One low residual:** `ADMITTED_OBJECTIVE_SCHEMA_CLASSES` (`:209-215`) still admits `OBJECTIVE_ACTOR_POSITION` and `OBJECTIVE_ACTOR_OPPORTUNITY` while the role narrowing excludes `OBJECTIVE_POSITION`/`OBJECTIVE_OPPORTUNITY`, and nothing links schema class to semantic family — probe P6 authored a `V556_TOPOLOGY` rule carrying an `OBJECTIVE_MEASUREMENT` result schema class.

### R6 — Court repair: **SUBSTANTIALLY CLOSED; three witnesses still missing**

The prior review's specific vacuity defects are genuinely gone. I verified by reading all 565 lines: the no-op ternary at old line 205 is absent; `V556_ATTRACTOR_PREREQUISITE` is spelled correctly (test at `:265-269`); the duplicate-family test now builds two **distinct** rule keys and asserts they differ before asserting the family branch (`:326-346`); the misspelled-family lookup is gone. The prior review's "6 constant assertions" and "2 substring scans" are replaced by refusal assertions through the authoring path.

Three caveats, none of them fatal but all relevant to "prove, don't assert":

1. `test_blocked_nouns_are_quoted_from_adopted_law_not_invented` (`:240-243`) asserts that constant string literals appear in `BLOCKED_STRONG_NOUNS`. This is a **constant assertion**, the same class the prior review flagged, though it claims provenance rather than behaviour.
2. `test_numeric_scalar_leaf_is_refused` (`:228-237`) proves only that `number`/`integer` **node types** are refused. It does not and cannot catch the string-riding magnitude (P4). The numeric ceiling is therefore **asserted at the type level and unproven at the value level**.
3. `test_actor_semantic_participant_labels_are_refused` (`:196-202`) tests four labels. `SELF_MODEL`, `HABITUS`, `DISPOSITION`, `ORIENTATION`, `TEMPERAMENT`, `WORLDVIEW` are unprobed and accepted (P5).

**No test covers the commission's attack #2**: there is no witness for `UNBOUNDED` payload values, none for `UNBOUNDED` exact-ref kinds, and none for the generic-path authoring of `V556_INTERACTION_RELATION`/`V556_ATTRACTOR_PREREQUISITE`. The commission's §"mandatory attacks" #6 asks for "the specific vacuity defects from the prior review" to be rechecked; those are fixed, but the repaired court has a matching hole against the commission's own #2.

### R7 — Robustness: **CLOSED**

Deep freeze is real and observable: every in-place mutation I attempted on `rule.rule`, `rule.result_contract`, the nested schema fields and the nested refs failed (`TypeError` on mapping proxies, `AttributeError`/`TypeError` on tuples). `MULTIPLICITY_POLICIES` (`:130-133`) is enforced at `:645-649`. `_plain`/`_freeze` are exact inverses for the JSON-able material and hashing is performed on the plain form, so freeze/unfreeze cannot drift a hash.

**One low residual:** `GovernedRule.result_contract` is `result_contract.binding`, i.e. the already-frozen object authored by `author_result_contract_binding` (`:594`). A caller who hand-builds a `ResultContractBinding` from raw dicts and passes it to `author_governed_rule` gets `validate_result_contract_binding` run over it (`:654`) but `result_contract=result_contract.binding` stored **unfrozen** (`:710`). The registry re-validates (`:741`), so this fails closed; the immutability guarantee is weaker than "authored material is deep-frozen" implies for that construction path.

## 3. M3 preservation and the five implementation-discovered defects

M3/M2 byte-identity is verified (§1.2). All five defects are real; I verified each fix at source rather than accepting the narrative:

| # | Defect | Fix verified |
|---|---|---|
| 1 | binding validator required `contract_id`; M3's exact set excludes it | `_EXPECTED_BINDING_FIELDS` (`:493-499`) == M3 `_RESULT_CONTRACT_FIELDS` (`m3…:64-69`), 13 fields, no `contract_id`; `contract_id` re-inserted only for hashing (`:537`) |
| 2 | `rule_content_hash` recomputation omitted `contract_id` | registry `rule_body` re-inserts it (`:747`) and excludes exactly the authority triple + hash; matches M3 `_rule_body_material` |
| 3 | payload join preferred `content_hash`; natural key is `route_id`/`object_id` | `validate_payload_against_participants` accepts **either** identifier (`:826-833`, `:850-851`) |
| 4 | invented endpoint ref kind `V555_ROUTE_IDENTITY` | now `V555_FAMILY` (`:877-878`), the real `m2_v555_atomic_route.SEMANTIC_FAMILY` |
| 5 | derived unbound-field defect reported before structural cardinality | cardinality at `:834-841`, field binding at `:843-854` |

No substitute defects introduced by fixes 1–5. Fix 4's residual (a) labelling gap and fix 5's helper-only status are recorded in §2 R4.

## 4. Attack-by-attack answer

| # | Commission attack | Verdict |
|---|---|---|
| 1 | Authoring validation, schema_ref recomputation, embedded binding/rule validation, registry revalidation | **CLOSED**; one low residual (binding_ref `object_id` unchecked at authoring, caught at seam) |
| 2 | Ontology gating — actor labels, strong nouns, numeric leaves, **generic enum/exact-ref escape routes** | **OPEN** — declared-value gating is real; the `UNBOUNDED` escape delivers blocked strong nouns, arbitrary ref kinds and numeric magnitudes into positive objects (P1/P2/P4/Q3) |
| 3 | Interaction law — forbidden premises; `VALID_EMPTY` lawful not accidental | Reasoning and authority **correct**; `VALID_EMPTY` is a **canary-instance** claim, not a machinery ceiling — the family is authorable and positively evaluable through the generic path (P7) |
| 4 | Topology truthfulness — dyadic maximum, no UNBOUNDED lie, payload refs bound, no F2 claim | **CLOSED**; two low residuals (label not in emitted material; route-binding helper not on the evaluation path) |
| 5 | Registry/tranche ceilings — frozen families, tranche-local one-rule-per-family, `OBJECTIVE_ACTOR_INDEXED` | **CLOSED**; one low residual (actor-named schema classes admitted while their roles are excluded; no class↔family link) |
| 6 | Court authenticity — reach machinery, recheck prior vacuity defects | **SUBSTANTIALLY CLOSED**; prior defects genuinely fixed; three witnesses missing, incl. attack #2 and the string-riding magnitude |
| 7 | Robustness — multiplicity vocabulary, stale-hash/mutation resistance | **CLOSED**; one low residual (hand-built binding stored unfrozen, caught at registry) |
| 8 | No ontology smuggling — zero new ontology, no fabricated relation kind, no attractor population | **PARTIAL** — zero new families/states/kinds and no attractor population in the shipped registry; but the machinery still materializes forbidden ontology at value level (P1/P2/P4/P7) |
| 9 | M3 preservation byte/commit verified | **VERIFIED TRUE** |
| 10 | Qualification — reproduce 35+29+28=92 and regression zero-new-ID; distinguish reconstructed from governed | **92 reproduced exactly.** Full-suite baseline **not reproducible here** (env mismatch) — reported as reconstructed, not certified; structural guarantee (two files, zero importers, seam identical) supplied instead |

## 5. Bounded repair set

All repairs are documentary plus one narrow gate change. No architecture change, no new ontology, no seam change.

**Repair 1 (blocking, attack #2).** Close the `UNBOUNDED` value path. One of: (a) require every leaf to declare a closed enum / closed kind list, and refuse the `UNBOUNDED` sentinel in `_node_string`/`_node_exact_ref` outright; (b) keep `UNBOUNDED` only for leaves whose **values** are validated by a governed vocabulary at emission, and implement that validation in a path that actually runs before the positive object is assembled. Whichever is chosen, the same gate must run on **payload values**, not only on declared literals. Record explicitly that today the gate is syntactic against the declaration.

**Repair 2 (blocking, attack #3).** Make the interaction/attractor valid-empty claim machinery-true or restate it as instance-true. Either refuse `V556_INTERACTION_RELATION` and `V556_ATTRACTOR_PREREQUISITE` at the rule author and the registry until a governed interaction-rule registry exists (matching what `interaction_relation_canary_rule()` already refuses), or amend every claim to say "empty in the shipped registry only". As written, `03_TOPOLOGY_AND_INTERACTION_DISPOSITION.json` and `07_FINAL_DISPOSITION.json` assert a ceiling the generic path disproves.

**Repair 3 (blocking, attack #2).** Restate the two false receipt claims: `numeric_ceiling.consequence` ("no numeric … magnitude can be authored through any positive path") and R2's "the whole semantic class is blocked". Either make them true (Repair 1 + a widened role vocabulary) or qualify them to what the declared-value gate actually delivers.

**Repair 4 (required).** Extend the actor-semantic role refusal to the class the receipt claims, or narrow the claim. The ten accepted labels in P5 are the evidence.

**Repair 5 (required).** Add the missing court witnesses: `UNBOUNDED` string payload value carrying a blocked noun; `UNBOUNDED` exact-ref kind carrying a blocked noun; numeric magnitude riding a string leaf; generic-path authoring of `V556_INTERACTION_RELATION` and `V556_ATTRACTOR_PREREQUISITE`. Replace `test_blocked_nouns_are_quoted_from_adopted_law_not_invented`'s constant assertion with a behavioural one, or drop it and state that provenance is documented, not proven.

**Repair 6 (low).** Put `TOPOLOGY_CANARY_SHAPE_LABEL` and `TOPOLOGY_CANARY_F2_CLAIM` into the rule/schema/contract material (or a governed canary flag), not only into `snapshot()`; or restate `03_…json`'s "the material declares itself". Decide and document whether `validate_payload_against_participants` is load-bearing (then wire it into the evaluation path) or a court helper (then stop describing it as enforcement).

**Repair 7 (low).** Reconcile the role/class lists: `ADMITTED_OBJECTIVE_SCHEMA_CLASSES` admits `OBJECTIVE_ACTOR_POSITION`/`OBJECTIVE_ACTOR_OPPORTUNITY` while the role narrowing excludes their roles. Add the `binding_ref["object_id"]` check at `:655-659`, and freeze the binding on the hand-built `ResultContractBinding` path.

## 6. What is genuinely achieved (do not discard)

- The load-bearing change is correct and is verified against TD_R03 at source: the inverted non-inference law is un-inverted, and no replacement relation kind was fabricated.
- Authoring-time refusal now genuinely covers the binding author, the rule author and the registry build, with hash mirroring that matches the seam exactly. The prior review's F1/F2 are closed for **closed** leaves.
- The false `UNBOUNDED` topology maximum is corrected to a truthful dyadic 2, and the seam refuses a third participant.
- The mandatory shared-channel field is gone; the shape is labelled illustrative with an explicit no-F2-claim label, and no F2 grain is materialized.
- The tranche-local narrowings and the one-rule-per-family restriction are named data with correct "not a timeless ceiling" notes.
- `OBJECTIVE_ACTOR_INDEXED` is withdrawn rather than left as a dead accepted mode.
- Material is deep-frozen; multiplicity is a frozen two-value vocabulary.
- The positive core survives: `SUPPORTED` through the unmodified seam with stable replay (independently re-run green).
- The adopted M3/M2 seam is byte-identical, and the change has zero importers and therefore zero blast radius.
- Five genuine implementation-discovered defects were caught and correctly fixed, including two that would have refused every lawful binding.

## 7. Bound on this review

No raw survey files, no locator discovery, no warrant, no live C4, no C7, no actor/person implementation, no attractor population, no new V556 semantics, no implementation edits, no self-adoption. All probes were read-only imports of the candidate module from a checkout at the exact candidate SHA; probe scripts were written outside the repository. I modified no implementation file. The only artifacts are these six return files: `00_REVIEW.md` plus the five JSON artifacts required by the commission.

## 8. Answer to the commission, plainly

`accept_and_adopt = false`.
`smallest_blocking_repair = Repairs 1 + 3` (the `UNBOUNDED` value path and the two false claims it makes true-or-false), with Repair 2 for the interaction-valid-empty ceiling and Repairs 4–5 to make the court and the vocabulary match their own receipts.
`architecture_conflict = false`. `authority_overreach = false`. `seam_modified = false`. `missing_exact_evidence = false` for the candidate itself; the full-suite regression baseline is **not independently certified in this environment** and is reported as reconstructed.
