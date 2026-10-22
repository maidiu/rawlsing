# R56-R04BYTE — actual consumed-byte custody — author return

Status: `PREPARED_CANDIDATE__AUTHOR_ENGINEERING_QUALIFIED__R04BYTEV_INDEPENDENT_NATIVE_REVIEW_REQUIRED`.

## Scope and authority

- Task: `R04BYTE`; class `I2-I3 / S3`.
- Exact startup: `6d95a78bf6b7bcf70022e303a151255e65edc38a`.
- Branch: `agent/rabochii-pyat-r56-r04byte-consumed-byte-custody-r1`.
- Isolated sparse worktree: `/Users/matthewsmith/Desktop/Rawlsing/R56-R04BYTE-consumed-byte-custody-wt`.
- Authority: R56 narrow sourcefree grant; R57 R00P-R2 TEST_ONLY admission and bounded technical-seal delegation; user/director direction in this session.
- Author/session: OpenCode native session, model `opencode-go/deepseek-v4.1-flash`; harness OpenCode; host mainMac; Python `3.11.3`; pytest `9.0.2`; pyreadstat `1.3.2`. Actual reasoning effort is `UNKNOWN_NOT_EXPOSED`; the commission requested MAX and no different model/provider was silently selected.
- Separation: this session is not the R00P policy owner and did not author R02. No reviewer role was self-performed. Distinct `R56-R04BYTEV` native review remains required.

## Files written

- `rawlsing_next/pre553_physical_decoder.py`
- `rawlsing_next/tests/test_universal_source_byte_custody.py`
- `rawlsing_next/tests/test_universal_source_byte_custody.py.proof.json` (R57-classified non-executable documentary witness)
- `WORKER_RETURNS/PYAT-R56-R04BYTE-CONSUMED-BYTE-CUSTODY-R1/`

No adapter, C11, I03, Batch, Route B, frozen policy, foreign return or production module was edited. No original respondent data was read or generated.

## Implemented custody mechanism

`_acquire_source_snapshot` now opens the source once, copies the exact bytes to a private temporary snapshot file while computing SHA-256, applies the optional expected-digest gate before any reader call, and keeps a private read descriptor for verification. Snapshot directory is private; snapshot file is mode `0400`.

`_decode` uses that snapshot for:

- raw-layout prefix bytes via `pread` at offset zero;
- the `metadataonly=True` dictionary/metadata pass;
- the compatibility full read, when configured;
- the existing lazy `pyreadstat.read_file_in_chunks` value path.

`PhysicalSourceIncidence.iter_batches` refuses a mutable-path reopen when no content-bound snapshot exists. `verify_source_identity()` rehashes the snapshot before metadata/full-read and before each lazy pass; altered, truncated or closed snapshots produce typed `DecoderError` before differently sourced native facts are served. `source_custody` exposes the identity/size binding, and `close()` removes the private snapshot.

A replacement at the original path after acquisition cannot change metadata or values because no later read reopens that mutable path. A valid same-path new source decoded as a new acquisition gets the new digest and new facts; decoding it under the old expected digest is refused. A prehash followed by an unconstrained original-path reopen is not used.

The actual implementation has a metadata/value split: `metadataonly=True` followed by `read_file_in_chunks` for the value pass. There is no invented metadata/value call.

## Actual qualification

Core command:

```text
python3 -m pytest rawlsing_next/tests/test_universal_source_byte_custody.py \
  rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py \
  rawlsing_next/tests/test_r35_i01_physical_metadata.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py \
  rawlsing_next/tests/test_pre553_route_b_production.py \
  rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py \
  rawlsing_next/tests/test_fiabc_lm1_r1e_n1_physical_boundary.py -q
```

Result: `80 passed, 1 skipped` (receipt: `evidence/core_test_receipt.txt`).

The new test module alone: `16 passed`. It generates actual SAV and DTA files with the installed pyreadstat writer, decodes them through `decode_sav`/`decode_dta`, projects through the unchanged `pre553_source_backed_c11_facade` into validated C11 `RespondentEvent` facts, and executes the unchanged PRE553 I03 query path. The named downstream fact is the same `EmpiricalFact` and its `i03_fact_ref`, `raw_numerator_support`, `raw_denominator_support`, and `i03_y_cells` across positive, fault/refusal and restored runs.

Covered actual cases:

- positive immutable SAV and DTA input;
- replacement at the original path immediately after snapshot acquisition and before the metadata pass, yielding the original downstream facts;
- replacement between the metadata pass and the lazy value pass, with the chunk reader receiving only the snapshot path;
- replacement between the prehash identity gate and snapshot acquisition, refused before the reader;
- deliberately altered/truncated snapshot bytes, refused before lazy facts;
- valid same-path new-source identity, with old facts preserved by the old snapshot and the new acquisition carrying only the new identity;
- old-digest decode of the replaced path refused;
- fresh-process cold replay: changed bytes under the old digest fail, restoring the original bytes restores the exact same downstream fact payload.

`evidence/byte_identity_probe.json` records actual generated SAV/DTA byte sizes, source/snapshot SHA-256 equality, C11 release hashes, I03 fact references and cell digests.

Proof-integrity witness:

```text
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint rawlsing_next/tests/test_universal_source_byte_custody.py
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness rawlsing_next/tests/test_universal_source_byte_custody.py.proof.json --root . --receipt WORKER_RETURNS/PYAT-R56-R04BYTE-CONSUMED-BYTE-CUSTODY-R1/evidence/proof_witness.json
```

Result: AST lint pass; witness baseline pass; exact lazy-reader mutation produced `TARGET_ASSERTION_FAILED`; source restored. Receipt: `evidence/proof_witness.json`.

Retained S1/S2 decoder/carrier, metadata, facade, Route B, LiTS representation and N1 physical-boundary tests passed in the core receipt. Additional older R1E/R1I/R1J suites were also run after their retained artifacts were made available: `24 passed, 10 failed`; the failures are pre-existing frozen-authority/artifact mismatches in `authorized_decoder_physical_value`, `LOCK2`, and expected carrier values, not changes in this decoder diff. They are recorded as inherited/unrelated REDs and are not claimed as this candidate's qualification.

## Scope limits

- No claim of joined issued workload, partial interrupted Batch, revocation, dedup or R04.joined; those require R03 and later authorization.
- No original source, original35/N11 measurement, protected R09 CI, production promotion, Route B edit, shared-caller amendment or scientific adoption.
- Author engineering PASS is not independent `R56-R04BYTEV` acceptance.
- No shared-caller change was needed to demonstrate the commissioned edge at this baseline.

## Next action

Publish this one scoped candidate and stop for distinct `R56-R04BYTEV` native review. The reviewer should attack the same named C11/I03 fact under original-path replacement, lazy-reader boundary, altered/closed snapshot and cold old-digest replay, and may use the sibling proof witness.
