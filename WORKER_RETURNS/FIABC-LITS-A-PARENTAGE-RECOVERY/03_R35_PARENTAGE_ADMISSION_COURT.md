# FIABC LiTS-A Preserved First-Build — R35 Parentage Admission Court

## Disposition

`HISTORICAL_E8F37557_PARENTAGE_NOT_ADMISSIBLE_FROM_BROWSER_PERSISTED_EVIDENCE`

The preserved LiTS-I Candidate-A first-build is genuine historical build evidence. It is not, on the evidence persisted in Git/GitHub, a complete generic R35 derivative-parentage chain.

This court does **not** authorize a rebuild.

## Governing R35 law

The generic R35-I02 chain is:

`DERIVATIVE IDENTITY -> GOVERNED PRODUCER / OPERATION / CONFIG -> IMMUTABLE EXTERNAL PARENT RECEIPT -> CANONICAL SOURCE SHA`.

The inverse is forbidden:

`derivative embeds/asserts canonical source SHA -/-> derivative descended from those source bytes`.

The live LiTS-A consumer additionally requires an independently supplied:

- preserved R5 root;
- external `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0`;
- exact independently pinned derivative-receipt identity.

Path, shape, row count, internal source SHA, root self-consistency, or reproduction of the same root elsewhere are not substitutes.

## Exact historical derivative

The governed post-Lock2 first-build commit is:

`02a7ff71ae65b1aa8c52add0b315244a9eaea9df`.

The first-build receipt freezes:

- source: LiTS-I;
- source SHA: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- physical root: `e8f37557493b816e4562f5f47df110cf49b429e9ead54e5b624d6638ee07aa3d`;
- canonical rows: 34,745,595;
- final shards: 2,121;
- logical stream digest: `de8f060aa72eff7e45f8355ed683cb8ee4b6aca7ff255167cb41bcf8e5a7e3d6`;
- projection: `84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872`;
- C11 release: `e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`;
- replay: `6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd`;
- runtime: Darwin x86_64 / CPython 3.11.3 / pyreadstat 1.3.6 / pyarrow 25.0.1;
- raw first-build receipt SHA-256: `89bd0719f0c546bc3e6e0d3ef7678c01c3fb3ab51cf0c82c84f9a343e08d5337`.

The commit itself added only:

1. `00_EXECUTION_BINDING.json`;
2. `00_RETURN.md`;
3. `01_LITS_I_A_FIRST_BUILD_STAGE.json`.

No external source-verification receipt and no external derivative-parentage receipt were committed with that build. The commit has no GitHub Actions run whose artifact could supply such a receipt.

## Admission matrix

| R35 requirement | Browser holding | Basis |
|---|---|---|
| canonical source identity/SHA | **PROVED** | first-build receipt + current canonical source estate |
| historical derivative identity | **PROVED** | exact `e8f37557...` root + rows/shards/logical stream |
| source observation occurred in first build | **STRONG PARTIAL** | exact source SHA, bytes, source-open/decode counters and fresh-build status are contemporaneous |
| immutable source-verification receipt identity | **NOT PROVED** | none persisted with first build; execution binding is not the R35 source receipt |
| exact reader/config | **PARTIAL** | pyreadstat 1.3.6 + `decode_dta(..., encoding=latin1)` known; full sealed current R35 reader-config object not contemporaneously bound |
| exact builder identity/class | **PROVED LATER** | authoritative class is `R5CompactLongShardedBuilder` |
| exact builder Git blob used by first build | **NOT PROVED** | historical first-build receipt does not bind it |
| complete build configuration | **NOT PROVED** | root/build config is not externally sealed into the historical receipt chain |
| exact derivation operation | **PARTIAL** | fresh absent-target R5 first-build is contemporaneous; generic R35 operation receipt absent |
| derivative receipt parented to source receipt | **NOT PROVED** | required cryptographic edge absent |
| current ownership/currentness | **NOT PROVED** | local derivative availability/bundle not browser-observable; current live producer pin also conflicts with qualified builder object |

Therefore the generic R35 admission predicate does not close.

## Why nearby evidence does not repair the edge

### R10L

R10L built the same `e8f37557...` physical root and same `de8f...` logical stream from the same canonical LiTS-I source. Its script hashes the source before decoding.

That is powerful determinism/corroboration evidence. It is a pre-P2 calibration execution and cannot retroactively become the P2X first-build parent receipt.

`same deterministic output -/-> exact historical ancestry receipt`.

### P2R6O

P2R6O freezes the accepted Candidate-A owner blob:

`d4915e7e6755ba1850756aebff72f982f73a332b`

and preserves the historical first-build stage without rerunning it. It also freezes the current runtime catalog, active binding, and runtime release.

P2R6O performed no source/library access and did not create the missing source-to-derivative parentage edge.

### P2R6X

P2R6X guarantees that stopped-ledger reconciliation must leave LiTS-A S00/S01 preservation and durable transformed/external carriers untouched.

That is preservation law, not proof that the exact historical root still exists at the present local path, and not an ancestry receipt.

### LM1-R1A

LM1-R1A independently inspected fourteen historical evidence candidates and reached:

`HISTORICAL_R5_PARENTAGE_NOT_PROVED`.

Its missing links are the same links found here: contemporaneous builder blob/config, source-receipt identity, derivative receipt, and currentness closure.

### LM1-R1C

LM1-R1C later created a valid generic R35 source receipt and derivative bundle, but for replacement root:

`7d85c5e4c3a91c3f6dc8f7896fe487cda116fc8cf67f0ab263a2654ff938afcd`.

Its bundle `8b63de4e...` and derivative receipt `dbfe6014...` cannot be applied to historical root `e8f37557...`.

Doing so would replace an exact derivative identity with another derivative's ancestry.

## Current producer-pin conflict

There is also a separate current consumer defect.

The qualified owner commit:

`0b96b8de9aac774566f872cf0630ebd4ddeb70e6`

contains `rawlsing_next/pre553_r5_compact_carrier.py` at Git blob:

`92e364b31eaf27be1bca2081eff65f6ffb779c3d`.

The live backend at the exact common base instead pins:

`92e68693d72cbfcdd1c6d16e7f247ca3f60c8c55`.

LM1-R1A independently classified that live value as stale/malformed and found no accepted succession displacing the qualified builder object.

This court does not modify that live pin. It records it because a recovered historical receipt naming the qualified builder would still fail the current consumer until the exact producer pin is separately reconciled.

## Current preserved-work classification

Primary classification:

`DERIVATIVE_PRESENT_BUT_CURRENTNESS_UNPROVED`

Meaning:

- a governed historical derivative with exact identity is proved to have existed;
- court law continues to preserve that completed stage;
- browser evidence does not prove that the exact local root and all required independent historical evidence survive now;
- no browser-persisted generic R35 parentage bundle closes the historical derivative to its source.

T4's stricter accounting classification remains:

`PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY`.

No historical numeric P2 credit is promoted by this court.

## Admission result

`R35_PARENTAGE_ADMISSION = FAIL_CLOSED_PENDING_MINIMAL_LOCAL_PRESERVED_ARTIFACT_VERIFICATION`.

The local fallback is limited to locating and hashing already-preserved first-build artifacts. It may not reopen LiTS raw source bytes and may not rebuild 34,745,595 rows.
