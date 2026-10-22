# R56-R02V — open-challenge adjudication

This file adjudicates the six challenges in the author's
`03_R02V_HANDOFF_AND_OPEN_CHALLENGES.md` within this finite engineering pass.
It does not issue source semantics, production adoption, or scientific
acceptance.

## 1. `source_missing_declaration` physical-binding envelope

**Author use.** Every selected response cell is transformed so that
`source_missing_declaration` becomes:

```
{
  "schema": "PRE553_GOVERNED_OCCURRENCE_BINDING@1.0.0",
  "source_declaration": <the decoder declaration, verbatim or null>,
  "occurrence_key": <governed occurrence key>,
  "source_value": <governed source occasion token>,
  "fields": <governed multiplicity/order/rank fields>
}
```

The facade's `physical_value_binding_key()` then hashes the whole envelope, so
two physical cells with the same raw value and missing state but different
governed occurrences acquire different binding keys. The C11 event still
carries the unchanged raw value through `raw_physical_value_witness()`. The
adapter does not alter `raw_value`, `missing_state`, or `raw_value_label`.

**Independent checks performed.** `test_r02v_envelope_preserves_raw_declaration_and_binds_occurrence`
builds an exact two-row stream with the same user-missing declaration on both
occurrences, confirms the decoder declaration is nested verbatim, confirms the
top-level schema/occurrence/source/fields identity, confirms raw value and
missing state are unchanged, confirms the two occurrence binding keys differ,
and confirms re-hashing the same envelope is stable. It also confirms a
non-response cell (`PID`) keeps its original declaration.

**Adjudication.** Within the exact R02 `adapter -> unchanged facade -> C11 ->
I03` path this is a bounded compatible engineering use: the facade treats the
declaration as opaque binding material, the C11 event exposes only the raw
value, and the original declaration is preserved nested. It does not issue a
new source meaning and it does not by itself fabricate substantive support.

It is not a general substitute for a decoder `PhysicalCell`. Two exact
receivers will reject the envelope if it is passed to them outside this path:

- `rawlsing_next/fiabc_lits_i_representation_authority.py::authorized_banked_raw_value`
  raises `ValueError: LiTS observed representation has unexpected missing
  declaration` for any non-`None` declaration on an observed cell. A live
  probe is recorded in `evidence/envelope_strict_receiver_probe.out.txt`.
- `rawlsing_next/fiabc_lm2_r1e_common_c11.py::_cells` compares the carrier
  declaration to the decoder-packed declaration and raises
  `source missing-declaration drift` on a mismatch.

No receiver in the tested R02 path performs either check. The returned
`NativePreimageBundle.physical_stream` is therefore a **transformed** stream,
not the raw decoder stream; consumers must not treat it as raw custody. The
adapter preserves the original declaration nested but does not preserve the
top-level declaration identity. That is the exact interface boundary. A future
revision should name/export the transformed stream explicitly (or add a
separate occurrence binding carrier) before any other receiver consumes it.

**Residual missing-state scope.** All non-observed decoder states are projected
to the C11 event state `MISSING`. The original declaration remains in the
transformed physical stream, but the C11 release does not distinguish
system-missing from format-user-missing, DK, or refusal. That is a conservative
boundary, not invented support. R02 does not claim DK/refusal discrimination.

## 2. Query domain constructed from emitted event IDs

**Author pattern.** `domain_from_bundle()` walks the candidate release and
builds the I03 target domain from the emitted event IDs. This is circular: if
the candidate omits or remaps an event, the candidate-generated domain can
shrink with the output. The author's missingness test also uses
`canonical_response_value_if_authorized` directly, which yields `None` for a
missing event instead of I03's `{"typed_response_state": "MISSING"}`.

**Independent replacement.** `test_r02v_prospective_domain_exact_tuples_permuted_and_alternative_labels`
and `test_r02v_missingness_is_typed_and_resolvable` freeze the domain from the
generated source cells, the governed row/occasion mapping, and the event
identity formula in the unchanged facade (`_event`). The oracle reproduces the
C11 respondent/question/projection identities and the physical binding key
from those inputs; it does not read emitted event IDs first. The resulting
domain matches the candidate for 4 respondents x 3 occasions (interleaved
rows, alternative occurrence labels) and for 3 respondents x 2 occasions with
a missing cell. I03 returns `SUPPORTED` with exact cell values.

**Fault demonstration.** `test_r02v_prospective_domain_catches_omission_remap_and_value_fault`
uses the same frozen domain while applying, in memory and with the source SHA
held fixed:

- an omitted selected cell, which the adapter refuses with
  `SELECTED_VARIABLE_CELL_ABSENT` before a release exists;
- an occurrence-field remap, which changes the realized ordered cell and makes
  the same query non-`SUPPORTED` with a different fact ref;
- a value replacement at one cell, which changes the event identity and makes
  the same query non-`SUPPORTED` with a different fact ref.

A fresh subprocess reading the restored baseline fixture reproduces the
baseline fingerprint.

**Adjudication.** The candidate's row/occasion/value behavior is independently
supported, but the author's `domain_from_bundle()` is not a prospective oracle
and its missing-value representation is wrong for I03. The reviewer added the
source-derived oracle; the author should not cite the emitted-domain test as
independent evidence. This is a test-quality defect, not a production defect.

## 3. Administration/form scope

- The unadministered rule is held as `HELD_NOT_ADMINISTERED`; no question ref
  or response event is created for it. Reproduced in the author test and in
  `test_r02v_mr_rank_admin_are_consumed_at_their_topology`.
- `MR1` is consumed as `MULTISELECT` and `RANK1` as `ORDERED_SEQUENCE` through
  the real I03 consumer; both return `SUPPORTED` with the exact expected cell
  values at denominator 2. The same test confirms the held variable is absent.
- A scalar `FORM` repeated across physical rows with two `SCALAR_SINGULAR`
  bindings is refused as `SCALAR_OCCURRENCE_PLAN_AMBIGUOUS`. This is the correct
  supported-scope boundary: without a governed form/occurrence rule the
  adapter must not collapse repeated rows. Reproduced by the author test.

**Adjudication.** Accepted boundary. No form semantics were silently collapsed;
the refusal is honest. This pass does not add a form-constant rule.

## 4. S1 scalar and S2 separate-unit scope

- **S1 positive:** `test_r02v_s1_scalar_and_s2_separate_unit_positives` builds a
  seven-row rectangular scalar source, obtains seven exact `ROW-nnnn`
  respondent/occ-0/value tuples, and gets `SUPPORTED` with denominator 7 and
  cell counts 3/4.
- **S2 positive:** the same test builds a person-unit package and a separate
  household-unit package at their own grain. Each has three exact row tuples,
  each returns `SUPPORTED` with denominator 3, and the two release refs differ.
  This demonstrates that separate-unit positives still work; it is not merely
  the adapter's refusal of pooled input.
- **Cross-unit refusal:** a package selecting household `HMEAS` and person
  `OUTCOME` together is refused with `CROSS_UNIT_POOLING_UNAUTHORIZED`.

**Adjudication.** The R02 preservation boundary is satisfied at the existing
one-unit-per-package grain. No linked household/person positive is claimed; the
R00P-R2 policy defers that link. The author's refusal-only S2 test was
insufficient on its own, and the independent positive test now covers it.

## 5. Source identity stability

The synthetic SAV writer's bytes vary per Python process. Three fresh-process
generations of the same logical rows produced three different source SHA-256
values. Deterministic binary bytes are therefore not required for this review:
the independent oracle derives its expected event identities and query domain
from the actual run's source SHA and decoded cells, and the receipt records the
exact per-run source, release, and fact hashes.

Exact examples in `evidence/r02v_independent_receipt.json`:

- 4x3 interleaved: source `9b8acd92c24213a0eb5b7b47ddbeed85669f4162125f6db4c5a419772bd2e8a0`,
  release `459e6f05d61d1c25867e8291ddecf0a934b1f024b39ec7b781df4fa9d5bb4ed5`,
  fact `3164d309c383251d1df0dce57ce087169617cee924d5b6ffaad7be63fa698a8d`,
  `SUPPORTED`, denominator 4, 12 events.
- 3x2 with one missing cell: source `d2d82e072813039a7f31899417d1e660ca2929a6332084262f79eca707253134`,
  release `c14c251e38d8256999f90312be540ec59274fe033bb70fd492f514263e31a361`,
  fact `c118ba2bc01c30eb23bca427d6ef072311996d4524df34142fc570c13fb5a48f`,
  `SUPPORTED`, denominator 3, 6 events.

**Adjudication.** Acceptable for review replay. A committed deterministic binary
fixture is not required. The exact run hashes are recorded; the source is
replayable from the test generator.

## 6. No R00E gate

R00E/R00V gate implementation was not used, not imported, and not claimed. The
independent tests exercise the actual adapter, unchanged facade/C11, and
unchanged I03 consumer only. Any gate-qualified integration claim remains
`NOT_RUN`. R03/compiler/original35/N11/N12 and all protected holds are
unchanged.

## Additional finding: incomplete occurrence fields

An `OccurrenceBinding` for `REPEATED_EVENT` whose fields contain only
`{"kind": "REPEATED_EVENT"}` is accepted by the adapter and a C11 release is
built. A correct I03 query over that release does not fabricate support:
`test_r02v_incomplete_order_fields_do_not_fabricate_support` observes a typed
`INTEGRITY_FAILURE`/`UNRESOLVED` result, not `SUPPORTED`. This is a weaker
fail-closed boundary than the author's stated "before C11 release" promise and
should be hardened by validating an exact order key before release
construction, but it is not a false-fact path in this pass.

## Additional finding: omitted row/occurrence plan on a repeated source

`row_occurrence_plan=None` is the S1 scalar path. If a caller omits the plan on
a repeated source (for example, two PIDs each appearing twice), the adapter
treats every physical row as a separate `ROW-nnnn` respondent and can return a
scalar `SUPPORTED` fact over the inflated row count. The adapter cannot infer
the source shape from the selected response rule alone; the author's docstring
states the plan is mandatory for repeated sources, but no shape witness is
enforced. This is a caller-contract boundary, not a false claim under a
governed plan. It should be made explicit in the adapter API (shape declaration
or mandatory plan for any source with a governed respondent variable) before
broader use.

## Defect decisive for this pass

The normalized mapping collision is different: it is inside the governed map
and produces a false `SUPPORTED` fact. See `00_RETURN.md` defect D1/D2 and the
two executable reproducers. The author must repair the same input-normalization
boundary before acceptance.
