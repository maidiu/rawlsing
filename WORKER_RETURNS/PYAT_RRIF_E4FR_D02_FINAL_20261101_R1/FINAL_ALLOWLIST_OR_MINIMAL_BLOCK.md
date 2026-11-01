# FINAL ALLOWLIST OR MINIMAL BLOCK — PYAT RRIF-E4FR D02 FINAL

## 1. Verdict

`APPROVE_E4F_PHYSICAL_D01_D02_SOURCEFREE_FANIN`

This is an exact-scope independent engineering fan-in approval, not HQ adoption, not a merge, not source-use or scientific authority, and not timezone-aware carrier authority. It accepts the E4F corrected candidate at:

- `f2c0af3273d612bff0a7bd2407532b52caf4348b`
- parent / correction base: `ffd03934d0a86c98ed095d973e45587bd5751013`
- live PREMAIN / reviewer branch start: `8e44ca9c751049d65e6def47600b5c073ee04b29`

No further historical court is required for this bounded E4F correction. Pyat HQ still separately adjudicates this exact returned review SHA; this reviewer does not self-adopt or implement.

## 2. Exact three-source-file allowlist

These three files, and only these three, are the production/test allowlist for the E4F correction:

| # | Path | Git blob | sha256 | Role |
|---|---|---|---|---|
| 1 | `rawlsing_next/pre553_physical_decoder.py` | `4b89c4598f324834de064c1200c63698a20e3c5c` | `f9794976aef51c418e8152850a7b0143df6790d0596549ea7f0991fc1f4501e9` | decoder subclass gate, typed range classification, `__all__` |
| 2 | `rawlsing_next/pre553_r5_codec.py` | `f5f64d9b8b6c9af1d1b755f86b44fe43a8e741b7` | `fc3aaec95d1ea6b396afb7484e5b58a242a878f9a003b47a30d7f35d48eaa9ae` | naive subclass canonicalizer, aware/lossy refusal, opaque packer |
| 3 | `rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py` | `c07c2019455e6264b4297c1c1d782bd887b96bdd` | `1042789d92c94dd5ef983299f4cbc46b40bc55e2d556f055f6777ada11254737` | bounded real SAV/DTA and hostile D02 tests |

## 3. Original E1 test allowlist (unchanged, 33 tests)

These E1 test files are part of the acceptance evidence and are unchanged by E4F:

| # | Path | Git blob | Tests |
|---|---|---|---|
| 4 | `rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py` | `625f1d8b1f3fa8c24501addcaff7d70209598596` | 11 |
| 5 | `rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py` | `ac5f331322a69dab224eeeda14b05681918b432e` | 18 |
| 6 | `rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py` | `bfa20f7a35ef9a399bec5380b6c3e6f9caad0115` | 4 |

The E4F correction does not modify these files. They are the original E1 test allowlist, not new production authority.

## 4. Not in the allowlist

- The five return documents under `WORKER_RETURNS/PYAT_RRIF_E4F_D02_20261101_R1/` are documentary evidence only; they are not production or test authority.
- No D01 constant/config, PR526 custody code, SAV float code, G01 representation, R9 broker, native/source grant, or aware-carrier representation is in the allowlist.
- No pinned seam file is added to production. `rawlsing_next/pre553_r5_seam.py` is absent at E4F and is loaded test-only from the historical Git object database.
- No file from E4, F0, PROGRAMMA, Sorok, native, or protected PREMAIN is in the allowlist.

## 5. Pre-merge verification commands

From a clean checkout or verification worktree, before applying anything:

```
git fetch origin \
  agent/pyat-rrif-e4f-d02-real-datetime-fix-20261101-r1 \
  integration/pre-main-reconciliation-r1

git rev-parse f2c0af3273d612bff0a7bd2407532b52caf4348b
git rev-parse f2c0af327^       # must be ffd03934d0a86c98ed095d973e45587bd5751013
git ls-remote origin refs/heads/agent/pyat-rrif-e4f-d02-real-datetime-fix-20261101-r1
git ls-remote origin refs/heads/integration/pre-main-reconciliation-r1
```

Expected live values at review time: E4F `f2c0af3273d612bff0a7bd2407532b52caf4348b`; PREMAIN `8e44ca9c751049d65e6def47600b5c073ee04b29`.

Verify the exact change surface:

```
git diff --name-only ffd03934 f2c0af32
git diff --stat    ffd03934 f2c0af32
git diff --numstat ffd03934 f2c0af32 -- \
  rawlsing_next/pre553_physical_decoder.py \
  rawlsing_next/pre553_r5_codec.py \
  rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py
```

Expected name-only set: the two production files, the new D02 test, and the five E4F return documents. Expected numstat: decoder `22/6`, codec `71/13`, test `314/0`. Any other path is outside this allowlist.

Verify the exact blobs:

```
for p in \
  rawlsing_next/pre553_physical_decoder.py \
  rawlsing_next/pre553_r5_codec.py \
  rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py
do
  printf '%s ' "$p"
  git rev-parse "f2c0af32:$p"
  git show "f2c0af32:$p" | shasum -a 256
done
```

Expected blob and sha256 pairs are exactly those in §2 and §3. Reject if any differ, if the seam file appears in the production tree, or if `git diff --name-only` contains any additional production/test path.

## 6. Acceptance test commands

Create a clean detached worktree at the exact E4F SHA. Do not test in an author worktree.

```
git worktree add --detach --no-checkout /tmp/e4fr-accept f2c0af3273d612bff0a7bd2407532b52caf4348b
cd /tmp/e4fr-accept
git sparse-checkout init --cone
git sparse-checkout set rawlsing_next tests \
  WORKER_RETURNS/EE-P2R6S \
  WORKER_RETURNS/FIABC-LM2 \
  WORKER_RETURNS/FIABC-LM2-R1F-CARRIER-ARCHAEOLOGY \
  WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING
git checkout --detach f2c0af3273d612bff0a7bd2407532b52caf4348b
test -z "$(git status --porcelain)"
```

### 6.1 New E4F D02 tests — must be 12 passed, exit 0

```
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py
```

### 6.2 Original E1 33 — must be 33 passed, exit 0

```
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py
```

### 6.3 Selected PR526/SAV/C11/EE-P2X — must be 194 passed, 1 skipped, exit 0

```
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py \
  rawlsing_next/tests/test_universal_source_byte_custody.py \
  rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py \
  rawlsing_next/tests/test_fiabc_lm1_r1e_n1_physical_boundary.py \
  rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py \
  rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py \
  rawlsing_next/tests/test_universal_source_projection.py \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_r35_i01_physical_metadata.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  tests/test_ee_p2x_darwin_court_driver.py \
  tests/test_fiabc_final_measurement_telemetry_closure.py
```

The skip must be `test_real_writer_dta_extended_missing_fixture_or_typed_dependency_limitation`; any other skip or any failure is a new defect and blocks this allowlist.

### 6.4 G01 baseline severance — expected nonzero, not an E4F regression

Run the same two G01 files on PREMAIN `8e44ca9c` and E4F `f2c0af32`. Expected on both: exactly `test_native_to_canonical_mapping_authority_does_not_bridge_physical_representation` and `test_special_states_remain_noncanonical_and_mapping_authority_does_not_leak` fail, with the same `47f141e43fb2…` vs `b9b720335f37…` assertion and `StopIteration`. If the GC stall occurs, use a wrapper that only does `gc.disable()`, calls `pytest.main(sys.argv[1:])`, prints `PYTEST_MAIN_RETURN`, and `os._exit(rc)`; do not change tests or options.

```
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 <gc-wrapper> \
  -q -p no:cacheprovider --tb=short -rA \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_inventory.py \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py
```

Expected: `2 failed, 7 passed`, exit `1`, same two failure identities on both cuts. A different count or different assertion values is a new defect and blocks this allowlist. G01 itself remains `HELD`; this is severance evidence, not repair.

### 6.5 D01 exact-pair spot check — must match

```
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from rawlsing_next import pre553_physical_decoder as d
expected = {
 "ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2": "BIG5",
 "5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2": "WINDOWS-1252",
 "66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec": "WINDOWS-1252",
}
assert dict(d.DECLARED_ENCODING_ALLOWLIST) == expected
assert not (set(d.DECLARED_ENCODING_ALLOWLIST) & set(d.COMPATIBILITY_ALLOWLIST))
for sha, enc in expected.items():
    assert d._compatibility_config(sha, enc) == {
        "encoding": enc,
        "authority_status": "SOURCE_DECLARED_EXACT_SHA_ENCODING__PHYSICAL_DECODING_ONLY",
    }
print("D01 exact pairs OK")
PY
```

## 7. Acceptance criteria

Accept the E4F correction for the bounded PRE-MAIN integration only if all of the following hold:

1. `f2c0af32^ == ffd03934d0a86c98ed095d973e45587bd5751013` and the live E4F ref still equals `f2c0af3273d612bff0a7bd2407532b52caf4348b` (or HQ adjudicates the exact newer SHA separately).
2. The change surface is exactly the two production files, the one bounded D02 test, and the five return documents; no other production/test path.
3. The six blobs in §2–§3 match exactly.
4. New 12: `12 passed`, exit `0`.
5. E1 33: `33 passed`, exit `0`.
6. Selected suite: `194 passed, 1 skipped`, exit `0`, skip exactly the known writer limitation.
7. G01: `2 failed, 7 passed` on both PREMAIN and E4F with the same two node ids/assertion values; treat as baseline, not a pass.
8. D01 exact-pair spot check passes; PR526 custody and SAV float tests are included in the selected suite and pass.
9. No production seam file is added; no test-only pinned-seam execution is cited as installed-current production first seam.

## 8. Non-blocking recorded boundary

The following is explicitly not a blocker for this bounded allowlist, but must travel with the acceptance record:

- A two-or-more-level `.item()` wrapper containing an aware date can still stringify through unchanged recursive `_jsonable`. It is outside the accepted one-level D02 promise, is not reachable from the current pyreadstat SAV/DTA cell route, and is not aware-carrier authority. Do not describe it as a refused or carried aware value.
- `numpy.datetime64[ns]` and `numpy.datetime64('NaT')` are not built-in date/time subclasses and are not produced by the current SAV/DTA `DATETIME` cell route; their `.item()` returns int/None and they are outside this D02 scope.
- The test's first-choice import of `rawlsing_next.pre553_r5_seam` would prefer a future installed production seam over the pinned historical blob. At this cut the seam is absent and the pinned blob was executed. Do not cite the test as proof of an installed-current seam.

If future hardening of recursive item handling is desired, it is a new bounded change with its own review/tests; this exact E4F allowlist does not require it and does not need another historical court.

## 9. Authority and closeout

- ENGINEERING: `PASS` at the exact bounded E4F scope, subject to the commands above.
- SCIENTIFIC: `NO_SCIENTIFIC_OR_SOURCE_MEANING_CLAIM__HELD`.
- AUTHORITY: `HELD`; no source-use/license/rights, aware-carrier authority, G01 authority, issuer/use, protected PRE-MAIN merge, adoption, or self-review is granted.
- HQ adjudicates this returned review SHA separately. This reviewer does not self-adopt or implement.
- No PROGRAMMA work, native/survey source execution, protected PRE-MAIN/main/Sorok write, or mutation of the E4F branch is authorized or performed.

Terminal: `E4FR_FINAL_ALLOWLIST__APPROVE_E4F_PHYSICAL_D01_D02_SOURCEFREE_FANIN__NESTED_ITEM_BOUNDARY_NONBLOCKING__HQ_ADJUDICATION_HELD`
