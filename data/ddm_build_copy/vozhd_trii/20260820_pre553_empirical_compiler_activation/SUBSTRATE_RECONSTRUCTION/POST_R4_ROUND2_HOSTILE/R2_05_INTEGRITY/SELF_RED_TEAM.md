# R2-05 SELF RED TEAM — ATTACK THE MINIMUM FLAT INTEGRITY CORRECTION

Status: `HOSTILE_TO_OWN_ROUND2_CORRECTION`

Disposition under attack: `ROUND2_PASS_WITH_REQUIRED_CORRECTIONS__P0_REPAIRABLE`.

The corrected proposal intentionally removes mandatory Merkle/chunk machinery. This document attacks that subtraction and the new active-selector/one-copy law. If any attack cannot be closed without weakening frozen semantics, the Round-2 disposition must be rejected or reopened.

## RT01 — Flat whole-member verification may be too slow

**Attack:** CLOSED_35 or a large release has members big enough that fresh-process whole-member hashing dominates cold open and violates the later practical gate.

**Why it matters:** minimality cannot become dogma. If member granularity makes correct reopen operationally impossible, a finer integrity unit can have a named job.

**Required response:** measure first. Before C14, reduce deterministic member/shard size within the R01 bounded-shard design and measure file-count/metadata cost. If that remains insufficient, test a flat root-bound chunk-hash inventory. Only if the flat chunk inventory itself is a measured bottleneck or remote proof distribution requires logarithmic proofs does Merkle become admissible.

**Falsifies current C14 rejection only if:** the measured whole-workflow court demonstrates a named member-granularity failure not cured by smaller members, and chunk verification materially cures it without weakening negative/query closure.

## RT02 — A root-bound coverage map can be cryptographically intact and semantically wrong

**Attack:** the compiler emits a perfectly hashed member coverage descriptor that omits a member capable of holding a query match.

**Break:** cryptography authenticates the compiler's mistake. Exact negative truth is still false.

**Required response:** coverage semantics are part of the independent R03 equivalence/oracle court and hostile completeness fixtures. The integrity layer may authenticate coverage but may not self-certify its correctness. When coverage proof is unavailable, broaden the scan.

**Reject correction if:** a negative result can rely solely on producer-authored coverage metadata that has not passed independent semantic/completeness validation.

## RT03 — Linearizable selector storage is assumed, not implemented

**Attack:** the target storage substrate offers only eventual consistency, stale replicas, or best-effort filesystem aliases.

**Break:** an old but valid selector can authorize stale truth.

**Required response:** this is a hard platform requirement. Use a proved linearizable transactional/CAS control primitive or block serving. Do not invent directory `latest`, mtime, or a local cache fallback.

**Reject correction if:** the implementation claims ABA-safe authorization while selector reads can be stale.

## RT04 — Generation counters can themselves ABA through reset/wrap

**Attack:** `activation_generation` is reset during restore, copied from an old snapshot, or wraps.

**Break:** stale publishers can again match a reused selector generation.

**Required response:** generation is never reused within a serving slot. Use a transactionally monotonic logical sequence with a width/representation for which wrap is operationally impossible, or an equivalent unique activation token plus predecessor token under the linearizable store. Snapshot restore must preserve/advance control-plane generation rather than rewind it silently.

## RT05 — Selector generation prevents ABA but not malicious organizational authorization

**Attack:** a privileged actor intentionally writes a selector record authorizing the wrong root with internally consistent fields.

**Break:** hashes and generations cannot distinguish authorized misuse from correct administration.

**Required response:** this court's threat model is corruption/staleness/concurrency/implementation failure, not compromise of the root-authorization authority. If malicious control-plane compromise enters scope, signed/externally anchored activation receipts and key governance become a new named requirement. Do not pretend Merkle solves organizational authorization.

## RT06 — Final generation recheck has a race with output emission

**Attack:** query checks selector generation, then publication CAS occurs one instruction later, then query sends the old-root result.

**Required response:** define the successful final selector check as the query's linearization/authorization point. A CAS after that point means the query logically completed before activation even if network bytes leave later. If product semantics require stricter wall-clock freshness, that is a separate serving-consistency requirement and needs a stronger read transaction, not integrity reinterpretation.

**Reject correction if:** implementation cannot define a single exact authorization point and instead mixes mutable selector state throughout query execution.

## RT07 — Old-root deletion can race pinned readers

**Attack:** after activation, cleanup deletes the old root while a reader still has a handle.

**Break:** depending on storage semantics, the reader can fail mid-read or reopen a now-reused path.

**Required response:** root-pinned readers use immutable generation handles; publication cleanup waits for handle drain or uses a substrate whose immutable object lifetime is safe under delete. Old-root bytes are `DRAINING_TRANSIENT`, not a serving fallback. Migration is not declared settled until drain/delete completes.

## RT08 — The transient duplicate may be accused of violating one-copy law immediately

**Attack:** strict reading says no two complete C11-equivalent physical copies may exist even during migration.

**Response:** existing Authority-44 accounting explicitly distinguishes atomic staging peak from canonical steady state. P0 already requires non-serving staging/shadow build before activation. R2-05 therefore interprets one-copy as one serving/authoritative root plus no duplicate **post-success steady-state** truth. If HQ instead forbids even transient staging duplication, atomic replacement itself requires new storage-law adjudication; R2-05 cannot solve that by retaining a rollback database.

## RT09 — Rebuild-only rollback may make availability terrible

**Attack:** after old-root deletion, new root corrupts and rebuilding multi-gigabyte canonical storage takes substantial time.

**Response:** availability does not authorize hidden truth. The system fails closed while a deterministic rebuild/restore is performed and verified. A later explicit availability requirement can justify an independently governed backup/restore design, but it cannot silently reclassify a standing duplicate as non-authoritative while runtime falls back to it.

## RT10 — Whole-member hash detects corruption only after reading the whole member

**Attack:** one byte near the end is corrupt; verification pays full I/O before detection.

**Response:** true. This is a latency/repair-localization issue, not a correctness gap. It is precisely the measured failure that could justify flat chunk hashes later. Until it is measured as a blocking practical gate, the extra layer is not admitted.

## RT11 — No chunk tree means no surgical repair

**Attack:** a single corrupt range forces full-member/release rebuild.

**Response:** P0 recovery law deliberately forbids repairing canonical truth from cache. Deterministic rebuild from governed source/authority is the safe baseline. Surgical repair becomes a named requirement only if rebuild cost is measured unacceptable and the repair source itself has independent authority/integrity. Merkle is not required merely because repair would be convenient.

## RT12 — Member sharding can become a tiny-file disaster

**Attack:** replacing chunk verification with ever-smaller canonical members creates millions of files and worse reopen/inode behavior.

**Required response:** the escalation order is empirical, not ideological: benchmark member size. If safe member sizing creates an operational file-count failure, that is evidence for flat chunk hashes inside larger members. Do not shrink indefinitely.

## RT13 — A streamed member inventory can itself be huge/corrupt

**Attack:** the inventory contains millions of records; parsing or hashing it becomes a scale problem.

**Response:** R01 requires sequential framing and incremental hashing. Live memory remains bounded. If inventory I/O becomes a measured cold-open failure, grouping inventories hierarchically may become justified. That still does not automatically require a Merkle tree over member payload chunks.

## RT14 — Root/member hashes do not catch semantically wrong but correctly hashed bytes

**Attack:** a buggy compiler deterministically emits wrong missingness/topology/weights, seals hashes, and publishes.

**Response:** correct. Integrity is not semantic equivalence. Activation remains gated by the independent R03 source/C11/I03/I05/I04 oracle. The selector binds its admission receipt. Removing that independent gate would make the flat integrity design dangerously self-certifying.

## RT15 — Cache positive hints can still poison execution order or resource exhaustion

**Attack:** a corrupt cache lists huge false-positive candidate sets, causing pathological work or denial of service.

**Response:** correctness remains canonical because hits are revalidated and misses cannot prune. Cache bounds, decode limits, and deletion on malformed/pathological input are operational resource laws. A cache may hurt speed but cannot change truth.

## RT16 — Forbidding direct cached final answers may throw away useful speed

**Attack:** immutable-root-keyed query result caching could be safe and dramatically improve repeated work.

**Response:** it may be conditionally safe, but it is not needed for the minimum P0 integrity stack. Direct empirical answer caches need their own integrity/dependency/admission proof so corruption cannot create truth. Admit later only if repeated-query measurement makes it material and the cache remains fully bypassable.

## RT17 — Cache false-negative safety can make bitmap acceleration nearly useless

**Attack:** if a bitmap miss cannot prune, expensive canonical scans remain.

**Response:** then the bitmap has not earned a correctness-relevant role as a non-authoritative cache. If exact pruning is materially required, promote the exact index/completeness structure under the canonical root and prove it independently. Do not obtain speed by letting a disposable artifact decide absence.

## RT18 — Fresh-process member verification may repeat expensive work unnecessarily

**Attack:** immutable content-addressed storage with strong object-generation guarantees could safely reuse a trusted prior verification receipt.

**Response:** current Round-1 law refuses a bare persisted boolean because it can outlive corruption. A future storage substrate may define a stronger immutable-generation attestation contract whose trust survives process restart. That would be a separate named mechanism with threat/storage proof. R2-05 does not weaken current expectations merely for reopen speed.

## RT19 — Physical root identity can drift under harmless encoder changes

**Attack:** library/compression version changes produce new bytes for the same semantic release.

**Response:** expected. `physical_root_id` names exact bytes; `semantic_release_id`/logical digests name logical replay. A byte-different root remains inactive until independently proven equivalent and admitted. Only `BYTE_REPRODUCIBLE` profiles promise root equality.

## RT20 — Semantic/admission receipt binding can create circularity

**Attack:** root manifest includes admission receipt, but admission receipt itself hashes the root, producing a cycle.

**Required response:** avoid recursive identity. The physical root binds the immutable candidate content and semantic/oracle contract identity; the **active selector record** binds the separately generated acceptance/admission receipt for that already-sealed root. If a receipt must be stored with the release, store it as post-seal audit metadata outside the physical-root preimage or define an acyclic two-stage receipt scheme.

## RT21 — Wrong selector slot can still produce a valid tuple

**Attack:** a perfectly valid root/receipt tuple is activated under the wrong serving channel.

**Response:** `serving_slot` is part of the active authorization record and the admission receipt. Activation validates that the candidate is approved for that slot. The slot is organizational routing metadata, not empirical content.

## RT22 — Extra files can become hidden canonical material

**Attack:** implementation scans a release directory and reads an unlisted file because its name matches a pattern.

**Response:** the verified root-bound member inventory is the sole canonical membership authority. Unreferenced files are garbage/diagnostic violations and never join a query.

## RT23 — Known corruption quarantine may be overbroad

**Attack:** one cold member fails but a hot query provably does not depend on it; global quarantine sacrifices availability.

**Response:** R1 R05 intentionally chose whole-root quarantine after detected canonical corruption because the observed mismatch does not prove corruption is locally bounded. R2-05 retains that conservative law. Narrow quarantine would require a separately proved failure-containment model and is not minimum P0.

## RT24 — Global quarantine plus no fallback can stop the entire empirical service

**Attack:** yes.

**Response:** that is the intended fail-closed result. Availability is restored only by deterministic rebuild or separately verified explicit activation. A plausible answer from a stale/cache/legacy store is worse than temporary unavailability.

## RT25 — Merkle could be useful even if not required for correctness

**Attack:** true; it can provide logarithmic inclusion proofs, remote partial verification, and corruption localization.

**Response:** R06 minimality law asks what accepted failure occurs without it. Today none. Utility is not necessity. The benchmark plan preserves a precise escalation court so this ruling can change when evidence changes.

## FINAL SELF-RED-TEAM VERDICT

`SURVIVES_ONLY_AS_A_REPAIRABLE_MINIMUM_WITH_EXPLICIT_PLATFORM_PROOFS`.

The corrected flat integrity stack is safer than the Round-1 hierarchical default because it has fewer authorities and still closes every currently named correctness failure. Its hardest unresolved implementation proofs are not cryptographic: linearizable active authorization, immutable consume-after-verify storage semantics, independently valid canonical coverage, and safe reader-drain/old-root deletion.

If any of those cannot be proven, adding Merkle does not rescue P0.
