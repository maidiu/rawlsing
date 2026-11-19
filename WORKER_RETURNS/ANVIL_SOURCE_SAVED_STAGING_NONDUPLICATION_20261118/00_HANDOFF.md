# Source-saved staging nonduplication — scratch harness proof

## Result

**PASS — one existing writer driven directly from exact projected sections; duplicate body journal and explicit first I02 pass removed in the harness path.**

- Exact source baseline: `aee95429609c372564e996c2d3d3eb30e9253cbf`
- Construction-only patch used: `ffa4520f965e4f2fd22ea5043d0c80528f44a47f94afdb763d3b77c21ca3a08f`
- Scratch base: `c2c09c98739dbb8361c55ff46073974519543836`
- Harness commit: `8d65749ea9c71fc18627d54d40b05c4c24e32917`
- Harness source: `staging_nonduplication_harness.py`
- Harness patch: `harness.patch`
- Proof: `proof.json`

This is scratch-only. No product writer, C11 schema, Q2 body-tee/postconsumer
path, F1–F4 custody, protected branch, or real SRC04 artifact was modified.

## What was exercised

Baseline uses the existing construction-only path:
first I02 certificate, projection spool, `SourceI02BodyTee` body journal,
`SourceSavedBodySink` journal replay, and `write_direct_estate` (which performs
its own I02 proof and Parquet publication from one iterator stream).

Candidate uses the same exact projected sections and the **same existing
`write_direct_estate`** directly. It removes the body journal and the explicit
first I02 pass. It does not introduce a second writer, a full-object graph, or a
new format.

Matched TEST_ONLY fixture results:

- Baseline exact roots and candidate exact roots are equal.
- Manifest SHA-256 equal: `65474d37cfdd0e2756dd91bffb54d57de0d14a317dfa6464d6c37d10dd73fbd4`
- Per-family counts equal: 13 families, 29 retained objects.
- Full canonical object payloads equal for every family.
- Full `RespondentIdentity` payloads equal.
- Full `RoutingEligibilityFact` payloads equal.
- Replay identity/manifest equality true.
- Both outputs passed independent cold `VerifiedDirectEstate` reopen using the
  baseline receipt roots and manifest as the held authority; the fixture current
  callback is exact `roots == held_i02`.
- One mutated candidate Parquet copy refused with
  `body/index Parquet member missing or corrupt`.
- Revoked current refused with `current source/operation authority refused`.

## Resource accounting (measured fixture, not a benchmark)

Baseline peak observed phase: **610,955 bytes**.
Candidate peak observed phase: **387,759 bytes**.
Observed peak reduction: **223,196 bytes (36.5%)**.
Baseline I02 passes: **2**. Candidate I02 passes: **1**.
Body journal removed: **78,168 bytes / 13 files**.
Explicit first certificate removed: **176,128 bytes**.
Candidate still has projection spool **31,100 bytes** and one writer stage
**288,601 bytes** at its observed phase; final retained bytes equal baseline
**356,659 bytes**.

The live aggregate snapshot `evidence/SRC04_LIVE_STAGING_FOOTPRINT.json` showed
projection JSONL 4,505,034,543 bytes, replay body journal 8,276,350,027 bytes,
direct writer stage 13,743,239,168 bytes, and 16,101,466,112 free bytes. The
candidate removes the body journal and one explicit I02 pass, but **not** the
projection spool or the writer's one-pass I02/Parquet stage. No full-scale peak
or launcher-cutoff claim is made; remaining headroom must be measured by a real
authorized run. This is the feasibility limit.

## Authority boundary

The candidate does not trust writer-generated roots. The baseline receipt roots
and manifest are held as the matched expectation; the candidate writer receives
`expected_i02=baseline_receipt.i02`. Cold readers use the baseline roots and
manifest with the fixture exact-root current scope. A future authorized run
still needs its exact external grant/current authority; this fixture scope is
not that authority.

`VerifiedDirectEstate` requires an exact held manifest SHA and exact I02 roots;
it does not require a retained SQLite certificate. The scratch `.i02-proof.sqlite`
inside the writer remains temporary and is deleted by the existing writer. If a
different real first reader requires a retained certificate, that is the exact
blocker: it is not part of the existing direct-estate reader contract.

## Preserved boundaries

No original source read, stat, hash, or decode; no running SRC04 writer
interruption/restart/read; no artifact modification; no WVS or larger benchmark;
no C11 schema/writer change; no new grant; no protected/product branch write.
Original-source admission remains in the untouched construction-only production
patch and its prior pre-read denial test.

## Reproduce

```bash
cd /tmp/anvil_staging_nondup
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  python3 -B rawlsing_next/tests/staging_nonduplication_harness.py /tmp/anvil_staging_proof
```
