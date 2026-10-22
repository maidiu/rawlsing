# R56-R04BYTEV r2 — exact commands, exits and observed results

All runs in `/Users/matthewsmith/Desktop/Rawlsing/R56-R04BYTEV-r2-custody-requalification-wt`
unless stated. Host macOS 13.2.1, Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2,
pandas 2.3.1.

## Startup / identity

- `git cat-file -t ea0d6f0f9` -> commit; parent `c1b0abec5`; startup
  `6d95a78bf` ancestor (`git merge-base --is-ancestor` exit 0).
- `git ls-remote --heads origin agent/rabochii-pyat-r56-r04byte-consumed-byte-custody-r1`
  -> `ea0d6f0f9840db0e33645b40ceda54456612709e`.
- Successor reviewer branch absent remotely and no successor worktree before
  creation; author worktree left at `ea0d6f0f9` untouched.
- Candidate decoder sha256 `a767b653dc119f85d11e050bc42b01dbc90ede9de28fbddbce8be0d6c6e7ce46`
  (candidate-side test file sha256 `379cca5ce1...`; sidecar sha256
  `f4ff0cd8bf...`; author r2 manifest verified against commit: 16 files,
  0 mismatches once the reviewer's added test lines are accounted for).

## Repaired author result (counterexample deselected; author-side state)

```
python3 -m pytest rawlsing_next/tests/test_universal_source_byte_custody.py -q -k 'not mmap'
24 passed, 1 deselected in 8.99s          exit 0
```

```
python3 -m pytest rawlsing_next/tests/test_universal_source_byte_custody.py \
  rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py \
  rawlsing_next/tests/test_r35_i01_physical_metadata.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py \
  rawlsing_next/tests/test_pre553_route_b_production.py \
  rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py \
  rawlsing_next/tests/test_fiabc_lm1_r1e_n1_physical_boundary.py -q -k 'not r2_mmap' -rs
SKIPPED [1] rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py:268: installed pyreadstat writer/readback does not expose missing_user_values in metadata
88 passed, 1 skipped, 1 deselected in 30.10s   exit 0
```

## Full suite including reviewer counterexample

```
python3 -m pytest rawlsing_next/tests/test_universal_source_byte_custody.py -q
1 failed, 24 passed in 8.07s             exit 1
FAILED ...::test_r2_mmap_between_batch_change_cannot_release_altered_c11_i03_under_old_identity
AssertionError: assert {'0': 0, '1': 2} == {'0': 1, '1': 1}
```

```
python3 -m pytest <8 core modules> -q -rs      # with counterexample included
1 failed, 88 passed, 1 skipped in 27.91s  exit 1
```

Counterexample repeated 3/3 runs failed. `probe_r2_mmap_fact_bypass.py` repeated
2/2 runs produced `i03_y_cells={'0':0,'1':2}`, old source artifact hash,
`signature_changed_by_mmap=false`.

## Proof integrity

```
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint rawlsing_next/tests/test_universal_source_byte_custody.py
{"state": "AST_LINT_PASS", ...}           exit 0

python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness \
  rawlsing_next/tests/test_universal_source_byte_custody.py.proof.json --root . \
  --receipt WORKER_RETURNS/.../revisions/r2/evidence/proof_witness.json
3/3 claims baseline PASS, fault_probe TARGET_ASSERTION_FAILED,
grade BOUNDED_MUTATION_DETECTED        exit 0
```

Decoder after witness: `a767b653dc119f85...` (exact candidate bytes).

## Probes (all under `evidence/`)

- `r1_probe_snapshot_path_toctou.py` / `r1_probe_metadata_and_batch_windows.py`:
  preserved reviewer r1 negative-baseline probe sources.
- `r1_negative_baseline_toctou_sav.json`,
  `r1_negative_baseline_metadata_and_batch.json`: preserved r1 failing outputs
  (old identity on replacement facts) for before/after comparison.
- `probe_r2_attack_windows.json`:
  - binding SAV/DTA: all captured reader sources `/dev/fd/N`, pathname
    replacement `observed_equals_baseline=true`, original digests, replacement
    survives close;
  - direct `seek(0)` `/dev/fd/N` digest equals source (separate check);
  - in-place pwrite before lazy: typed `DecoderError` (SAV+DTA);
  - between-batch external pwrite: typed `DecoderError`, 7 pre-change cells,
    prefix of baseline;
  - truncation: typed `DecoderError`; closed read: typed `DecoderError`;
  - DTA direct chunk on `/dev/fd`: `ReadstatError: This version of the file
    format is not supported`; DTA value pass: one `read_dta`, zero chunk calls;
  - SAV value pass uses `read_file_in_chunks`;
  - POSIX refusal: typed `DecoderError: content-bound reader path requires
    POSIX /dev/fd`;
  - cold replay SAV/DTA: changed bytes rc=1, empty stdout, restore rc=0 and
    identical payload;
  - repeated reads: first == second == third (21 cells);
  - mmap before lazy: typed `DecoderError` via full digest;
  - mmap between batches: no per-batch error, signature unchanged, altered
    cells yielded (the counterexample).
- `probe_r2_mmap_fact_bypass.json`: end-to-end C11 release + I03 fact built
  from mixed bytes: `source_artifact_ref.content_hash` = original digest,
  `i03_y_cells={'0':0,'1':2}` vs baseline `{'0':1,'1':1}`, `verify_after_attack`
  detects only after the fact.
- `probe_r2_read_shape.json`: child-process maxrss deltas SAV ~0.7–1.2 MB and
  DTA 0.78/1.9/12.5 MB at 1k/10k/50k rows (DTA O(rows) full frame).

## Inherited older failures

Author repaired-code receipt read at
`WORKER_RETURNS/PYAT-R56-R04BYTE-CONSUMED-BYTE-CUSTODY-R1/revisions/r2/evidence/`:
`10 failed, 23 passed` with the same 10 node names and messages as the r1
baseline (`representation authority variable identity/ordinal mismatch` ×7,
LOCK2 successor mismatch, physical_key mismatch, StopIteration). No new sweep
run; no concrete regression indicated.
