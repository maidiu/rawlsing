# SOROK HQ313 OUT8 — restored ACK and revoked historical viewer repair

**Disposition:** `IMPLEMENTATION_RETURNED__TWO_OUT7_RESTORE_DEFECTS_REPAIRED__SOURCEFREE_ONLY__I2_REQUIRED__NO_ADOPTION`.

**Sealed startup:** `862b5c6b427e1fb5d1a6000f9faf1c8352987d20`. **OUT6 source pin:** `673233571b7d899c309dd26f9b9cd2508404c0b6`, imported Python Git blob `aa002cb634e81cb980820c14220a1ab55bc5e015`. **OUT7 reviewer pin:** `d3d0836d922dcb88eaf0a0591e66551aa6fb9f0a`.

## Actual Python execution (all original tests unchanged)

| Suite | Original, pre-repair | After OUT8 |
|---|---|---|
| Original 137 | 135P / 2 historical RED | 135P / 2 historical RED |
| Exact OUT3 independent 22 | 22P | 22P |
| OUT4 29 | 29P | 29P |
| OUT6 18 | 18P | 18P |
| Exact OUT7 independent 21 | **17P / 4 NEW RED** | **21P** |
| OUT8 new actual-entrypoint 20 | NOT_RUN | **20P** |
| **Combined** | **221P / 6RED / 227** | **245P / 2RED / 247** |

Actual complete combined pytest runs, zero errors/skips, exit 1 solely because two original REDs persist. Actual postrepair source Git blob `331840768ce0b5f6f73e5e93094ca0d217ddaebf`; actual new 20-test file Git blob `d23e6cfc441de6fee11855966b16cc7ba6fd544a`. `OUT8_REPRO_SOURCE_AND_TESTS.tar.xz` contains a unified patch from exact OUT6 Python, exact 20 new tests, and reproduction instructions (Git blob `f6f54252e3faff80cf1321937bf306446db76a77`).

## Two restored-state defects corrected

1. **Forged global terminal ACK** (OUT7 I08/I13): a viewer-bound aggregate `ACKNOWLEDGED` state now requires at least one historical `ACKNOWLEDGED` client receipt for **that same occurrence**, belonging to an active or formerly authorized revoked viewer. Prevents global ACK_count=1 while only clients remain DELIVERED_UNACKED/ACK_count0. This is receipt internal congruence, *not* human perception or independently trusted client delivery.
2. **Forged revoked zero-attempt viewer receipt** (OUT7 I09/I14): a receipt for a revoked viewer must record at least one prior attempt, so a forged `revoked_viewers` tombstone cannot create an impossible `NOT_SENT`/attempts0 historical receipt, even in a rehashed cold journal. An **active** viewer `NOT_SENT` placeholder remains fixture-compatible to preserve original OUT6 `test_failed_not_sent_state_not_fabricated_by_client_fail`.

Failed restores remain failure-atomic through existing detached validation, and real new cold process tests exercised `Journal.recover()`, unkeyed digest rewrite, and `os._exit(79)` before/after rename. Twenty newly authored tests passed and both repaired OUT7 counterexamples passed unchanged. The first overly strict attempt caused a regression, was corrected, and the full 247-case rerun verified the final bounded rule.

## Scope and evidence honesty

Two untouched **historical REDs**: frozen S27 test demands unissued physical mug movement (owner MISSING), and stale multiwriter journal overwrite (outside single-writer grant). **OUT5's unpublished exact 14 tests were NOT reproduced.** OUTP L1/L2 legacy fixture admission and A1/A2 ACK/opportunity policy remain competent-owner **HOLD**; this patch does not rule on them. No production ADP019 signer/issuer, human perception, external trusted journal integrity, real model/actor, multiwriter warranty, V3 or canonical/PRE-MAIN/CURRENT mutation.

**Evidence custody:** Full local 247-case evidence archive, 227-case baseline JUnit/stdout, full per-case JSON matrix, original source bytes and recorded import path, source/test SHA receipts exist in the delivered conversation file `OUT8_EXECUTED_EVIDENCE.tar.xz`. The *pushed* smaller source reproduction archive contains patch+new test+commands. Do not claim the full local archive or full matrix is in GitHub unless separately published and verified. Independent I2 OUT9 is mandatory.
