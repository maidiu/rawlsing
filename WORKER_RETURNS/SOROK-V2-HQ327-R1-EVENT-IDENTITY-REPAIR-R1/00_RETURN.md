# HQ327 R1 — B2 event-identity custody repair

**Grade: `SOURCEFREE_EVENT_IDENTITY_REPAIR_CANDIDATE_PENDING_INDEPENDENT_I2`.** The synthetic ingress collision is repaired and executed. This is an author repair return for HQ’s later independent acceptance, with no production event authority, actor grant, psychological adoption or original survey execution.

Assigned branch: `agent/rabochii-sorok-v2-hq327-r1-b2-event-identity-repair-r1`. Exact startup and directly observed initial remote: `a52fc56c72b2a0496356a68c9a9e8563edf1c107`; its parent is original B2 `950ecf0b3816ea7d0dd3ab48b62c92cedfe0e883`. One accountable Codex implementer; no helpers, provider/model change or external model calls. Final commit identity is obtained from the returned remote ref, rather than embedded into its own preimage.

## Defect reproduced and repaired

Before editing, `run_repair.py before` reconstructed all original B2 files from Git and ran its unchanged court, frozen X2 court and collision probe in a disposable directory. X2’s 17 tests passed, **including its assertion that the defect exists**. The raw SQLite result was two occurrence rows, one nominal event ID and two different objective payload hashes. Both downstream target-denied responses rolled back; both objective rows persisted. This is a custody RED despite that defect-demonstration test being green. Complete reproducible input, receipts and raw SQL row bodies are in `evidence/before/collision.json`.

The same probe after repair produces one row. Its second admission is `DENIED / EVENT_IDENTITY_CONFLICT`, with `event_admission=NOT_PERFORMED`, no B1 response invocation and the checkpoint unchanged. See `evidence/after/collision.json` and `source_diff.patch`.

Only the commissioned B2 candidate `bridge.py` changed outside this return. B1/P1/D1/F1 source, all historical B2 tests and evidence, frozen X2, accepted controls, Pyat and PREMAIN remain unchanged. Original B2 remains available at its immutable comparison SHA.

## Identity and transaction contract

`b2_event_identity` has one **global event ID within this bounded SQLite synthetic registrar**, rather than extra actor/world/issuer namespace columns that would let a caller reuse the ID. Its immutable binding contains the full witness, packet, context/readset, policy, selected candidate, fixed focal actor and ingress rule. That binds issuer, parent, expected actor checkpoint, objective payload, both witnessed wall-clock time and B1’s existing numbered effective time, world, participants, independent actions and attributed utterances, including fields not projected into B1.Event. This repair does not change either inherited time representation or create a general temporal law.

`BEGIN IMMEDIATE` precedes the checkpoint read and all ingress validation. Identity reconciliation, the inherited B1 occurrence insert, B2 ingress insert and unique identity insert run under that actual SQLite writer lock. B1’s `admit_fixture` executes an insert on an autocommit connection but contains no explicit commit; inside this enclosing transaction it is safely controlled by B2. The registrar commits all three rows together. Any denial before commit rolls the transaction back; SQL failures return a typed storage refusal. No read-then-write identity gap exists between independent connections.

After that admission commit, the original B1 response/target transaction runs separately. Capability, owner-grant and storage denials preserve the valid objective fact. The repair does not erase a previously admitted fact to compensate for a response failure.

An exact replay reuses the same occurrence and ingress. If its actor checkpoint has advanced, it returns `ALREADY_ADMITTED`, `admission_replay=EXACT_EVENT_ALREADY_ADMITTED`, and no response invocation. The legacy `reason=WITNESS_BINDING_OR_STALE_STATE` and `response_status=DENIED` describe the prohibited response rebinding; this preserves the unchanged author stale-response assertion. With the original prestate still current, downstream capability/grant conditions may be retried without inserting another occurrence. Capability packets, owner grants and response mode are deliberately outside the event binding. Distinct lawful IDs remain admissible.

An old/direct B1 occurrence lacking B2 identity provenance fails closed with `EVENT_IDENTITY_UNBOUND_LEGACY`; this return invents no retrospective migration authority. Missing or inconsistent mapped ledger rows fail an integrity check. Direct writes through B1 or arbitrary SQL remain outside this B2 boundary. B2 still supports its fixed child fixture; actor/issuer alterations are refusal controls, not a new general multi-actor or multi-issuer implementation. The local witness allowlist and tuple binding are not external authentication, signing, revocation or ADP019 production issuance.

## Executed results

| Court | Before | Final candidate |
|---|---:|---:|
| Unchanged B1 | 39 pass | 39 pass |
| Unchanged P1 | 74 pass | 74 pass |
| Unchanged original D1 | 22 pass, historical defective absence guard | same |
| Unchanged corrected D1 | 17 pass | 17 pass |
| Frozen F1 reference | 97 pass | 97 pass |
| Unchanged connected B2 | 45 pass | 45 pass |
| Unchanged F1 applicability accounting | 36 pass | 36 pass |
| Frozen X2 hostile oracle | 17 pass, including collision demonstration | 16 pass, 1 expected failure of collision-demonstration assertion |
| New R1 expected-refusal/transaction court | not run on baseline | **45 pass** |
| Frozen native F1 runner | exit 1, **17 RED** | exit 1, **same 17 RED** |

Thus all **249 inherited +81 unchanged B2** checks are preserved. F1 remains **19 boundary negative/deferral passes and 17 N/A** in B2 accounting; native F1 is still RED. IDs: F01–F08, F10, F11, F13, F15–F19, F21. There is no native-positive promotion. Raw native JSON and its exit receipt are preserved; derived native/Node JUnit explicitly retains their actual results and is supplementary to the unchanged runners.

The frozen X2 source is byte-identical to `931aec3497c60114444806c375d1bb51ec7c0e7d`. Its only post-repair failure is `test_same_event_id_accepts_distinct_objective_payload_hashes`: it indexes a now-refused second admission as if it were an admitted object. The raw failure and JUnit remain intact. The new regression asserts refusal and unchanged tables; the original oracle was not rewritten or marked xfail.

The 45 new checks cover 20 witness collisions, changed complete readsets, exact replay after success/denial/fault/later events, legacy custody, failures at each of the three SQL inserts, missing mapped rows, cold replay, lock-protected stale prestate, four simultaneous fresh OS processes over eight admission terrains, four simultaneous successful replays committing exactly one response, and a killed writer between occurrence insertion and identity commit. The killed transaction is invisible from another connection and fully absent after reopening; a fresh valid attempt then succeeds. Per-process receipts, distinct process IDs and raw table snapshots are under `evidence/after/concurrency/`.

The original real two-event positive and journal-only control still produce `joint_check:caretaker` versus `inspect_alone:caretaker`; fresh-process reconstruction matches exact receipts and final state. Their trace JSONs also match the baseline byte-for-byte.

## Reproduction and evidence custody

From this return directory:

```sh
python3 run_repair.py before
python3 run_repair.py after
python3 audit_return.py
```

The scripts use the existing authorized Git object store; no clone, dependency install or remote model is required. They reconstruct the original B2 closure in a temporary directory, substitute only candidate bridge.py for the after court, and copy fresh logs into this return. They never overwrite historical B2 evidence. `run_repair.py` verifies the exact frozen-X2 failure identity and collision row counts. `audit_return.py` verifies 69 imported files, frozen X2 bytes, source hashes and JUnit, then creates portable supplemental JUnit and a byte manifest. `runtime_probe.py` records actual imported module files relative to the staging root and their SHA-256 values.

Primary evidence: `evidence/{before,after}/commands.json`, `b2_execution_receipt.json`, `b2/*.xml`, `x2.xml`, `collision.json`; final `identity.xml`, `runtime.json`, `source_runtime.json`, and `concurrency/*.json`. `source_manifest.json` supplies Git blob SHA-1 and content SHA-256 separately. XML hostname and ephemeral user/path fields are sanitized in evidence copies only; source/frozen bytes are untouched.

Development disclosures: an initial new replay reason failed the unchanged stale-response assertion (80/81); the final receipt separates successful idempotent admission from denied stale response and all 81 pass. The first new process tests compared stored JSON lists against initializer tuples (33 pass/8 test failures); the correction compares the actual stored prestate. A new crash-recovery test initially omitted re-registering downstream capability witnesses after reopening (44 pass/1 test failure); registration was restored. Both new-test failure logs/JUnit remain under `evidence/development/`. An evidence-only XML sanitizer initially inserted unescaped placeholders; it was corrected to transform parsed XML nodes, and final XML was regenerated and parsed successfully. One duplicate early court launch occurred while retrieving a lost process-session handle; it made no source mutations and is not counted as additional independent evidence.

Governance read: exact commission, HQ327 intake at `f0ef08f6076365874e9d700ac7056a7abd8ce5f4`, X2 return and full hostile source, S2 return and full science court at `7e6ac81e85aa2c8dca0cea53349ad61f10fb6665`, exact B2/B1 admission source, and sealed 00D. 00C is absent from the sealed/HQ327 trees; the governing copy was read at `3c685eb4734856b61f2d601e082eb325e3f6f1d1` (blob `c33afd5d00b6c2ca735baa759d17ebaa932a2b03`), preserving the supplied one-agent/editor assignment and later independent-review boundary.

S2’s scientific limits remain: recognized_plan/imposed_plan are authored hypotheses, not grounded psychological law; no real event signer, independent ongoing actor, calibrated human probability, native CAN011 grant, ADP019/020 production ingress or original survey execution is established. HQ owns subsequent independent I2 acceptance.
