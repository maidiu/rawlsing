# PYAT C4 — Disputed-claims independent re-check — R2 (corrected)

**Disposition: `MATERIAL_CORRECTION_REQUIRED`**

Terminal: `C4_DISPUTED_CLAIMS_RECHECK_R2_RETURNED__HQ_ADJUDICATION_REQUIRED`

Branch `agent/opencode-pyat-hq183-c4-disputed-claims-recheck-r1`.
I am the independent reviewer. I do not adjudicate, adopt, or self-adopt.

## Lineage — verified, not assumed

| | |
|---|---|
| Expected HEAD | `e00823a9132b612b595df04a26a4fd5e7c7e0ada` |
| **Observed HEAD** | `e00823a9132b612b595df04a26a4fd5e7c7e0ada` — **matches** |
| R1 commissioned tip | `dd00896848c98de5e6ff124fd50f8508431fc0ff` |
| Anchor | `git merge-base --is-ancestor dd008968 HEAD` → **holds** |
| Commits over commissioned tip | **23** |
| Force-push used | none observed |

Tooling as commissioned: `python3` = **3.11.3** at `/usr/local/bin/python3`, functional.
`git` 2.39.1.

**One lineage fact HQ should know:** the freeze `8ff40d37d` and C4A `8f7efe690` are
**not ancestors of HEAD**. This branch diverges from the freeze at merge-base
`87029d34`. The corrected packet cites the freeze by SHA across a control-plane
lineage rather than containing it. That is consistent with the commission directing
comparison against `8ff40d37d`, and it changed none of my findings — I resolved all
five against the exact pinned commits. But a verifier working only from HEAD cannot
reach the freeze by ancestry.

## Bottom line

**C1's withdrawal is correct. C1's substitute justification is not, and the packet's
statement "No counterexample exists" is refuted.**

I found the counterexample the commission asked me to hunt for. It is not in the
four rows of the packet's table — all four of those are exactly right, and I
extended them to all eight court modules and all eight still match. The
counterexample is one level down, in the **transitive closure**.

| Finding | Verdict |
|---|---|
| **C1** — withdrawal of HQ183's producer claim | **UPHELD** |
| **C1** — substitute basis ("61/61 qualifies the exact freeze bytes") | **REFUTED** |
| **C2** — R7 wording and residual class | **UPHELD**, residual class needs completing |
| **C3** — hash census | **UPHELD**, two clarifications |
| **C4** — R9 gap | **UPHELD**, one field-name correction |
| **C5** — R10 digest | **UPHELD** |

## C1 — the withdrawal stands

HQ183 claimed the producer was `6560d7a9` at M01 bounded-court time. That is false,
and the withdrawal is correct. The full binding chain, read from the file rather
than from commit messages:

| Binding commit | `semantic_candidate_sha` | producer blob at that candidate |
|---|---|---|
| `295d270c3` | `1982dec1…` | **`6560d7a9`** ← HQ183's source |
| `c0f538b6c` | `903c262e4…` | `2385cd32` |
| `ddf0ccfee` | `a1545aee…` | `2385cd32` |
| `74a06774` | `46f3bec8…` | `2385cd32` |

`74a06774` changed exactly one file, 1 insertion / 1 deletion
(`.rabochii/court_spec.json`), repointing `semantic_candidate_sha` from `a1545aee…`
to `46f3bec8…`. Both `46f3bec82` and `74a06774` are ancestors of C4A `8f7efe690`.
All four of the packet's table rows reproduce exactly, and I extended the check to
the two production modules and two test modules the packet omitted
(`pre553_discovery_exact.py`, `pre553_empirical_query.py`,
`test_pre553_discovery_exact.py`, `test_pre553_empirical_query.py`) — **all match**.

## C1 — the counterexample

The court's `tests[]` array has **four** files, not two. Their transitive closure is
**23 modules** (independently derived; corroborates the packet's own "23 modules"
figure). Closure membership is identical at `46f3bec82` and at the freeze. But two
modules inside it have **different bytes**:

| Module | at `46f3bec82` | at freeze `8ff40d37d` |
|---|---|---|
| `rawlsing_next/pre553_physical_decoder.py` | `d2a074a4…` | **`d3d828c1…`** |
| `rawlsing_next/pre553_r5_codec.py` | `72f8f3c0…` | **`6000a170…`** |

Both were changed by `30686b18` "Integrate accepted C3" — the accepted C3 head that
C4A merged. And `test_pre553_route_b_production.py` — **11 of the 61** — imports
`PhysicalCell, PhysicalMissingState` from `pre553_physical_decoder`, which imports
`pre553_r5_codec`.

So **11 of the 61 tests executed against different decoder and codec bytes than the
freeze pins.** The `rawlsing_next` tree is `8ce223b7…` at the M01 court head and
`b0c1ab47…` at the freeze — **37 files differ**.

The packet's own hedge does not cover this. It disclaims a *Darwin rerun*
("No claim is made that the complete producer-inclusive M01 path was freshly rerun
on Darwin"), not a byte difference already present at binding time.

### Why this does not move a stage blocker

The two differing modules are exercised **at the freeze's exact bytes** by C4C3's
authoritative six-file / 55-test court — all six of those files import them, and the
three C3 surface test blobs at the freeze are exactly the pinned accepted C3 blobs
`fb7b0908` / `8fc05965` / `3901f10a`. C4C3 ran 55/55 twice on the combined tree at
those bytes. So the freeze's authority for `pre553_physical_decoder` and
`pre553_r5_codec` comes from C3's accepted court plus C4C3's rerun — **not** from
M01. The defect is in the record's characterisation, not in the freeze's evidence.

Stage-separated blockers therefore **stand as the packet states**: freeze acceptance
0, warrant issuance 1 (R9), live execution 1 (R7), advisory 9. What changes is that
**"counterexamples: 0" is no longer true** — there is one, against the substitute
justification.

## C2 — upheld

Exact wording at `1df64cc59`, blob `3953caae…` (identical at the freeze):

> "The venv lives in a per-session temporary directory. It is NOT durable and NOT
> reproducible **from this path alone**. … The reproducible content is the freeze
> below, not the path."

The packet is right that the wording is "from **this path alone**", not "from the
repository" — the string `from the repository` does not occur in the file. A pinned
**13-package** `reproduce_command` exists, all `==`-pinned.

**Residual class: the packet says "fingerprint incompleteness". That is the
load-bearing class but not the whole answer — the correct answer is "both".**

- *Fingerprint incompleteness*: only a **32-hex (16-byte)** prefix of the base
  interpreter is recorded (`base_interpreter_sha256_prefix32`).
- *Environment irreproducibility, weakly*: the recipe pins 13 packages but **not**
  `narwhals`, the unpinned transitive of `pyarrow` that the freeze itself records.
  A re-resolve could therefore select a different `narwhals`.

The record does not *claim* irreproducibility — it disclaims it and supplies a recipe
— so HQ should not record R7 as environment irreproducibility. But "both" is the
honest classification.

## C3 — upheld

Structural field-path walk of the lock (not a grep):

| Class | Count | Verdict |
|---|---|---|
| 16-hex, all field-named `*_prefix16` | **32** (16 packages × `metadata_prefix16` + `wheel_prefix16`) | as asserted |
| 32-hex structural fields | **6** (1 `base_interpreter_sha256_prefix32` + 5 `compiled_extensions.*.cpython-311-darwin.so`, no prefix marker in the key) | as asserted |
| 40-hex complete Git SHA-1 tree identities | **2** (`no_repo_mutation.rawlsing_next_tree_before` / `_after`, both `b0c1ab47…`) | as asserted |
| complete 64-hex | **3**, all `9cde8e5ab9abba…` | as asserted |

38 SHA-256 prefixes + 2 Git trees + 3 full digests = 43. **HQ182's "40 truncated
SHA-256" was indeed wrong** — the 40-hex values are complete Git SHA-1 tree
identities, not truncated SHA-256.

Two clarifications so HQ is not caught on a re-count:
1. The 32 16-hex values are 32 field instances but **29 distinct** (three wheel
   digests are shared across package pairs: pandas/numpy, python-dateutil/pytz,
   pip/setuptools).
2. The 32-hex values occur **9 times in raw text**, not 6 — three are prose
   restatements inside the `CROSS_ENVIRONMENT_REPRODUCIBILITY_DATUM` narrative
   string, not additional fingerprint fields. Counting structural fields gives 6.

## C4 — upheld, one field-name correction

Per-source constraints **do** survive in artifact 07 for all eight sources, and the
warrant retains `canonical_sha256`, `allowed_operations`, `reader_lane`, `authority`,
`max_retry_budget` (0) and `raw_bytes_retention` per source. Only explicit per-source
read-limit counters are absent: C4B's template carried
`source_access_accounting` with seven slots for each of seven sources; the candidate
has **no** per-source block, but does carry a **global**
`access_accounting_instrumentation_bound` (top-level, 10 accounts,
`basis_required_per_figure: true`).

**Correction:** the packet says artifact 07's 8 sources carry
`expected_full_reads` and `expected_selected_reads`. They carry them for **6 of 8**.
`SRC27` instead carries `expected_full_route_passes: 1` / `_max: 1`; `SRC35` carries
`fresh_reads: 0`. The constraint content survives for all eight; two of the four named
field names do not exist for two sources. `max_retry_budget` and `retry_law` are
present 8/8.

## C5 — upheld, recovered not guessed

`T3_freeze_sha256` is present in full at
`WORKER_RETURNS/PYAT-C4B-WORKLOAD-ORACLE-FREEZE-R1/04_WVS_ORACLE_CUSTODY.json`
(blob `42067aac…`, identical at `c2af4f61` and at the freeze), field path
`later_T3_standardization.T3_freeze_sha256`:

```
7dfb62362b983b92dee2774d8621f... -> 7dfb62362b983b92dee2774d862a46c0c0ce3ca2c3bb48850e0f400346936908
```

Exact match to the asserted value. The freeze packet's `"7dfb6..."` in
`05_ORACLE_AND_COMPARISON_LAW.json` is the **only** truncated-in-value identity
anywhere in that 12-file packet — I swept for it.

One oddity to note: this same digest appears in Omega-1 at
`identity_rules.full_route_oracles.LiTS_I.T3_sha256` — the *same literal* recorded
under the LiTS lane in Omega-1 and under WVS `later_T3_standardization` in C4B.
Cross-lane attribution is worth reconciling at some point; it does not affect C5.

## Failure-mode check

**None of C2–C5 shares HQ's inference-from-truncated-evidence failure mode.**

- **C2** quotes a field read whole from a pinned blob.
- **C3** is a structural field-path walk, which is *structurally immune* to the
  truncation failure — a truncated grep cannot produce a field-path census.
- **C4** reads three artifacts in full at pinned commits.
- **C5** recovers a named field from its authoritative source rather than
  reconstructing it from `7dfb6…`.

This matters: C3 in particular is the check most likely to have reproduced the
failure, and it did not.

## Pointer coherence — confirmed

The HQ185 repair holds. `LATEST.json` blob `6e671bfc…` at HEAD:

- `checkpoint_id` `20261002-PYAT-HQ186-C1-WITHDRAWN-R1` == `MANIFEST.checkpoint_id` == directory name
- `pyat_review_adjudication_decision` `HQD-2026-10-02-186` == `MANIFEST.governing_decision`
- `current_md_path`, `current_json_path`, `manifest_path` all exist at HEAD
- `handoff_commit` `5e456988…` is an ancestor of HEAD and contains all three files
- `MANIFEST.files[].blob_sha` — the field name is `blob_sha`, not `git_blob` — matches
  the actual blobs exactly: `CURRENT.md` `9a8ba96d…`, `CURRENT.json` `b1ca42f4…`,
  identical at the handoff commit and at HEAD
- `adoption_status` = `NOT_ADOPTED_INTO_BUILD__HQ182_HOLD_UNLIFTED` — hold preserved
- `DECISION_LEDGER.jsonl`: 191 lines, **0 invalid JSON**; the HQ186 row is present
  with status `C1_WITHDRAWN_IN_FULL__C2_C5_UPHELD__…__HQ182_HOLD_UNLIFTED__RAW_SOURCE_EXECUTION_HELD`

The superseded packet is preserved unmodified: `00_C4_CONSOLIDATED_DECISION_CLAIMS.md`
has one commit in its history (`4c4da2fe8`) and blob `a1202b64…` at HEAD.

## What I did not verify

- The **61/61** run count itself. Static `def test_` counts in the four court files
  are 11 / 4 / 14 / **30**, against a claimed 32 for the fourth. The 2-case gap is
  consistent with parametrisation but I did not run pytest, so I neither confirm nor
  refute 61. GitHub Actions run 36302391261 is not in this repository.
- The 37 other `rawlsing_next` files differing between the M01 head and the freeze —
  I characterised the count, not each file's relevance.

## Constraints observed

Raw survey source access **0**. No source locator discovered or filled. C4 not
executed; no test suite run. No warrant issued or altered. No production code
mutated; `git status` clean. Freeze not adopted; HQ182's hold not lifted; no
self-adoption. C4 review not rerun. Writes confined to
`WORKER_RETURNS/PYAT-C4-DISPUTED-CLAIMS-RECHECK-R1/**`.

## Required corrections

1. Withdraw "**No counterexample exists**" from the corrected packet.
2. Narrow the substitute justification: the 61/61 binds the freeze's bytes for the
   four court test files and their two named production modules, **not** for
   `pre553_physical_decoder.py` / `pre553_r5_codec.py`, which at binding time were
   `d2a074a4…` / `72f8f3c0…` rather than the freeze's `d3d828c1…` / `6000a170…`.
3. State that the authority for those two modules is C3's accepted court plus C4C3's
   55/55 at freeze bytes, not M01.
4. Record R7's residual class as "both", with the unpinned `narwhals` as the
   irreproducibility component.
5. Correct C4's field-name claim to 6-of-8 for the two `expected_*_reads` fields.
6. Leave the stage-separated blocker counts unchanged.