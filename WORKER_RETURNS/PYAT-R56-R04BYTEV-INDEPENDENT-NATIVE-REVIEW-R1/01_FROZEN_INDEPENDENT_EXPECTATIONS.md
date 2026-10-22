# R56-R04BYTEV — frozen independent semantic/identity expectations

Written BEFORE executing the candidate test suite or generating any candidate
outputs in this session. Derived only from: the pre-existing (startup
`6d95a78b`) test fixtures `_fixture`/`_branch_predicate`/`_query`, the
pre-existing facade contract in `pre553_source_backed_c11_facade.py`, the
pre-existing I03 query engine, and the row data in the author test module
(`_ROWS`). Candidate-produced hashes/values are NOT used as the oracle.
(Author evidence JSON was inspected for custody/record purposes after these
semantic expectations were derivable from the pre-existing source above; no
expected value below is copied from it.)

## 1. Generated inputs (synthetic, real writer)

`_ROWS` = 3 rows × 7 variables:

| row | X | Y | M | O | R | G | W |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 1 | AB | AB | XY | A | 2 |
| 2 | 0 | 0 | A | BA | XZ | B | 1 |
| 3 | None | 1 | "" | AB | XY | A | 3 |

Written with installed `pyreadstat.write_sav` / `write_dta` to `*.sav` / `*.dta`.

- Expected physical cells per file: 21 (3 rows × 7 variables), row ordinals 1–3, variable ordinals 1–7.
- Y physical values in row order: `1, 0, 1` (row 3 observed).
- X row 3 is system missing.
- Source identity: `sha256(file bytes)` must equal `incidence.source_sha256`
  and `incidence.source_custody["snapshot_sha256"]`; snapshot bytes digest must
  equal the same value; `snapshot_path != source_path`; snapshot path must be
  in a private temp directory (not the source directory).

## 2. Expected C11 facts (unchanged facade)

- Projection fixture `_fixture("r04byte-{fmt}")` binds response slots
  X(1), Y(2), M(3), O(4), R(5), coordinate G(6), weight W(7).
- Occurrence counts: X 1+1+1=3 (row 3 MISSING rule carries one scalar
  occurrence in the fixture), Y 3, M 2+1+0=3, O 6, R 6 → expected
  `RespondentEvent` count = **21**.
- Routing fixture: risk set `R` for Y has members {R1, R2} (row 3 NOT_ELIGIBLE).
- All 3 respondents are in the branch-cohort predicate.

## 3. Expected I03 EmpiricalFact (unchanged query engine)

Query: targets ("Y",), domain ["0","1"], measure RAW, risk set R, predicate =
exact branch cohort of all 3 respondents.

- `typed_state == "SUPPORTED"`.
- `raw_denominator_support == 2` (R1, R2 only; R3 not routed for Y).
- cell "1" numerator 1 (R1 Y=1), cell "0" numerator 1 (R2 Y=0).
- total `raw_numerator_support == 2`.
- denominator member refs = exactly {R1, R2}.
- Two independent decodes of byte-identical sources must yield the same
  release content hash and the same `EmpiricalFact` ref and payload.
- Different bytes (e.g. `_ALTERNATE_ROWS`) must yield a different source
  sha256, different release content hash, different fact ref and different
  Y-cell values. The old source sha256 must never appear in facts derived
  from the alternate bytes.

## 4. Frozen custody/refusal expectations

1. `decode_*` with an `expected_source_sha256` different from the actual file
   digest → typed `DecoderError` before any reader call.
2. Replace the original source path immediately after snapshot acquisition
   (before metadata/value reads) → decode consumes the acquired snapshot;
   downstream facts must equal the baseline facts and
   `source_custody["snapshot_sha256"]` must equal the original digest.
3. Replace the original source path between metadata and lazy value phases →
   lazy values must come only from the snapshot path; facts equal baseline.
4. Alter/truncate the snapshot in place after acquisition → typed
   `DecoderError` before native facts are served.
5. `close()` → snapshot path and directory removed; subsequent lazy reads →
   typed `DecoderError`.
6. Fresh-process old-digest cold replay with changed bytes → nonzero exit,
   no fact JSON; restoring exact original bytes → identical fact payload.
7. Genuinely changed same-path bytes acquired anew → new digest/new facts;
   the previously decoded old incidence still serves the old facts.
8. Content-verification-to-reader window: after `verify_source_identity()`
   passes, but before the actual reader opens the file (metadata pass or lazy
   value pass), replacing the **private snapshot path** with valid alternate
   bytes must NOT result in downstream C11/I03 facts built from the alternate
   bytes while carrying the old `source_sha256`/`snapshot_sha256`. The
   consumed bytes must determine the facts; either refuse or serve the bound
   original content.
9. Between-batch window: altering the snapshot in place after the first lazy
   batch but before later batches must not silently serve later rows from the
   altered bytes under the old identity (unless the implementation re-verifies
   before each read or otherwise binds consumed bytes).
10. Any implementation claim of identity must be evaluated on actual C11
    `RespondentEvent`/I03 `EmpiricalFact` values and source identity fields,
    not on decoder status flags or comments. Private snapshot/runtime trust
    assumptions (same-uid write access to the private directory, no hostile
    same-uid process) must be reported explicitly rather than claimed as
    unconditional immutability.
