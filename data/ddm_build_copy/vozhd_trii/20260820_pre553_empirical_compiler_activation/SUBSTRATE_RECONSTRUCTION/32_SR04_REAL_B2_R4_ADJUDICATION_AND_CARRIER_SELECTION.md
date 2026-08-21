# SR04 — REAL B2 R4 ADJUDICATION AND PHYSICAL CARRIER SELECTION

Status: `ACCEPTED__G_SR04_CLOSED__PARQUET_DUCKDB_DIRECT_SELECTED`

Repository: `maidiu/rawlsing`

Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

Authorized launch HEAD: `3469e21b5d9f298a0e65983f2043891a6e2b87cd`

Accepted harness implementation: `e249f809f194cb369bf08094ac2cbf4c2d1fcd43`

Accepted harness SHA-256: `e1aa6deaeedf7fb2bbb68c6019e791363e8ad10dcf492087b32a221959e90211`

## 1. R4 execution adjudication

HQ accepts the exact executor return for REAL B2 R4.

Execution completed with exit code `0` using checkpoint-only `--stage-b2`, no `--source-root`, no raw-source decode, no live Rawlsing database path, and required token:

`PRE553_SR04_CARRIER_BAKEOFF_RECEIPT_COMPLETE`

The accepted B1 checkpoint preflight matched all six frozen file identities and total `114705938` bytes before execution and remained byte-identical afterward.

All four candidates returned `MEASURED_CORRECT`.

For all four candidates:

- canonical Q00-Q15 oracle comparison passed;
- stored relation replay comparison passed;
- deliberate wrong-oracle negative test passed;
- stored-corruption negative test passed.

PostgreSQL used the accepted disposable UTF-8 lifecycle and stopped cleanly. The server/client encoding assertions executed in the accepted harness although the final package did not serialize those values.

`DATABASE_URL_unused=true` and raw-source decoding was false.

## 2. Accepted measurements

| candidate | disposition | batch seconds | persistent disk bytes | peak RSS bytes |
|---|---|---:|---:|---:|
| `PARQUET_DUCKDB_DIRECT` | `MEASURED_CORRECT` | `0.4734193090` | `16881380` | `1997832192` |
| `DUCKDB_NATIVE` | `MEASURED_CORRECT` | `0.4626857310` | `63451136` | `4064673792` |
| `POSTGRES_EPHEMERAL` | `MEASURED_CORRECT` | `5.77611619799` | `1553857745` | `4680519680` |
| `SQLITE` | `MEASURED_CORRECT` | `4.9855595440` | `705019904` | `4113063936` |

Local final result directory reported by the executor:

`/private/tmp/SR04_B2_R4_CARRIER_BAKEOFF_RESULTS`

Deterministic ZIP:

- path: `/private/tmp/SR04_B2_R4_CARRIER_BAKEOFF_RESULTS.zip`
- bytes: `21515`
- SHA-256: `ec26b4f6e9d88f9ffa9e7e9da400cf542b7d8b1bf64b5deb4035e51d9a0624c4`

The local execution package contains the exact required nine files:

- `RECEIPT.json`
- `ENVIRONMENT.json`
- `FIXTURE_MANIFEST.json`
- `FIXTURE_DIGESTS.json`
- `QUERY_ORACLE.json`
- `CANDIDATE_RESULTS.json`
- `PROVISIONAL_SELECTION.json`
- `STDOUT.txt`
- `STDERR.txt`

Execution outputs remain local evidence and are not committed as production runtime.

## 3. Binding selection law

The frozen court orders:

`FLAWLESS_EFFECTIVENESS -> SPEED -> <=10% SPEED TIE -> LIGHTNESS`

All four candidates satisfy the correctness prerequisite, so performance becomes dispositive.

`DUCKDB_NATIVE` is the raw fastest batch at `0.4626857310 s`.

`PARQUET_DUCKDB_DIRECT` is `0.4734193090 s`, only approximately `2.32%` slower than the fastest result. It therefore falls inside the frozen `<=10%` operational speed tie.

The tie is resolved by lightness.

Compared with `DUCKDB_NATIVE`, `PARQUET_DUCKDB_DIRECT`:

- uses `16881380` versus `63451136` persistent bytes, about `3.76x` less disk for the measured candidate;
- uses substantially lower measured peak RSS (`1997832192` versus `4064673792` bytes);
- requires no persistent DuckDB database copy in addition to the canonical Parquet relations;
- requires no background database service.

No measured capability or speed benefit justifies the heavier native-DuckDB copy under the frozen court law.

## 4. Final carrier ruling

Selected physical carrier:

`PARQUET_DUCKDB_DIRECT`

Binding physical role:

- canonical persistent empirical relations are immutable/content-addressed Parquet;
- embedded DuckDB is the direct analytical/query engine over those Parquet relations;
- a DuckDB database file is not canonical empirical authority;
- PostgreSQL and SQLite receive no primary C11 carrier role from SR04;
- nonauthoritative derived caches remain separately governed and may not become a second empirical truth source.

This ruling selects persistence/query machinery only. It does not alter I01-I07, M01-M18, source semantics, source authority, I03/I05/I04 truth conditions, or V553-V558 semantics.

## 5. Gate disposition

`G-SR04 = ACCEPTED`

Closure token:

`PRE553_SR04_PARQUET_DUCKDB_DIRECT_CARRIER_SELECTED`

The SR04 execution harness is now historical/verification machinery. No further carrier bakeoff execution is authorized absent a new HQ reopening authority.

G-SR06 is unblocked because both G-SR04 and G-SR05 are accepted.
