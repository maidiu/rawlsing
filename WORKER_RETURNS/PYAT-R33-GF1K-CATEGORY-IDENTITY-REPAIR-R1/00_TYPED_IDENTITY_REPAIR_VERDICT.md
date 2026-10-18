# PYAT R33 GF1K — exact native category identity repair

**Verdict: `GF1K_EXACT_NATIVE_CATEGORY_IDENTITY_REPAIR_COMPLETE__GF1J_TWO_REDS_CLOSED__REQUIRES_INDEPENDENT_GF1L`**

Role: bounded sourcefree GF1H consumer author/repairer. **NOT** HQ, **NOT** an
independent I2 court, **NOT** a source / Field Forge / N11 / V3 issuer.

- Repository `maidiu/rawlsing` (private).
- Branch `agent/userdirect-pyat-20261017-r33-gf1k-exact-native-category-identity-repair-r1`.
- Sealed launch SHA **`d2169b3db2e364506a606adec2b6b7c508497307`**
  (branch tip == commission commit; direct remote verified).
- Write terrain: `WORKER_RETURNS/PYAT-R33-GF1K-CATEGORY-IDENTITY-REPAIR-R1/` only.

## 1. The defect, stated exactly

GF1H's `_decode_profile` coerced source-native domain values and nested row/cell
state values to `str()`. A category whose native declared value is the **string**
`"0"` was therefore accepted when a fully rehashed semantic relation supplied an
**integer** `0` at `condition_state` or `target_state` — and both computed as
`EXACT_PAIR_SEPARATION`. Python's `False == 0` folded in the same way.

That is a scientific exact-identity violation: two distinct native categories
collapsed into one, and a spoofed category was answered as if it were genuine.

## 2. The repair

`REPAIR_VERSION = GF1K_EXACT_NATIVE_CATEGORY_IDENTITY@1`, minimal and strictly
additive over GF1H.

```python
def _same_native(a, b) -> bool:
    return type(a) is type(b) and a == b
```

Applied to the declared conditioner/target domains and to every row
`condition_state` / cell `target_state`. No `str()` coercion, no bool/int
folding, no auto-normalisation. A spoofed row or target category is refused with
`CONSUMER_RELATION_INTEGRITY_REJECTED` — `separation_class = None`,
`downstream_value_produced = False` — **before** any total, class, result hash or
value is computed. No consumer product exists to be re-used.

Any legitimate cross-type conversion would require a separately qualified
source-owner mapping. **This module performs none and authorises none.**

## 3. The two GF1J REDs: before → after

| Case | Against GF1H | Against GF1K |
|---|---|---|
| `test_gf1j_red1_conditioner_integer_spoofed` | **RED** | **PASS** |
| `test_gf1j_red2_target_integer_spoofed` | **RED** | **PASS** |

Same test file in both phases; only the seated consumer changes. Full evidence in
`01_GF1J_TWO_REDS_BEFORE_AFTER.json`.

## 4. Everything reproduced, with the frozen truth preserved

I re-ran the complete staged closure myself rather than accepting recorded
tallies. Every court matched its expected exit.

| Court | Tests | Pass | RED | Expected |
|---|---:|---:|---:|---|
| original44 | 44 | **44** | 0 | must be green |
| GF1G26 | 26 | **26** | 0 | must be green |
| GF1H26 | 26 | **26** | 0 | must be green |
| GF1K native identity | 12 | **12** | 0 | must be green |
| GF1J two REDs — before | 2 | 0 | **2** | must reproduce |
| GF1J two REDs — after | 2 | **2** | 0 | must close |
| GF1F100 | 100 | 96 | **4** | **stays NOT GREEN** |
| GF1I19 | 19 | 17 | **2** | **stays NOT GREEN** |

GF1F's 4 and GF1I's 2 stale cases were left untouched — not regraded, not
re-baselined, not xfailed. They remain visible as failures.

**Cold:** two independent processes, distinct PIDs (34944, 34961), identical
`consumer_sha256`, `relation_hash`, `result_hash`, `FORWARD_NATIVE_ORDER`,
`EXACT_PAIR_SEPARATION`, and `production_owner_commit = false` in both.

## 5. Custody

- True native **74-module** producer closure re-attested from its own pinned
  `commit:source_path` bytes: **74/74** on Git blob SHA-1 **and** sha256, zero
  unresolvable. Read, never mutated.
- Pre-repair consumer identity **`66658149fd7362e17c064a3fc1f9029d638f9ed9`**
  (blob) / **`a4915b845853e70f9430190aebde298346ea5ad4472de8380e26182113f97c8a`**
  (sha256) — **exactly the GF1H pin named in the commission**, so the reproduced
  baseline is the genuine GF1H artifact and not a substitute.
- Repaired consumer **`bbbda32facce…`** / **`06bf4ea9e71b084b…`**.
- No frozen test mutated. No accepted owner mutated. No production file touched.

## 6. What this does NOT establish

Passing source-free consumer tests do **not** establish population-calibrated
scenario probabilities, any adopted ADP015/020 change, genuine conception/birth
semantics, or actual V3 person generation. `GENERIC_NATIVE_SEMANTICS_HOLD` is
retained; the candidate remains `SOURCEFREE_GENERIC_PAIR_CANDIDATE_TEST_ONLY`,
UNISSUED and NOT ACCEPTED. No original35, Field Forge, N11/N12, OC05, V3 or
actor/wake grant. `production_owner_commit = false`.

Full statement in `04_SCIENTIFIC_CONSERVATION_AND_ISSUER_HOLDS.md`.

## 7. Deliberate limitation left open

The repair answers the **negative** half of cross-type category identity — a
consumer must never cast. It does **not** answer the positive half: whether a
source-owned typed-domain mapping should exist for genuine cross-instrument
category identity, and who owns it. That is left for GF1L rather than resolved by
convenience.

## 8. Next edge

**Independent GF1L review is required.** This is an implementer repair, not an
independent adjudication, and it does not self-adopt. HQ retains the final
scientific and critical-path judgment.

---

**Deliverables:** [01 two REDs before/after](01_GF1J_TWO_REDS_BEFORE_AFTER.json) ·
[02 native modules and SHA](02_NATIVE_MODULES_IMPORT_AND_SHA.json) ·
[03 JUnit + cold](03_REAL_FROZEN_COURTS_JUNIT_COLD/) ·
[04 conservation and issuer holds](04_SCIENTIFIC_CONSERVATION_AND_ISSUER_HOLDS.md) ·
`gf1_pair_support_consumer.py` (candidate) + `before/` (pinned GF1H) +
`reproduce.py`, `test_gf1k_native_identity.py`, `test_gf1h_adversarial.py`,
`test_gf1j_exact_native_identity_red_isolated.py`, `cold_child.py`.