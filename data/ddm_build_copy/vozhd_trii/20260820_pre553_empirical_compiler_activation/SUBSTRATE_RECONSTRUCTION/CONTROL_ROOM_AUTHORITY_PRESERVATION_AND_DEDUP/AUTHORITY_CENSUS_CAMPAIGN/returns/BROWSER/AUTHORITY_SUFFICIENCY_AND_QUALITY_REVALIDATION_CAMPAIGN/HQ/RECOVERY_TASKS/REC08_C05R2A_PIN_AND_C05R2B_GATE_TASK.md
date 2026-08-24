# REC-08 — C05-R2A EXACT-PIN / CURRENT-HQ INTAKE AND C05-R2B GATE

Status: `ISSUED__STAGED_REC08__C05R2A_PIN_AND_INTAKE_FIRST__C05R2B_EXECUTION_NOT_YET_AUTHORIZED`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-authority-revalidation-control`

Control parent before this handoff: `8049ddf3d71f228ca2eeae853a299f04192e4705`

Worker branch:
`agent/vozhd-trii-rec08-c05r2a-intake`

The commit that adds this handoff file is the exact worker starting HEAD. Verify the branch tip against the handoff SHA supplied by HQ before doing any work. No other pre-execution delta is authorized.

## 0. Mission

REC-08 is no longer a search for a missing production `DiscoveryAuthority`.

Prior Chetiri HQ already adopted the binding production discovery profile:

- `C05R1B_PRODUCTION_DISCOVERY_RULE_PROFILE@1.0.0`
- production operation `PRE553_PRODUCTION_EXACT_BOUNDED_AUTONOMOUS_DISCOVERY@1.0.0`
- frozen algorithm `PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0`
- coverage `COMPLETE_FOR_EXACT_DECLARED_FRONTIER`

The live REC-08 mission is staged:

1. recover and pin the exact immutable final HEAD of the historical C05-R2A worker;
2. validate its ancestry, authorized write scope, declared tests and return receipts;
3. produce a current-HQ intake recommendation for C05-R2A;
4. determine the exact remaining real-source/release instance-authority prerequisites for C05-R2B;
5. STOP.

Do NOT execute C05-R2B in this cell.

## 1. Read first

Read, in this order:

1. current HQ correction:
   `.../AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/HQ/HQ_REC02_INTAKE_AND_C05_LINEAGE_RECOVERY_CORRECTION.md`
2. current queue:
   `.../AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/HQ/CHETIRI_RECOVERY_AND_LOCAL_ESCALATION_QUEUE.csv`
3. prior Chetiri HQ adoption/launch authority:
   `.../VOZHD_CHETIRI_COMPILER_PERSISTENCE/36_C05R1B_HQ_ADOPTION_AND_C05R2A_SOURCE_BACKED_C11_FACADE_IMPLEMENTATION_AUTHORITY.md`
4. historical C05-R2A result bundle under:
   `.../VOZHD_CHETIRI_COMPILER_PERSISTENCE/returns/C05R2A/`
5. the C05-R1A/R1B lineage only as necessary to verify adoption ancestry:
   - `34_C05R1_NO_RETURN_AND_C05R1A_HISTORICAL_LINEAGE_SPLIT_AUTHORITY.md`
   - `35_C05R1A_ACCEPTANCE_AND_C05R1B_PRODUCTION_DISCOVERY_RULE_AUTHORITY_DECISION.md`
   - `returns/C05R1A/`
   - `returns/C05R1B/`

Historical worker branch to inspect immutably:
`agent/vozhd-chetiri-c05r2a-source-backed-c11-facade`

Declared C05-R2A start HEAD:
`d16d988ea51e02482e9f6887fa8ecdcde3c7eb66`

Prior HQ-adopted C05-R1B worker HEAD:
`2ddddaa131ff54780fe232fd86a5c6442bec426b`

## 2. Stage A — exact immutable C05-R2A pin

Determine the exact current remote tip SHA of:

`agent/vozhd-chetiri-c05r2a-source-backed-c11-facade`

Then prove:

- merge base with declared start is exactly `d16d988ea51e02482e9f6887fa8ecdcde3c7eb66`;
- branch is descendant-only from that start;
- no later unrelated contamination exists;
- changed files are confined to the authority-36 write jurisdiction:
  - additive `rawlsing_next/` facade implementation;
  - additive PRE553 tests;
  - `returns/C05R2A/` receipts;
- no frozen C11/I03/I05 semantic truth-condition file was mutated;
- no production selector or architecture A/B/C decision was introduced.

Do not infer the final SHA from branch name, mtime, commit date or README text. Return the exact Git commit SHA.

## 3. Stage B — return/test receipt validation

Validate the historical return against authority 36.

At minimum inspect:

- `returns/C05R2A/C05R2A_RESULT.json`
- `SOURCE_BACKED_C11_FACADE_IMPLEMENTATION.md`
- `PHYSICAL_TO_C11_SEMANTIC_PARITY_MATRIX.csv`
- `I03_FACADE_PARITY_RECEIPT.json`
- `HOSTILE_BRIDGE_TEST_RECEIPT.json`
- `AUTHORITY70_CONTRADICTION_DISPOSITION.md`
- `WVS7_INSTANCE_READINESS.md`
- `AUTHORITY_READ_RECEIPT.md`
- `CHANGED_FILES.txt`
- `UNRESOLVED_EVIDENCE.md`
- `rawlsing_next/pre553_source_backed_c11_facade.py`
- `rawlsing_next/tests/test_pre553_source_backed_c11_facade.py`

The historical result currently reports:

`C05R2A_PASS__GENERIC_FACADE_PROVED__NAMED_REAL_SOURCE_INSTANCE_AUTHORITY_PENDING`

Reported evidence includes:

- 10/10 focused hostile/parity tests passed;
- 5/5 supplemental frozen-I03 probes passed;
- exact logical-oracle vs source-backed-release parity;
- exact native vs replay-equivalent transport parity;
- exact frozen-I03 empirical-fact identity/content-hash parity;
- risk/denominator/target replay parity;
- no unauthorized semantic inference;
- no permanent full-event-payload persistence requirement;
- Authority-70 generic bridge gap closed;
- WVS7 / real-source production-instance authority still pending.

Your task is to verify those claims against the actual pinned branch/receipts, not merely repeat them.

If the tests can be rerun cheaply and deterministically from the checked-out historical branch without external source material, rerun the exact focused test set and record the command/result. Do not broaden into a full repository or raw-source campaign merely to improve confidence.

## 4. Stage C — current-HQ C05-R2A intake recommendation

Return exactly one recommended disposition:

- `REC08_C05R2A_ACCEPT_CANDIDATE__EXACT_PIN_AND_RECEIPTS_VALIDATED`
- `REC08_C05R2A_RETURN_VALID_BUT_TEST_RERUN_UNAVAILABLE__RECEIPTS_AND_SCOPE_VALIDATE`
- `REC08_C05R2A_BLOCK__EXACT_PIN_OR_ANCESTRY_INVALID`
- `REC08_C05R2A_BLOCK__WRITE_SCOPE_OR_SEMANTIC_CONTRACT_VIOLATION`
- `REC08_C05R2A_RETURN__NAMED_EVIDENCE_REQUIRED`

REC-08 is nondispositive. Only HQ may convert an acceptance candidate into binding current-HQ C05-R2A acceptance.

## 5. Stage D — C05-R2B exact prerequisite frontier

Assuming C05-R2A is an acceptance candidate, determine the exact remaining prerequisites for C05-R2B under authority 36 and current source-certification law.

Do not redesign the production discovery profile.

Identify the minimum exact real-source/release instance package needed to construct one lawful production discovery instance, including at least:

- immutable source/release identity;
- exact source SHA;
- source-native row/variable/slot identity;
- canonical question/component/value/state projection authority;
- occurrence/event-group/index/topology authority;
- routing/applicability/risk-set authority;
- weight/design/estimand authority;
- source-universe relation/comparability authority;
- replay/provenance determinants;
- exact `C11LogicalRelease` / repository identity;
- exact adopted `DiscoveryAuthority` instance identity and derived grammar/catalog/frontier hashes.

Distinguish clearly:

- `ALREADY_BINDING_AND_AVAILABLE`;
- `AVAILABLE_AS_ACCEPTED_SOURCE_CERT_OR_PROJECTION_AUTHORITY`;
- `AVAILABLE_BUT_NOT_YET_ASSEMBLED_INTO_ONE_INSTANCE`;
- `SOURCE_LIMITED__NAMED_INSTANCE_AUTHORITY_PENDING`;
- `MISSING_PROVED` — prohibited unless an explicit governing search law authorizes that conclusion. This handoff does not.

Choose the smallest lawful proving source/release already carrying sufficient exact certification. Do not assume WVS7 if a smaller exact source/release is legally sufficient for C05-R2B proof. Conversely, do not substitute a synthetic fixture for the required real-source production-instance proof.

## 6. Explicit prohibitions

Do NOT:

- search again for whether production DiscoveryAuthority exists; it is already prior-HQ adopted;
- invent a new K/J/depth cap;
- add score/top-k/frequency/unary pruning;
- mutate C11/I03/I05 semantics;
- infer semantic authority from source variable names, labels, missingness or empirical distributions;
- launch C05-R2B;
- launch C09;
- select architecture A/B/C;
- broaden into unrelated local filesystem archaeology;
- declare REC-02 fragments globally missing;
- merge sibling recovery workers.

## 7. Authorized writes

Write only under:

`.../AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/returns/REC-08/`

Required outputs:

- `README.md`
- `C05R2A_EXACT_PIN_AND_ANCESTRY_RECEIPT.json`
- `C05R2A_WRITE_SCOPE_AUDIT.csv`
- `C05R2A_RETURN_AND_TEST_VALIDATION.md`
- `C05R2A_HQ_INTAKE_RECOMMENDATION.md`
- `C05R2B_REAL_SOURCE_INSTANCE_PREREQUISITE_MATRIX.csv`
- `C05R2B_EXACT_LAUNCH_PREREQUISITES.md`
- `OPEN_HQ_QUESTIONS.md`
- `CHANGED_FILES.txt`

No runtime, semantic authority, source binary, schema, production selector or historical worker branch mutation is authorized.

## 8. Return requirements

Return:

- REC-08 branch name;
- exact REC-08 start HEAD;
- exact REC-08 final HEAD;
- exact historical C05-R2A final HEAD;
- ancestry/write-scope verdict;
- receipt/test validation verdict;
- one C05-R2A intake recommendation status;
- exact remaining C05-R2B prerequisite classes and whether each is already available or pending;
- whether C05-R2B is ready for a separate HQ launch handoff;
- changed files;
- stop token.

Stop token:

`REC08_C05R2A_PIN_AND_INTAKE_RETURNED`

Then STOP. Do not execute C05-R2B.