# B3_ATOMIC_ADMISSION_R1 transaction and source contract

This is an isolated sourcefree B3 candidate. The frozen B2, M2, target owner, F2 cases and all historical tests retain their exact bytes. Only candidate `integration.py` and `fixture_authority.py` differ from frozen B3. The version and exact file hashes are in `candidate_version.json`; the eventual pushed Git commit is the publication identity. The source-only `pinned_closure.tar.gz` and `verified_sources.json` preserve the imported closure. No M2 R3 is imported.

## Root cause and preflight

Frozen B3 admitted the main event through B2, which commits its own occurrence/ingress/identity transaction. B3 then autocommitted its source/audit rows. Only afterward did it resolve optional origin, construct and validate temporal scenes, and begin the target transaction. A downstream refusal could neither undo B2's commit nor the already written B3 rows. `stop()` then raised its own snapshot assertion. Future event time 99 at frame time 7 was converted into a B2 context time 99 without first checking the actual frame clock. Optional origin was also absent from the registrar binding.

The repair checks `event.time <= as_of`, source qualification/registration, historical raw preimages, past exposure insertion, source identity and monotone clock. It resolves a requested origin from an actual admitted B2 audit bundle and requires origin time no later than the current event. It constructs every loss/current scene, checks its event clocks, checks derived source collisions and executes frozen M2 eligibility before the first B2 admission. The registrar now binds `origin_event_id` including its absent/null value. Unknown origin and unregistered rebinding refuse before B2 executes. Original witness/claim/permission owner checks remain in force.

`preflight_*` SQL receipts demonstrate zero B2 admission calls for missing origin, future event, unbound origin, later origin and derived source collision. `boundary_sql_before_first_b2_admission.json` retains the complete unchanged tentative snapshot and SQL trace at the first-admission boundary. Snapshot preparation copies already existing SQLite content into a disposable private file; that file copy is not event admission and writes no public table.

## Chosen transaction policy

The public unit is one complete **valid B3 run**, not each internal call to B2. All newly proposed B2 source admissions and B3 bookkeeping within this run are tentative until successful publication. This is a strict atomic envelope, rather than the permitted alternative of exposing durable source phase commits on a later B3 refusal.

1. Hold the existing B3 advisory file lock. Read the full public snapshot and use SQLite backup to create a private scratch database.
2. Execute the preflight and complete B3 calculation against scratch. B2 keeps its original internal BEGIN/COMMIT behavior there. No B2 method, SQL connection transaction API, owner permission or accepted occurrence semantics is patched.
3. REFUSED or DEFERRED discards scratch. Return a typed receipt with `owner_effect_committed=False`, no provisional owner receipt, and actual public snapshot equality in `no_mutation`. Unexpected Python/storage errors propagate after cleanup with no public writes.
4. For ELIGIBLE, take a real public `BEGIN IMMEDIATE`, compare the entire current snapshot with the original readset and require identical schema plus strictly additive row changes. Insert only new rows into each pinned table, then COMMIT once. There are no public DELETE, UPDATE, REPLACE, whole-database restore or retrospective provenance conversions.
5. Any publication failure rolls back the public transaction, including BaseException cleanup. A domain refusal returns a typed receipt; unexpected errors propagate. SIGKILL is recovered by SQLite on the next cold connection. Scratch can remain after SIGKILL, but no recovery/import path ever reads it.

This is deliberately bounded and O(database size) in staging, comparison and memory. It copies all tables; it is not a scalable production transaction manager. It assumes the pinned schema and additive B3 path. A future legitimate checkpoint update or schema change refuses `PUBLICATION_NONADDITIVE_CHANGE` or `PUBLICATION_SCHEMA_CHANGED` until a separately reviewed policy exists. Full-disk/power-loss durability, hostile filesystem replacement, arbitrary SQL corruption and general malformed input recovery are not certified.

## Table ownership and fate

| Tables | Custody | Within a refused/crashed new B3 run | After a completed valid run |
|---|---|---|---|
| `occurrence`, `b2_event_identity`, `b2_ingress` | Unchanged B2 objective source issuer | New tentative rows discarded; every independently committed existing row retained | New qualified source rows published together |
| `b3_source`, `b3_audit` | B3 source projection and exact B2 bundle provenance | Discarded; no orphan source/audit | Published with matching B2 rows |
| `b3_m2_sources`, `b3_preimage` | B3 immutable research readsets | Discarded; no ghost recruitment/history conditioning | Published with source/response boundary |
| `b3_response`, `b3_transition`, `b3_clock` | Immediate response, separate test target owner, processing clock | Discarded/rolled back, including a tentative validated target effect | Response/clock and any independently permitted target effect published atomically |
| `checkpoint`, `joint_receipt` | Legacy B1 owner | Existing bytes preserved | Unchanged; legacy B1 response remains uninvoked |

A target permission denial is an **eligible admitted event with a denied target transition**, not refusal of the event. Its valid source records persist and its target record stays empty. Missing permission is eligible valid-empty. B2 may still independently admit facts through its original public Bridge; B3 neither rolls them back nor silently deletes them on any later refusal. Tests exercise unrelated independent facts across every injection/SIGKILL boundary, and an independently admitted exact B3 event followed by denied permission.

## Injection and cold proof

The new court covers before first B2 admission; after first source admission; immediately after B3 source insertion; after B3 preimage insertion; after target effect before scratch commit; and additionally after all public inserts before public commit. Each boundary has domain-refusal, unexpected exception and SQLite error controls with clean/existing-independent-fact databases. Each also has actual child-process SIGKILL for both database conditions. All tables are compared through a separate fresh Python process, `PRAGMA integrity_check` must return `ok`, and later permission-absent replay must produce no retained practice or CHECK_LOCK recruitment. Two additional tests inject immediately after the first `admit_projection` has completed its internal B2 commit. Separate boundary receipts include tentative table snapshots and both scratch/public SQL traces.

The optimistic publication readset also detects X3's privileged second connection before publishing. Its independently written row is retained; our tentative source/response/target rows are discarded. Here `no_mutation=False` truthfully reports external change. The frozen X3 test expected ELIGIBLE followed by later detection, so it now fails on the stronger immediate refusal. Arbitrary SQL can still damage the store; this is detection at the publication boundary, not authentication or authority over that writer. Raw `admit_projection`, `_run`, M2 helpers and the trusted fixture CLI are not independently secured public issuer APIs.
