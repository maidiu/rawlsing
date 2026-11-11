# SR04 — REAL B1 ACCEPTANCE AND CHECKPOINT-ONLY B2 AUTHORITY

Repository: `maidiu/rawlsing`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`
Accepted harness implementation: `4743c40c783544c6c21ec490644896bd0b71ada5`
Accepted harness SHA-256: `d33a86ccfa4fc75916f2f24a3ca627732abc45fa29cafd15cc8ab3439836b5b4`

## Ruling

Real SR04 B1 is ACCEPTED.

Disposition:

`REAL_B1_NEUTRAL_CHECKPOINT_ACCEPTED__RAW_SOURCE_DECODE_CLOSED_FOR_SR04__B2_CHECKPOINT_ONLY_AUTHORIZED`

B1 executed at control checkout HEAD:

`1964fd0fccf153c8d981c56585abbe63448b8371`

Required token was present:

`PRE553_SR04_B1_NEUTRAL_CHECKPOINT_COMPLETE`

The return recorded:

- exit code `0`;
- `candidate_execution_started=false`;
- `DATABASE_URL_unused=true`;
- `raw_source_decode=true`;
- checkpoint readback verification `PASS`;
- no B2 execution;
- no repository modification.

## Accepted exact checkpoint

The sole authorized real B2 input is the preserved directory:

`/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`

Checkpoint version:

`SR04_NEUTRAL_CHECKPOINT_V1`

Total substantive checkpoint bytes:

`114705938`

### Exact checkpoint file identities

| file | bytes | SHA-256 |
|---|---:|---|
| `CHECKPOINT_MANIFEST.json` | 4490 | `f56e6c0710babde0449e5e85da3f1446df4abf1da7b8e866f1f3c4743b031bb0` |
| `QUERY_ORACLE.json` | 131552 | `446c3a2d2ba5127dd48441156e8bfec6a288674233862eb694c2577816845f1a` |
| `events.arrow` | 104610186 | `c0d3c0d3fb426a24408738148424740ff9eb8103fa7cbc01d5c3eb3971e57c25` |
| `respondents.arrow` | 9920410 | `1eca810c4eb369299f62dda31eef3a972e4b3b4ac5c499384ff4298099ff6b73` |
| `sources.arrow` | 5418 | `080ec67148c16d34760daadc94d667c0dd6c101b5b9dcb7d063b24909bd3bf2d` |
| `variables.arrow` | 33882 | `cf8db06e43834a252e737b5f273059cb028d20ad9d51d38f374bfb02e28f241b` |

A transport ZIP uploaded to HQ independently reproduced all six substantive file byte sizes and SHA-256 identities. Mac `__MACOSX` transport entries are not checkpoint members and have no authority.

## Accepted source identities embedded in checkpoint

WVS7:

`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

LiTS I:

`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

## Accepted neutral relation digests

- `sources`: `931e0031c0d1b1e441f5fdce8853077de23f3de91851878efaae8664dd27d2c0`
- `respondents`: `709e2a6c33a5d3aaba11e9cd55ded5878a6ae01b0ced78f352875faad24a7ddf`
- `variables`: `7bffb7c5881de36e03a41acf74ff3800e24d4150a49c939dabeb1ac6fecf7552`
- `events`: `e0e306157f26a306426c479cccb3ed9d067f3c5b8fc05ee86f1aa2439c020219`

Accepted oracle canonical digest:

`778aff15d0b41333c44125b08f8a2e465f417c80eb431016b0ef48e1fcef09cd`

## Accepted fixture shape

- sources: `2`
- respondents: `126222`
- variables: `48`
- events: `3029328`

### WVS7 hostile facts

- rows: `97220`
- Q152 SPSS user-missing: `2557`
- Q153 SPSS user-missing: `4877`
- Q154 SPSS user-missing: `1802`
- Q155 SPSS user-missing: `3777`
- Q156 SPSS user-missing: `1745`
- Q157 SPSS user-missing: `3626`
- I_PSU `-4`: `31137`
- D_INTERVIEW target duplicate value count: `1000`
- distinct benchmark weight variables represented: `2`

### LiTS I hostile facts

- rows: `29002`
- distinct `id`: `29002`
- `country=9`: `1000`
- each of `weight_0`, `weight_1`, `weight_2`: `29000 ORDINARY`, `2 SYSTEM_MISSING`, `0 STATA_EXTENDED_MISSING`

## B2 authority

B2 is now authorized, and ONLY B2 is authorized.

B2 must:

1. use `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT` exactly;
2. preflight the six file byte sizes and SHA-256 identities above before execution;
3. run only explicit `--stage-b2` mode;
4. let the accepted checkpoint reader recompute/verify source identity, all neutral relation digests, and oracle digest;
5. execute the accepted shared four-candidate carrier court;
6. apply the accepted correctness-first, speed-second, lightness-third selection rule;
7. write the exact final Stage-B package and deterministic ZIP;
8. return the complete package to HQ;
9. preserve the accepted B1 checkpoint unchanged until HQ closes G-SR04.

B2 MUST NOT:

- pass `--source-root`;
- invoke B1 or `build_fixture`;
- decode WVS7 or LiTS I;
- inspect or use `DATABASE_URL`;
- touch the live Rawlsing PostgreSQL database;
- modify the harness or governance;
- alter the checkpoint;
- alter candidate/query/budget/selection law.

Required final B2 token:

`PRE553_SR04_CARRIER_BAKEOFF_RECEIPT_COMPLETE`

## Gate consequence

G-SR04 remains open only for the real B2 carrier result and HQ final selection adjudication.

No further raw-source reconstruction is authorized under SR04.