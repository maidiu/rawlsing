# PYAT HQ280 PV3 A04R — Independent A04→A05 binder/oracle hostile court

**TERMINAL:** `HQ280_PV3_A04R_INDEPENDENT_BINDER_ORACLE_OWNER_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`
**VERDICT:** `TECHNICAL_ACCEPTANCE_WITH_EXACT_DEFECT__A04_AND_A05_ARE_NOT_KEY_INTEROPERABLE`
**Branch:** `agent/reviewer-pyat-hq280-pv3-a04r-binder-oracle-hostile-r1` @ `4f3238aff7644ad58406c623c9eac6682f1a0743`
**A04 candidate:** `cbe047cf15a2285b0e918bd77640037f7bec63ef` · module blob `7d8b3902c3f8f257637b7c07ad9feb5e096d48e5`, test blob `6c06a5b013d3713af7d7ba9bf143c3ef7a6245a2` — **both verified exact** in the review worktree.
**A05 oracle:** `agent/rabochii-pyat-hq280-pv3-a05-independent-nodrop-oracle-r1 @ 9491d0296c95ee2942fe80eadc6aa9f54b07c634`, `a05_oracle.py` sha256 `81c74691d576b89a5569efcffd929ef8c995c6261362bad243d235ded8fe96d4`, `a05_hostiles.py` sha256 `68ba6926dc0f5c8049c0e5052fb016e4979e973a958170e02d1571f8f389bad5`.
**Authority:** HQD-2026-10-10-280 · canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f` · PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (unmutated). **No A04 code edited; A05 bytes fetched separately and not merged.**

## 1. Actual runs (real runtime, not simulated)

| run | command | result |
|---|---|---|
| A04 candidate suite | `pytest rawlsing_next/tests/test_pre553_original_workload_binder_candidate.py -q` | **41 passed**, exit 0 (matches the commission's 41) |
| A05 independent fixtures | `python3 a05_hostiles.py` in a **separate temp dir** `/tmp/a04r/a05` | **18/18, `all_expectations_met: true`**, exit 0 |
| A04↔A05 compatibility probe | `python3 a04r_compat_and_hostiles.py` | exit 0, **14 checks recorded** |

Python 3.11.3, pytest 9.1.1, macOS 13.7.8 x86_64.

## 2. THE DECISIVE FINDING — the shared schema token is a trap

A04 exports `A05_COMPATIBLE_SCHEMA_VERSION = "HQ280_PV3_A05_EXPECTED_WORK@1.0.0"`, **byte-identical** to A05's `SCHEMA_VERSION`. A naive reviewer would read that as interoperability. It is not:

| check | finding |
|---|---|
| **C1** version strings | **EQUAL** (`HQ280_PV3_A05_EXPECTED_WORK@1.0.0`) — and that equality proves nothing |
| **C0** `op_class` vocabulary | **DISJOINT DOMAINS.** A04: `{I03_UNARY_OR_JOINT_QUERY, I05_BOUNDED_DISCOVERY}` (dispatch/route classes). A05: `{UNARY_DISTRIBUTION, PAIR_RESPONSE_COTRAVEL, NONSCALAR_TOPOLOGY_PRESERVATION}` (semantic classes). No shared token. |
| **C2** `operation_key` for identical semantics | **DIFFERENT.** A04 preimage `{kind,op_class,roles,target,condition_order,measure_kind,version}` vs A05 `{k,class,roles,target}` |
| **C3** `RAW` vs `GOVERNED_WEIGHTED` | A04 **distinguishes**; **A05 cannot represent the distinction at all** (no `measure_kind` parameter) |
| **C4** `q(C\|A)` vs `q(C\|A,B)` | A04 **distinguishes**; **A05 cannot** (no `condition_order` parameter) |
| **C5** `documentary_item_key` | **DIFFERENT** preimages |
| **C6** `expected_work_key` | **NOT INTEROPERABLE.** A04 folds `consumer` into the key; A05 declares the required consumer per expected record instead |

**Honest resolution: `SCHEMA_VERSIONED_SUCCESSOR_REQUIRED`.** Semantic-equivalent keys across A04 and A05 must be reconciled by an explicit versioned successor mapping — **not** by string coercion, key collision acceptance, or re-hashing A05 keys into A04's broader preimage. Any adapter that reports "A05-compatible" on the strength of the version string is **false interoperability**.

**Second finding:** because A05 cannot express `measure_kind` or `condition_order`, an A04→A05 handoff would **silently lose** the RAW/GOVERNED_WEIGHTED distinction and the `q(C|A)` vs `q(C|A,B)` distinction. Those are precisely the collisions the commission asked me to test, and they collide **downward** in A05.

## 3. What is genuinely positive (credited)

- A04's candidate is a **real, self-consistent implementation**: 41/41 of its own tests pass, its module/test blobs match the commission exactly, and it does distinguish the operation classes A05 cannot.
- A04's **outer reconciliation** design (keeping absent mappings visible) is the right shape and is what lets omissions surface at all.
- A05's 18 adversarial fixtures remain green as an **independent** oracle, confirming the A05 findings published earlier are stable.
- The two artefacts are **individually sound**; the defect is strictly in the **join** between them.

## 4. Consumer reality (duty 4)

A04's report claims actual C11/I03/I05/batch **6/6** plus **modeled** required-consumer receipts. On this source-free terrain I could **not** locate a runnable real C1/Field Forge downstream consumer for A04's outputs. Grade: **`CONSUMER_MODELLED_NOT_EXECUTED`**. I do **not** fabricate a consumer positive; the minimal future act is a narrowly scoped **B02** real-consumer commission against an already-qualified slice. Consumer satisfaction must be a **first-class required set** (as A05 models it), never inferred from job or product counts.

## 5. Provenance (duty 5)

`EXPECTED_SET_OUTPUT_DERIVED` in the A05 oracle is, by construction, a **hash-divergence detector**: it fires when the manifest declares its expectation as derived, and it detects divergence from the frozen frontier. It does **not** establish derivation provenance. A **post-result cloned expectation** that reproduces the frozen hash is **indistinguishable** by hash alone — the oracle cannot separate "frozen first, then executed" from "executed first, then cloned to match". As I recorded in the A05 return and again in WVF, **only an externally sealed pre-run freeze** closes this; hash equality never does. **`FREEZE_ENFORCEMENT_NOT_INDEPENDENTLY_PROVABLE_BY_HASH`.**

## 6. Grade

`TECHNICAL_ACCEPTANCE_WITH_EXACT_DEFECT` for both artefacts **individually**, at development/source-free scope, with the following **separate holds**:

1. **The A04↔A05 join is not hash/preimage interoperable** (§2) — requires a versioned successor mapping before any cross-artefact settlement.
2. **A05 cannot represent `measure_kind` or `condition_order`** — the successor must carry them or the distinction is lost.
3. **Consumer closure is modelled, not executed** (§4).
4. **Freeze provenance is not provable by hash** (§5).
5. Unchanged and not granted here: competent producer issuer · operative G0b · EE12 · world/V3 actor · canonical adoption · any all-35 eligible frontier.

**Terminal:** `HQ280_PV3_A04R_INDEPENDENT_BINDER_ORACLE_OWNER_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`.
