# 04 — C1 consumer grain and adapter boundary

**Status:** `PARTIAL__C1_CHAIN_NOT_READABLE_IN_GOVERNED_LINEAGE`
**Commission:** PYAT-HQ203-HD-MATURE-WORLD-F8-SERVICE-CONTRACT-R1
**Control tip examined:** `3760ba31761cd6e27e978c31749161feced1a47a`

---

## 1. The grain premise the commission asks H-D to respect

The commission states HQ168's accepted grain as:

> scalar positioned-subject provider **is narrower than** broader C1 analytical composition

and requires H-D to determine "what is already consumable, what needs only a bounded adapter, and what would need a new semantic authority."

That premise cannot be discharged on this Mac, for a reason that is itself a finding.

## 2. Material inventory conflict

The commission lists as "at minimum inspect":

- `rawlsing_next/pre553_analytical_composition.py`
- `rawlsing_next/pre553_empirical_possibility_provider.py`
- `rawlsing_next/pre553_analytical_state_and_route.py`

**None of the three exists at any examined tip.**

| module | added | last touched | at commission HEAD `de129fea` | at base `15018a30` | at audit `b3ea471a` | at control `3760ba31` |
|---|---|---|---|---|---|---|
| `pre553_analytical_composition.py` | `c1d18480e0` (2026-09-29) | `bc661188b5` (2026-09-30) | absent | absent | absent | absent |
| `pre553_empirical_possibility_provider.py` | `e3bcbbb4fa` (2026-09-30) | `e3bcbbb4fa` | absent | absent | absent | absent |
| `pre553_analytical_state_and_route.py` | `a3c07426b0` (2026-09-30) | `4f5555459e` (2026-10-01) | absent | absent | absent | absent |

`rawlsing_next/` carries 307 files at both the control tip and the commission HEAD — identical counts, so this is not a partial listing.

**These modules were never deleted.** Every commit in their path history is an `A` or `M`. They survive on side branches (`agent/deepseek-pyat-hq140-…`, `agent/opencode-pyat-hq146-…`, `agent/rabochii-pyat-hq197-r1`, `agent/astra-pyat-hq168-omega1-production-readiness-r1`, and ~20 others), none of which is an ancestor of the governed lineage.

**Consequence:** the broader C1 analytical composition is *historical functional capital on side branches*, not adopted current capability readable at the governed tip. The scalar source-local exact-lookup path in `source_backed_positioned_subject_possibility.py` is the **only** current F8 producer.

This also puts pressure on several terminal-audit claims, which assert a C1/N10E consumer chain that is not present at the audit's own tip:

- MATRIX C03/C04/C05/C09/C10 — "C1-02 conjunctive producer", "C1-02 multi-target geometry", "C1-02 joint target producer"
- MATRIX C18 — "C1 producer and consumer accepted; N10E scalar adapter narrower"
- REPORT §236 — "Its base ontology/model and accepted producer/consumer chain are sufficiently constituted at their declared grain."

**No mutation was performed to resolve this.** Absence was established by exact tree listing and ancestry queries only. Importing side-branch history into the governed terrain would be a re-commission decision, not a worker decision.

## 3. What is actually consumable at the governed tip

Working only from what is present, the current F8 consumer boundary is:

```
exact source-local empirical fact
  → ConditionerBinding (requires POSITIVE comparability_authority_ref)
  → PositionedSubjectPossibilityQuery (single source_universe + single release;
        purpose must be EMPIRICAL_POSSIBILITY_ONLY)
  → PossibilitySliceEvidence selected by EXACT
        (source_universe, release, target, retained_conditioner_ids)
  → governed strictly-decreasing specificity walkback, same source/release only
  → PositionedSubjectPossibilityResult
```

Algorithm: `EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION`.

## 4. Already consumable / needs bounded adapter / needs new authority

| world input | verdict | reason |
|---|---|---|
| exact source-local empirical fact as conditioner | **already consumable** | full binding contract exists and is enforced; only the per-scope positive instance is missing |
| typed uncertainty / noncomparability | **already consumable** | six evidence states, six result states; nothing to build |
| currentness selection | **already consumable** | lifecycle states + fail-closed |
| structural position/role as conditioner | **needs a bounded adapter** | requires an exact comparator; OBL031 is adopted for exactly one field at `TYPE_AND_VALUE_ONLY` grain. Each further field needs its own mapping + evidence, not new form |
| branches / configurations / minority outcomes | **needs a bounded adapter** | C07/C10 forms closed; a branch predicate + validation authority must be instantiated per scope |
| higher-order (multi-arity) targets | **needs a bounded adapter** | the query admits multiple conditioner bindings structurally, but the joint/multi-target producer is the absent C1-02. A bounded adapter can populate exact-arity targets; general arity coverage is not proved |
| cross-source composition | **needs a new semantic authority** | `cross_source_proxy = FORBIDDEN_IN_V1` is frozen in the model rule. Not an adapter question |
| service-specific source selection | **needs a new semantic authority** | no adopted successor licenses selection; current code only validates. This is H-C's lane — recorded, not answered |
| temporal products as conditioners | **needs a new semantic authority** | no current positive temporal producer. H-A's lane — recorded, not answered |
| pressure/counterpressure as conditioners | **unresolved** | H-B's lane. H-D declines to name a new object |

## 5. The grain claim, restated honestly

The commission's framing — scalar provider is narrower than C1 composition — **cannot be confirmed or denied** from the governed lineage, because the broader side is not in it.

What *can* be stated from current evidence:

- The scalar provider's grain is exact: one source universe, one release, exact conditioner-set match, no smoothing.
- It is therefore **strictly narrower** than any broader composition chain by construction, whatever that chain contains.
- Whether the broader chain's products are **needed** at the terminal F8 seam, and whether an adapter suffices, is undetermined pending HQ adjudication of the inventory conflict.

This is recorded as a dependency in `07_CONDITIONAL_DEPENDENCY_MAP.json` under `H-D-INTRINSIC`, not resolved.

## 6. Adapter boundary rule

An adapter is sufficient for an input **only if** all of the following hold:

1. the required authority **form** already exists in the governed lineage;
2. the adapter introduces no new semantic operation — it binds existing refs and selects existing evidence;
3. the resulting claim stays at or below the input's `ClaimCeiling`;
4. no probability, coefficient or confidence renormalization occurs;
5. no cross-source/universe/release bridge is introduced;
6. the actor firewall is structurally preserved (`purpose == EMPIRICAL_POSSIBILITY_ONLY`).

Where any of 1–6 fails, the requirement is a **new semantic authority**, not an adapter.