# PYAT HQ207 — R9 bounded porting repair — R1

**Disposition:** `R9_GOVERNED_ENVIRONMENT_QUALIFICATION_FAILURE`

**Branch:** `agent/rabochii-pyat-hq207-r9-repair-r1`
**Startup SHA (verified exact):** `70ca48345d97f26ac1d7061df2138ab3f14c474c`
**Exact repair base:** `dfdf5659fd78e9bc996b07383349094059a5553d`
**Independent adjudication read:** `7a5cf25ab3fb98fe5311e0a394b4432a498f6546`
**HQ207 adjudication applied:** `cfe648bd462ddf6fc1252182c5e784ec43bf4405`
**Checkout:** `SPARSE_REQUIRED` — no clone, no full worktree.

**Terminal:** `HQ207_R9_BOUNDED_PORTING_REPAIR_RETURNED__HQ_FINAL_REVIEW_REQUIRED`

---

## Short version

**Repairs 1 and 2 are done and verified. Repair 3 cannot be performed, because the interpreter the
commission names does not exist on this machine — and the same commission forbids me from making it.**

The porting gap is genuinely closed: the two SR06 regressions are gone, zero new failures, and the
resulting failure set is **identical to the pure pre-fan-in control baseline**. That is the strongest
result available on the repair itself.

I am not claiming the governed qualification happened. I ran every court in a disclosed,
package-set-identical substitute and I am labelling it as exactly that.

---

## Repair 1 — SR06 test port: COMPLETE

`rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py`

| | before | after |
|---|---|---|
| test blob | `b2c279e6ad85d695` | **`dfd063227e4a0897`** (adopted, byte-exact) |
| decoder blob | `b406d45fae419c02` | `b406d45fae419c02` — **untouched** |
| test count | 17 | 17 |
| test name set | — | **identical** |

The pair is now correct: accepted decoder `b406d45f` with its co-evolved accepted test `dfd06322`,
exactly as co-located on `0deb6478`. The control decoder `d2a074a4` was never restored.

**Nothing was retired.** The sorted `def test_` name lists before and after diff to empty.

I read both blobs and confirmed HQ205's causal account myself rather than inheriting it:

- **Test 1** — *only the seam name changed.* The old test patched `decoder._sha`; the accepted
  revision patches `decoder._governed_source_sha`. Same invariant, same `hash_calls == [path]`
  assertion. I verified the ordering in the accepted decoder myself: `_governed_source_sha` at
  **line 615**, `metadata_read` at **623**, `selected_read`/`full_read` at **643/652**. The hash
  still precedes every decode.
- **Test 2** — the chunk-path and compatibility-routing halves are preserved, and the compatibility
  half is actually **strengthened**: the accepted revision adds `full_reads == 1` and
  `selected_reads == 0`, which the old test never asserted. Only the `read_file_in_chunks`
  `chunksize == 2` assertion is dropped, replaced by the stronger governed property
  `chunk_reads >= 1 AND path_opens == 1` plus exact cell tuples.

**Both target tests pass.**

**Honest weakening, recorded not hidden:** the ported test no longer asserts a requested chunksize,
so a chunk-size regression on a multi-chunk carrier would slip through. The underlying behaviour is
independently verified correct (HQ197, 1000-row carrier). This is a **coverage weakness, not a
defect** — and I did **not** write a replacement assertion, because inventing one exceeds a bounded
port. Referred to HQ as an open item.

---

## Repair 2 — R7 gate attribution: COMPLETE

**The canonical 55-test six-file R7 denominator is the qualification of the accepted C4C3 lineage. It
is not a current-control obligation.**

Its authority — `05_AUTHORITATIVE_C3_COURT.json` at `1df64cc59` — is on the accepted lineage and is
**not an ancestor of control**. The three unreachable files are tests for accepted-C3 *production*
modules, and one of those modules (`closed35_g01_sav_numeric_representation_authority`) is **wholly
absent from control**, so restoring the courts cannot be a court-file-only act. Control carries its
own sanctioned court set in `.rabochii/court_spec.json`, which excludes all six R7 files.

The unsatisfiability on control is a **gate-attribution error, not a missing-dependency defect.**

Current-control acceptance is therefore restated as three parts:

1. current-control sanctioned court set (`.rabochii/court_spec.json`)
2. the reachable R7 subset — **25 collected, 25 passed** ✓
3. the accepted R9 focused courts — **69/69** ✓

**No C3 production module and no closed35 court was imported.** Nothing was done to manufacture 55
collected on control.

**One method choice worth flagging:** I did **not** rewrite the fan-in lane's signed receipt. That
lane's measurements, counts and blobs were accurate — only the *attribution* was wrong. Overwriting a
prior lane's receipt would destroy the audit trail, so I preserved
`03_TEST_AND_R7_RECEIPT.json` byte-for-byte at blob `ddc1f39f` and placed a clearly-marked
`06_HQ207_GATE_ATTRIBUTION_CORRECTION_NOTICE.json` beside it. HQ ordered the receipts "state
truthfully"; a correction notice beside a preserved receipt does that without erasing what a lane
actually observed.

**Part 1 was not run by me** — the control court set is outside this bounded repair. Named in the
criterion for completeness; flagged, not claimed.

---

## Repair 3 — Governed environment: **FAILED**

The commissioned interpreter:

```
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python
```

**does not exist.** Neither do its parents `qualification/` or `tooling/`. A bounded
`find /Users/matthewsmith -maxdepth 7` for the venv name returns nothing. `/var/folders/.../c4c3-env`
— the exact path recorded in the governed lock — is also gone.

Reconstitution is prohibited, so the governed qualification could not be performed. **I did not
reconstitute, did not install anything, and did not relax the pin.**

What I did instead: ran all five commissioned court sets in an already-existing, fully disclosed
substitute whose freeze is **set-identical (14/14)** to the governed
`01_ENVIRONMENT_LOCK.json` at `deea4054`, on CPython 3.11.3, with **pyreadstat 1.3.6 held exactly**.

| court | expected | result |
|---|---|---|
| execution-binding | 34 | **34/34** |
| source-session | 15 | **15/15** |
| broker | 20 | **20/20** |
| R9 aggregate | 69 | **69/69** |
| reachable R7 subset | 25 | **25/25** (79.42s) |
| ported SR06 file | — | 14 passed, 2 failed, 1 skipped; **both target tests pass** |

All three R9 court blobs verified byte-identical to `0deb6478`.

The 2 residual SR06 failures are `ModuleNotFoundError: No module named 'duckdb'` — and **`duckdb` is
absent from the governed lock too**, so they are expected under the governed freeze and are *not* an
artifact of my substitute.

**These are strong evidence, not a governed-environment certification.** HQ must either restore the
governed environment or explicitly re-authorise this substitute.

---

## Regression proof

The 12-file list was never enumerated in the record, so I reconstructed it: 16 decoder/codec-consuming
test files → per-file collection → the three R9 courts excluded (they did not exist at pure control
base) → 13 candidates / 115 tests → one 6-test file excluded. I then **ran both arithmetically valid
12-file candidates in the pre-port state and both reproduce the recorded baseline exactly**, so the
choice is immaterial to the delta.

| state | failed | passed | skipped |
|---|---|---|---|
| pure control base *(recorded by fan-in lane)* | 14 | 94 | 1 |
| fan-in candidate, pre-port *(measured by me)* | **16** | 92 | 1 |
| **post-port, this lane** | **14** | **94** | 1 |

**Set-level comparison**, not aggregate — I diffed the sorted `FAILED` lists on the five files
containing any failure:

**Fixed (exactly 2):**
- `test_pre553_sr06_decoder_carrier.py::test_expected_source_identity_is_hashed_once_before_reader_decode`
- `test_pre553_sr06_decoder_carrier.py::test_normal_decode_uses_chunk_path_and_compatibility_uses_full_read`

**New failures introduced: none.**

So the post-port failure set is **identical to the pure pre-fan-in control baseline**. The accepted R9
runtime fan-in is now **regression-neutral** on this slice. The two `MATERIAL_MECHANISM_DIVERGENCE`
findings the fan-in lane honestly reported against itself are fully resolved — and the resolution
required only the co-evolved test adoption.

Nothing suppressed, retried away, xfailed or skipped to go green.

---

## Material new counterexample — recorded at HIGH severity

**Four checkable claims in the independent adjudication `7a5cf25a` (`03_ENVIRONMENT_QUALIFICATION.json`)
are false on this host.** I did not use this as my headline disposition, but HQ needs it, because
**HQ207's Repair 3 was authorised on its premise.**

| adjudication claim | actual here |
|---|---|
| governed R7 venv present, runs, 3.11.3/1.3.6/2.3.3/2.4.6/25.0.1 | **ABSENT** |
| governed C4C3 base interpreter present, runs | **ABSENT** |
| `c4c3-env` present | **ABSENT** |
| `hq204-r9-env` **deleted** — a durability defect in the fan-in lane's evidence | **PRESENT and functional** |

The last one is **inverted**: the durability defect HQ205 attributed to the fan-in lane does not
exist. That lane's declared environment is re-runnable — I used it.

The most serious item: the adjudication states *"proof_i_used_it: I ran pytest --collect-only … with
the governed interpreter and obtained … 25 tests collected."* I reproduced that exact 25/25 — **in a
different interpreter**. The governed one cannot run here.

**What I am not claiming:** nothing about motive. `TMPDIR` and `LOCAL_COURTS` are volatile, and a
genuine difference in host state is entirely possible. I record only what is checkable here and now.

**Corroboration:** the fan-in lane's own receipt already recorded
`governed_r7_interpreter_present: false` and `governed_environment_reproducible_from_this_machine: false`.
My deeper search **agrees with the fan-in lane and disagrees with the adjudication**, which means
HQ205's proposed explanation — that the candidate merely searched too shallowly — does not hold. A
deeper search finds nothing.

---

## For HQ — open items

1. **Blocking:** restore the governed environment, or explicitly re-authorise the substitute. No
   governed qualification can be claimed until then.
2. Annotate or correct HQ205 `03_ENVIRONMENT_QUALIFICATION.json`; four environment claims are false here.
3. Chunk-size assertion coverage is weaker post-port. Recovering it needs a new assertion on a
   multi-chunk carrier — outside this bounded repair, so not done.
4. Part 1 of the restated criterion — the control sanctioned court set — was not run here. The
   final-acceptance lane must run it.
5. The service-source applicability implementation candidate `e7d3598…` still needs the independent
   hostile review HQ207 mandated. Out of scope; untouched.

---

## Holds respected

No decoder change · no production C3 backport · no test retirement · no environment reconstitution ·
no packages installed · no raw source access · no warrant · no live C4 · no C7 · no actor/person work ·
no self-adoption · no fabricated 55-collected · no suppression or retry of any failure · pyreadstat
1.3.6 pin held · prior lane receipts preserved byte-for-byte.

**Files changed:** one authorised test port; one additive correction notice; this return directory.

`HQ207_R9_BOUNDED_PORTING_REPAIR_RETURNED__HQ_FINAL_REVIEW_REQUIRED`
