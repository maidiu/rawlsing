# RECEIVING TEST AND CAS PREFLIGHT — RRIF-F0

## 1. Frozen state

- PRE-MAIN: `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- E1: `ffd03934d0a86c98ed095d973e45587bd5751013`.
- E4 hostile: `5dc00a1eb0d2881a9d74661b7a94d436cc7b7c60`.
- E4F: `f2c0af3273d612bff0a7bd2407532b52caf4348b`.
- E5: `96e6d49ac18274332751c5fbb87c6ed370e8fd9c`.
- E4FR return: `7cd2206fd976606d3816589e2fce03c03c827f39`.
- E6 return: `b0f7675bf4f434bc8964c9b3ebc8392bb33d56fb`.
- HQ ledger commissioned cut: `d80901e9de78803c031fa9d25146f7d8b6aeba2c`; live head `75eb695ad27652020f9ffc0363f846a7c85ca758`.

All worktrees below are detached, sparse, and disposable. No active worker worktree or PRE-MAIN ref is mutated.

```sh
REPO=/Users/matthewsmith/Desktop/Rawlsing
WORK=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode

git -C "$REPO" worktree add --detach "$WORK/f0-wt-premain" 8e44ca9c751049d65e6def47600b5c073ee04b29
git -C "$REPO" worktree add --detach "$WORK/f0-wt-e1"      ffd03934d0a86c98ed095d973e45587bd5751013
git -C "$REPO" worktree add --detach "$WORK/f0-wt-e4f"     f2c0af3273d612bff0a7bd2407532b52caf4348b
git -C "$REPO" worktree add --detach "$WORK/f0-wt-e5"      96e6d49ac18274332751c5fbb87c6ed370e8fd9c
for w in premain e1 e4f e5; do
  git -C "$WORK/f0-wt-$w" sparse-checkout init --cone
  git -C "$WORK/f0-wt-$w" sparse-checkout set rawlsing_next tests WORKER_RETURNS
done
```

Test virtualenv (isolated; system pytest/pandas are reused):

```sh
python3 -m venv --system-site-packages "$WORK/f0-venv"
"$WORK/f0-venv/bin/python" -m pip install pyreadstat==1.3.6 pyarrow==25.0.1 duckdb==2.0.0
"$WORK/f0-venv/bin/python" -c "import pytest,pandas,numpy,pyreadstat,pyarrow,duckdb; print(pytest.__version__,pandas.__version__,numpy.__version__,pyreadstat.__version__,pyarrow.__version__,duckdb.__version__)"
# observed: 9.1.1 3.0.6 2.4.6 1.3.6 25.0.1 2.0.0
```

## 2. PRE-MAIN baseline sourcefree regressions

```sh
cd "$WORK/f0-wt-premain"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. "$WORK/f0-venv/bin/python" -m pytest -q -p no:cacheprovider \
  --junitxml="$WORK/f0_baseline_b5_m2.xml" \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py
```

Observed: `67 passed in 0.67s`, exit `0` (39 accepted B5 + 28 accepted M2).

```sh
mkdir -p "$WORK/f0-overlay"
git -C "$REPO" show 96e6d49ac:rawlsing_next/tests/test_pre553_e5_s06g_independent_hostile.py \
  > "$WORK/f0-overlay/test_pre553_e5_s06g_independent_hostile_e2.py"
git -C "$REPO" hash-object "$WORK/f0-overlay/test_pre553_e5_s06g_independent_hostile_e2.py"
# 9a469ad0940216e02967c94159db943d2979154a

cd "$WORK/f0-wt-premain"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. "$WORK/f0-venv/bin/python" -m pytest -q -p no:cacheprovider --tb=line \
  --junitxml="$WORK/f0_e2_premain_serial.xml" \
  "$WORK/f0-overlay/test_pre553_e5_s06g_independent_hostile_e2.py"
```

Observed: `10 failed in 0.21s`, exit `1`. This is the PRE-MAIN defect-presence baseline, not an E5 regression. One run concurrent with a separate pytest process produced `9 failed, 1 passed` because `test_concurrent_selection_one_winner_one_conflict_and_cold_restore` is timing-sensitive on unpatched PRE-MAIN; the serial clean runs produce `10 failed`. E6 independently recorded the same caveat.

## 3. E1 D02 explicit RED witness

E1's own unit suite is green but does not exercise the real pandas subclass route:

```sh
cd "$WORK/f0-wt-e1"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. "$WORK/f0-venv/bin/python" -m pytest -q -p no:cacheprovider \
  --junitxml="$WORK/f0_e1_33.xml" \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py
```

Observed: `33 passed in 1.59s`, exit `0`.

The real SAV/DTA witness uses the E4F test as a test-only overlay in the throwaway E1 worktree:

```sh
cp "$WORK/f0-wt-e4f/rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py" \
   "$WORK/f0-wt-e1/rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py"

cd "$WORK/f0-wt-e1"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. "$WORK/f0-venv/bin/python" -m pytest -q -p no:cacheprovider --tb=line \
  --junitxml="$WORK/f0_e1_d02_red.xml" \
  'rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py::test_real_sav_and_dta_datetime_cells_are_opaque_at_cells_and_first_seam' \
  'rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py::test_naive_timestamp_and_subclasses_canonicalize_to_exact_carrier'
rm "$WORK/f0-wt-e1/rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py"
```

Observed: `3 failed in 1.18s`, exit `1`:

- SAV param: `assert <class 'str'> is R5OpaqueValue`; cell `raw_value='2008-04-05 06:07:08'`.
- DTA param: same `str` assertion and value.
- Naive subclass: `R5CodecError: unsupported opaque decoder value type _NaiveDT`.

E1 D02 is explicitly RED. The 33 unit-level passes do not override the real-cell failure.

## 4. E4F receiving-shape preflight

```sh
cd "$WORK/f0-wt-e4f"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. "$WORK/f0-venv/bin/python" -m pytest -q -p no:cacheprovider \
  --junitxml="$WORK/f0_e4f_45.xml" \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py \
  rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py
```

Observed: `45 passed in 5.08s`, exit `0` (11 D01 + 18 E1 D02 + 4 integration + 12 E4F).

```sh
cd "$WORK/f0-wt-e4f"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. "$WORK/f0-venv/bin/python" -m pytest -q -p no:cacheprovider \
  --junitxml="$WORK/f0_e4f_selected.xml" \
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

Observed: `194 passed, 1 skipped in 250.27s`, exit `0`. The skip is `test_real_writer_dta_extended_missing_fixture_or_typed_dependency_limitation` (pyreadstat writer/readback does not expose `missing_user_values`). This run requires `WORKER_RETURNS` in the sparse set plus `pyarrow` and `duckdb`. Without that fixture directory the first sparse run reported 14 failures; without `pyarrow`/`duckdb` the carrier court reported 7 more. Those were missing-fixture or missing-module failures, not E4F defects; all disappear with the exact tree and test dependencies installed.

The E4FR independent review of exact `f2c0af32` is `7cd2206f`. It approves the bounded D01/D02 sourcefree fan-in, records the two-level item-chain stringification as a disclosed non-blocking residual outside the one-level promise, and holds science and authority. This F0 document transcribes that verdict; it does not independently re-review it.

## 5. E5 receiving-shape preflight

```sh
git -C "$REPO" show 1b5b6072:rawlsing_next/tests/test_hq284_s06fr_native_review.py \
  > "$WORK/f0-overlay/test_hq284_s06fr_native_review.py"
git -C "$REPO" hash-object "$WORK/f0-overlay/test_hq284_s06fr_native_review.py"
# a25cf5a5ecec4b473ccceaec8a032747d804da7d

E5_FILES=(
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py
  rawlsing_next/tests/test_pre553_learned_product_release.py
  rawlsing_next/tests/test_pre553_s06g_atomic_integrity.py
  rawlsing_next/tests/test_pre553_e5_s06g_independent_hostile.py
  rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py
  rawlsing_next/tests/test_pre553_learned_world_composition.py
  "$WORK/f0-overlay/test_hq284_s06fr_native_review.py"
)

cd "$WORK/f0-wt-e5"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. "$WORK/f0-venv/bin/python" -m pytest -q -p no:cacheprovider --tb=line -rA \
  --junitxml="$WORK/f0_e5_unfiltered.xml" "${E5_FILES[@]}"
```

Observed: `179 passed, 14 failed in 22.85s`, exit `1`. Per court:

| Court | Tests | Pass | Fail |
|---|---:|---:|---:|
| Accepted B5 | 39 | 39 | 0 |
| Accepted M2 | 28 | 26 | 2 |
| S06G repair | 42 | 42 | 0 |
| E2 independent | 10 | 10 | 0 |
| Adjacent EE14 asof + world | 45 | 45 | 0 |
| Frozen S06FR overlay | 29 | 17 | 12 |
| Total | 193 | 179 | 14 |

The two M2 failures are the unchanged accepted tests `test_17_binding_cannot_resolve_different_release` and `test_18_endpoint_failover_only_among_same_release`, both refusing at foreign release/binding setup with `M2ReleaseError: RELEASE_UNAVAILABLE`. The twelve overlay failures are preserved `OBSERVED` defect-presence assertions.

```sh
cd "$WORK/f0-wt-e5"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. "$WORK/f0-venv/bin/python" -m pytest -q -p no:cacheprovider --tb=line \
  -k 'not OBSERVED and not test_17_binding_cannot_resolve_different_release and not test_18_endpoint_failover_only_among_same_release' \
  --junitxml="$WORK/f0_e5_filtered.xml" "${E5_FILES[@]}"
```

Observed: `179 passed, 14 deselected in 25.09s`, exit `0`. This is a selection, not a green full suite.

E6 returned `b0f7675b` with `HOLD_E5_LOCAL_SOURCEFREE_FANIN_PENDING_OWNER_AUTHORIZED_VERSIONED_M2_FIXTURE_AMENDMENT`. The accepted-M2 owner decision is absent. E6 states that an owner amendment must be followed by a fresh full court and a distinct review of the resulting SHA. E5 is not selectable.

## 6. G01 severance baseline

```sh
cd "$WORK/f0-wt-premain"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. "$WORK/f0-venv/bin/python" -m pytest -q -p no:cacheprovider --tb=line -rA \
  --junitxml="$WORK/f0_g01_premain.xml" -k 'native_to_canonical or special_states' \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py
# 2 failed, 6 deselected; exit 1

cd "$WORK/f0-wt-e4f"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. "$WORK/f0-venv/bin/python" -m pytest -q -p no:cacheprovider --tb=line -rA \
  --junitxml="$WORK/f0_g01_e4f.xml" -k 'native_to_canonical or special_states' \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py
# 2 failed, 6 deselected; exit 1
```

Both runs fail the same two node ids with the same assertion values:

- `test_native_to_canonical_mapping_authority_does_not_bridge_physical_representation`: `47f141e43fb2...` vs `b9b720335f37...`.
- `test_special_states_remain_noncanonical_and_mapping_authority_does_not_leak`: `StopIteration`.

G01 remains held and out of D02 scope.

## 7. Receiving preflight tool

From the F0 branch worktree:

```sh
cd "$WORK/pyat-rrif-f0-receiving-20261101-r1"
PYTHONDONTWRITEBYTECODE=1 "$WORK/f0-venv/bin/python" -m pytest -q -p no:cacheprovider \
  --junitxml="$WORK/f0_preflight_tests.xml" \
  WORKER_RETURNS/PYAT_RRIF_F0_RECEIVING_PREFLIGHT_20261101_R1/test_receiving_preflight.py
```

Observed: `16 passed in 0.05s`, exit `0`.

No-receipt live refusal:

```sh
PYTHONDONTWRITEBYTECODE=1 "$WORK/f0-venv/bin/python" \
  WORKER_RETURNS/PYAT_RRIF_F0_RECEIVING_PREFLIGHT_20261101_R1/receiving_preflight.py \
  --repo "$REPO" \
  --allowlist WORKER_RETURNS/PYAT_RRIF_F0_RECEIVING_PREFLIGHT_20261101_R1/EXACT_PATCH_PATH_AND_BLOB_ALLOWLIST.json \
  --premain-ref refs/remotes/origin/integration/pre-main-reconciliation-r1 \
  --json-out "$WORK/f0_live_pending.json"
```

Observed: exit `2`; both gates `BLOCKED`; `receiving_ready: false`; `selectable_payload: []`. The blockers are the missing exact independent review receipts, all required test receipts, and the missing M2 owner decision. The reviewer branches are returned, not at PRE-MAIN, but the gate still refuses without receipts.

Prepared E4FR receipt:

```sh
python3 - <<'PY'
import json
from pathlib import Path
allow = Path("WORKER_RETURNS/PYAT_RRIF_F0_RECEIVING_PREFLIGHT_20261101_R1/EXACT_PATCH_PATH_AND_BLOB_ALLOWLIST.json")
data = json.loads(allow.read_text())
Path("/tmp/f0_ready_receipts.json").write_text(json.dumps(data["receipts_template"], indent=2) + "\n")
PY
PYTHONDONTWRITEBYTECODE=1 "$WORK/f0-venv/bin/python" \
  WORKER_RETURNS/PYAT_RRIF_F0_RECEIVING_PREFLIGHT_20261101_R1/receiving_preflight.py \
  --repo "$REPO" \
  --allowlist WORKER_RETURNS/PYAT_RRIF_F0_RECEIVING_PREFLIGHT_20261101_R1/EXACT_PATCH_PATH_AND_BLOB_ALLOWLIST.json \
  --premain-ref refs/remotes/origin/integration/pre-main-reconciliation-r1 \
  --receipts /tmp/f0_ready_receipts.json \
  --json-out "$WORK/f0_live_ready.json"
```

Observed: exit `2`; E4F `SELECTABLE` with exactly six payload paths; E5 `BLOCKED` by `REVIEW_VERDICT 'HOLD' != 'ACCEPT'`, the RED unfiltered status, and the missing owner decision; `receiving_ready: false`.

The checker verifies live candidate SHAs, before/after blobs, changed paths outside the allowlist, payload collisions, PRE-MAIN head, reviewer branch state, receipt path existence at the live reviewer SHA, reviewer SHA, reviewed candidate SHA, reviewer distinctness, required test-receipt fields, M2 owner decision, and conflict-test set. It does not execute the pytest courts; the integrator must run them and attest the receipts. A false declaration is outside what a source-free preflight can prove.

## 8. Receipt hashes

| Receipt | sha256 |
|---|---|
| baseline B5/M2 JUnit | `affd8cbf604626673ab1d4991632640171af7e7f2f61b1d84273c0242d86ed8b` |
| PRE-MAIN E2 serial log | `31271278b2145d122f8e7dbfdb8d4aebf282e7d442fe9f8329e1d8d623746749` |
| PRE-MAIN E2 serial JUnit | `88a8499174f47b0949fc73ae4d21f9cadc74d06665f7883cbdcf14b98683f4ca` |
| E1 33 log | `92f093df9c20d0092a2d8da22ca7279d33b2dd0341c361766a52675fa9449ef8` |
| E1 33 JUnit | `44a1fc36c68539946b4f20eff21867c2cdaad7ad329e0c6d024af14b8e23e54e` |
| E1 D02 RED log | `ab5b95313bc785f4974d6ff54e97b162a639ca7cb3e9024d77e9154282ef20fe` |
| E1 D02 RED JUnit | `c69b3a2bbe2e69e66ccebf78983b70b8ebad15a6dca05180e01e41f76e673b2f` |
| E4F 45 JUnit | `9e4a7238c8724e780cac04ab74fb58b0ade53a2a2a60c6539c6a28c57ae7f203` |
| E4F selected log | `24b36de8c9760cc36a101e58a67ed674d1eb99844baaef9776fb6fd80a039b4f` |
| E4F selected JUnit | `d1f676ec6da50e8d27c9cd39472ef33df6888c5869ebee7dbee08f76769c57bf` |
| E5 unfiltered log | `249d26508ae56dcb84aba274f2be5addc3f70ff7a5e17a92bf10cda904d98af1` |
| E5 unfiltered JUnit | `0c628a910403b48bad6a8b278d5f76519460214975b9e92a451734ce6a1fa45d` |
| E5 filtered log | `59ced46e75d9a78d0f85f4463ecc26b68aa93fe8538bca6b48445419377d5425` |
| E5 filtered JUnit | `b9016d498cf76aef62e90114b34ae7329555428e98b67f51e32229447d693e59` |
| G01 PRE-MAIN log | `35cb2ce12d585903d7c422b520d27eff65ff790797ff68a91606cc9ce63253b7` |
| G01 E4F log | `2d0d7f12039f35c0b7c3307185f8004e2c5b70ebf8d5a550602d61b970b0d14e` |
| Preflight unit log | `590dbc4f5c123295cd127dfad099b8f0f74b5daff9de9099967616ab6655a2b8` |
| Live no-receipt JSON | `7fe39bbf087ab9efb992354d7cc9ee2ba861c850eb96894c39a88d9bd545f840` |
| Live prepared-receipt JSON | `fad719586c5d642bc69047189407ae13e55d62df38016c82ee91da8ae18a3f88` |
| Ledger precheck log | `539adc231d108f69b2516b4afb269489277402b05d497732f5be284189d5ee16` |

## 9. Disabled approvals

- E1 `ffd03934` alone; E4 `5dc00a1e` as acceptance.
- E4F merge/adoption without the integrator receipt binding exact E4FR `7cd2206f` to exact E4F `f2c0af32`.
- E5 on the E6 HOLD, without an owner-authorized versioned M2 fixture amendment for both named conflicts, or without a fresh distinct review of the resulting SHA.
- E5 filtered `179 passed / 14 deselected` as a green full suite.
- Wholesale branch cherry-pick or merge; old S06F owner import; R9 broker; G01 repair or authority.
- Source-native survey/source/U-E_pre/actor/N11/N12/Sorok/PROGRAMMA execution.
- Protected PRE-MAIN write, merge, force-push, branch deletion, or self-adoption.
- Scientific meaning, source rights, licence, issuer/use, or external release authority.

## 10. No protected write

The preflight uses only `git rev-parse`, `git diff --name-only`, `git show`, `git cat-file`, and `git merge-tree`, read-only. It does not checkout, fetch, merge, cherry-pick, write refs, delete branches, or execute source-native code. The test worktrees are detached and disposable; the E1 overlay test copy is untracked and removed after the run.
