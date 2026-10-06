# PYAT HQ223 — N10E EXACT-DETERMINANT LIFECYCLE REPAIR — R1 RETURN

**DISPOSITION:** `N10E_EXACT_DETERMINANT_LIFECYCLE_REPAIR_COMPLETE__READY_FOR_FINAL_REREVIEW`
**AGENT:** bounded replay/dependency implementation worker
**BRANCH:** `agent/rabochii-pyat-hq223-n10e-exact-determinant-lifecycle-repair-r1`
**EXACT STARTUP TIP:** `988325dd9f65b70765eba7053057536a4b3fda84`
**PRIOR HOSTILE REVIEW:** `agent/reviewer-pyat-hq222-...-r1 @ bdf025b3a412560db17224813a822ad64e283229`
**RAW SOURCE ACCESS:** FORBIDDEN — NOT USED
**LIVE C4 / C7:** FORBIDDEN — NOT USED
**SELF-ADOPTION:** NOT PERFORMED

---

## 1. Bottom line

HQ222's blocking defect is **real and confirmed**. `build_graph()` serialised
`determinant_exact_refs` and then ignored them: it emitted zero edges for the query,
predicate, consumer-query and witness determinants. Only the model authority was a
lifecycle root, so AT19 was demonstrated for one determinant class.

It is now **closed for every consumed determinant that current owner law can actually
root**. The graph emits *reachable* two-hop edges, and it **refuses** to claim coverage
for determinants no authority owns rather than emitting a decorative edge.

**Exactly one production file was mutated** — `pre553_analytical_replay_dependency.py`,
the file the commission permitted. No authority kind was created, no `ExactRef` was
promoted to an `AuthorityRef`, no ownership was inferred from a ref name, and
`pre553_authority_maintenance.py` was not touched.

I did **not** close AT19 by appending orphan `determinant -> product` edges. That is
precisely what the commission forbade, and it would have been worse than the defect.

---

## 2. The repair

```
GOVERNED CHANGE ROOT (sealed authority revision)
  -> owner->determinant      authority_edge   (new)
  -> determinant->product    dependency_edge  (new)
  -> N10E analytical product
```

`SemanticDeterminantGraph.affected()` is seeded only by governed changed *authority*
refs. So a `determinant -> product` edge alone is unreachable by construction. The
repair therefore emits **both** edges, and roots each determinant **only** from an
authority recorded on the determinant itself.

New in the bounded adapter:

| Addition | Purpose |
|---|---|
| `ExactDeterminantOwnership` | records how a consumed determinant can lawfully reach invalidation |
| `…Registration.determinant_ownerships` | carries that classification |
| `build_graph()` | emits `owner→determinant` + `determinant→product` |
| `assert_lifecycle_coverage_is_owned()` | fail-closed anti-decorative-edge guard |
| `UnownedDeterminantRefused` | typed error for a falsely-claimed covered determinant |
| `build_owner_recompiler(determinant_recompose=…)` | second hop, so an affected determinant is recompiled, not skipped |
| `_product_consumed_authorities()` | a product reached *transitively* resolves its successor from that determinant's recorded owner |
| `build_graph(omit_dependency_edges=…)` | lets the orphan-edge hostile cut `determinant→product` specifically |

---

## 3. Required determinant census — every class classified

Ownership was read **only from recorded fields**. No name, kind or position inference.

| Class | Recorded owner field | Classification | Governed change root staged? |
|---|---|---|---|
| `empirical_query.ref` | `authority_snapshot_refs[0]` | AUTHORITY_ROOTED | **yes — proved** |
| `predicate.ref` | `authority_snapshot_refs[0]` | AUTHORITY_ROOTED | **yes — proved** |
| `model_rule.model_authority_ref` | `model_authority_ref` | AUTHORITY_ROOTED | yes (HQ221 lineage) |
| `source_universe.ref` | `authority_snapshot_refs[0]` | AUTHORITY_ROOTED | stageable, census-only |
| `consumer_query.ref` | `binding.comparability_authority_ref` | AUTHORITY_ROOTED | **no — unstaged, see §5** |
| `conditioner_binding_witness.ref` | `witness.pairing_authority_ref` | AUTHORITY_ROOTED | **no — unstaged, see §5** |
| `release_refs[0]` | **none** | **UNOWNED → blocker** | no |
| `consumer_query.target_ref` | **none** | IMMUTABLE_IDENTITY | n/a |
| `…empirical_coordinate_ref` | **none** | IMMUTABLE_IDENTITY | n/a |
| provider/consumer contract ids | module constants | IMMUTABLE_IDENTITY | n/a |

**No invalidation witness was manufactured for an immutable or unowned class.** For
`QUESTION_NATIVE` targets the reasoning is recorded: a content-addressed coordinate
identity cannot change in place — a different ref is a different question invocation,
not a lifecycle transition of this product.

---

## 4. AT19 proven *beyond* model authority

The new discriminating witness: a governed **v1→v2 revision of the `PREDICATE_GRAMMAR`
query authority**, minted through the accepted owner's own
`candidate → APPROVED → seal → promote_current` ceremony.

The owner reported **three** affected dependents — the query ref, the predicate ref and
the N10E product — and each received a **new exact ref from real recomposition** through
the accepted producer:

- query ref genuinely re-identifies (`52934ea8…` ≠ `ebef7e84…`)
- product identity genuinely moves, reaching `EXACT_SUPPORTED_SLICE_PRODUCED` /
  `EXACT_SUPPORTED` with denominator **60** preserved — no refusal, no invented geometry

Required conditions, all discharged:

- all and only products that consumed D are affected
- a **non-consumer** product is unaffected *despite being resident and known* — object
  presence never manufactures an edge
- deleting `owner→determinant` makes the product unreachable **while the orphan
  `determinant→product` edge remains present** — this is the exact decorative-edge case
  HQ223 forbade, now demonstrated rather than assumed
- deleting `determinant→product` also severs the product while the determinant stays rooted
- cache/object presence does not restore a noncurrent product

---

## 5. Two honest limits I did not paper over

**(a) Comparability-owned classes are rooted but unstaged.**
`C1-AT07-COMPARABILITY` genuinely owns the consumer query and the witness through recorded
fields, and `build_graph()` emits a real root edge — `affected()` provably reaches the
product. But the installed fixture entry is **not a full `AuthoritySnapshot`**: it carries
no `authority_kind`, `scope_envelope`, `governed_object_families` or `replay_protocol_ref`,
and no entry in `AUTHORITY_KINDS` names comparability. Staging a ceremony would require
inventing authority content, which the commission forbids. `test_r11` asserts the
*absence* rather than manufacturing one.

**(b) The release ref is an exact blocker.**
`C11LogicalRelease` is content-addressed repository identity. No authority owns it; it
cannot be coerced to `AuthorityRef`. No governed authority-maintenance transition can seed
it. Named, not invented.

---

## 6. HQ222 defect-002 — stated, not faked

The accepted owner law, read from `_recompile`:

> `affected dependent recompilation must produce a new exact ref; an unchanged ref does not prove absence of a lawful replacement`

This fires **categorically, before any semantic-equivalence adjudication**. Therefore an
affected dependent whose *actual* recomputation lawfully yields the **same** exact
identity has **no lawful representation** in the current analytical lifecycle owner.

I did not fake this branch. An identity-returning lambda is used **only to obtain and
record the owner's refusal**, never as a substitute for recomputation, and the court
asserts the law against the owner's own source rather than merely reporting it.

**This does not make the AT18/AT19 grade false**: for every lifecycle-relevant class
proved here, a governed revision genuinely re-identifies the product.

---

## 7. Documentary corrections — all three applied

| # | Defect found by HQ222 | Correction | Observed at runtime |
|---|---|---|---|
| 1 | runner emitted the *provider* path under `producer_path` | emits `producer_path` = composition, `provider_path` = N10E seam, as distinct callables | composition `…compose_positioned_subject_possibility`; provider `…provide_empirical_possibility_slice` |
| 2 | packet recorded both `fresh_process_exit: 0` and `fresh_process_exit_code: 1` | one single **measured** integer; the court asserts non-zero and never reports an unobserved code | **exit 1**, marker present |
| 3 | H12 claimed an "observed AssertionError" for a test that catches nothing | H12 restated as a **positive** assertion of owner currentness; no exception is caught or claimed | no runtime exception; evidence is the owner-derived replacement ref |

---

## 8. Regression

Full `rawlsing_next/tests` collection run **twice** — with and without this repair:

- baseline: **54** failures/errors
- with repair: **54** failures/errors
- `diff`: **IDENTICAL**

**Zero regression.** The 54 are pre-existing at the startup tip, outside this lane's
terrain, and were neither fixed nor masked.

**Court result: `188 passed`** (45 N10E court + 143 dependent/owner/provider courts).

---

## 9. Return artifacts

All under `WORKER_RETURNS/PYAT-HQ223-N10E-EXACT-DETERMINANT-LIFECYCLE-REPAIR-R1/`:

- `00_RETURN.md`
- `01_CONSUMED_DETERMINANT_OWNER_CENSUS.json`
- `02_REACHABLE_DEPENDENCY_GRAPH_REPAIR.json`
- `03_AT19_SELECTIVE_INVALIDATION_COURT.json`
- `04_FRESH_RECOMPUTATION_AND_DOCUMENTARY_CORRECTIONS.json`
- `05_FINAL_DISPOSITION.json`

---

## 10. Recommended next step

Final rereview. The sharpest attacks available against this lane:

- Can the `AUTHORITY_ROOTED` classification of `consumer_query.ref` / witness be
  contested? It rests on `comparability_authority_ref` / `pairing_authority_ref` being
  genuine recorded ownership, not on name inference.
- Is the non-consumer witness in `test_r04` weaker than a real direction-scoped sibling?
  The fixture's query authority is **not** direction-scoped, so forward and reverse share
  one identity — I did not manufacture a false discrimination, but HQ may want a
  direction-scoped authority fixture before claiming more.
- Should `source_universe.ref` be registered as a consumed determinant? It has a
  stageable root but the provider request contract does not consume it, so it is
  census-only here.
- The three named blockers in §5 and §6 need owner decisions HQ has not made.

`HQ223_N10E_EXACT_DETERMINANT_LIFECYCLE_REPAIR_RETURNED__READY_FOR_FINAL_REREVIEW`