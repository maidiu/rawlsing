# W1-H sourcefree selective receiving — proof-integrity repair

**Status: proof repair locally and in CI PASS; reference replay PASS; broad governed court retains exactly three reproduced baseline failures. Ready for competent receiving-owner disposition, not merged.**

Repository `maidiu/rawlsing`; PR [#615](https://github.com/maidiu/rawlsing/pull/615); branch `integration/programma-pyat-w1h-selective-receiving-20261102-r1`. Canonical read/baseline `9809203fd915a84bae056a67210e9213879840db`; incoming receiving head `5fe94cf0f22fba228e0b76cf0d48b9d89d0be5ce`. User-selected local Codex / GPT-6.1 High persists; Python 3.11.3, pytest 9.0.2, pandas 2.3.1 and pyreadstat 1.3.2 observed locally. Backend effort telemetry and quota/cost UNKNOWN. No provider switch.

## Narrow repair and original review applicability

- Proof contract: `rawlsing_next/programma_pyat_reference/test_reference.py.proof.json`, schema `RAWLSING_PROOF_INTEGRITY_R1`, added at `490bc16e291b209fc40c281ca90b5fd3813e4491`. No implementation/test assertions were changed.
- CI runner: one `fetch-depth: 0` checkout setting at `8e2507c3bde8f13ca3da0995c964f44a5f3bfeea`. This is required by an observed CI positive-baseline failure resolving the immutable W1-A Git input; bundled bytes do not replace exact Git evidence. No checker or source-lock bypass.
- The original 47 implementation/data and six essential document Git blobs all match independent-review publication `dbd79795b99b2ac7abca47feba454be82b385e30`. The unchanged implementation was reviewed at `3e2832e0aabab1c72ab9d9f6570869cc75e2c804`.
- Independent review SHA256 remains `8551eb718b5f6ba1ab7e154f5c35f7950b3b2f0639fd2d4d891c7fd3126ac11b`. Original complete receipts remain on that immutable W1-H branch; no duplicate replay corpus is imported.
- Existing distinct implementation review applies to unchanged code/data. New proof metadata and the runner dependency fix are mechanically exercised; this repair does not self-issue a fresh independent whole-map review or adoption.

## Actual positive/fault/restoration witnesses

1. `reference.py::select_edges` depends on excluding `CONDITIONAL_PREREQUISITE` when `unconditional=True`. The contract disables the one uniquely occurring exclusion. `ReferenceTests::test_conditional_edges_not_universal` passes normally and fails its `assertFalse` under the implementation fault.
2. `reference.py::query` exposes the implementation BOUNDARY. Changing its uniquely occurring `source_native_empirical_pilot` from `HOLD` to `PASS` makes `ReferenceTests::test_actual_source_not_consumer_or_fixture` fail its equality assertion.

The canonical checker verifies named-test JUnit failures, refuses import/collection/error-only/skip results and restores the implementation in `finally`. Both witnesses completed locally with the unchanged source restored (Git diff zero for reference.py/test_reference.py).

```json
{
  "schema": "RAWLSING_PROOF_INTEGRITY_R1",
  "status": "MECHANICAL_WITNESS_PASS_NOT_SEMANTIC_ADOPTION",
  "claims": [
    {
      "claim_id": "W1H_CONDITIONAL_PREREQUISITES_REMAIN_CONDITIONAL",
      "positive_node": "rawlsing_next/programma_pyat_reference/test_reference.py::ReferenceTests::test_conditional_edges_not_universal",
      "fault_path": "rawlsing_next/programma_pyat_reference/reference.py",
      "baseline": "PASS",
      "fault_probe": "TARGET_ASSERTION_FAILED",
      "grade": "BOUNDED_MUTATION_DETECTED"
    },
    {
      "claim_id": "W1H_SOURCEFREE_REFERENCE_DOES_NOT_PROMOTE_NATIVE_PILOT",
      "positive_node": "rawlsing_next/programma_pyat_reference/test_reference.py::ReferenceTests::test_actual_source_not_consumer_or_fixture",
      "fault_path": "rawlsing_next/programma_pyat_reference/reference.py",
      "baseline": "PASS",
      "fault_probe": "TARGET_ASSERTION_FAILED",
      "grade": "BOUNDED_MUTATION_DETECTED"
    }
  ]
}
```

## Focused replay and exact proof identity

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest rawlsing_next.programma_pyat_reference.test_reference -v`: all 20 tests pass, unfiltered, 16.417 seconds locally.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m rawlsing_next.programma_pyat_reference.replay`: exit 0 from a disposable detached receiving checkout at proof commit `490bc16e291b209fc40c281ca90b5fd3813e4491`; replay also reruns all 20 tests. Generated outputs stay outside this selective payload.
- All six forward/reverse navigation pairs preserve the same edge IDs. All 39 frozen files, 2,162,728 bytes and 1,048 raw records retained, with 12 H adjudications, 35 source identities and original lane cuts unchanged.
- Cold bytes equal. Snapshot hash `042ec18fe573a2aacd8a4afff8d3750ec102ba696a93e97015ba858e6c45aa65`; snapshot SHA256 `f4fbfecc980d10c17fbd26ec17dfc72069af644601a35f917621b8924b435a20`, both identical to the independently reviewed original.
- Evidence withdrawal changes exactly 12 dependent claims, preserves 1,048 other claims, restores exactly and leaves independent N9C RED intact. No survey/source grant is revoked or restored by this sourcefree evidence test.
- 164 semantically unjoined assertions, eight unavailable declared paths and 14 nonimmutable pointers remain explicit. No scientific/source-native/N11/N12/actor promotion.

## Governed court: inherited failures are not a green court

Local current court and exact PRE-MAIN baseline court both return **144 PASS / 3 FAIL**, with the same three failing nodes below. The court spec and relevant test/implementation Git blobs are identical. No expected result or legacy code was changed.

- `rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py::RuntimePackagingRebindTests::test_lits_authority_overlay_v2_pins_integrated_normalized_sourcebacked_scope`
- `rawlsing_next/tests/test_fiabc_final_preflight_fanin.py::test_live_candidate_c_and_packaging_bind_final_hq_state`
- `rawlsing_next/tests/test_fiabc_final_preflight_fanin.py::test_t5_contract_binds_final_successor_and_lits_current_law`

| Exact path | Baseline and receiving Git blob |
|---|---|
| `rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py` | `fea5a0457062ce639f42d75c470ec89a9dbea531` |
| `rawlsing_next/tests/test_fiabc_final_preflight_fanin.py` | `d9a6c263bf44d86994cb562e835efffe7734c6f0` |
| `rawlsing_next/ee_p2x_darwin_stage_backend.py` | `b655d8b8c73f7721dceb1996baf1b37388dffa60` |
| `rawlsing_next/pre553_candidate_c_production_binding.py` | `c2451b1b9d54b9588455022e0d6625083bb955d2` |
| `.rabochii/court_spec.json` | `67eb1c668c6d03a31f678d6b09db3288bd1ef810` |

The runtime-packaging test retains its historic backend blob expectation; the other two retain the historical candidate-C binding hash. These mismatches reproduce unchanged at the original PRE-MAIN baseline. A first local sparse-checkout run additionally lacked `HQ_HANDOFF/DECISION_LEDGER.jsonl`; materializing that existing tracked fixture resolved the terrain errors before the 144/3 comparison. No original survey was read.

Actual commands (local logs/JSON receipts held under `/tmp/w1h-receiving-repair-20261102/`; remote CI is the durable execution record):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness rawlsing_next/programma_pyat_reference/test_reference.py.proof.json --root . --receipt /tmp/w1h-receiving-repair-20261102/witness.json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest rawlsing_next.programma_pyat_reference.test_reference -v
PYTHONDONTWRITEBYTECODE=1 python3 -m rawlsing_next.programma_pyat_reference.replay
PYTHONDONTWRITEBYTECODE=1 python3 -m rawlsing_next.rabochii_bounded_court .rabochii/court_spec.json --receipt /tmp/w1h-receiving-repair-20261102/court-complete.json
# Same court executed in a detached checkout at exact PRE-MAIN baseline:
PYTHONDONTWRITEBYTECODE=1 RABOCHII_EVIDENCE_EXECUTION_SHA=9809203fd915a84bae056a67210e9213879840db python3 -m rawlsing_next.rabochii_bounded_court .rabochii/court_spec.json --receipt /tmp/w1h-receiving-repair-20261102/baseline-court.json
```

## CI and receiving decision

- [Run 41394001981](https://github.com/maidiu/rawlsing/actions/runs/41394001981): original failure, missing material-integration proof JSON; focused H tests were not disproved.
- [Run 41403430550](https://github.com/maidiu/rawlsing/actions/runs/41403430550): proof JSON found, but its positive baseline could not resolve immutable W1-A Git input in the shallow checkout. Classified runner/source-history dependency, corrected by full-history checkout.
- [Run 41403793263](https://github.com/maidiu/rawlsing/actions/runs/41403793263), exact `8e2507c3bde8f13ca3da0995c964f44a5f3bfeea`: canonical checker self-test 9 PASS; changed-test proof gate PASS with both TARGET_ASSERTION_FAILED witnesses; protocol self-test 20 PASS; court spec PASS; complete bounded court **144 PASS / 3 inherited FAIL**, overall workflow FAILURE. All three failures match the local original PRE-MAIN baseline in node identity and hash mismatch. No new W1-H failure was observed.

PR #615 had no submitted owner review or approval in the inspected PR metadata/comments; it is prepared for the owner decision, not represented as merge-approved. Its receiving conditions explicitly reserve adoption/merge to the rightful receiving owner. The launch authorizes repair and qualified receiving only when that approval and the required gate disposition are available; no approval is fabricated. The historical baseline comparison does not waive a required failing check.

Until the competent existing owner approves this exact selective sourcefree receiving and accepts the documented inherited 3-failure disposition under established governance, PRE-MAIN and canonical Pyat progress MD/JSON remain unchanged. No merge or integrated-reference claim is made. After an authorized actual merge, record its exact GitHub merge SHA and update the canonical progress pair together by current-head CAS, retaining all science/source-native/F6/F7/N9/N11/N12/Sorok holds.

**Engineering:** missing witness repaired locally and in canonical CI; focused/replay PASS with the original reviewed snapshot; broad court remains RED at inherited baseline grain. **Scientific/source/actor authority:** unchanged HOLD. **Protected receiving:** pending the named CI/owner gates.
