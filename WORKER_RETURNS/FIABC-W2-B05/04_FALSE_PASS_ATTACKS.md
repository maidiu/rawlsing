# FIABC-W2-B05 — False-PASS Challenge Cases

The filename is fixed by commission. The substance here is a bounded set of challenge cases designed to make an apparently complete succession manifest pass when the required functional/authority/execution chain is actually incomplete. Each loophole is closed by a schema field plus a deterministic preflight rule.

## FP01 — Floating branch ref masquerades as exact evidence

**False-PASS construction:** populate every evidence field with a plausible branch/path but omit the exact resolved commit or allow `latest` behavior.

**Why it can look valid:** every named artifact exists and a reviewer can open it.

**Closure:** `evidenceRef.resolved_commit_sha` is mandatory; P00 verifies ref resolution and declared content identity. A changing branch ref cannot silently validate a receipt or authority at a different commit.

**Expected BLOCK:** `PF_REF_UNRESOLVED` or `PF_FLOATING_OR_FUZZY_REF`.

## FP02 — Historical bytes occupy the current-owner slot

**False-PASS construction:** point `current_owner` at a surviving historical V550/V551/D15/C06/PostgreSQL implementation because it still contains the needed function.

**Why it can look valid:** the function/evidence genuinely survives.

**Closure:** `owner_status` is explicit. Only `CURRENT` can satisfy P03. A superseded implementation can support genealogy/equivalence evidence but cannot become current by survival.

**Expected BLOCK:** `PF_OWNER_SUPERSEDED_OR_HISTORICAL`.

## FP03 — Adopted module exists but the runnable graph never calls it

**False-PASS construction:** provide a valid current owner path and stop the proof there.

**Why it can look valid:** repository archaeology shows the correct implementation is present.

**Closure:** separate `executable_binding` and `live_consumer` nodes are mandatory. P04 requires producer-to-consumer binding; P05 requires a governed receipt from the exact execution ref.

**Expected BLOCK:** `PF_EXECUTABLE_BINDING_MISSING` and/or `PF_LIVE_RECEIPT_MISSING`.

## FP04 — Stale path points toward the right authority family

**False-PASS construction:** record the right authority identity/commit while runtime still opens a retired or nonexistent directory name.

**Why it can look valid:** semantic authority is not actually missing.

**Closure:** the executable binding has its own exact ref and must resolve at the consuming commit. Authority identity cannot compensate for a stale runtime path.

**Expected BLOCK:** `PF_BINDING_REF_STALE` or `PF_REF_UNRESOLVED`.

## FP05 — Local wrapper shadows the accepted producer

**False-PASS construction:** import the accepted binder but call a same-named local wrapper that recursively invokes itself or otherwise bypasses the imported owner.

**Why it can look valid:** source inspection sees the correct import and symbol name.

**Closure:** P04 requires `binding_identity_matches_owner=true` plus a contract receipt from the production entrypoint. Symbol-name similarity is not accepted as owner identity.

**Expected BLOCK:** `PF_BINDING_OWNER_MISMATCH` or `PF_WRAPPER_SHADOWS_CURRENT_OWNER`.

## FP06 — Candidate self-replay masquerades as parity

**False-PASS construction:** run Candidate A twice through the same binding, hash both results, and populate semantic/replay/frontier parity fields from their equality.

**Why it can look valid:** repeatability is real and hashes match.

**Closure:** the parity oracle must be frozen before candidate output and `candidate_output_used_to_construct_expected_truth=false`. Candidate self-replay is explicitly nonqualifying as cross-candidate expected truth.

**Expected BLOCK:** `PF_SELF_REPLAY_USED_AS_PARITY` plus the relevant oracle-freeze code.

## FP07 — Negative states collapse to generic empty/None

**False-PASS construction:** normalize `UNKNOWN`, `INAPPLICABLE`, physical missingness, `VALID_EMPTY`, integrity failure, `DENIED`, or `NONCOMPARABLE` into one generic absent value while preserving positive facts.

**Why it can look valid:** many ordinary queries still return the same positive values.

**Closure:** each function chain carries explicit `negative_state_law`, required distinctions, a no-collapse flag, and consumer preservation evidence. P06 compares the governed state set and its live preservation.

**Expected BLOCK:** `PF_NEGATIVE_STATE_COLLAPSE`.

## FP08 — Missing Candidate-C production capability is relabeled not-applicable

**False-PASS construction:** omit LiTS-C or WVS-C from the comparison after discovering that production determinants, atom preimages, or portable execution do not exist.

**Why it can look valid:** the remaining A/B cells can execute a clean common workload.

**Closure:** every frozen source×candidate cell has a required capability row. A not-applicable escape needs competent scope/candidate-contract authority established before measurement; otherwise a missing production capability stays a typed blocker.

**Expected BLOCK:** `PF_SOURCE_CANDIDATE_CAPABILITY_MISSING` or `PF_UNAUTHORIZED_NOT_APPLICABLE_ESCAPE`.

## FP09 — Synthetic/test determinants substitute for production realization

**False-PASS construction:** satisfy a missing real-source capability using synthetic B20/test determinants or partial role bindings whose types match the production constructor.

**Why it can look valid:** the code path can become executable and type-correct.

**Closure:** source×candidate rows set `synthetic_fixture_substitution_forbidden=true`; P08 requires production realization and exact source provenance.

**Expected BLOCK:** `PF_SYNTHETIC_FIXTURE_SUBSTITUTION` and, where applicable, `PF_PARTIAL_PREIMAGE_SET`.

## FP10 — Binder-valid semantic promotion fills a genuine authority gap

**False-PASS construction:** promote an available source field into a required semantic role because doing so makes the C11 binder complete.

**Why it can look valid:** the raw field meaning may be adjacent to the requested role and the resulting package validates mechanically.

**Closure:** accepted authority is a separate node from binder validity. P02 requires exact downstream use/scope authority. No label, raw meaning, geography, code, or distribution may manufacture the missing semantic relation.

**Expected BLOCK:** `PF_AUTHORITY_MISSING` or `PF_SEMANTIC_INFERENCE_SUBSTITUTION`.

## FP11 — Same metric labels hide different work

**False-PASS construction:** give A/B/C the same terminal metric keys while one value is candidate-total CPU, another is the last nested call, one RSS value is process-global, or one rebuild metric times only receipt writing.

**Why it can look valid:** the vectors are rectangular and numerically comparable.

**Closure:** every comparison metric has an exact definition ref, accumulation semantics, candidate-local flag, non-overwrite state, measurement kind, and cross-candidate method identity. P09 compares meanings, not labels.

**Expected BLOCK:** `PF_METRIC_METHOD_MISMATCH`, `PF_METRIC_NOT_CANDIDATE_LOCAL`, `PF_METRIC_OVERWRITTEN`, or `PF_DOCUMENTARY_VALUE_MISLABELED_OBSERVED`.

## FP12 — Stale live receipt validates newer wiring

**False-PASS construction:** after a repair fan-in, reuse a governed receipt from the pre-repair run because it exercised the same named stage.

**Why it can look valid:** stage names and source/candidate IDs are unchanged.

**Closure:** the live-consumer node records execution-code ref and requires `receipt_code_commit_matches=true` and `receipt_after_required_repairs=true`.

**Expected BLOCK:** `PF_LIVE_RECEIPT_CODE_REF_MISMATCH` or `PF_LIVE_RECEIPT_PREDATES_REQUIRED_REPAIR`.

## FP13 — Deferred work is skipped without competent boundary authority

**False-PASS construction:** mark difficult F019-F024 or another inherited function as post-cut merely because current code does not need it to reach a convenient output.

**Why it can look valid:** the runnable graph becomes internally complete.

**Closure:** a deferred function requires `INTENTIONALLY_DEFERRED_BEYOND_TERMINAL` plus `deferment_authority_ref` tied to the adjudicated comparison boundary. Implementation convenience is not a boundary decision.

**Expected BLOCK:** `PF_DEFERMENT_UNPROVED`.

## FP14 — `GENUINELY_MISSING` is used before falsifying disconnection/supersession/deferral

**False-PASS construction:** label any unresolved row genuinely missing and remove it from the executable closure expectation.

**Why it can look valid:** the present branch does not contain an obvious usable object.

**Closure:** schema conditionally requires `missingness_search` with five explicit checks and evidence refs before `GENUINELY_MISSING` is valid. This preserves the Wave-1 distinction between disconnected accepted capital, superseded implementations, lawful deferral, and true absence.

**Expected BLOCK:** `PF_MISSINGNESS_NOT_FALSIFIED_FIRST`.

## FP15 — Semantic owner and cost owner are silently treated as one field

**False-PASS construction:** because an upstream authority owns truth, exempt all candidate realization work from cost; or because a candidate pays realization cost, treat the candidate as semantic owner.

**Why it can look valid:** one ownership label appears simpler and can make accounting symmetric on paper.

**Closure:** `abc_class.semantic_owner_id` and `cost_owner_id` are separately required. The accounting contract also requires `semantic_owner_cost_owner_separated=true`.

**Expected BLOCK:** `PF_SEMANTIC_COST_OWNERSHIP_CONFLATED`.

## FP16 — Common infrastructure failure becomes candidate evidence

**False-PASS construction:** serialize a driver/verifier failure under the currently executing source×candidate row and continue comparison of remaining cells.

**Why it can look valid:** the failure occurred while that candidate was active.

**Closure:** P10 requires explicit failure-scope ownership and lifecycle sequencing. Common, source-wide, candidate-local, and court-wide failures cannot be interchanged.

**Expected BLOCK:** `PF_FAILURE_SCOPE_MISCLASSIFIED` and/or `PF_LIFECYCLE_ORDER_MISMATCH`.

## Result of the challenge set

No challenge above reaches PASS under the specified schema plus P00-P10 evaluator. The important closure is structural: a manifest cannot pass merely by naming the right files. It must prove exact authority, currentness, executable binding, live consumption, negative-state/provenance conservation, lawful A/B/C scope, independent parity, and equal-work accounting as separate links.
