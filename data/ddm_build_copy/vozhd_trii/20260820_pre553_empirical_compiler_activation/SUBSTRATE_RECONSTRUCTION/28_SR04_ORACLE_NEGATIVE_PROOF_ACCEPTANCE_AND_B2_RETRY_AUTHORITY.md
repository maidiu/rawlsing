# SR04 — ORACLE NEGATIVE-TEST PROOF ACCEPTANCE AND REAL B2 RETRY AUTHORITY

Repository: `maidiu/rawlsing`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Accepted real B1 checkpoint: `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`

## Accepted state

The real B1 neutral checkpoint remains ACCEPTED and immutable.

The first two real B2 attempts remain NON-ADMISSIBLE carrier evidence:

1. first failed closed during PostgreSQL ASCII COPY transport;
2. second passed the accepted PostgreSQL UTF-8 correction, then failed closed in the deliberate wrong-oracle negative test because the synthetic-era test assumed a list while the real Q02 oracle value is dictionary-shaped.

Neither failed attempt produced a lawful four-candidate disposition or provisional selection.

The bounded oracle-negative-test correction committed at harness HEAD:

`ea0d02ffde10a98872e73ea2b1fed8e453246cfb`

with harness SHA-256:

`12a4eb3bace293ddf355c9661e051f77be3735813d6d776c61c472be0ba81c7d`

is ACCEPTED.

Static HQ review confirms that the actual shared carrier-court validation path now invokes the same shape-agnostic corruption helper exercised by the cheap proof.

The accepted helper:

- supports dict/list/scalar/null values;
- deterministically alters the supplied value;
- does not mutate the input;
- uses stable key ordering for dictionaries;
- is used only for the deliberate wrong-oracle negative test.

No oracle construction, normalization, Q00-Q15 semantics, candidate implementation, replay logic, timing, index, budget, selection, checkpoint, source, or PostgreSQL UTF-8 transport semantics were reopened.

## Accepted proof

Required token observed:

`PRE553_SR04_ORACLE_NEGATIVE_TEST_SHAPE_PROOF_PASS`

Accepted assertions include:

- synthetic list corruption passes;
- real-like dictionary corruption passes;
- both original values remain unchanged;
- wrong-oracle detection succeeds for both shapes;
- dict/list empty values, scalar values, and null values are supported by the helper;
- no exception;
- no raw-source decode;
- accepted checkpoint unchanged;
- no carrier-court execution;
- `DATABASE_URL` unused.

The commit from correction-gate control HEAD to accepted harness HEAD changes only:

`SR04_CARRIER_BAKEOFF.py`

## Real B2 retry authority

REAL B2 RETRY IS AUTHORIZED.

The retry must use only the preserved accepted B1 checkpoint. No raw-source decode is authorized.

Accepted corrected harness:

- HEAD: `ea0d02ffde10a98872e73ea2b1fed8e453246cfb`
- SHA-256: `12a4eb3bace293ddf355c9661e051f77be3735813d6d776c61c472be0ba81c7d`

Accepted checkpoint identities remain:

| file | bytes | SHA-256 |
|---|---:|---|
| `CHECKPOINT_MANIFEST.json` | 4490 | `f56e6c0710babde0449e5e85da3f1446df4abf1da7b8e866f1f3c4743b031bb0` |
| `QUERY_ORACLE.json` | 131552 | `446c3a2d2ba5127dd48441156e8bfec6a288674233862eb694c2577816845f1a` |
| `events.arrow` | 104610186 | `c0d3c0d3fb426a24408738148424740ff9eb8103fa7cbc01d5c3eb3971e57c25` |
| `respondents.arrow` | 9920410 | `1eca810c4eb369299f62dda31eef3a972e4b3b4ac5c499384ff4298099ff6b73` |
| `sources.arrow` | 5418 | `080ec67148c16d34760daadc94d667c0dd6c101b5b9dcb7d063b24909bd3bf2d` |
| `variables.arrow` | 33882 | `cf8db06e43834a252e737b5f273059cb028d20ad9d51d38f374bfb02e28f241b` |

Relation/oracle digests remain:

- `sources`: `931e0031c0d1b1e441f5fdce8853077de23f3de91851878efaae8664dd27d2c0`
- `respondents`: `709e2a6c33a5d3aaba11e9cd55ded5878a6ae01b0ced78f352875faad24a7ddf`
- `variables`: `7bffb7c5881de36e03a41acf74ff3800e24d4150a49c939dabeb1ac6fecf7552`
- `events`: `e0e306157f26a306426c479cccb3ed9d067f3c5b8fc05ee86f1aa2439c020219`
- oracle: `778aff15d0b41333c44125b08f8a2e465f417c80eb431016b0ef48e1fcef09cd`

Before retry, remove only the failed B2 output/work paths if they still exist, after verifying they are the exact disposable paths and are neither symlinks nor aliases/parents/children of the accepted checkpoint.

Then execute exactly one `--stage-b2` run with no `--source-root`.

Required final token:

`PRE553_SR04_CARRIER_BAKEOFF_RECEIPT_COMPLETE`

## Retry invariants

Do not:

- rerun B1;
- decode WVS7 or LiTS I;
- alter checkpoint bytes;
- use or inspect `DATABASE_URL`;
- touch live Rawlsing PostgreSQL;
- change candidate set or Q00-Q15;
- change oracle construction, normalization, replay, timing, indexes, budgets, or selection law;
- reopen the accepted PostgreSQL UTF-8 transport correction;
- modify harness/governance/runtime during the retry;
- treat either earlier failed B2 attempt as carrier evidence.

G-SR04 remains open until HQ adjudicates a successful final B2 package and freezes the selected carrier.
