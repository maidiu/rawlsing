# PYAT N10E — PROOF / PROVENANCE CORRECTION — NARROW INDEPENDENT REREVIEW R1

Status: COMPLETE__APPROVE_AT_DECLARED_GRAIN__HQ_ADJUDICATION_REQUIRED

Review branch:
`agent/reviewer-pyat-hq145-n10e-proof-provenance-rereview-r1`

Commission tip:
`80eb275f40ffb2d096433c218fecb009063a0bd1`

Correction return rereviewed:
`52e41a41e8bc3b77390016a049095b5aea1721d0`

Prior independent review:
`b89268d1824409d20a91a37a0a3ff7751a7ae75a`

Findings under narrow rereview:
- `REV-N10E-001`
- `REV-N10E-002`
- `REV-N10E-003`

## Disposition

`APPROVE_AT_DECLARED_GRAIN`

The correction closes both blocking findings and correctly repairs the nonblocking provenance wording.

The provider implementation itself is not reopened. No concrete provider counterexample was found.

## REV-N10E-001 — changed-source P6 proof

The prior defect is gone.

The pre-correction court constructed a 60-row `narrowed_rows` list but then called `_provide(case)` again on the unchanged canonical case. Its apparent “changed geometry” proof was therefore vacuous.

The corrected court:

`test_p6_geometry_is_recomputed_not_fixed_when_the_empirical_slice_changes`

now builds two complete cases and invokes the real public provider on both:
- canonical forward case from the 100-row AT07 source law;
- changed forward case from a separately built 110-row source law.

The changed law is exactly the canonical law plus ten new respondents with:
- `POSITION=P1`;
- `ANSWER=no`.

Independent row arithmetic therefore gives:

### Canonical forward
- P1/yes = 54
- P1/no = 6
- forward denominator = 60
- cells = yes 54 / no 6

### Changed forward
- P1/yes = 54
- P1/no = 16
- forward denominator = 70
- cells = yes 54 / no 16
- yes fraction = 54/70 = 27/35
- no fraction = 16/70 = 8/35

The court asserts exactly those values through the provider-produced evidence.

The changed input is real at the provider boundary. `build_provider_case(..., variant=CHANGED_SOURCE_LAW)` builds a new source repository, release, universe, empirical query, predicate, witness, consumer query, model rule, and exact authority registry from the changed rows, and `_provide(changed)` passes those exact changed determinants to `provide_empirical_possibility_slice`.

The court additionally asserts:
- changed source universe != canonical source universe;
- changed release != canonical release;
- source question refs remain the same because the fixture preserves the question namespace;
- conditioner ids remain the same.

This is therefore a changed empirical source law at the same declared source-free semantic grain rather than an unrelated second fixture.

## Producer/composition-derived evidence

The changed result remains on the accepted seam.

The court proves:
- `changed_result.generated_evidence_or_null is changed_result.composition_result.possibility_slice_evidence_or_null`;
- the consumer result is likewise the composition's exact consumer result object;
- the receipt records `generated_evidence_identity_is_producer_derived == True`;
- changed evidence raw support == changed producer fact raw denominator == changed composition raw denominator == 70;
- changed composition producer fact ref == the executed changed producer fact ref.

Identity reidentification is also established:
- changed producer fact ref != canonical producer fact ref;
- changed evidence ref != canonical evidence ref;
- changed provider receipt ref != canonical provider receipt ref.

The provider result identity also reidentifies by construction: `EmpiricalPossibilitySliceProviderResult.result_identity_hash` hashes material containing the provider receipt material, generated evidence ref, and consumer result identity. With receipt/evidence identities changed, the provider result identity preimage changes as well.

No geometry was added to the provider. Provider blob remains exactly:

`23167aa25291fb148b1e3cf210ac33fe7769b783`

before and after correction.

## Reverse-direction control

The reverse control is meaningful.

Reverse conditioning is `ANSWER=yes`. The ten changed rows are all `ANSWER=no`, so the yes cohort remains:
- P1/yes = 54
- P2/yes = 8
- denominator = 62

The corrected court executes both canonical reverse and changed reverse cases and requires:
- changed reverse denominator = 62;
- canonical reverse denominator = 62;
- changed reverse cells = P1 54 / P2 8;
- changed and canonical reverse evidence identities remain distinct because source identity differs despite equal numeric geometry.

This distinguishes a source-law-specific forward geometry change from the trivial proposition that “a second invocation returns something different.”

## Changed-source authority

The authority handling is fail-closed and fixture-local.

The canonical synthetic query authority is explicitly scoped to one exact canonical source universe in its frozen `scope_envelope.source_universe_refs`.

The corrected changed fixture constructs:
`frozen_changed_source_query_authority(universe_ref)`

which:
- starts from the frozen canonical query snapshot;
- preserves its authority kind, governed operations, governed object families, effective-time context, replay root, dependencies, interpretation fingerprint, and other semantic law;
- replaces the exact source-universe scope with a one-element list containing the changed universe;
- gives the changed fixture authority its own fixture authority id;
- recomputes the content hash from that exact changed authority material.

It does not:
- widen the canonical authority;
- use `latest`, `default`, nearest, fuzzy, or universal scope;
- alter provider behavior;
- alter empirical-query owner behavior;
- add a production authority.

The refusal law is independently grounded:
- `require_positive_authority` raises `Pre553AuthorityError("exact authority scope does not include source_universe_refs")` when the required universe is absent;
- `pre553_empirical_query._failure_code` maps `Pre553AuthorityError` to typed `UNAVAILABLE / MISSING_REQUIRED_AUTHORITY`;
- the final 88-test court includes and passes `test_astra002_shared_i03_rejects_allow_authority_excluding_actual_universe`, which asserts `MISSING_REQUIRED_AUTHORITY` for exactly this source-scope class.

The correction packet also records the changed-source development attempt being refused through that exact typed path before the fixture-local changed authority was supplied. No coercion route was introduced.

## REV-N10E-002 — final execution provenance

The final record is internally coherent.

Authoritative command:

`python -m pytest rawlsing_next/tests/test_pre553_analytical_composition.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py rawlsing_next/tests/test_pre553_empirical_possibility_provider.py -v`

Authoritative result:

`88 passed, 0 failed, 0 errors, 0 skipped, 15.14s`

The committed verbose output:
- says `collected 88 items`;
- contains exactly 88 `PASSED` result lines;
- partitions them as 13 + 32 + 13 + 30;
- ends exactly with `88 passed in 15.14s`.

The corrected `00_RETURN.md` and `06_EXECUTION_RECEIPT.json` record the same final count and duration and explicitly mark 20.01s, 19.09s, 22.84s, and 16.44s as superseded historical timings.

The correction packet consistently records one authoritative final court run. This Browser/GitHub rereview did not independently rerun pytest.

Correction ancestry also transfers cleanly:
- correction commission `a7f7eec...`;
- correction return `52e41a41...` is exactly one commit above it;
- rereview commission `80eb275f...` is exactly one commit above the correction return and adds only the rereview commission document.

Thus no executable/test/fixture delta exists between the correction return and the state under rereview.

## REV-N10E-003 — provenance wording

The stale limitation is repaired.

`07_FINAL_DISPOSITION.json` no longer lists commission-tip unavailability as a current limitation.

It instead carries `historical_provenance_note`, explicitly stating:
- the tip was absent during the early local phase;
- early fetch failed for lack of credentials in that sandbox;
- work initially began from the declared accepted base;
- credentials later became available;
- the assigned branch was fetched;
- the issued commission tip was confirmed;
- the lane was rebased onto it;
- the final history is lawful and resolved;
- the early unavailability is provenance history, not a standing blocker.

`00_RETURN.md` likewise labels the branch note “resolved.”

## Scope / preservation

The correction is a lawful descendant of original N10E return `58ba4320...`.

Correction executable/test changes are confined to:
- `rawlsing_next/tests/n10e_empirical_slice_fixture.py`;
- `rawlsing_next/tests/test_pre553_empirical_possibility_provider.py`.

The remaining correction changes are in explicitly allowed N10E proof/return packets.

The prior independent review return directory is untouched.

The reviewed provider blob is byte-identical:
`23167aa25291fb148b1e3cf210ac33fe7769b783`.

Accepted owners are byte-identical:
- analytical composition: `26f3380cb83cbbcedc87c74aaf603b0492c8ce8f`;
- positioned-subject possibility owner: `62e5eced47b64512f47b004e3e13a6ef3fe21de7`.

All 30 provider test names remain; the correction changes only the P6 changed-source court plus a helper signature and its P1/P2 call sites. The helper change removes an unused `case` argument and does not weaken P1/P2.

No accepted provider finding is contradicted:
- provider seam remains the accepted composition path;
- no handwritten-evidence provider bypass;
- P1/P2 intact;
- P3 intact;
- receipt identity intact;
- P5 fail-closed behavior intact;
- P7 replay intact;
- authority ceiling intact.

## Nonblocking documentary notes

Two small wording defects remain in the correction material.

1. `n10e_empirical_slice_fixture.py` comments/docstrings twice say the P1 cohort “stays at 60.” That is false: after adding ten P1/no respondents the P1 conditioning cohort is 70. The executable rows, frozen oracle, test assertions, and exact arithmetic are all correct at 70. This is a comment-only typo and does not affect the proof.

2. `02_EXECUTION_PROVENANCE_RECONCILIATION.json` says “command_strings_identical_across_all_three: true.” The raw pytest output file does not print the shell invocation. It does, however, enumerate exactly the four commissioned files/test nodes and the same 88-test result, while the return and receipt carry the command. This is an overstatement about literal text presence, not a conflicting execution record.

Neither note requires reopening code or tests for this acceptance decision.

## Authority ceiling

No AT33 claim.
No real-source qualification.
No structural-world admission.
No actor/person/V3 state.
No smoothing/proxy authority.
No provider broadening.
No merge or self-adoption.

## HQ disposition

`REV-N10E-001`: CLOSED.

`REV-N10E-002`: CLOSED.

`REV-N10E-003`: CORRECTED.

The N10E proof/provenance correction is approved at the declared source-free AT07/AT17 R1 grain only.

Terminal:

`N10E_PROOF_PROVENANCE_REREVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`
