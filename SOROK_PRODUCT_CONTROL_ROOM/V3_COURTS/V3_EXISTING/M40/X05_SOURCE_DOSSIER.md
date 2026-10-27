# M40 — generation readiness / global ready surface: X05 direct-source dossier

**Court:** X05 historical source / material-actor-world bridge. **Evidence grade:** `HISTORICAL_SOURCE_AUDITED`; `CURRENT_INTEGRATION: UNTRACED`; `THEORY: PROPOSED_NOT_ISSUED`; `AUTHORITY: NO_NATIVE_GRANT`.  
**Direct source:** `v3/core/generation_integrity.py` `5265aac2fda4d6e6ac62927353518045f215d7d1916930e19e980b6d77eff214`; `server/generation/store.py` `eb592702327427a22b5d901337e6ee8b251b164ad41fe8848b165a14730a942c`; `server/generation/simulation.py` `5d68ffe3bc6902dc60b90625443a03127cf0d04b4eed4327270a3a0226bc78d1`; `server/session_state.py` `9c9c3b0e2b3bff700af127e03805166102920019d6acd099ee8270fbe63bc15a`; `server/generation/diagnostics.py` `e682303cfc8bc94d244a34b081688e3625d160d32e6512ff95d1f70536841ddc`.

## 1. Exact as-built map

| Element | Source | Inputs / reads | Operation | Writes / outputs | Consumers |
|---|---|---|---|---|---|
| `IntegrityStatus` | `v3/core/generation_integrity.py:7-11` | — | CLEAN/DEGRADED/BLOCKED | constants | accumulator |
| `GenerationIntegrityAccumulator` | `v3/core/generation_integrity.py:13-79` | diagnostics entries | records stage/status/timestamp/fallback/fields/impact; `verdict` chooses worst status; optionally merges `classify_field_provenance` | verdict dict | sheet metadata; store; API |
| `classify_field_provenance` | `v3/core/generation_integrity.py:82-105` | field provenance | checks only `ethnicity/religion/language`; blocked if source missing/unknown/defaulted; degraded on factbook fallback/language invalid | string | verdict |
| `_validate_persona_for_store_write` | `server/generation/store.py:245-322` | identity, sheet, accumulator verdict | starts `clean_ready`; blocked on missing verdict/name/country; degraded on language placeholder/identity mismatch; clean otherwise | readiness summary | simulation store write |
| `_validate_stored_persona_for_live_use` | `server/generation/store.py:183-244` | identity/sheet/generation integrity | requires name and country; **does not inspect generation grade**; returns clean_ready if those pass | usable/status | `/api/start` stored persona |
| `_golden_eligibility_for_session_dir` | `server/generation/store.py:77-142` | persona sheet, diagnostics, readiness, generation verdict | eligible only if readiness clean/degraded and generation clean/degraded; golden_clean/degraded | eligibility | **tests only**; no production caller found |
| `_artifact_integrity_for_session_dir` | `server/generation/store.py:43-75` | generation integrity/diagnostics | `clean`, `missing_diagnostics`, `contaminated` (degraded/blocked), `generated_legacy`, `unknown` | artifact status | summary/golden |
| `GenerationState` | `server/session_state.py:35-58` | enum | ready = `clean_ready` or `degraded_ready` | ready boolean | status/personas/start routes |
| `write_persona_to_store` | `server/generation/store.py:324-430` | complete run | writes identity/state/derived/sheet/integrity/diagnostics/year records | store artifacts | later `/api/start` |
| Simulation finalisation | `server/generation/simulation.py:780-850` | accumulator/field provenance | computes verdict; writes diagnostics; writes sheet metadata; calls store validation; blocks store write only if `blocked` | session state/persona/store | API |

**What is real.** The archive has a structured readiness/generation-integrity system, not a simple `ready=True` based on persona-sheet existence. It distinguishes `clean_ready`, `degraded_ready`, `blocked`, `legacy_unknown`; records per-stage diagnostics; writes generation artifacts; has golden eligibility (tested); and blocks store writes on a blocked verdict. TD-R05's correction is right.

**Where it falls short.** Readiness is **generation completeness**, not product/person readiness:
- `_validate_stored_persona_for_live_use` does not check the generation grade. A stored persona with a `blocked`/`degraded` generation verdict but a name and country is returned `usable=True` with `readiness_status="clean_ready"` (`store.py:215-241`). This is a concrete defect.
- `degraded_ready` counts as ready for chat (`server/session_state.py:53-58`), so a degraded generation can be presented as a normal person.
- Hardcoded defaults (`capacity.time=50`, `health=50`, `social_support=50`, `skill=50`, `risk_tolerance=50`, `dependents=0`, `caregiving_load=0`, `legal_status=100`) are not recorded as degraded. The accumulator only knows about explicit stage failures; a clean run on defaults can be `clean`.
- `classify_field_provenance` checks only ethnicity/religion/language; it does not check material facts, parent history, care, source authority, scientific rule, or current consumer.
- `_golden_eligibility_for_session_dir` is not wired into the API; only tests call it.
- `_write_generation_integrity_artifacts` writes `generation_diagnostics.json`, not `generation_integrity.json`; the store writes `generation_integrity.json` when called. Two artifact shapes exist.
- The readiness verdict contains no science/rule/source permission, no actor provenance, no “actual person” proof, and no C9/C12 consumer proof.

## 2. What this actually models, and what it does not

It models a **generation-integrity and storage-readiness gate**: did stages fail, are identity placeholders present, is there a generation verdict? It does not model:

- executable engine vs science-qualified rule;
- native source/actor permission;
- historical actor provenance;
- autobiographical memory/access;
- a consumer-observed person;
- a current C9/C12 semantic read;
- a distinction between “no generation error” and “valid material/care/other-actor history”.

This is a useful engineering scaffold, but it is not the M40 “global ready surface” in the product sense. It must not be used as proof that a person is scientifically or authorially ready.

## 3. Coverage and disposition

| Target | Coverage | Reason |
|---|---|---|
| N11/N12 | `INFRASTRUCTURE_ONLY` | readiness scaffolding exists; no native event/state/memory loop or consumer |
| M40 card | ADAPT | structured readiness is real; extend to product/source/science/consumer dimensions |
| Current C9/C12 | `UNKNOWN`/HOLD | RC review: no qualified current compiled person; S49 empty B source, S42 default predicates, S48 one-call, S52 withheld |

**Disposition: ADAPT.** Keep the accumulator, status taxonomy, diagnostics and blocked-store-write. Split readiness into independently owned gates:
1. `ENGINE_READY` (executable component);
2. `SCIENCE_RULE_READY` (issued rule/version);
3. `SOURCE_ACTOR_READY` (source/rights/actor/world);
4. `HISTORY_READY` (generated actor history, including care/other actors);
5. `MEMORY_ACCESS_READY` (ADP016/017);
6. `CONSUMER_READY` (current C9/C12 same-person semantic read);
7. `A5/HUMAN_ENCOUNTER_READY`.

No aggregate `ready` may be true unless each required gate is explicitly satisfied or lawfully waived by its owner.

## 4. Harmful defaults / defects to remove

1. **`_validate_stored_persona_for_live_use` ignores generation grade**; name+country is enough.
2. **`degraded_ready` counts as ready** for chat.
3. **Hardcoded defaults are not degraded**; a clean run can be built on 50/0/100 defaults.
4. **Only identity fields are classified**; no material/care/actor/source/rule/consumer.
5. **`_golden_eligibility` not wired**; golden status is test-only.
6. **Two integrity artifact shapes** (`generation_diagnostics.json` vs `generation_integrity.json`).
7. **`contaminated` label for degraded/blocked** in `_artifact_integrity` is a coarse mapping; it does not say what is contaminated.
8. **No source/actor/rule version** in the verdict.

## 5. Proposed typed seam (nonissuing)

```text
ReadinessGate {
  gate_id; status (READY | DEGRADED | BLOCKED | NOT_RUN | UNKNOWN);
  owner; evidence_refs[]; rule_version; source_refs[]; waiver_ref;
}
PersonReadiness {
  actor_id; gates[]; aggregate (only if all required gates READY/waived);
  no_science_or_source_inference; timestamp;
}
```
The consumer must read individual gates; a single `ready` boolean is not admissible. `DEGRADED` is not silently equivalent to `READY`; the consumer must know which gate is degraded.

**Owner:** C12/engineering for the gate machinery; CAN008/CAN010/CAN011 for science; ADP016/017 for memory; SDTF/Pyat/C8 for source/actor; current C9/C12 for consumer. **Not issued by X05.**

## 6. Counterexamples and hostile alternative

**Counterexample (blocked generation, usable persona).** Store a persona with a name/country but a blocked generation verdict; `_validate_stored_persona_for_live_use` returns usable with clean_ready. The route then starts a chat with it. The readiness gate did not protect the user.

**Counterexample (clean defaults).** A run with all hardcoded 50/0 defaults and no actual parent history can have no stage failures; the accumulator returns clean. `clean_ready` is then true despite missing material/care/actor facts.

**Counterexample (degraded ready).** `GenerationState.DEGRADED_READY` is treated as ready in `session_state.py`; a degraded generation is presented as normal unless the UI separately reads the integrity. That is a product decision, not a science qualification.

**Hostile alternative.** The current server may never load a stored persona with a blocked verdict because the store write blocks it. That is true for newly generated blocked runs, but not for legacy/imported/store-corrupted artifacts; `_validate_stored_persona_for_live_use` is the guard and it does not check the grade. A hostile test constructs a stored sheet with a blocked verdict and no name/country check failure; the guard passes.

**Falsifier.** Remove the name/country fields from a blocked stored persona; if the guard still starts, it is not a readiness gate. Add a blocked generation verdict but valid identity; if the guard passes, it is not checking generation.

## 7. Tests and limits

- Tests read: `tests/test_generation_integrity.py:273-305` (golden eligibility); `v3/tests/test_architecture_invariants.py` (unrelated).
- Sourcefree X05 probes: no direct server store test run (would require constructing a persona store and would be a current product test). Static source read only.
- **NOT_RUN:** full old suite; current server end-to-end; current C9/C12; native person.
- **No native rule or source permission is issued.**

**Required future reviewer:** independent C12/readiness reviewer for M40; current C9/C12 implementer; CAN008/CAN010/CAN011 science owners; ADP016/017 memory; SDTF/Pyat/C8 source/actor owners. X05 does not self-adopt.
