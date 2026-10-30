# G17 — reproduced original tests, JUnit and faults

Observed FINDING: the original reviewer cut is exactly 11 PASS / 3 RED; the three REDs are real material-owner, nested future-child and C9 source-authentication bypasses. Causal INTERPRETATION: the author paths authenticate only partial bindings; they do not authenticate the owner-canonical material event or recursively partition the visible input. Proposed HQ ACTION: review the separate candidate overlay and the three same-assertion repairs; do not merge or adopt. Accountable OWNER: original G17 author, C9 owner and a separate source-qualified reviewer appointed by incumbent HQ.

## Environment and exact cuts

Local macOS x86_64, Python 3.11.3, pytest 9.1.1. Base worker HEAD at launch `a9291cf6…`; sealed startup `342164a0…`; PRE-MAIN pin `299f41e9…`. Author cut `90d0eb79…`; reviewer cut `156b84cc…`. All runs used `PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1`. No original source, raw survey, PR514/516/519 or PRE-MAIN was modified.

## 1. Original reviewer baseline — 11 PASS / 3 RED

Reviewed test blob: `83f17006b22271f17c87f4563608de08395d7a1c` (byte-identical to the pinned original). Run against the reviewer `target_candidate` (author blobs `c9318dcf…`, `fc954993…`, `47e59c12…`):

```sh
python3 -m pytest tests/test_g17i_independent.py -q --junitxml=.../g17-baseline.xml
```

Result: **11 passed, 3 failed, 0 errors, 0 skipped** in 1.53s. JUnit SHA-256 `c2781f7405bea386e9675bb09a36666ea4ae766bf2123d4361b970772bfea24d`; log `85ee84133d758384deb304fd81bd4b5d36f1272bfbeced7892ff79f3d654afcb`.

Exact failures:

1. `test_forged_material_event_supplying_cash_must_be_refused` — `continue_person` returned `PARENT_CONTINUATION` with cash **100058** for forged material `sha256:bbfb9d35d90851fa5e6b168b27baf612cc158ce54d7e9f2227fc42568ae862d6`.
2. `test_future_child_nested_alias_must_be_refused` — `assert 'COMMITTED' != 'COMMITTED'`; nested `metadata.future_child_personality=NESTED_ALIAS` reached COMMITTED.
3. `test_c9_forged_material_event_must_be_refused` — `DID NOT RAISE C9Refusal`; receipt `ACCEPTED` with cash **100055**, handoff `sha256:ed58fb443bc5409ee3dbd2bbd4fd1e96432fcadecc6631f94f7b11c8c924b33c`.

Exact before-state details are preserved in `evidence/06_ORIGINAL_RED_DETAILS.json` (SHA-256 `f107706085d1b544b2224c1086bac03ad1eb9377e1102db76f44a63dd434fb4b`).

## 2. Patched candidate — same assertions, 14/14 PASS

Candidate overlay: three files under `candidate/` (hashes in `01_SOURCE_PATCH_AND_ORIGINAL_REDS.json`). Applied only to the temp target candidate; original author/reviewer cuts untouched.

```sh
python3 -m pytest tests/test_g17i_independent.py -q --junitxml=.../g17-patched-green.xml
```

Result: **14 passed**, 0 failed/errors/skipped in 0.78s. JUnit SHA-256 `40f764f231e0e6ff7174b964ae7998cfa849adbc005902baa980f1088b16d6fb`.

After-state: forged material returns `None`; nested alias returns `FUTURE_CHILD_INFORMATION_LEAK` with leak field `future_child_personality`; forged C9 material raises `C9Refusal("MATERIAL_SOURCE_NOT_AUTHENTIC")`. Details: `evidence/07_PATCHED_AFTER_DETAILS.json` (SHA-256 `32f660b0154e6890b6168fa40638705fbfd20a8fe8ae460fade6ffc7617bb92a`).

The exact three original assertions were not weakened, skipped, xfailed or rewritten. The original test file remains byte-identical.

## 3. Original author positive — 13/13 PASS

Applied the same overlay to the author’s own `candidate/` and root C9 file, then ran the author court:

```sh
python3 -m pytest tests/test_g17_material_history_consumer.py -q --junitxml=.../g17-author-patched.xml
```

Result: **13 passed**, 0 failed/errors/skipped in 0.62s. JUnit SHA-256 `99134f112401a2a47bed9cace60de5e1b45abbb35f9910682d1f6ba65667c537`.

## 4. Cold-process replay / severance / C9 consumer

The reviewer and author courts were rerun in fresh Python processes (no shared test state): reviewer **14/14** in 0.87s (JUnit SHA-256 `e2ae1b651e9baae4f75144e3865341780970ff83044d66596722850cbd48e6a6`); author **13/13** in 0.54s (JUnit SHA-256 `d4c6a2582ebb2f08fbd83776bf05363306de291117dbba24665176399f0a994a`).

`test_c9_material_handoff_genuine_and_severed` passes: the genuine handoff reaches the same `receive_handoff` consumer with `ACCEPTED`; removing the material causal parent raises `SEVERED_MATERIAL_SOURCE`. `test_c9_forged_material_event_must_be_refused` now raises the typed refusal. Full C9 E1/RULE_A/RULE_T/E2 is **NOT_RUN / HOLD_UNISSUED**; no C9 durable store or native consumer is claimed. This is a cold-process replay, not a durable C9 reopen; that layer remains held.

## 5. Original corpus and authority boundary

Tests use sourcefree synthetic histories, labor/material fixtures and frozen author/reviewer code only. No original survey/respondent corpus, no native Rule A/T, no M2/MP fabrication, no C11/C12 weld, no child/person generation, no PR519/514/516 or PRE-MAIN mutation. M2 and MP remain typed coverage HOLDs; native actor/science authority remains with the original owners. No self-review or adoption.

DONE: exact original 11/3 reproduction, three same-assertion repairs, 14/14 reviewer, 13/13 author, cold-process replay, C9 positive/severed/forged checks. REMAINING: original owner/reviewer replay and owner disposition. CRITICAL BLOCKERS: none for the bounded engineering patch; native C9 E1/E2, M2/MP, Rule A/T and person authority remain HOLD. LARGEST PRODUCTIVE MOVE: original G17 author replays the three patched blobs at `90d0eb79…` and C9 owner reviews `receive_handoff`. FLIGHT: sourcefree local Git/Python only. DELTA: the three original REDs are closed under their original assertions while all known holds remain explicit.
