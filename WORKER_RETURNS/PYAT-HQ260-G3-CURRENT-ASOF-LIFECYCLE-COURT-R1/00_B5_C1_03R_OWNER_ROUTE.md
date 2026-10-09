# HQ260 G03 — B5/C1-03R selected CURRENT/as-of owner route

**TERMINAL:** `HQ260_G03_RETURNED__NOT_ADOPTED`
**Route result:** `EXISTING_OWNER_POSITIVE_CONFIRMED__SERVICE_JOIN_PENDING`

**Agent:** existing DeepSeek-Harness/OpenCode source-free lifecycle worker
**Branch:** `agent/deepseek-harness-pyat-hq260-g3-current-asof-lifecycle-court-r1`
**HEAD at run:** `35a8e2c0da7d22d3f54badd5ddb9d5f1dec2e5f5` (startup base `cb5f363b…`)
**Live control:** `integration/pre-main-reconciliation-r1 @ 788b2bf7e53c35e25d3f83b638e989169f3d990c`
**Sealed HQ260 row:** `HQ260_G03_B5_C1_03R_CURRENT_ASOF` in checkpoint
`20261009-PYAT-HQ260-EE14-G0A-G1-G3-LITS-TEMPORAL-FOUR-ISSUED-R1 @ a39a4b2c…` — branch,
`commission_tip 35a8e2c0…` and `parent_sha cb5f363b…` all match.
**Runtime:** governed CPython 3.11.3, pytest 9.1.1, macOS 13.7.8 x86_64, isolated sparse shared-store
worktree, clean except the single new test file.
**No** Library/raw `.sav`/`.dta`, **no** G01 branch read, **no** production edit, **no** model-use or
issuer authority, **no** self-adoption.

## 1. Actual existing owner and first (only) route

The commission named the owner APIs; I verified them from the committed tree and used them
unchanged:

| owner | blob | role here |
|---|---|---|
| `LearnedProductLifecycleExecutor` (`rawlsing_next/pre553_learned_product_lifecycle.py`) | `a11c9eb73abab9be118ef4f0b6e325e676059f27` | selected CURRENT/as-of, checkpoint, invalidation |
| `resolve_current_analytical_product` / `transition_analytical_dependencies` (`rawlsing_next/pre553_analytical_replay_dependency.py`) | `47e65aad5e0a8df7af6fda72fc8807a002e556ce` | analytical-grain owner-unknown/noncurrent refusals |
| `AuthorityMaintenanceExecutor` (`rawlsing_next/pre553_authority_maintenance.py`, transitive) | `547e6bf20354f38179a0e2600de64c7cb2260ea0` | real owner used for the analytical refusal |

**First missing edge found: none.** The accepted B5 owner already exposes the complete route —
`stage_release` → `register_product` → `publish_product` → `selection_key` → `select_current` →
`resolve_current_as_of(as_of_event_ref=… | as_of_checkpoint=…)`, plus `supersede_current`,
`declare_invalidation`, `export_checkpoint` / `from_checkpoint`. It accepts an opaque
`LearnedProductLifecycleSubject`, so a **fixture-only** release/product identity satisfies it with no
producer or authority wiring. Therefore, per the commission, **no production adapter and no second
state machine were written**. The only change is one bounded source-free court:

`rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py`
(sha256 `122d8b6af2ecd431d8cdbc3db6971f5410933cde937b98203c1d53105f9618dc`,
git blob `a1ec3dba504ff866b681d6bbe942d12a9e238257`).

## 2. What the court actually proves (executed, not asserted)

`97 passed` combined, exit 0, in the governed interpreter on the clean committed SHA:

| court | result |
|---|---|
| new G3 court (`test_pre553_ee14_selected_current_asof_hq260.py`) | **15 passed** |
| existing accepted lifecycle owner court | **39 passed** (unchanged, no regression) |
| existing accepted analytical dependency court | **43 passed** (unchanged, no regression) |

The 15 G3 tests prove, at the fixture grain:

1. **CURRENT comes from the owner receipt.** `resolve_current_as_of(key, as_of_event_ref=…)` returns
   `CURRENT_SELECTED` with the exact selected release *and* the exact `receipt_ref` the owner issued;
   the same ref is returned by the owner's `current_selection_receipt_ref`.
2. **No cache/flag inference.** The release subject has no currentness attribute, and the executor
   exposes no `latest`/`current`/`default`/`newest` accessor; currentness is only obtainable through
   the exact-as-of resolver.
3. **Scopes/purposes do not bleed.** A second selection purpose resolves `UNKNOWN_CURRENTNESS`.
4. **Event and checkpoint agree** for the same scenario (same state, release and receipt).
5. **A tampered checkpoint is refused** (`LearnedProductLifecycleConflict`).
6. **Fresh-process reconstruction.** The checkpoint is exported, written to disk, and reconstructed
   in a **new interpreter process** (`subprocess.run([sys.executable, …])`); the fresh process
   resolves `CURRENT_SELECTED` with the exact release and receipt. This is the additive G3 evidence
   the existing in-process court cannot provide.
7. **Historical replay.** After `supersede_current`, as-of the earlier selection event still resolves
   the prior product A; as-of the later event resolves B.
8. **Affected/unaffected invalidation.** Changing determinant D1 marks exactly A and C affected
   (direct + transitive) and leaves the D2-only sibling B unaffected; current becomes `NO_CURRENT`.
9. **Typed stale refusal.** The invalidated release cannot be re-selected as current
   (`invalidated/withdrawn product cannot be selected current`), while its historical receipt still
   resolves the old product as history, never as current.
10. **Hostiles.** An unknown/fabricated selection key raises a typed
    `LearnedProductLifecycleError`; a fabricated "current selection receipt" is refused by
    `resolve_selection_exact`; a staged-but-never-selected release resolves `UNKNOWN_CURRENTNESS`,
    not current; the analytical owner refuses an absent dependent with `OwnerUnknownDependent`
    (never current).

## 3. Grade separation (what this is NOT)

- This is **local B5/C1-03R lifecycle capability**, proved with clearly-scoped
  `urn:hq260:g3:fixture:` identities. It is **not** an EE14/T1 selected-service use, not a model-use
  grant, not an issuer/AT07 principal, not native F7, not actor/V3, and not a pair or temporal
  authority.
- Test-created `ExactRef`/`AuthorityRef` values are identities for a state machine, never authority;
  the court defines no permission-issuing surface and the owners expose none.
- The G3 requirement's **service join** (the actual selected service consuming the selected current
  product through the T1 serving route) remains pending on G0b/G1 — see
  `02_G3_SELECTED_GRADE_GAPS.md`.

## 4. Integrity

- Production blobs `a11c9eb7…` and `47e65aad…` are byte-identical to the commission-named blobs and
  were **not modified** (`git diff HEAD -- <owner>` empty).
- Change surface vs the commission tip: exactly one new test file (plus this return directory).
- Sparse extension beyond the two named owner modules is listed in `01_…json`; it is the owners'
  source-free import closure plus two retained synthetic-authority fixture artifacts and the
  `c1_at18_at19_fresh_process_runner.py` helper that the **existing** analytical court requires.
  No raw source, no Library.

**Terminal:** `HQ260_G03_RETURNED__NOT_ADOPTED`.
