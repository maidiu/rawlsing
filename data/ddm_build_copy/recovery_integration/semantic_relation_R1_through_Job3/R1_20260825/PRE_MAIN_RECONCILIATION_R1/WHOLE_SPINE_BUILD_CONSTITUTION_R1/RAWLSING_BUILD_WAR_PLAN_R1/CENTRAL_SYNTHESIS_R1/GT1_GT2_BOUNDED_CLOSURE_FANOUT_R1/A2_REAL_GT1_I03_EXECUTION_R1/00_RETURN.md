# GT12 Closure A2 — real GT1 I03 execution + deterministic replay R1 — return

## Terminal

`PASS__REAL_GT1_SUPPORTED_19210__DETERMINISTIC_REPLAY`

Repository: `maidiu/rawlsing`

Branch:

`agent/rabochii-gt12-closure-a2-real-gt1-r1`

Exact starting HEAD:

`2753d1abbcb702e9260f4ab60c528748fb28c7d2`

Execution-code tip before this return receipt:

`0674b6bc599d80a6f4fd33f60bb8f1a78c105cbc`

This worker consumed A1 only from exact starting ancestry plus the recreated governed Library artifacts. It did not consume A3, Closure B/C/D, or any sibling closure branch.

## Governing refs

- bounded Closure-A program: `a473091473f5729dd9aa6e54d68b88de49f9d608`
- frozen GT1/GT2 canary contract: `a9416094cbb4653dd2de2e4aa7b67577a355560c`
- A1 terminal:
  `PASS__GT12_A1_REAL_19210_C11_BUILD_SCALE_CLOSED`

## Governed Library inputs

Persistent Library tree used:

`/Rawlsing/FIELD_FORGE_R2/`

Exact recreated governed artifacts consumed:

- `FFP014_R5_CURRENT_RESPONDENT_ADMISSION_Q73A_R1/carrier-00000.tsv.gz`
- `FFP017_FIRST_GENUINE_CANARY_COEXPOSURE_RISKSET_R1/core_claim_common_risk_set.tsv.gz`
- `FFP017_FIRST_GENUINE_CANARY_COEXPOSURE_RISKSET_R1/deterministic_replay_receipt.json`
- `FFP017_FIRST_GENUINE_CANARY_COEXPOSURE_RISKSET_R1/selected_response_facts.tsv.gz`
- `FFP017_FIRST_GENUINE_CANARY_COEXPOSURE_RISKSET_R1/selected_exposure_facts.tsv.gz`

No governed carrier/source bytes were committed to Git.

## A1 exact C11 boundary re-resolved

A1 exact release:

- kind: `C11LogicalRelease`
- object id: `R5_GT12_Q86A_Q86B_FROZEN`
- content hash: `8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295`
- replay manifest hash: `c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa`
- public objects: `96,057`
- internal records: `19,212`
- exact claim members: `19,210`
- source rows preserved: `51,587`

Exact empirical universe ref:

- kind: `EmpiricalUniverse@1.0.0`
- object id:
  `urn:rawlsing:pre553:EmpiricalUniverse:sha256:4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1`
- content hash:
  `4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1`

## GT1 exact claim

Claim:

`GT1_R5_Q86A_RAW_UNARY_EXACT_RISK_SET@1`

Target:

`Q86A`

Question implementation:

`question_impl.phase0.67f036c0efb7fb98ff4a`

Risk set:

`FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`

Measure:

`RAW`

Weights:

`NOT_APPLICABLE`

Target-use ceiling:

`GT1_POSITIVE_EMPIRICAL_FACT_ONLY__NO_STRUCTURAL_OR_ACTOR_PROMOTION`

## Claim-specific authority closure

The inherited C11 authority snapshots were retained for source/routing/carrier semantics.

Because the positive I03 authorities must be scoped to the actual post-A1 empirical universe, A2 constructed only the bounded claim-specific execution authorities after the exact universe ref was known.

### PREDICATE_GRAMMAR

- authority id:
  `GT12-A2-R5-Q86A-I03-PREDICATE-GRAMMAR`
- version: `1.0.0`
- content hash:
  `cb690360c6b5a2b091310fad5d1cda1ea843c505959ffe2ee8613eafe22089dc`

### TARGET_USE_PERMISSION

- authority id:
  `GT12-A2-R5-Q86A-GT1-TARGET-USE`
- version: `1.0.0`
- content hash:
  `a4f1195a0736224ac5751a43c714e5a79ecb845fe436551cd0511a7e11d1719f`

The target-use permission is carried in the exact query/fact authority closure as a distinct `TARGET_USE_PERMISSION` authority; it is not reinterpreted as predicate grammar.

## Exact GT1 query

Predicate ref:

- kind: `EmpiricalPredicate@1.0.0`
- content hash:
  `03c63b3ad74e14586a97c39f3ec2ccac5aa75230b3cb63e5c66f9035d09086ae`

Query ref:

- kind: `EmpiricalQuerySpec@1.0.0`
- object id:
  `urn:rawlsing:pre553:EmpiricalQuerySpec:sha256:aeac560d90bd504ce488d63227f812ff2f8613d8a0570a0b6cdcae0b72658aba`
- content hash:
  `aeac560d90bd504ce488d63227f812ff2f8613d8a0570a0b6cdcae0b72658aba`

The query is exactly single-universe, raw, unweighted, Q86A unary, and exact-risk-set scoped.

## Genuine current-I03 result

Result state:

`SUPPORTED`

Exact denominator:

`19,210`

Raw resolved target support:

`19,210`

Exactly one positive producer-owned `EmpiricalFact` was produced.

Fact ref:

- kind: `EmpiricalFact@1.0.0`
- object id:
  `urn:rawlsing:pre553:EmpiricalFact:sha256:6fbd00cc6d0086f686a310857647f0aa0e6076d0be5a46ed3d2a8fe13a0a8baf`
- content hash:
  `6fbd00cc6d0086f686a310857647f0aa0e6076d0be5a46ed3d2a8fe13a0a8baf`

Exact fact authority closure includes:

- `GT12-A-R5-Q86-CARRIER-REEXPRESSION@1.0.0`
  hash `a62630cdc2c81161bcce4c3be7f3757bb4a7e279c9cb334e0b9b013d7339a435`
- `GT12-A-R5-Q86-COMMON-RISK-ROUTING@1.0.0`
  hash `943fa2c44710480948f1dc7a5ae2fe512b806462776e89dcd6de761c5c956d0a`
- `GT12-A-R5-Q86-SOURCE-SEMANTICS@1.0.0`
  hash `c89c04fcaeb0742e5c6248f526082f90156af78f978f44023ab75eef53e830a4`
- A2 `PREDICATE_GRAMMAR`
  hash `cb690360c6b5a2b091310fad5d1cda1ea843c505959ffe2ee8613eafe22089dc`
- A2 `TARGET_USE_PERMISSION`
  hash `a4f1195a0736224ac5751a43c714e5a79ecb845fe436551cd0511a7e11d1719f`

## Exact raw support cells

| Q86A source-native state | cell state | raw support |
| --- | --- | ---: |
| `0` | `OBSERVED_POSITIVE` | 2,643 |
| `1` | `OBSERVED_POSITIVE` | 15,984 |
| `DK` | `OBSERVED_POSITIVE` | 575 |
| `MISSING` | `OBSERVED_POSITIVE` | 8 |
| `NOT_ASKED` | `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET` | 0 |
| `REFUSAL` | `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET` | 0 |

Exact sum:

`2,643 + 15,984 + 575 + 8 + 0 + 0 = 19,210`

Administrative typed states were preserved explicitly. Zero-support administrative states were not dropped or collapsed.

## Deterministic replay

Replay equality:

`TRUE`

Replay ref:

- kind: `PRE553_I03_QUERY_REPLAY`
- object id:
  `urn:rawlsing:pre553:i03-query-replay:sha256:809b661c33637ca1b19c5225e7d95df2dd4a759e7ac09d10d6d8ee50e9c533d0`
- content hash:
  `809b661c33637ca1b19c5225e7d95df2dd4a759e7ac09d10d6d8ee50e9c533d0`

Replay reproduced the original current-I03 result exactly, including query identity, denominator, support cells, authority closure, and final fact identity.

## Genuine-scale engineering defects reproduced and repaired

### 1. GT12-B exact release/member validation memory cliff

The inherited adapter independently materialized duplicate routing/event maps over the same 19,210-member release.

Repair:

- one compact exact pass over immutable respondent/routing/event ref keys;
- exact Q86A/Q86B routing equality retained;
- unresolved routing remains fail-closed;
- exact per-target scalar event uniqueness retained;
- source-native domain completeness retained.

Observed exact-member validation after repair:

approximately `1.2 s` for all 19,210 members.

### 2. PRE553 DERIVED_BRANCH_COHORT accidental O(n²)

The current predicate evaluator reparsed and canonicalized the exact 19,210-member cohort for each respondent.

Repair:

- verify predicate identity normally;
- compile the exact immutable derived-cohort member refs once per execution;
- perform exact O(1) membership lookup per respondent;
- retain the original predicate AST/ref/hash and replay semantics unchanged.

No predicate semantic identity was changed by this cache.

## Real execution timings

From the final production-helper run:

- governed preparation: `5.037117424 s`
- A1 claim projection: `5.866656059 s`
- A1 C11 candidate: `9.704329639 s`
- A1 C11 validation: `13.155692500 s`
- A2 context/claim-specific authorities: `0.220914933 s`
- GT1 plan: `1.633557370 s`
- current-I03 execution: `5.476648571 s`
- deterministic replay: `5.188514141 s`

## Focused regression actually executed

Command:

`PYTHONPATH=. pytest -q rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py rawlsing_next/tests/test_wave1_gt12_a2_real_gt1.py rawlsing_next/tests/test_wave1_r5_q86_c11_projection.py rawlsing_next/tests/test_pre553_source_backed_c11_facade.py`

Final result after banking corrections:

`54 passed in 0.66s`

Coverage includes inherited PRE553 I03/query/replay behavior, GT12-B positive-fact adapter, A2 exact A1-release/hash failure, claim-scoped authority binding at the actual empirical universe, target-use authority preservation into the positive fact, A1 C11 release integrity, source/risk/carrier tamper, ordering invariance, typed administrative states, and source-backed C11 hostiles.

## Files changed from exact A2 start

- `rawlsing_next/_pre553_query_eval.py`
- `rawlsing_next/_pre553_query_predicate.py`
- `rawlsing_next/wave1_gt12_i03_positive_facts.py`
- `rawlsing_next/wave1_gt12_a2_real_gt1.py`
- `rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py`
- `rawlsing_next/tests/test_wave1_gt12_a2_real_gt1.py`
- this return receipt

No governed data, temporary pickle/carrier, GitHub Actions/export scaffold, GT2 output, FIELD FORGE/PRE-V3/M1 object, actor/V3/V2 promotion, Closure B/C/D output, PRE-MAIN movement, or `main` movement is present.

## Terminal

`PASS__REAL_GT1_SUPPORTED_19210__DETERMINISTIC_REPLAY`
