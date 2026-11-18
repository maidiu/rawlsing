# ANVIL routing joint scale gate

## Verdict

**`NO_EXISTING_SEALED_JOINT_FIXTURE__INPUT_GATE_FIRST`**

No existing authorized sealed fixture contains both substantial respondent count and actual populated width. The two existing estates are complementary, not combined:

| Fixture | Respondents | Questions | Build wall | Build RSS peak | Scratch peak | Retained |
|---|---:|---:|---:|---:|---:|---:|
| 10k/5-role | 10,000 | 5 | 210.423 s | 234,422,272 B | 535,740,432 B | 31,163,472 B |
| width128/600 | 128 | 600 | 293.956 s | 200,609,792 B | 826,683,762 B | 55,187,741 B |

Both individual builds fit the 600 s / 6 GiB / 4 GiB gates. A **joint 10k×600 build is not established**. No linear forecast or joint cap claim is made.

## First blocker

The first blocker is the **pre-run input gate**, not a measured cap: there is no sealed 10k×600 estate. The existing bounded writer can be invoked, but it would construct a new fixture:

```text
build_context(ShapeSpec)
→ build_width(ctx, 600)
→ write_direct_estate
```

No separate phase timing exists for the combined shape. The existing width writer is tied to a base `ShapeSpec`; the existing 10k builder hardcodes five questions. The 10k and width contracts therefore cannot be composed as a reusable sealed input.

## Concrete next command if authorized

```bash
python3 /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118/WIDTH128/build_width128.py \
  --snapshot <authorized-68aa-snapshot> \
  --out <new-authorized-combined-estate-root> \
  --respondents 10000 \
  --questions 600
```

This is a fixture-construction command, not an existing sealed input. It was **not run** here, under the no-new-fixture/new-benchmark constraint. It must be wrapped in the existing supervised caps if authorized, with no retry loop.

## Smallest next receiving step

Authorize either:

1. a bounded writer build of the 10k×600 combined sourcefree estate under the existing 600 s build / 900 s total / 6 GiB RSS / 4 GiB scratch / 8 GiB free caps; or
2. supply an already sealed combined 10k×600 estate contract.

No query or matched run can be scheduled from existing sealed fixtures alone.

## Source evidence

- 10k contract: `.../EXECUTION/fixture_contract_10k.json` (SHA-256 `d2a7ffa8…`), manifest `e192dc25…`.
- Width contract: `.../WIDTH128/fixture_contract_width128.json` (SHA-256 `89645891…`), manifest `4d9604dc…`.
- 10k build script: `.../EXECUTION/build_10k_estate.py` (`e953c466…`).
- Width build script: `.../WIDTH128/build_width128.py` (`32efbeb0…`).
- Width fixture: `.../ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117/width_fixture.py` (`8d9efbb7…`).

Correctness at `aee95429609c372564e996c2d3d3eb30e9253cbf` / receipt `bbc3114f70fa6948f4f3c6a55aa7d3cf5f23cef1` is not reopened.

## Limits

No new benchmark, query, fixture, product change, source/science/actor/CURRENT/protected grant, or linear joint forecast. Own return only.

**STOP for receiving authorization or a sealed joint input.**
