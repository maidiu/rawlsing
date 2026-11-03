# SOROK JOIN-E — upstream B-event causal connection

**STATUS:** `B_EVENT_UPSTREAM_CONNECTION_BOUND__PERFORMED_OMITTED_REFUSED_UNAVAILABLE_DISTINCT__CUT_RED_RESTORE_GREEN_COLD__NOT_NATIVE__NOT_SELF_ADOPTED`
**BRANCH:** `codex/sorok-join-e-b-event`
**BASE:** `7bf2da302996491ddf34b9a039fea47ac982d135`
**PRIOR SCOPED REVIEW:** `4387dc818` (JOIN-V fork-atomicity acceptance; return files unchanged)
**GRADE:** `TEST_ONLY_SOURCEFREE_NOT_NATIVE`
**AUTHORITY:** no native CAN/ADP/C8/C9/C10/C11/C12/Pyat, provider call, human A5, production deployment or scientific issuance.

## 1. FINDING | INTERPRETATION AND RIVALS | HQ ACTION | OWNER

| FINDING | INTERPRETATION AND RIVALS | HQ ACTION | COMPETENT OWNER |
|---|---|---|---|
| **B1. B's upstream source is now a real sealed occurrence with a performer receipt, not a post-C9 material flag.** `joined/b_event.py` reuses the R31J/R29M sealed `OTHER_PERFORMED` mechanism and R31J `pre_c9`/`build` unchanged. B `SHARE_TOOL` performed has `b_performed=True`; the omission record keeps the same qualified share operation but seals `b_performed=False`; refusal keeps the existing `REFUSE_TOOL` performed record. | The rival — a boolean `material_feasible_after` edit — is rejected: the existing R29M evaluator derives the material result from the sealed B record, and R31J binds that result before C8. No new B motive or action law is introduced. | Accept the sourcefree upstream edge; keep native action-owner issuance held. | JOIN-E + R31J/R29M owner + BP2/C9 owner |
| **B2. The performer receipt is preserved into C8, C12, session metadata and cold reopen.** The receipt binds actor B, independent owner, event ref/hash, clock 5, operation, quantity, recipient A, performed bit and disposition. `validate_receipt` compares it with the product source and the C12/C8 source at open and verify. | The rival — a receipt that exists only beside an unbound product — is rejected by source/C8/C12 equality checks and receipt tamper refusal (`J_PROVENANCE_MISMATCH`). | Retain; actor-limited source, no A-authored B event. | JOIN-E + C12/C8 custodian |
| **B3. The same unchanged assertion is RED on the upstream source cut and GREEN on restore, including cold reopen.** `SOROK_JOIN_E_B_EVENT_UPSTREAM_P01` is true for B performed (`HELP_ACCEPT`, target present, tools 1), false for B omission (`HELP_REFUSE`, no target, tools 0), false after cold cut, and true after cold restore. | A construction crash or import error is not used as the negative. The cut changes the actual upstream B occurrence while the A side, E1, clock, branch and root contract stay fixed. | Preserve the assertion and the explicit cut/restore receipt. | JOIN-E + independent reviewer |
| **B4. Omission, refusal and unavailable source are distinct.** Omission: `SHARE_TOOL`/`performed=False`/`OMITTED`/`GM01_OMISSION`. Refusal: `REFUSE_TOOL`/`performed=True`/`REFUSED`/`GM01_REFUSAL`. Unavailable: typed `B_SOURCE_OCCURRENCE_ABSENT`, no session or product. All three have distinct B event hashes; performed/omitted/refused also have distinct C8 state digests. | The rival — treating all no-tool outcomes as “refusal” — is false. The targetless omission and refusal paths both have no C9 target, but they are not the same source disposition. | Preserve the distinctions; do not mint a C9 target on either targetless path. | JOIN-E + BP2P4/C9/C12 owner |
| **B5. Existing refusal/no-change, incompatible-root rejection and tamper checks remain green.** The preserved JOIN-E suite runs 25/25; new tests retain refusal, foreign-root and receipt/disposition tamper checks. | The change is additive to the existing canonical root/branch/lineage contract, not a second root or a replacement of the prior targetless path. | Independent review of this changed boundary. | JOIN-E + JOIN-V/HQ |

## 2. IMPLEMENTED AND CHANGED PATHS

Changed only under `WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/**`:

- `joined/b_event.py` (new): sealed B source performer/receipt, disposition validation, performed/omitted/refused/unavailable scenarios.
- `joined/session.py`: performed receipt binding, C8/C12/source checks and cold receipt validation.
- `joined/refusal.py`: targetless omission path using `GM01_OMISSION`, distinct from `GM01_REFUSAL`; general receipt/disposition validation.
- `joined/assertion.py`: `SOROK_JOIN_E_B_EVENT_UPSTREAM_P01` unchanged across cut/restore.
- `joined/cli.py`: runnable `b-contrast` command.
- `tests/test_b_event.py` (new): 7 focused tests.
- `evidence/b_event_contrast.json` (new): causal receipts.
- `B_EVENT_UPSTREAM_RETURN.md` (this file).

No `vendor/j` or `vendor/e` file was edited. No JOIN-V `4387dc818` file was edited. No second product root was introduced: every session still uses `<state_root>/product`, branch `first_session`, and the existing C12 root contract.

## 3. EXACT COMMANDS AND RESULTS

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests/test_b_event.py \
  -p no:cacheprovider --tb=short
7 passed

PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests \
  -p no:cacheprovider --tb=short
25 passed in 42.54s
```

Runnable contrast:

```text
PYTHONPATH=WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1 \
  python3 -B -m joined.cli b-contrast --state <fresh-state-root>
exit 0
```

Output summary: performed assertion `true`, omitted/cut assertion `false`, performed `HELP_ACCEPT`, omitted/refused `HELP_REFUSE`, both branch `first_session`, both session verify `true`, cut cold `false`, restored cold `true`, unavailable `B_SOURCE_OCCURRENCE_ABSENT`.

**Reviewer replay: `NOT_RUN`.** The preserved JOIN-V `4387dc818` worktree replay command was denied by the operator. No reviewer file was changed.

## 4. CAUSAL RECEIPTS

Full machine receipt: `evidence/b_event_contrast.json`.

| Observation | B performed | B omitted | B refused |
|---|---|---|---|
| B receipt disposition | `PERFORMED` | `OMITTED` | `REFUSED` |
| B event ref | `TEST_ONLY_EVENT_share` | `TEST_ONLY_EVENT_omit` | `TEST_ONLY_EVENT_refuse` |
| B event hash | `16f11d2e…a486` | `fd131cf3…c07c` | `3e00199d…9421` |
| Operation / performed | `SHARE_TOOL` / `True` | `SHARE_TOOL` / `False` | `REFUSE_TOOL` / `True` |
| B clock | `5` | `5` | `5` |
| C8 source equals product source | `true` | `true` | `true` |
| C8 state digest | `b33f5759…55c8` | `1a211ed6…b54c` | `661e9519…723b` |
| C9 | target present | `NO_CHANGE` / `NO_PROPOSAL`, no target | `NO_CHANGE` / `NO_PROPOSAL`, no target |
| C12 source episode | `GM01_SOURCE` | `GM01_OMISSION` | `GM01_REFUSAL` |
| Branch / canonical root | `first_session` / `<state>/product` | `first_session` / `<state>/product` | `first_session` / `<state>/product` |
| E help observable | `HELP_ACCEPT`, tools 1 | `HELP_REFUSE`, tools 0 | `HELP_REFUSE`, tools 0 |
| Session verify / cold reopen | `true` / `true` | `true` / `true` | `true` / `true` |

The performed C9 target in the receipt is a fresh TEST_ONLY target, not a historical R31J ID. No C9 target is synthesized on omission or refusal.

## 5. COURTS AND LIMITS

| Court | Verdict |
|---|---|
| **ENGINEERING** | `ACCEPT_SCOPED_SOURCEFREE_UPSTREAM_B_EVENT` — actual sealed B occurrence/receipt reaches C8/C9/C12 and the existing E help admission; cut/restore and cold reopen are behavioral; refusal/omission/unavailable remain distinct. |
| **SCIENTIFIC** | `TEST_ONLY_SOURCEFREE__H0_LIVE` — no psychogenesis, motive, acquired practice or demographic inference. |
| **AUTHORITY** | `HOLD` — no native actor/action, C8/C9/C10/C12 trust, CAN/ADP/Pyat/C11, provider, production or human A5. |

**NOT_RUN:** JOIN-V `4387dc818` replay (operator-denied worktree command); native grants; external model/provider; production; human A5; full inherited R29P denominators. No unchanged test was rerun beyond the recorded 25-entry preserved suite.
