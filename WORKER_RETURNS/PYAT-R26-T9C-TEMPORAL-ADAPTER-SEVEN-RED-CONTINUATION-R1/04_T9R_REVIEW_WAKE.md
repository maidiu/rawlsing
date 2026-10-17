# 04 — independent T9R review wake (PYAT R26 T9C)

This is a **wake for an independent reviewer**, not a sent HQ instruction, not a
method accession, and not an EE12 issuance.

---

## 1. What to review

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (verify PRIVATE yourself) |
| Branch | `agent/rabochii-pyat-r26-t9c-temporal-adapter-seven-red-repair-r1` |
| Sealed startup | `79cf24ee615ec24bee2dc8584b31fb6b240fd3cf` |
| Candidate under review | the return commit reported in `05_REMOTE_VERIFICATION.json` |
| Original author | `edf3494b1b11cb71a78540aba950aa15da900c8a` |
| Prior independent court | `a2a7bdeda76aa008b3d620b01af71f7fd6efaaae` |
| Reviewer role required | **independent T9R**, not the T9C author, not HQ |

Write only inside your own return directory. Do not modify this return.

---

## 2. What the T9C author claims, and what it does not claim

**Claimed.** That the ten independent failed assertions across seven defect classes
(R1..R7) are repaired at the adapter-contract level, that the original V553
machinery is unmodified and is what actually decides the temporal key, that the 28
author positives and 8 inherited native tests are preserved, and that the AS_OF
versus RETROSPECTIVE clock distinction is still honest.

**Not claimed.** No EE12 source pair. No national inference. No OC05. No N11. No
N12. No V3. No adoption. No N8E/N8S/N9 execution. No actor exposure or
remembered-exposure evidence. No observed temporal calibration. No historical-rights
reconstruction. No authenticated dated archive snapshot. No method accession.

---

## 3. Reproduction

From the return root:

```
python3 -B run_all.py                       # four separate courts, real pytest
python3 -B guarded_runner.py                # frozen independent T9I transport only
python3 -B run_pinned_v553_suite_t9c.py     # inherited original V553 8 tests
python3 -B 02_counterexamples.py            # regenerate side-by-side counterexamples
```

Expected exits: `frozen_t9i_independent_48` **1**, `t9c_own_repair_suite` **0**,
`inherited_original_v553_native_8` **0**, `unchanged_t9b_author_28` **0**.

Top-level reproduction exits 1 because of the one disclosed residual in §4. That is
expected and is not to be read as an unexplained failure.

---

## 4. The one residual you must adjudicate

`test_two_time_original_consumer_and_numerical_products_reproduced` — **fails**.

It compares the repaired consumer output against the original T9B published
two-time artifact. Repairing **R5** requires a `PROBE_ONLY` read to stop presenting
a route as a permission-valid open opportunity; the artifact records
`opportunity_ids = ["ROUTE_DEFERRED_REVIEW"]` for the 1990 `PROBE_ONLY` read.

Exactly one semantic field differs: `1990.opportunity_ids`
(`["ROUTE_DEFERRED_REVIEW"]` → `["ROUTE_BLOCKED_NO_SUPPORT"]`). Everything the
prior independent court endorsed is byte-identical: values 0.20 / 0.60, bands,
`basis_wave_ids`, `uncertainty`, `temporal_key`, `refused_code`, and the whole
`provenance` block. All other differences are additive disclosure fields.

**Your job here is to decide whether R5 was repaired the right way.** The author's
position is that an exploratory estimate must not open an authorized world option,
and therefore the rejected artifact's route list is itself an instance of the defect.
If T9R judges that `opportunity_ids` should have remained the route list and that a
separate flag would have sufficed, that is a real methodological disagreement about
the consumer contract and should be recorded as such — it is not a hidden regression
either way, because the change is frozen, diffed field-by-field, and disclosed in
`00_REAL_REPAIR.md` §5 and `03_NATIVE_JUNIT_AND_IMPORT_LEDGER.md` §5.

---

## 5. Specific things to attack

1. **R1 honesty.** Does calling `_authorize_v553_multi_wave_key` with caller-supplied
   eligibility declarations actually prevent a false native grant, or does it merely
   launder the same assumption through a native function? Check
   `t9c_temporal.native_authorization` and whether the inputs are validated or merely
   forwarded. The author's position is that the caller's declarations are forwarded
   verbatim and recorded, that the *status* is native, and that a single eligible
   anchor can no longer produce `AUTHORIZED`. Check the downgrade rule
   (`_resolved_key`) and the native gap control with `allow_interpolation=True`.
2. **R1 downgrade is one-directional.** Confirm native can only ever downgrade, never
   upgrade, and that `INTERPOLATED_NOT_OBSERVED` cannot be promoted by a two-anchor
   native grant.
3. **R2.** Confirm `NaN`/`None`/`inf`/declared-MISSING never reach `_bounded_score`,
   that observed zero is still a real zero, and that the accepted native
   default-to-0.0 is genuinely untouched.
4. **R3.** Confirm provenance is basis-bound and that a conflicting basis is refused
   rather than narrowed. Ask whether refusal is the right response versus a typed
   multi-source disclosure.
5. **R4.** Confirm `structural_world_fields` really is complete and that the helper
   alone still cannot certify structural constancy in another fixture.
6. **R5.** See §4.
7. **R6.** Confirm the post-rupture result is a *labelled bounded hypothetical* and
   not silently presented as the post-break cohort estimand, and that the accepted
   author positive (`hold across a rupture == 0.30`, `refused_code is None`) survives.
   Ask whether keeping the value with a caveat is acceptable versus refusing outright.
8. **R7.** Confirm `pub_lag_of` is basis-only and `archive_context_wave_ids` is
   genuinely separate lineage and is never presented as product publication basis.
9. **Transport fidelity.** Confirm `frozen_t9i_court/test_independent_clock_custody.py`
   is byte-identical to the independent court's file
   (git blob `f624177d4980f524781c84956eb23a45bfa52a78`) and that the frozen
   `pinned_candidate/evidence/02_real_temporal_to_selected_world_two_times.json`
   matches the independent court's pinned copy.
10. **Custody.** Confirm 22/22 staged native files are byte-identical to repo blobs at
    `79cf24ee`, that the T9B author return is unmodified, that no reviewer assertion
    was touched, and that `guarded_runner.verify` rejects both untrusted paths and
    changed preimages.
11. **Ambient shadowing.** Independently re-run a bare relative invocation and see
    what the ambient `pytest.ini` and ambient `data/ddm_build_copy/` do. The author's
    runs always pass `--rootdir` and `-c` explicitly; that choice should be audited,
    not assumed.
12. **Clock discipline.** Confirm the API still has no independent archival known-at
    upper bound, no effective/discovered-at revocation timestamps, and no
    historical-entitlement versus current-computation grant pair, and that no
    historical publication is being read as historic person knowledge.

---

## 6. Evidence index

| Path | Use |
|---|---|
| `01_SEVEN_DEFECT_CONTRACTS.json` | frozen before execution; expected outputs and defect contracts |
| `02_ACTUAL_ORIGINAL_V553_AND_CONSUMER.json` | native controls + side-by-side counterexamples + corrected consumer outputs |
| `evidence/03_T9I_RED_TO_GREEN_CROSSWALK.json` | per-case crosswalk against the independent court's own JUnit |
| `evidence/t9c_native_import_ledger.json` | 22-file ledger with repo blob identity |
| `evidence/t9c_frozen_t9i_module_receipts.json` | 16 loaded project module `__file__` receipts |
| `evidence/independent_observations.json` | raw observations written by the frozen independent transport |
| `evidence/t9c_four_court_execution.json` | four-court assembly with JUnit hashes |
| `junit/*.xml`, `logs/*.log` | complete JUnit and full stdout/stderr |
| `environment_passport.json` | interpreter, libraries, import custody, clock caveat |
| `05_REMOTE_VERIFICATION.json` | publication receipt and exact remote SHA |

---

## 7. Authority boundary

This return repairs an **adapted contract** and publishes its evidence. It does not
grant method acceptance. **Independent T9R review is required before HQ method
accession.** No source issuance, no EE12, no adoption, and no N8E/N8S/N9 execution is
performed or requested here.
