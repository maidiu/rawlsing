# PYAT C1-03R — ZERO-RELEASE CURRENTNESS CORRECTION — R3

Status: `PASS_C1_03R_ZERO_RELEASE_CURRENTNESS_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`

Branch: `agent/opencode-pyat-hq157-c1-03r-zero-release-currentness-r3`
Commission tip: `b77937f7f2c79e9007ff7d8cd19061d1758f7f15`
Base: `7f64493758f6b3b77d7e9ce1486c1324ff709edc`
Rereview: `agent/reviewer-pyat-hq156-c1-03r-r2-rereview-r1 @ 08b53e8b6` — `CHANGES_REQUIRED`

Sole blocker: **F-1**. All other R2 blockers independently approved; none reopened.

## Court

| Suite | Tests |
|---|---|
| `test_pre553_authority_maintenance.py` | 57 |
| `test_pre553_replay_audit.py` | 54 |
| `test_pre553_analytical_replay_dependency.py` | 43 |
| `test_pre553_analytical_composition.py` | 13 |
| **total** | **167 passed, 0 failed, 0 errors, 0 skipped** |

Runtime 52.50 s, exit 0. R2 baseline was 160. +7 F-1 courts; **no approved R2 court
removed, weakened or reopened.** Only these four suites were executed — no broader
sweep claimed.

## F-1 reproduced, then closed

Before the fix:

```
known dependent, zero releases -> CURRENT, governing_release_ref=None
resolve_current_analytical_product -> served it as a CURRENT analytical product
unknown ref (control)           -> NOT_GOVERNED  (already correct)
```

The reviewer's structural fact checks out: after any real release the owner computes
`A` and `U` over the same declared graph grain, so `A ∪ U` covers every known
dependent. A known dependent with no covering release is therefore reachable *only*
in the zero-release state — precisely where no release has established currentness.

That branch now returns typed `NOT_GOVERNED` with `reason_code =
NO_GOVERNING_RELEASE`, distinct from the preserved `OWNER_UNKNOWN_DEPENDENT`, so both
fail-closed cases stay auditable. `governing_release_ref` stays `None`; nothing is
fabricated. The resolver raises the existing typed not-governed failure, proven by a
direct resolver court.

**Currentness is no longer inferable** from `known_dependent_refs` membership,
cache/object/evidence residency, or absence of a transition. Both cache hostiles use
*genuinely resident* owner artifacts — a real sealed snapshot and a real recorded
evidence receipt — and still return `NOT_GOVERNED`.

## The docstring was stating the defect as law

The old approval law read:

```
* known but never transitioned -> CURRENT (the owner knows it and nothing governed it);
```

That is the defect written down as an owner rule. Corrected to `NOT_GOVERNED`, with
the reasoning that `CURRENT` requires a governing release and recorded outcome. A
reviewer finding the code and then the docstring contradicting itself would have been
right to call that a second issue.

## One wording residual I did not fix

`resolve_current_analytical_product`'s `NOT_GOVERNED` message says the ref "is absent
from the owner's known dependent set" — inaccurate for the zero-release case, where
the owner *does* know the ref. `pre553_analytical_replay_dependency.py` is **outside
this commission's write terrain** (permitted here only for a direct resolver court),
so I left it. The typed failure class is correct and the status mapping carries the
accurate `NO_GOVERNING_RELEASE`. Flagging it rather than reaching outside the terrain
for a one-line prose fix; HQ may wish to authorise that later.

F-2 (unknown extra top-level field dropped/unhashed) is recorded as a nonblocking
residual. No schema-version redesign attempted.

## Preserved

All approved R2 repairs green and untouched: Astra Option A, the single generic
noncurrent disposition, DEFERRED/UNAVAILABLE/DELETED refusal, error→noncurrent
prohibition, duplicate replacement rejection, negative-row schema fail-closed,
positive-only historical receipt identity, owner-unknown typed `NOT_GOVERNED`,
checkpoint affected/unaffected re-derivation, strict refusal of new-schema-with-zero-
noncurrent, sealed-successor repair, decoy correction, mixed AT19 topology, omitted-edge
hostile, shared promotion/rollback law, AuthorityCandidate identity, AT18 replay
grades. A targeted selection run over the preserve courts: **38 passed**.

`pre553_analytical_replay_dependency.py`, `pre553_replay_audit.py`,
`pre553_analytical_composition.py`, `pre553_analytical_state_and_route.py` and
`c1_at18_at19_fixture.py` all verified byte-identical. No fixture change.

## Changed files

- `rawlsing_next/pre553_authority_maintenance.py`
- `rawlsing_next/tests/test_pre553_authority_maintenance.py`
- `rawlsing_next/tests/test_pre553_analytical_replay_dependency.py` (one resolver court)
- `WORKER_RETURNS/PYAT-C1-03R-ZERO-RELEASE-CURRENTNESS-R3/**`

## Non-claims

No raw sources. No C1-03 join. Not merged, not self-adopted.

## Terminal

`C1_03R_ZERO_RELEASE_CURRENTNESS_RETURNED__HQ_ADJUDICATION_REQUIRED`
