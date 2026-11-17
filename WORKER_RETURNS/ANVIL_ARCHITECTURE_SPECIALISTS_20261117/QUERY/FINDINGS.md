# QUERY specialist — minimum native query/preparation/evidence arrangement

**Frame read:** immutable author S1 commit `5a619ff9fa79be9183eb4d4378d42f040ef2bd9b`,
`evidence/S1_FROZEN/` + `S1_FROZEN_PINS.json`; product cut
`cea2d4d3009e9087d2267e9d1f53bec28b730dc7`; protected currentness observed
`31291d08179890852246c8742700e055168e9933`; live issues #909/#960/#997/#998/
#1006/#1009/#1011/#1097/#1108/#1133.

**Grade:** AUTHOR_FROZEN frame, NOT independently accepted. This return is one
bounded specialist analysis for the integrated architect; it is **not** final
architecture acceptance, not native/source/actor rights, not H1, and not a
measurement of native 100k or 1/10/100 economics.

**Independence:** I did not read the integrated architect's S2 draft or any
sibling specialist return. I read only the shared S1 frozen inputs, immutable
prior evidence, live issue bodies and the product-cut source named below.

## 1. Independent check of the “16 prepared narratives” claim

The frozen `S1/FRAME.json` contains the 16 requirement rows and the
118-entry source inventory; `S1_COMMON_FRAME.md` itself labels them
“reviewed common frame” while also stating this is an author checkpoint. That
is **instrument-preparation acceptance**, not a new architecture, current-code
or source-science acceptance. I found no material requirement from the QUERY
lane that is absent from the 16 rows, but I did find one material
**decomposition/contract gap** that should go back for shared-frame versioning:
the frame does not separate cold validation, index build, per-operation
scientific counting and evidence-output amplification, and therefore cannot
state what “1/10/100 economical” means without conflating them. Also absent is
an explicit derived-index proof/invalidation contract. These are proposed in
`NEW_FRAME_REQUIREMENTS.json`, not silently added as private requirements.

## 2. Actual code trace (product cut `cea2d4d`)

### 2.1 Cold open and validation

`VerifiedDirectEstate.__init__`
(`pre553_source_direct_parquet_estate.py`, snapshot lines 605–697) does, before
any query:

1. an independent live current/rights callback (`_live`) before any source-derived
   byte is opened;
2. exact path and release-identity checks;
3. SHA-256 of `manifest.json` against an **independently held** manifest digest;
4. SHA-256 of every one of the 14 emitted members (13 family Parquet files +
   `event_locator.parquet`) against the manifest (`for name, digest in
   members.items(): _hash(member)`);
5. Parquet footer census + row-group topology checks for event bodies and
   locator.

This is **cold validation `H`**. It is not repeated per operation: it happens
when a `VerifiedDirectEstate` / `SavedC11Admission` is opened. `SavedC11Admission`
re-verifies into a private estate when constructed directly, so a careless
caller can pay `H` twice at admission; `SavedC11Admission.open` uses the
`_from_verified_estate` fast path and pays once. `PreparedSavedC11Admission`'s
prepared context pays no second full hash.

### 2.2 Session index build

`DirectEstateI03Session.__enter__` (`pre553_direct_estate_i03.py`, lines
140–173) creates a temporary directory, a temporary SQLite database, the
`events` and `members` tables, and two indexes; `_build` (lines 252–345) then:

- reads the universe, all in-universe `RespondentIdentity` rows and
  `SourceUniverseRelation` rows through `iter_family` (body decode);
- reads **every** `RespondentEvent` and `event_locator` row group, checks
  positional/selector coverage, reconstructs the canonical body through the
  existing codec, runs `_validate_event_body_truth` (ref/native/canonical/
  component/state/occurrence/universe/respondent equality) and inserts into
  `events`;
- reads every `EmpiricalCoordinateFact`, `RoutingEligibilityFact` and
  `WeightMeasureFact` row group, checks census, inserts in-universe members.

This is **index build `S`**: O(total events + side-family rows), with a full
body decode/validation pass. It is the 1.30 GB temporary SQLite artifact in the
cited 100k-shape witness. It is currently discarded in `__exit__`.

### 2.3 Group-scope refusal

`execute_empirical_query` (`pre553_empirical_query.py`, lines 734–916)
explicitly refuses a grouped scope on the cold session:

> `if type(repository) is DirectEstateI03Session and group_scope is not None:
> raise EmpiricalQueryExecutionError("grouped native I03 cache not yet
> qualified for cold sourcefree estate")`

`CarrierNeutralResearchExecutor.execute_i03`
(`pre553_carrier_execution.py`, lines 431–474) also refuses a supplied
`group_scope` for a `VerifiedDirectEstate` (“grouped saved I03 scope awaits
distinct S2-D qualification”) and opens a **new** `DirectEstateI03Session` per
call. `I03GroupedExecutionScope`
(`pre553_empirical_query.py`, lines 490–563; core build/materialization in
`_pre553_query_eval.py`, lines 418–628) is therefore an existing, proven
mechanism for compatible C11 repositories only. It is not available to the
cold saved estate and cannot be assumed for 10/100 distinct operations.

### 2.4 Prepared session reuse

`PreparedI03Session` (`pre553_prepared_saved_i03.py`, lines 51–150) holds one
`DirectEstateI03Session` and calls the existing `execute_empirical_query` /
`execute_exact_bounded_discovery` per operation. `check_current()` is called
before and after each operation. The test
`test_pre553_prepared_saved_i03.py` asserts exactly **one** `_build` for four
distinct queries (selected, F2, F4, raw) and exact fact-ref parity with the
one-shot baseline. This removes repeated `S`; it does **not** remove the
per-operation evaluator scan or the fact/output construction. It is still a
process-local, ephemeral session, and it is an author candidate at `cea2d4d`,
not independently accepted.

### 2.5 Actual evaluators and per-operation cost

`_evaluate_index_group` (`_pre553_query_eval.py`, lines 640–833) iterates
`_query_respondents(index)` — **all** respondents in the sealed universe — for
every operation, regardless of predicate selectivity. For each respondent it
resolves routing facts per target, predicate truth, weights, and target cell.
It builds risk-member and denominator-member lists. There is no per-query
respondent pushdown in the current cold path. `_build_fact` (lines 893–990)
then emits an `EmpiricalFact` containing **full `risk_set_member_refs` and
`denominator_member_refs`** (each an `ExactRef` with kind/object-id/hash),
provenance, authorities, dependency refs, cell projection and replay ref. This
is per-operation scientific counting `Q` and evidence output `O`.

`execute_exact_bounded_discovery` (`pre553_discovery_exact.py`, lines
1052–1109+) compiles the exact frontier **before** evaluating (no
result-based pruning), then `_evaluate_candidate` (lines 994–1049) runs one
`execute_empirical_query` for **each query role** of each candidate. I05 cost
is therefore candidates × roles × per-query scan, plus receipt/output. It is
not a free “discovery” layer.

F1–F4 composition (`pre553_analytical_composition.py`, lines 1064–1259) calls
the same `execute_empirical_query` as producer (direct, discovery or recursive
route), validates fact identity/risk/measure/universe, builds evidence and the
consumer result. It does not introduce a second evaluator. A composition that
needs forward and reverse F2, or a 3+ target F4, pays separate producer
queries; marginals/pairwise products are not a joint.

### 2.6 Batch / NORMAL / resume handoffs

`execute_saved_batch` (`pre553_saved_workload_integration.py`, lines 81–139)
runs the real Batch runner but its per-unit `execute` calls
`admission.execute_i03` / `admission.execute_i05`. `SavedC11Admission.execute_i03`
(lines 424–444) delegates to `CarrierNeutralResearchExecutor`, which opens a
fresh session per call; `execute_i05` (lines 446–477) itself opens a fresh
session. Consequently even the “saved Batch” path pays `S` **per unit**, not
once per admission. `require_batch_owner_ack`, `require_normal_owner_ack` and
`require_resume_owner_ack` are exact typed refusals for shared-file owner
handoffs; NORMAL/resume are not wired. The prepared session is not currently
forward-wired into Batch, NORMAL or resume.

## 3. Four distinct cost layers

| Layer | What it is | Current status | Does a prepared session remove it? | Does a durable index remove it? |
|---|---|---|---|---|
| `H` cold validation | independent admission, member hashes, manifest/I02/root checks, footer census | required on every fresh open | no (still once per open) | no (must still revalidate source truth) |
| `S` index build | scan all event/side-family rows, full body decode/truth check, temp SQLite `events`/`members` + indexes | every new `DirectEstateI03Session` | yes, within one process/workload | yes, if a validated durable index replaces rebuild |
| `Q` scientific counting | all-universe routing/predicate/target/weight evaluation per operation | every `execute_empirical_query` | **no** | **no** (unless index-aware evaluator input is owner-qualified) |
| `O` evidence output | fact construction with full risk/denominator member refs, provenance, replay, cell projection; I05 receipts/support | every operation | no | no (unless exact set-ref sharing is owner-qualified) |

The 1.69–1.70× author report is consistent with removing `S` over four
operations; it is **not** evidence that 100 distinct operations improve by
1.69–1.70×. Under the analytic assumption that the four-operation test is the
reported basis and `O` is ignored, the implied ratio is `S/Q ≈ 1.2`, and the
prepared-session factor for `N` operations is
`N(1+S/Q)/(N+S/Q)`, which is 1.97× at 10 and 2.18× at 100 and asymptotes at
`1+S/Q ≈ 2.2×`. That is an analytic inference from an author report, not a
measurement. If `Q` dominates, prepared reuse alone cannot make 100 operations
economical; if `O` dominates, the problem is evidence output, not indexing.

## 4. 1/10/100 economics under the actual paths

- **One-shot admission (current `execute_saved_i03`/Batch):** `N × (S + Q + O)`
  for one fresh process with `N` operations (fresh admission pays `H` once per
  process). One operation pays a full index build; 100 operations pay it 100
  times.
- **Prepared session (`cea2d4d`):** `H + S + N × (Q + O)` within one process.
  One operation gets no benefit; 10 and 100 amortize `S`. Fresh process still
  pays `S`, so 10/100 **fresh-process opens** are not improved by this alone.
- **Validated durable derived index:** `H + I + N × (Q + O)` where `I` is
  index validation rather than rebuild; one-op fresh open no longer pays `S`.
  This is the only route that can help the 1-operation fresh-open case, and it
  is the only one that needs a new proof/invalidation policy.
- **Index-aware pushdown (typed/columnar/bitmap/posting):** `H + I + N ×
  (q + O)` with `q < Q` only for the scannable routing/predicate/target
  portions. This requires an owner-qualified index-aware input to the existing
  evaluator; without that it is either a second evaluator (forbidden) or a
  cosmetic wrapper.

Cited physical witness (sourcefree, cut-specific, **not** production 100k):
writer 3033.723 s; retained 310.16 MB; staging 5.26 GB; writer temporary I02
≈4.39 GB; native session index 1.30 GB; pre-W05 selected query 562.362 s;
prepared factor 1.69–1.70× (author report); old candidate peak
6,468,513,792 B > 6 GiB cap 6,442,450,944 B. The witness geometry is not
established as 100k dense respondents; the 3.245-event/respondent canary is
not representative. 562.362 s is not decomposed into `H`, `S`, `Q` or `O`.

## 5. Alternatives and legal boundaries

- **A. Status quo one-shot admission.** Safest, no new artifact; fails
  repeated-operation economics because `S` is paid per operation.
- **B. Forward-wire the existing prepared session (minimal).** One admission +
  one prepared session per process/workload; use it in the real first consumer,
  Batch adapters and F1–F4 composition. No new format, no semantic change, no
  second evaluator. Cost `H+S+N(Q+O)`. This is the minimum justified change
  from actual code and should be done before any new index format.
- **C. Persist the existing posting index as a derived artifact.** Build with
  the same `_build`; store `events`/`members` locators (no bodies); bind to
  estate manifest SHA, I02 roots, release/replay/universe, row-group topology,
  schema and censuses; independently hold/verify its digest; validate on open;
  invalidate on any source/root/currentness/authority/wave change. Removes `S`
  from fresh open. It adds 1.30 GB retained in the cited witness (4.2× the
  310.16 MB estate) and therefore conflicts with “compact TOTAL retention”
  unless a much more compact exact encoding is proven. It is **not**
  economically disposable by declaration: it must have an owner, proof,
  rebuild/restore and revocation contract.
- **D. Typed/columnar/posting/mask/bitmap pushdown.** The only route that can
  reduce `Q`; must not create a second scientific evaluator. It must feed the
  existing `execute_empirical_query` inputs with exact candidate streams while
  preserving all-universe risk-set/`NOT_APPLICABLE`/`ZERO_OVERLAP` states,
  typed missingness, repeated occurrences and exact cells. This needs an S04/
  I03 scientific+physical owner qualification and parity facts, not a backend
  fashion choice. It is not justified before measurement shows `Q` dominates.
- **E. Grouped core reuse.** Existing `I03GroupedExecutionScope` can share a
  measure-independent core across compatible operations, but it is explicitly
  refused for `DirectEstateI03Session`; a separate S2-D qualification would be
  required. It helps only compatible cores (same predicate/risk/targets,
  different measure), not arbitrary F1–F4 distinct queries. Do not assume it.
- **F. Fact/replay cache.** Not a shortcut for distinct operations. Replay must
  re-execute and compare exact fact refs (`replay_empirical_query`); identical
  facts can be referenced/deduplicated by content address, but a stale fact
  from an earlier authority/currentness state must refuse. Caching *facts*
  across distinct queries is not lawful evidence reuse.

**Strongest reverser:** if measurement shows `S ≪ Q`, then B/C are marginal and
only D changes the 1/10/100 curve; if `O ≫ Q+S`, then neither index nor
pushdown helps and the required work is exact set-ref sharing and streaming
evidence output. If operations are mostly one-per-fresh-process and the
derived index invalidates often (multi-wave, revocation, changed source), C
adds retained cost without reuse benefit. If the first consumer needs only one
operation, B is indistinguishable from status quo and C must justify its
retained/proof cost on that operation alone.

## 6. Recommended minimal path (not final architecture acceptance)

1. **Adopt B as the bounded recommendation:** one cold admission and one
   prepared session per exact release/universe/workload, forward-wired to the
   actual first consumer and to saved Batch/NORMAL/resume only through their
   existing owner handoffs. Keep `check_current` before/after every operation
   and keep every fact/replay recomputed.
2. **Measure before C/D:** decompose `H`, `S`, `Q`, `O` on one real-width
   authorized workload; run 1/10/100 distinct operations in one process and 10
   separate fresh-process opens; include weighted and unweighted, F2 forward
   and reverse, true 3+ F4, I05 multiple roles, changed source and revocation,
   and evidence bytes. This is the #1006 G2 plan, not a new benchmark matrix.
3. **If and only if `S` is material:** qualify C (validated compact derived
   index) with its own owner-approved proof/invalidation contract and a
   retained-size gate; if `Q` is material, qualify D only through the existing
   evaluator with scientific-owner parity, never as a second evaluator.
4. **Evidence output:** bind facts to exact shared risk/denominator set refs
   where the set identity is identical; do not re-emit member lists per
   operation; never share across forward/reverse, weighted/unweighted,
   missing/routing or wave boundaries.

## 7. Semantic/contract findings that constrain any index

- F2 forward and reverse denominators are distinct and must each be computed
  from their own routing/predicate; an index must not serve one as the
  algebraic inverse of the other.
- Weighted and unweighted populations are distinct; a shared membership index
  may store exact membership but must not cache a weighted result across
  measure regimes.
- Missing/UNKNOWN/refused/inapplicable/routing-unknown are typed states, not
  zero; the `events.state` and routing facts must remain exact.
- Repeated/ranked occurrences must not collapse to first value; the event ref
  and occurrence topology remain per event.
- F3 minority/recursive and signed/neutral information: I05 evaluates the fixed
  frontier and cannot prune by diagnostics; signed/neutral must not collapse.
- F4 must be a true same-person 3+ joint; pairwise marginals are insufficient.
  Odd/even parity witness is required for any index/optimization.
- F6 numeric bounds do not follow from the I07 guard; FF01 descriptive and
  FF02 independent structural must remain separate; SEAM Other/encounter/
  access/SOROK actor rights are not granted by a query index. F26
  caller/invalidation remains the exact `K1-CAP-24`/`P4R-R02` hold.
- Cross-wave/country nonpooling: one index per exact universe/release; the cold
  path refuses multi-universe/composite (`indices_for`); no pooled index and no
  wave join promotion.

## 8. Invalidation and proof reuse

A derived index is a **physical locator/selection artifact**, not source truth.
On every fresh open: `H` (manifest, independent I02 roots, member hashes,
censuses) remains mandatory; the index digest is checked only after `H`; any
change to source root, release, replay, universe, manifest, family census,
row-group topology or schema refuses the index. `check_current` remains
per-operation, so revocation refuses before and after work. Proof reuse is
limited to locator rebuild avoidance; fact identity, authority snapshots,
denominators, negative states and replay remain per-operation. A re-pinned
manifest or a re-hashed index cannot launder a changed source.

## 9. Where empirical measurement is indispensable

The cited 562.362 s selected-query number is not decomposed, the prepared
factor is an author report at a small operation count, and the 100k-shape
geometry is not established as dense 100k respondents. Therefore the choice
between B, C and D cannot be made honestly from the current numbers. The
smallest lawful test is the #1006 G2 protocol on one authorized real-width
workload: one writer/admission, then 1/10/100 distinct issued operations in
one process and 10 fresh-process opens, with F1–F4/I03/I05 parity, fact/replay
identity, changed-source/revocation refusal, peak process-tree RSS, retained/
scratch/output bytes and per-layer timing. This specialist did not execute it
(no native/heavy benchmark, no raw-data access); no speedup is claimed.

## 10. Findings vs interpretations vs owner holds

**Findings (code/source grounded):** cold `H` hashes all 14 members; `_build`
scans all event and side-family row groups and full-body-validates; per-query
evaluation loops all universe respondents; group scope is explicitly refused
for the cold session; prepared session removes repeated `_build` only; saved
Batch/NORMAL/resume either pay a fresh session per unit or are typed refusals;
facts carry full risk/denominator member refs; I05 evaluates every candidate
role without result pruning; cross-universe/release is refused in the cold
path; the 1.69–1.70× is an author report, not independent acceptance.

**Interpretations (analytic, not measured):** the ~2.2× prepared-session
asymptote under a four-operation basis; per-fact evidence output in the tens of
MB at 100k respondents; durable index value only if `S` is material; compact
index could be far smaller than the 1.30 GB SQLite but this is unproven.

**Owner holds (not decided here):** whether a durable derived index is
admissible and under what independent proof; whether index-aware pushdown may
change the evaluator's respondent input; S04/I03 science ownership of any
denominator/core sharing; S2-D qualification of grouped scope; F6 numeric,
FF02/N9, SEAM/SOROK actor rights; F26 caller; native source/rights and
original35; 100k/6 GiB/1/10/100 acceptance; independent C/H1.

**Self-found oversight in my own lane:** the frozen frame's “prepared
narratives are the reviewed common frame” wording overstates the grade; it is
instrument-preparation review. I also initially treated “prepared session” as
if it reduced per-query counting; the code shows it only reduces `_build`.
Both are flagged rather than silently repaired.

No final architecture decision, no protected adoption, no new science.
