# SOROK HQ313 OC6 — holds, owner map, changed paths and claim ceiling

## Claim ceiling

```
SOURCEFREE_TEST_ONLY_CUSTODY_PROTOTYPE_CANDIDATE__NOT_ADOPTED__
NO_REAL_ISSUER__NO_EXTERNAL_MODEL_USE__NO_ADOPTION
```

This return repairs six independently demonstrated input-contract families in a
**TEST_ONLY sourcefree custody prototype**.  It is a candidate only.  A distinct
independent **OC7 I2 review is required after this return**, and adoption remains
with the competent owner.

## What is NOT claimed

| Item | Status |
|---|---|
| Real independent institutional signer | **NOT CLAIMED** — all signatures are ephemeral TEST_ONLY fixture credentials with a transparent, publicly derivable verification root |
| Protected holdout corpus | **NOT ISSUED** |
| Durable externally anchored journal | **NOT ISSUED** — the escrow event seal is an in-process preimage anchor |
| Independently issued semantic oracle | **NOT ISSUED** — hash equality is not independent semantic agreement |
| Real semantic issuance / adoption | **NOT CLAIMED** |
| External model-use / privacy / spend grant | **NOT GRANTED** |
| Cross-process persistence (C07) | **NOT_REACHED** — absent an API |
| Original survey data | **NONE** |
| V3 / N12 / production / CURRENT / PRE-MAIN edits | **NONE** |
| Universal semantic non-leakage | **NOT CLAIMED** — `detect_leakage` is explicitly a lexical/schema gate |

## Owner / HOLD map

| Concern | Disposition | Competent owner / residual |
|---|---|---|
| OC4 capsule arrow / capsule source | **HOLD** | OC4 author (this return's candidate is a staged copy; the pinned dir is untouched) |
| OC7 independent review | **REQUIRED, not started** | HQ-assigned distinct I2 reviewer |
| Adoption / promotion of OC4 or of this repair | **HOLD** | competent OC4 semantic owner + Pyat HQ |
| Real independent custodian institution | **HOLD** | not issued anywhere in this repo |
| EE-class source / respondent permissions | **HOLD** | not in scope, not granted |
| OC5E excerpt/native staging gap | **CLOSED by OC5E** | superseded; not re-litigated here |
| The two malformed OC5E A2 inputs | **RESIDUAL** | OC5E author; see `01_` §`malformed_oc5e_inputs` |
| C07 cross-process persistence API | **HOLD (absent API)** | owner design decision required |

## Residuals to close before adoption

1. **Distinct independent OC7 I2 review** of this candidate, run against the
   same sealed closure.
2. **OC5E's two malformed A2 inputs** either corrected by their author, or
   formally recorded as superseded by the OC6 author controls that spell the
   tokens correctly (`test_a2_confusable_leak_token_spell_ref`).
3. **Owner decision on the boundary claim for A2**: this repair demonstrates
   *bounded, enumerated* confusable folding. It does not establish universal
   semantic non-leakage, and the return says so in code, in the passport and in
   `00_RETURN.md`.

## Changed paths

Only `WORKER_RETURNS/SOROK-R3-HQ313-OC6-NATIVE-INPUT-CONTRACT-REPAIR-R1/` is
written. No tracked path outside that prefix is modified. In particular:

* `WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/` — **read-only
  reference provenance**, never edited.
* Every inherited court file is `git hash-object`-re-verified against its pin
  after staging (7 direct blob matches, 2 sealed-archive member extractions,
  1 pinned source re-staged and then repaired).
* No test was rewritten, skipped, xfailed or special-cased; no `None`-capsule
  signature path was introduced to fake a green count.

## Environment (00D R1 passport)

| Field | Value |
|---|---|
| `passport_schema` | `SOROK_WARM_ENVIRONMENT_PASSPORT_R1` |
| `environment_id` | `opencode-muse-spark-local-dominant-sparse` |
| `surface` | `LOCAL_SHARED_STORE` |
| `status` | `LIVE_VERIFIED` |
| editor/host | OpenCode (existing Muse-configured installation) |
| model | Muse Spark, one agent, no Codex / DeepSeek-Harness / helpers / switch / paid calls |
| Python / pytest | 3.11.3 / 9.1.1, real `subprocess` + `--junitxml` |
| cash / quota | **UNKNOWN, not measured** — no owner telemetry was used |
| next affinity | eligible for a distinct independent OC7 I2 review; **not** eligible for any issuance, adoption or V3 wake |

Full machine-readable detail is in `environment_passport_delta.json`
(`claims`, `covers`, `staged_object_manifest`, `source_identity`).

## Verification performed by this worker

* Direct remote HEAD verified against the sealed startup before any edit.
* BEFORE-phase courts executed the **unrepaired pinned blob**
  (`imported blob is pinned blob: True`).
* AFTER-phase courts executed the **repaired blob**
  (`imported blob is pinned blob: False`, by design).
* The 349-case court is byte-identical in both phases.
* `repro/reproduce.py` re-runs stage → before → repair → after → adjudicate →
  passport end to end from a clean state.
