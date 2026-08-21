# SR04 — PHYSICAL CARRIER BAKEOFF — REVISION 7 POSTGRES UTF-8 TRANSPORT CORRECTION

Repository: `maidiu/rawlsing`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`
Accepted real B1 checkpoint: `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`

The exact launch HEAD is supplied by HQ. Verify it before doing anything.

## Current status

Accepted:

- Stage A
- Stage A.1
- Stage A.2
- B1/B2 CLI separation
- real B1 neutral checkpoint

A real B2 attempt from `5d8cc8314c4d57d2dff58c25dcc1ff1d4739485d` failed closed during `POSTGRES_EPHEMERAL` COPY with an ASCII `UnicodeEncodeError` on U+2013 EN DASH.

No carrier selection is admissible from that failed run.

Binding newest authority:

`25_SR04_B2_POSTGRES_UTF8_TRANSPORT_CORRECTION_GATE.md`

REAL B2 RETRY IS BLOCKED.

## Immediate mission — cheap PostgreSQL UTF-8 transport proof only

Modify only:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py`

Do not modify any other repository file.

The correction is mechanical and bounded:

1. retain ephemeral PostgreSQL `--locale=C`;
2. explicitly initialize the ephemeral cluster/database as UTF-8 (`--encoding=UTF8` or exact equivalent);
3. explicitly set the psycopg2 client encoding to UTF-8 after connect;
4. assert `SHOW server_encoding` is `UTF8`;
5. assert `SHOW client_encoding` is `UTF8`;
6. leave the candidate text COPY semantics otherwise unchanged;
7. do not change Q00-Q15, oracle/replay logic, timing, indexes, budgets, selection, checkpoint format, source handling, or any non-PostgreSQL candidate.

Add a tiny proof mode or equivalently isolated synthetic proof path that uses the exact corrected PostgreSQL init/connect/COPY mechanics and round-trips exactly at minimum:

- `en–dash`
- `café`
- `Ж`
- `م`

Required proof assertions:

- `postgres_server_encoding = UTF8`
- `postgres_client_encoding = UTF8`
- `unicode_copy_roundtrip_exact = true`
- `en_dash_roundtrip = true`
- `latin1_range_roundtrip = true`
- `non_latin1_cyrillic_roundtrip = true`
- `non_latin1_arabic_roundtrip = true`
- `DATABASE_URL_unused = true`
- clean disposable PostgreSQL shutdown
- no raw-source decode
- no accepted-checkpoint mutation
- no four-candidate carrier court execution

Required token:

`PRE553_SR04_POSTGRES_UTF8_TRANSPORT_PROOF_PASS`

## Inputs that must remain untouched

Do not modify, move, delete, or regenerate:

`/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`

The accepted checkpoint identities remain those frozen in `24_SR04_REAL_B1_ACCEPTANCE_AND_B2_AUTHORITY.md`.

Do not read WVS7 or LiTS I during this proof.
Do not pass `--source-root`.
Do not run `--stage-b1` or `--stage-b2`.
Do not use or inspect `DATABASE_URL`.
Do not touch live Rawlsing PostgreSQL.

## Publication after proof

After the cheap proof passes:

1. syntax/static-check the harness;
2. verify only `SR04_CARRIER_BAKEOFF.py` changed;
3. commit only that file;
4. commit message: `Fix SR04 PostgreSQL UTF-8 transport`;
5. push the control branch;
6. return to HQ:
   - exact starting HEAD;
   - exact new harness HEAD;
   - harness SHA-256;
   - exact proof command;
   - complete small proof receipt;
   - required token;
   - server/client encoding values;
   - exact Unicode strings read back;
   - final `git status -sb`;
   - pushed branch HEAD;
7. STOP.

Real B2 retry is separately authorized only after HQ accepts the committed correction.

## Forbidden

Do not:

- rerun B1;
- run real B2;
- decode raw source bytes;
- convert neutral/checkpoint text to Latin-1;
- change checkpoint bytes;
- change candidate set, query semantics, correctness law, timing law, storage budget, or selection law;
- alter any non-PostgreSQL candidate except shared helper extraction strictly necessary to make the exact same PostgreSQL transport mechanics testable;
- commit execution outputs.

Fail closed on ambiguity.