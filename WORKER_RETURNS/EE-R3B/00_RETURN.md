# EE-R3B — LiTS D03 EXACT ROOTS / REPLAY — governed return

Status: `PASS__EXACT_ACCEPTED_DECODER_R2_R7_R27_EXTENSIONS_ROOTS_TYPED_ACCOUNTING_AND_REPLAY_FROZEN`

Worker: `EE-R3B`  
Branch: `agent/rabochii-prev3-ee-r3b-lits-d03-roots-replay-r1`  
Commission tip: `61fcf0135f71c3c37424af5a6756142ced891333`  
Exact grain: `PSC04_LITS_I_ACCEPTED_DECODER_EXACT_R2_R7_R27_EXTENTIONAL_ROOT_MATERIALIZATION_AND_REPLAY_ONLY`

## Canonical HQ authority

Current control-branch `HQ_HANDOFF/LATEST.json` resolves to sealed checkpoint `20260916T1214-0400 @ d24f377f2fb4bcf7d7e2a29941a925b983e42f42`; semantic PRE-MAIN remains `1dcd2a79dd6d4208738f655ab7fe4e71c219e354`.

That checkpoint activates EE-R3B at this exact branch/tip and preserves `EXACT_ONLY` Library authority for only `file_0000000036dc81f8b8b546e356590a03`, version `1`.

Binding predecessors consumed:

- EE-W2/D03 blocker/contract `4523f1ea392abbd3a500e3459fef176607d790b4`;
- EE-R2B co-location PASS `485c0424337ae49b4ed6512b7030716e11cb81e0`;
- N02 identity/materialization law `a06e49fa5ccaa29bd757663c3ca9cf088d963b74`;
- K03 q301 target/risk authority `9c765641a0c1c32c1becbc308feec488c136c30d`.

No post-checkpoint sibling return was required.

## Exact source and accepted decoder/runtime

Only the commissioned Library carrier was materialized:

- file id `file_0000000036dc81f8b8b546e356590a03`;
- version `1`;
- `LITS-2006-data.dta`;
- bytes `139531180`;
- SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`.

The executed decoder was exactly:

- `rawlsing_next/pre553_physical_decoder.py`;
- Git blob `13aa733b511dc23e00bfcdf288c5b920e3f09983`;
- locally reconstructed byte-for-byte from repository content and verified with `git hash-object` to the same blob;
- local file SHA-256 `6ca15efcb6df4cdfd91c0592ae771f6e9e463546c9ff826670909c6306cd1e02`;
- `encoding="latin1"`;
- `apply_value_formats=False`;
- `user_missing=True`.

The EE-R2B runtime-to-carrier path was reproduced exactly:

- R2B workflow run `35120057454`;
- artifact id `10456488840`;
- downloaded artifact ZIP SHA-256 `ccf5a7236142f1c763fae5016adca5b662bf6a6550a150c50b44d02ff84b1225`;
- pinned wheel `pyreadstat-1.3.6-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl`;
- wheel SHA-256 `3ac231771dc038e0a42a4d14599af3112684f7eba680983b3ef9581db3e3b163`;
- installed with `--no-deps`;
- imported runtime `pyreadstat 1.3.6` under CPython `3.13.5`.

No source substitution, decoder substitution, public/mutable mirror, or pandas decode fallback occurred.

## Two accepted-decoder executions

The accepted decoder was executed independently twice against the exact same carrier. Both runs produced:

- source format `DTA`;
- rows `29002`;
- variables `1198`;
- physical-cell surface `34744396`;
- `q301_2` variable ordinal `194`;
- `q301_7` variable ordinal `199`;
- reader `pyreadstat 1.3.6`;
- exact source SHA match.

Frozen record identity remains exactly:

`(exact source SHA-256, one-based source row ordinal)`

Native `id` is not promoted to cross-release/person identity.

## Exact extensional roots

### R2 — q301_2 native states 1..5

- member count: **24897**;
- canonical full member-coordinate TSV SHA-256: `f224533ce0a705bf0839e6bb40bd49dec0c8366e5a5ede0a389e3e67811a13b3`;
- run 2 root: identical.

Complete 29,002-row K03 accounting:

- `DENOMINATOR_MEMBER`: `24897`;
- code `6` / `SOURCE_SPECIAL_NOT_APPLICABLE` / authorized pre-query exclusion: `1774`;
- code `7` / `TYPED_MISSING_NONRESPONSE_DONT_KNOW` / authorized pre-query exclusion: `2327`;
- physical/system missing / reason unspecified / authorized pre-query exclusion: `4`;
- other unauthorized state: `0`.

Full typed-accounting TSV SHA-256: `6b2a87706c8f3a2f3586bc7e6e6348e45bdbe09cb4c94a238795936570c0d16d`; run 2 identical.

### R7 — q301_7 native states 1..5

- member count: **28325**;
- canonical full member-coordinate TSV SHA-256: `0978bd4d87afd88831593ca5977fa9978948d598bf981adfd7fd96ceab979844`;
- run 2 root: identical.

Complete 29,002-row K03 accounting:

- `DENOMINATOR_MEMBER`: `28325`;
- code `6` / `SOURCE_SPECIAL_NOT_APPLICABLE` / authorized pre-query exclusion: `224`;
- code `7` / `TYPED_MISSING_NONRESPONSE_DONT_KNOW` / authorized pre-query exclusion: `442`;
- physical/system missing / reason unspecified / authorized pre-query exclusion: `11`;
- other unauthorized state: `0`.

Full typed-accounting TSV SHA-256: `a726aaf84979b90b0a5d80a6bca233aaabf1c5ea45d5077bcaa0235b890a8470`; run 2 identical.

### R27 — exact R2 ∩ R7

R27 was derived mechanically from the accepted-decoder R2 and R7 member-coordinate extensions, not inherited from the old pandas diagnostic.

- exact accepted-decoder-derived member count: **24630**;
- canonical full member-coordinate TSV SHA-256: `f9c87f610bcaf0539cc91e7f2608b230cea39d806d3611d6a398519a86386d29`;
- run 2 root: identical.

The fact that this fresh accepted-decoder result is numerically equal to the previously quarantined pandas diagnostic is observational only. Authority comes from this accepted-decoder derivation and replay.

## Canonical extension publication

`01_EXTENTIONAL_ROOTS_AND_TYPED_ACCOUNTING.json` plus the ordered `04_EXTENSION_PAYLOAD_B64_PART_*.txt` files publish the exact coordinate extensions losslessly in one compact payload. R2 and R7 each use a 2-bit-per-row state vector across all 29,002 one-based source ordinals (`0=DENOMINATOR_MEMBER`, `1=code 6 Not applicable`, `2=code 7 Don't know`, `3=physical/system missing reason unspecified`); R27 uses a one-bit membership vector. The fixed-layout 18,128-byte payload is zlib-level-9 compressed, Base64-encoded, and SHA-256 bound before and after compression. R2/R7 member extensions are exactly the rows carrying state code `0`; thus the same bytes freeze both complete typed accounting and exact member coordinates.

The canonical roots above do **not** hash the compact payload encoding. They hash the fully expanded UTF-8 TSV coordinate stream:

`source_sha256<TAB>one_based_source_row_ordinal<LF>`

with a fixed header and ascending row ordinal. A reconstruction audit decompressed the committed payload, reconstructed R2/R7/R27 extensions, and reproduced all three canonical full-TSV roots exactly; partition checks prove each target accounts for all 29,002 rows exactly once and that R27 equals the exact R2∩R7 member intersection. This is a serialization of the already-frozen identity coordinate, not a new identity scheme.

## Replay identities

Run-identity receipt SHA-256:

- run 1: `b6c397f93a2dbcac3b37899b74bfd668b443116c19457342e373507a68c82e2d`;
- run 2: `b6c397f93a2dbcac3b37899b74bfd668b443116c19457342e373507a68c82e2d`;
- parity: **EXACT**.

The identity receipt excludes observational wall-clock timing but binds source, decoder, runtime/config, decoded shape, identity law, exact root counts/hashes, and typed-accounting hashes.

Raw per-run receipts differ only in run identifier/observational timing and have SHA-256:

- run 1: `d70d2bb9fdddfe9f32d16f8ad734dde54e4d1eb4009d3c2aa93c8b73237ec3fa`;
- run 2: `78b403fc1abde47bd683a25cc29b1e5cea32e7f961bff0637fa9ea0ebc95d33f`.

## Governed artifacts

- `WORKER_RETURNS/EE-R3B/00_RETURN.md`
- `WORKER_RETURNS/EE-R3B/01_EXTENTIONAL_ROOTS_AND_TYPED_ACCOUNTING.json`
- `WORKER_RETURNS/EE-R3B/02_REPLAY_RECEIPT.json`
- `WORKER_RETURNS/EE-R3B/03_SOURCE_EXECUTION_RECEIPT.json`
- `WORKER_RETURNS/EE-R3B/04_EXTENSION_PAYLOAD_B64_PART_01.txt`
- `WORKER_RETURNS/EE-R3B/04_EXTENSION_PAYLOAD_B64_PART_02.txt`
- `WORKER_RETURNS/EE-R3B/04_EXTENSION_PAYLOAD_B64_PART_03.txt`

Artifact source SHA-256 before Git publication:

- `01_EXTENTIONAL_ROOTS_AND_TYPED_ACCOUNTING.json`: `9079a65053190850ca5081689dfc5668f81ec9ac9abeaaefa23f099761f1a46b`;
- `02_REPLAY_RECEIPT.json`: `4df58d5c78fc437ef1e4e54217c549e5414d85c7ad16b1c144cd3f2567b9239b`;
- `03_SOURCE_EXECUTION_RECEIPT.json`: `c2c214519c799d758a89a9dba13d607b1287c332f1581369db1d4217983a8d8d`.
- `04_EXTENSION_PAYLOAD_B64_PART_01.txt`: `06462ccd2237207ccb3081c1db4617b33d5c721ec5aba8ccbbb363cbb3cb1fd4`.
- `04_EXTENSION_PAYLOAD_B64_PART_02.txt`: `50bf96e1b0dd9dcf25b35b3405647d4d9b545e82a8524ab355d492135ce88193`.
- `04_EXTENSION_PAYLOAD_B64_PART_03.txt`: `bcc0a54f40b02ba1e8e100b2fab63fe251b60100a5eddd813ca59a07f2a06c86`.

## Boundary audit

- learned discovery/outcome execution: `NONE`;
- A/B/C execution/ranking: `NONE`;
- structural admission: `NONE`;
- person/V3 state: `NONE`;
- denominator repair after outcomes: `NONE`;
- predictor-missingness rule invention: `NONE`;
- new identity scheme: `NONE`;
- source substitution: `NONE`;
- decoder substitution: `NONE`;
- pandas decode fallback: `NONE`;
- MAIN mutation: `NONE`;
- semantic PRE-MAIN mutation: `NONE`.

## Successor wake

**PASS closes the LiTS D03 exact extensional-root/replay blocker.** D04 may wake after HQ adoption of this exact return. The exact LiTS R2/R7/R27 premises are now available to the selection-critical A/B/C positive-executability work without importing the quarantined pandas derivation as authority.

Terminal:

`EE_R3B_PASS__LITS_D03_R2_R7_R27_EXACT_ACCEPTED_DECODER_EXTENSIONS_ROOTS_TYPED_ACCOUNTING_AND_REPLAY_FROZEN__D04_WAKE_AFTER_HQ_ADOPTION`
