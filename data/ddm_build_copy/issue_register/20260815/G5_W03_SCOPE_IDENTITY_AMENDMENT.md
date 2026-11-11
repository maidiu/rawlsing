# Rawlsing V550–V552J Repair — G5 W03 Scope-Identity Amendment

This is a **narrow SRC-001 integration amendment** discovered by Vozhd after the G4 final worker wave. It does not reopen the issue register, transfer ownership of SRC-001, or authorize semantic redesign. SRC-001 remains Vozhd-owned. W03 is authorized only to implement and test the minimum V551J producer-scope hook described here.

Work on branch:
`agent/v550-v552j-w03-final-scope-identity`

Target a draft PR to:
`agent/v550-v552j-repair-integration`

## Proven integration defect

For a governed **single-country shard**, the two sides of the V552J join currently publish different exact scope identities even though they originate from the same inherited run:

- V550 bridge rows carry both `country_code` and `shard_id`.
- V551 preserves both; V552 inherits that exact V551 scope.
- V550J intentionally publishes shard scope with `country_code=""`, `country_codes=[...]`, and `shard_id=<shard>`.
- V551J `_expected_v551_scope()` currently preserves the V550J blank `country_code` whenever `shard_id` exists, even when the verified V550J frame/manifest scope contains exactly one country in `country_codes`.
- Therefore a single-country V551J producer can publish `country_code=""` + shard while its sibling V552 producer publishes `country_code=<the known singleton>` + the same shard.
- V552J correctly fails closed on this disagreement. Do **not** weaken or special-case V552J exact-scope matching.

## Required amendment

In W03-owned V551J producer code, preserve the already-verified singleton country identity:

- when the resolved/verified V550J scope has exactly one `country_codes` value, V551J's expected/published scope must set `country_code` to that singleton **even when `shard_id` is also present**;
- retain the exact `shard_id` and `scope_kind="shard"` so shard lineage is not lost;
- when the governed V550J shard spans multiple countries, `country_code` must remain blank and the scope remains shard-only;
- do not infer a country from names, IDs, registry similarity, or semantic matching; use only the V550J producer/frame scope that W03 already verifies;
- preserve all existing run/source/wave/shard and `country_codes` equality checks and all artifact hash/version/typed-state verification;
- preserve W03-A registry/publishability/threshold behavior and all W03-B V551J semantics.

## Write domain

Authorized production file:
- `data/ddm_build_copy/compile_v551j_joint_evidence_packets.py`

Authorized tests:
- W03-namespaced regression/integration tests only.

Do not edit V550J semantics, V551, V552, V552J, W05, Section85, downstream V553+, or issue-register governance.

## Required regression coverage

At minimum prove:

1. single-country V550J shard with producer `country_code=""`, verified `country_codes=["IS"]`, and a shard ID resolves V551J expected scope to `country_code="IS"` while retaining the same shard ID and `scope_kind="shard"`;
2. a multi-country shard retains blank `country_code` and exact shard identity;
3. V551J still rejects disagreement between producer `country_codes` and observed frame countries;
4. the single-country V551J scope now agrees with an otherwise-identical V552 scope at the existing V552J exact-scope join boundary; do this as a test only—do not modify V552J;
5. wrong-country, wrong-shard, wrong-run, and multi-country-to-country coercion remain fail-closed;
6. existing W03 V551J producer-boundary regressions continue to pass or, if full execution is unavailable, run the strongest focused executable set and report the limitation precisely.

## Return contract

Commit and push to the assigned branch and open a draft PR against the integration branch.

Return the normal WORKER_PLAN machine-readable fields. Because SRC-001 remains Vozhd-owned, use `primary_issue_ids: []` and include an explicit `assisted_integration_issue: "SRC-001"` field plus the exact before/after scope behavior and tests. Do not claim terminal resolution of SRC-001; Vozhd will adjudicate and close it after integration reconciliation.
