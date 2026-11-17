# ANVIL R7 — A0 INDEPENDENT DESIGN (architect A)

**Schema:** ANVIL_R7_A0_DESIGN@1
**Campaign scope:** C11_QUERY_DESIGN
**Stage:** A0 only. No A1, P15, P2, C, H1, reciprocal exchange or measurement is performed or claimed here.
**Designer lane:** independent architect A; blind to architect B's substantive work.
**Startup source cut:** `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`
**Prior tested baseline named by H0:** `b830458c3ebfe0a3f0e2d18e516e68b90324c88a`
**Protected head:** `7fc00289dd801d2d0a8ce159986c7595fc27a4d9`
**Protected capability constraint:** K3 terminal 29 historical families / 26 NOT_ADOPTED proposals / 14 held obligations; no K4.
**Proof grade of this document:** S0/S1 source-static design evidence at the exact startup cut. It is not a measured receipt, native/source/science grant, independent review, protected adoption or merge authority.

---

## 0. One-paragraph decision

The strongest incumbent adaptation is **not** a new C11 engine and **not** a claim that the prepared-session candidate is already economical. It is a composition of five already-present exact mechanisms — the Q2 body tee/bridge, the frozen S2-C 13-family writer, the S2-C/S2-D authenticated estate, the prepared saved admission/session, and the native I03/I05/Batch owners — plus **one bounded physical repair**: materialise the already-authenticated event and side-family bodies into the existing execution-local SQLite posting index so that repeated queries stop re-reading Parquet row groups per respondent. The unmodified prepared session (A1) is the measured fallback; the body-complete prepared index (A2) is the candidate that must earn its place under matched P15. A0 freezes the design and the falsifiers; it does not choose a measured winner.

---

## 1. Exact problem and selected consumer

H0 freezes the problem as: complete sealed 13-family corpus → fresh native I03/I05/Batch, plus economical 1/10/100 distinct operations, respondent-coherent 3-way joint/routing/negative/replay, at or below **6,442,450,944 bytes process-tree RSS**, with 22 mandatory H0 case-metrics in six workload families.

H0 names the first consumer:

```text
rawlsing_next/pre553_saved_c11_admission.py::SavedC11Admission.execute_i03 / execute_i05
```

with native I03/I05 and Batch retained, and the prepared-saved candidate inspected for actual continuity. This design keeps that consumer exact. It does not substitute a synthetic benchmark consumer, a new evaluator, or a new scientific issuer.

The material question is therefore:

> Can one authenticated complete 13-family estate be built once, opened cold in a fresh process, indexed once, and reused for 1/10/100 distinct native operations with exact fact/replay/negative conservation and ≤6 GiB process-tree RSS — without rebuilding C11 per operation?

The actual source already contains most of the answer. What is unproven is the 100k/6GiB and repeated-query economics, not the existence of a lawful composition.

---

## 2. Actual source inventory inspected

All blob identifiers below are `git rev-parse cea2d4d3:<path>` values at the startup cut.

### 2.1 Complete 13-family source → S2-B direct I02

`rawlsing_next/_pre553_direct_i02_sourcefree.py`
blob `451727511af7f727b082c518aae2f4a3dbe2ba3a`

- `_FAMILIES` is the exact 13-family map:
  `EmpiricalUniverse`, `RespondentIdentity`, `QuestionVariableBinding`,
  `RespondentEvent`, `RoutingEligibilityFact`, `EmpiricalCoordinateFact`,
  `WeightMeasureFact`, `AuthoritySnapshot`, `SourceUniverseRelation`,
  `EmpiricalPredicateReplayBinding`, `ComparatorReplayBinding`,
  `DiscoveryBranchReplayBinding`, `StructuralAdmissionReplayBinding`.
- `build_sourcefree_direct_i02(...)` consumes `SourcefreeDirectI02Sections`,
  checks identities/relations as rows are consumed, and produces direct-I02
  certificate roots without a `C11LogicalRelease`, `ReplayManifest.closure_refs`
  tuple or `C11Repository` object graph.
- It is explicitly a **direct** schema identity, not a fake v1 seal.

### 2.2 One-pass Q2 body transport and S2-C bridge

`rawlsing_next/pre553_source_i02_handoff.py`
blob `31d99b70b9e726ecd1b2413aa68d642df4dc8151`

- `build_source_i02_handoff(...)` accepts `body_sink: SourceI02BodySink | None`.
- The same one-shot 13-family objects consumed by the direct builder are
  synchronously teed to the sink. Source reads = 1, source decodes = 1, cell
  pass = 1 for the sourcefree fixture path; no second SAV/DTA decode.
- The body sink is committed against the published exact certificate roots;
  failure aborts the sink and invalidates the target.

`rawlsing_next/pre553_source_i02_streams.py`
blob `9547fe3d5972005c3bb96cb91083c39743cb2d0c`

- `SourceI02BodyTee.begin/emit/absence/finish` forwards the exact body
  transport; it does not create a second source read.

`rawlsing_next/pre553_source_saved_body_bridge.py`
blob `eddaa9a57eec4e44ce5d0ee5c223facae8d5775d`

- `SourceSavedBodySink.begin/emit/absence/finish` journals every exact typed
  family body as canonical JSONL in a private temporary stage, validates
  header/roots/manifest/counts/absences, then replays a pull iterator into the
  **unchanged** `write_direct_estate`.
- `stats` explicitly discloses `second_i02_certification_in_frozen_writer`,
  `journal_bytes`, `source_decodes_by_sink=0` and `full_c11_builds_by_sink=0`.
- The journal is deleted after commit; it is not a second durable corpus.
- Existing executable witness:
  `rawlsing_next/tests/test_pyat997_s1e_saved_source_bridge.py`
  blob `c3077ce89c05d6e39349c08468ce4022a3a6f506`, especially
  `test_q2_one_sav_to_complete_cold_saved_thirteen_families`. It asserts one
  source open, one decode, one cell pass, zero full-C11 builds, exact body
  transport, 14 Parquet members, no SQLite in the estate, and exact family
  iteration.

**Consequence:** the #997 “missing body iterator” is no longer honestly called
missing at this cut. A tested candidate bridge exists. The unresolved issues are
its 100k cost, scratch/journal peak, second certification, and first-consumer
integration economics — not the absence of a body ABI.

### 2.3 Frozen S2-C 13-family writer and authenticated estate

`rawlsing_next/pre553_source_direct_parquet_estate.py`
blob `e8622ac6bf59c4d1ec052e21410e63aab7dd9aa1`

- `write_direct_estate(source, universe_ref, authorized_private_root, chunk_rows=512, expected_i02=...)`
  is a one-pass tap over all 13 typed families, co-producing Parquet and the
  direct-I02 proof. It writes 13 `<Family>.parquet` members plus
  `event_locator.parquet`, all Zstandard-compressed (`_Sink`, `_IndexSink`
  lines 220–322).
- It verifies every emitted canonical body/ref/family against the same I02
  certificate, verifies physical ref uniqueness with a disk-bounded SQLite
  scratch, deletes the I02 proof scratch, hashes every committed member, and
  publishes by exclusive directory name plus an atomic `manifest.json` link.
- `EstateReceipt` carries path, manifest SHA-256, direct-I02 roots,
  reconstructed v1 release identity, family counts and retained bytes.
- `VerifiedDirectEstate.__init__` (line 612) requires an independently held
  manifest digest, exact direct-I02 roots and a live current/rights callback.
  It hashes **all 14 members** on every cold open, validates the complete family
  member set and census, and checks event/locator row-group topology.
- `iter_family` is bounded (`batch_size`), decodes through the existing codec
  and checks body/ref/family on every row. `_locators` is a bounded selector
  scan but is not the native prepared path.

The frozen writer remains the only S2-C writer. A0 does not propose a second
writer, a second body corpus, or a different manifest.

### 2.4 S2-D cold native readers

`rawlsing_next/pre553_direct_estate_i03.py`
blob `8825832f8067c7fce7a99a94505743cbb4eada06`

- `DirectEstateI03Session.__enter__` creates a private temporary directory under
  the estate root and an execution-local `postings.sqlite` with:
  - `events(respondent, ref UNIQUE, native, canonical, component, state, gid, off)`
  - `members(family, respondent, ref, gid, off, PRIMARY KEY(family,ref))`
- `_build` walks every event row group and every physical event body, checks
  positional locator coverage and full canonical body truth before insert, then
  walks `EmpiricalCoordinateFact`, `RoutingEligibilityFact` and
  `WeightMeasureFact` row groups to insert member locators. It never calls
  `pq.read_table`, never creates a full C11 graph and never stores a durable
  body corpus.
- `indices_for` returns one exact `_ReleaseIndex` with
  `native_verified_physical_respondent_order=True`, the scoped universe,
  respondent identities, and providers for events, coordinates, routing and
  weights.
- `_selected_events` resolves selected refs from SQLite and then reads event
  bodies from Parquet row groups per respondent/target.
- `_respondent_family` resolves member refs from SQLite and then reads the
  entire Parquet row group before selecting one offset. Its one-row-group cache
  is per family and is cleared when the group changes. This is correct but is
  the measured random-access amplification described in §5.

`rawlsing_next/_pre553_query_common.py`
blob `da536ff74ce526f53a802d37430382a7369ce993`

- `_ReleaseIndex` is the exact consumer-facing index ABI. It carries the
  release identity, universe, respondents, per-respondent event selectors,
  coordinates, routing, weights and source relations. The
  `native_verified_physical_respondent_order` flag is opted in only by the
  authenticated direct-estate session.

`rawlsing_next/pre553_empirical_query.py`
blob `8885e637eb176946c8496671ff49ee70665b3bc6`

- `execute_empirical_query(...)` is the original native I03 semantic owner.
  It accepts only `C11Repository` or the exact `DirectEstateI03Session` type,
  verifies query/predicate identity and authority fitness, parses the target
  plan (including multi-target joint domains), resolves the release index,
  evaluates denominator/routing/target/weight semantics, and returns typed
  `EmpiricalFact` objects or typed negative facts.
- `replay_empirical_query(...)` is the native deterministic replay owner.
- `I03GroupedExecutionScope` exists but grouped native I03 cache is explicitly
  refused for a cold sourcefree estate at this cut.

`rawlsing_next/_pre553_query_eval.py`
blob `87849f7cc41a2d4647582aba2eae00ab4531b90b`

- `_evaluate_index_group_core` enumerates the exact risk population, resolves
  routing membership, condition truth, target support, denominator members,
  raw numerator/denominator and weighted numerator/denominator.
- For multi-target queries the same respondent must satisfy the joint target
  topology; the denominator is shared, not a per-target marginal set.
- `_evaluate_index_group` is the exact grouped/cache path.

`rawlsing_next/pre553_discovery_exact.py`
blob `1b82b6df993bf14afa5e78782d988cba6e76b668`

- `execute_exact_bounded_discovery(...)` (line 1052) is the native I05 owner,
  taking the same bounded repository view and exact discovery authority.

### 2.5 Saved admission, prepared session and Batch

`rawlsing_next/pre553_saved_c11_admission.py`
blob `22749addc1fca5f0b90e12728847c390aafa7a84`

- `SavedC11Admission.open(...)` requires the independently held manifest
  SHA-256, exact `ExternalI02Roots`, reconstructed v1 release ref, exact
  `RuntimeObjectCatalog` and a live current authorizer. It re-verifies the
  estate into a private reader, snapshots the catalog, constructs the existing
  `CarrierNeutralResearchExecutor`, and freezes its binding.
- `execute_i03` and `execute_i05` are the H0 first consumer. Both check current
  before and after the operation.
- The estate/release/universe/source scope checks refuse foreign scope.
- `SavedReleaseIdentity` is identity-only, not a v1 release or validation seal.

`rawlsing_next/pre553_prepared_saved_i03.py`
blob `bcb146edae680028e027e47cae45891693f63526`

- `PreparedSavedC11Admission.prepared_i03()` opens one exact
  `DirectEstateI03Session` and yields a `PreparedI03Session` that reuses it for
  many operations.
- `PreparedI03Session.execute_i03` re-resolves the exact query/predicate,
  checks the query condition identity, calls the original
  `execute_empirical_query`, re-checks current, and increments the operation
  count.
- `execute_i05` calls the original `execute_exact_bounded_discovery` with the
  same shared session.
- `close()` exits the underlying session, deleting the temporary SQLite index.
- Existing executable witness:
  `rawlsing_next/tests/test_pre553_prepared_saved_i03.py`
  blob `29ac46f252e26131086ed555265d72029d280dda`:
  one index build for four I03 operations, exact fact/projection parity,
  revocation refusal and restore, condition mismatch refusal, and prepared I05
  frontier/receipt parity.

`rawlsing_next/pre553_batch_runner.py`
blob `49e3974c658d66a270815d9faa3798b40d4488b1`

- `BatchExecutionRunner.__init__` accepts `C11Repository` or, when
  `saved_mode=True`, the exact `SavedC11Admission` type; it resolves every
  unit's release through `resolve_release_exact`.
- Deterministic sequential scheduling, unit receipts and pending/retry logic
  are the existing Batch owner.

`rawlsing_next/pre553_saved_workload_integration.py`
blob `cc8aa32512378261406d765f0b049c748cb3e11f`

- `execute_saved_batch` drives the existing runner with `saved_mode=True`.
- Its executor calls `admission.execute_i03` / `execute_i05` per unit. Because
  the base admission opens a fresh `DirectEstateI03Session` per call, **Batch
  currently does not reuse the prepared session**.
- `type(admission) is not SavedC11Admission` at lines 42, 54 and 94, and
  `type(repository) is SavedC11Admission` at `pre553_batch_runner.py:406`,
  reject the `PreparedSavedC11Admission` subclass by exact type. This is a real
  ABI defect for the prepared Batch path, not a missing capability in the
  evaluator.

### 2.6 Not used

`rawlsing_next/pre553_c11_repository.py` (`C11Repository`,
`C11LogicalRelease`) remains the legacy in-process full-object repository. The
design deliberately does not construct it. A full C11 build is not a
prerequisite for scoped C11 query work and is a known memory failure route.

---

## 3. Candidate A0 architecture

### 3.1 Name and claim

**A0-A: Prepared, Body-Complete Cold Saved Estate (BCPPI) — compose/adapt/repair.**

Claim to be tested later: one complete 13-family sealed estate, one cold
admission, one execution-local body-complete posting index per process, and
native I03/I05/Batch operations across that index can satisfy the H0 problem
within 6 GiB at 100k scale. This is a design claim only.

### 3.2 Build path (source-free at P15; original source separately held)

```text
Q2 one-pass S1-B/S2-B source projection
  -> build_source_i02_handoff(body_sink=SourceSavedBodySink)
     - one source open / one decode / one cell pass
     - exact 13 typed family bodies tee'd
  -> SourceSavedBodySink.finish(roots, manifest, counts, transport)
     - journal census/absence/header checks
     - replay exact pull iterators into unchanged write_direct_estate
     - expected_i02=roots
  -> write_direct_estate
     - 13 family Parquet/Zstd + event_locator
     - complete I02 proof + physical body/ref/family verification
     - atomic manifest link
  -> EstateReceipt(path, manifest_sha256, i02, reconstructed_v1_release_ref,
                   family_counts, retained_bytes)
```

**Exact ABI obligations:**

- `SourceSavedBodySink.finish` must receive the exact Q2 transport and must
  reject any family/count/absence/header drift.
- `write_direct_estate` is called with the unchanged signature and
  `expected_i02=handoff.roots`; any root drift is a hard failure.
- The estate must contain all 13 family members plus `event_locator.parquet`
  and `manifest.json`; no `.sqlite`, journal or second body store may survive.
- One source open and one decode are required; a second decode is a reverser,
  not an optimization.
- Original-source use remains a separate S1-B/S1-D permission event. A0/P15
  sourcefree evidence does not grant it.

**Costs:** the bridge adds a temporary JSONL journal approximately equal to
canonical body bytes, and the frozen writer performs a second I02
certification. Both must be counted in `scratch_peak_bytes` and
`build_wall_s`. Removing either is a proof-scope change requiring owner
decision; A0 does not silently weaken it.

### 3.3 Cold admission path

```text
VerifiedDirectEstate(root, exact_path, held_manifest_sha256, held_i02,
                     current_authorizer)
  - hashes all 14 members, checks complete family set/census/topology
SavedC11Admission.open(...)
  - re-verifies into a private reader
  - binds exact release/universe/catalog/current
PreparedSavedC11Admission.open(...)
  - the same inherited construction; no new authority
```

No C11 repository, no C11LogicalRelease, no full replay closure, no source
reopen, no durable index. Every materialising call re-checks the external
current/rights callback.

### 3.4 Prepared index: A1 fallback and A2 repair

**A1 (unmodified candidate, already measured).** One
`DirectEstateI03Session` per process; `PreparedI03Session` reuses it. Index
build happens once, but query evaluation still resolves side-family bodies by
reading the entire Parquet row group per respondent/ref and event bodies by
row-group reads per respondent/target.

**A2 (candidate repair; not implemented or measured in A0).** Extend the
*existing* execution-local SQLite index with the exact `body_json` of the
authenticated event and the three I03 side families:

- `events` gains `body_json TEXT NOT NULL`;
- `members` gains `body_json TEXT NOT NULL`;
- `_build` inserts the already-read, already-body-truth-checked event
  `body_json`, and inserts the three side-family bodies after decoding and
  checking `type/ref/respondent/universe`;
- `_selected_events` and `_respondent_family` decode from SQLite by exact ref
  instead of reading Parquet row groups;
- all existing validations remain: exact body/ref, family type, respondent,
  universe, positional locator coverage, census, current/revocation;
- the index remains temporary, private, process-local, deleted on close; no
  durable SQLite, no new persistent corpus, no new evaluator.

This is a physical access-path repair, not a semantic change. It reuses the
same SQLite file the reader already creates. Its cost is additional scratch
bytes and index-build CPU; its benefit is removal of O(respondents × families)
row-group reads per operation.

**Why this is necessary rather than speculative:** the prior sourcefree return
measured 71,304 row-group reads for 20 prepared operations on only 64
respondents (3,565 reads/op). At 100k respondents, a linear continuation is not
an economical 100-operation path even though the index rebuild is amortized.
The prepared session removes rebuild cost but does not remove the respondent-
major Parquet random-access cost.

### 3.5 Native readers on the prepared index

- **I03:** `PreparedI03Session.execute_i03` → `execute_empirical_query`.
  Query/predicate exact resolution, condition identity, scope, authority,
  routing/risk, denominator, target topology, weights, typed negatives and
  replay remain the native owner.
- **I05:** `PreparedI03Session.execute_i05` →
  `execute_exact_bounded_discovery` with the same bounded session.
- **Batch:** the existing `BatchExecutionRunner(saved_mode=True)` must execute
  all units inside one prepared context. Minimal exact change:
  1. widen the exact-type guard in `BatchExecutionRunner.__init__` from
     `type(repository) is SavedC11Admission` to an explicit closure of
     `SavedC11Admission` and `PreparedSavedC11Admission` (still rejecting all
     duck types and arbitrary subclasses);
  2. in `execute_saved_batch`, accept the prepared admission, enter
     `prepared_i03()` once around `runner.run(...)`, and have the QUERY /
     DISCOVERY executors call the prepared session, not the base admission;
  3. keep `resolve_release_exact` identity-only and keep all current/fate
     checks.
  If the Batch owner does not grant this exact two-function change, Batch stays
  on the one-index-per-unit path and is reported as a conditional result; I03
  and I05 remain honest.

No monkeypatch, no fake `C11Repository`, no guard bypass.

### 3.6 Negative, restore and replay

- Typed negative facts come from the native evaluator (`_negative_result`,
  `_negative_for_index`) and must preserve `p01/p02` failure state, zero/absent
  distinctions, `UNAVAILABLE` risk set, and `ZERO_SUPPORT` versus
  `OBSERVED_ZERO`.
- Revocation is the existing current-callback refusal; restore is the same
  callback returning true. The prepared session must refuse mid-operation and
  refuse a closed session.
- Replay is `replay_empirical_query` and the native replay/ref identities; a
  prepared A2 body cache must not bypass replay or serve stale bodies after a
  failed current check.
- Tamper/restore must include: altered member hash, altered manifest, missing
  family, duplicate/equal-count locator, forged body/ref, revoked authority,
  and restored exact estate. Failure must be typed refusal, never EMPTY/ZERO.

---

## 4. Workload families and the 22 H0 cells

H0 froze 22 cell IDs but did not freeze workload profile counters. The
following profile semantics are **A0 proposals to be frozen by the P15
controller before any comparison**; they are not executed profiles and must not
be treated as validated `ANVIL_PLAN` data.

| Family | Proposed semantics (to freeze) | H0 cells |
|---|---|---|
| **W-S** sealed scale | 100,000 distinct respondents × 3 occasions, complete 13-family estate, sparse 5-question core + one governed weight; fresh process per count; 1/10/100 distinct I03 operations. | build_wall_s, cold_open_wall_s, query_1/10/100_wall_s, process_tree_peak_rss_bytes, retained_bytes, scratch_peak_bytes |
| **W-D** dense width | 100,000 distinct respondents × 300 columns, high response density; question-major and respondent-major projections; 1/100 distinct operations. | build_wall_s, query_1/100_wall_s, process_tree_peak_rss_bytes, retained_bytes, scratch_peak_bytes |
| **W-R** routed | 100,000 respondents with exact routing/eligibility and a conditional cohort/risk set; one conditional I03 operation. | query_1_wall_s |
| **W-O** operations | 100,000 respondents × 20 columns; 1/10/100 distinct operations split into disjoint and overlapping exact query scopes. | query_1/10/100_wall_s |
| **W-J** joint | 100,000 respondents × 20 columns; one 3-target query with true same-respondent joint topology and a shared exact denominator; 10/100 distinct joint operations. | query_10/100_wall_s |
| **W-X** cold/negative/restore | Cold close/reopen, tamper/denied/restore, revocation/restore and exact replay on the same sealed estate. | cold_open_wall_s, process_tree_peak_rss_bytes |

All metrics are wall seconds, bytes, or exact parity receipts. No metric in
this table has been executed at A0.

The six families must not be collapsed into one synthetic fixture. In
particular, W-D dense width cannot be claimed from W-S sparse counters, and W-J
joint cannot be claimed from three independent marginals.

---

## 5. Storage, index, query, proof and recovery costs

### 5.1 Sourced anchors (evidence, not new measurements)

From `WORKER_RETURNS/PYAT_P0_C11_OPERABLE_20261115_R1/evidence/summary.json`
and its `00_RETURN.md` at the startup cut (sourcefree TEST_ONLY, owner grant
pending):

| Anchor | 128 R × 5 Q, 100 ops | 64 R × 30 Q, 20 ops |
|---|---:|---:|
| baseline wall | 213.456 s | 142.996 s |
| prepared wall | 126.424 s | 83.873 s |
| speedup | 1.688× | 1.705× |
| baseline session builds | 100 | 20 |
| prepared session builds | 1 | 1 |
| baseline row-group reads | 28,076 | 121,882 |
| prepared row-group reads | 17,384 | 71,304 |
| RSS peak baseline → prepared | 97.6 → 89.1 MB | 263.9 → 162.9 MB |
| temp SQLite peak | 1.70 MB | 4.71 MB |
| index build | 0.412 s | 2.403 s |
| retained estate | — | 39,609,311 B |
| writer | — | 29.954 s + 3.196 s fixture |
| cold admission | — | 0.423 s |
| first query | — | 1.587 s |

Historical 100k facts (different old code path, explicitly not S2-C):
old W03 ~777.5 s total, ~292.5 s persistence, ~124.5 s first consumer,
5,923,426,304 B persistence RSS; a later saved-artifact pilot peaked
6,468,513,792 B > 6 GiB and was killed. These are evidence anchors and
falsifiers, not this candidate's measurements.

### 5.2 Cost model (sourced estimates, not measurements)

Let `E` = event count, `R` = respondent count, `T` = targets per query,
`O` = distinct operations, `S` = retained estate bytes.

- **Cold open / member authentication:** `T_open ≈ 0.011 s/MB × S` from the
  0.423 s / 39.6 MB anchor. At S = 1–3.5 GB this is ~11–38 s. All 14 members
  are hashed; this is proof cost, not avoidable without changing the accepted
  reader.
- **A1 index build:** `T_index ≈ (0.6–1.5 ms) × E`. At E = 200k–600k this is
  ~120–900 s. One build per process, not per operation.
- **A2 index build:** A1 plus SQLite body insertion; estimate 1.2–2.5× A1,
  i.e. ~150–2,000 s, with scratch growth of roughly one serialized body copy.
- **A1 per-operation evaluation:** the measured 3,565 row-group reads/op at
  64 respondents implies a respondent-major amplification. A linear estimate
  at 100k respondents is not defensible as an economy claim; it is the primary
  reason A1 is only a fallback. Range: ~5–100+ s/op if unimproved.
- **A2 per-operation evaluation:** exact SQLite point lookups per
  respondent/target plus native evaluation; estimate ~0.05–3 s/op at 100k
  depending on targets, weights and SQLite page locality. 100 ops: ~5–300 s
  plus the one-time build.
- **Retained bytes:** the 64 R × 30 Q estate is 39.6 MB. Event-dominated
  extrapolation to 100k × 3 is ~0.5–2.5 GB, but the fixed 13-family overhead,
  body_json + typed-column duplication and Zstd ratio make this a wide
  estimate. It is a P15 falsifier, not a claim.
- **Scratch peak:** bridge journal + Parquet stage + I02 proof SQLite +
  physical-ref uniqueness SQLite + A2 body SQLite. At 100k this can plausibly
  be several GB of transient disk even when RSS stays below 6 GiB. The prior
  preflight host had ~4.57 GB free disk, so disk space is itself a first-class
  risk. P15 must record `scratch_peak_bytes` and the actual free-disk floor.
- **RSS:** A1 measured 89–163 MB on tiny estates. A2 adds SQLite page traffic
  but should stay bounded because bodies are streamed and not held as Python
  objects. A 0.3–1.0 GB estimate at 100k is plausible; it is not evidence.
  The old 6.468 GB saved-artifact failure shows how a different materialization
  strategy can cross the cap without warning.
- **Recovery:** there is no durable index. Process kill loses only the derived
  index; the sealed estate remains. Re-open re-hashes 14 members and rebuilds.
  There is no crash-interruption recovery receipt for this candidate. A1/A2
  must not claim durable interrupted-operation recovery.

All numbers in this section are **sourced estimates or explicit unknowns**,
except the anchored measurements cited in §5.1.

---

## 6. Workload-to-mechanism trace

| Requirement | Exact current owner | What A0 adds |
|---|---|---|
| complete sealed 13-family corpus | `write_direct_estate` + `build_sourcefree_direct_i02` | nothing; compose unchanged |
| body iterator from one source pass | `SourceSavedBodySink` + `SourceI02BodyTee` | nothing; use tested candidate |
| fresh cold open with independent pins | `VerifiedDirectEstate` + `SavedC11Admission.open` | nothing |
| economical repeated ops | `PreparedI03Session` | A2 body-complete temp index; A1 fallback |
| native I03 semantics | `execute_empirical_query` | nothing |
| native I05 semantics | `execute_exact_bounded_discovery` | nothing |
| Batch reuse | `BatchExecutionRunner(saved_mode=True)` | two-function prepared-mode owner edit |
| same-respondent 3-way joint | multi-target `EmpiricalQuerySpec` + `_ReleaseIndex` | nothing; exercised through prepared session |
| routing/risk | `RoutingEligibilityFact` + `_routing_fact_for` | nothing |
| typed negative/zero | `_negative_result` / `_negative_for_index` | nothing |
| exact replay | `replay_empirical_query` | nothing |
| current/revocation/restore | `SavedC11Admission.check_current` | preserve exact before/after checks |
| proof/recovery | manifest + member hashes + permanent estate | no durable index claim |

---

## 7. Strongest self-objection

**The prepared session is an index-rebuild optimization, not yet a 100k
query-economics proof.** The measured 1.69–1.70× speedup is real but is
dominated by eliminating repeated session builds on tiny fixtures. The measured
3,565 row-group reads per prepared operation on only 64 respondents is a
warning that the respondent-major Parquet path does not scale economically to
100k × 100 operations. A2 is a plausible repair, but it is **unimplemented and
unmeasured**; it grows the execution-local SQLite scratch, may increase index
build time, and could still fail the 6 GiB or disk budget. The body-json plus
typed-column duplication in the frozen writer, the second I02 certification,
the full 14-member cold hash, and the native fact/replay materialization cost
all remain. A rival that stores a compact persistent respondent-major index or
a dense typed substrate at writer time could be materially better on W-D/W-O,
and an eager typed compact design could beat A2 on repeated cold F4. Without a
matched 100k P15, A2 must not be called economical, and A1 must not be called
a modern production speedup. The design's strongest claim is only that it is
the most lawful incumbent composition with an exact, measurable repair path.

---

## 8. Decision-changing falsifiers

1. **RSS veto.** Any W-S/W-D/W-X measured process-tree peak above
   6,442,450,944 B kills the candidate as stated. Reverser: A2 or the
   persistent-index rival must reduce materialized objects, not just wall time.
2. **Retained/scratch veto.** If retained + scratch exceeds the agreed compact
   budget, or if the 100k build runs out of disk before a complete sealed
   estate, the candidate is not economical even if RSS passes.
3. **Row-group amplification.** If A1's W-S 100-operation row-group reads
   scale linearly with respondents (or A2 does not materially reduce them),
   A1/A2 loses to a respondent-major index rival. This is the decisive
   mechanism-level falsifier.
4. **Joint correctness.** Any W-J 3-way same-respondent fact whose denominator,
   per-respondent joint support or cell projection differs from the native
   in-memory oracle is a semantic failure, not a performance tradeoff.
5. **Routing/negative correctness.** Coercing an unresolved routing state,
   zero-risk-set state or typed negative into EMPTY/ZERO/membership reverses
   the design.
6. **Source bridge integrity.** A second source decode, missing family,
   absence/count drift, journal omission, duplicate/equal-count locator,
   forged body/ref, or surviving journal/SQLite in the committed estate
   reverses the build path.
7. **Current/revocation.** A served result after mid-operation revocation, or
   a failure to restore after the exact current callback returns, reverses the
   admission path.
8. **Batch ABI.** If the Batch owner refuses the prepared-session edit, Batch
   remains one-index-per-unit; any claim of prepared Batch economy is
   withdrawn, not inferred from I03.
9. **Build wall.** If W-S `build_wall_s` materially exceeds the P15 frozen
   bound (the old 100k 3,033.7 s writer anchor is the comparison point), the
   one-time construction claim is not economical; a new build path is an owner
   decision, not a silent substitute.
10. **Rights/source.** If the exact source or rights callback is not valid for
    the selected input, no measurement may be represented as native/source
    evidence.

---

## 9. Five-part law dispositions for named historical method capital

| Historical asset | Disposition | Exact current successor / reason |
|---|---|---|
| V549 respondent branch mask | `PRESENT_COMPOSED_NO_BUILD` | `RoutingEligibilityFact` + `EmpiricalPredicate` + `_routing_fact_for`; preserve as oracle only. |
| V550 shared country prefetch | `COMPARE_ONLY_UNKNOWN` | Single sealed estate does not need cross-country prefetch; cross-universe authority is separate and not selected. |
| V550J corespondent prepared joint | `PRESENT_COMPOSED_NO_BUILD` | Multi-target `EmpiricalQuerySpec` with same-respondent joint domain and shared denominator; historical code not ported. |
| F26 query-signature cache | `HISTORICAL_REJECTED_PRESERVE` | A process-local prepared index is lawful; a stale persistent query-signature cache is not. |
| F03/F08 source-semantic rules | `PRESENT_COMPOSED_NO_BUILD` | S1-B/S2-B typed projection and the bridge consume exact objects; no reinterpretation in this design. |
| V553 temporal index | `NO_JUSTIFIED_CONSUMER` in this scope | Temporal admission is a separate route; not needed for C11 query design. |

No historical function is promoted to a new build requirement by this table.

---

## 10. Source, semantic and physical reversers

**Source reversers:**
- Q2 body transport not exactly the 13 declared families;
- source opened or decoded twice;
- manifest counts/absences/family yields disagree;
- original-source rights/current callback invalid;
- any attempt to treat the fixture identity as an original source.

**Semantic reversers:**
- target topology/arity/domain mismatch;
- same-respondent joint denominator replaced by independent marginals;
- routing/risk state coerced to membership or nonmembership;
- weight applied outside the exact denominator;
- negative state lost or converted to EMPTY/ZERO;
- replay identity/fact mismatch;
- foreign universe/release/query/predicate scope accepted.

**Physical reversers:**
- any of the 14 member hashes mismatch;
- event/locator positional coverage or row-group topology mismatch;
- duplicate or equal-count forged locator accepted;
- body/ref/family identity drift;
- committed estate contains a journal, SQLite or second body store;
- prepared index survives close or is reused across a retargeted admission;
- process-tree RSS > 6,442,450,944 B;
- scratch/retained budget exceeded;
- Batch subclass guard bypassed by duck typing.

---

## 11. Proposed matched P15 probes (not run)

The controller must freeze exact profiles, fixtures, host, runner and counters
**before** the first comparison. A0 proposes, but does not execute:

1. **P15-P0 profile freeze:** write W-S/W-D/W-R/W-O/W-J/W-X counters,
   generator seed, respondent/event/slot cardinalities, question widths,
   routing/weight/negative cases, exact operation lists and expected fact
   oracle. Hash each profile file.
2. **P15-P1 build:** sourcefree one-pass Q2 → bridge → frozen S2-C writer;
   record build wall, fixture wall, journal bytes, I02 scratch bytes, physical
   uniqueness scratch, retained bytes, process-tree RSS samples, exact
   13-family counts and manifest hash.
3. **P15-P2 cold open:** fresh process; `VerifiedDirectEstate` +
   `SavedC11Admission.open`; record open wall, member-hash time, RSS, failure
   cases (missing member, altered hash, altered manifest).
4. **P15-P3 A1/A2 index:** one process each; build the unmodified prepared
   session and the A2 body-complete session; record index wall, SQLite bytes,
   row-group reads (instrumented), RSS, exact operation parity.
5. **P15-P4 repeated operations:** 1/10/100 distinct I03 and I05 operations;
   same exact catalogs and inputs; record wall, facts, full fact SHA-256,
   typed state, numerator/denominator, replay ref; compare against native
   in-memory oracle and baseline.
6. **P15-P5 joint/routed/negative/replay:** W-J 3-way same-respondent joint,
   W-R conditional routing/risk, typed negatives, revocation/restore, tamper/
   denied/restored, replay equality.
7. **P15-P6 Batch:** only after the exact owner edit; one prepared context over
   a manifest with QUERY and DISCOVERY units; compare with baseline unit
   receipts and exact refs.
8. **P15-P7 14 candidate-veto receipts:** one exact receipt per H0 veto:
   source semantics/routing; true same-respondent joint; fault/tamper denied/
   restored; source rights currentness; nonpreclusion; measurement input
   comparability; full decision dependency closure — plus the seven physical/
   ABI conditions named in §10.
9. **P15-P8 evidence:** store raw logs, counters, hashes, fixture/profile
   hashes, host/runner identity and exact source cut under an evidence root.
   No fabricated B run, no missing-B win, no tiny-fixture substitution for
   100k.

Source-only runnable falsifiers (specified, not executed):
- `python3 -m pytest rawlsing_next/tests/test_pre553_prepared_saved_i03.py rawlsing_next/tests/test_pyat997_s1e_saved_source_bridge.py rawlsing_next/tests/test_pyat991_s2d_five_readers.py -q`
- a P15 probe driver that imports `pyat1001_scale_harness.ProcessTreeObservation`
  and records RSS/scratch/retained around one fresh process per cell;
- a hostile probe that mutates the event locator, member hash, manifest,
  journal family count, and current callback, asserting typed refusal and
  exact restore;
- a joint-oracle probe comparing 3-way same-respondent facts against the
  native in-memory evaluator.

These are proposals. A0 claims none of them ran.

---

## 12. Unrun and held limits at A0

- No P15, no 100k, no native performance run, no measured receipt.
- No original-source access, original35 execution, S2/S3, science, actor or
  host grant.
- No edit to any product/source file; no Batch owner edit; no P2; no C or H1.
- No protected merge, protected CAS, branch rewrite or other worker's output.
- No claim that A1/A2 passes 6 GiB, disk, retained or build budgets.
- No claim that the prepared session is adopted; it remains an additive
  candidate pending owner qualification.
- No claim that a tiny fixture represents dense, sparse, joint or routed
  coverage.
- No claim that K3 29/26/14 is a new K4 or a build backlog.
- No reciprocal exchange with B and no access to B's substantive return.

---

## 13. A0 verdict

**A0_FROZEN** for the design only:

- selected candidate: **A0-A BCPPI** (compose Q2 bridge + frozen S2-C writer +
  authenticated estate + prepared admission + native I03/I05, with A2
  body-complete temp index and A1 measured fallback);
- exact first consumer: `SavedC11Admission.execute_i03/execute_i05`, with
  native I03/I05 and Batch retained;
- strongest challenge: A1's measured row-group amplification and A2's
  unmeasured scratch/RSS; neither is an economy proof at 100k;
- decision-changing falsifiers: §8;
- next eligible stage: one reciprocal A1/B1 exchange after both A0/B0 are
  frozen, then matched P15 under the controller's pre-result frozen plan.

No measured winner is declared. No rights or protected status are promoted.
