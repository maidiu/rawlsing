# PYAT R32 GF1H — pair consumer integrity repair

**Disposition:** `REPAIR_EXECUTED_SOURCEFREE_TEST_ONLY__GF1J_INDEPENDENT_REVIEW_REQUIRED`. This is a versioned consumer candidate, not an adopted generic owner, source issuer, Field Forge port, or actor permission. The original GF1E artifact at `eeb726357204653b22458dc267dd70ba0009bd77` remains unchanged.

## Custody and execution

Sealed startup and assigned branch base: `70265e59dab9d190e736010f6afdeebe1729b396`. Exact GF1E consumer Git blob `75670c69dc587233d462e4a636b63e7fd233c0bd`, SHA-256 `06dd484b0e9b4b2c9fb0a1583453ac7ffa8c052135304eaaee167a34127cb402`. The repaired `gf1_pair_support_consumer.py` SHA-256 is recorded in `04_REAL_SOURCE_IMPORTS_AND_COLD.json`; the reproducer verifies that its staged imported `__file__` has those bytes. The unchanged GF1G Phase-A test and oracle, original44, GF1F100, and GF1I19 test sources were checked against exact Git blobs; see the same receipt.

Run `python3 reproduce.py` from this return. It creates a fresh disposable stage from pinned Git objects, executes the original consumer, seats only this versioned consumer into the disposable court, runs every suite, launches two fresh cold processes, verifies source identities, and writes JUnit/log receipts to `02_FROZEN44_GF1F100_GF1I19_AND_NEW_JUNIT/`. No original SAV/DTA, original35, paid model, signed issuer, or production actor is used.

| Unchanged court | Original GF1E | Repaired GF1H | Interpretation |
|---|---:|---:|---|
| Original frozen44 | 44/44 | **44/44** | genuine 2×2, reverse role and native pipeline retained |
| GF1G preregistered 26 | 17/26 | **26/26** | nine independent REDs repaired without editing expectations |
| GF1F historical 100 | 100/100 | **96/100** | four old expectations encode the superseded risk-class/valid-empty semantics; REDs preserved |
| GF1I historical 19 | not rerun here | **17/19** | two pre-consumer “module absent” expectations correctly remain RED |
| GF1H new hostile 26 | N/A | **26/26** | strict counts, conservation, typed states, roles, forged self-hash |

`01_BEFORE_AFTER_INDEPENDENT_26.json` lists every failed case and the actual JUnit totals. In the final fresh-stage run, the GF1G original exited 1 (9 failures), repaired exited 0, original44 exited 0 both times, GF1F original exited 0 and repaired exited 1 (4 failures), GF1I exited 1 (2 historical failures), and new adversarial tests exited 0. Failing exits were expected and are preserved in raw logs/JUnit; they were not rewritten into green checks.

## Repair applied

1. Requires each condition denominator to equal the sum of its two target counts, preserving the true native risk grain.
2. Refuses joint support above eligible joint risk; requires exact nonnegative `int` for eligible/excluded risk, per-condition denominators, and all cell supports. Bool, float, string, negative, malformed 2×2 roles/order, and inconsistent zero/positive cell states return `CONSUMER_RELATION_INTEGRITY_REJECTED` with no downstream value or class.
3. Checks producer blocking and `typed_state` before empty-profile handling. Missing, unresolved, and nonresponse return a typed blocking refusal; typed `ZERO_SUPPORT` carries `UNDETERMINED_ZERO_SUPPORT_RISK` but no value. A nonblocking SUPPORTED empty profile still returns `RESPONSE_INPUTS_VALID_EMPTY`.
4. Distinguishes no eligible risk from eligible risk with no supported observations. The former returns `UNDETERMINED_NO_ELIGIBLE_RISK`; the latter `UNDETERMINED_ZERO_SUPPORT_RISK`. One absent conditioner level with positive support remains no eligible risk at that level. Genuine original44 still passes.
5. Keeps computed support vectors, role order, result hash, separate reverse grant, F2 noncopy, and `production_owner_commit=False`. A self-rehashed forged provenance remains TEST_ONLY because this schema has no independent issuer signature.

Two cold OS processes imported the repaired file from the staged court, had distinct PIDs and the same consumer SHA, genuine relation hash, result hash, role order and class. The genuine baseline result hash remained unchanged. `04_REAL_SOURCE_IMPORTS_AND_COLD.json` contains the receipt; `03_TYPED_STATE_AND_SCIENTIFIC_ERROR_CONSERVATION.md` gives the exact semantic mapping and historical conflicts.

**Ceiling:** source-free computed-consumer candidate only. No signed producer/issuer, original35, Field Forge S1–S9, OC05, N11/N12/V3, canonical semantic change, or HQ acceptance. GF1J must independently rerun and adjudicate the four GF1F historical conflicts before any scoped acceptance.
