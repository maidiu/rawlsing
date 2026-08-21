# SR04 — B2 POSTGRES UTF-8 TRANSPORT CORRECTION GATE

Repository: `maidiu/rawlsing`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`
Accepted real B1 checkpoint: `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`
Accepted B1 checkpoint version: `SR04_NEUTRAL_CHECKPOINT_V1`

## Status

Real B2 was attempted from authorized control HEAD `5d8cc8314c4d57d2dff58c25dcc1ff1d4739485d` using accepted harness SHA-256 `d33a86ccfa4fc75916f2f24a3ca627732abc45fa29cafd15cc8ab3439836b5b4`.

The run failed closed during `POSTGRES_EPHEMERAL` materialization before a final four-candidate result existed.

Exact failure class:

`POSTGRES_EPHEMERAL_COPY_TEXT_ENCODING_FAILURE__NO_CARRIER_DISPOSITION`

Observed error:

`COPY from stdin failed: error in .read() call: UnicodeEncodeError 'ascii' codec can't encode character '\u2013'`

The accepted B1 checkpoint remained byte-identical. No raw source decode occurred in B2. No carrier selection is admissible from the failed run.

## Diagnosis

This is not a source-reader encoding problem and does not reopen the LiTS/EVS compatibility-decoding law.

The source-reader layer has already produced Unicode strings and the accepted neutral checkpoint is authoritative for SR04 carrier testing.

The failure occurs later in the disposable PostgreSQL candidate transport path.

The harness initializes the ephemeral PostgreSQL cluster with:

`--locale=C`

but does not explicitly set database encoding. Under this environment PostgreSQL/psycopg2 can expose an ASCII/SQL_ASCII text path, causing the text `COPY` stream to fail on valid Unicode such as U+2013 EN DASH.

Binding distinction:

- source compatibility decoding may lawfully use `latin1` for exact hash-bound legacy source files;
- the neutral checkpoint and candidate stores must preserve the resulting Unicode without loss;
- no conversion of the checkpoint or candidate payload to Latin-1 is authorized.

## Frozen correction

Modify only the PostgreSQL candidate transport mechanics so that:

1. ephemeral `initdb` retains `--locale=C`;
2. ephemeral `initdb` explicitly sets database encoding UTF-8 (`--encoding=UTF8` or exact equivalent);
3. after connection, the client encoding is explicitly UTF-8;
4. before COPY, the harness verifies PostgreSQL `server_encoding = UTF8` and `client_encoding = UTF8`;
5. the existing text COPY path must round-trip Unicode exactly;
6. candidate query/oracle/replay/timing/index/budget/selection semantics remain unchanged.

No source decoder, checkpoint, query, candidate set, timing law, disk law, selection law, or non-PostgreSQL candidate behavior may change.

## Required cheap proof before B2 retry

Do not run real B2 while implementing this correction.

Add a tiny synthetic PostgreSQL transport proof using the exact corrected cluster-init/connect/COPY mechanics.

It must COPY and read back exactly these Unicode strings at minimum:

- `en–dash` (U+2013)
- `café` (Latin-1-representable non-ASCII)
- `Ж` (Cyrillic; not Latin-1)
- `م` (Arabic; not Latin-1)

The proof must establish:

- `postgres_server_encoding = UTF8`
- `postgres_client_encoding = UTF8`
- `unicode_copy_roundtrip_exact = true`
- `en_dash_roundtrip = true`
- `latin1_range_roundtrip = true`
- `non_latin1_cyrillic_roundtrip = true`
- `non_latin1_arabic_roundtrip = true`
- `DATABASE_URL_unused = true`
- disposable PostgreSQL lifecycle stops cleanly
- no raw source decode
- no checkpoint mutation
- no carrier court execution

Required token:

`PRE553_SR04_POSTGRES_UTF8_TRANSPORT_PROOF_PASS`

## Publication law

Codex may modify only:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py`

After the cheap proof passes:

1. syntax/static check;
2. verify that only the harness changed;
3. commit only the harness;
4. commit message: `Fix SR04 PostgreSQL UTF-8 transport`;
5. push the control branch;
6. return exact new harness HEAD, harness SHA-256, proof command, proof receipt/token, final git status, pushed branch HEAD;
7. STOP.

Real B2 retry requires separate HQ authorization after static review of the committed correction.

## Forbidden

Do not:

- rerun B1;
- alter or regenerate `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`;
- decode WVS7/LiTS I;
- convert checkpoint text to Latin-1;
- use `DATABASE_URL` or live Rawlsing PostgreSQL;
- run the four-candidate court during the cheap proof;
- change any non-PostgreSQL candidate semantics;
- treat the failed B2 attempt as carrier evidence.
