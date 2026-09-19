# FIABC-W2-B03 — Measurement Constitution

## 1. Scope and authority

This constitution closes FIABC Wave-1 open cell `OC08` at accounting-definition grain. It governs how the frozen P2X physical-carrier court must assign and measure work; it does not alter source meaning, semantic authority, query/discovery authority, candidate meaning, workload shape, or Candidate-C lawful scope.

Governing evidence, in descending relevance for this burden:

- `WORKER_RETURNS/FIABC-HQ-WAVE1-FANIN/04_ABC_INVARIANT_MANIFEST_DRAFT.csv@dfdae1dfcef5e3061094935312c3db2cc0fde2f0`, especially INV015/INV016/INV018;
- `WORKER_RETURNS/FIABC-B03/00_RETURN.md` blob `7ced91aae64e2e97a9b903a57feafbdcb0799c1f` and its accounting/risk ledgers;
- `HQ_HANDOFF/CHETIRI_FINAL_P2_COURT_MANIFEST_R1.md@617c9c9426db12a3c0f7fea6b68a582c10759553` and its JSON authority;
- `WORKER_COMMISSIONS/EE-P2X/00_COMMISSION.md@617c9c9426db12a3c0f7fea6b68a582c10759553`;
- `WORKER_RETURNS/EE-R6B/04_EXECUTION_MEASUREMENT_ORDER_RESET_LAW.json` blob `ca5fed67c0816edf602c5a5a8211d0b69419fd82`;
- current implementation evidence `rawlsing_next/ee_p2x_darwin_stage_backend.py@617c9c9426db12a3c0f7fea6b68a582c10759553`.

The controlling noncollapse is:

`SEMANTIC_OWNER != COST_OWNER`.

A common authoritative object may be produced outside candidate timing while a candidate still pays to open, deserialize, attach, traverse, reconstruct from, or otherwise use that object. Conversely, a candidate may pay substantial physical work without becoming owner of the truth it realizes.

## 2. Comparison unit

The atomic measurement unit is:

`(source_id, source_sha256, candidate_id, frozen_workload_id, frozen_authority_set)`.

LiTS-I and WVS7 remain separate universes. No metric may be summed, averaged, normalized, or compared after dropping `source_id` unless HQ later performs a clearly labeled non-dispositive synthesis. Source-local raw vectors remain the evidence of record.

Candidate order stays the frozen order `A -> B -> C`; this constitution does not redesign it.

## 3. Cost classes

Every operation entering the court must be classified as exactly one of these cost classes.

### C0 — `COMMON_UPSTREAM_PRODUCTION__EXCLUDED_FROM_CANDIDATE_COST`

Production of immutable candidate-neutral truth or court material that exists before any candidate invocation:

- source identity / SHA authority;
- accepted semantic/routing/topology/design authority;
- Lock1/Lock2 workload authority;
- runtime query/discovery authority and fixed frontier;
- independently prepared parity-oracle material;
- immutable producer-owned replay/reference roots.

C0 is produced once and reused. Repeating it once per candidate merely for symmetry is forbidden.

### C1 — `CANDIDATE_ACCESS_TO_COMMON_INPUT__INCLUDED`

Actual candidate-local cost of opening, reading, hashing, deserializing, importing, attaching, or traversing a frozen C0 object after the candidate boundary starts. This is physical realization/access work even though the object remains semantically common.

### C2 — `CANDIDATE_PHYSICAL_REALIZATION__INCLUDED`

Candidate-specific source decoding, transformed-carrier construction/open, cache/accelerator construction/open, provider binding, candidate-owned persistence, warm reuse, deletion/regeneration, invalidation, replay, stale/corrupt handling, and interruption recovery.

### C3 — `COMMON_LOGICAL_OUTPUT_EXECUTION__INCLUDED`

The candidate-local execution needed to produce the invariant logical workload/output through that candidate: exact I03 work, exact I05/learned production, required audit/replay, and the frozen common output identities. Semantic truth is common; the physical cost of producing it through each candidate is measured.

### C4 — `COURT_ADMINISTRATION__EXCLUDED_FROM_CANDIDATE_COST`

After-stop evidence formatting, Git operations, return-package writes, HQ fan-in, report prose, and court-level verifier/report serialization. A metric receipt must not become part of the metric it reports.

## 4. Candidate-local start boundary

A candidate cell may start only after all of the following are true:

1. exact source identity is verified at court level;
2. exact Lock1/Lock2 identities and fixed source-local workload are verified;
3. all required candidate-neutral authority/reference objects are present and immutable;
4. the independent parity oracle required by FIABC-W2-B02 has been materialized and frozen without candidate output;
5. candidate scratch/durable/log roots are isolated;
6. no prior candidate process, `_SESSIONS` entry, candidate module object, candidate cache, candidate transformed state, or candidate scratch/durable state is reachable by the new candidate process, except a specifically adjudicated preserved candidate artifact listed in `03_PRESERVED_WORK_ACCOUNTING.csv`;
7. the candidate's cold-state predicate for the operation to be measured is recorded.

The start timestamp for candidate-total wall accounting is taken immediately before the first candidate-specific process/action that realizes or accesses the candidate path. Common C0 preparation is already complete.

Candidate-specific imports/owner initialization after this timestamp are candidate cost. Common upstream producer creation is not.

## 5. Candidate-local stop boundary

A candidate cell stops only after every lawfully reachable frozen workload/lifecycle obligation for that source×candidate has either:

- completed and produced its metric/behavior/output receipt; or
- reached an authorized typed stop under the frozen court law.

For a complete cell, stop follows:

- final required I03/I05/learned output production;
- required deletion/rebuild/persistence operation;
- source-release invalidation operation;
- semantic-authority invalidation operation;
- stale/corrupt behavior where applicable;
- actual interruption/failure-recovery operation;
- fresh-process replay;
- required audit;
- final governed output/product/semantic/replay identity capture;
- final high-water/resource counters for the candidate envelope.

The stop timestamp precedes C4 court-verifier/report/fan-in/Git work.

## 6. Process and memory isolation

A fresh OS process is required for each source×candidate cell. Process reuse across candidates is forbidden for dispositive RSS/CPU accounting.

Within a candidate process, same-candidate warm state may persist only where the workload explicitly calls for warm/repeated research. Candidate B's lack of retained transformed empirical payload does not prohibit transient in-process objects during its own cell; it prohibits carrying them into another candidate cell.

Darwin `ru_maxrss` is interpreted as bytes under accepted EE-R8B law, but only the peak from the candidate's own process lifetime qualifies as `peak_rss_bytes`. A process-global peak inherited from A cannot be reported for B or C.

If a governed lifecycle stage spawns a child process (for example fresh-process replay), the child reports its own CPU and RSS. Candidate-total CPU includes child CPU exactly once. Candidate peak RSS is the maximum of the isolated candidate main-process peak and required child-process peaks, not their sum.

## 7. Wall and CPU accounting

Every measured phase has an immutable `phase_id`, start monotonic timestamp, stop monotonic timestamp, user-CPU delta, system-CPU delta, and process identity.

Candidate-total CPU is computed from non-overlapping process envelopes plus required child-process deltas. It is never the last `_measure` call and never a sum of overlapping nested timers.

Candidate-total wall is the outer candidate envelope. Per-operation wall fields remain separately reported. The court must not derive candidate-total wall by summing nested operation timers.

Measurement overhead is accepted as court instrumentation overhead only when it is structurally identical across candidates; expensive evidence serialization after stop is C4 and excluded.

## 8. Cold / warm / repeat law

`cold` means no candidate-owned state capable of accelerating that operation exists beyond the frozen cold-state predicate. It does not claim the host OS page cache has been globally flushed unless the frozen court explicitly provides such a mechanism.

Canonical `cold_i03_latency_ns` is the first invocation of the designated exact I03 request from the recorded candidate-owned cold state and against the already-frozen independent oracle. If parity machinery has already invoked that same query/session and thereby warmed candidate state, the cold metric is invalid until the cold-state predicate is lawfully re-established.

`warm_i03_latency_ns` is the designated repeat of the same exact request after the allowed candidate-owned warm state from the cold execution remains in place.

Cold and warm fields are write-once. A later stage may not overwrite an earlier metric key. Additional cold-like samples require distinct names such as `parity_i03_latency_ns` or `research_cold_i03_latency_ns` and cannot silently replace the canonical field.

## 9. Preserved work law

Preservation is about avoiding unlawful or wasteful repetition, not granting free cost.

A preserved candidate-local receipt may contribute numeric cost only when all of these are proved:

- exact source and candidate identity match;
- exact Lock1/Lock2/workload/runtime binding matches;
- the measured operation is identical to the current metric definition;
- cold/preserved start state is proved;
- process/resource isolation required by this constitution is proved;
- the receipt directly observed the metric rather than deriving it from final state;
- no metric is inferred for a field the receipt did not capture.

Failure of any condition yields `MEASUREMENT_NOT_CAPTURED` for that field, not zero and not an estimated substitute.

Candidate-neutral C0 work is reused without candidate numeric charge and need not be repeated to make candidate rows look symmetric.

## 10. Observed I/O and state-size law

`bytes_read`, `bytes_written`, and `bytes_rewritten` are observed I/O event totals during the candidate envelope.

They are not directory-size aliases.

- `bytes_read`: actual bytes returned to candidate execution by source/carrier/cache/authority reads after candidate start. If candidate-local SHA verification reads the source and decode reads it again, both reads count. A court-level preflight read completed before start does not.
- `bytes_written`: actual bytes issued by candidate execution to candidate-owned transformed state, scratch, caches/accelerators, and required common-output materialization inside the envelope.
- `bytes_rewritten`: the subset of writes that replace/rewrite an already existing logical candidate object or are performed because rebuild/invalidation replaced prior candidate state. It must be derived from write events/object lineage, not hardcoded.

Endpoint state is reported separately:

- `durable_authoritative_bytes`;
- `durable_transformed_regenerable_bytes`;
- `warm_retained_state_bytes`;
- `persistent_bytes_removable_with_zero_information_loss`.

A zero value is lawful only when positively observed/proved. Missing telemetry is typed missing, never zero.

## 11. Scratch and durable high-water law

`peak_scratch_bytes` and `peak_scratch_file_count` are high-water marks over the entire candidate envelope or named phase, updated on write/delete events or sufficiently complete observation. One `_dir_stats` sample at phase end cannot be called a peak.

`durable_transformed_regenerable_bytes` is an endpoint retained-state size after the named operation and may lawfully use an exact filesystem/object inventory. It must not be repurposed as bytes-written.

`durable_authoritative_bytes` counts only retained candidate-root bytes positively classified as P1/P2/P3 authority/product/replay material by the frozen persistence law. Candidate-specific R5/CACC/cache bytes are not authoritative merely because they persist. A hardcoded zero without classification evidence is insufficient.

## 12. Rebuild / deletion / persistence law

The comparison must preserve candidate meaning rather than force identical physical actions.

- A pays actual A first materialization where required, actual reopen/reuse, and any lifecycle rebuild required by the frozen profile. A persistence-classification receipt is evidence, not a substitute for rebuild timing.
- B pays actual source-backed reconstruction/rebind and any transient-state deletion/regeneration required by the frozen profile. A B cache operation may be `NOT_APPLICABLE_BY_FROZEN_COURT`; that is not numeric zero.
- C pays only lawful accepted C physical state/accelerator work at that source. No rescue accelerator may be invented.

`delete_rebuild_wall_ns` names an actual deletion + regeneration/rebind/rebuild action. Receipt-writing time cannot populate it.

## 13. Invalidation law

Source-release and semantic-authority invalidation must execute the already-governed dependency/lifecycle operation or terminate typed-unmeasured if no lawful executable trigger exists.

For each invalidation event record:

- exact trigger identity/profile;
- exact candidate-owned objects/nodes invalidated;
- exact objects/nodes recomputed;
- observed wall/CPU;
- observed read/write/rewrite bytes;
- scratch/RSS high-water where required;
- post-invalidation semantic/output identity parity.

`recomputation_units` is the observed count of the frozen dependency-closure units actually recomputed. Formulae such as `1 + int(candidate...)` are model assertions, not measurements.

## 14. Stale / corrupt / interruption law

Behavior evidence must exercise candidate implementation state.

- stale-state test: alter or invalidate the governed determinant so retained candidate state is stale; observe rejection/rebuild/fail-closed behavior;
- corrupt-state test: corrupt candidate-owned regenerable state through the already-authorized lifecycle profile; observe detection/fail-closed/rebuild behavior;
- interruption test: interrupt the candidate's real build/session operation at the frozen lifecycle checkpoint and observe cleanup/resume/rebuild without admitting partial truth.

Hashing a law string or creating/deleting an unrelated generic partial file is documentary evidence only, not observed candidate behavior.

Where a behavior is genuinely inapplicable to a candidate under frozen law, emit `NOT_APPLICABLE_BY_FROZEN_COURT` with the governing reason/ref.

## 15. Metric state vocabulary

Every metric field has exactly one state:

- `MEASURED` — directly observed under this constitution;
- `NOT_APPLICABLE_BY_FROZEN_COURT` — the frozen candidate meaning makes the operation inapplicable;
- `NOT_REACHED_AUTHORIZED_STOP` — lawful stop occurred before the metric;
- `MEASUREMENT_NOT_CAPTURED` — work occurred/preserved but no qualifying telemetry exists;
- `INVALID_MEASUREMENT__ACCOUNTING_CONTRACT_BREACH` — a number exists but violates this constitution and is barred from comparison.

Only `MEASURED` numeric values enter resource comparison. Typed nonnumeric states remain evidence and cannot be coerced to zero.

A source×candidate cell is `METRIC_VECTOR_COMPLETE` only when every mandatory field is `MEASURED` or lawfully `NOT_APPLICABLE_BY_FROZEN_COURT`; an authorized correctness/source stop may instead terminalize the cell with `NOT_REACHED_AUTHORIZED_STOP` fields but cannot be called a complete performance vector.

## 16. Preserved semantic parity and performance

Parity truth belongs to the candidate-neutral oracle court, not to the candidate. Oracle materialization is C0. Candidate execution used to demonstrate parity is candidate work if it is also part of the frozen logical workload; pure duplicate verification overhead is reported separately and excluded from the primary performance vector.

Performance admission requires the independent parity contract, but this constitution does not define B02's oracle contents.

## 17. Mechanical acceptance conditions

A future P2X metric receipt satisfies this constitution only if a verifier can prove all of the following:

1. exact source×candidate key retained;
2. pre-candidate C0 identities frozen;
3. candidate start/stop ordinals/timestamps present;
4. candidate OS process identity unique from prior candidate;
5. candidate roots isolated;
6. no cross-candidate session object survives;
7. CPU totals accumulated without overlap/overwrite;
8. RSS is candidate-process-local;
9. I/O byte counters are observed events, not endpoint proxies;
10. scratch peaks are high-water observations;
11. cold/warm fields are write-once and cold-state predicate is proved;
12. preserved-work numeric credit passes Section 9;
13. deletion/rebuild/invalidation/recovery are actual operations or typed nonmeasurement;
14. no source-universe aggregation erases `source_id`;
15. no missing/null field is converted to numeric zero;
16. common upstream production is not repeated solely for symmetry;
17. candidate access to common inputs is not hidden as free work;
18. post-stop court administration is excluded;
19. exact output/product/semantic/replay identities remain bound to the metric vector;
20. no ranking, scalar score, or candidate selection is emitted by the accounting layer.

## 18. Constitutional terminal

These rules fully determine the accounting boundary required by Wave-2 B03. Current P2X code remains noncompliant until mechanically changed and requalified, but no unresolved accounting-definition question remains at this commission's grain.

Terminal:

`FIABC_W2_B03_EQUAL_WORK_ACCOUNTING_CONSTITUTION_PROVED`
