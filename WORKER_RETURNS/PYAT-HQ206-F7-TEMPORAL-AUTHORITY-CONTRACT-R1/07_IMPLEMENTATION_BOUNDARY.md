# 07 — Implementation boundary

Lane: `PYAT-HQ206-F7-TEMPORAL-AUTHORITY-CONTRACT-R1`
Role: documentary authority-contract worker — Space Bunny Max or High
Status: **CONTRACT_DERIVED__NOT_ADOPTED__AWAITING_INDEPENDENT_REVIEW**

## What this return is

A documentary authority-contract derivation. It converts the F7 forensic
candidate into an explicit current authority package, defines the positive
temporal relation form it authorizes, and closes the bare-string
`TEMPORAL_NONCOMPARABLE` defect at contract grain.

## What this return is NOT

It is **not** an adoption, **not** an implementation authorization, and **not**
a code change. No production code accompanies this return. `git diff` against
the commissioned tip touches only `WORKER_RETURNS/PYAT-HQ206-F7-TEMPORAL-AUTHORITY-CONTRACT-R1/`.

## Verified no-change assertions

| Assertion | Verification |
| --- | --- |
| Zero production files modified | Change set is 9 new files, all under `WORKER_RETURNS/` |
| `AUTHORITY_KINDS` closed set unmodified | 18 kinds at the tip; this lane proposes 1 addition to 19. The set itself is **not edited** by this lane — the proposal lives only in the return documents |
| No existing authority kind redefined | All 7 commission-named reuse targets are referenced by `ExactRef`, never redefined |
| No new authority **state** created | `AUTHORITY_STATE` / `FAIL_CLOSED_STATES` reused unchanged |
| No new selector semantics | `FORBIDDEN_SELECTOR_TOKENS` remains binding |
| No new family in a production module | `TEMPORAL_RELATION_STATE` and `TEMPORAL_COMPARABILITY` are **proposed** names only |

## Scope boundaries this lane must not cross

**Authored here (documents only):**
- `TEMPORAL_COMPARABILITY` — one proposed authority kind, contract grain
- `TEMPORAL_RELATION_RECEIPT` — one proposed receipt family, contract grain
- `TEMPORAL_RELATION_STATE` + reason codes — one proposed state family

**Explicitly NOT authored, NOT implemented, NOT adopted:**
- No production `AUTHORITY_KINDS` edit
- No `EmpiricalFact` time field
- No temporal-gap object
- No time-indexed observation object
- No rupture-candidate producer
- No grain enum or grain validation
- No trajectory object
- No scalar temporal-pressure field, coefficient, threshold or deadband
- No interpolation or midpoint logic
- No new selector or resolution rule
- No Astra packet or referral
- No actor/person semantics
- No source data, survey execution or locator discovery
- No self-adoption

## Downstream obligations created by this contract

These are **named, not discharged**. This lane names them so the next lane
inherits them explicitly rather than rediscovering them.

1. **`IDENTITY_CONTRACT_INSTANCE_MISSING`** — no instance composes the temporal identity key. Composition must occur under `TEMPORAL_EVIDENCE`.
2. **`TIME_INDEXED_OBSERVATION_OBJECT_ABSENT`** — `EmpiricalFact.REQUIRED_FIELDS` has no time field (`rawlsing_next/pre553_empirical_objects.py:696-724`). Interim: the anchor ref carries time.
3. **`TIME_REFS_CURRENTLY_EXACT_AND_GRAIN_UNVALIDATED`** — `allowed_effective_time_or_interval_refs` is a tuple of `ExactRef` naming either a point or an interval and constraining neither (`rawlsing_next/pre553_structural_admission.py:218`). Grain lives in bound authority by design; a grain enum at substrate level is **not** recommended and is not authorized.
4. **`RUPTURE_CANDIDATE_PRODUCER_AND_CALIBRATION_AUTHORITY_UNCONSTITUTED`** — no producer authorized; event-override slot remains `reserved_not_filled`.
5. **`TEMPORAL_GAP_OBJECT_ABSENT__TYPED_SPAN_STATE_SUBSTITUTE`** — `intervening_span_state` is a substitute, not a gap object.
6. **Family-scoped mapping material unadopted** — a generic evaluator cannot decide comparability for a family whose mapping is unadopted. Correct outcome is a typed refusal, never a guess.

## Sequencing note

`TEMPORAL_COMPARABILITY` becomes usable only once an actual instance is
authored under it. This lane derives the contract; it does not authorize or
produce the instance. **A contract with no instance is the expected state of
this lane** and must not be reported as a capability.

## Relationship to existing downstream refusal language

Existing M1 states `NO_POSITIVE_V553_OUTPUT__MISSING_TEMPORAL_AUTHORITY`,
`__MISSING_COMPARABILITY_AUTHORITY` and `INELIGIBLE_TEMPORAL_SIGNATURE`
(`rawlsing_next/m1_temporal_v554_admission_dedup.py:50-57,83,240-247`) remain
binding and are **not** superseded. This contract supplies the authority
beneath them; it does not replace them.

## Verification performed by this lane

- Commissioned tip `20568aae374396cbc058bb500777491379a29f8c` verified exact.
- All 7 commission-named reuse targets verified present in the adopted closed 18-kind `AUTHORITY_KINDS` set — this is the minimality proof for proposing exactly one new kind.
- `TEMPORAL_NONCOMPARABLE` located at exactly one production site (`rawlsing_next/pre553_source_relations.py:54`) and confirmed to be a bare string with no producer, no schema and no reason code.
- Source-side counterpart `EMPIRICAL_FACT_NONCOMPARABLE` confirmed to be a **produced** decision with reason codes (`rawlsing_next/pre553_structural_admission.py:47,65,639-640,680-681`), establishing the contrast that defines the defect.
- Withdrawn HQ201 grain-fork framing confirmed **not** reinstated; no Astra referral claimed.
- All JSON artifacts parse.