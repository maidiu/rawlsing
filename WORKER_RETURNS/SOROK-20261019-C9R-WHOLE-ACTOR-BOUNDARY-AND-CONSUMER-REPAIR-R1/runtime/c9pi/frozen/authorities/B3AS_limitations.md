# Requirements, preserved limitations and owner permissions

## Transaction contract as accepted

The two schema-contract REDs are closed at `Integration.run` for the tested pinned schema. The publication readset is one consistent logical snapshot: `sqlite_master` definitions (tables, indexes, triggers, views), `schema_version`/`user_version`/`application_id` metadata, and every table's rows. It is captured before scratch work and rechecked under `BEGIN IMMEDIATE`; drift refuses with `PUBLICATION_READSET_CHANGED` or `PUBLICATION_SCHEMA_CHANGED`. The scratch copy's `schema_version` is compared to its own immediate post-backup baseline, never across files, because SQLite backup advances the destination schema cookie. Refusal receipts compute `no_mutation` over the same logical snapshot. Row publication stays strictly additive; independently admitted rows and external schema objects are preserved, never deleted or rolled back.

`exact_replay` asserts source-identity re-entry. It does not assert a write-free call: a repeat under a changed middle appends its own `b3_response` record. `no_mutation` answers whether the call changed the logical database, and it does so truthfully across the measured matrix (fresh success, identical repeat, post-target repeat, valid-empty, denied, clean refusal, schema/row-refusal).

This acceptance does not certify `_run`, `admit_projection`, fixture registration, direct Bridge/B1 SQL or helper modules as universal public ingress. Constructor schema creation is outside the reviewed `run` envelope.

## Boundaries of the guarantee

- The readset is **logical database state**. Physical file layout, freelist/page bytes, connection-local settings (journal mode, cache, foreign_keys), and forgery by an arbitrary privileged SQL writer are outside it. Nothing here prevents DBA-level corruption or proves unauthenticated request data can alter schema.
- Whole-store staging and comparison remain **O(database size)** with scratch storage and writer contention. No production scale, disk-full recovery, filesystem replacement, malicious ledger JSON, OS failure or power-loss/fsync durability is certified. SIGKILL results are observed process-death recovery only.
- The `BEGIN IMMEDIATE` window blocks concurrent writers through SQLite's writer lock (verified with `timeout=0` DDL). That is a locking boundary, not cryptographic protection.
- External schema/row writers in this court are privileged test adversaries using the sanctioned `fault` seam or independent OS processes. They are not evidence of an event-driven attack path.
- A second event reusing the same utterance/exposure evidence is refused `SOURCE_PREIMAGE_IDENTITY_COLLISION` because projections are bound to event identity. This is protective, and it constrains how multi-event fixtures must be built.

## Three older scientific/helper topics, preserved

1. Two IDs for one same-time physical check can satisfy the authored practice predicate. This is a distinct-opportunity/witness-identity limitation of the unmodified test-only target rule. It blocks interpreting that predicate as proof of repeated enacted practice. Future evidence contracts need actual opportunity/act identities, not a new invented human-learning score.
2. Both qualifying checks may occur after loss. A pre-loss threshold is not required by the published target rule; the frozen prospective assertion is stronger than that rule. Preserve the RED and qualify before/after claims without declaring post-loss repetition impossible or adding an unsupported developmental law.
3. Standalone `source_guard.check` checks overlaps, not completeness of a historical readset. It is not safe alone as a complete history-continuity validator. Integrated B3 additionally checks persisted raw preimages; unchanged removal and rewrite negatives pass. This is a helper-reuse limitation at its own grain.

Historical negatives remain at their exact identities: native F1 17 RED, M3 source-preimage 3 RED, full E2 2 RED, X2 1 RED, M1-on-M2 19 RED, strict I2-on-M2 10 RED, and original-B3 seeded refusal 4 RED. Historical D1's known absence defect is not erased by its 22 passes. The 97 F1 reference passes and 36 applicability accounting checks confer no native positive qualification.

## Permissions still NOT granted

No new integration commission or grant is issued here. HQ and the competent owners must separately authorize any bounded adapter at exact pins:

- An independently qualified M2 source/history/lineage implementation and explicit permission for the exact read/enumeration versus durable-write API. Frozen M2 `5c2fbe14ccfa5027becfabc682206a1e61aaf986` retains its three M3 preimage REDs; durable interpretation remains quarantined. No newer M2 R3/R4 or ONECALL was incorporated.
- ADP019 owner-issued producer/event-kind/temporal-history admission authority and exact envelope/projection/receipt identities. Synthetic fixture allowlists and P1 proposal selection are not native event authority.
- CAN008 exact accepted rule/version, read-only conditioning state, lawful actor receivability/uptake/recruitment and bounded immediate consequence; no menu item becomes selected belief or affect by implication.
- CAN011 independently accepted concrete kind/target/update-rule and bound actor, before-state, operation, causal-parent/opportunity witnesses, payload, time and permission. Valid-empty/denied target outcomes remain lawful and cannot erase previously admitted events. No arbitrary numeric traits or deterministic personality endpoint may be supplied as a substitute.
- Separate ADP016/017 permissions if memory or epistemic/access writes are required (currently NOT_GRANTED). Native actors, original survey sources, external model calls, production stores, ADP020 randomness and ADP021 scheduling each require their own actual owner contracts/grants. Missing grants are typed owner HOLDs, not permission to counterfeit fixtures.

## Scientific ceiling

A sourcefree SQL repair and its independent acceptance are not calibrated human habit acquisition, an enacted third check at t9, autonomous other-actor development, selected durable belief/affect, native actor/source authority, full recursive formation, production feasibility, or CAN008/CAN011 law admission. A durable observed candidate is not evidence of actual practice formation or human psychology. No secure/insecure labels, arbitrary trait scores, romantic resolution or psychologically predetermined ending is assigned. This reviewer makes no semantic adoption and creates no next commission; the findings return to Sorok HQ for adjudication.
