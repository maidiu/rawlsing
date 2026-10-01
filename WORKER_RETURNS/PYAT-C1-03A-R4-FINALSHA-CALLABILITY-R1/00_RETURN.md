# PYAT C1-03A — R4 FINAL-SHA CALLABILITY CORRECTION — R1

Status: `PASS_C1_03A_R4_FINALSHA_CALLABILITY_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`

Branch: `agent/opencode-pyat-hq156-c1-03a-r4-finalsha-callability-r1`
Commission tip: `b2b62c14f4b9a1ec7c97094a2d1ac4101f63314d`
Base / returned R4: `3bd481163ac1b2b1e30817b2704e89341099a960`
Code fix commit: `72ef80aef4ea4148b0814c9b89f3e5b6eb61a96d`

## Court

| Suite | Tests |
|---|---|
| `test_pre553_analytical_state_and_route.py` | 75 |
| `test_pre553_analytical_composition_higher_order.py` | 35 |
| `test_pre553_empirical_query.py` | 32 |
| `test_pre553_structural_admission.py` | 17 |
| `test_pre553_discovery_exact.py` | 14 |
| `test_pre553_analytical_composition.py` | 13 |
| `test_source_backed_positioned_subject_possibility.py` | 13 |
| `test_pre553_discovery_adaptive.py` | 8 |
| `test_pre553_discovery_adaptive_admission.py` | 3 |
| `test_pre553_recursive_handoff.py` | 2 |
| **total** | **212 passed, 0 failed, 0 errors, 0 skipped** |

Runtime 12.54 s, exit 0, run against a **clean tree identical to commit
`72ef80ae`**. R4 returned 208; +4 final-SHA callability courts, nothing removed or
weakened. **Only these ten files were executed — no broader sweep claimed.**

## The duplicate decorator was real. The TypeError was not.

HQ intake found a genuine defect: `from_empirical_integrity_refusal` carried **two
consecutive `@classmethod` decorators** at the returned R4 SHA, and predicted that
calling it raises `TypeError: 'classmethod' object is not callable`, contradicting my
208-pass claim.

I have to report that the second half of that does not hold up.

The duplicate decorator is definitely there — lines 853–855 of the blob at
`3bd48116`. I removed it: exactly one line, nothing else.

But I measured the predicted failure on **two** interpreters, and it does not occur:

| | Python 3.9.6 | Python 3.12.14 |
|---|---|---|
| `classmethod` object called directly | `TypeError` | `TypeError` |
| `Class.attr` on the nested chain | bound `method`, **call succeeds** | bound `method`, **call succeeds** |
| `classmethod.__wrapped__` present | no | yes |

HQ's error message is exactly right for calling the *descriptor object*. But normal
attribute access resolves the nested chain to a bound method on both versions. So on
the returned R4 SHA, with genuine witnesses:

```
from_empirical_integrity_refusal(witness=<genuine>) -> INTEGRITY_FAILURE
from_blocked_authority_refusal(witness=<genuine>)   -> BLOCKED_REQUIRED_AUTHORITY
```

**My R4 208-pass claim was accurate, and the integrity-refusal path was genuinely
exercised by that court** — `test_at14_integrity_failure_cannot_become_valid_empty`
calls it directly.

I could have just removed the decorator and let the report imply the bug had been
breaking the build. It wasn't, and saying otherwise would have been the easy
misreport.

## What the defect actually is

Real but narrower than reported: incorrect, needlessly fragile code, and a latent
portability hazard — not a live callability failure on the commissioned
interpreter. Worth removing, which is done.

## Four final-SHA callability courts

They call both refusal factories directly, assert the single decorator *structurally*
(no `classmethod` inside `__func__`), sweep **every** factory for a nested
`classmethod` so this cannot silently return on any method, and prove the two
mandatory refusal states remain distinct.

## Preserved

Refusal semantics, witness semantics, provenance, route law, AT15, AT16 and G5 are all
unchanged. No owner module and **no fixture** was modified. C1-02 untouched.

## Changed files

- `rawlsing_next/pre553_analytical_state_and_route.py` (one line deleted)
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py` (4 new courts)
- `WORKER_RETURNS/PYAT-C1-03A-R4-FINALSHA-CALLABILITY-R1/**`

## Non-claims

No raw sources. No merge. Not self-adopted.

## Terminal

`C1_03A_R4_FINALSHA_CALLABILITY_RETURNED__HQ_ADJUDICATION_REQUIRED`
