> **HISTORICAL / SUPERSEDED_BY_FINAL.** Authoritative final state: `S2_S3/FINAL_ARCHITECTURE.md`, `S2_S3/FINAL_DECISION.json`, `S2_S3/SPECIALIST_ADJUDICATION.md`, `S2_S3/FINAL_OBLIGATION_CROSSWALK.tsv`, `RETURN.md`. This file is preserved as prior evidence only; its PENDING/provisional/SC-ESTATE statements are not live.

# S2/S3 — PROVISIONAL INTEGRATED ANALYSIS

**Status:** `PROVISIONAL_PENDING_TWO_SPECIALIST_RETURNS`.
**Not frozen:** no final selected decision, no independent C, no H1, no native
grant.
**Frame:** `S1/FRAME.json` (`7e7bfb9638f23894fd244a703e8a6b88d361f90fafa5b2b10ac78c1f24229913`),
author checkpoint commit `5a619ff9fa79be9183eb4d4378d42f040ef2bd9b`, separately
frozen by HQ as `evidence/S1_FROZEN`. No independent S1 acceptance is claimed.
**Structural packet:** `S2_S3/PROVISIONAL_DECISION.json`, local guard
`PASS_LOCAL_INTEGRATED_DECISION_PENDING_C` (16 requirements, 118 identity rows).
**Provisional crosswalk:** `S2_S3/OBLIGATION_CROSSWALK.tsv` (118 identities +
16 requirements + 3 separate-estate navigation rows).

## 0. Grade correction

The accepted instrument's 16 requirement narratives and 118 identity rows are
used here for **structural coverage and exact source pins only**. They are not:

- an independent source-owner re-review of current code;
- a native-grade `CURRENT_PRESERVED` finding;
- acceptance of this candidate;
- adoption of the prepared `DECISION.json` or `C.json`.

The candidate-specific physical effects and the leading direction below are
author analysis at `CONDITIONAL_DIRECTION`. No source fate is promoted. The 26
PYAT-PC rows remain `NOT_ADOPTED`; the 14 P4R rows remain `HELD`; F26 remains
the exact source-owner hold. The 52/24/21 #1097 estate is navigation/negative,
not additive tickets.

## 1. The actual engineering problem

The current accepted route is semantically careful but physically
over-serialized. On a sourcefree 100k-shape witness (#1097, cut-specific, not
production):

| Phase | Measured | Why it is there |
|---|---:|---|
| writer wall | 3033.723 s | one 100k-shape write |
| retained estate | 310.16 MB | Parquet/Zstd canonical body estate |
| staging peak | 5.26 GB | stage + I02 + uniqueness scratch |
| temporary writer I02 | ~4.39 GB | SQLite proof corpus |
| native session index | 1.30 GB | per-session `events`/`members` SQLite |
| one selected query | 562.362 s | after the session index is built |

The code path explains the shape:

1. Q2 decodes the source once, projects 13 typed families, and builds direct
   I02 certificate **#1**.
2. `SourceSavedBodySink` writes 13 temporary JSONL family journals and replays
   them into frozen S2-C.
3. S2-C builds direct I02 certificate **#2**.
4. S2-C re-reads every Parquet row, decodes `body_json`, recomputes `_row`, and
   compares every typed/identity/occurrence lane.
5. A fresh process hashes every estate member.
6. `DirectEstateI03Session._build` scans all event and side-family row groups to
   build a temporary SQLite index.
7. Only then does one native I03 query execute.

The redundancy is not a semantic requirement. It is a composition of two
independently accepted components that were never jointly optimized. The
semantic authority (native I03/I05/F1–F4 and the I02 roots) can be preserved
while removing the duplicate certification, JSONL replay, per-row re-encode and
per-session full scan.

## 2. Provisional leading direction — SC-ESTATE

**Name:** Single-certification canonical C11 estate + immutable derived access
index + shared evidence fragments.

**One sentence:** compile the one-pass Q2 typed 13-family stream into one
canonical Parquet/Zstd estate certified once by the independent I02 roots and
per-row-group physical digests; build a rebuildable, manifest-bound selector/
denominator index once per release; run the existing native evaluators over
lazy selected row groups; emit content-addressed evidence fragments that share
risk/denominator work.

This is a **physical/computational** change, not a new science engine.

### 2.1 Source → C11

- One SAV/DTA source snapshot decode per release.
- The Q2 stream carries native question/option/form/translation/routing/missing,
  respondent and occurrence identity, repeated/ranked topology, weights,
  design/strata/PSU, authority/current and typed absence.
- The C11 compiler consumes that stream once. It does **not** write 13 JSONL
  journals and does **not** build a second I02.
- The canonical row is generated once: exact `body_json` + typed query
  projection columns + locator fields. The dual representation is deliberate:
  - body-only would force JSON parse on every query and lose typed pruning;
  - typed-only would lose exact body/replay/refs;
  - generating both once is the correct trade.
- The I02 logical root is computed streaming over the exact object/selector
  semantics (per-family Merkle roots over canonical sorted object bytes and
  selector postings). The physical root is a per-row-group digest over exact row
  bytes plus the member manifest. Both are in the manifest; both are checked.
- Publish is atomic: stage in an owner-private directory, fsync, publish
  members, link the manifest last, no clobber. A failed build leaves no valid
  release.

### 2.2 Derived access index

At publish, build one immutable sidecar:

- per-respondent event offsets sorted by `(respondent, question, occurrence)`;
- native/canonical/component selector postings;
- risk/denominator basis keys: eligible / asked / observed / refused /
  inapplicable / routing-unknown;
- per-family respondent offsets for coordinates, routing and weights;
- row-group min/max and optional bloom statistics.

It contains **keys and locators only**. It never contains bodies, authority or
source truth. Its root is bound into the manifest. It is derived from the
canonical estate and can be rebuilt from it. A missing, changed, stale or
revoked index refuses; it never overrides the manifest/I02/source guard.

This replaces the per-session SQLite scan with a read-only memory-mappable
index. Fresh-process open becomes O(manifest + index root + selected row
groups), not O(all events). The existing `PreparedI03Session` already shows the
right amortization in one process (one `_build` for four distinct operations);
the durable index makes that survive process exit.

### 2.3 Native execution and evidence output

- Keep `execute_empirical_query` and `execute_exact_bounded_discovery` as the
  semantic authority. The physical adapter presents a lazy `_ReleaseIndex` view
  backed by the durable index and selected row groups.
- I03: exact query condition/predicate → eligible postings → lazy body read →
  native risk/denominator/authority/fact/replay.
- I05: same view for bounded discovery; branch/minority/recursive receipts
  unchanged.
- F1–F4: native composition over the facts; true same-person k≥3 and directional
  denominators; no pairwise substitute.
- Batch/NORMAL/resume: reuse the existing `pre553_saved_workload_integration`
  adapters; complete the shared-file owner ACKs rather than silently editing
  shared owners.
- Evidence: one operation emits a content-addressed fact fragment, a small
  receipt, and a replay delta. Risk sets and denominator bases are stored once
  and referenced. Full fact/replay materialization remains available on demand.
  This avoids O(corpus) output per query.

### 2.4 Downstream boundary

The estate preserves the information needed for F5–F8, N9/N10E/N10W, PRE-V3,
N11/N12, SEAM and SOROK, but it does not issue them. FF01 descriptive ≠ FF02
structural/material; N9 world ≠ N10W situated possibility ≠ SOROK actor.
Encounter/access/consent are separate. No survey-to-actor private knowledge, no
opinion-to-institutional-power, no fictional-to-observed backflow.

## 3. Alternatives considered

| ID | Approach | State | Why |
|---|---|---|---|
| A | Keep current two-I02 + JSONL + per-session SQLite | RULED_OUT | measured 3033.7 s / 5.26 GB / 1.30 GB / 562 s; duplicate work is avoidable |
| B | SC-ESTATE: one certification + derived index | **PROVISIONAL LEADING** | smallest authority surface; reuses body format, native guards and evaluators |
| C | Primary SQLite/DuckDB/Postgres for all families | VIABLE_NOT_SELECTED | new primary authority/ABI, migration, concurrency, duplicate body; derived index is enough |
| D | Old W03 full object-materialized graph | RULED_OUT | 6.47 GB peak, whole-graph rebuild, no cold query proof |
| E | JSONL/document store as primary | RULED_OUT | no typed pruning/statistics, repeated parse, output amplification |
| F | One wide/generic table | RULED_OUT | family semantics, typed absence, authorities and exact body collapse |
| G | Stone/packed incidence/Arrow IPC primary | VIABLE_NOT_SELECTED | unaccepted prototype; no evidence-bearing multi-way proof; possible future derived accelerator only |
| H | Precompute all query answers | RULED_OUT | open query space, stale/revocation, unbounded output |
| I | Re-read source per query | RULED_OUT | custody/cost/nondeterminism; defeats saved C11 |
| J | Split body/proof/index into services | VIABLE_NOT_SELECTED | operational complexity without a demonstrated 100k need |
| K | Columnar F1–F4/risk accelerator | VIABLE_NOT_SELECTED | may be needed if native enumeration dominates; must reproduce exact facts/negatives; separate measured decision |

No full backend bakeoff is proposed. The smallest discriminating measurement is
the phase profile in `REV-2`; a targeted duel is optional only if the two
specialist returns leave one exact unresolved question.

## 4. Resource model (analytic, not measured)

Let:
- `S` = source bytes, `O` = object count, `E` = event count, `R` = respondent
  count, `B` = retained estate bytes, `X` = selected postings/body bytes, `Q` =
  number of distinct operations.

**Current route:** two I02 builds `2·f(O)`, JSONL journal `O` bodies, full
Parquet verify `O` object reconstructions, per-session index `O`, query `O` scan
+ native `R`. Approximate: `T_current ≈ 2·f(O) + O·(serialize + parse + encode)
+ O_session + Q·(O + R)`.

**SC-ESTATE:** one I02 `f(O)`, one Parquet write `O`, one byte-level digest
`B`, one index build `O log O`, cold open `M + I`, query `X + R_native`.
Approximate: `T_new ≈ f(O) + O·serialize + B + O log O + Q·(X + R_native)`.

This predicts a large writer/staging reduction and a cold-open reduction from
O(E) to O(manifest/index). It does **not** claim native 100k/6 GiB/1-10-100.
The remaining O(R) native risk enumeration is science-bound for full-domain F4;
a columnar accelerator is a separate option, not a hidden assumption.

**Retained:** baseline Parquet + compact index + manifest. No second body
corpus, no JSONL residual, no SQLite session corpus.
**Scratch:** largest sort run + stage + digest, not two I02/JSONL corpora.
**RSS:** index memory-mapped; selected row groups bounded; no whole-corpus
Python object graph. Exact 6 GiB proof remains `NOT_RUN`.

## 5. 1/10/100 distinct operations — what is actually amortized

- **Same process, prepared session:** one open, one index verification, one
  catalog/current binding; each operation pays selected postings/body + native
  risk. The current P0 test proves one `_build` for four distinct operations at
  sourcefree grade.
- **Fresh process:** manifest/index root verification + selected reads. No full
  event scan. This is the main improvement over the current 1.30 GB session
  rebuild.
- **10/100 repeated distinct operations:** share risk sets/denominator bases and
  evidence fragments; cache only exact issued operations with invalidation on
  source/release/frame/current/revocation change.
- **Heavy F4:** true k≥3 joint is O(risk population × support), not a storage
  scan; the estate keeps respondent coherence so the native evaluator can do it.
  If a columnar accelerator is later selected, it must produce identical native
  facts/negatives/replay.

## 6. Recovery, revocation and negative

- **Crash before manifest link:** stage is orphaned and cleaned; no reader sees a
  valid release.
- **Crash after member publish but before manifest:** `VerifiedDirectEstate`
  refuses the directory as incomplete; a later build can reclaim it only under
  the owner's lease.
- **Changed member/row group:** manifest or per-row-group digest mismatch →
  typed refusal, no valid EMPTY/ZERO.
- **Changed locator/index:** index root or selected body/ref mismatch → refusal;
  rebuild index from canonical estate.
- **Changed release/source/current:** `SavedC11Admission` current authorizer
  refuses; prepared session rechecks after each operation.
- **Revocation after preparation:** revoked member refuses even if the index or
  a prepared session exists; exact restore reproduces the same facts.
- **Negative:** missing/not-asked/routing-unknown remain typed; no false zero.

## 7. First consumer and owner interfaces

**Current first consumer (executed sourcefree):**
`SavedC11Admission.execute_i03` / `PreparedI03Session.execute_i03` over the exact
13-family sourcefree estate. Witnesses: 3 prepared-session tests, 7 direct-estate
I03 tests, 24 saved-native first-consumer tests passed locally. These are
sourcefree; they are not native/original35.

**Next interfaces:**
- `write_direct_estate_from_certified_stream` (proposed): one-shot sections +
  already-built Q2 roots; no second I02; no JSONL.
- `SavedC11Admission.execute_i05` (existing).
- `execute_saved_batch` / `execute_saved_normal` / `_execute_saved_resume`
  (existing owner-gated adapters; complete ACKs, no silent shared-file edit).
- `AnalyticalCompositionResult` / `FieldForgeConditionalSupport` (existing
  scoped F1–F4/FF01 consumers).
- `sorok_history.owner.HistoricalWorld` (exact owner hold; no source→actor).

## 8. Strongest surviving objection / reverser

**Objection:** the single-certification per-row-group digest may not be as
strong as the current full per-row object re-encode verification; and a durable
index can become a stale second authority. If either is true, the design must
retain the second verification pass or rebuild the index, reducing the gain.

**Response:** bind two roots — I02 logical root for exact object/selector
semantics, per-row-group digest for exact physical bytes — and check both before
first use. A changed body, locator, index entry, release root or revoked member
must refuse; exact restore must reproduce the facts. The reversal condition is
explicit: if any of these attacks passes, retain the second pass and re-cost.

**Second objection:** native full-risk enumeration, not storage, may dominate
1/10/100. The architecture preserves the native evaluator and a future columnar
accelerator as a separate measured decision. This is a `BOUNDED_BY_NEXT_PROFILE`
reverser, not a hidden certainty.

**Third objection:** the 100k witness is sourcefree and cut-specific; it is not
native 100k/6 GiB. It is used only as a bottleneck witness. Native economics
remain `NOT_RUN`.

## 9. Shortest implementable next operation

Implement the single-certification seam first:

1. Add a versioned `write_direct_estate_from_certified_stream` that accepts the
   one-shot `SourcefreeDirectI02Sections` plus the already-built Q2
   `ExternalI02Roots`, writes the existing 13-family Parquet/locator estate and
   manifest, computes per-row-group byte digests, and does **not** call
   `build_sourcefree_direct_i02` again or write 13 JSONL journals.
2. Prove on the sourcefree fixture: one source decode, one I02, zero JSONL,
   identical I03/I05 facts to the current path, changed body/locator/root/
   revocation typed refusal, exact restore, measured retained/scratch/open/query.
3. Only then add the durable derived index as a second bounded change.
4. Do not change the canonical body format, native evaluator, authority guards
   or source rights in this step.

This is the smallest operation that resolves the largest measured bottleneck
while preserving every present-hard distinction.

## 10. What must wait for the two specialist returns

- construction/storage/proof/recovery economics: whether the single-
  certification proof is equal or must retain the second pass; exact writer/
  retained/scratch/recovery cost; strongest falsifier.
- native repeated-query/shared-preparation/evidence-output economics: whether the
  durable index + prepared session actually delivers 1/10/100; where native
  enumeration dominates; evidence output accounting; index invalidation.
- any material new requirement or source contradiction → new S1 frame version
  before decision.
- final selection remains unfrozen; independent C remains separate and is not
  performed by this author.

See `S2_S3/SPECIALIST_CONSUMPTION.md` for the exact return schema and
adjudication rule.
