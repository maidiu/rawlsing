# PYAT R35 F6C — native A/B/C method comparative and consumer verdict

**Role:** existing bounded F6 scientific comparison worker. Not HQ, not an
original-source issuer, not an independent reviewer, not an actor/model issuer.

**Sealed commission head:** `fec96baf6b9a1e3379d308e486230a39b67ab2b8`
**Branch:** `agent/rabochii-pyat-r35-f6c-native-comparative-consumer-r1`
**Method:** executed native modules only, loaded by absolute path from verified
Git blobs, in cold separate processes. No documentation debate.

---

## 0. Bottom line

Repaired F6M (comparison B) is confirmed as the strongest supported candidate,
but only once it is compared against the **corrected** S03FO producer. Against
that corrected producer, method A — the historical native S03FO synthesis —
carries a real, reproducible defect: when a source stratum fails the aggregate
support gate, A silently renormalizes that source's planned mixture share onto
the survivors and reports **full coverage**. The same evidence loss under B is
retained as **unknown mass** and the point is refused.

This was reproduced twice: once in this court's own frozen worlds, and once
inside WP2's real consumer on WP2's own inherited frozen case.

**The amendment is not closed.** The sealed R35 commission still pins the
superseded blob and this worker has no authority to re-seal it. See §7.

---

## 1. Corrected source identity — and why it was not cosmetic

The sealed R35 commission pins S03FO to `182cc7970d7624f6614015f5a51d0602e1630d52`.
That blob is **superseded**. The real blob at the real commit and path is
`fc5e37fa5b2f0eb689593b42d95479d1327cb94c`.

The superseded blob is not a near-identical earlier draft. It is two defect
repairs behind on the same path:

```
69a168652 / c6dba4b70 -> 182cc7970d76...  20443 bytes
bb739fb6d (HQ284 S03F) -> b1b05e7d60f9...  21807 bytes  two F6 joint-domain and leakage defects
1428c2e92 (HQ287 S03FO) -> fc5e37fa5b2f...  22257 bytes  F6 canonical output-order defect
```

All blob SHA-1 values were recomputed with the method the HQ addendum specifies
(`sha1(b"blob " + len + b"\0" + bytes)`), not merely read from a report.

**Executed proof of the three missing repairs** (comparison A0, historical
custody control, explicitly *not* comparison A):

| case | `182cc797` (obsolete) | `fc5e37fa` (corrected) and `2df811d7` (F6M) |
|---|---|---|
| W5 positivity — source omits one native cell | confident point `{formal 22/35, informal 13/35}` | `SynthesisError: incomplete native joint domain; omitted category cannot be silently manufactured as zero (domain_size=4, observed=3)` |
| W4 outcome-as-its-own-condition | `SUPPORTED_MODEL` | `DESCRIPTIVE_SELF_CONDITIONING` / `OUTCOME_LEAKAGE_TAUTOLOGY` |
| category ordering | lexical `sorted()` | `category_map` insertion order (S03FO) |

Had the stale pin been used, comparison A would have published a confident
distribution built partly on an unobserved cell. **The correction is
scientifically load-bearing, not clerical.**

Independent textual confirmation: F6M's blob declares
`ORIGINAL_PRODUCER_BLOB = "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"`. The
repaired producer is derived from the **corrected** producer, not the obsolete
one — so the corrected identity is the fair basis for the A/B comparison.

**On the F6M commit reference.** The correction names
`1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa` where the sealed commission names
`5ed8e5389dd3510cf29a4947b04bd05901c8d213`. **This is not a defect.** Both
commits contain the identical blob `2df811d7...` at the identical path;
`5ed8e5389` is the later custody/publication commit. Zero effect on executed
bytes.

---

## 2. Frozen oracle, frozen before execution

`01_FROZEN_ESTIMANDS_AND_INDEPENDENT_ORACLE.json` was written before any
candidate was imported, and is validated by a separate program
(`repro/independent_oracle_recompute.py`) that imports **no producer** and
recomputes the expectations from the declared counts with `Fraction`.

That self-check earned its keep twice. It caught a genuine error in my own
hand-computed oracle: I had listed per-stratum contributions where the producer
emits a **single mixed target joint**. The corrected W1 conditional is
`formal 5/8, informal 3/8` over denominator `1/2`, not `3/5, 2/5` over `1/4`.
The oracle is frozen at the corrected values, and method A matched them exactly
on first execution — which is the only reason that agreement means anything.

Final self-check: **64 checks, 0 failures**.

---

## 3. What the court executed

Cold, two rounds, four distinct processes per round, distinct PIDs, scientific
content bit-identical across rounds. 11 inherited F6 files staged by
`git archive` and re-verified byte-exact against their pinned blobs (0
mismatches). No test rewritten, skipped or relaxed.

| suite | result |
|---|---|
| inherited F6M decision/admission repair (`f6110081`) | **20 / 20 pass** |
| inherited original F6 heterogeneous synthesis (`07f40503`) | **35 / 35 pass** (24 cases + 11 subtests) |
| R35 F6C A/B/C court | **40 / 40 pass** |
| R35 F6C WP2 consumer experiment | **23 / 23 pass** |

One custody control was required and is disclosed rather than hidden:
`preimport_pinned_producer`. `rawlsing_next` is a namespace package whose
portions are split between the test-run directory and the candidate directory;
pytest mutates `sys.path` during collection, after which the producer's portion
becomes unreachable and collection aborts with `ModuleNotFoundError` before a
single test runs. Pre-importing pins the correct pinned blob. This edits no
test, assertion or fixture — the same class of control WP2I already recorded.

---

## 4. A/B/C outcome on the scientific questions

Numbers are exact rationals. Full table in
`04_REAL_CONSUMER_DELTA_AND_ALTERNATIVE_RANKING.json`.

| | A (corrected S03FO) | B (repaired F6M) | C (no-pooling bounds) | A0 (obsolete) |
|---|---|---|---|---|
| W1 full coverage, disjoint | point, `5/8` / `3/8` | **identical** point | `[0,1]`, no transport admitted | identical |
| W2 source fails gate in one stratum | **point `7/10` / `3/10`, uncovered `0`** | refuses, uncovered **`1/4`** | `[0,1]` | same defect as A |
| W7 source excluded everywhere | **point `3/5` / `2/5`, uncovered `0`** | refuses, uncovered **`1/2`** | `[0,1]` | same defect as A |
| W3 stratum absent everywhere | refuses, uncovered `1/5`, **but decision still `SYNTHETIC_CANDIDATE`** | refuses, uncovered `1/5`, decision `PARTIAL_IDENTIFICATION_ONLY` | `[0,1]` | refuses |
| W4 outcome leakage | `DESCRIPTIVE_SELF_CONDITIONING` | identical | no predictive probability | `SUPPORTED_MODEL` |
| W5 positivity | raises | raises | refuses independently | **silent point** |
| W6 duplicate sample | `SOURCE_INDEXED_BACKOFF` | identical | refuses | identical |
| W8 condition out of support | refuses | identical | refuses | identical |
| `REAL_USE` request | not expressible | **always `UNAVAILABLE` / `UNVERIFIED_OWNER_ADMISSION`** | never applicable | not expressible |

### The decisive defect, stated precisely

In W2 and W7 method A reports `uncovered_target_mass = 0` and emits a confident
point, while the planned evidence for a quarter and then half the target was
destroyed. A takes its mixture denominator over **eligible** sources only, so a
dropped source's planned share is silently redistributed onto survivors.

The important nuance, which I checked rather than assumed: A's W2 conditional
(`7/10`) is *not* numerically identical to its W1 conditional (`5/8`). The
defect is **not** numerical blindness. The defect is that A reports full
coverage in both worlds, so **its output cannot distinguish a stratum that was
adequately measured from one that lost half its planned weight** — and it
presents the destroyed-evidence estimate at the same confidence grade as the
fully-supported one.

A is right on W3 for the wrong reason: it accumulates unknown mass only when
*no* source is eligible. It also mislabels that bundle
`SYNTHETIC_CANDIDATE` while carrying no distribution and `1/5` unknown mass —
A has no `PARTIAL_IDENTIFICATION_ONLY` state at all.

---

## 5. Second experiment — the required consumer

Three cold runs of the **unmodified** `wp2.py` (blob `55e567e4...`, WP2 commit
`f7824794...`), differing **only** in which pinned F6 producer blob was staged:
A, A0, B. `wp2.py` was never edited; each run got a fresh tree; the one
`discovery/staged_manifest.json` row that the substitution touched was updated
to the blob actually staged so WP2's own `import_manifest` assertion stayed
**true** rather than being bypassed. That is disclosed in the receipt, and those
runs' manifests therefore no longer certify the original F6M blob.

### 5.1 A real F6-caused value-read delta, on WP2's own inherited frozen case

Case `P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED`:

| | `uncovered_target_mass` | `decision` | value read |
|---|---|---|---|
| A | `0` | `SYNTHETIC_CANDIDATE` | `SUPPORTED_MODEL {NO: 1/2, YES: 1/2}` |
| A0 | `0` | `SYNTHETIC_CANDIDATE` | `SUPPORTED_MODEL {NO: 1/2, YES: 1/2}` |
| B | **`1/2`** | `PARTIAL_IDENTIFICATION_ONLY` | **`UNAVAILABLE / NO_COMPLETE_TARGET_JOINT`** |

Same inputs, different output. Identical input payloads are asserted across all
three methods (`test_the_same_F6_inputs_were_used_by_all_three_methods`), so
this is method-caused, not fixture-caused.

### 5.2 Not an unrelated edit

Exactly three top-level envelope keys differ — `call_counts`, `f6_sourcefree`,
`generic_read_only_input` — all F6's own accounting. Every empirical and
structural value is **bit-identical**: `actual_C1_returns` (79 native C1
returns), `actual_N10E_returns`, `at07_native_2x2`, `cases`, `edge_statuses`,
`hold`, `installation`, `terminal`.

### 5.3 Genuine scientific invariance

- `world_a`: all three methods return `formal 26/31, informal 5/31` — **equal
  values, three distinct bundle hashes** (`fb5f2815…`, `5b29fb32…`, `9a295f1e…`).
  Invariance that is bound to distinct provenance is credible; the same object
  counted twice would not be.
- `world_b`: all three refuse identically.

**On `26/31` and `5/31`:** these are not a validated real-world opportunity
probability and not a generated person's life-route probability. They are a
conditional read off a sourcefree experimental joint at `TEST_ONLY` grade, with
`uncertainty = CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED`.

### 5.4 The named consumer did not move — and why that is the correct answer

`NONPARENT_OPTIONS` consumer material SHA-256 is identical across A, A0 and B
(`0d9e0b3e68e39d95…`). The F6 sidecar moved; the world consumer did not.

This is **not** a broken experiment. At the permitted grade the F6 sidecar is
an inert sibling dict key with **no data-flow edge** to the consumer, and the run
says so itself: `state = UNINSTALLED_TEST_ONLY_PORT`,
`join_state = NO_AUTHORIZED_COMMON_WORLD_OR_RESPONDENT_JOIN`,
`hold = NAMED_N10W_RULE_HOLD`, `actor_executions = 0`, `model_calls = 0`.

An F6-caused change in the world consumer's material is exactly the finite
owner motion WP2 and WP2I both leave open and neither authorizes. Manufacturing
one would fabricate the join this court was told not to fabricate. **So the
honest outcome is invariance, and the reason for it is recorded rather than
papered over.**

Route/selection quantities: the run contains **15** `route_probability` slots
and **28** `selection_weight` slots. **Every one is `null`**, with
`route_probability_reason = NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL`. The
consumer is structurally offered these slots and refuses to fill them. Asserting
the keys were absent would have hidden that.

---

## 6. Scientific ranking

Pre-registered before execution; execution agreed.

**B (repaired F6M) — best supported candidate. Reuse.** It satisfies all six
criteria: positivity, planned-share preservation, partial-identification
refusal, conditioning honesty, overlap blocking, no route quantity. It also
fails closed on `REAL_USE` unconditionally.

**C (no-pooling bounds) — necessary complement, not a replacement.** C refuses
to mix sources under any circumstance, so with two admissible sources per
stratum it yields complete ignorance and discards everything B learned. It is
strictly weaker wherever transport is admissible. But C is still needed for
three reasons: neither A nor B emits a genuine `[q, q+unknown]` marginal
interval (B emits a covered subprobability plus a scalar that the *reader* must
recombine); B's per-cell disagreement bounds span only the covered share and so
are **not** marginal bounds; and C enforces positivity and
distinct-respondent checks itself rather than trusting a producer. Executed
proof: with one source admitted for the majority stratum only, C yields
`formal [13/40, 33/40]` where B would have offered only the covered component.

**A (corrected S03FO) — do not adopt as the F6 producer.** Sound on positivity,
leakage, overlap and route discipline; **fails on unknown-mass preservation and
partial-identification refusal** in exactly the cases that matter.

**A0 (obsolete `182cc797`) — must not be used.** Demonstrated to violate
positivity, conditioning honesty and ordering.

---

## 7. Open blocker — amendment authority

The sealed R35 commission still pins `182cc797…`. Competent HQ has **already**
established the correction by addendum
(`PYAT-R23-F6C-NATIVE-F6-COMPARATIVE-CONTINUATION-R1/01_HQ_R24_S03FO_EXACT_BLOB_CORRECTION_AND_NATIVE_PROOF.md`
at `11f5fd571…`, carried in the R25 checkpoint), and R26 F6I independently
confirmed it. But **no addendum is attached to the R35 commission**, and this
worker is not HQ and holds no delegation to re-seal a commission.

**The R35 `00_COMMISSION.md` was not edited.** All prior records stand verbatim.
This is recorded as an **OPEN** blocker in
`06_CORRECTIVE_AMENDMENT_AND_AUTHORIZATION_BLOCKER.json`, with the minimum
competent action requested: attach the R24 blob-correction addendum to the R35
commission directory, or record an explicit succession note so the stale pin is
superseded by reference rather than by edit.

Risk if left unresolved: a future worker reading only the R35 text will stage
`182cc797…` as comparison A and publish a confident distribution built partly on
an unobserved cell.

---

## 8. Unresolved ownership, carried forward unresolved

- **Original source ownership.** These are synthetic, source-free tables. No
  original survey, weight, design or sampling frame was granted or used. The
  invariant across all worlds is
  `NO_CROSS_SURVEY_RESPONDENT_LINKS`. Respondent-level joins were never
  invented; W6 proves the code refuses when lineage and sample collide.
- **Transport ownership.** `conditional_invariance_status = REVIEWED_ASSUMPTION`
  is an assumption, not a finding. No competent owner has admitted transport.
  That is precisely why method C reports `[0,1]`.
- **Model/actor ownership.** Untouched. `actor_executions = 0`,
  `model_calls = 0`, all route/selection slots null. F6 remains
  `F6M_I2_METHOD_CANDIDATE__NO_INSTALL`.
- **F6M adoption.** B is the best *supported candidate* for this bounded
  comparison. It is **not** an adopted F6C winner and this return does not
  promote it.

---

## 9. Delivered

| artifact | content |
|---|---|
| `00_NATIVE_METHOD_COMPARATIVE_AND_CONSUMER_VERDICT.md` | this document |
| `01_FROZEN_ESTIMANDS_AND_INDEPENDENT_ORACLE.json` | oracle frozen before execution + pre-registered ranking |
| `02_EXACT_F6_OWNER_BLOB_IMPORTS_AND_CUSTODY.json` | exact blobs, native imports, environment passport, custody controls |
| `03_EXECUTABLE_JUNIT_AND_TWO_COLD/` | 4 real JUnit files + inherited-suite replay receipt |
| `04_REAL_CONSUMER_DELTA_AND_ALTERNATIVE_RANKING.json` | exact values read by the consumer, provenance, ranking |
| `05_SPECIFIC_COMPETENT_SCIENCE_OWNER_MOTION.md` | the finite decisions requested |
| `06_CORRECTIVE_AMENDMENT_AND_AUTHORIZATION_BLOCKER.json` | OPEN amendment blocker |
| `05_COLD/round1, round2` | per-candidate cold JSON, A / A0 / B / C |
| `consumer_runs/` | three real `wp2.py` runs + substitution receipt |
| `02_TESTS/`, `repro/` | court and consumer tests; all reproducers |

**Not issued:** no original source, no semantic, no actor, no model, no Field
Forge meaning, no N11/N12, no V3, no route probability, no selection weight, no
production promotion.