# PYAT HQ — user-requested universal asked-eligible RAW distribution policy

**Source code base:** current PYAT PR #1173 `b0f45c16e0a9901832e13ea7df4a4cff3a346c78`. Existing REMONT, SOROK and R03 original-issuer source branches unchanged. Protected PRE-MAIN `5d387a9a8c72c68e6ef87a671d6d486bfd1fc43e`. This is bounded sourcefree implementation, not a new authority, original I03 receipt, or scientific accreditation.

## User's controlling rule, now implemented as generic native policy

The primary denominator for an ordinary unweighted question is **all respondents explicitly evidenced by native authorized routing as asked/eligible and whose condition is true**, not merely people who gave substantive answers. Recorded `DK`, `REFUSAL`, physically recorded `MISSING`, and `SOURCE_SPECIFIC_SPECIAL` remain disjoint observable outcome types alongside the source's substantive codes. The output gives both `asked_eligible_n` and, separately, `substantive_response_n`, with numerator/denominator pairs for all-asked and substantive-only percentages; never silently changes between denominators. Unknown eligibility is a typed refusal, not eligible or ineligible by guess.

The source/issuer distinguishes:
- **Known never asked, inapplicable, not eligible**: excluded by the existing I03 `RoutingEligibilityFact` law.
- **Asked and source-recorded nonanswer**: included once in denominator AND correct explicitly typed response-state cell.
- **Asked but absent event**: respondent remains within known-true denominator, but the target is `UNRESOLVED`; a missing event cannot be invented as a source-recorded refusal.
- **Unknown administration (`ROUTING_UNKNOWN`)**: no full descriptive fact issued. A narrower recorded-response-only estimand would need an explicitly different title and risk definition, not use the asked-eligible label.
- **Source-coded 97/98/99**: never auto-cast to not clear/DK/refusal. Those labels need a source-specific admitted codebook rule. This source mapping can now be supplied once per `NativeSourceRule` in the existing R56/R03 projection adapter; no per-query recoding or independent estimator.

## Actual changed existing operating code

1. `pre553_asked_eligible_raw_distribution.py`: reusable target component specification/validation, exact typed nonanswer cells, all-asked/substantive-only RAW fact summary and explicit HELD output on partially resolved I03. The summary consumes the EXISTING `EmpiricalFact`; it is not a second evaluator.
2. `pre553_native_workload_binding._query_for_bundle`: the existing governed R03 builder **defaults** to `ASKED_ELIGIBLE_RAW_DISTRIBUTION@1` for eligible RAW operations whose targets are all `SCALAR_SINGULAR`, including conditional/multiple same-risk scalar queries. It still uses original inherited source/operation authority and baseline condition; does not select a source or issue original-wave permission. Other topologies and weighted science remain unchanged, not covertly scalarized. The B49 one-response `EQ` predicate-specific fixture is **not** a whole-question descriptive marginal, so it is not mislabeled.
3. `_pre553_query_common._profile/_parse_target_plan`: native I03 **enforces** the policy whenever claimed. A forged issuer can no longer advertise asked-eligible semantics while omitting nonanswer states/domain cells or running a weighted request under a RAW-only label.
4. `pre553_source_native_preimage_adapter.NativeSourceRule`: adds optional, hash-identified `response_state_by_source_value` mapping for explicitly codebook-admitted source-native numeric responses to `DK/REFUSAL/MISSING/SOURCE_SPECIFIC_SPECIAL`; rejects conflicting aliases, invented state names, or silent 97/98/99 assumptions. When empty, the package hash remains byte-compatible with the existing historical sourcefree package identity.
5. Sourcefree fixtures `test_pre553_empirical_query.py`, `test_universal_source_projection.py` extended backwards-compatibly; no historical negative removed. New `test_pre553_asked_eligible_raw_distribution.py` exercises the actual native I03 evaluator, not a parallel fake count.
6. `run_preff_c0_first_fault_local.sh`: new `R03_ASKED_ELIGIBLE` court, included in `C0_ALL_SMALL`.

## Sourcefree falsifiers written; NOT EXECUTED by this GitHub-only author

- Six confirmed asked/eligible, each substantive (2), DK (1), refusal (1), explicit missing (1), source-specific special (1), and a seventh source event from a respondent explicitly `NOT_ASKED` excluded. Expect raw asked N=6 and separate substantive N=2 with exact shares.
- Additional asked respondent with *no* emitted response event: denominator grows to 7, resolved N stays 6, I03 `UNRESOLVED` rather than counterfeit accepted distribution.
- Unknown routing causes strict typed refusal; 98 without source semantic declaration cannot magically become DK.
- Caller-claimed profile with substantive-only cells is rejected in I03; weighted marker rejects rather than self-issue method rights.
- Multi-target scalar I03 uses same risk and retains `DK/REFUSAL` as typed joint states; impossible scalar/nonanswer domain combinations refused.
- Synthetic DTA source mapping test verifies raw numeric 98/99/97 are substantive absent codebook mapping and separately typed only when the explicit source rule supplies their meaning; package identity changes and conflicting state/alias mappings refuse.

## Honest limits / shortest test

**No sourcefree code/tests executed on new HEAD in this environment**, so no GREEN. No current original SRC16/SRC04 source issuer, GSS busing eligible/routing decision or saved ANVIL catalog adapter is created by a standard counting policy. Original I03 input issuer and source administration are separate; the user explicitly rejects requiring fresh scientific *method development* each time but does not authorize making up who was asked.

Run on a clean checkout at exact final PR HEAD:
```bash
SHA=<CURRENT_PR_HEAD>
EXPECTED_PREFF_C0_HEAD="$SHA" PREFF_COURT=R03_ASKED_ELIGIBLE \
  bash rawlsing_next/tests/run_preff_c0_first_fault_local.sh
```
Fix actual RED on isolated branch, then run `C0_ALL_SMALL` and a distinct nonauthor review. Do not merge into protected PRE-MAIN without paired competent receiving.

**Disposition:** `QUERYER_POLICY_IMPLEMENTED_IN_EXISTING_R03_AND_I03__NONANSWER_SOURCE_CODE_ADAPTER_BUILT__TESTS_AUTHORED_NOT_RUN__ORIGINAL_WAVE_ISSUANCE_HELD__HQ_CURRENTNESS_HOLD`.
