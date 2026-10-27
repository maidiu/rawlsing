# M18 — court return

**Court:** HISTORICAL_V3 / EXACT_MECHANISM; X03 independent source return, awaiting independent review. **Coverage:** PARTIAL_WRONG_MEANING

**Source identity:** X03 sealed startup `2647a4cf25d8bb33a00471e1af9c5e58c2825efb`; direct read-only files are hashed in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`. The S50-selected files are 31/31 exact. X03 files outside S50 were matched to `CAN_011_V3_MIDDLE_STATE/AUTHORITY.json`, `CAN_012_V3_RUPTURE_METABOLIZATION/AUTHORITY.json`, `CAN_010_V3_NEED_EXPECTATION_STRIVING/AUTHORITY.json`, `ADP_007_V3_ACTOR_INITIALIZATION/AUTHORITY.json`, or are explicitly local-source-only. The local staging zip `3f2c5ed9…` is not the TD-R05 archive `953c9149…`; archive-level exactness is not claimed.

**Claim ceiling:** historical source and sourcefree probe behavior at the cited grain. This is not current C9/C12 integration, a native person, a scientific law, or a source/actor/C8/C9/C11/C12/Pyat grant.


**Terminal:** `X03_M18_HISTORICAL_SOURCE_VERIFIED__PARTIAL_WRONG_MEANING__SCIENCE_HOLD_RULE_UNISSUED__AUTHORITY_NO_NATIVE_GRANT`

## Immutable source and return identity

- Sealed startup: `2647a4cf25d8bb33a00471e1af9c5e58c2825efb`.
- Source files: direct read-only local historical V3; hashes in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`.
- X03 return branch: `agent/v3court-x03-development-topology-r1`.
- The return content commit and final remote head are recorded in `WORKER_RETURNS/X03/00_RETURN.md`; this dossier is part of that return and does not claim a self-referential SHA.
- Current integration: **UNTRACED**; no current C9/C12 consumer run.

## Evidence grades

- **HISTORICAL_CODE:** `HISTORICAL_SOURCE_AUDITED` for cited files; direct body inspection and line mapping.
- **HISTORICAL_RUN:** `HISTORICAL_RUN` for the 71 focused sourcefree tests and the direct probe; not for any mechanism-specific behavior the tests do not cover.
- **CURRENT_INTEGRATION:** `UNTRACED`.
- **THEORY:** `RULE_PROPOSED` only; no issued scientific law.
- **AUTHORITY:** `NO_NATIVE_GRANT`; source/actor/C8/C9/C11/C12/Pyat remain separately owned.
- **COURT:** `RETURNED_AWAITING_INDEPENDENT_REVIEW`.

## Findings

- **FINDING:** The LLM/event path creates a `RuptureShard` and one `MetabolizationProcess`, both status `"raw"`, and sets a plasticity window. It does not update the wound vector. The age-band server path calls both `create_rupture_shard_from_event` and `update_wound_vector_from_rupture`.
- **FINDING:** Severity is inconsistent. `create_rupture_shard_from_event` maps `intensity` `"major"`/`"shock"` to `"major"`; every other value, including `"malheur"` and `"minor"`, becomes `"micro"`. `update_wound_vector_from_rupture` is passed the original `"malheur"` by the age path, so the process can be `"micro"` while the wound receives the +15 malheur bump. Probe: malheur event -> process severity micro, shard raw; direct malheur wound update changed abandonment 50→69; create-only left wounds unchanged.
- **FINDING:** `RuptureShard.current_status` is created `"raw"` and never changed. `meaning_attempts` stays empty. `MetabolizationProcess` starts `"raw"` with empty narrators/provisional frame/reactivation triggers and remains so. Persona code reads a nonexistent `metabolization_mode` attribute in two places, so that branch is always false.
- **FINDING:** `maybe_inject_rupture_at_band_age` uses hardcoded age bands (3, 7, 11, 14, 17, 24, 30) and global `random.random()/choices()`; template selection, severity, opacity, and mode are sampled. Probe at age 14 with seeds 0–19 injected 14 times, with process status raw, modes varying (accommodation, collapse, sealing, assimilation, mis_aim), and wound changes from the original severity.
- **FINDING:** The server calls `maybe_inject_rupture_at_band_age` after every `run_one_year` (simulation.py:539). The event path is separate. There is no admission rule, pre-event actor-state hash, exact parent event, actor-specific basis, or rule receipt.
- **FINDING:** The process severity `"micro"`/`"major"` makes `is_malheur(proc.severity, ...)` false in the yearly path; the `"malheur"` multiplier is therefore not reached for the malheur case. `reactivation_triggers` is never populated, so `delta_templates`’ reactivation bump has no matches.

- **ENGINEERING RED:** Age-band probability is an automatic trauma generator without actor basis.
- **ENGINEERING RED:** Global/unnamed RNG violates replay and ADP-020 semantics.
- **ENGINEERING RED:** Severity mapping contradicts the wound update; malheur is silently converted to micro for the process.
- **ENGINEERING RED:** LLM event path has no wound update; age path does. The two causal paths disagree.
- **ENGINEERING RED:** Shard/process statuses and meaning attempts are never developed.
- **ENGINEERING RED:** The persona’s mode field does not exist; the displayed rupture meaning is incomplete.

## Interpretation

The old mechanism is **PARTIAL_WRONG_MEANING** overall, not a green implementation. It retains a real carrier/operator in places, but the causal operation required by the linked N cards is absent or wrong. The strongest real affordances are:

- Typed persistent shard/process records and JSON exist.
- Epistemic rupture events can create a shard/process through the event path.
- The age path can add a bounded wound increment; the direct malheur probe shows a real numeric effect.
- Pass 1/persona have rupture/context surfaces, even though they are incomplete.

The strongest overclaims are the presets, missing lifecycle, missing support/history, and missing same-person consumer. The old code must not be described as current integration or as a native psychological law.

## Action and owner

| Finding | Interpretation | Action | Owner |
|---|---|---|---|
| RuptureShard / epistemic rupture admission carrier exists but is not the required operation | Retain compatibility only; do not adopt as law | A CAN012 admission record and later recurrence rule; downstream effects require separate target-owner rules. First consumer: later same-person C9 semantic read and causal memory, not persona text. | CAN012 / ADP019 for external event admission; ADP020 RNG; C9/C12 consumer |
| Old presets stand in for missing history | Demographic/age/label/random presets are source defects | Age-band injection, global/unnamed RNG, automatic adverse-label rupture, direct domain-to-wound mapping, severity micro/malheur mismatch, and empty status/meaning placeholders presented as substantial state. | Source owner / CAN011 or CAN012 as applicable |
| No current same-person consumer | Pass 1/persona/derived are insufficient | Build and independently test a later C9/C12 semantic read | C9/C12 + CAN/ADP owners |
| No issued scientific rule | The exact transition is not established | Request one domain-qualified rule with alternatives and NO_CHANGE | Competent science issuer |

## Tests and limits

- **Executed:** 71 focused tests passed; direct probe completed. See `TEST_MANIFEST.json`.
- **NOT_RUN:** mechanism-specific scientific validation; current C9/C12; native actor; full distribution smoke; full V3 suite (timed attempt incomplete and not counted); LLM/V2 run; source permission.
- **Self-limitation:** no primary literature re-read; no current product source import traced; no claim that the probe establishes a human mechanism.
- **Reviewer trigger:** an independent source/science reviewer must verify exact source hashes, line mappings, probe reproduction, the coverage classification, and the distinction between fixed old regime switches and acquired relations.

## Next finite action

Remove age injection and global RNG; make admission conditional on exact parents/basis/rule; separate wound/target effects; specify positive, NO_CHANGE, benign and same-event-different-history cases.

No native rule, actor/source grant, production adoption, or self-review is claimed.
