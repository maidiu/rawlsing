# M20 — magnets / relational field: X05 direct-source dossier

**Court:** X05 historical source / material-actor-world bridge. **Evidence grade:** `HISTORICAL_SOURCE_AUDITED` plus sourcefree probe; `CURRENT_INTEGRATION: UNTRACED`; `THEORY: PROPOSED_NOT_ISSUED`; `AUTHORITY: NO_NATIVE_GRANT`.  
**Direct source:** `v3/core/state.py` `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`; `v3/engine/active_magnets.py` `68a7b75aa4bb98f7251f72a05747425edb40d24edbe06611ce998e7b6c26a391`; `v3/systems/relational_field.py` `75cfd5f27528ee00306de353b730d50ab3fc028970c11afcf84edea7eea7b8cd`; `v3/systems/health_drift.py` `ba4608b7b9ab5dc758085ea90ed6eef64b4e40cc20790508e6623e51dc13995b`.

## 1. Exact as-built map — two distinct ideas

### A. Persistent magnets

| Element | Source | Inputs / reads | Operation | Writes | Consumers |
|---|---|---|---|---|---|
| `Magnet` | `v3/core/state.py:205-215` | `id, magnet_type, label, intensity, tenure_years` | dataclass, clamp | stored `state.active_magnets` | JSON; LLM summary; persona micrograph; health drift |
| seed magnets | `v3/io/identity_to_backbone.py:407-430` | identity religion/region/age/urbanicity | **always** appends `mother` (parent, 60), `father` (parent, 55), plus optional religion/region/school/city magnets | `state.active_magnets` | first year |
| `_candidate_to_magnet` | `v3/engine/active_magnets.py:15-22` | selected candidate `id, magnet_type, label, intensity` | creates `Magnet`; **drops `who`, `entry_point`, `stickiness`, offers/costs, compatibility, branches, implicated** | one `Magnet` | state |
| `apply_selected_magnets_to_state` | `v3/engine/active_magnets.py:25-55` | selected candidate list; plasticity `magnet_susceptibility`; max 12 | adds new IDs, boosts default intensity by `0.9 + susceptibility/100*0.2`, caps list | `state.active_magnets` | after Pass 1 |
| `update_active_magnets_step` | `v3/engine/active_magnets.py:58-86` | config decay default 2.0, floor 15, max 12; plasticity | decay intensity, increment tenure, remove below floor | `state.active_magnets` | yearly step |
| Candidate sanitisation | `v3/engine/llm_contract.py:290-339` | LLM `magnet_candidate` | keeps `who`, `entry_point`, etc. in the **candidate** dict | candidate only | scoring/selection |
| Selection | `v3/engine/scoring.py:181-200` | capacity binding/agency, susceptibility | score `0.6+0.2*binding+0.2*agency+susceptibility*0.1`; select top 2 | selected candidate list | apply |
| LLM summary | `v3/engine/llm_contract.py:747-751` | active magnets | only `id/label/magnet_type` for first 10 | Pass-1 context | event proposal |
| Persona micrograph | `v3/io/persona_sheet.py:376-410` | magnet type/label | maps to `caregivers`, `peers`, `institutions` | persona sheet | V2 context |
| Hidden lexical law | `v3/systems/health_drift.py:69-77,98-162` | magnet count/label keywords | magnet count raises `intensity_and_capture.intensity`; labels containing `art/music/...`, `famil/...`, `community/...`, `activist/...` add practice points | `intensity`, `practice_stack` | next year |

**Critical:** the `Magnet` dataclass has no `who`, entity ID, relation ID, source event, actual encounter, reciprocity, or history. The LLM candidate's `who` field is sanitized but discarded by `_candidate_to_magnet`. The seeded `mother`/`father` magnets exist even if the parent is absent, dead, unknown, or non-caring. `intensity` is a free numeric score, not observed closeness or attractiveness.

### B. Relational-field projection

| Element | Source | Inputs / reads | Operation | Writes | Consumers |
|---|---|---|---|---|---|
| `build_relational_field_projection` | `v3/systems/relational_field.py:13-42` | `state.strata_stack` levels/names/salience | adjacent-level `contrast`, direction; attaches `absolute_horizon` as internal-only | projection dict | calibration / state |
| `apply_relational_field_to_state` | `v3/systems/relational_field.py:45-71` | projection dict | attaches summary to `strata_salience["relational_field"]`, `strata_salience["absolute_horizon"]`, `yearly_integrity` | state surface | flow |
| Flow conductance | `v3/psyche/flow.py:238-259` | relational status, strata count, absolute-horizon flags, domain/channel | fixed small bonus `strata_count/250` plus flags; no actual relation | trace conductance | pressure-flow |
| Test | `v3/tests/test_v5_relational_field_does_not_add_tenth_stratum.py` | strata stack | verifies 9 strata and no tenth | — | architecture check |

**What the relational field is not.** It is not a graph of persons, ties, obligations or power. It is a summary of the existing nine-strata stack: adjacent levels, names, salience contrast, and an `absolute_horizon` marker that is explicitly excluded from surface export. The only “mediation” is a tiny fixed conductance bonus. It cannot represent a real relational magnet toward a specific person or institution.

## 2. What this actually models, and what it does not

The code models:

- a persistent **label/intensity** carrier for people/scenes/institutions;
- decay/tenure and a plasticity boost;
- a structural summary of the nine strata with an absolute-horizon guard;
- a lexical mapping from magnet labels to practice increments.

It does not model:

- a real other actor with independent intentions/actions;
- actual relationship history, reciprocity, dependency, power or care;
- an entity reference that can be resolved to a generated person/institution;
- a distinction between love, attachment, coercion, admiration, dependency and attraction;
- a structural relational graph with rights/obligations.

The “mother/father” seed is especially harmful: it manufactures a relation to a parent even when the parent record is missing. The old code can have an absent parent and an active `mother` magnet simultaneously. That is exactly the kind of constructed relationship label the commission asks us to separate from an independent actor.

## 3. Coverage and disposition

| Target | Coverage | Reason |
|---|---|---|
| N07 independent others/power/love | `PARTIAL_WRONG_MEANING` | magnets/relational labels exist, but no independent actor or actual relation |
| N04 multiple interpressures (adjacent) | `INFRASTRUCTURE_ONLY` | magnet count affects intensity, not concurrent recruitment |
| N10 ideology/cosmology (adjacent) | `INFRASTRUCTURE_ONLY` | institutions/labels only |
| N12 actual C12 person | `UNKNOWN` | no current C9/C12 consumer |

**Disposition: ADAPT.** Keep the persistent magnet carrier, decay/tenure, selection and plasticity as a candidate affordance. Keep the absolute-horizon separation and nine-strata summary. Remove the unconditional parent magnets, the dropped `who`, the free intensity-as-truth, and the lexical practice law. Bind magnets to source-qualified actor/institution IDs with actual relation histories; if no entity exists, the magnet is `unknown/absent`, not a relation.

## 4. Harmful defaults / defects to remove

1. **Unconditional `mother`/`father` magnets** (`identity_to_backbone.py:407-430`) regardless of actual parent presence.
2. **`who` is dropped** by `_candidate_to_magnet`; `Magnet` has no entity reference.
3. **Free `intensity`** is treated as a real pull; no actual encounter or reciprocity.
4. **Lexical label → practice** (`health_drift.py:98-162`): “music” or “community” in a label adds craft/organizing; this is a hidden policy inference.
5. **Magnet count → intensity** (`health_drift.py:69-77`): more labels mean deeper engagement.
6. **Relational field is a summary**, not a causal graph; the fixed conductance bonus is not a relation.
7. **No parents/co-care/distinct actors**; seeded labels can coexist with missing parent records.

## 5. Proposed typed seam (nonissuing)

```text
ActorEntityRef {
  entity_id; kind (person/institution/scene); source_ref; identity_status;
  generated_history_refs[]; access_rights; clock; rule_version;
}
RelationHistory {
  actor_id; entity_id; relation_kind; start/end; actual_encounters[];
  reciprocity; dependency; power_asymmetry; care_received/given;
  source_refs; actor_access; unknown_fields[];
}
MagnetView {
  actor_id; entity_id; current_pull; evidence_refs[]; tenure;
  rule_version; uncertainty;
}
```
A magnet must resolve to an `ActorEntityRef`; a relation label without an entity is not a relation. The C9/C12 consumer reads the relation/encounter, not an intensity scalar. The relational-field projection may remain a structural view if it cites exact entity/tie refs and never exports an analyst-only absolute horizon.

**Owner:** ADP019/C8/world for other actors; ADP015 for relation; CAN010/CAN011 for actor orientation; C9/C12 for consumer. **Not issued by X05.**

## 6. Counterexamples and hostile alternative

**Counterexample (absent parent, present magnet).** A child has no father record, but the connector appends `father` intensity 55. A later persona micrograph lists `father` as a caregiver. The old code fabricates a relationship label; it does not prove a father acted.

**Counterexample (co-care).** The mother magnet is high but the mother works; the aunt provides daily care. The old code has no aunt entity and no care record; the aunt cannot become a magnet unless the LLM invents a label, and even then `who` is dropped.

**Counterexample (materially present but coercive).** A parent magnet may be high because the parent is present, while the parent is coercive. Intensity does not distinguish presence, warmth, coercion or dependency.

**Hostile alternative.** The persona's “caregiver” may be a narrative artefact of the magnet label, not a real actor. A hostile test removes the parent record but keeps the seeded magnet; if the persona still reports a father/caregiver, the label is doing the causal work.

**Falsifier.** If a real generated other actor/encounter changes a later C9 relation read while a magnet intensity change does not, the magnet is only a label. If the magnet change alone changes it, the consumer is reading a policy label.

## 7. Tests and limits

- Sourcefree X05 probe: seeded magnet `mentor` with `who='Ms X'` becomes `Magnet(id='m1', magnet_type='mentor', label='music mentor', ...)`; `who` is absent. Decay 70→67.74 after one year (susceptibility 10). Magnet labels `music studio`/`teacher`/`community movement` added craft/study/organizing without any practice event.
- Historical tests read: `test_wave4.py:72-87` (magnet persistence); `test_llm_contract.py:168-190` (summary); `test_v5_relational_field_does_not_add_tenth_stratum.py`.
- **NOT_RUN:** full old suite; current C9/C12; native person.
- **No native rule or source permission is issued.**

**Required future reviewer:** independent V3 source/consumer reviewer for M20/N07; ADP019/C8/world owner for independent actors; ADP015 for relations; current C9/C12 implementer. X05 does not self-adopt.
