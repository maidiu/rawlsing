# ANVIL routing 10k/5-role F2 oracle

## Result

**Pins concrete.** This is a read-only truth pin for the exact forward/reverse F2 operations on the retained sourcefree 10k/5-role estate. No query, build, fixture construction, product edit, or full review replay was performed.

## Fixture identity

- Fixture: `PYAT-1006-SCALE-10K-20261118`
- Respondents: `10000`; questions: `5`
- Estate manifest SHA-256: `e192dc25e55528101b6116f81aa7bce49c170a9a72f61386e97d20a9f9e09619`
- Estate: `MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118/EXECUTION/.local-data-10k/releases/0bcf5d40882ac09fc4cd7083c20d2ce32763e64dcd428f387e6da27b80391aad`
- Release: `C11LogicalRelease|REL-PYAT-1006-SCALE-10K-20261118|e8f79a13bbc8aea3fb8a5d647fb677dc1f434f5509c145e1d93e858ff09e31fe`
- Universe: `EmpiricalUniverse@1.0.0|...:126a42ee320ac089d43272a0e5413f8d74cbcede7ac181b5b2e41c55298023c8|...`
- Accepted truth correction: `55d2239e9ea98b3e47aa02a7969cb21c0624115e`

## Operation pins

### `f2_forward_raw`

- Risk refs: **10,000**, ordered payload hash `27aa0694c1d18c0ede9a60e5ca7db6db78b2a4f52623b047b80eb3d736dbf34d`; expected set hash identical.
- Denominator refs: **5,000**, ordered payload hash `4f87ca252fa67e21fcdebe29a3d6e65d22ccea752a1dba7fa69fbf6518777b17`; expected set hash identical.
- Cells: `0=3333 OBSERVED_POSITIVE`; `1=1667 OBSERVED_POSITIVE`; raw numerator/denominator **5000/5000**; typed state `SUPPORTED`.
- Fact: `EmpiricalFact@1.0.0|urn:rawlsing:pre553:EmpiricalFact:sha256:d7009e0b440ebe2ce609d3588f2fff2076eed78501295adf2e590e535821ce09|d7009e0b...`; canonical fact SHA-256 `25593d4f520dbce843765103da3ca790ba5c3515d1230491b20ded0f674d15db`; payload file SHA-256 `f86668fd138aabb774fe8703966a0a29984a3c2fcd0a5aaf7748661ef1ee741b`.
- Replay: `PRE553_I03_QUERY_REPLAY|...:7a7be0dfaaeba2884b4455253ac368337bcf0ec708bd9e31f1c39ec682d3fc9d|...`.
- Query: `EmpiricalQuerySpec@1.0.0|...:9385ea71ee06bdf74e5e5812c1c30d5ec148f9a11333f4e79e79f0e1a1d15ea6|...`.
- Predicate: `EmpiricalPredicate@1.0.0|...:86afb73dd021aee092729c48173a13dae5ca929efaba128f7001f4f1e0466345|...`.
- Provenance: **25,003** refs, canonical SHA-256 `e4eae355e347d0c32b28a4b1ebd7c619bee619387cd6219a6dc31fe379cef092`.

### `f2_reverse_raw`

- Risk refs: **10,000**, ordered payload hash `27aa0694c1d18c0ede9a60e5ca7db6db78b2a4f52623b047b80eb3d736dbf34d`; expected set hash identical.
- Denominator refs: **3,333**, ordered payload hash `e481b104767b2a23a2942123ae5865e0416b78bc5d7f12883dec0bfad1730417`; expected set hash identical.
- Cells: `0=1666 OBSERVED_POSITIVE`; `1=1667 OBSERVED_POSITIVE`; raw numerator/denominator **3333/3333**; typed state `SUPPORTED`.
- Fact: `EmpiricalFact@1.0.0|urn:rawlsing:pre553:EmpiricalFact:sha256:720a158498d583f1c94285c664cb571e91d68f626b49898ba9a68328140dca1d|720a1584...`; canonical fact SHA-256 `96db45da1e205f0e62d4b3d624a4285a60df9054dceb4b2f2ccb54d339f7cfd7`; payload file SHA-256 `f06e9a0a54da90a4d034590f70fbe1b857c9e3764902a3197a60076b593d7771`.
- Replay: `PRE553_I03_QUERY_REPLAY|...:d3d12648b7c259d6f807466ad7f9a27f9404608e66cf654b86f9365752c27ed6|...`.
- Query: `EmpiricalQuerySpec@1.0.0|...:08e2491f771f905f81dc8dc9006151b6e3eb154fa362f9709daeef173fc8d92e|...`.
- Predicate: `EmpiricalPredicate@1.0.0|...:ac7b04a76883d2f39b332564731b0cf3b075f56dcaac4e9d86f828ea0ede149d|...`.
- Provenance: **23,336** refs, canonical SHA-256 `636c6458eb1141234d1e8385772a81e0cfc125c83e00f384e7c1dd7dba895669`.

The ordered risk/denominator arrays are the exact earlier payload order and match the accepted `ACTUAL_SETS` order. The accepted `EXPECTED_SETS` arrays are set-equal but may be ordered differently because they are pattern-derived; the checker therefore requires **payload order** for ordered identity and **set equality** against expected.

## Pinned sources

- Accepted truth review receipt: `OWNER/WORKER_RETURNS/ANVIL_ENGINEERING_TRUTH_CORRECTION_G5_20261118/REVIEW_RECEIPT.json`, SHA-256 `070c97c6f48c187ef7b3b78cab6cfaa9672c9c50e993be849216910b55bddc8a`.
- Accepted `EXPECTED_SETS.json.gz`: SHA-256 `4b199527567c8dcd0cdc12736d6a974a0289a5a31322b72ff2eb53ddcfdb09ed`.
- Accepted `ACTUAL_SETS.json.gz`: SHA-256 `77ba3751db2ceea2f26f4b4e6c2dd408ebf965a83b902347a5cda8013b44179d`.
- Semantic `RESULT.json`: SHA-256 `aaa676323c41934f5df2e7135f95fc981967201da9b5203de9069cf0b1924156`.
- `EXPECTED_TRUTH.json`: SHA-256 `2d358038a6133623c9c6cafa544d9e2c4d1a54ef4dff4fe9cb5a4188fdbf6952`.
- Forward payload: `.../SEMANTIC_CLOSURE/f2_forward_raw.payload.json.gz`, SHA-256 `f86668fd138aabb774fe8703966a0a29984a3c2fcd0a5aaf7748661ef1ee741b`.
- Reverse payload: `.../SEMANTIC_CLOSURE/f2_reverse_raw.payload.json.gz`, SHA-256 `f06e9a0a54da90a4d034590f70fbe1b857c9e3764902a3197a60076b593d7771`.

## Offline checker

`check_10k_f2_oracle.py` reads only `ORACLE_PINS.json.gz` and a forthcoming matched-output JSON. It does not import product code or execute a query.

```bash
python3 check_10k_f2_oracle.py --input /path/to/candidate.json --verify-sources
python3 check_10k_f2_oracle.py --self-test --verify-sources
```

Statuses distinguish:

- `PASS`
- `MISMATCH` (value/set mismatch)
- `ORDER_MISMATCH` (set exact, ordered refs differ)
- `MISSING_OUTPUT_FIELD` (field absent from the forthcoming output)
- `MISSING_PRIOR_EVIDENCE` (pins or pinned source absent/hash-invalid)

Evidence: `selftest.txt` (SELFTEST_PASS with all source hashes), `positive-prior-check.txt` (offline prior payload reconstruction PASS), `missing-prior.txt`, `mismatch.txt`, `missing-field.txt`.

## Limits

This pin covers only the exact two F2 operations on the retained 10k/5-role sourcefree estate, using earlier controlled fixture truth. It is not a new native run, a full matched performance measurement, survey width, 100k, production, protected, or science claim. The physical payload fact and member sets are pinned; no end-to-end timing is implied.
