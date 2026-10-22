# R56-R02V r2 — affected independent requalification — RETURN

**Disposition:** `ACCEPT_SCOPED_LOCAL__R02V_R2_AFFECTED_REQUALIFICATION_PASS`
**Commission:** R56-R02V affected requalification, task I2–I3/S3, under
`WORKER_COMMISSIONS/PYAT-R56-FIRST-REPAIR-FLIGHT-R1/REVIEW_SHARED_START_AND_RETURN.md`
at `485f31e52ca82905dcfbbc79c5f8c8294fb55f49` and
`NATIVE_SHARED_EXECUTION_CONTRACT.md` at
`eb28fdcc311e2534b66def445e745cb25cb8a9bd`.
**Candidate:** `6f4be33854c0437a52e1c49b977104db111ac327`
(`agent/rabochii-pyat-r56-r02-occurrence-projection-repair-r1`).
**Reviewer branch:** `agent/rabochii-pyat-r56-r02v-r2-projection-requalification-r1`.
**Return root:** `WORKER_RETURNS/PYAT-R56-R02V-INDEPENDENT-NATIVE-REVIEW-R1/revisions/r2/`.
**Frozen policy:** `6d95a78bf6b7bcf70022e303a151255e65edc38a` read-only.

## Session and startup

This is a fresh independent reviewer session, distinct from the author repair
session `ses_e9dea5a24ffeBtsLScgC81lfet` and from the original R02V review.
The former R02V session authored the repair and was not used as independent
evidence. Exact session, model, provider, host, usage and duplicate-reviewer
checks are in `01_SESSION_AND_STARTUP_PROVENANCE.md`.

The remote candidate branch head equalled the pinned candidate
`6f4be33854c0437a52e1c49b977104db111ac327` at start and remained there through
this pass. The candidate is the author r2 repair head; its parent
`236fd4d1064f7c14113616db300c955294a474ac` is an ancestor. The pinned author
r2 return at `6f4be338.../revisions/r2/` and the original reviewer evidence at
`a287674b97a2bbde4bf9acf3b6badf19b5ce72f5` were read as evidence, not imported
as acceptance.

## Public path exercised

No mock returned authored expected values. The exercised route was:

```
pre553_source_native_preimage_adapter.materialize_native_preimages
  -> unchanged pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream
  -> unchanged C11 validation/repository
  -> unchanged pre553_empirical_query.execute_empirical_query (real I03)
```

Production files were read-only. The adapter SHA-256 at start and after the
proof witness is
`c9ea22ada390babf7b3a977352b784bcfeb498e738dcb0024fc7f4d793b90b95`,
the author-declared repaired hash. The unchanged facade, C11, I03 and decoder
hashes are in `02_EVIDENCE_INDEX_AND_COUNTS.md`. `git diff` over all production
paths is empty.

## Targeted acceptance results

### 1. Both original mappings refuse before C11/I03

Both original reviewer reproducers were re-run against the repaired public
adapter. Both now refuse, with no bundle, C11 release, or I03 fact returned:

| Original input | Actual typed refusal | Detail |
|---|---|---|
| `{0: "1", 1: 1}` | `DUPLICATE_RESPONDENT_KEY_MAPPING` | `1` |
| `{0: "P0", "0": "P1", 1: "P2"}` | `DUPLICATE_NORMALIZED_SOURCE_KEY` | `0` |

The same assertions were added through the public adapter in
`test_r2v_r2_original_collision_mappings_refuse_before_c11`, not through a
local plan-validation helper. A test-only sentinel on the unchanged facade
release builder confirms the refusal occurs before C11 construction. The
original defect scripts, imported from `a287` and executed against the repaired
candidate, print exactly those refusals
(`evidence/defect_scripts_on_repaired_candidate.txt`).

### 2. Normalized uniqueness and type admission

`test_r2v_r2_normalized_admission_uniqueness_matrix` independently varies
non-literal source identities and destination representations. It confirms:

- duplicate normalized destination keys refuse, including `10 -> 20` versus
  `11 -> "20"` and `0 -> True` versus `1 -> "True"`;
- duplicate normalized source keys refuse, including `20` versus `"20"` and
  `0.0` versus `"0"`;
- non-finite floats, empty strings, `None`, bytes, tuples, lists and mappings
  refuse with typed codes;
- a legitimate mapping with mixed int/string/float source keys and injective
  string/numeric destinations preserves exact respondent/occasion/value tuples
  and a source-derived prospective I03 domain (`SUPPORTED`, denominator 4,
  numerator 4, 12 events);
- a numeric-destination mapping `{0: 7, 1: 8, 2: 9}` preserves respondent keys
  `7`, `8`, `9`; a non-literal `{10: "P10", 11: "P11"}` mapping preserves its
  exact tuples and `SUPPORTED` denominator 2;
- interleaved/reversed row order preserves the exact tuple set and each run's
  own source-derived domain.

No literal `0`/`1` collision special case was found. The checks operate on the
admitted token representation before the lookup dictionary is built.

### 3. Required suites, counts and overlap

| Run | Result | Evidence |
|---|---|---|
| 15 author tests | 15 passed, 0 failed, 0 skipped | `evidence/pytest_author15.log` / `.xml` |
| 9 ported reviewer tests (7 positives + 2 defects) | 9 passed, 0 failed, 0 skipped | `evidence/pytest_reviewer9.log` / `.xml` |
| 26 pre-existing focused tests (15 author + 11 r2) | 26 passed, 0 failed, 0 skipped | `evidence/pytest_focused26_preexisting.log` / `.xml` |
| 31 full focused tests (26 + 5 independent r2v-r2 additions) | 31 passed, 0 failed, 0 skipped | `evidence/pytest_full31.log` / `.xml` |
| 42 retained facade + empirical-query tests | 42 passed, 0 failed, 0 skipped | `evidence/pytest_retained42.log` / `.xml` |
| Proof AST lint | `AST_LINT_PASS` | `evidence/proof_lint.json` |
| Proof witness, 8 claims | baseline PASS; `TARGET_ASSERTION_FAILED` under each fault; adapter restored | `evidence/proof_witness.json` |

Overlaps are recorded honestly: the 15 author tests and the 9 ported reviewer
tests are subsets of the 26 pre-existing focused tests; the 26 are a subset of
the 31 full focused tests. The five independent additions are exactly
`test_r2v_r2_*`. Distinct focused+retained evidence is 73 tests (31 + 42), not
a sum of overlapping suite counts. No test was skipped.

### 4. Retained positives and same-assertion fault/restore

The 9 ported reviewer tests were rerun and passed, covering the actual
S1/scalar path, separate-unit S2 person and household positives with distinct
release refs, the cross-unit refusal, MR/rank consumption, unadministered-rule
holding, typed missingness, and the envelope binding. The independent
`test_r2v_r2_scalar_and_separate_unit_positives_retained` rechecks the S1
seven-row scalar positive (`SUPPORTED`, denominator 7, cell counts 3/4) and the
S2 separate-unit positives/unlinked refusal.

`test_r2v_r2_source_domain_faults_same_assertion_and_fresh_restore` freezes the
expected tuples and prospective I03 domain from the generated source cells and
governed mapping before inspecting candidate events. On that same frozen query
assertion it then:

- omits a selected cell: adapter refuses `SELECTED_VARIABLE_CELL_ABSENT`;
- remaps occurrence order: event tuples differ and the same query is no longer
  `SUPPORTED` with the baseline fact ref;
- replaces one value: event tuples differ and the same query is no longer
  `SUPPORTED` with the baseline fact ref;
- restores baseline in a fresh Python process and reproduces the exact
  baseline fingerprint (`state`, fact ref, denominator, numerator, cells).

### 5. Binding-envelope limitation

The transformed `NativePreimageBundle.physical_stream` remains explicitly
bounded to the tested adapter -> unchanged facade/C11 -> unchanged I03 route.
It is not claimed to be a raw `PhysicalCell` stream and is not a general
compatibility repair. The inherited strict-receiver limitation is not lifted:
a direct probe of
`fiabc_lits_i_representation_authority.authorized_banked_raw_value` with the
transformed occurrence declaration still refuses with
`ValueError: LiTS observed representation has unexpected missing declaration`
(`evidence/strict_receiver_bound_retained.txt`). The unchanged
`test_r02v_envelope_preserves_raw_declaration_and_binds_occurrence` also passes,
confirming the original declaration is nested while raw value/missing state are
unchanged.

## Proof integrity

The proof sibling
`rawlsing_next/tests/test_universal_source_projection.py.proof.json` is a
non-executable documentary sidecar. It retains the author's four claims and adds
four independent claims: original destination-collision refusal, original
source-key refusal, mixed-identity tuple/domain conservation, and same-domain
respondent-assignment fault. The witness disabled each named production
dependency, observed the named test fail by assertion, and restored the exact
adapter bytes. The post-witness adapter SHA-256 equals the candidate hash
`c9ea22ad...`; `evidence/proof_restore_receipt.txt` records the readback.

## Engineering / science / authority

**Engineering:** `ACCEPT_SCOPED_LOCAL`. The two original false-population paths
refuse at the repaired public adapter boundary before C11/I03, legitimate
numeric/string identities and injective destinations retain exact tuples and
prospective I03 domains, and the required retained suites and proof witness
pass.

**Science:** `NOT_ASSERTED`. TEST_ONLY synthetic sourcefree fixtures only. No
original SAV/DTA, original respondent data, original35, E_pre, F1–F8,
learned/world, actor, N11 or N12 issuance. No scientific meaning is promoted
from synthetic values.

**Authority:** `NOT_ASSERTED`. No production adoption, protected CI, R00E gate,
R03/compiler/lowering, R04.byte/R04.joined, R05/R06, original-source, or
N11/N12 claim. J52/W52 remain stopped. Gate-qualified combined functioning is
not implied by this isolated targeted pass.

## Residual observations (inherited, not defects in this pass)

- `row_occurrence_plan=None` remains the S1 scalar path; omitting a plan on a
  repeated source remains a caller-contract boundary.
- Incomplete order fields still fail closed at I03
  (`INTEGRITY_FAILURE`/`UNRESOLVED`) rather than fabricating support.
- The raw exact-duplicate destination guard can refuse raw-equal but
  normalized-distinct scalar destinations such as `1`/`True` before the
  normalized check; this is conservative over-refusal, not false population,
  and lies outside the requested numeric/string destination controls.

## Next action

No new investigation or general court. If a later ordinary defect is found, it
goes to the same R02 adapter owner with a minimum reproducer. This finite
targeted pass is complete.
