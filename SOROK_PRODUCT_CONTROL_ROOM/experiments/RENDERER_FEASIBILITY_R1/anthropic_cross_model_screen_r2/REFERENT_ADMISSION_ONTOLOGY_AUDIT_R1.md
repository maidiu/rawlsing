# RFA-06C — referent admission ontology audit (independent source court)

**Scope:** original `lab_fixture/OBJECTIVE_OCCURRENCE_OUTPUT_SCHEMA_R1.json`, `CLAUDE_ACTOR_REALIZATION_CONTRACT_R1.md`, RF001–RF010 fixtures, RFA-05B WP/N packet compilation and paired inputs, RFA-06A `court_common.py` and RFA-06B `court_common_r2.py`, Sorok 101. Authority remains the source authors' contracts, not subsequent status counts.

## Exact governing warrants

1. **RFA-05 output schema:** `atoms[].referent_ids` is an array of unique **strings**, with *no scene-only enumeration or prefix constraint*. `world_effect_proposals[].referent_id`, by contrast, is expressly limited by its description to **documented object state changes** and is separate from atom grounding. This difference is material.
2. **RFA-05 Claude actor realization contract, “Binding invariants,” “Compiling the prompt,” and “Post-call deterministic admission”:** the renderer must maintain canonical historical/relational grounding and actor-access limits, while only objectively possible physical actions and objects can become proposals. Historical false speech remains a permitted utterance; it is not a physical-world truth claim. An arbitrary reference or nonexistent physical object must still fail.
3. **RFA-05B Whole-person compilation rule:** `whole_current_developed_person` has `ORG`, `MAT`, `PR`, `K`, `D`, `BIO` ID-bearing components; selectively sampled `H` episodes and case-activated `MEM` references also have their own IDs. `differentiated_relations` contains `R`, `NP`, `REL` components. Their explicit source IDs exist in actor realization-safe input and can ground expression even when not physical props.
4. **RFA-05B N compilation rule:** N contains exact sealed `shared.actor_projection_exact_from_RFA05.actor_accessible_refs`; its named references may include memories, projects, relational episodes, or organizational practice as well as scene-world IDs. N does **not** inherit the WP-only ID universe.
5. **All ten RF pairs:** `RF001` narrows to H006/MEM01/R13 as well as W03; `RF002` references ORG04/MAT03; `RF003` H017/MEM07/T02; `RF004` H015/MEM06 (not W09); `RF005` H006; `RF006` ORG04; `RF007` H019/H020/PR04; `RF008` R10–R13/NP01; `RF009` adds branch-only R14B/R15B; `RF010` H016/MEM05/T03 with restricted knowledge. These are actor-visible IDs, not an open-ended or cross-case grant.
6. **Sorok 101, sections 6, 7, 18:** causal activity differs from actor accessibility and narration; the objective occurrence layer records what is externally done, distinct from user phenomenal attention; the renderer's lawful context can contain stable person, historical, relational, event and physical-world layers. It does **not** reduce every grounding reference to a physical object.
7. **RFA-06A/B code:** `deterministic_candidate(candidate,case_id,refs)` receives only `shared.scene.facts[*].source_ref`, expands with actor/participant literals, and rejects every other atom reference under `UNKNOWN_ATOM_REFERENT`. That is narrower than the atom schema and the actual actor-visible multi-layer packet. The same checker separately validates `world_effect_proposals`, where restricting to documented scene IDs *is* correct.

## Typed verdict

The lawful interpretation is **C: typed intermediate rule**. `atoms[].referent_ids` may identify a source-grounded semantic anchor for a proposed outward atom, not only a physically observable item. This field **does not** create permission to physically act on the thing named, to materialize it, or to narrate private contents.

| Class | Permissible origin | What is *not* licensed |
| --- | --- | --- |
| `PHYSICAL_SCENE_REFERENT` | Exact `shared.scene.facts[*].source_ref` W ID | Physical actions outside scene capacity or a previously unobserved object |
| `ACTOR_OR_PARTICIPANT_REFERENT` | Explicit actor NADIA and speaker P0 | Private user states or unnamed persons |
| `ACTOR_ACCESSIBLE_MEMORY_OR_HISTORY_REFERENT` | H/MEM IDs in precise actor-access or WP curator fields | Detailed missing memory, hidden upstream cause or compulsory self-explanation |
| `RELATIONAL_REFERENT` | R/NP/REL IDs in actor-access or WP differentiated-relations fields | Objective certainty about P0's private motivations; foreign branch |
| `TASK_PROJECT_OBLIGATION_REFERENT` | PR IDs in source actor-access / WP current-person components | Imaginary object physically present or new project-owner writes |
| `ORGANIZATIONAL_OR_INSTITUTIONAL_REFERENT` | ORG ID in actor-visible organization | Global behavioral stereotype or first-person access to causal machinery |
| `OTHER_SEMANTIC_GROUNDING_REFERENT` | Explicit K/D/MAT/BIO/T IDs in recognized source paths | A new world fact, unbounded skill, narrator-only explanation |
| `NON_GROUNDABLE_HIDDEN_CAUSAL_REFERENT` | Not in allowed actor-realization-safe fields | **Never admitted** solely from evaluator canon or causal oracle |
| `UNKNOWN_OR_UNAUTHORIZED_REFERENT` | Unknown, unsupported, or other-case identifier | **Rejected** |

**BEHAVIOR_ONLY versus NARRATABLE_WHEN_RELEVANT:** a `BEHAVIOR_ONLY` source component may explain the model's choice of outward behavior while still not authorizing speech about that source's contents. Reference-ID allowance is thus only *structural grounding*, not a first-person narrative permission or substantive score. The post-generation checker flags such references for substantive review but does not automatically declare them invalid.

## Original evidence versus inference

The owner reports R2: 60/60 parsed, 60/60 full-schema valid, 22 of 23 original structural-invalid statuses due only to `UNKNOWN_ATOM_REFERENT`, one exact speech mismatch, and 59/60 substantive passes. These counts are **owner-reported**; no R2 raw provider responses are present in the committed GitHub source. The source-based finding is independent: the old atom checker is **OVERRESTRICTIVE**. The corrected checker is not authorized to relabel those 22 as substantive successes without locally reading each actual response, deriving permissions per packet, and applying separate qualitative evaluation.

## Resulting disposition

`INHERITED_REFERENT_CHECKER = OVERRESTRICTIVE`; a strict, case-and-arm-local, typed allowlist is warranted for atoms. Keep physical world effects as documented-W-only. No reason exists in these sources to change model inputs or reconstruct Nadia's actor-safe packet. The post-generation-only repair leaves the existing Opus R2 comparison generation contract intact.
