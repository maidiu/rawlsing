# FIABC-LM1-R1C return

Terminal: `FIABC_LM1_R1C_BLOCKED__NEW_NONMECHANICAL_ADJUDICATION_REQUIRED`

The exact LiTS-I source was verified and one fresh Candidate-A R5 physical carrier was built, fully audited, parentage-sealed, and tested through the current source-free consumer path. The work is blocked only at the accepted physical-to-C11 semantic boundary; no semantic conversion was invented.

## Identity and ancestry

- Exact base: `7e33b76c7d46dcee31dd3be7b3b0230f3c18a152`
- Branch: `agent/rabochii-premain-fiabc-lm1-r1c-governed-r5-rebuild-r1`
- Mechanical repair commit: `1508ec9b`
- LiTS-I source: `/Users/matthewsmith/Desktop/Rawlsing/data/Data/LiTS_I.dta`
- Source bytes/SHA-256: `139531180` / `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- Decoder: `decode_dta(..., encoding="latin1")`; compatibility execution only
- Fresh carrier: `/tmp/fiabc_lm1_r1c_lits_a_r5_replacement_r1`
- Final physical root: `7d85c5e4c3a91c3f6dc8f7896fe487cda116fc8cf67f0ab263a2654ff938afcd`
- Final logical stream: `076c6527f292c1d4ae2cce53c1f0363093eb9a5b5fb652edd96b448823589aba`
- Rows/members: `34745595` / `2121`

The mechanical repair added `CANONICAL_SOURCE::<source SHA>` to the R5 release `source_artifact_ref.object_id`, as required by the accepted Candidate-A adapter. It changed only the root manifest identity; members, row count, source bytes, and logical stream were unchanged.

## Qualification evidence

- Final single-pass full audit: PASS.
- Generic R35 parentage bundle: PASS; bundle `8b63de4ea902350ce197bc3ed49b59259bef2ad400c9f3c7db65ac96b015ace7`.
- Required compile/import and regression ledger: PASS; see `08_TEST_LEDGER.csv`.
- Old preserved R5 numeric credit remains `0`; the new physical build is `EXECUTED_NOW` but was not consumed as a successful replacement.

## Exact blocker

The current accepted `_compose_lits` Candidate-A admission completed R5 physical validation, then failed at `physical_value_binding_key` because `pre553_empirical_objects.canonicalize` raises `Pre553IntegrityError: float/NaN/Infinity forbidden in semantic identity`. The R5 codec intentionally preserves exact float/non-finite physical lanes, and no accepted authority specifies a lossless conversion or missingness reinterpretation at this boundary. Resolving that requires semantic/authority adjudication.

Therefore the carrier is not marked successfully sealed or numerically consumed, and the required terminal is:

`FIABC_LM1_R1C_BLOCKED__NEW_NONMECHANICAL_ADJUDICATION_REQUIRED`

## Preserved boundaries

No WVS7 source, Candidate B/C execution, I03/I05, measured P2X, or semantic certification was run. The pre-existing untracked `.DS_Store` and generated `__pycache__` entries were left untouched; the carrier remains outside Git.
