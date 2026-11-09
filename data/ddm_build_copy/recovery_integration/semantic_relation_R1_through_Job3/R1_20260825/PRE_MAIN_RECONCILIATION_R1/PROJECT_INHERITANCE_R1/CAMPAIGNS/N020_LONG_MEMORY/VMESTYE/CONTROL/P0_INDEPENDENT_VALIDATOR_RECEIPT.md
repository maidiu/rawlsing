# VMESTYE ZL-P0R — independent validator and negative-control receipt

**Verdict:** `NOT_RUN_AUTHORIZED_S2_UNVERIFIED`. **No PASS inference.** This is independent S0–S1 source-code inspection, not a test invocation.

## Exact source and execution surface

- Protected PRE-MAIN at receiving startup: `2162d85db5e6822707e5cdff7aac2656ebef4761`.
- Script: `VMESTYE/validation/validate_vmestye.py`, blob `fb39e939ef4bdd21e52bce78d5a50825317acc6f` (197 lines), independently fetched from the protected SHA.
- Actual reviewing host: ChatGPT authenticated GitHub connector with deterministic CodeMode JavaScript documentary reads. Exact model/effort attestation not exposed; no Browser/GPT-6-High claim. No independently qualified S2 project runner or original native/S3 rights.
- Python structural validator: `NOT_RUN`. Deliberate mutant executions: `NOT_RUN`. CI on receiving candidate: `NOT_RUN`. S3/original35/science/actor operations: `NOT_RUN`.
- No stdout/stderr or exit-code receipt exists; any asserted pass would be fabricated.

## What the code *does* and does not check

1. Lines 39–50 enforce one header, unique header field names and strict TSV row widths for its declared input tables. **This is not a P0-01 full census validator**: neither 6,120 census rows nor 110 anti-join rows are parsed and cross-validated by this script.
2. Lines 60–66 compare five protected seed files with pinned Git blob IDs. This guards byte drift, not semantic equivalence.
3. Lines 102–108 demand 18 `NOT_DISPATCHED` flights and nine `NOT_RUN` gates. These are accurate as an older protected planning snapshot, but **incompatible with treating actual ZL-00/ZL-01 returned sessions as the live flight state**. Stage-aware event reconciliation is still missing.
4. Lines 110–152 demand 30 RM locator identities and two SR-01 status/count summaries (Pyat 2,416 and Sorok 1,314); they do not compare every manifest composite key to its original source registries.
5. Lines 154–172 preserve seed estate denominators and keep downstream estates `bootstrapped_ids=0`/`NOT_IMPORTED`. They do not test exact source-field fidelity, 30 frozen AJ-RM check IDs, 23 per-file evidence links, 48 index-only subset, 82 seam predicates, 345 owner-target mappings or actual first-consumer constraints.
6. Lines 174–186 check existing landing paths and canonical files but not versioned literal headers for all required ZL-02–14 return tables.

## Required negative-control cases for a genuinely authorized runner

| Counterexample | Required rejection |
|---|---|
| Remove one LMX/LMQ/C6 seed ID or duplicate one under the same count | Exact-set failure |
| Alter one frozen seed blob byte | Pinned-content failure |
| Drop RM24 or misrepresent RM09 `REPAIR` as `PASS` | Source/status failure |
| Mark SR-01 independent acceptance/functional equivalence `PASS` without receiving | False-green failure |
| Drop a specific Sorok 48 index-only ID while retaining summary count | Per-ID anti-join failure (new P0 validator required) |
| Rename AJ-RMxx without bijection | Contract crosswalk failure (new P0 validator required) |
| Supply per-file D02–D07 evidence pointer selecting no census rows | Dangling foreign-key failure (new P0 validator required) |
| Modify one of 82 seam `original_predicate` values but preserve edge ID | Source-grain/predicate failure (new P0 validator required) |
| Change an actual worker to `RETURNED_AT_SHA` while old snapshot remains `NOT_DISPATCHED` | Correct event-aware handling; do not overwrite history or assert no return |

**Required acceptance receipt:** exact qualified runner and permission, protected/project source cut, invocation, unmodified baseline exit/status, mutant names and expected/actual rejection, stdout/stderr, validator version, and independent readback. A revised validator cannot invent native S3 proof or current functional zero loss.

**Owner:** qualified S2 runner issuer + ZL-00 contract/validator author; independent #799 re-review at corrected immutable heads. Until then `P0_VALIDATOR_NEGATIVES_NOT_RUN__NO_P1_RELEASE`.
