# AT17/N10E SUCCESSOR REQUALIFICATION + C1-03 LARGE JOIN RERUN — R1

Status: `PASS_AT17_SUCCESSOR_REQUAL_AND_C1_03_JOIN_RERUN__INDEPENDENT_INTEGRATION_REVIEW_REQUIRED`

Branch: `agent/opencode-pyat-hq166-at17-requal-c1-03-join-rerun-r1`
Commission tip: `02ab67856243e19cd34539155729bbb9eca49ace`
Base: `8b2c45d754a0ff3922a7b60c510c9e96df995bc5`
Final commit: `933a3d31aa961719c73e6ce7eebcfe40bc8cd45e`

One combined job, as commissioned.

## Final court

| | prior | now | delta |
|---|---|---|---|
| accepted union | 413 | 426 | **+13** (provider successor courts) |
| join-specific | 22 | 28 | **+6** (successor integration) |
| **total collected** | **435** | **454** | **+19** |

```
454 passed, 0 failed, 0 errors, 0 skipped   exit 0   79.26s
```

Clean final tree, file list constructed from the filesystem with an existence
assertion. The old provider surface was **not** reduced to keep counts tidy.

## Phase 0–1 — lock and merge

Branch base, historical join commit and all five frozen blobs verified exactly. I
**reproduced the historical failed run locally** — 434 passed / 1 failed — and it
remains historical failed evidence, not relabelled.

The HQ-adopted successor spine merged ancestry-preservingly, **zero conflicts**. The
full oracle package merged (not just two digest strings) and **zero production files
changed**.

## Phase 2 — historical R8 preserved, asserted stronger

The failing P7 court conflated two different things. Split into two:

- `test_p7_historical_fixture_law_bindings_still_hold` — every fixture-law binding the
  R8 spine recorded (universe, release, query authority, predicate + hash, producer and
  consumer queries, 16-field witness, evidence ref, denominator) still holds.
- `test_p7_historical_r8_composed_identity_is_preserved_as_historical_only` — the
  historical digest is **re-derived from the pinned 38-field historical preimage in both
  directions** and proved **distinct** from the current C1-02 identity.

Nothing deleted, skipped, xfailed or weakened. The historical claim is now *stronger*
than the original, because it reproduces from the preimage rather than trusting a
recorded string.

## Phase 3 — both directions requalified

Production `composition_result.identity_material()` canonicalizes to the adopted
successor preimage with **zero field mismatches across all 44 fields**, forward and
reverse. I compared the **complete preimage**, not just the digest — a digest match
alone would have been insufficient evidence.

```
forward  01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd
reverse  a3bd7e85ae14babb5ac5a12b0bcc57a8cdf3eccf8f43394895903dc43aca40ca
```

Expected truth comes **only** from the adopted oracle package. Production is compared
against it and never defines it — no field was fitted to production output.

Forward: denominator 60, cells yes=54/no=6, exact fraction 9/10, `EXACT_SUPPORTED`.
Reverse: denominator 62, cells P1=54/P2=8, exact fraction 27/31, `EXACT_SUPPORTED`.

## Phase 5 — provider suite 30 → 43

P7 split (+1) plus twelve successor courts: historical preservation both directions,
full preimage equality both directions, digest equality both directions, wrong-direction
failure, six-field omission, six-field wrong value, and old-R8-cannot-masquerade.

## Phase 6 — join suite 22 → 28

All 22 historical join courts rerun and green, plus 6 successor integration courts. The
real AT17 composition dependent used by lifecycle integration carries the **current
successor** identity (`01c381d3…`), not the historical `03610f9d…`. A retained
historical R8 ref stays `NOT_GOVERNED / OWNER_UNKNOWN_DEPENDENT` and the
current-product resolver refuses it — historical evidence does not become current by
existing. Mixed outcomes, mutation, atomic rollback, checkpoint replay and both
fail-closed lifecycle cases unchanged.

## Phase 7 — replay grades and the known limitation

All four replay grades stay distinct; AT17 fresh-process provider replay, R
checkpoint/replay courts and the join-specific fresh-process lifecycle reconstruction
all ran. The known limitation stands **recorded, not fabricated**: there is still no
accepted single fresh-process bridge carrying provider recomputation → named consumer →
lifecycle restore. No concrete reason it blocks acceptance was found at this grain, so
it remains nonblocking and is referred onward rather than invented.

## Phase 8 — production conservation

All five accepted production blobs byte-identical. **Tests/fixtures terrain only**;
no owner mutation was required or made.

```
pre553_analytical_state_and_route.py      3a5e3db8a0897900d0b2606813bda7c3f586d46e
pre553_empirical_possibility_provider.py  23167aa25291fb148b1e3cf210ac33fe7769b783
pre553_authority_maintenance.py           547e6bf20354f38179a0e2600de64c7cb2260ea0
pre553_analytical_replay_dependency.py    47e65aad5e0a8df7af6fda72fc8807a002e556ce
pre553_analytical_composition.py         604c8d591d4cc2b646e9b149cdb233fc9d69cf6b
```

## Process note

I mistyped `pre753` for `pre553` again in a throwaway helper line, and separately
guarded the final run by generating the file list from disk with an existence
assertion — the failure mode that previously produced a silent "no tests ran" false
green. Phase 9 uses the asserted list.

## Non-claims

Not self-adopted. No control merge. No C1-R. No Omega-1. No C4/live production. No
raw sources. No C7. No PRE-V3→V3 actor/person work. The historical 434/1 run is
preserved as failed evidence.

## Terminal

`AT17_SUCCESSOR_REQUAL_C1_03_JOIN_RERUN_RETURNED__HQ_ADJUDICATION_REQUIRED`
