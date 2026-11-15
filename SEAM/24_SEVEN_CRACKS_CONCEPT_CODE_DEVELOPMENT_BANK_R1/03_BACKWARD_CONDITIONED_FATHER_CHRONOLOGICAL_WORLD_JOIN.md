# SC-03 — Backward-conditioned father, independent past, one causal world

**Status:** SEAM/20 inverse order **PRESERVED**; father conditional support and historical admission **OPEN**. **Connects:** [index](00_INDEX_AND_REVIEW_PROTOCOL.md) · [SC-02](02_MATERNAL_OBSERVATION_INVERSE_HISTORY_AND_FIRST_CONSUMER.md) · [SC-04](04_PARENTAL_CONTINUITY_SAME_ONTOLOGY_MULTIACTOR_AGENCY.md) · [SC-06](06_ORDINARY_LIFE_PROCESS_AND_CAUSAL_COVERAGE.md). Governing: [SEAM/20 ``0,3–5](../20_SEAM_GENERATIVE_PARENT_ICEBERG_COMPRESSED_ONTOGENESIS_R1.md), [SEAM/23 `2/4](../23_C5_SHADOW_GRAVITY_MATERIAL_CARE_COVERAGE_ATTRACTOR_TEST_R1.md).

## The actual model—DO NOT invert this inversion

The mother exists first **computationally** as a source-conditioned, independently historically generated person. Her actual life supplies multiple feasible encounter alternatives. One eligible encounter is selected. The father is then generated **backward-conditionally on that selected intersection AND the selected branch's eventual child birth**; his in-world history is causally earlier, even though the software constructs it later.

The father must be a genuinely different person: his own demographic/material/response cloud (source-graded), his own compressed pre-encounter life under the same CAN/ADP developmental ontology, his own actor-local interpretations and projects. **He is not sampled forward as an unrelated person whom a simulator is then obliged to match to the mother**, and he is not reverse-engineered to agree with her psychology.

The stipulated branch birth is a condition of this **candidate-story construction**, not evidence that all couples reproduce, that all eligible encounters create a relationship, or that PYAT measures couple-level likelihood. ADP-015 maintains encounter ≠ relationship ≠ household ≠ parenthood ≠ child-generation ≠ child initialization. Others can be caregivers; biological father need not share household.

## Why this deserves its own concept/code record

The severe engineering problem is **two chronologies**. Father construction happens after a mother-world trajectory has been generated, but father's earlier actions might have world effects: moving, working, acquiring property, participating in institutions or changing someone else's possibilities. A timeline-coherent private biography is not sufficient if its events conflict with the already constructed objective shared world.

Conversely, simply forcing all pre-encounter father acts to have zero world effects would hollow out his independence and violate Z's material generativity. The goal is a **candidate historical reconciliation** with immutable commitments and bounded uncertainty, not global retroactive rewrites or a magical historical merge operation.

PYAT's F7 temporal and F6 nonpooled discipline, positional/region/institution and opportunity qualification constrain eligibility; SOROK's actual P2/ADP-015 chronology and actor-specific states own admitted fictional effects. One sourceful mother–father couple probability **cannot be fabricated from two WVS respondents**.

## Existing relevant authorities/source, graded

- [ADP-015 relationship/household/genealogy](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W2_AUTHORITY_CONTRACT_COMPLETION/ADP_015_V3_RELATIONSHIP_GENEALOGY/AUTHORITY.md): independent histories, separate perceived-other images, objective relationship and household; historical semantic law, not a working father sampler.
- [ADP-020 causal randomness](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W0_AUTHORITY_FOUNDATION/ADP_020_V3_CAUSAL_RNG/AUTHORITY.md): named causal streams; no hidden `first eligible father` or random branch perturbing mother's frozen history.
- [`model_cycle.RecursionCycle`](https://github.com/maidiu/rawlsing/blob/ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9/WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/model_cycle.py): ordinary P2 engine batch preserves root/actor/branch and refuses clock regression; **not a demonstrated multi-actor historical merge**.
- [`p2_owner.P2Owner`](https://github.com/maidiu/rawlsing/blob/ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9/WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py): bounded sourcefree event admission; check historical state/branch contracts before proposing any father-backhistory writer.
- [PYAT `pre553_universal_world_binding.select_world_view`](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/pre553_universal_world_binding.py#L227): refuses mixed source units (`CROSS_UNIT_LINKED_QUERY_UNAVAILABLE`), unsupported context structural authority and unobserved temporal pair. It cannot be called a linked couple creator.

## Proposed candidate-stage architecture (not current API)

```text
COMMITTED MOTHER: frozen actor history H_m, world-as-of snapshots W_m(t)
  -> SOROK encounter proposals from her actual trajectory
  -> world/eligibility owner checks t_E, location, institution, access, role,
     network/rights; retain MULTIPLE eligible and refused alternatives
  -> select E with named causal stream

FATHER INVERSE CANDIDATE (not yet shared-world committed):
  -> PYAT candidate F observable/cloud conditioned on E and stipulated B
     [SOURCEFUL support only if actually identified; else TEST_ONLY SCENARIO]
  -> SOROK construct independent H_f over t < t_E in isolated candidate scope
  -> validate father's work/place/role/care/resources/actor state as-of t_E
  -> reconcile objective past effects with FROZEN mother/world history:
       time/order, ownership/currency, institutional events, overlap,
       any encounter effects on mother, named RNG, causal ancestry

  -> ACCEPT candidate if it coexists under exact world/branch contract
     OR REFUSE / produce another independent candidate, never rewrite H_m
  -> jointly establish two separate actor roots and objective E event
  -> forward continuation: distinct actor states/perceptions + actual events
  -> relationship/household/child generation admitted SEPARATELY
```

**Possible reconciliation strategies to compare, not decree:**
- Candidate father history can reference shared earlier world facts without re-enacting them.
- A father candidate may have actor-local earlier activity with bounded effects on world facts that do not conflict with the frozen mother-world history; the competent owner must prove admissibility, not merely string equality.
- If both histories would require mutually incompatible changes to already committed world history, refuse this candidate, or branch to an **uncommitted** alternative mother-world construction with its own provenance. Never silently mutate the accepted mother.
- Do not materialize father-specific earlier events by appending them at t_E and lying about their performed time.

This is a proposed **world/history admissibility** obligation under existing owners, not permission to install a general retroactive event store.

## Hostile counterfactuals and acceptance evidence

1. **Impossible co-location:** mother intersects father at workplace at time t_E but father candidate has incompatible location/work constraint. REFUSE, no LLM relocation.
2. **Independent alternatives:** two plausible fathers satisfy t_E/B, retain different possible prehistories. Selecting one leaves unchanged mother H_m and other candidate fates.
3. **Shared-history contradiction:** father past requires a world effect that contradicts a sealed mother-world fact. Refuse or reconstruct a distinct uncommitted candidate branch; never graft silently.
4. **In-world vs computation order:** father can be created later in software while having chronologically valid earlier event parents; no clock rollback or double event.
5. **Separated relation:** encountered father never co-resides; household/carer structure independently governed. No forced marriage or nuclear family.
6. **Birth condition epistemic:** branch selected for eventual birth, but no empirical couple/birth likelihood exists. Retain `SOURCEFREE_CONDITIONAL`; do not claim population frequencies.
7. **Cold root and named RNG:** restore and replay do not change maternal earlier state due solely to father search.

## Decisions/questions to hand back

**UM-PYAT:** what exact coadministered adult and external time/place/role sources (if any) bound a father candidate at `t_E` and `t_B`? Which cross-source joins must remain F6 partial-ID? What is *conditional possibility* versus observed matching frequency?

**UM-SOROK:** where is the current owner of *candidate, uncommitted historical world effects*? Can the existing P2/branch/ADP-015 contract reconcile two earlier biographies without general past insertion? What minimal acceptance receipt distinguishes a real linked earlier world from two prose biographies?

**Depends on SC-02** for sealed maternal H; **feeds SC-04** continuing parental coagency and **SC-06** later household/care world. **Status:** plausible necessity; no claimed admitted backward-produced father or successful shared chronology run.
