# ZAK01-S2-F03 native hostile witness

**Obligation:** `ZAK01-HOSTILE` (minimum S2).  
**Scope:** synthetic-fixture execution of the actual historical F03 function only.  
**Result:** `F03_S2_POSITIVE_DENIED_PARTIAL_RESTORED_PROVED__PENDING_INDEPENDENT_RECEIVING`.

This directory does **not** contain respondent data, does **not** run S3, and does **not**
claim independent receiving, original source issuance, scientific issuance, or the
original historical production first reader.

## Pins verified on the execution runner

| Item | Value |
|---|---|
| Historical F03 source | `data/ddm_build_copy/ddm_v550_question_relation_authority.py` |
| Historical source commit | `9253064bc9423a0f0ccda4fbdea43c2f54f800c6` |
| Git blob SHA-1 | `62084cbed10a5975f79bd504bf4fb99025e4e64e` |
| Source SHA-256 / bytes | `2fb0851d8bac6f3d381fdf11749f7e04e676de914d643e5be1ad4603cc39f63c` / 38,858 |
| Input-head commit | `52206dc889e094c48c610e30f72824630c697560` |
| Input-head source blob | `62084cbed10a5975f79bd504bf4fb99025e4e64e` (unchanged from historical commit) |
| Selected active registry | `data/ddm_build_copy/bindings/question_relation_registry_35wave_active_v1.csv` |
| Selected registry SHA-256 / bytes | `a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b` / 1,119,028 |
| Selected registry Git blob SHA-1 | `daac001bb8da645c7d99408e2239f4e04b6e9f9b` |
| Synthetic fixture canonical SHA-256 | `bc1f8cda38c83615d0a8ae077976790cb0423dd37ef553095bf8657528363f38` |
| Synthetic fixture file SHA-256 | `eb8b734bf76d959d5de67c3a5a0593d5c1d3a94336533a6a1ef68ce35da982a7` |

Runner: `mainMac.lan`, user `matthewsmith`, macOS 13.2.1 x86_64, Python 3.11.3
(`/usr/local/bin/python3`), pandas 2.3.1.

## Synthetic identity and no-match proof

The synthetic question identity is:

- `source_family = WVS`
- `canonical_wave = W7`
- `country_code = US`
- `question_id = zak01_s2_synthetic_no_match_q1`
- `var_code = zak01_s2_synthetic_no_match_v1`

The selected active registry contains no WVS/W7/US row at all. The script verifies this
both by scanning every registry row through the historical module's own resolution-key
function and by calling the historical resolver, which returns
`BLOCKED_MISSING_AUTHORITY` with `match_count = 0` and `resolved = False`.

The six synthetic structural coordinates are distinct nonempty strings:

`SYNTH_DRIVER_ZAK01_S2_A`, `SYNTH_FACET_ZAK01_S2_B`, `SYNTH_BLOCK_ZAK01_S2_C`,
`SYNTH_DOMAIN_ZAK01_S2_D`, `SYNTH_AXIS_ZAK01_S2_E`, `SYNTH_TARGET_ZAK01_S2_F`.

## Actual execution command

From the evidence worktree:

```text
cd <repo-root>
/usr/local/bin/python3 WORKER_RETURNS/VMESTYE_ZAK01_MCR_R1/S2_NATIVE_F03/run_f03_s2_native.py \
  --repo-root . \
  --out-dir WORKER_RETURNS/VMESTYE_ZAK01_MCR_R1/S2_NATIVE_F03
```

The script imports the historical module by file path with
`importlib.util.spec_from_file_location`, verifies the pinned source SHA-256/Git blob and
registry SHA-256/bytes before import, and writes `WITNESS.json` plus the five output
files. `sys.dont_write_bytecode = True` keeps the source tree clean.

## Outputs and hashes

Canonical serialization for all reported output hashes:

```text
json.dumps(value, sort_keys=True, ensure_ascii=False,
           separators=(',', ':'), allow_nan=False).encode('utf-8')
```

| Case | Input canonical SHA-256 | Output canonical SHA-256 | Output file SHA-256 |
|---|---|---|---|
| A positive | `bc1f8cda38c83615d0a8ae077976790cb0423dd37ef553095bf8657528363f38` | `9741e4a21d089e0e99cf715878cee07a9184bdbe09d05091612f4dcf5177546b` | `e53c74d719451d8d326724851368ed84f56d2929a6c6d667a301484ea40fd8b7` |
| B denied permission | `cde28b9b7fd16e9938cba934494a43a4626f57266d776fdb89484c2b4e7312dd` | `017fdbb6f2d273bfe2cb22fc64783ee85c672fcbee0fc7933a3d2bac1387db3b` | `0309c7ac8a3cc20501ef36d5efebb96f085c164113c442fb910e5dddf1a73cae` |
| C PARTIAL mapping | `63c16c96d893cf493d4fbdfcbc021013a3a81720627381587a07f8032fab6dc7` | `017fdbb6f2d273bfe2cb22fc64783ee85c672fcbee0fc7933a3d2bac1387db3b` | `0309c7ac8a3cc20501ef36d5efebb96f085c164113c442fb910e5dddf1a73cae` |
| D restored exact A input | `bc1f8cda38c83615d0a8ae077976790cb0423dd37ef553095bf8657528363f38` | `9741e4a21d089e0e99cf715878cee07a9184bdbe09d05091612f4dcf5177546b` | `e53c74d719451d8d326724851368ed84f56d2929a6c6d667a301484ea40fd8b7` |
| Supplemental hostile control | `c2bb654a40d1243ed63df585429db73125d87b17a82c635973a0dfa208a85c6c` | `017fdbb6f2d273bfe2cb22fc64783ee85c672fcbee0fc7933a3d2bac1387db3b` | `0309c7ac8a3cc20501ef36d5efebb96f085c164113c442fb910e5dddf1a73cae` |

B, C, and the supplemental hostile control have distinct inputs but converge on the same
output. Each fails the same `quc_is_certified` gate, and the historical function
normalises all three into the same fail-closed cleared-coordinate output. This is an
observed property of the historical branch, not duplicated execution.

`WITNESS.json` SHA-256: `602b7f7970701db36b989838262315ed437c4ddb79e9a74a3e8827b9de680cd4`.
`run_f03_s2_native.py` SHA-256: `73950c198bd20740f81ca0c77a7f9d9f453c6a447d142bc3648d4f8b0cf888a5`.

## Test-time invocation path and first reader

- Invocation path: `run_f03_s2_native.py::execute_case` →
  `ddm_v550_question_relation_authority.apply_question_relation_authority`.
- Test-time first reader: `run_f03_s2_native.py::execute_case` and the
  `AssertionLog` checks are the first code that reads the returned output.
- **The test-time reader is not proof of the original historical production first
  reader.** The original call site, inputs, production consumer, and authority remain
  `NOT_PROVED`.

## Hostile interpretation

Rejected conclusion:

> Because F03 preserved six coordinates and marked the inbound row certified, F03 itself
> established original source authority.

The positive output explicitly reports `question_relation_registry_match = false` and
`question_relation_authority_resolution_status = BLOCKED_MISSING_AUTHORITY`. It preserves
six already-present inbound coordinates and the inbound `CERTIFIED` / `RELATION_EVIDENCE`
labels only because all five inbound conditions are present. It does not establish who
certified the source, whether that issuer was competent, or whether original
source/scientific permissions exist. The supplemental control removes only inbound
certification and shows the same no-match path fails closed, confirming F03 consumes
rather than creates semantic authority.

## Reproduction

1. Check out the evidence commit or the evidence branch.
2. Confirm the pinned source and registry bytes (the `PIN_RECEIPT.txt` contains the exact
   `git` and `shasum` commands and observed output).
3. Run the command above with a Python 3.11 environment that has pandas 2.3.1.
4. Compare `WITNESS.json` output hashes and the `restoration` equality fields. Environment
   fields such as timestamp and PID will differ; output hashes must not.
5. Treat any assertion failure in `WITNESS.json.failures` as a failed rerun and report it
   exactly. All 116 assertions passed in the recorded run.
