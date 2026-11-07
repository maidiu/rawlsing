# PYAT #753 R8 LOCAL_S2 Continuation Return

**Verdict:** `LOCAL_SOURCEFREE_AUTHORITY_TO_ABI_COMPARISON_EXECUTED__HISTORICAL_READER_AND_MODERN_C11_POSITIVE_WITH_CLOSED_NEGATIVES__NO_PROVED_CURRENT_SELECTED_DEMEMP_CONSUMER`

This is a continuation of PR #769 / issue #766. It does not overwrite the seven-file R8 return. It adds a locally executed companion receipt for the previously `NOT_RUN` sourcefree parity step.

## Scope

- Historical target: `AR-0007 + AR-0046 / Afrobarometer R1 / dememp`, contract `44c656ab1aeccb1e0e7b1254f01360f985fbd8dc99be9c8751bac37bd43ba1ab`.
- Actual historical bytes read from the local Mac originals under `/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/authority/`.
- Modern ABI: `GovernedC11Projection` -> `project_c11_candidate_from_physical_cells` -> C11 candidate validation/replay.
- Synthetic sourcefree physical cells only. No original respondent data, SAV, or product code was executed or modified.
- No I03 `execute_empirical_query`, Field Forge issuance, protected merge, or native authority promotion.

## Environment and byte custody

- R8 worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat753-r8-local-s2-20261107-r1`, branch `research/pyat753-r8-local-s2-continuation-20261107-r1`, base `490fc5f862410d0bd5c55bad4413d1ca991c549b`.
- Candidate adapter worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat748-r5`, head `1a214e6e8d1edef1844001b8772f7581917584f9`.
- Python 3.11.3, pandas 2.3.1, pytest 9.0.2, numpy 2.3.2.
- The five modern C11 ABI files are byte-identical at the R8 base and the candidate adapter commit, including `pre553_source_backed_c11_facade.py` (`7788feb514ad5eceb71e7d76191b1b80a66688dc64a56b0dc05f4a1b19bbdfcf`). The candidate adapter itself is not established as protected/installed.

| Role | Path | Bytes | SHA-256 | Mac == Git worktree |
|---|---|---:|---|---|
| AR-0007 binding | `data/ddm_build_copy/authority/v550_v551_response_semantics_contract_binding_v1.csv` | 5,734 | `89d0cb28c20f014278a58fcbb269b8726efe8a9580f2d470caa299ab113f00eb` | yes |
| AR-0007 manifest | `data/ddm_build_copy/authority/v550_v551_response_semantics_contract_binding_v1.manifest.json` | 5,610 | `5bcfea51b6a62a20aceb7b16dbf122a5dd60e5b236e64e7edb6948322ba396ec` | yes |
| AR-0046 registry | `data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.csv` | 76,430 | `d270f59da94029780b0e7f26f78cc0f5ede418ed431b5ababeefd2c5e2a00fc8` | yes |
| AR-0046 manifest | `data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.manifest.json` | 2,872 | `5e25ae393aef241d17b70b4ee139e5560d1ffbd8379f8b77c26af7cf0c8b0990` | yes |

## Executed tests and results

### 1. Historical reader pytest: PASS

Command, from the R8 worktree:

```sh
PYTHONPATH=. python3 -B -m pytest -v -p no:cacheprovider \
  data/ddm_build_copy/tests/test_postg5_v550_v551_response_semantics_contract.py
```

Result: `14 passed in 1.44s`. Log: `HISTORICAL_READER_PYTEST.log`.

Covered exact registry-key mechanics, legacy whole-frame hash non-substitution, live binding identity, special-row inheritance without scale-contract creation, fail-closed unknown/incomplete semantics, deterministic distinct-contract lookup, preflight six certified R1 keys, and scoped serialization.

### 2. Candidate historical adapter pytest: PASS

Command, from the candidate worktree:

```sh
PYTHONPATH=. python3 -B -m pytest -v -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_historical_authority.py
```

Result: `104 passed in 79.10s`. Log: `CANDIDATE_ADAPTER_PYTEST.log`.

This executes the restored historical reader against the Git-resident AR-0007/AR-0046 and full QSM R1 documents, and exercises the current `AuthorityRegistry` / `RuntimeObjectCatalog` receiving objects and target-use negatives. It is candidate-branch evidence, not a protected installation claim.

### 3. Local sourcefree authority-to-ABI harness: PASS

Command, from this `local_s2` directory:

```sh
PYTHONPATH=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat748-r5 \
R8_ROOT=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat753-r8-local-s2-20261107-r1 \
CANDIDATE_ROOT=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat748-r5 \
python3 -B run_local_s2.py
```

Result: exit 0. Receipt: `LOCAL_S2_RECEIPT.json`; command summary: `LOCAL_S2_COMMANDS_AND_OUTPUT.txt`.

The harness read the four actual Mac original files, verified Mac/Git byte equality and the selected AR-0007/AR-0046 identities, loaded `ResponseSemanticsContractAuthority.from_documents(...)`, and obtained:

- 236 bindings and 145 registry contracts.
- `Afrobarometer/R1/dememp` -> `44c656ab1aeccb1e0e7b1254f01360f985fbd8dc99be9c8751bac37bd43ba1ab`.
- `Afrobarometer/R2/dememp` -> `None`; `ArabBarometer/R1/dememp` -> `None`.
- Exact snapshot authority id `V551_RESPONSE_SEMANTICS_CONTRACT:44c656ab...`, kind `SOURCE_SEMANTICS_TOPOLOGY`, decision `ALLOW`, content hash `44c656ab...`, canonical scope `afrobarometer|ROUND1|dememp`, target use `V551_SIGNED_RELATION_EVIDENCE`, effective time `HISTORICAL_FROZEN`.

## Modern C11 positive and negative receipt

Positive: the exact historical snapshot was bound as both `semantic_authority_ref` and `topology_authority_ref` on a synthetic `dememp` question. The modern C11 projection/candidate accepted it with 7 synthetic cells:

- 4 substantive values: `1`, `2`, `3`, `4`.
- 3 missing values: `9`, `98`, `99`.
- 37 public objects, 7 `RespondentEvent`s, deterministic release ref `729ac0962427544065ba1b0e5a7a212ef05959a5e07ea3ee45e552f833fef073` on repeat.
- Every event authority closure includes the exact `44c656ab...` historical snapshot; the `QuestionVariableBinding` semantic and topology refs both equal that snapshot ref.

This is a genuine local sourcefree authority-to-ABI comparison. It is not evidence that any current operation selects the historical dememp tuple.

Closed negatives:

| Negative | Result |
|---|---|
| Wrong expected source SHA | rejected: `SourceBackedC11FacadeError: snapshot ref does not bind expected source SHA` |
| Historical authority removed from closure | rejected: `C11IntegrityError: exact historical authority unavailable; no fallback permitted` |
| Observed code `4` without a response mapping | rejected: `SourceBackedC11FacadeError: unbound response value/state; no label/frequency/missingness inference` |
| Wrong target use on exact historical snapshot | rejected: `Pre553AuthorityError: exact authority scope does not include target_use_refs` |
| Alternate synthetic contract snapshot | accepted by generic C11; negative control only, not native selection |

The alternate-contract acceptance is deliberately recorded to prevent converting generic C11 compatibility into native authority.

## Current consumer search

Command and output: `CURRENT_CONSUMER_SEARCH.log`.

- `git grep -n -i dememp -- rawlsing_next` -> no matches (exit 1).
- The only current `V550_V551` reference is the infrastructure seam id in `rawlsing_next/pre553_legacy_compat.py:27`; it is not a dememp consumer.
- The real current GT12 operation `rawlsing_next/wave1_gt12_i03_positive_facts.py` selects Afrobarometer R5 `Q86A` and `Q86B`, not the historical R1 dememp tuple; neither Q86 variable is an AR-0007 member.
- No exact currently selected `R1/dememp` C11 physical slot, question binding, or I03 target use was observed in the bounded current source search.

## Five-test disposition

| # | Test | Disposition |
|---:|---|---|
| 1 | Current necessity | `NOT_PROVED` |
| 2 | Successor/equivalence | `UNKNOWN`; not `ALREADY_SATISFIED_BY_EQUIVALENT` |
| 3 | Exact first consumer | `MISSING_SELECTION_AT_UPSTREAM_SOURCE_QUESTION_SEMANTIC_PRODUCER` (conditional; not a confirmed active bug) |
| 4 | Historical vs sourcefree | `HISTORIC_SOURCE_READER_RELEVANT_BUT_CURRENT_CONSUMER_NOT_SELECTED`; `RIGHTS/ISSUER_NATIVE_ONLY_HOLD` for any new original R1/dememp native workload |
| 5 | Comparative gain | `NO_PROVED_GAIN_WITHOUT_EXACT_CURRENT_OPERATION`; no port, no product edit |

**Owner-correct action: HOLD.** Do not attach dememp semantics to GT12 R5 Q86A/Q86B, do not promote the candidate adapter to protected authority, and do not create a synthetic native issuance.

## Limits

- Synthetic cells are sourcefree and replay-only; they are not original respondent data.
- The candidate adapter is not established as protected/installed; only the modern C11 ABI files are byte-identical across the observed commits.
- No I03 `execute_empirical_query` or Field Forge issuance was performed because no exact currently authorized dememp query was formed.
- No product code, protected branch, or PR was modified; no merge was performed.
- A future owner request for an exact current `(Afrobarometer, R1, dememp)` operation remains the trigger for any bounded producer repair.

## Reproduction files

- `run_local_s2.py` — executed harness.
- `LOCAL_S2_RECEIPT.json` — full machine-readable receipt.
- `LOCAL_S2_COMMANDS_AND_OUTPUT.txt` — command/result summary.
- `HISTORICAL_READER_PYTEST.log` — 14/14 pass.
- `CANDIDATE_ADAPTER_PYTEST.log` — 104/104 pass.
- `CURRENT_CONSUMER_SEARCH.log` — current-source negative search.
- `01_LOCAL_S2_FIVE_TEST_DISPOSITION.tsv` — tabular disposition.
