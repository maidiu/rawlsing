# C1 independent commands and evidence

All commands run from `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-independent-review`.
Writes only under `C1_INDEPENDENT_REVIEW/`; source/read-only metadata only.

## 1. Q86 direct sourcefree tests (smallest semantic suite; 97-test suite not repeated)

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B -m pytest -q -p no:cacheprovider \
  --basetemp=.../C1_INDEPENDENT_REVIEW/probes/pytest-q86 \
  rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py
```

Result: exit 0, **8 passed in 0.36s**. These are the synthetic sourcefree Q86 tests;
they prove first-reader mechanics, not selected AR-0033 authority. Log:
`logs/q86_direct_tests.log`.

## 2. Independent metadata/source/callgraph probe

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  .../C1_INDEPENDENT_REVIEW/probes/independent_checks.py
```

Result: exit 0; full output `logs/independent_checks.log`. It verifies:

- CSV: 15,498,257 bytes, SHA-256 `305cb215485bc95ebecee395e578c52739311bc2fc15faed27318bd922f47332`.
- Q86A/Q86B: 6 rows each, `context_only`, `recommended_computation=none`,
  `ordinal_context`, substantive `0/1`, specials `-1/9/997/998`, contract hashes
  `198f189a...` / `01ceeb78...`; statuses `curated_packet` for substantive rows and
  `curated_special` for specials.
- No literal Q86 contract hashes in `rawlsing_next/`.
- Non-test call-site scan: `execute_and_replay_a2_gt1` only in its defining non-test
  module; no non-test caller. `build_gt1_q86a_i03_plan` in defining module and
  `wave1_gt12_a2_real_gt1` (test-imported). `produce_exact_conditional_support_profile`
  only in the FF producer and `gt12_c_to_d_relation_bridge`; no non-test Q86 joint
  caller. `build_r5_q86_c11_projection` only in its defining module.
- Source semantics authority `GT12-A-R5-Q86-SOURCE-SEMANTICS` exists at
  `wave1_r5_q86_c11_projection.py:334`, operation
  `R5_Q86A_Q86B_NATIVE_RESPONSE_SEMANTICS`, code-created from frozen source/codebook/
  QIMPL/domain/currentness material.
- R4 ledger AR-0033 row (immutable Git `0c5b385...`):
  `HISTORICAL_VERSION_SELECTED`, `ASSET_BYTES_VERIFIED`,
  `f3b_issuer_grade=A02_RECORDED_HISTORICAL_DECISION_NOT_ORIGINAL_SIGNER`,
  `current_vs_historical=HISTORICAL_ONLY__CURRENT_PROTECTED_PATH_ABSENT`,
  `current_native_status=CURRENT_NATIVE_ISSUER_NEEDED__CURRENT_NATIVE_NOT_RUN`,
  `restoration_disposition=RESTORABLE_AS_HISTORICAL_PRODUCER_INPUT`,
  `f3a_class_or_status=ISSUER-HOLD-AR-0033`, note:
  “Do not reload the packet as a per-query runtime authority; it is the certified
  producer input.”

## 3. C1 evidence inspected read-only

- `C1_SOURCE_CONSUMER/00_RETURN.md`
- `01_CASES.jsonl`, `02_CASES.tsv`
- `03_TEST_RECEIPTS.md` (97-suite and 8-test logs; not rerun)
- `04_MINIMAL_OWNER_ACTIONS.tsv`
- `05_REGISTER_ANTIJOIN.tsv` (212 rows: 17 matched / 195 unmatched)
- `probes/q86_source_semantics_probe.py/.json`
- `probes/q86_negative_probe.py/.json`
- `logs/97_suite.log`, `logs/q86_i03_tests.log`, `logs/q86_negative_probe.log`

## 4. Findings

- **Supported:** CSV identity/hash; Q86 row semantics; A02 issuer grade; current Q86
  source SHA/QIMPL/risk/target-use guards; 8/8 sourcefree Q86 tests; absence of literal
  selected contract hashes; sourcefree negative/restoration; actual selected-row
  version/shadow/withdrawal/cold restore NOT_RUN; generic T01 kept separate; 212-row
  anti-join preserved.
- **Overstated:** “actual present/current operation” as current non-test demand;
  “existing FF consumer” as non-test consumer; “no competent current equivalent”;
  bind-or-retire AR-0033 as the minimum action.
- **Correction:** call Q86 a sourcefree canary/candidate with no proved non-test first
  consumer; source-semantic owner decides whether `context_only` rows require any
  raw-count response semantics; assess the current code-created
  `GT12-A-R5-Q86-SOURCE-SEMANTICS` authority/source-native domain as a possible
  adequate equivalent; do not require historical packet reinstatement; only then
  bind/no-build/retire; add actual selected-row positive plus wrong-version/source/
  wave/shadow/withdrawal/cold-restore tests when a legal selected fixture exists.
- **Verdict preserved:** `FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED` is
  correct. Do not upgrade to proved severance or equivalence; no native/science/full
  #777 claim.
