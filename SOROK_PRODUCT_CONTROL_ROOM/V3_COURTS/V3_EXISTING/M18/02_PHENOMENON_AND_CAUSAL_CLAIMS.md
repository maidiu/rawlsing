# M18 — phenomenon and causal claims

**Court:** HISTORICAL_V3 / EXACT_MECHANISM; X03 independent source return, awaiting independent review. **Coverage:** PARTIAL_WRONG_MEANING

**Source identity:** X03 sealed startup `2647a4cf25d8bb33a00471e1af9c5e58c2825efb`; direct read-only files are hashed in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`. The S50-selected files are 31/31 exact. X03 files outside S50 were matched to `CAN_011_V3_MIDDLE_STATE/AUTHORITY.json`, `CAN_012_V3_RUPTURE_METABOLIZATION/AUTHORITY.json`, `CAN_010_V3_NEED_EXPECTATION_STRIVING/AUTHORITY.json`, `ADP_007_V3_ACTOR_INITIALIZATION/AUTHORITY.json`, or are explicitly local-source-only. The local staging zip `3f2c5ed9…` is not the TD-R05 archive `953c9149…`; archive-level exactness is not claimed.

**Claim ceiling:** historical source and sourcefree probe behavior at the cited grain. This is not current C9/C12 integration, a native person, a scientific law, or a source/actor/C8/C9/C11/C12/Pyat grant.


## Phenomenon the code says it models

An actor-specific rupture of effective orientation: a concrete encounter that the actor’s prior assumptions/practical relations cannot assimilate and that may reorganize later response. The code creates a `RuptureShard`; the required phenomenon is not every adverse event, negative affect, or age-band transition.

## What the source actually computes

The source does not implement the full phenomenon. Its concrete behavior is:

- The LLM/event path creates a `RuptureShard` and one `MetabolizationProcess`, both status `"raw"`, and sets a plasticity window. It does not update the wound vector. The age-band server path calls both `create_rupture_shard_from_event` and `update_wound_vector_from_rupture`.
- Severity is inconsistent. `create_rupture_shard_from_event` maps `intensity` `"major"`/`"shock"` to `"major"`; every other value, including `"malheur"` and `"minor"`, becomes `"micro"`. `update_wound_vector_from_rupture` is passed the original `"malheur"` by the age path, so the process can be `"micro"` while the wound receives the +15 malheur bump. Probe: malheur event -> process severity micro, shard raw; direct malheur wound update changed abandonment 50→69; create-only left wounds unchanged.
- `RuptureShard.current_status` is created `"raw"` and never changed. `meaning_attempts` stays empty. `MetabolizationProcess` starts `"raw"` with empty narrators/provisional frame/reactivation triggers and remains so. Persona code reads a nonexistent `metabolization_mode` attribute in two places, so that branch is always false.
- `maybe_inject_rupture_at_band_age` uses hardcoded age bands (3, 7, 11, 14, 17, 24, 30) and global `random.random()/choices()`; template selection, severity, opacity, and mode are sampled. Probe at age 14 with seeds 0–19 injected 14 times, with process status raw, modes varying (accommodation, collapse, sealing, assimilation, mis_aim), and wound changes from the original severity.
- The server calls `maybe_inject_rupture_at_band_age` after every `run_one_year` (simulation.py:539). The event path is separate. There is no admission rule, pre-event actor-state hash, exact parent event, actor-specific basis, or rule receipt.
- The process severity `"micro"`/`"major"` makes `is_malheur(proc.severity, ...)` false in the yearly path; the `"malheur"` multiplier is therefore not reached for the malheur case. `reactivation_triggers` is never populated, so `delta_templates`’ reactivation bump has no matches.

The observed causal role of **RuptureShard / epistemic rupture admission** is therefore split between: (a) a real typed/persistence affordance, (b) one or more real numeric or hysteresis operations, and (c) demographic, age, label, random, or source-free presets that stand in for missing history.

## Conceptual weakness

- Age-band probability is an automatic trauma generator without actor basis.
- Global/unnamed RNG violates replay and ADP-020 semantics.
- Severity mapping contradicts the wound update; malheur is silently converted to micro for the process.
- LLM event path has no wound update; age path does. The two causal paths disagree.
- Shard/process statuses and meaning attempts are never developed.
- The persona’s mode field does not exist; the displayed rupture meaning is incomplete.

## Competing human-mechanism accounts

1. **Historically formed, context-sensitive organization.** The required account treats this mechanism as arising from actual activity, care, contradiction, recognition, or support, with scope and revision. This is the needs-first direction, not a claim that the old code already implements it.
2. **Situated response without a stored trait.** The same observable response may be produced by current conditions and access without a durable internal object. The old code often assumes a stored scalar/record and cannot distinguish this alternative.
3. **Narrative or analyst classification.** A label can describe a person without causing the state. The old source sometimes treats an event label, rendered phrase, or demographic category as causal; that is a category error, not a competing psychology.
4. **Plural/contradictory organization.** Multiple tensions, frameworks, practices, or strivings may coexist. The source's counts, dominance, and single enum cannot represent this without loss.

Project-attached Leontiev, Sève, Lahire, Elder, Dreier, Luria, Archer, Kohn/Schooler, Wright and Mortimer materials are contextual sources, not a quantified actor law. No primary text was re-read for this return; the scientific decision remains HOLD. The RS review’s boundary is binding: motives form through actual activity; plurality and latent dispositions cannot be presumed without formation evidence; language/instruction may itself create an operation in some circumstances.

## Claim limits

The source shows what the historical code does, not what a human must do. No coefficient, threshold, age band, status ladder, or mode prior is promoted to psychological law here. A later competent issuer must decide whether a concrete transition exists; this return only distinguishes the old software behavior from the required semantic question.
