# SOROK B03 Agent A return

**Task:** B03 `Commit selected inhabited dwelling/tenancy/noise/space/resource facts` (CG-B).
**Grade:** `SOURCEFREE_S2_ONLY`; no native/science/actor/human/rights/merge authority.
**Code:** `99333985190d872d825a1ec205db224179daa4af` (final tested tree; B03 feature commit `6deb7b71`) on `codex/sorok-duel-b01-a-relay-b03-20261112-r1`.
**Full handoff:** `AGENT_A_HANDOFF.md`. **ABI:** `B03_ABI.md`. **Delta/impact:** `PROGRAMMA_DELTA.json`, `impact.json`.

## FINDING

The actual P6 root now commits a bounded `p6_dwelling` material fact through the same S47/P2 checkpoint writer as B01. A concrete junior drum-kit request is `ADMISSIBLE` under the committed home/space/acoustics/tenancy/costs and live household cash; the acoustic kit is `REFUSED_NOISE` + `REFUSED_AFFORDABILITY`; prohibited tenancy, tight space and unknown acoustics produce `REFUSED`/`UNKNOWN` rather than a fabricated trait, possession, or mother action. The drum kit never appears as a house object.

## ACTION

Added `p6_dwelling` home/tenancy/space/acoustics/costs facts, `read_dwelling`, `commit_dwelling`/`establish_dwelling`, `material_feasibility`, and `mother_material_input` (`NONE_VERIFIED`). Preserved B's C12 fork inheritance, added P6 fork provenance, and strengthened B's shared-prefix check to verify actual copied rows rather than mutable `root_counts`. No purchase, calendar, mother decision, PsycheStore dwelling fact, class-to-trait rule, or new owner/scheduler/ledger.

## EVIDENCE

- B03 suite: 8 passed in 48.97s (`evidence/b03_dwelling.log`).
- B01 + A fork provenance: 11 passed in 74.88s (`../SOROK-DUEL-B01-R1/evidence/a_relay_b01.log`).
- B01 + B03 combined: 19 passed in 120.90s (`evidence/b01_b03_relay.log`).
- P6 `test_house.py`: 8 passed; `test_mii.py`: 18 passed (`evidence/p6_test_house.log`, `evidence/p6_test_mii.log`).
- Adjacent P2/actor/P3 subset: 9 passed (`evidence/adjacent.log`).
- Pre-existing chronology proof failure unchanged at baseline and this cut (`evidence/p6_chronology_pre_existing.log`).

## LIMITS

Mother decision/utterance and first consumer are `NONE_VERIFIED`; B02 calendar, B04 purchase/action, B05 duration remain future. Fork reads are material/C12-scoped (`C12_FORK_WITHOUT_S46_INTERVAL_STATE`), never full P3 composite; cold fork is not proved. Child new occupancy needs a future household re-establishment ABI. Prior-cut P3 code-pin roots are incompatible; no migration invented. Same-root PsycheStore injection and ancestor relabel remain attack surfaces. Cost UNKNOWN. The two Library architecture records remain NOT_INSPECTED locally.
