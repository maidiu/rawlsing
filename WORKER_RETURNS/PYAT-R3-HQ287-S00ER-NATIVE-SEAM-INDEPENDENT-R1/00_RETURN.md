# PYAT HQ287 S00ER — Independent native seam court

**TERMINAL:** `PYAT_R3_HQ287_S00ER_NATIVE_SEAM_INDEPENDENT_COURT_COMPLETE__GITHUB_PUSHED`
**GRADE:** `SOURCEFREE_HOLD__ORIGINAL_INDEPENDENT_ACCEPTANCE_NOT_PRESERVED`
**Branch:** `agent/reviewer-pyat-r3-hq287-s00er-native-seam-independent-r1` @ `0ab4ada15aeacfc265db10a745957de07bd702c7`
**S00E candidate:** `ac75c6fc899804b226a0fbd22245cbe0030ce876` · **original S00CR:** `7f0d655ff98056bfe161e4947ef0f17add521db2`
**Environment:** SECONDARY Mac · Python 3.11.3 · pytest 9.1.1 · isolated sparse worktree. **No original survey data. Retained GT2 scientific HOLD persists. No protected CURRENT, canonical merge, G0b or V3.** **No model identity, endpoint-privacy claim or cost figure invented; no automatic paid fallback used.**

## 1. THE CENTRAL RESULT — the original independent suite is NOT preserved

I ran the **byte-original** S00C test file as a **read-only overlay** (`/tmp/s00er_overlay/tests/test_original_s00c_overlay.py`, no assertion touched, no freeze identity altered, no implementation edited) against **S00E's implementation**:

```
python3.11 -m pytest /tmp/s00er_overlay/tests/test_original_s00c_overlay.py -q
  ->  26 passed, 1 FAILED   EXIT 1
FAILED …::test_s00c_change_source_owned_synthetic_numeric_values_changes_result
       KeyError: 'exact_probabilities'   (overlay line 311)
```

Against the same implementation, **S00E's own two files pass**:
```
test_r3_s02_seam_witness.py          -> 27 passed
test_hq286_s00e_s00cr_overlay.py     -> 18 passed     (27 + 18 = the reported 45)
```

**So the "45 passing" is real — but it is achieved with S00E's *modified* test file, not the original independent acceptance.** The original suite **fails 1/27** against the new implementation. That is precisely the distinction this commission was issued to establish.

## 2. The test file was modified — and the modification changes an acceptance expectation

| file | sha256 | bytes | `def test_` count |
|---|---|---|---|
| **original** S00C `54f14553` | `09ac3d24875007f1cbffd8f4cd8b3fd413ccaa7292c9f43f9d49225422f8dce1` | 16,264 | **27** |
| **S00E** `ac75c6fc` | `5a7d698b5df441410dfefbdff10c5f5d36e77fb6d0932502415cf7e8f9ff2d63` | 17,325 | **27** |

`cmp` → **DIFFERENT**. The modification is **additive** (not a deletion of assertions): S00E's copy adds
`value["raw_probability_exact_fraction"] = {"$exact_fraction": [1, 2]}` to the edited channel value, and adds new `edited_steps` and `stale` (self-rehashed) mutation blocks with their own `REFUSED` assertions.

**But the substance is a representation change.** S00E's implementation reads `exact_probabilities` from channel values; the **original** synthetic mutation set only `raw_numerator_support`, so the original test now dies with `KeyError: 'exact_probabilities'`. The original acceptance expectation — that mutating a source-owned synthetic numeric value is enough to change the result — is **no longer satisfied as originally written**.

I state this carefully: the modification **adds** coverage (self-rehashed substitution refusal is genuinely new) and I found **no evidence of assertion weakening or oracle loosening**. The defect is that the **original independent acceptance is not byte-preserved and does not pass**, so S00E's 45-green cannot be read as "the original independent court still holds".

## 3. On the "16-test file" figure

The commission describes the original as a **16-test** file. I measure **27** `def test_` functions in the original S00C file (and 18 cases in the overlay). **I record the discrepancy rather than adopting either number**, and I do not silently reinterpret the commission's figure. The relevant comparison (original bytes vs S00E bytes, same function count, different sha) is unaffected by it.

## 4. Internally consistent source-free data vs independently authenticated producer values

Preserved as required: everything exercised here is **internally consistent source-free synthetic data**. A **local content hash is not an external source issuer**; a self-rehashed bundle passing or failing an internal assertion establishes local consistency only. **No producer authentication is claimed, and none of these results issues scientific or source authority.**

## 5. Grades, kept separate

| dimension | result |
|---|---|
| S00E own author/overlay suites | **45 passed** (27 + 18) — internally consistent |
| **original independent S00CR/S00C suite vs S00E impl** | **26 passed, 1 FAILED** — acceptance expectation changed |
| freeze identity / assertions / implementation | **not edited by this reviewer** |
| science | **HOLD** — retained GT2 scientific hold persists; no scientific issuance |

## 6. Exact open requirement for the next owner

Either (a) the original S00C acceptance test is re-satisfied by the implementation as written, or (b) an **explicit, versioned acceptance migration** is recorded stating that the source-owned synthetic numeric-value representation moved from `raw_numerator_support`-only mutation to requiring `exact_probabilities`/`raw_probability_exact_fraction`, with the original test replaced by a declared successor — **not** by an unannounced edit to the frozen independent file. Until one of those is committed, the original independent acceptance stands **unmet** on the "34/1-style" evidence standard this programme has been applying.

**Terminal:** `PYAT_R3_HQ287_S00ER_NATIVE_SEAM_INDEPENDENT_COURT_COMPLETE__GITHUB_PUSHED`.
