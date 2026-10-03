# OPS-04 — CURRENT consolidated C4 technical claims (HQ188-B)

Status:
`CURRENT_OPERATIONAL_CONSOLIDATION__DOCUMENTARY_ONLY__NOT_AN_ADOPTION_DECISION__DOES_NOT_LIFT_HQ182_HOLD__NO_SOURCE_ACCESS__NO_WARRANT__NO_LIVE_C4`

Lane: **PYAT HQ188-B — Current C4 consolidated claims and external decision packet — R1**
Role: RABOCHII / documentary forensics — Space Bunny
Worker branch: `agent/rabochii-pyat-hq188-b-c4-current-consolidation-r1`
Commissioned startup SHA: `9001be646305036e493eea3dbce427f62f91c9ae`
Artifact under consolidation: C4 executable freeze
`8ff40d37de69db2d8a6053a7c2242f481677f1a4`

## What this document is, and is not

This is the **single current C4 technical consolidation**. It supersedes the
historical OPS-04 `00` and `01` packets *as an operational summary*. It
modifies neither. Their bytes are preserved exactly as history and are not
edited, superseded-in-place, or deleted.

It records the current C4 truth at the evidentiary ceiling actually
established by the governed evidence. Where a later document corrected an
earlier one, the correction is carried and attributed. Where my own
independent re-derivation disagrees with the most recent prose, the
disagreement is recorded as such rather than silently harmonised.

It does **not**: adopt C4, lift HQ182's hold, issue or alter a warrant,
discover a locator, access a raw source, execute C4, mutate production,
implement C7, or implement actor/person work. It does not self-adopt. It does
not contact Astra.

Conclusions were not selected by model reputation, benchmark timing, lane
majority, or recency of prose. Every load-bearing claim below was re-derived
from git objects and governed artifacts on this branch, with the exact method
recorded in `03_CURRENT_CLAIM_EVIDENCE_MAP.json`.

## Governing inputs actually read

| Input | Commit | Read at |
|---|---|---|
| C4 executable freeze (fan-in) | `8ff40d37de69db2d8a6053a7c2242f481677f1a4` | this branch |
| Sol final reviewer (Lane A) | `fe6103cd50c634b92233f49815cc6d4abe49964d` | by exact ref |
| Space Bunny ALT-B reviewer | `3a5b2cbc7f1978384268376f3ee493c7c095780b` | by exact ref |
| Sol shadow HQ | `d0fc810de3bee0e1ea68c82fa44c61c749372077` | by exact ref |
| HQ182 checkpoint / HQD-2026-10-02-182 | `fe1b2729b0f9f1ff18044c2f655b74784e001217` (sealed) | this branch |
| HQ183 C1 allegation + C2–C5 | `4c4da2fe8`, OPS-04 `00` | this branch |
| HQ186 C1 withdrawal / HQD-2026-10-02-186 | `3b9b14448`, `ce27c7cf8` | this branch |
| HQ187 adjudication / HQD-2026-10-02-187 | `06e907cb3` | this branch |
| R2 disputed-claims re-check return | `afb1eb49bbd2ba49c1cb1c4f0501a35908d161d3` | by exact ref |
| October 3 corrections/evidence publication | `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/CORRECTIONS_AND_EVIDENCE_20261003.md` | this branch |
| October 3 publication/runtime audit | `f68903fdd` + `REVIEWS/HQ181_187_AUDIT_20261003/**` | this branch |
| Publication audit seal | `682016053` | this branch |
| C4A combined court | `8f7efe690a161902e79358eb31650c238a4c0be8` | by exact ref |
| C4B workload/oracle freeze | `c2af4f61d68e9803af83f8e26f633acfe31062fa` | by exact ref |
| C4C3 Darwin anchor runtime | `1df64cc596b5602c952518c87b1c71cc1fcfb35f` | by exact ref |
| D2P portable import review | `41bd7a7c056de9d45b905efc0f926b4ab6a097ad` | by exact ref |
| Omega-1 production readiness | `01762d7379be4e423dad3e21bcdcee47c536902d` | by exact ref |
| M01 qualified candidate | `46f3bec824c1c9da7037bacf94ec08923bc33506` | by exact ref |
| M01 final court binding | `74a067742a370d4f6296c56140c28cc8acc53e63` | by exact ref |
| Accepted C3 integration | `30686b185d4ceb2c94f61815ef70d8c8e76255d6` | by exact ref |

Tooling: `git` plumbing (`rev-parse`, `ls-tree`, `rev-list`, `merge-base`,
`cat-file`, `show`) and `node` v18.14.2 for closure traversal and census.
`python3` on this host was verified functional (3.11.3, exit 0) but was not
relied upon for any verification result.

---

# PART 1 — The M01 distinction, stated correctly

This is the single most consequential correction in the current record, and
it is a distinction between two things that are both true and are not
interchangeable.

## 1.1 M01 named-file identity — REAL

The four named M01 producer/carrier/test file pairs identified by Sol shadow
HQ (`d0fc810de`, section 9) are byte-identical between the qualified M01
candidate and the freeze. Re-derived by me with `git rev-parse <commit>:<path>`
on both sides:

| File | `46f3bec82` | freeze `8ff40d37d` | |
|---|---|---|---|
| `rawlsing_next/pre553_route_b_production.py` | `2385cd327dce` | `2385cd327dce` | **MATCH** |
| `rawlsing_next/pre553_carrier_execution.py` | `e7cda773e6a2` | `e7cda773e6a2` | **MATCH** |
| `rawlsing_next/tests/test_pre553_route_b_production.py` | `d244eaaa48f8` | `d244eaaa48f8` | **MATCH** |
| `rawlsing_next/tests/test_pre553_carrier_execution.py` | `bc0db646a803` | `bc0db646a803` | **MATCH** |

The M01 final court binding at `74a06774` carries
`.rabochii/court_spec.json` with `semantic_candidate_sha =
46f3bec824c1c9da7037bacf94ec08923bc33506` and exactly those four suites in its
`tests` array. This is confirmed. **C1's withdrawal stands.**

## 1.2 M01 transitive dependency identity — NOT ESTABLISHED, and demonstrably false for two modules

I computed the transitive import closure of the two M01 bounded-court test
suites by AST-style traversal of every `import`/`from` statement over the
committed trees, then compared blob identities member by member. This is my
own derivation; it is not a restatement of any lane.

**Membership:** the closure is **23 modules** at `46f3bec82` and **23
modules** at the freeze, and the two *path sets are identical*.

**Bytes:** of those 23 modules, **21 are byte-identical** and **2 differ**:

| Module | at `46f3bec82` | at freeze `8ff40d37d` |
|---|---|---|
| `rawlsing_next/pre553_physical_decoder.py` | `d2a074a41fb5` | **`d3d828c171ea`** |
| `rawlsing_next/pre553_r5_codec.py` | `72f8f3c03ed0` | **`6000a1704d71`** |

**Therefore, and this is the load-bearing sentence:**

> The M01 61/61 bounded court does **not** bind the freeze's exact 23-module
> closure bytes. It binds 21 of 23 exactly, and the remaining 2 were different
> bytes at the time it ran.

I further verified that **no M01 court binding ever carried the C3-accepted
bytes** of these two modules — not the earliest binding, not any of the three
final rebinds:

| Binding | decoder | codec |
|---|---|---|
| `903c262e4` | `d2a074a41fb5` | `72f8f3c03ed0` |
| `a1545aee` | `d2a074a41fb5` | `72f8f3c03ed0` |
| `46f3bec82` | `d2a074a41fb5` | `72f8f3c03ed0` |
| `74a06774` (final rebind) | `d2a074a41fb5` | `72f8f3c03ed0` |
| `30686b185` "Integrate accepted C3 source-free repair" | `d3d828c171ea` | `6000a1704d71` |
| freeze `8ff40d37d` | `d3d828c171ea` | `6000a1704d71` |

## 1.3 Correction to HQ187's stated import edge — documentary only, conclusion unchanged

HQ187 records the chain as *"`pre553_physical_decoder.py` L21 imports
`pre553_r5_codec`"*. That line number is correct **at the freeze**, and it is
not the edge that put the codec inside the M01-time closure. My traversal
found:

- At the **pre-C3** decoder (`46f3bec82`), `pre553_physical_decoder.py`
  contains **zero** references to `r5_codec`. It does not import the codec.
- The codec enters the M01-time closure through a different, already-existing
  edge: `test_pre553_route_b_production.py` L30 imports
  `rawlsing_next.pre553_source_backed_c11_facade`, and
  `pre553_source_backed_c11_facade.py` L38 imports
  `rawlsing_next.pre553_r5_codec`. The facade blob is `8a761119e4a8d68e…`,
  **identical at both** `46f3bec82` and the freeze.
- The decoder → codec edge at decoder L21 is an edge **added by the accepted
  C3 repair**. It exists at the freeze and did not exist pre-C3.

**Effect on the conclusion: none — it strengthens it.** Both modules are
inside the court's transitive closure at *both* states, but for different
reasons, and the codec's membership never depended on the changed decoder.
The counterexample is if anything firmer than HQ187 stated. This is recorded
as a documentary precision correction, not a blocker.

## 1.4 What the counterexample is and is not against

The one standing counterexample is against the **overbroad M01-closure
justification** — specifically the step from "the four named files match" to
"the 61/61 therefore qualifies the freeze's exact bytes," and the C4A
combined-court substitute offered in its place. It is **not** a counterexample
against the existence or integrity of the freeze evidence base, and it does not
invalidate any O1-C01..C1-C05 closure.

---

# PART 2 — The corrected authority basis for the later decoder/codec bytes

Because the M01 court cannot carry those two modules, their authority at the
freeze rests on the accepted C3 court plus C4C3. All three legs verified:

1. **Accepted C3 six-file 55-test court.** `C4C3/05_AUTHORITATIVE_C3_COURT.json`
   records `55 passed / 0 failed / 0 errors / 0 skipped`, denominator asserted
   by `--collect-only` **before** the timed run as 9+8+13+9+6+10 = 55, on
   CPython 3.11.3 / Darwin 22.6.0 / x86_64. Per-file results match the
   expected counts exactly. Run twice: `identical: true` (77.79s, 44.25s).

2. **C4C3 authoritative 55/55 executed twice on the freeze/combined-tree
   bytes.** The same file's `repeat_run_determinism` block records both runs
   at tree `8f7efe690`, and declares
   `"This is a FRESH EXECUTION on the combined C1+C3 tree … not an inheritance
   of the accepted result."` — an independent reproduction, not an admission.

3. **The exact pinned accepted C3 blobs are present at the freeze.** From
   `C4A/02_FINAL_BLOB_MATRIX.json`, six blobs carry `"side": "C3"`. I resolved
   every one of the eleven pinned blobs at the freeze:

   | Side | Path | Blob | At freeze |
   |---|---|---|---|
   | C1 | `pre553_analytical_state_and_route.py` | `3a5e3db8a089` | EXACT |
   | C1 | `pre553_empirical_possibility_provider.py` | `23167aa25291` | EXACT |
   | C1 | `pre553_authority_maintenance.py` | `547e6bf20354` | EXACT |
   | C1 | `pre553_analytical_replay_dependency.py` | `47e65aad5e0a` | EXACT |
   | C1 | `pre553_analytical_composition.py` | `604c8d591d4c` | EXACT |
   | C3 | `closed35_g01_sav_numeric_representation_authority.py` | `31a9afd7d91e` | EXACT |
   | C3 | **`pre553_physical_decoder.py`** | **`d3d828c171ea`** | **EXACT** |
   | C3 | **`pre553_r5_codec.py`** | **`6000a1704d71`** | **EXACT** |
   | C3 | `tests/test_closed35_g01_sav_numeric_representation_authority.py` | `fb7b090809a6` | EXACT |
   | C3 | `tests/test_closed35_d01_declared_encoding_admission.py` | `8fc059653860` | EXACT |
   | C3 | `tests/test_closed35_d02_opaque_datetime_carrier.py` | `3901f10a4878` | EXACT |

   **11 of 11 exact, 0 drift.** The decoder and codec are two of the six
   pinned accepted C3 blobs, so they sit **inside the authoritative C3
   denominator directly** — they are not merely adjacent to it.

4. **A supporting fact that matters for the ceiling.** `rawlsing_next` tree is
   `b0c1ab472cde…` at C4A `8f7efe690`, at C4C3's head `1df64cc59`, and at the
   freeze `8ff40d37d` — identical. C4C3's 21-module runtime trace therefore
   covered the freeze's *exact* decoder and codec bytes on Darwin, not an
   earlier revision.

**Defect location: the record, not the evidence.** The historical error was in
the justification and in the register's accounting of the justification. No
freeze evidence is missing.

---

# PART 3 — Closure wording: 21 → 23, and what must not be said

## 3.1 C4C3's 21 is real, and starts below M01 — independently reproduced

`C4C3/02_ACTUAL_C4_CALL_PATH.json` records a `module_count` of 21, rooted at
the five declared C4 production layers. I re-derived the closure from those
same five modules at the freeze and obtained **exactly 21**. C4C3's trace is
confirmed.

The four modules in C4C3's 21 that are *not* reachable from the M01 bounded
court's tests are:

| Module | At `46f3bec82` | At freeze |
|---|---|---|
| `pre553_analytical_composition.py` | **does not exist** | `604c8d591d4c` |
| `pre553_empirical_possibility_provider.py` | **does not exist** | `23167aa25291` |
| `pre553_recursive_handoff.py` | `868f43bf9869` | `868f43bf9869` |
| `source_backed_positioned_subject_possibility.py` | `62e5eced47b6` | `62e5eced47b6` |

The first two are C1-side modules and are among the five C1 pinned blobs,
verified EXACT at the freeze. All four carry zero `ee_p2x_*` / `duckdb` /
`subprocess` / `importlib` / `exec_module` / `spec_from_file` / `os.system` /
`os.popen` references, as do the producer and carrier. I confirmed all of this
independently, so Sol shadow's ground that the added modules "introduce no
`ee_p2x_*` edge, DuckDB edge, subprocess edge, or dynamic-loader/importlib
execution edge" is sound.

## 3.2 The producer-inclusive closure is exactly 23

Three root-sets, each independently computed at the freeze:

| Root set | Count |
|---|---|
| M01 bounded-court tests (2 files) | **23** |
| C4C3 five production layers | **21** |
| Producer + carrier alone | **19** |

Producer-inclusive production closure
= (producer ∪ carrier rooted, 19) ∪ (C4C3 layers, 21), overlap 17
= **exactly 23**.

This **tightens** the standing "at least 23" wording. It is not merely *at
least* 23; for static transitive import reachability from
{producer, carrier} ∪ {five C4 layers} at the freeze it is exactly 23.

Note that the 23-module *M01 court* closure and the 23-module
*producer-inclusive* closure are **different sets of 23**: they share 19
members, and differ by four test modules in one direction and four downstream
composition/provider modules in the other. Both counts are correct; they
answer different questions.

## 3.3 Three distinct qualification events — never collapse them

| # | Event | Grain | Fresh on Darwin? |
|---|---|---|---|
| 1 | M01 bounded source-free court, 61/61, GitHub Actions run 36302391261 | M01's historical dependency state (pre-C3 decoder/codec) | no — CI, not the Darwin anchor |
| 2 | Accepted C3 six-file court, 55/55, plus C4C3 55/55 twice | decoder + codec at C3-accepted bytes | yes, by C4C3, on `b0c1ab47` |
| 3 | C4C3 runtime qualification | 21-module downstream layer path | yes, on `b0c1ab47` |

**The sentence that must not be written:** *"the M01 61/61 qualified the
freeze's complete 23-module producer-inclusive transitive closure."* It is
false. M01 never saw the C3 decoder or codec bytes.

**The sentence that must not be written either:** *"all 23 modules of the
producer-inclusive closure were freshly rerun on Darwin."* Also false. The
producer and carrier sit **above** C4C3's five layers and are **not** in its
21. C4C3's fresh Darwin evidence covers the 21-module downstream path,
including the two C3-accepted modules; it does not cover producer or carrier.

---

# PART 4 — Court-count clarification (M01's 32)

Do not infer pytest case counts from static function counts. I re-derived the
reconciliation from the qualified candidate's own source:

| Suite | Static `def test_` | Cases |
|---|---|---|
| `test_pre553_route_b_production.py` | 11 | 11 |
| `test_pre553_carrier_execution.py` | 4 | 4 |
| `test_pre553_discovery_exact.py` | 14 | 14 |
| `test_pre553_empirical_query.py` | **30** | **32** |
| **BOUNDED_COURT_TOTAL** | 59 | **61** |

The +2 is fully located. `test_pre553_empirical_query.py` contains exactly one
`@pytest.mark.parametrize`, at **line 1388**, over the parameter
`authority_state` with the three values
`("DENY", "OUT_OF_SCOPE", "SUPERSEDED_NOT_REPLAYABLE")` — three **refusal /
non-positive authority states**. One function yields three cases instead of
one: **+2**. 30 + 2 = 32. 11 + 4 + 14 + 32 = **61**.

The freeze's own `04_OWNER_REGRESSION_LEDGER.tsv` already records
`"32 pytest cases from 30 functions"` and `BOUNDED_COURT_TOTAL … 61 pytest
cases … GitHub Actions run 36302391261; 61 passed in 2.58s`. My derivation
reproduces that arithmetic and supplies the mechanism the ledger omits. The
October 3 audit reached the identical explanation independently.

**Evidence ceiling, preserved:** the *count reconciliation* is now
source-derived and needs no external log. The *run result* "61 passed in
2.58s" is **inherited** from the ledger at the freeze. The full GitHub Actions
execution log for run 36302391261 was **not independently retrieved** on this
branch. Recorded 61/61 stands with that ceiling. It is not a discovered false
count, and it is not an independently re-observed pass.

---

# PART 5 — R7, restated as BOTH

**Current class: both fingerprint incompleteness AND weak environment
reproducibility.** This is HQ187's correction to the earlier
fingerprint-only classification, and it is correct.

Verbatim from `C4C3/01_ENVIRONMENT_LOCK.json`,
`environment_location.durable_note`:

> "The venv lives in a per-session temporary directory. It is NOT durable and
> NOT reproducible **from this path alone**. It is recorded so HQ can see
> exactly what executed. The reproducible content is the freeze below, not the
> path."

Two consequences:

1. **HQ182's wording was inaccurate.** HQ182 asserted the record says "NOT
   reproducible **from the repository**" and characterised that as
   self-declared non-reproducibility. The record says "from **this path
   alone**". The quotation repair is correct; the severity upgrade must not be
   built on the misquotation.

2. **The reproduce command does not freeze the entire resolved environment.**
   The `reproduce_command` pins exactly **13** packages. The resolved
   environment contains **14** entries. The difference is `narwhals`:

   | | Count | `narwhals` |
   |---|---|---|
   | `reproduce_command` pins | 13 | **absent, unpinned** |
   | `pip_freeze.sorted_output` | 14 | **present at `2.26.0`** |

   The record's own `reproducibility_caveat` discloses this: a future
   re-resolve "could select a different narwhals. Since narwhals is off the C4
   path and absent from the authoritative court, that would not affect the
   qualification result — but it would change the freeze hash."

   **So:** the 13-package subset is genuinely index-independent because every
   one of those is exactly pinned. But the *environment as resolved* is not
   fully reconstructible from the recipe. A correct quotation repair must not
   be converted into a fingerprint-only finding, and must not be inflated into
   a claim of exact index-independent environment reconstruction.

**What is genuinely incomplete — the fingerprint.** The base interpreter is
recorded only as `base_interpreter_sha256_prefix32 =
11d6f541a870a141249ce98d45834a67`. The five `compiled_extensions.*` digests
carry no prefix marker in their field names. The qualified interpreter resolves
under `LOCAL_COURTS/`, which is untracked in this repository, so the
interpreter is genuinely uncommitted. That part is fingerprint incompleteness.

**Bounded and off-path, stated accurately, not dismissed:** `narwhals` is
absent from the authoritative six-file court and off the C4 path (it is a
`pyarrow` transitive). It would not change the 55/55 result. It *would* change
the freeze hash. This is a bounded, achievable, off-path reproducibility
residual — not a licence to treat the environment as fully reconstructible.

**Required before any governed live run — one of:**

- **durable exact environment preservation**, with a complete interpreter
  digest (full 64-hex, not `prefix32`) and recorded provenance for the
  untracked interpreter; or
- **competent requalification** — re-create from the pinned 13-package recipe,
  additionally pin `narwhals`, and record complete digests for the interpreter
  and the five compiled extensions.

Neither is a re-derivation of the workload. Both are bounded documentary
acts.

---

# PART 6 — R9, with the accounting surface corrected

## 6.1 What artifact 07 actually binds — six of eight, not eight

`C4 FAN-IN / 07_EXECUTION_ACCOUNTING_AND_FAILURE_LAW.json`,
`per_source_expected_operation_class`, has **8** sources. Of those:

| Source | Explicit `expected_full_reads` / `expected_selected_reads`? | Governing law instead |
|---|---|---|
| SRC02 | **yes** (0 / 1) | selected-variable read |
| SRC06 | **yes** (0 / 1) | selected-variable read |
| SRC08 | **yes** (0 / 0) + `expected_metadata_reads: 1` | metadata-only admission |
| SRC12 | **yes** (0 / 0) + `expected_metadata_reads: 1` | metadata-only admission |
| SRC14 | **yes** (0 / 1) | witness-only exact-variable read |
| SRC26 | **yes** (0 / 0) + `expected_header_prefix_bytes: 176` | header-prefix + metadata |
| **SRC27** | **no — neither field** | `expected_full_route_passes: 1`, `expected_full_route_passes_max: 1`, `max_retry_budget: 0` |
| **SRC35** | **no — neither field** | `fresh_reads: 0`; zero fresh access at all |

**The corrected figure is 6 of 8.** The earlier 8-of-8 claim must not be
restored.

## 6.2 SRC27 — one governed full Route-B pass, maximum one, zero retries

SRC27 is `EXACTLY_ONE_GOVERNED_FRESH_FULL_ROUTE_PASS` with workload
`{candidates: 50, query_roles: 77}`. Its retry law is explicit:

> "Exactly ONE governed fresh pass. A second pass is not a retry; it is a
> separate run requiring new HQ-bound authority."

And its `critical_note`, reinforced by `hardened_note_on_the_SRC27_single_pass`:

> "One governed full Route-B pass is NOT one OS-level file open. The pass will
> involve multiple path-level opens, a hash pass, a metadata pass and a full
> read. **These must each be counted separately.**"

> "The frozen 'exactly one governed fresh full Route-B pass' is a WORKLOAD
> constraint, not an access constraint. It does NOT license assuming one file
> open. The run will require at minimum: one existence/access check, one full
> SHA-256 hash pass, one metadata read, and one full compatibility read. Each
> is a separate account under O1-C07… **Misreading this as one open would be
> an accounting failure and is expressly forbidden by Omega-1.**"

The consequence is stated plainly by the evidence itself: **the most
consequential read in the workload has no explicit expected read counters bound
in artifact 07.** That **strengthens** R9; it does not relieve it.

## 6.3 SRC35 — zero-fresh-read law

SRC35 is `RETAINED_COMPARATOR_REPLAY_AND_COMPARE` with `fresh_reads: 0` and
retry law "No fresh access at all. Replay uses retained material only."
Artifact 06 independently records its lane as
`"lane_id": "NONE__RETAINED_ONLY"`, `"read_path": "NO FRESH LANE. Retained
comparator; zero fresh raw reads."`, `"materialises_frame": false`. The
warrant candidate's `zero_authorizations` carries
`"WVS_SRC35_fresh_source_reads": 0`. The locator slot is
`"NOT_REQUIRED__RETAINED_COMPARATOR__NO_FRESH_ACCESS"`.

**Do not say SRC27 and SRC35 have no constraints.** Both are heavily
constrained. The defect is the *form* of the constraint, not its absence.

## 6.4 What the warrant candidate actually carries — the precise remaining gap

`04_SOURCE_EXECUTION_WARRANT_CANDIDATE.json` authorises **7** sources
(SRC02, SRC06, SRC08, SRC12, SRC14, SRC26, SRC27) and excludes SRC35 plus 27
non-selected sources. Of its seven `per_source` entries:

- **zero of seven** carry `expected_full_reads` or `expected_selected_reads`;
- all seven carry `max_retry_budget: 0`, `expected_operation_class`,
  `reader_lane`, and detailed `allowed_operations` (variables, ordinals, native
  codes, expected successor types, expected missing states, source
  declarations);
- SRC27's entry uniquely carries `expected_full_route_passes: 1`,
  `max_full_route_passes: 1`, an `accounting_warning`, an `oracle_binding`, a
  `RES_1` binding and `source_specific_authority`.

The candidate does carry a global `access_accounting_instrumentation_bound`
listing **10** account types — a richer taxonomy than C4B's 7 — plus
`basis_required_per_figure: true`. And artifact 07 requires every figure to
publish four basis fields: what was measured, at which layer, by what
mechanism, at what point in the run, warning that "a count of 'opens' is
meaningless without stating whether it means OS-level path opens, reader
invocations, or decoder calls."

**The remaining warrant-issuance repair, stated exactly:** bind explicit
per-access-layer measurement bases and limits into the **issued** warrant, for
all seven authorised sources — using artifact 07's already-frozen expectations,
the candidate's 10-account taxonomy, and its own four-field basis requirement;
and for SRC27 specifically, carrying the existence/access, hash, metadata and
full-read accounts **separately**, never collapsed into "one pass = one
open."

This is a **documentary completion of the instrument**, not a re-derivation of
the workload and not a loss of per-source constraints.

## 6.5 Retry position — unchanged and uncontested

`retry_budget_law.frozen_maximum`: "ZERO retries across all eight sources
under this freeze." Every per-source `max_retry_budget` is 0 because C4B
froze immediate-stop-on-mismatch. "A retry is authorised only by a NEW HQ-bound
warrant, never by this one." No conflict exists and no repair is needed here.

---

# PART 7 — Hash and identity hygiene (corrected census)

Census of every hex-valued string in `C4C3/01_ENVIRONMENT_LOCK.json`, by whole
field value:

| Length | Occurrences | Distinct | What they are |
|---|---|---|---|
| 16 | **32** | **29** | all field-named `*_prefix16` (metadata/wheel per distribution) |
| 32 | **6** | 6 | 1 × `base_interpreter_sha256_prefix32` + 5 × `compiled_extensions.*.cpython-311-darwin.so` with **no** prefix marker |
| 40 | **2** | 1 | `no_repo_mutation.rawlsing_next_tree_before/_after`, both `b0c1ab47…` |
| 64 | **3** | 1 | all `9cde8e5ab9abba…`, the historical C3 freeze hash |

The 29-of-32 distinctness is explained by exactly three collisions, which I
enumerated: `e56b47578e45e542` (pyarrow wheel / numpy wheel),
`f86fedd281ae13b5` (python-dateutil wheel / pytz wheel), and
`1b5e87e00dc87a84` (setuptools wheel / pip wheel).

**Raw-text census of 32-hex occurrences in the file: 9 total** — the 6
structural field values above, plus **3 prose restatements**, all three inside
the single narrative field `distribution_hashes.CROSS_ENVIRONMENT_REPRODUCIBILITY_DATUM`
at line 122.

**The correction that must be preserved:** the two 40-hex values are
**complete Git SHA-1 tree identities**, not truncated SHA-256. I confirmed
`git rev-parse 8ff40d37d:rawlsing_next` = `b0c1ab472cde033e21f1c2f63fbcbea2f0cccef0`,
so they are genuine complete tree object IDs. HQ182's "40 truncated hex
identity literals" was wrong in kind: 38 are prefixes, 2 are complete Git
identities, and 38 + 2 = 40 short hex values. Neither prefix set is
sufficient for its declared purpose — the base interpreter is recorded only to
32 hex and the interpreter is untracked — which is the fingerprint half of R7.

---

# PART 8 — R10 / T3, and the cross-lane attribution question at its actual severity

## 8.1 The digest is recovered, not guessed

`C4 FAN-IN / 05_ORACLE_AND_COMPARISON_LAW.json` line 44 carries
`"T3_freeze_sha256": "7dfb6..."` — a 5-character abbreviation sitting beside two
complete 64-hex digests in the same object.

Recovered from governing evidence:
`C4B/04_WVS_ORACLE_CUSTODY.json` at `c2af4f61`, field
`later_T3_standardization.T3_freeze_sha256`, value

```
7dfb62362b983b92dee2774d862a46c0c0ce3ca2c3bb48850e0f400346936908
```

The prefix `7dfb6` matches the abbreviation. No completion-by-pattern was used;
the value was read in full from a named field in an independent artifact. I
also swept all **12** files of the freeze packet for abbreviated hex in
JSON string values: exactly **1** occurrence, the R10 site. It is the only
truncated identity value anywhere in the packet.

## 8.2 Cross-lane T3 attribution — recorded, not escalated

The **same literal digest** is attributed to two different lanes in two
different upstream artifacts. I confirmed both sites:

| Artifact | Field path | Value |
|---|---|---|
| Omega-1 `01762d73` | `identity_rules.full_route_oracles.LiTS_I.T3_sha256` | `7dfb6236…36908` |
| C4B `c2af4f61` | `later_T3_standardization.T3_freeze_sha256` (WVS custody) | `7dfb6236…36908` |

**Severity, stated at its actual level:** this is a **record-level attribution
inconsistency in the upstream record**. It is:

- **not** a freeze-evidence defect — the digest is present, complete and
  identical in both places;
- **not** a blocker for R10, which asserts only that the value is recoverable
  from C4B and equals the stated digest, and that is confirmed exactly;
- **not** converted into a counterexample or stage blocker on the present
  evidence.

The open reconciliation question is whether one shared freeze digest
legitimately covers both the LiTS lane and the WVS later-standardization lane,
or whether the attributions are wrong. That is a question for HQ. I record it
and do not resolve it by preferring the newer document.

## 8.3 Cross-lane lineage — a different cross-lane issue, also advisory

Independently confirmed: the freeze `8ff40d37d` is **not** an ancestor of the
R2 re-check return `afb1eb49b`, and C4A `8f7efe690` is **not** an ancestor
either. The merge-base is `87029d349c8a7385cb673060a8e5decd4eb528ff` — exactly
as HQ187 recorded.

This is by design for a control/activation branch that cites the freeze by
SHA. Every R2 comparison was made against the exact pinned commits the
commission named, never against HEAD, and blob-SHA comparison is
ancestry-independent. **Severity: none for the findings.** The recorded
consequence worth keeping: a verifier working only from that branch's HEAD
cannot reach the freeze by ancestry, so any re-check must cite the freeze SHA
explicitly. I have done so throughout this document.

I also record, in the same spirit, that the R2 reviewer **self-disclosed** a
vacuous pass: its first manifest extraction guessed the field name and returned
`None` for both entries, comparing `None == None`. It then dumped the record
verbatim, found the field is `blob_sha`, and confirmed both blobs match. That
self-correction is the reason the commission forbids absent-field equality as
verification, and I have used non-empty exact blob IDs throughout.

---

# PART 9 — Freeze graph, custody, and warrant state

## 9.1 Freeze graph — lawful, and the count discrepancy is pure counting basis

`01256977..8ff40d37`: first-parent count **3**, total reachable **5**. The two
extra reachable commits are exactly `1df64cc59` (C4C3 return) and
`eba2f4249` (its HQ bind) — the declared merge side. Nothing unreviewed.
Fan-in lineage is 47 files added, 0 modified, 0 deleted, all confined to
`WORKER_RETURNS/`.

`rawlsing_next` tree `b0c1ab472cde…` is identical at all seven points HQ182
named — `9a5752a8`, `8f7efe690`, `01256977`, `39015a90`, `f8c8e2e4`,
`8ff40d37`, `2836f625` — and I add C4C3's head `1df64cc59`, also `b0c1ab47`.

## 9.2 Warrant candidate — intact, unaltered, and non-authorizing

I recomputed the SHA-256 of
`04_SOURCE_EXECUTION_WARRANT_CANDIDATE.json` at the freeze:

```
d57420f8016bf49cc0353f39dcd2271e6f370c3bd9b7e81f08466c0a1f574e0a
```

This matches the value HQ182 recorded, byte-exact. The candidate is
unaltered. Its own state:

- `warrant_status: "CANDIDATE_ONLY__NOT_ISSUED__NO_RAW_ACCESS_AUTHORIZED"`
- `issued: false`, `signed: false`, `authorizes_access: false`,
  `execution_authorized: false`, `issued_by: null`, `issue_date: null`

**Five issuance blockers, all still open:**

1. `SOURCE_LOCATOR_FILL_REQUIRED_BEFORE_WARRANT_ISSUANCE` — **seven slots
   unfilled**. I confirmed all seven `access_locator` values are the literal
   placeholder
   `<REQUIRED_FILL_IN_SLOT__SOURCE_LOCATOR_FILL_REQUIRED_BEFORE_WARRANT_ISSUANCE>`.
   No locator search was performed, by design.
2. HQ approval `UNSET` (`name`, `decision`, `signature_or_commit` all null).
3. Required user / resource owner approval `UNSET`.
4. Warrant unsigned.
5. Independent integration review of the freeze not yet completed.

Note item 5: the freeze now has two completed independent reviews (Lane A at
`fe6103cd` and ALT-B at `3a5b2cbc`, both `APPROVE_AT_DECLARED_GRAIN`) and the
R2 re-check at `afb1eb49`. Whether item 5 is now discharged is an HQ call; I
record it as written in the instrument and do not close it myself.

---

# PART 10 — Current stage register (stage-separated)

Carried from HQ187 (`HQD-2026-10-02-187`) and independently confirmed against
`HQ_HANDOFF/LATEST.json`. Exact evidence required no correction.

| Stage | Count | Item |
|---|---|---|
| Blocking **freeze acceptance** | **0** | — |
| Blocking **warrant issuance** | **1** | **R9** — bind explicit per-access-layer measurement bases and limits into the issued warrant, all 7 authorised sources |
| Blocking **live execution** | **1** | **R7** — durable exact preservation with complete interpreter digest, or competent requalification |
| Advisory | **9** | non-blocking; see below |
| Counterexamples | **1** | the overbroad M01-closure justification (§1.4) |

Both pointers agree: `c4_residual_blocking_freeze_acceptance: 0`,
`c4_residual_blocking_warrant_issuance: 1`,
`c4_residual_blocking_live_execution: 1`, `c4_residual_advisory: 9`,
`c4_residual_counterexamples: 1`, `c4_reconciliation_counterexamples: 1`.

The advisory class carries the D2P recorded-but-unverified identities
(`checkpoint_identity 3fab15f3…`, `canonical_closure_identity f264dd8f…`,
which D2P expressly did **not** convert into passes), the 24-snapshots-over-18-
authorities disclosure, the cross-lane T3 attribution question (§8.2), the
cross-lineage reachability note (§8.3), bookkeeping-denominator normalisation,
the entry-point record, and the dispatcher's own capability ceiling. All are
conservative-direction; none blocks any stage.

---

# PART 11 — D2P custody position

`D2P/04_FINAL_DISPOSITION.json`:
`APPROVE_D2P_PORTABLE_EXPORT_AT_DECLARED_GRAIN__B001_B002_B003_CLOSED`.
B001 50/50, B002 24/24 with 208/208 per-object rows, B003 50/50 with 18/18 P2
mappings — all `CLOSED_ACCEPTED`. 10 packet files, 3,836,107 bytes, byte-identical
between source path and repo import; 9 of 9 hashable files match
`SHA256SUMS.txt`; zero stale.

Explicitly **not** established and **not** authorised: any physical or
empirical claim about the LiTS source; the 3,404,445,161-byte checkpoint's
SHA-256; the 120 withheld member digests; byte-reproducibility of the
extraction; the two recorded-but-unverified identities; raw-source C4
execution; fresh LiTS decode; a source warrant; C7; PRE-V3→V3.

---

# PART 12 — Holds, all preserved

Every one of these was verified as still in force at this branch tip, and none
is altered by this document.

| Hold | State |
|---|---|
| C4 freeze adoption into build | `NOT_ADOPTED_INTO_BUILD` |
| HQ182 temporary non-adoption hold | **UNLIFTED** |
| Source locator discovery and fill | **0 locators discovered**; 7 slots unfilled by design |
| Warrant issuance | **not issued**, unsigned, 5 blockers open |
| Raw source access | **0** — nothing opened, stat-ed, hashed, decoded or materialised |
| Live C4 execution | **not executed** |
| Production mutation | **0** |
| C7 | **held** |
| PRE-V3→V3 actor/person implementation | **held** |

HQ182's hold is expressly **temporary and narrow**: it withholds build
adoption pending external cross-model adjudication on the reserved C4
decision. The October 3 audit records that it "must not be expanded into a
standing requirement that all HQ decisions go to Astra." Ordinary
already-authorised HQ adjudications remain HQ work. That framing is carried
into the external packet.

---

# PART 13 — Lane status and the publication/runtime audit

**Lane A** (Sol final reviewer, `fe6103cd`):
`APPROVE_AT_DECLARED_GRAIN`. It independently raised the 21→23 correction
("producer-inclusive static C4 closure is at least 23 modules rather than the
C4C3 downstream trace's 21"), which my derivation confirms and tightens to
exactly 23. **Formally unadjudicated**: `c4_final_review_adjudicated: false`,
and HQ182 held "lane A adjudication". Its content was read during the OPS-04
`00` reconciliation. I record the state; I do not close the adjudication.

**ALT-B** (Space Bunny, `3a5b2cbc`): `APPROVE_AT_DECLARED_GRAIN`, adjudicated
at HQ182 as `UPHELD_AT_DECLARED_GRAIN__NOT_ADOPTED_INTO_BUILD`. HQ182 found
its R7 materially understated and upgraded it — an upgrade whose *wording*
basis is now corrected by §5 while its *blocking* status stands.

**October 3 publication/runtime audit** (`f68903fdd`, sealed `682016053`):
`REPAIRS_REQUIRED_FOR_AUTONOMOUS_DISPATCH__PRESERVE_PROJECT_WORK`. It found **no
production-tree damage**, confirmed net Git conservation, verified all
193 ledger rows parse and all fourteen referenced checkpoint blobs match, and
held that production tree and source hold are unchanged. It is **not** a C4
adoption decision and does not lift the C4 hold. Its dispatcher findings
(vacuous gates, queue/recovery/concurrency overreach, OPS-03 not qualifying
autonomous operation) are a **separate bounded workstream** from C4 adoption;
final technical C4 adoption "remains a distinct bounded decision, not a
consequence of fixing the dispatcher." Repair-plan item 6 is this
consolidation, at documentary grain, with no new source access.

---

# PART 14 — Consolidated current wording

Offered as the accurate current statement of the C4 technical position. It is
**not** an adoption decision and authorises nothing.

> The exact frozen source-free implementation of C4 is accepted at the declared
> source-free grain. The Route-B producer and carrier at the freeze are
> byte-identical to the M01-qualified candidate `46f3bec82`, whose bounded
> source-free court ran 61/61 (11 + 4 + 14 + 32; the 32 being 30 functions in
> `test_pre553_empirical_query.py` with one test parameterized over three
> refusal states), rebound at `74a06774`.
>
> That named-file identity is **not** whole-closure identity. The M01 court's
> transitive import closure is 23 modules, identical in membership at both
> states; 21 of the 23 are byte-identical, and `pre553_physical_decoder.py`
> and `pre553_r5_codec.py` were pre-C3 bytes at every M01 binding and are
> C3-accepted bytes at the freeze. **The M01 61/61 does not qualify the
> freeze's exact 23-module closure.**
>
> Authority for those two modules at the freeze is the accepted C3 six-file
> 55-test court plus C4C3's 55/55 executed twice, on a `rawlsing_next` tree
> (`b0c1ab47`) byte-identical to the freeze's; both modules are two of the six
> pinned accepted C3 blobs, all eleven pinned blobs verified EXACT at the
> freeze. The defect was in the record, not the evidence.
>
> C4C3's 21-module trace is a downstream trace beginning below M01 and was
> independently reproduced as exactly 21. Adding producer and carrier gives a
> producer-inclusive static closure of exactly 23 modules. Source-free M01
> qualification applies at M01's historical dependency state; later C3
> qualification and fresh Darwin C4C3 runtime qualification apply to the
> downstream path at C3-accepted bytes. **No claim is made that the complete
> producer-inclusive 23-module path was freshly rerun on Darwin.**
>
> R7 is both fingerprint incompleteness and weak environment reproducibility:
> the venv is non-durable at its path and the 13-package reproduce command
> does not pin the resolved `narwhals`. R9 is that explicit per-access-layer
> measurement and limits are not yet bound into the issued warrant for any of
> the seven authorised sources, with SRC27 governed by one governed full
> Route-B pass — maximum one, zero retries, and four separately counted access
> layers — and SRC35 under a zero-fresh-read law. Before any governed live
> run: durable exact environment preservation with a complete interpreter
> digest, or competent requalification.
>
> Stage-separated: 0 freeze-acceptance blockers, 1 warrant-issuance blocker,
> 1 live-execution blocker, 9 advisories, 1 counterexample — the counterexample
> being against an overbroad M01-closure justification, not against the
> existence of the freeze evidence base.

---

# PART 15 — What this consolidation does not do

It does not adopt the C4 freeze into the build. It does not lift HQ182's hold.
It does not issue, sign or alter a warrant. It does not discover, fill or
infer a locator. It does not access, stat, hash, decode or materialise any raw
source. It does not execute C4. It does not mutate production. It does not
implement C7. It does not implement PRE-V3→V3 actor or person work. It does
not edit `HQ_HANDOFF/**`, the historical OPS-04 `00`/`01`, or any historical
worker return. It does not adjudicate Lane A. It does not contact or invoke
Astra. It does not self-adopt. It does not merge into control.

Where the governing evidence contradicted a lane — including a lane I myself
adjudicated earlier — I recorded the contradiction against the evidence. Where
I refine an existing finding, I say so and state that the conclusion is
unchanged. Where I could not verify, I preserved the ceiling rather than
promoting the claim.

Terminal:
`OPS04_CURRENT_CONSOLIDATED_C4_CLAIMS_PREPARED__PENDING_ASTRA_RESERVED_DECISION__NO_ADOPTION__HQ182_HOLD_UNLIFTED__NO_SOURCE_ACCESS`