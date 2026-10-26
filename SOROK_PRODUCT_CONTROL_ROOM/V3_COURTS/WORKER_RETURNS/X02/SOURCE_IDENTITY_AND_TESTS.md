# X02 source identity and test execution

## 1. Access and source cut

- Authorized local source: `<V3_SOURCE_ROOT>` (read-only inspection).
- Historical source bundle: `Rawlsing_code_bundle_staging`.
- Local staging zip: `<LOCAL_STAGING_ZIP>`.
- Local zip SHA-256: `3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289`.
- TD-R05 original archive identity: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`.
- **Archive-wide identity: NOT CLAIMED.** The local zip hash differs from the TD-R05 archive identity. The exact inspected files match the local source directory, the same entries in the local zip, and the S50 31-file identity manifest. This is a staging/repackaging caveat, not a claim of the original archive.

## 2. File-level identity

**S50 selected identity manifest:** `SOROK-20261025-S50-HISTORICAL-V3-ACTOR-RECOVERY-R1/01_SOURCE_IDENTITIES.json`, 31/31 exact.

| File | SHA-256 | Lines |
|---|---|---:|
| `v3/psyche/flow.py` | `6da4effde2b1ccb7c346f73b17632ceee3a7a8c37a63a10f096753d070ab1d3d` | 843 |
| `v3/psyche/channels.py` | `2d00bf6b8720879e610160e58455f983e1e63fbe8ceef1a93f46844de8a3f111` | 201 |
| `v3/psyche/gating.py` | `4a82c7c91828b87bb61cd651c777159f04b5733e64158f8679a24efcec1ccfc6` | 236 |
| `v3/psyche/vitality.py` | `56fed88e37299862774b2401c9a7e43363de6d6bb47a78f8f4744dcc6f91e912` | 191 |
| `v3/psyche/insulation.py` | `c8dd5f96111d3b247ddcf27b876d09c05460b06d7961193bff039e39e5967d28` | 147 |
| `v3/psyche/vessels.py` | `6f4855eef0c19ef514983d4cb47fc21873d6e2af5368b17ea294f8f187f17438` | 119 |
| `v3/core/state.py` | `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2` | 614 |
| `v3/core/derived.py` | `e479fc3eba21734752c372742fb2ee247cbdde6a73ac42545dc30b5039301360` | 378 |
| `v3/systems/domains.py` | `24e5215763a11e439075ea7a0f4ac32ae425856a9fd4624744d4a2a744758280` | 56 |
| `v3/systems/frameworks.py` | `0d59fc6e177009da92e39eb61ea729eace97f50392baa93999cb6513f81dd2cb` | 119 |
| `v3/systems/buffers.py` | `9c9ed09001dad364ab4011ee29e8ea2df3c332745db736b1a6e1dbe56e332b35` | 80 |
| `v3/systems/stability_inertia.py` | `5a11c8b07eafe2b8f1d7e9864c9cb066a5c45f19c2c45a8d4223b3a64c394c78` | 83 |
| `v3/systems/autonomy_safety.py` | `fdb6ae0d78bbb93041217e7cd98f16526c97d924393c9f6fd51aa56a128b0e56` | 110 |
| `v3/engine/yearly_step.py` | `da3147c3da7ff2724a61dd26d595055668899c83beb541400f58633568b92acb` | 200 |
| `v3/engine/event_engine.py` | `b57e7ef4df5dabd996dc7de19c1c2c273ad90ee89d73570df1fd85674dd98ded` | 210 |
| `v3/engine/llm_contract.py` | `f024debf7b8a637e91c546689a0bed31baff55d98f1378b06cb82ebb4c0fe9cf` | 891 |
| `v3/engine/run_llm_band.py` | `120e177462219e8ccd5d5e0d7fdb23de993639f5af8be6c40a06db36e0b37a38` | 431 |
| `v3/io/persona_sheet.py` | `4a0009533443baef2786fc498c7f8db3ead7d133d8ee7e97e6d7128d4322a00e` | 993 |
| `v3/v3_yearly_step_order.yaml` | see `source_identity.json` | — |

`vessels.py` is a helper for attribution/vessel labels, not a primary formula source.

Machine-readable rows: `source_identity.json`.

## 3. Test execution

**Command used:**

```sh
PYTHONPATH=<read-only YAML bridge> PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest -q -p no:cacheprovider <17 historical V3 test files>
```

**Result:** **82 passed**, 0 failed, 0 errors, `logs/pytest_x02_original_v3.log`.

**Important:** the runtime has no PyYAML; a read-only local `yaml.safe_load` bridge (Ruby Psych) was placed on `PYTHONPATH` outside the source tree. No package installation, no source edit, no network/provider call.

| Group | Passed |
|---|---:|
| `test_v5_pressure_flow.py` | 23 |
| `test_v5_pressureflow_golden_run.py` | 1 |
| `test_v5_pressureflow_mediates_relation_state_without_surface_leak.py` | 1 |
| `test_v5_surface_psyche_profile.py` | 5 |
| `test_v5_sublimation_channels.py` | 3 |
| `test_v5_baseline_load.py` | 8 |
| `test_phase3_activation_gate.py` | 5 |
| `test_v5_vitality_fatigue.py` | 3 |
| `test_v5_insulation_registry.py` | 4 |
| `test_v5_vessel_hints.py` | 4 |
| `test_step_logic.py` | 12 |
| `test_v5_render_surface_psyche.py` | 3 |
| `test_v5_persona_sheet_surface_psyche.py` | 2 |
| `test_v5_v2_chat_prompt_no_raw_v5_leaks.py` | 1 |
| `test_v5_structural_diagnostics.py` | 1 |
| `test_architecture_invariants.py` + `test_invariants.py` | 6 |
| **Total** | **82** |

**Not run:**

- the exact full TD-R05 80-test suite as a single run;
- server/model/provider integration;
- live persona conversation;
- current Sorok S44/S49/S52 consumer;
- original respondent/survey data;
- native actor/person tests.

**Coverage limit:** the 82 tests prove historical source behavior at the fixture/test grain; they do not prove current integration, native science or a developing person.

## 4. Read-only discipline

- Original source files were not edited.
- Test execution used `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider` for the logged run.
- The source directory contains pre-existing `__pycache__`/`.pytest_cache` from prior authorized runs; the reviewer did not remove them. No source bytes changed.
- Review artifacts are written only under the assigned M03/M05/M08/M10/M21/M23/M24 card directories and `V3_COURTS/WORKER_RETURNS/X02/`.

## 5. Evidence

- `evidence/probe_flow.py` — read-only probe (formula, channel, groove, memory, hostage duplicate, ratchet, transaction boundary, buffer, event semantics, categorical audit).
- `evidence/probe_flow.json` — probe output.
- `logs/pytest_x02_original_v3.log` — 82-pass test log.
- `source_identity.json` — exact file/zip/manifest checks.
- `SOURCE_INDEX.json` — index of source, evidence and dispositions.
- `EXECUTION_LEDGER.json` — commands/exit/results.
