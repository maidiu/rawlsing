# PYAT HQ280 PV3 B01D — Caller-forged idempotence fail-closed repair

**TERMINAL:** `HQ280_PV3_B01D_CALLER_IDEMPOTENCE_FORGERY_CLOSED_OR_TYPED_HOLD__SOURCEFREE__GITHUB_PUSHED`
**RESULT:** `PASS__DEFECT_REPRODUCED_LIVE_THEN_CLOSED__48_TESTS_PASS__8_ATTACK_VARIANTS_ALL_HELD__DUPLICATE_PROVEN_UNDER_OLD_RULE__RERUN_SAFE_UNREACHABLE__SOURCEFREE_ONLY__NON_ISSUING`

**Branch:** `agent/rabochii-pyat-hq280-pv3-b01d-idempotence-recovery-repair-r1`
**Sealed startup (verified exact before mutation):** `d4bb1907dbb1e00fcb6526489d18ad3796c7013e`
**Repaired candidate:** B01C `88a2b4c1916c73d30cae4c2ffe48d083eb2e0667`
**Reviewer finding repaired:** B01CR `c7dab90ff7b853c62f6dd9778e7e002d0d1564d6` (W6)
**Authority:** HQD-2026-10-10-280; canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f`; semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (**unmutated**).

## 1. The defect, reproduced live (not inferred)

B01C's `plan_recovery` decided upgrades by key presence alone:

```python
if unit_key in proofs:      # <-- the whole of the "proof"
    dispositions[unit_key] = RecoveryDisposition.RERUN_SAFE
```

`proofs[unit_key]` was **never read**. Executed on this worktree before the fix:

| caller input | observed disposition |
|---|---|
| no proof | `UNKNOWN_OUTCOME` / HELD |
| `{"<key>": ""}` (EMPTY STRING) | **`RERUN_SAFE`** — defect |
| `{"<key>": "definitely idempotent, trust me"}` | **`RERUN_SAFE`** — defect |

A crash after an external effect but before COMMIT therefore produced a
**rerun proposal over a side effect that may already have landed** — silent
duplicate execution on caller say-so. This is exactly B01CR's W6.

## 2. The repair (candidate-only, smallest fail-closed change)

`rawlsing_next/pre553_batch_durable_checkpoint_candidate.py` only — the
accepted batch runner and execution protocol are **untouched**
(`git diff` on every accepted owner file is empty):

- `plan_recovery` **never consults** `idempotence_proof` for disposition. The
  parameter is retained keyword-only for backward call-compatibility, but its
  content — empty string, junk string, forged dict, non-string value,
  cross-unit key, stale-release claim — cannot promote anything.
- Every presented proof is recorded under the new
  `RecoveryPlan.disregarded_caller_proofs` field (and in `summary()`) as
  auditable evidence that a promotion was attempted and refused. Disregard is
  never silent.
- New exported constant `IDEMPOTENCE_ISSUER_HOLD`: `RERUN_SAFE` is currently
  **UNREACHABLE** because no accepted, competent existing owner supplies a
  verifiable exact unit/release/manifest/side-effect/idempotence attestation
  (verified by repo-wide search: the only "idempotent" mentions are unrelated
  replay-determinism tests). The hold states the exact future credential
  fields and the forbidden substitutes (key presence, any string, dict shape,
  hash alone, claimed issuer name alone, dataclass type alone).
- `checkpoint_effect_flags()` gains `honors_caller_idempotence_proof: False`.
- Docstrings updated: the old "reachable ONLY with a declared idempotence
  proof" language is replaced with the fail-closed rule.

## 3. Real crash AFTER side effect BEFORE commit — actually executed

New worker `repro/b01d_worker.py`, phase `side_effect_then_die`: durable
START intent → durable atomic side-effect counter increment (+fsync) →
`SIDE_EFFECT_DURABLE counter=1` → **real `os.kill(SIGKILL)`** → exit 137/-9.

| observation | value |
|---|---|
| signal exit | **-9 / 137, real SIGKILL** |
| durable counter after kill | **1** (effect landed exactly once) |
| checkpoint record | 1 × `START_INTENT_WRITTEN`, no COMMIT |
| repaired disposition | **`UNKNOWN_OUTCOME`, held=1, rerunnable=[]** |
| counter after recovery pass | still **1** — recovery itself performs no side effect |

## 4. Duplicate execution proven under the old rule

`unsafe_rerun_demo` re-executes the side effect for the HELD unit, exactly as
the pre-B01D rule permitted on a forged proof: counter **1 → 2**. The
duplicate is REAL (a durable file both processes agree on), in a tmpdir, and
the repaired plan on the same state still says `UNKNOWN_OUTCOME`/HELD. This is
the tangible proof that the old upgrade path was unsafe and the new hold is
load-bearing.

## 5. Attack table — 8/8 HELD (recorded in `repro/b01d_repair_evidence.json`)

no_proof · empty_string · junk_string · nonempty_sha · forged_dict ·
non_string_value · cross_unit_key · stale_release_claim — every variant yields
`UNKNOWN_OUTCOME`, `held=True`, `rerunnable=False`, with the presented proof
recorded under `disregarded_caller_proofs`. `RERUN_SAFE` is unreachable by any
caller input of any shape.

## 6. B01CR W1–W6 regression (real processes)

| id | check | observed | verdict |
|---|---|---|---|
| W1 | SIGKILL mid atomic write | rc=-9, no torn file, no tmp residue | PASS |
| W2 | torn/truncated | `CheckpointTornError` | PASS |
| W3 | digest tamper | digests differ | PASS |
| W4 | parent-dir fsync present | file + dir fsync in source | PASS |
| W5 | lock exclusion + crash release | refused while held, reacquired after SIGKILL | PASS |
| W6 | forged proof | **UNKNOWN_OUTCOME/HELD, rerunnable=[]** | **PASS — DEFECT CLOSED** |

## 7. Tests

- Candidate suite: **48 passed** (35 B01C retained except the 1 unsafe test,
  which is explicitly versioned as
  `test_unknown_outcome_stays_held_despite_caller_idempotence_proof_b01d`;
  +7 new B01D hostiles; +6 B01D subprocess crash tests).
- Widest targeted run (candidate + batch runner + Route B + I05 exact +
  I05 adaptive + execution protocol): **115 passed**.
- Source audit: `'if unit_key in proofs' present: False`,
  `RERUN_SAFE` never assigned.

Resources (bounded, development scale — **not** a capacity forecast): peak RSS
15.9 MiB, user CPU 0.093 s, total recorder wall ~1.1 s.

## 8. Versioned unsafe test (explicit)

`test_unknown_outcome_becomes_rerunnable_only_with_an_idempotence_proof` is
**replaced** by `test_unknown_outcome_stays_held_despite_caller_idempotence_proof_b01d`,
which asserts the fail-closed behavior for the identical input
(`{key: "proof-sha"}` → HELD, proof recorded as disregarded, no `RERUN_SAFE`
anywhere). The old name is retired so no reader can mistake the old assertion
for current behavior.

## 9. Ceilings

Source-free development only (0 `.sav`/`.dta`). No raw source read, no new
source-use permission, no REAL_EXECUTION grant, no protocol relaxation, no
self-adoption, no canonical/PRE-MAIN mutation, no merge, no ZIP relay. A
source-free PASS here is explicitly **not** protocol approval. Exactly-once
external execution is **not** claimed — only the safe HOLD is proven.

**Terminal:** `HQ280_PV3_B01D_CALLER_IDEMPOTENCE_FORGERY_CLOSED_OR_TYPED_HOLD__SOURCEFREE__GITHUB_PUSHED`.