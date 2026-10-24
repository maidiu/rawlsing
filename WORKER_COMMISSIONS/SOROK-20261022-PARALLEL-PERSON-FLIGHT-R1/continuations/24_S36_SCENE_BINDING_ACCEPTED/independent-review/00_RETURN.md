# S36 access-scene defect closure — ACCEPT_SCOPED

Decision: **ACCEPT_SCOPED**.

## Exact cut

- Corrected candidate commit: `8da78d8031a06a4bd7e1297fd713e573299c0860`.
- Branch: `agent/rabochii-sorok-20261024-s36-actor-access-response-r1`.
- Prior rejected cut: `25fdc92bb9cac303c6f9a9b59add2d3fa9b0567c`.
- Base: `888ccae53ec02ca572cbb7ba208956e2c99170b9`.
- Reviewed in a disposable clone. No product edits, provider/model calls,
  controller-attachment edits, or native/science action.

## Corrected behavior

`candidate/actor_access_response.py` now refuses before commit when the access
witness scene is not a nonempty string (`S35_ACCESS_SCENE_MISSING`), the actual
event scene is not nonempty (`S35_ACCESS_EVENT_SCENE_MISSING`), or the two
scenes are unequal (`S35_ACCESS_SCENE_MISMATCH`). It retains the exact positive
path when the scene is exact.

## Reproduced checks

```text
PYTHONPATH=<S36 return>:<S36 return>/runtime/native \
  python3 -B -m pytest -q <S36 return>/tests -p no:cacheprovider
39 passed in 0.63s
```

Preserved reviewer oracle `SOROK_REVIEW/S36/oracles/s36_scene_binding_oracle.py`
was run against checkout `8da78d8` and returned **3 PASS / 0 FAIL**:
`scene_wrong` and `scene_empty` now `REFUSED` with no uptake/commit, while
`scene_exact` remains `RESPONSE_COMMITTED` with empty target proposals. The
oracle's static `cut` label names the prior target; the actual checkout used for
this run is `8da78d8031a06a4bd7e1297fd713e573299c0860`.

The 39 focused tests retain the positive exact-scene path, zero target
proposals, `CAN011 NO_CHANGE / NO_PROPOSAL`, targetless later consumer/no ghost,
missing access/response behavior, contradictory readset preservation, two-history
non-practice, and legacy behavior. No broad review campaign was reopened.

## Receipt

- 39-test output: `evidence/s36-8da-tests39.out` SHA-256 `f464d11c…`.
- Scene oracle output: `evidence/s36-8da-scene.json` SHA-256 `94f3ee0e…`;
  3 PASS / 0 FAIL.
- Corrected `actor_access_response.py` SHA-256 `987352a6…`; test file SHA-256
  `3fedc8cc…`.
- Preserved oracle SHA-256 `3c13550a…`.
- No provider/domain/native/production action was performed.
