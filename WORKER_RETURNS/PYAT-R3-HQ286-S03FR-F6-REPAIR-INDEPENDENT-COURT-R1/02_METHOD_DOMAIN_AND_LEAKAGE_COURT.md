# S03FR — exact source-free F6 domain/leakage scientific court

## 1. Categorical completeness

Frozen S03F module \`rawlsing_next/pre553_heterogeneous_synthesis.py\` blob \`b1b05e7d60f92357fb31cbea99e5b432415cc7b0\`, lines ~63–128:

For each source stratum, its cells are projected into native category tuples. Code checks:
- tuple arity equals number of axes, no duplicate tuples (\`categories in seen\`);
- each category is in that axis's declared \`category_map\`;
- raw \`n\` exact integer >=0 and weighted mass valid, unweighted mass==n, raw/weighted zero aligned;
- \`sum(n)+excluded_n==eligible_n\` and table claims \`EXHAUSTIVE_DECLARED_JOINT_RISK_SET\`;
- **new** \`len(seen)==Π(len(axis.category_map))\`.

**Proof within claimed domain:** Each distinct admitted tuple belongs to \`D=×_i keys(category_map_i)\`. There can be at most |D| admitted tuples. If there are exactly |D| distinct members, their set is D, including all cells where \`n=0\` but the cell must be explicitly present. The scoped S03R adversary removing cell 4 while redistributing support yields |seen|=3, |D|=4 and \`SynthesisError\`. The same is true if removed cell itself has zero \`n\`. **STATIC PASS** for declared-domain coverage.

**Scientific limitation:** \`D\` is not independently proven to equal original/native questionnaire category domain, because \`category_map\`, \`mapping_ref\`, \`response_semantics_ref\`, \`table_status\` and \`test_origin\` are source input fields. An adversary can author a DIFFERENT reduced synthetic domain and corresponding complete table; this code will consider that *different* domain internally complete. That is not proof that a real source code/category was legitimately absent. Original source-native code states, routing/NOT_ASKED and missingness require a competent original-source owner and exact risk/query/permission. No accepted code to parse a separately issued sparse-zero compression proof is in S03F; all declared native tuples must be explicitly enumerated. **HOLD** for original-domain completeness, source co-consumption.

There is also no automatic scientific proof that two distinct native category codes that map to one common semantic category are legitimately equivalent: \`_mapped\` sums mapped cells and records mapping hashes/review labels; mapping correspondence remains a separate Atlas/source issuer task. Full native table does not prove valid cross-source construct equivalence.

## 2. Descriptive vs predictive outcome leakage

S03F \`conditional\` lines ~340–385:
- verifies local bundle replay hash; requires modeled candidate and compatible topology;
- filters exact joint rows by AND of declared conditions, sums modeled joint probability mass, constructs target distribution;
- sets \`self_conditioning=outcome in conditions\`;
- positive support self-conditioning -> \`state=DESCRIPTIVE_SELF_CONDITIONING\`, \`self_conditioning_status=OUTCOME_LEAKAGE_TAUTOLOGY\`;
- zero support self-conditioning -> \`ZERO_MODEL_SUPPORT\` and same warning; ordinary non-self -> \`SUPPORTED_MODEL\` or \`ZERO_MODEL_SUPPORT\`;
- marks \`evidence_mode=INFERRED\`, \`observed_denominator=None\`, \`uncertainty=CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED\`.

If the condition directly fixes \`employment_position=formal\`, then \`P(employment_position=formal | employment_position=formal)=1\` is tautologically correct but cannot predict the outcome. **STATIC PASS** for marking this distinction. This is not a proof against proxy leakage through different axes, unqualified mappings, or external downstream service ignoring \`state\`. Prediction claims remain forbidden absent independent consumer and scientific admission. \`values_read_hash\` self-authenticates the modeled distribution, not measured person-level evidence.

## 3. Source-indexed, standardization, sparse minority, uncertainty

S03F \`synthesize\`:
- always retains source-indexed \`baseline\` native copy, input hash, optional mapped joint, mapping refusals and source-parent refs before candidate attempted;
- exact source scope/time/unit, mapping fingerprint, source pair overlap labels and joint topology control candidate;
- target shares 4/5 majority, 1/5 minority mix intact within each supported stratum, then weighted source mixture; does not join respondents across source families;
- if minority target 1/5 has no support, \`uncovered_target_mass=1/5\`, \`distribution=None\`, \`covered_subprobability\` totals 4/5; no invented renormalized 1;
- \`minimum_raw_support\` is source-stratum, *not necessarily per-cell*, so a rare supported category can have zero raw count and remain in model domain; original missing/zero states must not be collapsed;
- candidate \`sample_size=None\`, sampling covariance not inferred; if design variance missing \`sampling_variance=None\`, \`sampling_status=UNKNOWN_DESIGN\`; even with diagonal source variance the conditional uncertainty is not identified and bias sensitivity envelopes are not confidence intervals.

**PASS synthetic bounded properties** as static reasoning, **HOLD** real estimand/design, variance transport, independent sample overlap, original source/effective permission and target-world consumer.
