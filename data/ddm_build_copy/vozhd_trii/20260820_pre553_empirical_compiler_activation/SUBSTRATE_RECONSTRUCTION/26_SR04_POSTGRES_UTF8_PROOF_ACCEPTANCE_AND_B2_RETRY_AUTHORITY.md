# SR04 — POSTGRES UTF-8 PROOF ACCEPTANCE AND REAL B2 RETRY AUTHORITY

Repository: `maidiu/rawlsing`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

## Accepted state

The real B1 checkpoint remains ACCEPTED and immutable at:

`/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`

The first real B2 attempt from control HEAD `5d8cc8314c4d57d2dff58c25dcc1ff1d4739485d` is NON-ADMISSIBLE carrier evidence because it failed closed during `POSTGRES_EPHEMERAL` COPY before a four-candidate result existed.

Failure class:

`POSTGRES_EPHEMERAL_COPY_TEXT_ENCODING_FAILURE__NO_CARRIER_DISPOSITION`

The bounded transport correction committed at harness HEAD:

`8eee62ec694dd85d640f8420f1db3d5c84e7ec90`

with harness SHA-256:

`6218ee1adbf1fe6f2ccb3c8c67fa53683b6b5681fcab7fd28020cd6ae6340f1e`

is ACCEPTED.

Static HQ review confirms that the corrected helpers are used by the actual shared real-B2 PostgreSQL candidate path, not only by the proof mode.

The correction is limited to PostgreSQL transport mechanics:

- retain `--locale=C`;
- initialize disposable PostgreSQL with `--encoding=UTF8`;
- explicitly set psycopg2 client encoding to `UTF8`;
- assert `server_encoding = UTF8` and `client_encoding = UTF8` before COPY;
- preserve the existing text COPY semantics otherwise.

No source decoder, checkpoint, query, oracle, replay, timing, index, budget, selection, or non-PostgreSQL candidate semantics were reopened.

## Accepted cheap proof

Required token observed:

`PRE553_SR04_POSTGRES_UTF8_TRANSPORT_PROOF_PASS`

Accepted assertions:

- `postgres_server_encoding = UTF8`
- `postgres_client_encoding = UTF8`
- exact round-trip of `en–dash`
- exact round-trip of `café`
- exact round-trip of `Ж`
- exact round-trip of `م`
- `unicode_copy_roundtrip_exact = true`
- `DATABASE_URL_unused = true`
- disposable PostgreSQL lifecycle clean
- `raw_source_decode = false`
- accepted checkpoint unchanged
- carrier court not executed

The commit comparison from the correction gate head to the accepted harness head changes only:

`SR04_CARRIER_BAKEOFF.py`

## Real B2 retry authority

REAL B2 RETRY IS AUTHORIZED.

The B2 retry must use only the preserved B1 checkpoint. No raw-source decode is authorized.

Accepted checkpoint identities remain:

| file | bytes | SHA-256 |
|---|---:|---|
| `CHECKPOINT_MANIFEST.json` | 4490 | `f56e6c0710babde0449e5e85da3f1446df4abf1da7b8e866f1f3c4743b031bb0` |
| `QUERY_ORACLE.json` | 131552 | `446c3a2d2ba5127dd48441156e8bfec6a288674233862eb694c2577816845f1a` |
| `events.arrow` | 104610186 | `c0d3c0d3fb426a24408738148424740ff9eb8103fa7cbc01d5c3eb3971e57c25` |
| `respondents.arrow` | 9920410 | `1eca810c4eb369299f62dda31eef3a972e4b3b4ac5c499384ff4298099ff6b73` |
| `sources.arrow` | 5418 | `080ec67148c16d34760daadc94d667c0dd6c101b5b9dcb7d063b24909bd3bf2d` |
| `variables.arrow` | 33882 | `cf8db06e43834a252e737b5f273059cb028d20ad9d51d38f374bfb02e28f241b` |

Relation digests remain:

- `sources`: `931e0031c0d1b1e441f5fdce8853077de23f3de91851878efaae8664dd27d2c0`
- `respondents`: `709e2a6c33a5d3aaba11e9cd55ded5878a6ae01b0ced78f352875faad24a7ddf`
- `variables`: `7bffb7c5881de36e03a41acf74ff3800e24d4150a49c939dabeb1ac6fecf7552`
- `events`: `e0e306157f26a306426c479cccb3ed9d067f3c5b8fc05ee86f1aa2439c020219`
- oracle: `778aff15d0b41333c44125b08f8a2e465f417c80eb431016b0ef48e1fcef09cd`

Before retry, the executor must remove only the failed B2 output/work directories if they still exist, after verifying they are exactly the failed disposable B2 paths and that the accepted B1 checkpoint is not within them. The accepted checkpoint must not be deleted, moved, rewritten, or re-zipped.

Then execute exactly one `--stage-b2` run with no `--source-root`.

Required final token:

`PRE553_SR04_CARRIER_BAKEOFF_RECEIPT_COMPLETE`

## Retry invariants

Do not:

- rerun B1;
- decode raw WVS7 or LiTS I;
- alter checkpoint bytes;
- use `DATABASE_URL` or live Rawlsing PostgreSQL;
- change candidate set or Q00-Q15;
- change oracle/replay semantics;
- change timing/index/budget/selection law;
- modify harness/governance/runtime during the retry;
- treat the earlier failed B2 attempt as carrier evidence.

G-SR04 remains open until HQ adjudicates the successful final B2 package and freezes the selected carrier.
