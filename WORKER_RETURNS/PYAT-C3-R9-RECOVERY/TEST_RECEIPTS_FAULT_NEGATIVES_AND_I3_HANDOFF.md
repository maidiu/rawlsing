# TEST RECEIPTS, FAULT NEGATIVES, AND I3 HANDOFF

Status: `SOURCEFREE_EVIDENCE_COMPLETE__NO_CANDIDATE__ENGINEERING_HOLD`

Branch: `agent/pyat-recover-c3-r9-decoder-source-access-compatibility-20261030-r1`
Branch tip: `750548ddbb9b4392a16ce93097b856f349e16182`
Receiving PRE-MAIN baseline: `8e44ca9c751049d65e6def47600b5c073ee04b29`

## Fresh session provenance

- Host: `mainMac.lan`, Darwin 22.3.0, macOS 13.2.1, x86_64.
- Harness: OpenCode `1.18.34`, agent `build`, primary mode.
- Session ID: `ses_e6d2c881effeylhClQfNwjPOVq`.
- Directory: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-recover-c3-r9-decoder-source-access-compatibility-20261030-r1`.
- Model: `opencode-go/deepseek-v4.1-flash`, variant `max`.
- Session created 2026-10-31 16:38:14 UTC; not a historical C3/R9, S7, S7-FIX, PE/SC0, S1/H1/H03, or S6 session.
- No autonomous model/editor switch occurred.

## Environments

| Purpose | Interpreter | pytest | pandas | pyreadstat | Evidence |
|---|---|---|---|---|---|
| Current-tree tests | CPython 3.11.3 `/usr/local/bin/python3` | 9.0.2 | 2.3.1 | 1.3.2 | `TEST_RECEIPTS/ENVIRONMENT.txt` |
| Historical C3/R9 pinned reconstruction | CPython 3.11.3 in temp venv | 9.1.1 | 2.3.3 | 1.3.6 | `TEST_RECEIPTS/ENVIRONMENT.txt` |

The historical R9 broker requires pyreadstat `1.3.6` and fails closed otherwise. The pinned temp venv was reconstructed outside the repository. It is **not** a governed C4C3 environment; HQ207 already recorded the named governed interpreter as absent on this host. Results are strong evidence, not a governed-environment certification.

## Exact test commands and exits

### 1. Exact C3 55-test historical court

Reconstructed tree: `git archive 283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1 rawlsing_next` plus the three tracked fixtures:
`WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py`, `WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING/01_PHYSICAL_KEY_INVENTORY.json`, `WORKER_RETURNS/FIABC-LM2/wvs7_projection_structural_input.json`.

Command (ambient):
```
PYTHONPATH=. PYTHONHASHSEED=0 python3 -m pytest -q \
  rawlsing_next/tests/test_closed35_g01_sav_numeric_representation_authority.py \
  rawlsing_next/tests/test_closed35_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py \
  rawlsing_next/tests/test_r35_i01_physical_metadata.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py
```
Exit `0`; `55 passed in 48.53s`. Receipt `TEST_RECEIPTS/C3_55_COURT.txt` SHA-256 `c438b6266f8423c317120fffad698eae66eb0906ab9f365bc008cc38df3a96c0`.

Same command with the pinned `1.3.6/2.3.3/9.1.1` venv:
Exit `0`; `55 passed in 47.86s`. Receipt `TEST_RECEIPTS/C3_55_COURT_PINNED.txt` SHA-256 `bacf8ff4330f8e8995e9e1c43ca57b8c7a9cc19bb9e2bfaf549dea1dd103bc61`.

This is the exact historical six-file denominator, not a reduced gate. It is evidence that the accepted C3 sourcefree repairs work in their own tree. It is **not** evidence that they are present in current PRE-MAIN.

### 2. Nine SAV representation oracles

```
PYTHONPATH=. PYTHONHASHSEED=0 python3 -m pytest -q \
  rawlsing_next/tests/test_closed35_g01_sav_numeric_representation_authority.py
```
Exit `0`; `9 passed in 0.12s`. Receipt `TEST_RECEIPTS/C3_G01_NINE.txt` SHA-256 `38025b23df21b23d371cb04835992ad56739231045e0683deb6a80c6d699b19d`.

The nine surfaces are S016, S037, S038 and S005-S010 over exact sources 02, 06 and 21. The nine tests exercise exact source SHA, variable, ordinal, native int code, R5 float64 tokens and physical binding keys, including noncoercion and fail-closed wrong-source/variable/ordinal/code cases.

### 3. Accepted R9 broker/session/binding courts

Reconstructed tree: `git archive dfdf5659fd78e9bc996b07383349094059a5553d rawlsing_next` (the accepted R9 runtime placement).

```
PYTHONPATH=. PYTHONHASHSEED=0 <pinned-venv>/bin/python -m pytest -q \
  rawlsing_next/tests/test_pre553_execution_binding_court.py \
  rawlsing_next/tests/test_pre553_source_session_court.py \
  rawlsing_next/tests/test_pre553_source_access_broker_court.py
```
Exit `0`; `69 passed in 1.23s` (34 execution-binding + 15 source-session + 20 broker). Receipt `TEST_RECEIPTS/R9_69_COURT.txt` SHA-256 `0302c31c8c4226cff4b297669bea400b13fac2d8d6a9fb0e575e85d12392e6cd`.

Per-file counts were also measured separately: execution-binding `34 passed`, source-session `15 passed`, broker `20 passed`.

### 4. R9 tree against current SAV representation tests — counterexample

The accepted R9 tree was also run with the current `test_fiabc_lm2_r1j_sav_representation_authority.py`, `test_r35_i01_physical_metadata.py`, and `test_pre553_source_backed_c11_facade.py` alongside the 69 R9 courts.

Exit `1`; `6 failed, 88 passed in 1.65s`. Receipt `TEST_RECEIPTS/R9_TREE_CURRENT_REPRESENTATION_FAILURES.txt` SHA-256 `f33598c41ede3fc5872a112774f07ea246364a8ef42b0836540f5b3f53679c76`.

The six failures are in the current SAV representation court:
`test_exact_r1i_float_carrier_keyspace_now_matches_governed_numeric_rules`,
`test_no_generic_numeric_coercion_was_added_to_c11_key_law`,
`test_special_codes_remain_noncanonical_and_system_missing_remains_separate`,
`test_substantive_mapping_ceiling_and_question_mapping_are_unchanged`,
`test_projection_and_response_binding_reissued_but_lock2_preserved`,
`test_non_wvs_behavior_and_candidate_boundary_remain_closed`.

Interpretation: the accepted R9 decoder is not a drop-in current successor. This is lineage divergence, not a claim that R9 was wrong in its own tree. HQ204/HQ207 already recorded the two SR06 seam failures and their bounded resolution on the accepted lineage; this receipt adds the current representation court to the nonadoption boundary.

### 5. Current universal 105

```
PYTHONPATH=. PYTHONHASHSEED=0 python3 -m pytest -q \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_universal_source_projection.py \
  rawlsing_next/tests/test_universal_grammar.py \
  rawlsing_next/tests/test_universal_source_byte_custody.py
```
Exit `0`; `105 passed in 128.11s`. Receipt `TEST_RECEIPTS/CURRENT_105.txt` SHA-256 `f70fe202ff85793c79d5e192e6bdfef83d21c7694f482c1cd9697d8632673b5d`.

This is the current universal receiver positive baseline: actual decoder -> source-native adapter -> universal workload -> issued workload -> C11/Route B/I03/I05/Batch.

### 6. Current physical-decoder/source-custody courts

```
PYTHONPATH=. PYTHONHASHSEED=0 python3 -m pytest -q \
  rawlsing_next/tests/test_universal_source_byte_custody.py \
  rawlsing_next/tests/test_r35_i01_physical_metadata.py \
  rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py
```
Exit `0`; `51 passed in 56.63s`. Receipt `TEST_RECEIPTS/CURRENT_PHYSICAL_CUSTODY_51.txt` SHA-256 `2bc084810c8cfce320b8ab1c137587b0850ac1ee6a4f1f21de9de8314348894f`.

This exercises the PR526 `_SourceSnapshot` read-only, rewind, unlink, close, hash, replacement, stale and TOCTOU cases in the current tree.

### 7. Fault-negative harness

```
PYTHONPATH=. PYTHONHASHSEED=0 python3 -m pytest -q \
  WORKER_RETURNS/PYAT-C3-R9-RECOVERY/FAULT_NEGATIVES/test_c3_r9_fault_negatives.py
```
Exit `0`; `9 passed in 1.08s`. Receipt `TEST_RECEIPTS/FAULT_NEGATIVES_9.txt` SHA-256 `c0550b6229ae20f913d9972d30606eb4d69e38c3c596bec13370e8d9c05ed428`.

## Fault negatives: named receiver, mutation, restore

The harness is `FAULT_NEGATIVES/test_c3_r9_fault_negatives.py`. It never reads a real survey source. It uses synthetic SAV carriers only.

| # | Named receiving assertion | Producer mutation / absence | Observed failure | Baseline restore |
|---|---|---|---|---|
| 1 | `execute_universal_workload(...).anti_join()["no_drop_ok"] is True` | none; current positive | — | `105 passed` overall; harness positive executed C11/RouteB/I03/I05/Batch |
| 2 | G01 exact float binding key `47f141e4...` from `physical_value_binding_key` | native code delivered as Python `int 1` instead of `float 1.0` | int key `b9b72033...` != G01 key; named assertion fails | `float 1.0` restores exact key |
| 3 | `PhysicalSourceIncidence.physical_metadata_digest` equals F8.2 digest | SAV raw geometry F8.0 instead of F8.2 | digest differs; named assertion fails | F8.2 restores digest |
| 4 | D01 declared encoding admission for `ac0b8bc1 -> BIG5` | current decoder has no `DECLARED_ENCODING_ALLOWLIST`; `_compatibility_config` rejects | `DecoderError: encoding override is not in the frozen exact SHA/config allowlist` | compatibility latin1 lane and unencoded decode still pass |
| 5 | D02 exact opaque date/time carrier (`isinstance(raw_value, R5OpaqueValue)`) | current `_jsonable` stringifies `date(2020,1,2)` to `"2020-01-02"`; codec has no constructor | named assertion fails; `R5CodecError` on direct encode | ordinary string and float codec roundtrips still pass |
| 6 | `verify_source_identity()` equals original source SHA after tampering the original path | original file overwritten with `b"tampered"` | snapshot still equals original SHA; fresh decode with old SHA fails `source sha256 mismatch before governed decode` | restoring original bytes makes fresh decode pass |
| 7 | `verify_source_identity()` after snapshot-byte tamper / close | monkeypatched `_sha_fd` wrong digest; then closed snapshot | `source snapshot bytes changed after identity acquisition`; `source snapshot is closed` | restoring `_sha_fd` and a fresh decode pass |
| 8 | snapshot reads after source path removal; fresh decode after removal | original path deleted | snapshot still verifies and yields original cells; fresh decode fails `source bytes unavailable`; R9 broker/session/binding imports raise `ModuleNotFoundError` | restoring bytes makes fresh decode pass |
| 9 | current issuer/edition gate | wrong host, wrong scope permission, wrong source edition, empty scientific permissions, switched decision ref | `SOURCE_HOST_PURPOSE_MISMATCH`, `CURRENT_COMPETENT_SOURCE_AND_SCIENCE_DECISION_REQUIRED`, `ISSUED_SOURCE_EDITION_MISMATCH`, `SEPARATE_SOURCE_AND_SCIENTIFIC_PERMISSIONS_REQUIRED`, `UNKNOWN_DECISION_REF` | original TEST_ONLY record admits again |

Additional non-executable negatives, required by the commission but impossible without a real owner:

- **wrong role**: `IssuedWorkloadRecord` has no `role` field and no role owner exists. The harness asserts `"role" not in fields(record)` and `"issuer_role" not in fields(record)`. A test-only role would be a fake caller/issuer and was not created.
- **replay/session switch at R9 session level**: no `GovernedSourceSession` exists current. Only the current exact `decision_ref` switch is testable; it returns `UNKNOWN_DECISION_REF`. The R9 session-level guard is HOLD, not simulated.
- **missing broker**: the broker module is absent; import fails. The harness does not invent a stand-in broker.

## Same-claim first consumer actually executed

The following are not mocks:

- Current positive: `execute_universal_workload` actually called `execute_test_only_workload` -> `execute_issued_workload` -> `execute_route_b_production` and `build_source_backed_c11_repository`, then `BatchExecutionRunner` and `CarrierNeutralResearchExecutor` executed I03/I05 units. The positive anti-join passed.
- G01 receiver: `pre553_source_backed_c11_facade.physical_value_binding_key` actually executed and returned the exact accepted G01 key for float.
- D01 receiver: `pre553_physical_decoder._compatibility_config` actually executed and rejected BIG5.
- D02 receivers: `pre553_physical_decoder._jsonable` and `pre553_r5_codec.R5TypedValueCodec.encode` actually executed; date/time was stringified/rejected.
- PR526 receiver: `decode_sav` actually executed `_acquire_source_snapshot`, `source_custody`, `verify_source_identity`, `iter_cells`, `close`.
- R9: no consumer executed because no current consumer exists. The historical courts were executed only in the reconstructed historical tree.

## Missing prerequisites

1. A real current issuer/role owner. `TestOnlyDecisionResolver` is the current test double; it is not a production issuer.
2. Raw source authority for D01 declared encoding SHAs and D02 affected source 14. None was opened or materialized.
3. PRE-MAIN write permission for the production decoder/codec changes D01/D02 require. This worker may write only under `WORKER_RETURNS/PYAT-C3-R9-RECOVERY/`.
4. A real current consumer for R9 broker/session/binding or for the G01 authority object. No current import/call exists.
5. Governed C4C3/R7 interpreter. The named path is absent; the pinned venv is a disclosed reconstruction, not a governed environment.
6. all35 frontier producer and N9/N10W implementation. The current all35 path requires an external `IssuedEstateFrontier`; N9/N10W are explicitly not implemented.

## I3 handoff

An independent I3 reviewer should attack at least:

1. **PR526 custody not weakened**: diff `rawlsing_next` against `750548ddb` and `8e44ca9c`; `_SourceSnapshot` must be byte-identical `8732e34d`; fault tests 6-8 must still pass.
2. **No production writes**: `git diff --name-only 750548ddb` must show only `WORKER_RETURNS/PYAT-C3-R9-RECOVERY/**`.
3. **No fake issuer/role**: confirm the harness does not manufacture an `IssuedWorkloadRecord` for production; confirm `TestOnlyDecisionResolver` is labelled TEST_ONLY; confirm no role field was invented.
4. **C3 court denominator**: rerun the exact six files at `283d2c5d2` with the three tracked fixtures; require 55/55 and do not accept 55/55 as evidence of current presence.
5. **R9 courts**: rerun the exact accepted blobs under pyreadstat 1.3.6; require 34/15/20 and confirm the module blobs are `090d978b/ac1390b8/0e11af22`.
6. **Current receiver**: rerun the 105 and 51 receipts; verify the positive fault test actually reaches C11/RouteB/I03/I05/Batch.
7. **Nonadoption boundary**: check each status in `ORIGINAL_FUNCTION_SUCCESSOR_COMPARISON.jsonl` against the current import graph; in particular confirm no current caller of G01/D01/D02/R9 exists.
8. **Source/fault negatives**: verify each named assertion fails on the mutation and restores on baseline; verify the two non-executable negatives (role, R9 session replay) are reported as HOLD, not faked.

The I3 reviewer must not accept this return on 55/55 alone, must not treat AST identity as behavioral equivalence, and must not merge or self-accept. This worker made no adoption, merge, or review decision.
