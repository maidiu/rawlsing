# Reproducibility and limits

## Exact source and lease verification

| Item | Observed |
|---|---|
| Canonical repository | `/Users/matthewsmith/Desktop/rawlsing_r02v_r2_canonical`; remote `https://github.com/maidiu/rawlsing.git` |
| Commission startup / PRE-MAIN | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| Origin branch tip before work | `8e44ca9c751049d65e6def47600b5c073ee04b29` — exact match |
| Existing worktree for this branch | none |
| D4 worker process before work | none |
| New worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-d4-structural-temporal-fates-20261031-r1` |
| Local branch upstream | `origin/agent/pyat-rrif-d4-structural-temporal-fates-20261031-r1` |
| Worktree status at creation | clean; branch head exactly the startup SHA |
| Force push | not used |
| PRE-MAIN / main mutation | none |
| Sorok / native / protected source | none |
| Other worker relaunch | none |
| Pending reviewer mutation | none |

The branch was created from the exact remote tip. No other worktree was checked out on this branch. The D1 worker was active in a separate worktree; it was not touched. D2/D3 worktrees were not touched.

## Host and harness

| Item | Observed |
|---|---|
| Host | mainMac (macOS Darwin), local OpenCode |
| Working directory for this session | `/Users/matthewsmith` |
| Active session metadata | provider `opencode-go`, model `deepseek-v4.1-flash`, variant `max`, agent `build` |
| Actual reasoning effort | variant `max` is recorded; internal effort is not independently observable |
| Python | `3.11.3` |
| pytest | `9.0.2` |
| Disk free before return | approximately 1.4–2.2 GiB on `/System/Volumes/Data`; volume at 100% capacity |
| Account quota | UNKNOWN |
| Provider cost | UNKNOWN |
| Browser | not used |

The session database records `variant: max` for the active `build` sessions in `/Users/matthewsmith`. No silent provider, model or effort switch was made. The provider account quota and the actual billed cost were not independently verified.

## Commands used for current-scope evidence

All commands were run from the D4 worktree. `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider` were used to avoid writing bytecode or pytest cache into the worktree.

```sh
python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_f8_receipt_permission_identity_hq254.py \
  rawlsing_next/tests/test_pre553_service_f8_source_scope_binding_court.py \
  rawlsing_next/tests/test_pre553_service_f8_source_scope_binding_repair_court.py \
  rawlsing_next/tests/test_pre553_service_f8_binding_authentication_court.py \
  rawlsing_next/tests/test_pre553_service_source_applicability_court.py
# 215 passed

python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  rawlsing_next/tests/test_pre553_source_relations.py
# 121 passed

python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py \
  rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py
# 161 passed
```

Total: **497 passed, 0 failed**. No test file was modified.

No historical candidate was re-staged or executed. Historical F6, P07 native, source-relations hardening and S04 evidence is cited from the exact commits and returns named in `SOURCE_CURRENT_COMPARISONS.md`.

## Scope controls

- E8 `e95d6edb` was read but its mechanical RETIRE/HOLD counts were not used as authentic decisions.
- RRIF-V's 1,333 branch-only implementation records are not current integration.
- The 291 exact-other-path copies require owner/ABI proof and were not promoted.
- B's 155 rows are branch rows, not distinct acceptances.
- The HQ274 checkpoint is not code adoption.
- No whole-estate recount and no PROGRAMMA PYAT work was performed.
- `.rabochii/return_manifest.json` was not written: the commission's deliverable scope is the six named files under `WORKER_RETURNS/PYAT_RRIF_D4_20261031_R1/`. No return-beacon certification is claimed.

## What this return does not establish

- No real survey, respondent, population, cohort, weight, design, transport or target authority.
- No Field Forge structure, causal structure, actor psychology or model-use permission.
- No native P07 execution, TCB acceptance, refcount acceptance or cutover.
- No external issuer, protected current, revocation stream or external custody.
- No actual production service consumer for F6, P07 native, source relations, temporal comparability, F8/EE14 or learned-world composition.
- No behavioral equivalence from exact blob identity.
- No whole-estate recount, no PROGRAMMA PYAT work and no duplicate of #571/#577 reviews.

## Unresolved permissions and holds

- **P07 native execution / TCB / refcount:** HELD.
- **F7 non-forgeable custody (`F7-RR-04G`):** OPEN; architecture decision required.
- **F7 temporal comparability:** no current owner/consumer; S04 not scientifically qualified.
- **F8 / EE14:** `KEEP_EE14_T1_HOLD`; no model-use permission; HQ253 T01 custody gap OPEN; R01 OBS_01 duplicate insensitivity OPEN.
- **Learned world:** LOCAL_UNAUTHENTICATED only; external issuer/protected current/custody HOLD.
- **#580–#584:** held.
- **#571/#577:** not returned at the time of this work; no review of them is claimed.

## Return identity

The final return SHA is the remote branch tip after the final commit and push. It is reported in the handback and must be read back with `git ls-remote` / GitHub. A file cannot contain its own commit SHA.

`FINAL_REMOTE_SHA: REPORTED_OUT_OF_BAND_AFTER_PUSH`

**CLOSURE_ONLY** — no required or background work remains in this return.
