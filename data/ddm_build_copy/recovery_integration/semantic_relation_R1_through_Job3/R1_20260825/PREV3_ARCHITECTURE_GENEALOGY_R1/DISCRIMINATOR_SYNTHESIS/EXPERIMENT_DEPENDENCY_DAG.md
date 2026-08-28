# PRE-V3 EXPERIMENT DEPENDENCY DAG R1

Status: `DESIGN_ONLY__NO_ARCHITECTURE_SELECTED`

## 1. Existing prerequisite continuation

These are **not new discriminator experiments** and must not be duplicated:

```text
AS3R3 succession law daf4f79f...
        |
        +--> bounded successor producer cfc240aa...
        |          |
        |          +--> final 19 predicate + 3 query successor package [NOT YET ACCEPTED]
        |                         |
        +--> hostile oracle a1bbec8c... [FROZEN, AWAITS PACKAGE]
                                  |
                                  +--> AS4I0 successor adaptation preflight 49a58ffb...
                                                   |
                                                   +--> accepted C05R2B LiTS-I execution [NOT FOUND]
                                                              |
                                                              +--> C08 reconciliation -> historical G1 closure -> C09 launch sequence
```

LiTS-I source/C11 certification at `923f2c00...` is already accepted and is an input, not work to repeat.

WVS7 at `efca0824...` remains a separate fail-closed proving-source path and is not on the shortest path to the first LiTS-I discriminator.

## 2. Minimum discriminator DAG

```text
                    +-------------------------------+
                    | MX01 recursive topology       |
                    | common semantic closure       |
                    +---------------+---------------+
                                    |
                                    | common parity burden
                                    v
+-------------------------------+   +-------------------------------+
| MX02 component-vector         |-->| MX04 vertical DAG + seam      |
| common semantic closure       |   | physical discriminator        |
+---------------+---------------+   +---------------+---------------+
                |                                   |
                | common parity burden              | whole-machine physical-topology evidence
                |                                   v
                |                    [final architecture selection remains HQ-only]
                |
                +--------------------------+
                                           |
+--------------------------------------+   |
| MX03 Phase A LiTS-I C11 destructive |---+
| rebuild/replay parity               |   |
+-------------------+------------------+   |
                    |                      |
                    | physical parity gate |
                    v                      v
          +------------------------------------------------+
          | MX05 A/B/C lifecycle economics                 |
          | only after AS3R3+C05R2B+C08/G1+C09 launch law  |
          +------------------------------------------------+

C07 validation adoption + accepted learned release
                    |
                    +--> MX03 Phase B learned-product persistence
                    |
                    +--> MX04 positive learned-release branch

C07 comparability + PSEPF model adoption
                    |
                    +--> MX04 positive PSEPF branch where the fixture requests it
```

## 3. Parallelism

Wave 1 is deliberately parallel:

- `MX01`
- `MX02`
- `MX03_PHASE_A`

None depends on another and each fails for a different reason.

## 4. Why MX05 is last

`MX05` is not permitted to absorb MX01/MX02 as hidden benchmark tasks. If recursive topology or component-vector semantics require a common contract change, every A/B/C adapter must receive that same change before performance measurement.

The admissibility chain is:

```text
COMMON_SEMANTIC_CAPABILITY
-> NAMED_SOURCE_PHYSICAL_PARITY
-> FROZEN_ROUTE_COMMON_WORKLOAD
-> C09 EXECUTION AUTHORITY
-> PERFORMANCE
```

not:

```text
PERFORMANCE -> DEFINE_WHAT_COUNTS_AS_CAPABILITY
```

## 5. Full-C09 versus bounded engineering pilot

A LiTS-I-only engineering pilot can become executable earlier than a final C09 architecture verdict. The two must not be conflated.

A final C09 verdict remains subject to all still-binding proving-source and terminal-vision requirements, including WVS7 if HQ does not revise that law.
