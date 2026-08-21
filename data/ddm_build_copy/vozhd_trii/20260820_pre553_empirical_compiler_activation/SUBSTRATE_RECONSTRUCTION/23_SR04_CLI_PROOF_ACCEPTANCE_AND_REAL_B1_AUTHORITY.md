# SR04 — CLI PROOF ACCEPTANCE AND REAL B1 AUTHORITY

Status: `ACCEPTED_CLI_SEPARATION__REAL_B1_AUTHORIZED__REAL_B2_BLOCKED`

Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Accepted harness HEAD: `4743c40c783544c6c21ec490644896bd0b71ada5`
Accepted harness SHA-256: `d33a86ccfa4fc75916f2f24a3ca627732abc45fa29cafd15cc8ab3439836b5b4`

## HQ adjudication

The cheap B1/B2 CLI-separation proof is accepted.

The proof established that the actual explicit B1 mode:

- writes a neutral checkpoint;
- verifies that checkpoint through the same frozen checkpoint reader;
- emits the B1 receipt;
- records `candidate_execution_started=false`;
- does not invoke the shared carrier court.

The proof also established that the explicit B2 mode:

- consumes a checkpoint without raw-source decoding;
- invokes the already-accepted shared carrier court;
- reaches the already-accepted final package writer;
- rejects a corrupted checkpoint before candidate execution.

No duplicate query/candidate/oracle/checkpoint truth implementation was introduced.

## Real B1 authority

Real B1 is now authorized at the exact launch HEAD supplied by HQ.

B1 is the only expensive operation authorized by this authority.

Its exact semantic boundary is:

`exact raw WVS7 + exact raw LiTS I -> frozen neutral fixture -> hostile checks -> independent oracle -> relation digests -> immutable neutral checkpoint -> checkpoint readback verification -> B1 receipt -> STOP`

B1 must not execute any carrier candidate and must not touch live PostgreSQL or `DATABASE_URL`.

## Real B1 required source identities

- WVS7: `WVS Wave 7.sav`
  - SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
  - expected rows: `97220`
- LiTS I: `LiTS_I.dta`
  - SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
  - expected rows: `29002`

The neutral fixture must contain exactly `3029328` event rows.

The frozen hostile checks in the harness remain binding, including WVS user-missing counts, I_PSU `-4`, D_INTERVIEW duplicate target, LiTS identity count, LiTS weight physical states, LiTS country code 9 count, and distinct W_WEIGHT/S018 identity.

## B1 checkpoint retention law

The real B1 checkpoint is an execution artifact, not a repository artifact.

Do not commit it to Git.
Do not delete it after a successful B1 return.
Do not mutate it after a successful B1 return.

HQ must receive its exact absolute local path, total byte size, checkpoint manifest, exact relation digests, oracle digest, source hashes, and B1 receipt.

A later B2 authorization will bind to that exact checkpoint identity. If the checkpoint is missing or fails readback verification, B2 remains blocked and B1 must be re-executed from exact source bytes.

## B1 success token

`PRE553_SR04_B1_NEUTRAL_CHECKPOINT_COMPLETE`

The token is admissible only if:

- raw source hashes and expected row counts passed;
- all frozen hostile fixture checks passed;
- checkpoint write completed;
- checkpoint readback and relation-digest verification passed;
- oracle digest verification passed;
- `candidate_execution_started=false`;
- `DATABASE_URL_unused=true`;
- the checkpoint still exists at the returned absolute path.

## B2 status

Real B2 remains `BLOCKED_ON_HQ_B1_ADJUDICATION`.

The B1 success token does not itself authorize B2.

HQ must inspect the B1 receipt/checkpoint identities first and issue a separately pinned B2 launch order.
