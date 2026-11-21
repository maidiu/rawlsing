# SOROK REMONTATHON — R3 R4, provenance and money-flow first-fault repair

**Date:** 2026-11-19 (America/Chicago). **Immutable source parent:** REMONT PR #1171 @ `b29c3d28db66dc4439eb5899826289dd8b6ad6f7`. **Actual executable builder:** ORACLE R3 #1167 @ `3dba91136870ab5e766ca14faacd847531dea075`; historical SEAM Constitutive Person #1161 is documentary guidance, not a separate executable native authority. All work is an isolated sourcefree candidate, NOT a protected release.

## Reproduced before fixing (original code at immutable parent)

- **SR-P045 — state laundering:** After a direct, uncommitted SQLite edit to the canonical world or Nadia's actor state, `verify_chain()` correctly rejected the altered state. But the next ordinary `step()`, `cue()` or `seal_source()` appended a new event and then verification **returned `valid=True`**, silently admitting the unauthorized change as if historically caused. Fixed at the `ResearchLedger` write boundary: `commit()` and late `seal_source()` check the most recent committed event's exact canonical header/hash, single world, complete actor roster, world clock, and durable world/actor digests before mutations. Test covers actor/world, step/cue/seal; rejects before new event insertion.
- **SR-P046 — erased genesis laundering:** Erasing all events then calling `seal_source()` could create an internally hashed SOURCE_SEAL as a false first event and `verify_chain()` would report valid history. Fixed at two boundaries: every append demands a real original INITIALIZATION genesis and the full verifier demands the first event be INITIALIZATION and rejects repeated genesis. An adversarial in-test forged, hash-consistent SOURCE_SEAL event is also rejected. Neither a deleted history nor a missing initialized history is reconstructed from fiction.
- **SR-P047 — Boolean time:** Python treats `True` as `int(1)`, so `background(True)` advanced life and maturation one day. Fixed the independent ordinary-life clock interface to require exact `int` (1 to 3650).
- **SR-P048 — competing world genotypes:** A second `ConstitutiveRuntime` with another `world_id` could call `initialize` on a shared SQLite file, insert a second GENESIS and break the supposedly single chain. The existing research DB is strictly **single-world**; second genesis now raises `MULTIWORLD_RESEARCH_DB_UNSUPPORTED`. This is a conservative refusal, not a multiworld architecture.
- **SR-P049 — vanished monetary proceeds:** A successful `BUY_FOOD` from a workshop controlled by `workshop_steward` debited buyer funds but left the objectively identified seller's account unchanged; the money vanished from the modeled transaction. Now the site controller must be qualified, buyer and seller must have valid accounts, the payment is transferred and a typed objective FOOD_PURCHASE material claim is retained. Unowned home food cannot masquerade as a market sale; its legitimate shared-food `EAT` route remains intact. Additional positive/negative tests cover no seller, nonfinite seller balance, and buyer = seller.
- **SR-P050 — Boolean money:** `float(True) == 1.0`, so a Boolean price or wage could create an apparently valid economic transfer. The world monetary/material validation now refuses Boolean and nonnumeric values before writing objective consequences.

## Executed proof and limitations

Original 91-test sourcefree REMONT R3 was reopened and ran GREEN in normal and optimized Python. **Ten targeted RED tests/negative outcomes were executed against pre-fix code** (8 history/time and 2 material tests; the Boolean-money test has two red subcases). The repair adds **13 targeted regression tests total**. On the actual combined source tree:

- `python -m unittest discover -s tests -v`: **104 PASS / 0 FAIL**.
- `python -O -m unittest discover -s tests -q`: **104 PASS / 0 FAIL**.
- Relevant real source and test files: `storage.py`, `ordinary_life.py`, `world.py`, `tests/test_remontathon_r4.py` under `SEAM/ORACLE/UM_SOROK_ORGANISM_R3/`.
- Exact local `git hash-object` identities and runnable archive in `REMONTATHON_R4_FILE_IDENTITIES.json`; ZIP SHA-256 recorded in the final PR body after publishing.

## Custody and rights

P045–P050 are new **sourcefree author-repaired candidates**, not independently accepted production closures. They join the original 44 P identities without retiring or renumbering them. Accurate status breakdown: **50 P total = 10 OPEN/NOT FIXED, 6 PARTIAL, 34 AUTHOR-REPAIRED REVIEW-PENDING (0 independently accepted)**. The `SR-P020` historical R0 NOT_FIXED row is explicitly counted OPEN rather than mistaken for a FIX by substring. **0 confirmed T defects**, **6 outstanding E evidence/authority holds**. Earlier R1/R2/R3 receipts, source seals, and previous 62/84/88/91 test cuts remain historically distinct.

Still not solved: genuine psychological motive genesis, learned attention prior to named cues, source-qualified PYAT adult fidelity, full institutions and social reproduction, economically grounded employment/market behavior beyond this bounded sourcefree transaction, native owner P2–P6, CAN/ADP science, real LLM checks, independent receiving, production security, and canonical paired SOROK CURRENT_PROGRESS. Do **not** infer the isolated 104 tests prove whole personhood or scientific adequacy.
