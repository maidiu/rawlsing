# M13 — direct source map

**Court:** HISTORICAL_V3 / EXACT_MECHANISM; X03 independent source return, awaiting independent review. **Coverage:** PARTIAL_WRONG_MEANING

**Source identity:** X03 sealed startup `2647a4cf25d8bb33a00471e1af9c5e58c2825efb`; direct read-only files are hashed in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`. The S50-selected files are 31/31 exact. X03 files outside S50 were matched to `CAN_011_V3_MIDDLE_STATE/AUTHORITY.json`, `CAN_012_V3_RUPTURE_METABOLIZATION/AUTHORITY.json`, `CAN_010_V3_NEED_EXPECTATION_STRIVING/AUTHORITY.json`, `ADP_007_V3_ACTOR_INITIALIZATION/AUTHORITY.json`, or are explicitly local-source-only. The local staging zip `3f2c5ed9…` is not the TD-R05 archive `953c9149…`; archive-level exactness is not claimed.

**Claim ceiling:** historical source and sourcefree probe behavior at the cited grain. This is not current C9/C12 integration, a native person, a scientific law, or a source/actor/C8/C9/C11/C12/Pyat grant.


## Function and call-path map

| Symbol | File:lines | Inputs | Actual operation | State read/write | Callers/consumers | Test entry |
|---|---|---|---|---|---|---|
| `PracticeStack` | `v3/core/state.py:230–242` | six scalar practice fields | stores study/care/organizing/craft/spiritual/risk_training 0–100 | `practice_stack` | JSON; seed; update; flow | no acquisition test |
| `update_practice_stack` | `v3/systems/practices.py:19–40` | events_this_year, config | sums event practice_deltas by field; cap 15; clamps | `practice_stack` | yearly_step practice_and_infrastructure_update | test_step_logic::test_practice_stack_update_applies_event_deltas |
| `identity seeding` | `v3/io/identity_to_backbone.py:374–405` | religiosity, SES/class/age | spiritual=religiosity; study/care/organizing/craft/risk from SES base + age bonus | `practice_stack` | backbone_state_from_identity | no focused seed test |
| `event practice deltas` | `v3/engine/effects/delta_templates.py:94–96,161–219` | event kind/magnet labels | kind practice adds organizing/craft; magnet type/label adds study/craft/care/risk | `practice_stack` | run_llm_band / apply_deltas | test_wave4 shard tests only |
| `pressure-flow increments` | `v3/psyche/flow.py:500–541` | routed charge/channels | adds/subtracts practice scalars from routed psychic charge | `practice_stack` | run_pressure_flow_cycle after year | pressure-flow smoke |
| `dominance consumers` | `v3/io/persona_sheet.py:136–137,792–812,914` | practice_stack | job type, strategies, life snapshot | `persona surface` | V2 persona | test_wave4 persona presence |
| `update_domains` | `v3/systems/domains.py:50–56` | events only | ignores practice/framework despite step-order declaration | `domains` | yearly_step domains_update | domain event test only |

## What is actually run

- Practice is seeded from identity before any activity: spiritual equals religiosity; study/care/organizing/craft/risk_training use SES base values plus an age bonus (`min(20, (age-10)*1.5)` weighted per field). Probe: age-8 working -> study 25, care 30, organizing 35, craft 35, spiritual 80; age-40 middle -> study 55, care 26, organizing 19, craft 33, spiritual 50. The age bonus is arithmetic, not participation.
- The annual step only applies event `practice_deltas` with a cap of 15. With no events, the stack is unchanged. A single event can move organizing 40→50 and craft 50→45; there is no object, support, repetition, context, acquisition, transfer, or loss record.
- The LLM band and magnets can add practice from event kind or label (`practice` adds organizing/craft; mentor/teacher/arts/scene/romance/leader/care labels add selected fields). This is label-to-practice, not enacted history.
- The pressure-flow cycle also mutates practice from routed psychic charge, e.g. study/craft/care/spiritual/organizing/risk increments. This is an internal routing feedback, not an observed activity or support record.
- The domain step ignores practices despite `v3_yearly_step_order.yaml:218–229` listing practice_stack as an input; probe high/low practice produced identical domains. Practices do affect derived alignment/mis-aim, pressure-flow channel choice, persona strategies/job, and Pass 1 practices summary, so the carrier is not inert—but those are not actual acquisition.
- There is no support, access, object, repetition count, skill transfer, loss, or scope. A high seeded value is observationally indistinguishable from a high value produced by years of supported practice.

## Real affordance

- Persistent typed carrier and JSON persistence.
- Bounded event deltas and real downstream use in alignment, mis-aim, pressure-flow gating, persona and Pass 1.
- Probe confirms no-event persistence and event-driven changes.

## Source-level REDs

- SES/age/religiosity presets fabricate practice before activity.
- Label, route, or magnet increments are treated as practice.
- No acquisition, repetition, support, object, context, transfer, loss, or history.
- Domains ignore practice, contradicting the step-order contract.
- A single 0–100 scalar per category cannot distinguish ability, participation, support, and recognition.

## Tests actually covering this mechanism

- `test_step_logic::test_practice_stack_update_applies_event_deltas` — event delta only.
- No test covers acquisition, support, repetition, transfer, loss, or domain consumption.

## Probe evidence

Probe evidence: child/adult identity seeds above; no-event year unchanged; event delta changes; high/low practice leaves domains identical; pressure-flow source increments practice from routed charge.

## Identity and authority note

CAN_011 marks SES/age/religiosity practice seeds, active-magnet labels, and pressure-flow/gating increments as `REMOVE/REJECT` or `COMPATIBILITY_ONLY`. The source remains at compatibility grade.

The source files and hashes are in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`; the executable probe is `TEST_SOURCE_AND_LOGS/probe_x03.py` with output `probe_x03.json`. No production or source file was modified.
