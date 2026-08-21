# R01 — Streaming / Memory-Bounded / Transactional Carrier Mechanics

Status: `AUTHORIZED__NON_DISPOSITIVE__DESIGN_AND_PROOF_ONLY`

Return token: `POST_R4_R01_STREAMING_MEMORY_RETURNED`

Starting authority commit: `bc2d022d49b1a860a33b29ce171a89c91956c35e`

## WHOLE_MACHINE_CONTAINMENT

This return changes no semantic authority and proposes no production runtime. It is a physical-carrier design subordinate to the closed whole-machine architecture. The semantic reference remains source-native truth + frozen C11 + I03 + I05 + I04 + the closed whole-machine law. Evidence Authority remains distinct from Semantic Authority. No carrier encoding, cache, shard boundary, sort run, Parquet feature, manifest member, telemetry record, or publication path may become a semantic branch in I03/I05/V553+.

The proposal preserves the C11 rule that storage order is canonical storage order only: semantic order/rank/multiplicity remains in identity-bearing event/topology fields. It preserves exact source identity, M01–M18, ExactRef/content-hash laws, raw/canonical separation, physical-missing/semantic-absence separation, routing/risk-set information, repeated/multiple/ordered/ranked topology, weights/design/measure authority, source-relation/nonduplication provenance, replay closure, and exact positive and negative query truth.

The proposal is deliberately less ambitious than R02/R04. It does not infer functional dependencies, normalize event fields to another grain, change typed encodings, introduce bitmap/matrix semantics, or claim a preferred endgame query layout. Its job is to establish a safe bounded-memory long-form baseline against which more aggressive physical proposals can be judged.

## PROBLEM_OWNED

R01 owns C01, C02, C04, C15, C16, C17 and streaming-relevant transactional publication.

Accepted R4/C11 code demonstrates the resource fault precisely enough for design without a full-source autopsy:

- `pre553_physical_decoder.py` already exposes bounded `iter_batches`/`iter_cells` for the normal chunked reader path, with stable source row ordinals.
- `pre553_c11_ingest.py` represents logical package sections as immutable whole tuples and computes order-invariant candidate projections by sorting exact refs.
- `pre553_parquet_carrier.py` currently builds whole relation lists, sorts whole relations, creates `pa.Table.from_pylist(rows)`, stores all member/relation hash dictionaries, and on reopen executes `pq.read_table(...).to_pylist()` for every relation before reconstructing the release.
- The current one-file-per-relation shape also permits Parquet footer/dictionary/internal-writer state to grow with corpus cardinality even if the caller-side row batch were capped.

The required replacement must therefore bound four distinct surfaces, not one: producer-to-carrier queues; canonical ordering; writer/backend metadata; and reopen/audit state.

## PROPOSED_MECHANISM

Adopt a **segmented canonical run/merge carrier** with immutable sealed publication.

1. **Typed logical rows remain unchanged.** Each accepted C11 object/internal record is encoded with the same exact logical fields and identity material as the frozen C11 projection. R01 omits no logical field and performs no semantic deduplication.
2. **Bounded run formation.** For each fixed C11 logical relation family, the writer accepts a bounded stream, accumulates at most `B_rows` and `B_payload_bytes` plus one maximum logical row, canonical-encodes those rows, sorts only that bounded run by the C11 canonical storage key, writes a temporary immutable run, hashes it by streaming reads, then releases the run buffer.
3. **Bounded external merge.** Runs are merged with fixed fan-in `F`. If run count exceeds `F`, perform deterministic multi-pass merges. Each merge holds at most one bounded input batch per open run plus one bounded output batch. This is required because frozen C11 candidate projection is canonically sorted/order-invariant; arrival order cannot be promoted to semantics merely to save RAM.
4. **Fixed-size final shards.** The final merge emits deterministic, independently closed relation shards, each with capped rows/encoded payload and a capped Parquet row-group/page configuration. No corpus-scale single Parquet footer is permitted. Dictionary encoding must be disabled or explicitly cardinality-capped for unbounded-cardinality columns; an implementation that cannot prove its backend state bound fails R01.
5. **Streaming shard inventory.** Each relation has an on-disk sequential inventory containing shard ordinal, deterministic filename, row count, encoded-byte count, content hash, canonical-key lower/upper bounds, and relation-schema identity. The root seal stores only a fixed-size descriptor per logical relation plus the inventory hash/count/aggregate logical digest; it does not hold a Python dictionary with one entry per shard.
6. **Lazy exact reader.** Reopen verifies the fixed root seal, streams and verifies relation inventories, and exposes a sealed release handle whose relations are iterators/exact resolvers rather than eager corpus tuples. Audit and exact lookup use shard/batch iteration. A compatibility materialization operation may exist for explicitly bounded fixtures, but it is not the canonical reopen path and must reject/require an explicit bound rather than silently materialize a corpus.
7. **Exact arbitrary reconstruction.** `resolve_object_exact(ref)` or equivalent can scan the canonical inventory/shards and reconstruct an exact object while retaining only the current inventory record, shard metadata, bounded row batch, and one candidate. Absence is returned only after an integrity-valid complete scan. This is O(N) worst-case time but bounded memory and exact negative authority. Optional physical indexes are acceleration only and cannot be correctness-bearing.
8. **Transactional seal.** Build under a unique noncanonical staging root, close/hash every shard and inventory, write the root seal last, fsync the file/directory chain, then atomically rename the sealed directory into its immutable content-addressed destination on the same filesystem. Only the post-rename destination is discoverable as committed.

### Deterministic ordering and duplicate/override law

Canonical relation order must be derived from frozen C11 identity, not worker completion order. For identity-bearing C11 objects, the primary key is the exact canonical storage key based on family/ref identity. Where a frozen deterministic tie-order authority applies, its exact rule supplies the tie key. Semantic event order/rank remains encoded inside the event/topology object and is never inferred from shard order.

The physical layer **never applies last-write-wins, first-write-wins, dictionary overwrite, or unproved deduplication**. Every logical occurrence presented by frozen C11 is retained through run formation and merge. Exact duplicate occurrences remain duplicate occurrences unless frozen C11 validation itself proves an idempotent identity rule for that exact family. Same apparent ID with different exact content remains distinct or is rejected by the frozen validator as applicable; R01 does not choose. An ambiguous collision without an authority-defined tie identity is a hard deterministic-validation failure, not an override opportunity.

### Concurrency law

The baseline is one canonical emitter per relation. Bounded producer workers may decode/construct in parallel only behind a fixed-size queue and backpressure. Every produced item must carry its already-authorized stable source/logical identity before concurrency. Completion order cannot determine final order. External canonical sort/merge is the only permitted reordering mechanism. Open merge fan-in, worker count, queue depth, and per-worker batch size are fixed configuration bounds. No unbounded future/reorder map is permitted.

## WHAT_CHANGES_PHYSICALLY

- Whole in-memory relation lists become bounded sorted runs plus external fixed-fan-in merge.
- One corpus-sized Parquet file per relation becomes independently closed capped shards.
- Corpus-scale Python member/relation dictionaries become streamed inventories plus fixed root descriptors.
- Eager `read_table(...).to_pylist()` reopen becomes batch/shard iteration.
- Exact object/relation resolution is scan-capable and may use correctness-independent bounded indexes/caches.
- Publication adds an explicit seal-last/fsync/atomic-rename commit protocol.
- Telemetry becomes a non-authoritative streaming side channel.

Shard boundaries, compression pages, row groups, inventory line boundaries, merge-pass count, cache residency, and telemetry cadence are physical only.

## WHAT_MUST_NOT_CHANGE_LOGICALLY

The replacement must reconstruct exactly the same authorized C11 information and observable validation outcomes, including:

- exact source artifact identity/hash and release identity;
- exact object identity/content hash and replay closure;
- complete respondent identities and complete respondent-event incidence, including physically missing cells where source-native law requires incidence;
- exact native question/topology bindings;
- raw/native value evidence versus canonical/semantic response state;
- routing/applicability/risk-set facts or exact rules;
- coordinate, weight, design and measure authority/typed absence;
- source-universe relations or exact distinct-by-default state;
- replay bindings and typed deferred/not-applicable states;
- authority snapshots and exact authority references;
- M01–M18 coverage;
- multiplicity, event occurrence identity, order, rank, repeated/multiple-response topology;
- frozen C11 rejection states for integrity, topology loss, event-identity collapse, risk-set loss, unauthorized promotion, source-universe collapse, replay nondeterminism, and missing required authority;
- I03 exact positive and negative truth conditions, I05 discovery reachability including unforeseen combinations, and I04 structural-admission parity.

No field is allowed to disappear on the theory that it is “usually constant,” “not queried today,” or “recoverable later.”

## INFORMATION_ACCOUNT

R01 proposes **zero semantic omission**. The detailed ledger therefore classifies the C11/source-native material as `STORED_DIRECTLY` except fixed release facts that are already, under frozen law, reconstructed from immutable release identity. No new question-grain/respondent-grain functional dependency is claimed; such claims are R02 territory and are marked `REJECTED_NOT_PROVEN_DERIVABLE` where relevant.

Physical metadata added by R01—shard ordinal, inventory hashes, key bounds, merge-run metadata, compression parameters, backend format version, seal state—is not source semantics. It exists to make the semantic payload bounded, auditable and publishable.

## ASSUMPTIONS_AND_AUTHORITY

Authoritative basis:

- downstream `RAWLSING_GOVERNING_SPIRIT.md`, `CONSTRAINTS_PRIORITIES.md`, `TERMINAL_DEMAND_ENVELOPE.md`, `ARCHITECTURE_PASS_LAW.md`, `CAPABILITY_MATRIX.md`;
- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`;
- substrate `00_COMMAND_CHARTER.md`, `02_GATE_LAW.md`, `09_SOURCE_NATIVE_CONSTITUTION.md`, `10_FORMAT_DECODER_CONTRACT.md`, `12_WVS_LITS_HOSTILE_FIXTURE_ORACLE.md`, `49_SR06_R4_FINAL_ACCEPTANCE_AND_REAL_SOURCE_REOPEN.md`, `50_SR07_SR08_P2_R4_REAL_SOURCE_SCALE_CONFIRMATION_AUTHORITY.md`, `52_POST_R4_PHYSICAL_OPTIMIZATION_CANDIDATE_REGISTER_AND_SAFETY_LAW.md`, and campaign 53;
- narrow accepted code inspection of `pre553_physical_decoder.py`, `pre553_c11_ingest.py`, `pre553_c11_repository.py`, `pre553_parquet_carrier.py`, and `pre553_empirical_query.py`.

Critical non-semantic implementation assumptions are enumerated in `ASSUMPTION_LEDGER.csv`. The most important are: same-filesystem atomic rename/fsync semantics for the baseline publisher; a provably bounded Parquet/Arrow writer configuration; finite maximum single-row size as an unavoidable lower bound; and a bounded upstream decoder contract.

One important boundary remains explicit: the accepted decoder has a compatibility path that retains a full reader frame for exact encoding overrides. R01 does not reinterpret or remove those compatibility overrides. A future claim of **end-to-end** bounded compilation must either prove a chunked reader with identical source-native behavior for those exact sources or declare that dependency unresolved. The carrier itself must never hide that upstream unboundedness behind a false “bounded” label.

## HOSTILE_COUNTEREXAMPLES

The proposal was red-teamed against, at minimum: an N≫RAM relation; one enormous logical row; maximal-cardinality strings that explode encoder dictionaries; millions of tiny shards; conflicting apparent IDs; repeated exact occurrences; semantically meaningful occurrence/rank fields; all-physical-missing source regions; physical missing versus semantic absence; missing declarations/ranges/extended missing; many authority/dependency records; absent-key exact lookup; first/middle/last-shard lookup; crash before/after every seal step; orphan staging trees; truncated inventory; corrupt shard/footer; extra unreferenced file; concurrent publisher race; completion-order race; cache eviction; cache corruption; empty optional relation with typed absence; and I03/I05/I04 workloads not known when the carrier was designed.

The detailed cases and required outcomes are in `HOSTILE_CASES.csv` and `SELF_RED_TEAM.md`.

## I03_I05_I04_EFFECT

**I03:** no selector grammar or predicate truth changes. `variable`, `minimum`, `maximum`, `allowed`, and `excluded` semantics remain frozen. The carrier must expose the exact typed empirical inventory/ordinals/facts needed by I03. An absent value/object is negative truth only after an integrity-valid complete exact scan or an independently verified correctness-preserving index; cache miss is never semantic absence.

**I05:** no pair/k-way/conditional/reversal/recursive/cloud-like frontier is preselected by the carrier. Exact typed respondent-event incidence remains streamable so unforeseen combinations remain discoverable. Any downstream external spill needed by a bounded discovery algorithm is an I05 execution concern, not permission for R01 to delete event information.

**I04:** structural admission receives exactly the same evidence/authority boundary and exact refs. Physical shards, caches and row groups are not admissibility facts. If a sealed release cannot reconstruct the evidence closure expected by I04, reopen fails closed.

Net effect: intended semantic effect is zero; resource/latency effect is physical only.

## INTEGRITY_REPLAY_EFFECT

R01 strengthens publication mechanics but does not usurp R05’s final integrity/canonical-copy law. The R01 baseline requires:

- every final shard to be closed before its digest is admitted to its relation inventory;
- every relation inventory to be closed and hashed before the root seal;
- a fixed root seal binding schema/carrier version, exact release/source identities, relation inventory identities/counts, total logical counts/digests, replay identity, and required publication parameters;
- root seal written last;
- fsync of file and directory metadata before atomic rename;
- immutable content-addressed destination after commit;
- reopen to reject missing/malformed seal, schema mismatch, selector mismatch, missing/truncated/corrupt inventory, missing/corrupt shard, row/count/digest mismatch, replay-closure mismatch, and semantic-root mismatch.

Authoritative membership is defined by the sealed inventories. Unreferenced garbage must never become authoritative merely because it exists in a directory. A strict audit can additionally detect extra files in bounded memory by deterministic contiguous shard naming plus streamed directory entry counts; it need not load all filenames into a set.

Replay must be possible after deleting all correctness-independent caches. A cache cannot be part of the semantic/replay root.

## RESOURCE_EXPECTATION

Let:

- `R` = configured maximum rows per in-memory sort run;
- `P` = configured maximum canonical encoded payload bytes per run/output batch;
- `F` = fixed merge fan-in;
- `W` = fixed worker count;
- `Q` = fixed queue capacity per pipeline edge;
- `Smax` = maximum single canonical logical row size encountered;
- `E` = fixed backend writer/reader internal-state ceiling proven for the selected encoding configuration;
- `C` = bounded LRU/cache ceiling.

Then writer peak live state must be bounded by a corpus-independent function of approximately `O(P + F*(batch + E) + W*Q*Smax + C + fixed_relation_state)`, with the unavoidable `Smax` term. Reader/audit state must be `O(batch + E + C + one_candidate + fixed_seal_state)`. Run count, shard count and corpus N increase disk I/O and elapsed time, not live Python retention.

External sort costs O(N log_F K) merge work where K is run count; sequential final scan costs O(N); exact unindexed object lookup is O(N) worst-case. Those costs are consciously accepted by the baseline because memory safety and semantic conservatism dominate latency in R01. R04 may later propose faster physical access if it passes the same oracle.

No implementation passes merely because `B_rows` is fixed. Backend dictionaries, row-group metadata, Parquet footer growth, inventory accumulation, directory enumeration, futures/reorder buffers, hash tables, and reopen materialization are all part of the memory proof.

## COMPLEXITY_COST

Compared with current R4 persistence, the proposal adds:

- external run files and merge passes;
- multiple shards per relation;
- streamed inventories;
- a seal lifecycle;
- bounded lazy release/view APIs instead of assuming corpus tuples;
- explicit backpressure and concurrency discipline;
- crash cleanup for noncanonical staging artifacts;
- slower worst-case random lookup without an optional index.

The design intentionally refuses additional complexity such as semantic normalization, bitmap indexes, adaptive per-variable encodings, or a correctness-bearing database catalog. The external sort is not optional complexity: it is the price of retaining frozen C11 canonical ordering without corpus-scale RAM.

## RAW_SOURCE_PROBES_IF_ANY

None. Repository-first authority and accepted code answered the physical questions required by R01. No raw bytes were materialized, read or probed.

## REASONS_TO_REJECT_OWN_PROPOSAL

Reject this proposal if any of the following cannot be resolved in implementation/synthesis:

1. The chosen Parquet/Arrow writer cannot demonstrate a hard corpus-independent bound on dictionary/page/footer/internal metadata state per shard.
2. External run/merge ordering cannot reproduce frozen C11 canonical projection and deterministic tie law exactly.
3. A downstream accepted consumer semantically depends on eager tuple materialization rather than the file-neutral C11 logical contract and cannot be adapted without changing semantics.
4. The compatibility decoder path cannot be made bounded while retaining exact source-native behavior, yet synthesis claims end-to-end bounded compilation.
5. The target filesystem/storage backend cannot supply the assumed seal-last durable atomic publication primitive and no equivalent transactional adapter is provided.
6. Exact negative lookup cannot distinguish “not present” from “scan/integrity incomplete.”
7. Crash injection reveals any partially published release as valid/discoverable.
8. Cache deletion changes an answer or replay result.
9. Fixed shard/run settings cause a single unbounded backend structure despite caller-side batching.
10. R05’s integrity/publication architecture establishes a stronger canonical-copy requirement incompatible with the proposed inventory/seal layering.

## FALSIFICATION_CONDITIONS

The R01 claim is falsified by any one of:

- peak writer or reader/audit live memory grows monotonically with N after configured bounds and `Smax` are held fixed;
- any corpus relation is converted wholesale to a Python list/tuple/table during canonical write, reopen, validation or audit;
- run merge output changes when worker completion order changes;
- canonical logical event/ref digest differs from the frozen C11 oracle for the same accepted candidate;
- an exact duplicate/conflict is silently resolved by arrival order;
- a physically missing event, topology occurrence, risk-set fact, authority record, or other C11 material disappears;
- a corrupted/truncated member passes reopen/audit;
- an incomplete staging release is discoverable as committed;
- absence is asserted before a complete verified exact search;
- clearing/rebuilding a cache changes I03/I05/I04 results;
- any downstream semantic branch depends on shard/row-group/cache/storage details;
- end-to-end boundedness is claimed while an upstream compatibility decoder still retains corpus-scale state.

`BENCHMARK_PLAN.md` defines the proof plan; it deliberately uses hostile fixtures and synthetic scale before any authorization for another full CLOSED_35 run.

## SYNTHESIS_REQUIREMENTS

HQ/R06 synthesis should require R01 to compose with:

- **R02:** R01 is the no-semantic-omission baseline. Any R02 grain/FD compaction must prove itself independently and can be layered only after the R01 logical stream is preserved.
- **R03:** use the independent semantic equivalence oracle as acceptance authority; R01’s own digests are not sufficient proof.
- **R04:** vectorized/columnar indexes may replace linear scans only as physical acceleration, never as the sole semantic copy unless independently proven.
- **R05:** R05 owns final immutable root/member/chunk/canonical-copy integrity law. R01’s seal/inventory is a proposed transactional substrate, not a competing canon.
- **R06:** benchmark memory plateaus, crash atomicity, deterministic concurrency, cache deletion, exact reconstruction and full I03/I05/I04 reachability together; do not accept separate microbenchmarks as whole-machine proof.

Synthesis must also resolve the compatibility full-read decoder issue before using the phrase “end-to-end bounded-memory compiler.”

## RECOMMENDATION

`RECOMMEND_FOR_SYNTHESIS_WITH_HARD_GATES__NOT_PRODUCTION_AUTHORIZATION`

Adopt the segmented external-run/merge + fixed-size shard + streamed-inventory + lazy-reader + seal-last atomic publication design as the **simplest semantically conservative R01 baseline**. It directly removes the two known corpus-scale carrier mechanics—whole-relation retention/sort and eager reopen materialization—while refusing R02/R04 semantic or aggressive physical claims.

Do not accept it for production until R03 equivalence, R05 integrity composition, backend memory-bounds testing, compatibility-decoder boundedness, and crash/concurrency falsification all pass.

`POST_R4_R01_STREAMING_MEMORY_RETURNED`
