# PYAT HQ280 PV3 A04SR — Independent A04S v2 oracle, provenance/issuer and consumer hostile

**TERMINAL:** `HQ280_PV3_A04SR_V2_INDEPENDENT_SOURCEFREE_RUNTIME_AND_PROVENANCE_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`
**GRADES (kept separate, as required):**
- `TECHNICAL`: **narrow acceptance** — v2 is a real, self-consistent, better-modelled contract
- `INDEPENDENT_EXPECTATION_PROVENANCE`: **FAIL / NOT PROVEN**
- `REAL_CONSUMER`: **MODELLED_NOT_EXECUTED**
- `SOURCE_ISSUER`: **NOT ESTABLISHED**

**Branch:** `agent/reviewer-pyat-hq280-pv3-a04sr-v2-issuer-oracle-hostile-r1` @ `37c486099fd9aee36fbc33c8a64cd00e10c594bb`
**A04S v2:** `56574bec2176df7fc95d4b877dfab79469de9c03` — module blob `08bb75c431d3352cb0d17e9a65f7d855b4d35e59` (verified)
**A04 root:** `cbe047cf15a2285b0e918bd77640037f7bec63ef` · **A05:** `9491d0296c95ee2942fe80eadc6aa9f54b07c634` · **my A04R finding:** `fca056a3e8497a3acd6c6de597c269e3000df875`
**Authority:** HQD-2026-10-10-280 · canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f` · PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (unmutated). **Review only — no A04S/A04/A05/owner/canonical edits.**

## 1. Runtime (real)

| suite | result |
|---|---|
| A04S v2 26 tests | **26 passed**, exit 0 |
| A04 original 41 tests | **41 passed**, exit 0 |
| my interop/provenance probe | exit 0, results in `repro/a04sr_probe_results.json` |

## 2. THE CENTRAL QUESTION — answered

> Does A04S truly close A04R's interoperability defect, or merely move the incompatibility into a translation layer?

**IT MOVES IT.** `v2_to_a05_universe()`'s own docstring says *"This is a **TRANSLATION, not derivation**"*, and the code confirms it:

```python
E.append({
    "expected_work_key": d.expected_work_key,        # <-- v2 key COPIED VERBATIM
    "operation_key":      d.semantic_operation_key,  # <-- v2 semantic key, not an A05 key
    ...
})
...
return {"schema": V2_SCHEMA_VERSION, ...}            # <-- "HQ280_PV3_A04S_CANONICAL_V2@1.0.0"
```

The record is **A05-shaped** but carries **v2 keys under a v2 schema**. A05's `verify()` compares submitted job keys against keys **A05 computes itself** from `{item_k, op_k, authority, risk, topology, version}`. v2's key preimage is different, so a translated universe **cannot** equal A05's own key set: the outer join fails, and making it pass would require rewriting the oracle's keys — **precisely the coercion my A04R report forbade**.

**Verdict: `NOT_CLOSED__INCOMPATIBILITY_MOVED_INTO_A_TRANSLATION_LAYER`.**
**Honest resolution remains:** `SCHEMA_VERSIONED_SUCCESSOR_WITH_A_VERIFIED_PREIMAGE_MAPPING` — each v2 semantic key must be paired with an A05-scope key by an explicit, verified, **injective** mapping, not by copying one into the other's slot.

## 3. What v2 genuinely improves (credited)

v2 is not a regression. It **does** carry the two identities A05 could not express — `measure_kind` (RAW vs GOVERNED_WEIGHTED) and `condition_order` (`q(C|A)` vs `q(C|A,B)`) — inside its own semantic key preimage. That is real progress over A05 and it is the right modelling direction.

**But the improvement stops at v2's own boundary.** Because the only bridge to A05 is a shape-preserving copy, the two richer identities are **still lost at the join**: an A05 consumer of a translated universe sees neither.

## 4. Semantic→dispatch mapping is non-injective

`SEMANTIC_TO_DISPATCH` collapses **three** semantic operations onto one dispatch class `I03_UNARY_OR_JOINT_QUERY` (3→1), and the probe records `fail_closed_on_multiple: false`. A dispatch job therefore **cannot recover which semantic operation it came from**. The commission explicitly requires failing closed when multiple operations map to one job; current behaviour does not.

## 5. Issuer and custodian — `INDEPENDENT_EXPECTATION_PROVENANCE: FAIL`

`V2IssuerRecord.issuer_signature` is, per its own comment, a **SHA-256 over the issuer's declaration preimage** — i.e. a hash the candidate controls. `custodian_timestamp` is a **literal asserted string** (`2026-10-11T00:00:00Z` per the commission's observation).

**A preimage hash proves integrity, not principal. An asserted timestamp proves nothing about time.** Neither constitutes independently authenticated authorship or ordering. Concretely:

| attack | structurally detectable? |
|---|---|
| post-result forged issuer record | **No** — recomputing the same preimage yields the same hash |
| same-hash cloned custodian receipt | **No** — identical bytes hash identically |
| timestamp backdating / rewriting | **No** — the value is caller-supplied and unanchored |
| rewritten full expected frontier | **No** — a consistent rewrite is self-consistent |
| late-added operation | **Only** if an independent pre-run frozen set exists to compare against — it does not |

**What could prove write-once pre-execution sealing:** an **independent custodian** holding the expected set before execution, publishing an authenticated (signed) commitment to a preimage it controlled, with a time source the candidate cannot set — and ideally a transparency/append-only log. **Structural hash consistency must never be reported as competent external signature or custody.** No fake key issuance is proposed.

## 6. Consumer — `REAL_CONSUMER: MODELLED_NOT_EXECUTED`

A04S reports the consumer as **modelled**. I confirm: **no real consumer was executed**, and I do **not** mark it consumed. A **synthetic receipt produced by the same candidate cannot satisfy a consumer obligation** — the consumer set must remain an **independent obligation set** keyed by `(expected_work_key, consumer)`. The pre-existing C1 / Field Forge / learned target first consumer is the owner to bind; the exact runnable prerequisites for a separately issued **B02** are listed in `04_…`.

## 7. Hostile coverage actually performed vs held

**Performed:** interop translation inspection and key-preimage comparison; semantic→dispatch injectivity; issuer/custodian provenance analysis; run of all three suites.
**Held / not exhaustively exercised (recorded UNKNOWN, not PASS):** post-result forged-issuer *execution* (no independent custodian exists to forge against), timestamp backdating execution, restored-frontier rewriting, A+B-vs-A-only and missing-J2 through the v2 layer, equal-count substitution, restart reorder, zero-denominator/coverage-limited nulls through the v2 layer. These require a **pre-run sealed custodian** to be meaningful; absent one, adversarial execution would only prove self-consistency, which is the point being denied.

**Terminal:** `HQ280_PV3_A04SR_V2_INDEPENDENT_SOURCEFREE_RUNTIME_AND_PROVENANCE_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`.
