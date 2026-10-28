# SRC04 C/D native boundary review — REVISE

## Identity and custody

- Reviewer role: distinct C/D native-boundary reviewer, not C or D author.
- Branch: `agent/pyat-src04-cd-native-review-20261028`
- Startup/checkout HEAD: `36f0addf281c3e9ad94b44f4e69a51d2441ef3a7`
- Pinned C candidate: `44aaf2be06e026547e9b32d880ac588e84acc9e4`
- Pinned D consumer: `35bab35be55c80f90d9d0cfbc13fb6f555a0f8ce`
- C observed-response, C workload, and D consumer files at this HEAD are byte-identical to the pinned candidates.
- Only `campaign_src04_completion/empirical/review/**` was written by this review. No C/D author file was edited.

## Verdict

**REVISE** — the C work is executable and the actual C-observed fact reaches D's real discovery path, but D drops the observed-response status, contract provenance, and ledger required by the C/D adoption boundary. A downstream consumer cannot tell this fact from an ordinary eligible-risk fact. That is a falsifiable failure of the stated D preservation requirement.

No SRC04 original source was read, stat'ed, hashed, opened, decoded, or issued. The evidence is labelled NONRESPONDENT fixture only and is not source-local qualification.

## Independently measured positive boundary

The review-owned test command is:

```sh
PYTHONPATH=. python3 -m pytest campaign_src04_completion/empirical/review/test_cd_boundary_review.py -q -o addopts=''
```

Result: **8 passed** (exit 0), including the explicit defect discriminator named
`test_d_joined_path_is_positive_but_currently_omits_observed_ledger_DEFECT`.

Actual C fixture results (8 rows, SRC04 NONRESPONDENT fixture only):

- 44 operations built and executed: 3 unary, 3 same-respondent joint, 38 value/state conditional.
- Conditional instances carry exact condition value/state refs and real query/predicate objects; no formula-only placeholders.
- Resume after the first operation executes 43 operations and does not re-execute the prefix.
- 1 higher-order triple is explicitly requested-not-authorized; no triple is built.
- `ser` is absent from analytical targets.
- Unary observed ledger: 8 scoped respondents, 7 target observed, 1 target unobserved, denominator 7, `PER_TARGET_OBSERVED`, `not_eligible_population_estimate=true`.
- Co-observed joint ledger: denominator 6, 6 target observed, 2 target unobserved, `CO_OBSERVED_TARGETS`, not eligible population.
- Conditional ledger: denominator 1, `condition_unobserved=1`, `condition_false=5`, `ALL_REFERENCED_RESPONSE_VARIABLES_OBSERVED`, not eligible population.
- Observed profiles did not call eligible-risk `_risk_membership`; unresolved routing in the existing eligible-risk path still refuses.
- Fixture-only authority cannot be promoted to `ORIGINAL_SCIENTIFIC`; wrong release, source artifact, and operation authority refuse before positive execution.

Actual joined C → D result:

- D executed the C-observed fact through the existing query/replay owner and a real `execute_exact_bounded_discovery` recipient.
- Product status: `FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE`.
- Downstream effect: `SUBSTANTIVE_DISCOVERY_RESULT_SUPPORTED`, one supported candidate.
- D base fact: `1754358a977d6112e2acddec188e65ac9ed8ec2a88cbb06ca2462c7ad47f149a`.
- C fact observed contract: `c2c8caa48b95e1833350ea5845943631cb37c39153ec987b743e3e27c8e0df26`; status `OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION`; ledger present.
- A review-owned in-memory q236 fixture mutation (95.0 → 1.0) changed the D fact and discovery fact refs; restoring the original fixture reproduced the original refs exactly. No source file was written.

## Falsifiable failure

D's real output omits the C observed projection:

- `campaign_src04_completion/consumers/consumer.py:371-380` emits discovery facts with only `fact_ref`, `typed_state`, raw supports, and cells; it drops `target_topology["observed_response"]`.
- `campaign_src04_completion/consumers/consumer.py:628-659` returns the product without `observed_response`, `observed_ledger`, observed contract ref, status, or `not_eligible_population_estimate`.
- `consume_native_producer` (`consumer.py:489-589`) accepts and consumes the observed fact but never captures or validates its observed-response projection.

Measured result: the D product has **zero** top-level fields containing `observ`; its discovery facts have **zero** observed fields; the C fact had status `OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION`, `not_eligible_population_estimate=true`, contract ref `c2c8...`, and a full ledger. This is not a policy-only result: a real value-consuming discovery ran and returned a supported fact.

## Minimal owner repair

Owner: **D** — `campaign_src04_completion/consumers/consumer.py`.

Smallest required repair:

1. In `consume_native_producer`, after resolving the exact fact, capture
   `fact.target_topology["observed_response"]` when the query grain names an
   `observed_response_contract_ref`.
2. Require the projection to be an exact mapping with
   `status == "OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION"`,
   `not_eligible_population_estimate is True`, the exact
   `contract_ref` matching the query grain, and the full `ledger`.
3. Emit that projection on the product as `observed_response` (using the
   existing `_plain` conversion). Do not relabel it as eligible or population
   data and do not synthesize a new authority or ledger.
4. In `_run_downstream_discovery`, include each `fact.target_topology` observed
   projection in `empirical_facts` (and retain the observed contract ref for
   provenance). The same preservation is required for both the base fact and
   discovery facts.
5. Add one focused joined-path regression asserting equality to the C fact's
   status, contract ref, `not_eligible_population_estimate`, and ledger.

No C repair is required by this review. No new query engine, population weight, structural admission, or source authority is needed.

## Negative and authority evidence

- Wrong source SHA → `NATIVE_SOURCE_IDENTITY_MISMATCH`.
- Wrong release → `WRONG_RELEASE_IDENTITY`.
- Wrong fact → `FACT_SET_MISMATCH`.
- Missing native/policy authority → `MISSING_AUTHORITY`.
- C fixture promotion to original scientific grade → `Pre553AuthorityError` (fixture-only refusal).
- C query replay with the exact expected fact ref succeeded.
- Observed `_risk_membership` bypass proven; unresolved routing remains a refusal in the eligible-risk path.

## Limits

- All measured values are from the repository's labelled SRC04 nonrespondent fixture. They are engineering evidence only, not original SRC04 qualification and not a source-local claim.
- D's joined positive result is real but incomplete for adoption because observed provenance is absent; therefore this review does **not** issue `PASS_SCOPED`.
- The review did not assess original-source construction, original C11 qualification, q217/q715/q716 observed domains, or any population/structural adoption.
- No new worker, model, provider, CI/prod/actor, N11/N12/Sorok, or J52/W52 surface was used.
