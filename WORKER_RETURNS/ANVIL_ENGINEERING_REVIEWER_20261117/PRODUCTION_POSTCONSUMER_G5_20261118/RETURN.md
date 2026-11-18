# ANVIL production postconsumer G5 — independent acceptance

## Verdict

**`ACCEPT_SCOPED_PRODUCTION_POSTCONSUMER_PREPARED_ADMISSION`**

Author evidence commit: `e0445a00f2fbb9643880aeb83452aa956f8134fe`  
Actual code/test: `01dc90cb0d1c5c7cdcf5cb29a02bc0cfda650efd`  
Baseline: `6b5402658a342a32180e281c62f4762729e37220`  
Prior review: `4d41a11a1b4da4ca0b543791e679b2de6377a8b1`  
Reviewer: `ses_e30c25800ffeT8XbyTuHekRCme` — distinct nonauthor.

The exact authorized production delta is correct and independently executable. The new
focused tests, the 45-node affected suite, the changed-input/restore test, and the
actual sourcefree postconsumer witness all pass from an isolated snapshot of the exact
`01dc90cb` source.

## Exact delta

Only two files differ from baseline:

- `rawlsing_next/pre553_source_postconsumer_receipts.py`:
  - import `PreparedSavedC11Admission`;
  - in `join_saved_source_operation_fates`, replace the exact
    `type(admission) is not SavedC11Admission` guard with the exact tuple
    `type(admission) not in (SavedC11Admission, PreparedSavedC11Admission)`.
- `rawlsing_next/tests/test_anvil_prepared_saved_postconsumer_join.py`: new 276-line,
  8-node focused regression.

There is no `isinstance`, subclass acceptance, base proxy, producer-type change, or
relaxation of any other join guard. The source/current/authority/manifest/I02/U/root/
replay/runner.repository/issuer checks in the unchanged join body remain in force and
are exercised by the focused and affected tests.

Source blobs:

- `pre553_source_postconsumer_receipts.py`: `4bf3d8e38227df01c20308fd421b552f3cc0badc`
  → `0a2e7b899ebd392761d38b8ceb175f0bf81c6378`
- new test: `d555f811353532f6df4b1eed3ea3476e4bb87719`

## Independent execution

The source was extracted with `git archive 01dc90cb rawlsing_next` into a private
proof root, with `PYTHONPATH` set to that exact snapshot. No REVIEWER product was on
the import path. Snapshot source was not committed.

| Check | Command/result | Exit |
|---|---|---|
| Focused new suite | 8 passed in 8.82 s; max RSS 154,083,328 B | 0 |
| Affected suite | 45 passed in 29.05 s | 0 |
| Changed-input/restore | `test_source_to_saved_cold_s1c_i03_i05_batch_normal_and_exact_fate_join`: 1 passed, 23 deselected, 4.99 s | 0 |
| Frozen-author actual witness | 3.65 s; max RSS 135,921,664 B; no abort | 0 |

Focused negative coverage includes: arbitrary admission object; exact
`SavedC11Admission` subclass and exact `PreparedSavedC11Admission` subclass;
foreign runner/repository; estate manifest drift; independent-I02 logical-root drift;
CURRENT revoked after a valid prepared Batch; unissued/fabricated query; and forged
completed receipt/native output. The positive case checks exact base-vs-prepared
rows, audit, native output refs, provenance refs and result hash, plus one prepared
index build.

## Actual witness

The frozen author witness logic was copied to own evidence and only its output
directory was changed; the logic and source snapshot are exact. See
`evidence/witness_output_path.diff`.

Independent actual results:

- base: `SavedC11Admission`, 13 Batch units, all `COMPLETED`;
- prepared: `PreparedSavedC11Admission`, 13 Batch units, all `COMPLETED`;
- prepared index builds: **1**;
- 22 operation fates: **ELIGIBLE 8 / HELD 14**;
- **6** positive native-linked operations;
- **2** pending eligible operations;
- 13 native completed units rechecked;
- 8 native discovery candidates exactly joined;
- 0 issue grants created;
- v1 preserved at **0 QUERY / 1 DISCOVERY**;
- v2 issued **12 QUERY / 1 DISCOVERY**, scoped `TEST_ONLY_SOURCEFREE` with
  `native_original_source_rights = NOT_GRANTED`;
- exact `rows_equal`, `audit_equal`, `result_hash_equal`, native-output-refs equal,
  and batch-provenance equal.

No original35, native-science, source, production-CURRENT, issuer, writer, schema,
100k/6 GiB, protected-merge or full-matrix claim is made. The 45-node suite is
targeted, not the whole repository.

## Fixture identity and author evidence

The independent witness creates a fresh sourcefree SAV fixture. `pyreadstat.write_sav`
writes a source file whose identity can include a timestamp; therefore
source/root/dependent hashes are per-run. The author's reported source hash
`8d1f2...` and join hash `9ff0e2...` are not reproducible byte-for-byte from a new
private fixture; the independent run produced `0373cf...` and `f954ef...`. This is a
fixture reproducibility limit, not a production-code defect. The required exact
full-row, audit, native-output, provenance and result-hash parity is satisfied
**within** the independent run, not merely by counts. Details are in
`FIXTURE_IDENTITY.json`.

The author's 8-focused and 45-affected claims were independently reproduced: 8/8 and
45/45. Author source/test blobs match the frozen `01dc90cb` target exactly.

## Resource and scope

- Witness: 3.65 s wall, 135,921,664 B max RSS, no abort.
- Focused: 8.82 s wall, 154,083,328 B max RSS.
- Affected: 29.05 s wall.
- All under the existing 120 s / 2 GiB / 2 GiB child bounds; no subagent, model,
  provider, account or product-source rewrite was used.
- No new benchmark matrix, estate geometry, 100k/6 GiB run, or original35/source run.
- The concurrently active locality author worktree/file was not touched or reviewed
  prematurely.

## Authority and handoff

USER DIRECT GO 2026-11-18 authorized both exact production edits and this independent
review; no historical owner approval is required **for those exact edits**. This
acceptance is scoped to the exact two-file delta. It does **not** grant merge,
protected integration, scientific acceptance, original35/source rights, or broader
production adoption. The product remains **UNMERGED**; merge/broader adoption requires
the separate freeze and owner process. No author repair is requested.

Artifacts: `REVIEW_VERDICT.json`, `FIXTURE_IDENTITY.json`, `SOURCE_MANIFEST.json`,
`SOURCE_CHECKS.tsv`, `rawcommands.txt`, `evidence/` (independent logs, witness, exact
witness path diff, author comparison evidence), and `snapshot/` (only the two exact
changed payloads). Commit and remote verification follow; STOP after that.
