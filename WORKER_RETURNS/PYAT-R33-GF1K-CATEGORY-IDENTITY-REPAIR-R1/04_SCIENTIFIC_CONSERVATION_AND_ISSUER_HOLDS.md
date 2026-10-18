# 04 — Scientific conservation and issuer holds

## 1. What the repair changes, and what it deliberately does not

The repair is **one function**: `_decode_profile` in the test-only GF1H consumer,
plus two small helpers. `REPAIR_VERSION = GF1K_EXACT_NATIVE_CATEGORY_IDENTITY@1`.
Nothing else in the module moves, and no accepted owner, frozen test or producer
file is touched.

**Changed (the defect):** source-native domain values and nested row/cell state
values were coerced with `str()`.

```python
condition_order = [str(c) for c in relation.conditioner_domain]   # was
condition_order = list(relation.conditioner_domain)               # now
str(row.get("condition_state")) != expected_c                     # was
not _same_native(row.get("condition_state"), expected_c)           # now
```

with `_same_native(a, b) = type(a) is type(b) and a == b`.

**Consequence:** a category whose native declared value is the string `"0"` is no
longer satisfied by an integer `0` supplied at `condition_state`/`target_state`,
and `bool` no longer folds into `int` (`type(False) is bool` is not `type(0) is
int`). Both sides must now be the same declared native type and equal in value.

**Not changed:** every arithmetic, risk, denominator and typed-state repair GF1H
introduced. Those are asserted independently and still green (below).

## 2. Conservation verified, court by court

| Court | Result | What it protects |
|---|---|---|
| original44 | **44/44** | GF1 original expectations, untouched |
| GF1G26 | **26/26** | GF1G preregistered oracle, untouched |
| GF1H26 | **26/26** | GF1H arithmetic/risk/denominator/typed-state repairs |
| GF1K native identity | **12/12** | the new exact-identity hostiles |
| GF1J two REDs before | **0/2 (RED)** | defect reproduced against the pinned GF1H consumer |
| GF1J two REDs after | **2/2** | defect closed |
| GF1F100 | **96/100 (4 red)** | historical, **NOT GREEN and unchanged** |
| GF1I19 | **17/19 (2 red)** | historical, **NOT GREEN and unchanged** |

GF1F and GF1I were left exactly as they were found. They were **not** regraded,
re-baselined or xfailed; their stale cases stay visible as failures.

Within GF1H26 the conservation invariants are individually named and passing:

- exact non-negative counts with typed refusal for `-1`, `True`, `False`, `1.0`
  (bool/float coercion refused at the count boundary);
- `denominator_mismatch`, `support_exceeds_risk`, `positive_zero_state`,
  `zero_positive_state`, `duplicate_target`, `foreign_role`;
- blocking typed states (`MISSING_TARGET_STATE`, `UNRESOLVED_TARGET_STATE`,
  `NONRESPONSE`, `ZERO_SUPPORT`) never laundered into valid-empty;
- no-eligible vs eligible-zero-supported kept distinct — **genuine zero is not
  manufactured from absence**;
- `test_reverse_role_requires_separate_grant_and_is_noncopy` — reverse requires a
  separate grant and does not copy the forward object;
- `test_self_rehashed_forged_source_stays_test_only` — **no signer claim**.

## 3. Rejection happens before any science is computed

`compute_pair_support_signature` calls `_decode_profile` before any total,
class, result hash or downstream value is produced. A spoofed row or target
category therefore returns

```
decision_state      = CONSUMER_RELATION_INTEGRITY_REJECTED
separation_class    = None
downstream_value_produced = False
```

and no consumer product exists to be re-used downstream. The two GF1J hostiles
assert exactly this triple.

## 4. Cross-type conversion is not a consumer convenience

The repair admits **no** implicit cross-type mapping. The commission requires
that any legitimate cross-type conversion come from a **separately qualified
source-owner mapping**, never from consumer casting. This module performs none,
and therefore authorises none. If a real source ever declares a domain whose
native values differ in type across an instrument/wave boundary, that mapping
must be issued by the source owner before it can be consumed here. This return
does not create, suggest or pre-approve such a mapping.

## 5. What passing these tests does NOT establish

Source-free consumer correctness is not any of the following, and none is claimed:

- population-calibrated scenario probabilities;
- any adopted ADP015 / ADP020 change;
- genuine conception, birth or CHILD_GENERATED semantics;
- actual V3 person generation;
- Field Forge generic semantic issuance (`GENERIC_NATIVE_SEMANTICS_HOLD` retained);
- original source rights, OC05, N11/N12 or actor/wake grants;
- a signer or production-owner commitment (`production_owner_commit = false` in
  both cold processes).

The whole repair remains `SOURCEFREE_GENERIC_PAIR_CANDIDATE_TEST_ONLY`,
UNISSUED and NOT ACCEPTED.

## 6. Authority holds carried forward, unchanged

| Hold | State |
|---|---|
| `GENERIC_NATIVE_SEMANTICS_HOLD` | **OPEN** — no Field Forge generic issue |
| Original source / U / E_pre rights | **NOT SOUGHT, NOT USED** |
| OC05 / N11 / N12 | **NOT HELD** |
| V3 person generation | **NOT HELD** |
| Actor / wake grant | **NONE** |
| Production / signer authority | **NONE** — `production_owner_commit=false` |
| HQ self-adoption | **NONE** — HQ retains the final judgment |

## 7. Scope and custody

- Write terrain: `WORKER_RETURNS/PYAT-R33-GF1K-CATEGORY-IDENTITY-REPAIR-R1/` only.
- The true native 74-module producer closure was **read and re-attested**, never
  mutated: **74/74** match on both Git blob SHA-1 and sha256, re-derived from
  each entry's own pinned `commit:source_path` bytes
  (`02_NATIVE_MODULES_IMPORT_AND_SHA.json`).
- The pre-repair consumer's identity is **`66658149fd7362e17c064a3fc1f9029d638f9ed9`**
  Git blob / **`a4915b845853e70f9430190aebde298346ea5ad4472de8380e26182113f97c8a`**
  sha256 — exactly the GF1H pin named in the commission, confirming the
  reproduced baseline is the genuine GF1H artifact.
- No frozen test was mutated. Both before and after phases run the **same** test
  file; only the seated consumer changes.

## 8. Remaining open question for GF1L

The repair is deliberately narrow. One question is left open on purpose rather
than answered by convenience:

> Should a source-owned typed domain mapping exist for genuine cross-instrument
> category identity, and if so who owns it?

This return answers the *negative* half — a consumer must never cast — and does
not attempt the positive half. An independent GF1L review should decide whether
the absence of any conversion path is sufficient, or whether a missing
source-owner mapping is itself a latent HOLD.
