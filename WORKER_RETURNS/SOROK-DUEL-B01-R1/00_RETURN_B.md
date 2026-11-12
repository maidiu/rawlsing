# SOROK B01 Agent B return

**Task:** B01 `Select existing material writer and bounded household state ABI` (CG-B).
**Grade:** `SOURCEFREE_S2_ONLY`; no native/science/actor/human/rights/merge authority.
**Branch:** `codex/sorok-duel-b01-b-20261112-r1`.
**Implementation SHA:** `160cbbd0ae00fb965004085c0e07c872384fe0ff`.
**Opponent HEAD:** `edbb4b344d54731a527fd415a965bc848ed964e1`.
**Full handoff:** `AGENT_B_HANDOFF.md`.
**Machine records:** `PROGRAMMA_DELTA.json`, `impact.json`; A records retained as `PROGRAMMA_DELTA_A.json`, `impact_A.json`.
**ABI revision:** `B01_ABI_B_REVISION.md`.

## FINDING

A selected the real S47/P2 checkpoint writer and produced a working cold, world-owned household reader. That survives. A real C12 fork nevertheless refused the copied household: the stored `branch` is establishment provenance, but A compared it with equality to the current child branch, and `P2Owner.material_fact` called full session verification, which refuses unrelated unforked S46/S47 state. Evidence against A's exact HEAD: `evidence/a_head_fork_refusal.log`.

## ACTION

Preserved A's source/binding split, schemas and cold behavior. Added read-only `branch_is_ancestor`; `read_household`, `parent_choice_input`, `P2Owner.material_fact`, `read_house`, `scene` and a real P6 `GO` now follow a verified C12 ancestor without rebinding source or writing. Same-branch `P2Owner.material_fact` is unchanged, including no `state_scope` key. Added world-resource value, bound-resource/owner severance, fork/foreign-branch/read-purity tests.

## EVIDENCE

- B01: **7 passed in 61.18s** (`evidence/b01_household_b.log`).
- P6 house: **8 passed in 163.14s** (`evidence/p6_test_house_b.log`).
- P6 MII: **18 passed in 231.99s** (`evidence/p6_test_mii_b.log`).
- P2/P6/P3 adjacent: **9 passed in 54.58s** (`evidence/adjacent_b.log`).
- A HEAD fork refusals: `evidence/a_head_fork_refusal.log`.
- A-era P3 root under B code: `P3_CONFIG_CHANGED` (`evidence/p3_code_pin_a_era.log`).

## LIMITS

`p2_owner.py` byte changes break A-era and pre-B01 P3 code-pin roots; no migration invented. B `house.py` requires B `p2_owner.py`; C01 must rebase both. Fork proof is in-process, not a cold fork reopen. `state_hash` is scoped on fork (`C12_FORK_WITHOUT_S46_INTERVAL_STATE`). Child P6 events retain parent house provenance. Same-root PsycheStore injection unproved. Parent first consumer remains `NONE_VERIFIED`. Two Library architecture records remain NOT_INSPECTED locally. Cost UNKNOWN.
