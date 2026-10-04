# PYAT HQ205 — V556 positive substrate independent hostile review — R1

**Role:** independent hostile source-free reviewer
**Branch:** `agent/reviewer-pyat-hq205-v556-r1`
**Startup (commissioned) SHA:** `560f2394df3a65fed4dc115f64348b64415f2174`
**Commission base:** `0e8d5bcd98e5aba63cd7312f778dedbfe8b6b646`
**Candidate under review:** `87268ffaa60ebd9119aa46dc3f664e12d632b4d5`
**H-B authority basis:** `d691f9bad35232ccff4692ee811a8f0a5514835c`
**H-E terminal basis:** `15e28d61ec929891559884609b59ede30ac2ee64`
**HQ204 adjudication:** `ff4f06954824a3a5699bc5c1c9bd68cb3c5b4146`
**HQ205 adjudication:** `0e8d5bcd98e5aba63cd7312f778dedbfe8b6b646` (`PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ205_HQ204_PARTIAL_FANIN_AND_REVIEW_WAVE_R1.md`)

**Disposition:** `V556_SUBSTRATE_PARTIAL__ONTOLOGY_SMUGGLING_REPAIR_REQUIRED`
**Terminal:** `HQ205_V556_POSITIVE_SUBSTRATE_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

No implementation file was modified. No self-adoption. No source data read.

---

## 0. Answer to the commission in one paragraph

The substrate's **positive core is real and sound**: two governed source-free canary rules
commit to exact `M3ResultContractBinding@2.0.0` material with closed
`OBJECTIVE_STRUCTURAL_RESULT` schemas, and both evaluate to `M3DecisionState.SUPPORTED`
through the **unmodified** adopted M3 seam (`m3_v556_higher_order_structural.py`,
blob `9a4b26b2…` identical to control). The family ceiling (property A) holds. The canaries
contain no scalar, no person-state schema role, no actor indexing, and
`V556_ATTRACTOR_PREREQUISITE` is left unfilled (property G) — but for the shipped registry
only. **However, the substrate's own claim that it "materializes adopted semantics only and
will not introduce a family/noun/scalar" is true of the two canary *instances* and false of
the *machinery*.** The generic authoring path will author, register and positively evaluate
material whose ontology is neither adopted nor authorized, including person-state schema
roles, actor-desire participant labels, `DOMINATION`/`HEGEMONY`/`CAPITAL` relation kinds and
numeric scalar leaves — and in two of those cases the shipped court's own claimed properties
(11, 12) are demonstrated false at the machinery level. Refusal happens at the M3 evaluator
(starting `05` below), not at authoring time as the commission's property E requires.

---

## 1. What was run (exact)

Courts re-run in a detached worktree at the candidate SHA, CPython 3.12.14 / pytest 9.1.1:

| suite | observed |
|---|---|
| `rawlsing_next/tests/test_pre553_v556_positive_substrate_court.py` | **17 passed** |
| `rawlsing_next/tests/test_m3_v556_higher_order_structural.py` | **29 passed** |
| `rawlsing_next/tests/test_m2_v555_atomic_route.py` | **28 passed** |
| combined, run 1 | **74 passed** |
| combined, run 2 | **74 passed** |

Candidate's reported numbers reproduce exactly. Adversarial probes (read-only imports of the
candidate module; scripts outside the repository; hashes in `07_COURT_RECEIPT.json`) are the
evidential basis for §2.

---

## 2. Findings

### F1 — CRITICAL: authoring-time refusal does not cover the binding/rule/registry path

`author_closed_result_schema` (`pre553_v556_positive_substrate.py:273`) does validate the
root node. `author_result_contract_binding` (`:311`) does **not** validate the supplied
`schema` at all and does **not** verify that `schema_ref` resolves to that schema;
`author_governed_rule` (`:364`) does **not** validate `result_contract`; and
`V556RuleMaterialRegistry.build` (`:465`) validates only duplicate rule keys and duplicate
families.

Probe P1: an **open** schema (`additional_fields: True`) carrying a **person-state** role
(`SUBJECTIVE_BELIEF_IDEOLOGY`) and a `schema_ref` whose `content_hash` is unrelated to the
schema is accepted by `author_result_contract_binding`, accepted by `author_governed_rule`,
and registered: `registered_rule_count=1`, `state=GOVERNED_RULES_PRESENT`. Evaluation later
returns `INTEGRITY_FAILURE` (probe P13) — it fails closed at the seam, which is good, but the
commission's property E requires refusal **before positive material becomes registrable**.

The candidate's own return and `02_COURT_RESULTS.json` claim this was "fixed at source"
("fail-closed validation was added at authoring time"). The fix covers only
`author_closed_result_schema`. The court's single authoring-refusal test
(`test_schema_authoring_refuses_person_state_role`, court test 13) exercises only that
function, so it cannot see this.

### F2 — CRITICAL: the machinery will materialize unadopted and forbidden ontology

`author_governed_rule` constrains `participant_roles` only to be non-empty and
duplicate-free (`:385-387`). It constrains enum **values**, primitive types and role labels
nowhere. `author_closed_result_schema` accepts any string enum and any `integer`/`number`
leaf on an admitted objective role.

* **P2** — rule with `participant_roles=("ACTOR_DESIRE","ACTOR_BELIEF")` is registered and
  evaluates `SUPPORTED`; the positive V556 object's `participant_bindings` carry
  `role: ACTOR_DESIRE`, `role: ACTOR_BELIEF`.
* **P19** — rule built on a schema whose enum is
  `("DOMINATION","HEGEMONY","CAPITAL","PRESSURE_COUPLING")` is registered and evaluates
  `SUPPORTED`; the positive object's payload is `{"relation_kind": "DOMINATION"}` with
  `semantic_family = V556_INTERACTION_RELATION`.
* **P9** — `author_closed_result_schema` accepts a `number` leaf literally named
  `pressure_magnitude` under `OBJECTIVE_MEASUREMENT`.
* **P3** — `actor_indexing_mode="OBJECTIVE_ACTOR_INDEXED"` is accepted by
  `author_result_contract_binding`, but `ADMITTED_OBJECTIVE_ROLES` (`:60-69`) excludes
  `OBJECTIVE_ACTOR_INDEX`, so **no** binding this module can author can ever satisfy the M3
  requirement (`m3…:727-728`): a guaranteed `INTEGRITY_FAILURE` (fails closed, but the
  parameter is dead and undocumented as such).

`01_OWNER_AUTHORITY_MATRIX.json` lists "actor desire", "actor belief", "hegemony",
"capital", "scalar pressure magnitude" under `explicitly_not_authored`. That is true of the
two canary instances; the generic surface does author them.

### F3 — HIGH: the interaction relation-kind vocabulary canonizes premises that adopted V556 architecture forbids

The repository carries the V556 architecture of record at the candidate SHA
(`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/recalibration/TD_R03_V556/RESULT.md`,
blob `8af3016963e24bd5d439b78948592c93c30167b0`, byte-identical to control `06f306d8`), whose
§5 states:

> "No F1 may be created solely because routes coexist, have opposite signs/directions, share
> source/target/mediator/stratum, overlap in geography/time, derive from the same V554
> affordance, have similar labels, or appear together in runtime context. These may be
> candidate premises a future rule examines; they are never the rule itself."

and §21 gate **G14**: "no F1 inferred from coexistence/sign/common source/target/stratum/geography/time".

`PERMITTED_RELATION_KINDS` (`:73-77`) is exactly
`COEXISTING_STRUCTURAL_INCIDENCE`, `SHARED_UPSTREAM_STRUCTURAL_CHANNEL`,
`PARALLEL_STRUCTURAL_OCCURRENCE`, and the interaction canary's payload key is
`coexisting_relations` (min 2). The three governed relation kinds map 1:1 onto TD-R03's
forbidden premises (coexistence; shared mediator/channel; appearing together). TD-R03 §6/G13
also requires rule-bound `participant_cardinality_kind` (DYADIC or genuinely NARY) and
direction/symmetry semantics; neither is authored. This is the strongest form of the
commission's section B/C worry: it is not a *scalar* coupling that was smuggled, it is a
**non-inference law that was inverted** in the only authored relation vocabulary.

Mitigating and material: H-B itself recommends the *shape* — `03_POSITIVE_INSTANCE_AND_AUTHORITY_GAPS.json`
requires "a coexisting-relation array of min_items >= 2", and `07_FINAL_DISPOSITION.json`
recommends exactly that and "endpoint, route-identity and incidence fields" for
V556_TOPOLOGY. The *shapes* are H-B-authorized; only the **enum values** are minted here, and
they are the part that collides with TD-R03.

### F4 — HIGH: the topology canary privileges one topology and declares a false maximum

`_topology_schema` (`:521-535`) requires all four of `endpoint_a_ref`, `endpoint_b_ref`,
**`shared_structural_channel_ref`** and `incidence_kind`. The topology rule is `ORDERED`
with a two-role pattern (`:577`), so M3 (`m3…:441-449`) admits exactly two participants.

* **P6b** — a three-participant (path/generic) topology request returns
  `INVALID_PARTICIPANT_SET` even though the rule declares
  `maximum_cardinality_or_unbounded_marker="UNBOUNDED"` (`:579`). The declared maximum is
  false metadata: no cardinality other than 2 is realizable.
* **P6c** — a topology without `shared_structural_channel_ref` returns
  `RESULT_SCHEMA_NONCONFORMING`. The one shared-channel dyad is structurally mandatory, so
  this is **not** a generic machinery canary. H-B did authorize "route-identity" among the
  fields, which is where the shared channel comes from; the finding is that the canary is
  dyadic-and-channel-specific **and** mislabels itself UNBOUNDED, and that TD-R03's adopted
  topology grain (F2 = attractor-prerequisite motif over 1..n route refs plus 0..n F1 refs,
  §8) is not what is materialized.

Note the interaction canary has the same declared-UNBOUNDED/realized-dyadic inconsistency.

### F5 — MEDIUM: the frozen-family ceiling is not enforced at the registry

`author_governed_rule` refuses a non-frozen `semantic_family` (`:380-384`) and M3 re-checks
it (`m3…:279-280`), so property A holds at the two real gates. But
`V556RuleMaterialRegistry.build` does not check the family at all: **P4** registers a
hand-built `GovernedRule` with `semantic_family="V556_INVENTED_FAMILY"`, and
`populated_families` then reports `['V556_INVENTED_FAMILY']`. Fails closed at evaluation;
the registry is nonetheless an unguarded publication surface.

### F6 — MEDIUM: undocumented tranche ceiling narrower than adopted semantics

`ADMITTED_OBJECTIVE_ROLES` drops `OBJECTIVE_ACTOR_INDEX`, `OBJECTIVE_POSITION` and
`OBJECTIVE_OPPORTUNITY`, all of which the adopted M3 contract admits and whose
`OBJECTIVE_ACTOR_INDEXED` path the existing 29-test court proves `SUPPORTED`
(`rawlsing_next/tests/test_m3_v556_higher_order_structural.py:475-490`). Combined with **P3**,
the substrate accepts an `OBJECTIVE_ACTOR_INDEXED` parameter it can never satisfy. The
narrowing is a defensible tranche-local choice, but it is **not documented anywhere** — the
docstring's "no actor …" list is about person-state semantics, which is a different thing
(M3 line 9: "objective actor identifiers are not person-state"). Property D's "represented or
documented as such" is only half met.

### F7 — MEDIUM: one-rule-per-family is lawful but is not proven by the court

**P5** — a *second distinct* rule for the same family raises
`SubstrateAuthoringError("at most one governed rule per semantic family in this tranche")`.
**P14** — M3 with two distinct same-family rules both active still evaluates `SUPPORTED`, so
the restriction is registry-local and not an M3 or architectural ceiling. The
tranche-locality is stated only inside the exception string ("in this tranche"); it appears
in no constant, docstring or snapshot field, but it is also not exported as timeless law.
**The court's proof is invalid**: `test_canary_material_carries_no_real_world_authority_claim`
(court test 17, `:440-441`) registers `[topology_canary_rule(), topology_canary_rule()]` —
two *identical* rules — which trips the **duplicate-key** branch (**P5b**), not the family
branch. The advertised property is therefore not exercised by any test.

### F8 — MEDIUM: VALID_EMPTY is lawful at the substrate, but the adopted distinction is lost at the seam

`VALID_EMPTY_NO_GOVERNED_RULE` (`:45`) is not invented: TD-R03 §12 requires
"`VALID_EMPTY_NO_GOVERNED_RULE`" to be distinguished from integrity/build failure. The empty
registry is lawful, and **P7b** confirms evaluation against it yields no positive object and
no absence inference. But the seam result is `UNKNOWN_AUTHORITY` (**P7b**), the same state M3
uses for malformed or unavailable authority — so the adopted "no rule authorizes" vs
"authority/build failure" distinction is **not carried through** the only evaluation path.
The no-demand path correctly yields `behavior='ZERO_V556_OBJECTS'` (**P7c**). The empty
registry's `unfilled_families` naming is registry-scoped and does not assert world absence.

### F9 — LOW: material is not frozen

`MappingProxyType` is imported (`:28`) and never used. `GovernedRule.rule` /
`result_contract` are live dicts inside a frozen dataclass; a deep mutation after authoring
is registered and the stale hashes are only caught by M3 (**P16c** `INTEGRITY_FAILURE`).
Fails closed; the intended immutability was not delivered.

### F10 — LOW: no frozen multiplicity vocabulary

`multiplicity_policy` is only `_text`-checked (`:416`; M3 likewise `:271`). **P11** authors
`multiplicity_policy="WHATEVER_I_LIKE"` successfully.

---

## 3. Property-by-property verdict against the commission

| # | Commission property | Verdict |
|---|---|---|
| A | semantic-family ceiling | **HOLDS at `author_governed_rule` and M3**; not at the registry (F5) |
| B | topology canary generic / no privileged topology | **FAILS** — one mandatory shared-channel dyad, false UNBOUNDED max (F4) |
| C | interaction canary: ≥2 relations, no scalar/winner/dominance/strength | **PARTLY** — no scalar/winner/strength anywhere (clean); the authored relation kinds invert TD-R03's non-inference law (F3) |
| D | one-rule-per-family tranche-local, not a ceiling | **LAWFUL** (P5/P14), but undocumented in material and unproven by the court (F7) |
| E | authoring-time refusal before registrability | **FAILS** — F1, F2 |
| F | VALID_EMPTY lawful, emits nothing, infers nothing | **HOLDS at the substrate**; seam distinction lost (F8) |
| G | ATTRACTOR_PREREQUISITE supported but unfilled, no hidden default | **HOLDS** for the shipped registry (P8b); the generic surface will author it on explicit request (P8a), no default path |
| H | 17 + 29 + 28 courts prove the properties | **Numbers reproduce (74/74 twice)**; several properties are asserted as constants rather than proven, and two claimed proofs are demonstrably false (F7, §4) |

---

## 4. Do the courts prove, or assert?

Of 17 tests: 6 are constant assertions on material the same tranche authored (tests 1, 2,
3, 5, 6, 17), 2 are substring/structural scans of the canaries only (12, 14), 1 contains a
tautological no-op assertion (test 4, `:205`:
`x.v556_object["semantic_family"] if "semantic_family" in x.v556_object else True`), 1
asserts a **misspelled** family name (test 16, `:416`, `"V556_ATTRACTOR_PREREQUISATE"` —
vacuously `None`), and 1 exercises the wrong registry branch (test 17, F7). The remaining
tests are genuine behavioural proofs (tamper refusal, closed-vocabulary refusal, cardinality
floor, negatives, VALID_EMPTY, replay equality) and are the real evidential value of the
court.

The "13 commissioned properties" are **self-authored**: neither the HQ204 commission
(3 lines), `01_SCOPE.md`, the HQ204 adjudication `ff4f0695`, the HQ205 adjudication
`0e8d5bcd`, H-B `d691f9ba` nor H-E `15e28d61` enumerates 13 properties. The only 13-item list
is the candidate's own `02_COURT_RESULTS.json`, mapped 1:1 onto 13 of its own tests. That is
a self-referential proof structure, not a commissioned denominator.

---

## 5. What is genuinely achieved (do not discard)

* Two governed rules with exact authority/id/version and `rule_content_hash` committing to
  the exact R2 rule/result-binding material; tamper produces non-`SUPPORTED` (court test 7).
* Closed `OBJECTIVE_STRUCTURAL_RESULT` schemas (`additional_fields` always `False`,
  `:160,162`), enforced again by M3; enum values outside the schema and undeclared extra
  fields are refused (court test 8).
* Two positive `SUPPORTED` V556 objects through the unmodified M3 seam; stable replay
  (`x == y`, matching `replay_key_hash`; court test 15).
* No scalar, no winner, no aggregate strength, no person-state schema role and no actor
  indexing in either canary; binding carries `person_state_semantics="FORBIDDEN"` and
  `actor_indexing_mode="NO_ACTOR_INDEX"`.
* `V556_ATTRACTOR_PREREQUISITE` absent from the shipped registry and present in
  `unfilled_families` (**P18**); authoring an invented family is refused (court test 16).
* `VALID_EMPTY` typed outcome emits no positive object (court test 11, **P7b**).
* The authoring path and the M3 seam fail closed on every hostile construction attempted
  (open schema, person-state role, actor-indexed mode, mutated material, invented family).

---

## 6. Required repairs (bounded, no architecture change)

**R1 (E, F1)** Extend authoring-time validation to `author_result_contract_binding` (validate
`schema` with the same node validator, recompute `schema_ref` and require equality) and to
`author_governed_rule`/`V556RuleMaterialRegistry.build` (re-validate the embedded contract, or
refuse any contract produced outside the validated constructor). Unlawful material must not
reach `GOVERNED_RULES_PRESENT`.

**R2 (E, F2)** Constrain `participant_roles` at authoring against a declared vocabulary (or
explicitly document that role labels are caller-owned and remove the "no actor desire/belief"
promise from the owner matrix). Add a machinery-level refusal for person-state/actor-semantic
role labels if the promise is kept.

**R3 (B/C, F3)** Replace or re-scope the relation-kind vocabulary so that no governed kind is
one of TD-R03 §5/G14's forbidden premises (coexistence, shared channel/mediator, parallel
occurrence). If H-B's coexistence array is retained, its elements' `relation_kind` must be a
governed relation (e.g. the TD-R03 §5 list: flow continuation, reroute, buffering,
amplification, blockage, competition/counter-pressure, contradiction, reinforcement) and
must carry a cardinality/direction/symmetry declaration.

**R4 (B, F4)** Make the topology canary's declared maximum truthful (dyadic) or generalise it;
if it stays a single illustrative topology, say so in the material (rule/schema id or a
canary flag) rather than presenting it as a generic V556_TOPOLOGY instance. Reconcile against
TD-R03 §8's F2 grain (route refs + F1 refs).

**R5 (D, F5, F6)** Enforce the family set in `V556RuleMaterialRegistry.build`; document the
`ADMITTED_OBJECTIVE_ROLES` narrowing explicitly as tranche-local (and either support or
remove `OBJECTIVE_ACTOR_INDEXED`); record the one-rule-per-family restriction as named
data, not only as an exception string.

**R6 (E, H)** Repair the court: exercise the family branch of the registry restriction, use
the correct `V556_ATTRACTOR_PREREQUISITE` spelling, remove the tautology at test 4 line 205,
and add behavioural tests for the machinery-level refusals (open schema, person-state role,
actor-semantic role labels, strong-noun enum, numeric leaf, `OBJECTIVE_ACTOR_INDEXED`) so
properties 11 and 12 are proven of the machinery and not only of the canaries.

**R7 (low, F9, F10)** Either use `MappingProxyType` / immutable copies or drop the import;
freeze `multiplicity_policy` to a named enum.

---

## 7. Bound on this review

No source data, no live C4, no C7, no actor/person implementation, no attractor population
authorized or performed. Synthetic canaries authorize no real-world structural claim. The
reviewer modified no implementation file; the only artifacts are these nine return files.
