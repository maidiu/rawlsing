# REPRODUCIBILITY AND LIMITS

## Frozen source and live custody

| Item | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Assigned branch | `agent/pyat-rrif-d2-source-ingress-custody-20261031-r1` |
| Startup / PRE-MAIN | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| RRIF-C | `b75addf621c3a6c1a3b196bd92a810fad77ae3ae` |
| RRIF-V | `bec050449f0b38606718e4e9691caa1721fcd94f` |
| A | `84182f9fa7044d67689ea4f80eabf7e9337f15c2` |
| B | `59e6e62600814d82cfefd1a2137b7aa63316bc95` |
| A×B | `f5a9facd189af6756c2b15c8daebe680016f658a` |
| E8 | `e95d6edb9300b2cc8b0ad2c70dff3953c8afe1ba` |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-d2-source-ingress-custody-20261031-r1` |
| Content commit | `TO_BE_RECORDED_AFTER_COMMIT` |
| Final branch HEAD / readback | `TO_BE_RECORDED_AFTER_PUSH` |

## Host / model / effort

- Host: `mainMac`, macOS 13.2.1 (22D68), x86_64, Intel i9-9880H.
- Harness: OpenCode 1.18.34.
- Model surface: `opencode-go/deepseek-v4.1-flash`, local session variant `max`.
- Session: `ses_e6b412564ffeeBfEjjDzcgYT2f` (this D2 task may be a new session ID; see SESSION_LOCATOR).
- **MAX:** local session metadata reports `variant: max`; no provider-side entitlement attestation. Treat as local-session MAX evidence only.
- No model/harness switch, no subagent, no paid provider call.

## Exact reads

- RRIF-C `UNIQUE_IMPLEMENTATION_LINEAGES.jsonl` and `GENUINELY_UNRESOLVED_IMPLEMENTATIONS.jsonl` at `b75addf6`; six lineage rows read exactly once.
- RRIF-C `ACCEPTED_BUT_NOT_RETAINED.md`, `DENOMINATOR_AND_DEDUP_VALIDATION.json`, `SELECTIVE_FANIN_PROPOSALS.md`.
- RRIF-V `00_RETURN.md`, `ADMISSIBLE_REDUCED_SCOPE.md`, `HOSTILE_FINDINGS.md`, `DECISION_ATTRIBUTION_DEFECTS.jsonl`, `FALSE_SUBTRACTION_CASES.jsonl`.
- B5 historical: `agent/c02e-b5-mandatory-ingress-6b98a6e@20213bef`, `agent/c02g-producer-trust-90a6a1f@83a9208e`, `agent/c02h-separated-principal-0e01de5@82309fe1`, `agent/rabochii-pyat-hq281-c02j-mandatory-b5-owner-trust-r1@8959803`, `agent/rabochii-pyat-hq282-n04-b5-owner-interface-correction-r1@b5a6b640`, and N04R reviewer `fde95ee9`.
- EE14 historical/current: HQ262 `22cd4976`, HQ266 `bdc65ff8`, HQ268 `f10523e1`, current `8e44`.
- R56 historical/reviews: R02 `6f4be338`, R02V review `a287674b`, R02V-R2 `e1f0aeb6`, C1 `a5489365`, current `8e44`.
- R157: final review `d81bc2c67`, foundation `519355ec`, integration `056849e2`, LITS `c868cc73`, source handoff `6be64d7e`.
- SRC04: observed empirical `b6be4058`, actual carrier review `751fece9`, CD native review `9b66083f`, consumers `39c713a1`, current `8e44`.
- S00D: `4c8168b7`; current absence and missing `r3_s02_seam_witness.py` dependency.
- Current PRE-MAIN tests: B5/M2 67; R56 31; SRC04 query 32; EE14 96.

## Commands actually run

```sh
# static state probe (read-only; does not import branch code)
PYTHONPATH=. python3 WORKER_RETURNS/PYAT_RRIF_D2_20261031_R1/probes/lineage_state_probe.py

# current PRE-MAIN sourcefree tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_universal_source_projection.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_empirical_query.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py
```

Results: 67, 31, 32 and 96 passed; zero failures/errors/skips. Focused subsets 4+4+4 passed. No branch candidate source was imported or executed.

## Reviews and pending work

- Consumed: R02V `REVISE` then R02V-R2 `ACCEPT_SCOPED_LOCAL`; N04R bounded checkpoint `PASS`; current EE14 96-test court; current query tests.
- Not consumed because not returned at this cut: #564, #565, #569, #570, #571, #575–#579. Their sealed branches were still at dispatch SHAs. #577’s unchanged remote does **not** mean the worker is idle. #580–#584 stay held.
- R61 R09V/R2 reviews are about `CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py`, not the R56 adapter. They are not used as R56 verdicts.

## RRIF-V custody corrections preserved

- A’s 2,269 is not current subtraction: 1,333 branch-only, 291 other-path, 199 same-path exact, 62 non-code modified composition.
- 291 exact-other-path matches are source-copy/fixture-related, not runtime/ABI equivalence.
- B is 155 branch rows / 122 unique primary IDs / 135 decision records / 151 fate-classified / 4 unclassified / 5 `HQ_OTHER`.
- `CKPT-20261009-HQ274` is documentary intake with candidate NOT_ADOPTED, not code acceptance.
- No whole-estate recount, no 2,831 census, no PROGRAMMA PYAT.

## Limits

- Exact blob identity is not behavioral or semantic equivalence.
- Static imports are not proved live consumers.
- Current absence is not global absence; renamed/rewritten successors may exist.
- No raw survey, original U/E_pre, native source, CAN/ADP/SCI05, Pyat N11/N12, C11, actor or model-use grant was accessed or issued.
- No PRE-MAIN/main, protected source, pending reviewer or active worktree was modified. No force push or branch deletion.
- No sourcefree code patch is included because no clearly superior limited fix was established: B5/SRC04/S00D are blocked on issuer/authority/consumer; R157 has no current consumer; EE14/R56 are already current.
