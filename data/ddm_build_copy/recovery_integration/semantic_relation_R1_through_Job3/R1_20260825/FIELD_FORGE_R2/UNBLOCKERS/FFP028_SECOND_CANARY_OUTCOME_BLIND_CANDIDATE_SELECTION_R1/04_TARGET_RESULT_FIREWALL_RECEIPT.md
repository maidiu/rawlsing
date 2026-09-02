# FFP028 — TARGET-RESULT FIREWALL RECEIPT R1

Status: `PASS__TARGET_RESULTS_UNINSPECTED`

## Exact permitted source bytes

1. FFP017 `selected_response_facts.tsv.gz`
   - banked SHA-256: `98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709`
   - rematerialized SHA-256: `98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709`
   - use: exact source/project state identities and outcome-blind counts only.

2. FFP017 `core_claim_common_risk_set.tsv.gz`
   - banked SHA-256: `c5281c564c1cafdcbe6769013b46834bc4da9bb481e56a172a581fee745cb8dc`
   - rematerialized SHA-256: `c5281c564c1cafdcbe6769013b46834bc4da9bb481e56a172a581fee745cb8dc`
   - use: exact 19,210-member governed denominator only.

## Exact computation firewall

### Structural support computation

Columns/variables consumed:

- respondent identity;
- `Q70B`;
- `Q70C`;
- `Q73A`;
- `Q84`.

Operation:

`GROUP BY exact Z state identities, Q73A native state identity -> COUNT respondents`

No destination variable was present in the grouping frame.

### Global destination nondegeneracy computation

Variable consumed:

- `Q86A`.

Operation:

`GROUP BY Q86A exact native state identity -> COUNT respondents over complete R`

No `C` or `Z` variable was present in the destination-domain grouping frame.

Observed global-only state counts:

- state `0`: `2643`;
- state `1`: `15984`;
- state `9`: `575`;
- state `-1`: `8`.

These counts establish only global native-domain nondegeneracy. They do not establish a broad contrast, within-state contrast, effect direction, or support under any `C` or `Z` condition.

## Forbidden joins not executed

- `Q86A × Q73A`: NOT COMPUTED.
- `Q86A × Q73A × Q70B`: NOT COMPUTED.
- `Q86A × Q73A × Q70C`: NOT COMPUTED.
- `Q86A × Q73A × Q84`: NOT COMPUTED.
- `Q86A × Q73A × any Z tuple`: NOT COMPUTED.
- any destination-conditioned candidate ranking: NOT COMPUTED.
- any representation output: NOT REQUESTED / NOT COMPUTED.

## Candidate ranking inputs

Only:

1. hard FFIF009 structural floor;
2. already-established current authority/evidence completeness;
3. native/no-TTAR operation;
4. count of exact `Z` predicates with positive membership in both `Q73A` arms;
5. exact per-predicate `min(n_Q73A=0, n_Q73A=1)` counts as engineering evidence only;
6. structural fixture/holdout feasibility;
7. exact lexical identity.

No materiality or support threshold was introduced.

## Derived receipt hashes

- `00_RETURN.md`: `d5b7b1ae9a4b0882fe1e0ddadcd3f957d6c4dedc03a73e0a2f98c0d826810f30`
- `01_FROZEN_CANDIDATE_ORDER.tsv`: `4777ec6a60305191e5923581775720c2bdc56d6695c08d3bf7fc23c9acf5e46a`
- `02_CXZ_SUPPORT_COUNTS_WITHOUT_D_COMPACT.tsv.xz`: `74469cc180c0bc761e702e92a295219f5d8398403af4021cb5de4475a8a6111a`
- uncompressed compact exact-state-ref TSV semantic-byte SHA-256: `645de06ed0a127c45eb75a0fc26cb979ea494f0d338d2fde899c5b5b584882f8`
- `03_SF001_SF018_EVALUATION.tsv`: `5439a1ab863521a935d4bc96cbf020f2c48ca18b89a3f0e82cc5e5942b66c14c`

## Selection ceiling

`STRUCTURALLY_IDENTIFIABLE__POSITIVE_DENOMINATORS != SUPPORT_ADMISSIBLE`

Every statistical/support decision remains reserved to the later frozen support/uncertainty contract.

`PASS__TARGET_RESULTS_UNINSPECTED`
