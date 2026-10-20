# PA0 — FUNCTION EXISTENCE AND ORIGINAL BLOB CUSTODY

**Checkout:** `7623742bb9acd113d21de2d4528a1d5a35017989` (sealed PA0 startup, local isolated worktree).
**Method:** every module named below was read from the checkout; `git hash-object <path>` was compared with `git rev-parse HEAD:<path>` and, for the seven HQ leads, with the blob recorded in the P0/PA0 source-code priority motion. No source file was modified; this return subtree is the only write target.

## 1. The seven HQ priority leads — exact custody and motion agreement

| Module | Git blob at HEAD | Motion blob | Lines | Motion agrees | Producer output |
|---|---|---|---|---:|---|---|
| `rawlsing_next/gt34_u2_v3p1_authenticated_subject_materializer.py` | `b0cb39a9a975381f3f3b4a03e7e435b2932e89b9` | `b0cb39a9a975381f3f3b4a03e7e435b2932e89b9` | 810 | YES | `SubjectMaterializationReceipt` (subject_ref, not a person) |
| `rawlsing_next/gt34_s2_v3p1_subject_registry_materializer.py` | `0ac1df8ef4c91b9004f3ffb8d00fefcadc2980cf` | `0ac1df8ef4c91b9004f3ffb8d00fefcadc2980cf` | 341 | YES | same receipt shape; historical failed predecessor |
| `rawlsing_next/v3_adp010_oee_executor_authenticated.py` | `54d9acba40f0eb1db8bb03aec3c1bb900f849588` | `54d9acba40f0eb1db8bb03aec3c1bb900f849588` | 1795 | YES | `OEEExecutionResult` / `V3OEERealizationRecord` |
| `rawlsing_next/v3_psepf_zero_positive_guard.py` | `e0528d65215cb431196570c38bac4eae94217a1b` | `e0528d65215cb431196570c38bac4eae94217a1b` | 382 | YES | `GuardDecision` (deny zero-effect) |
| `rawlsing_next/wsc_gt0_v3_runtime.py` | `6c0494def59fc683241d8bff45bcbd68a25a7f3d` | `6c0494def59fc683241d8bff45bcbd68a25a7f3d` | 288 | YES | `GT0V3ZeroEffectResult` |
| `rawlsing_next/sdtf_r4_mechanism_rule_authority_binding.py` | `c94997f5c7f2bbee9cd99c570554fd48c0f47556` | `c94997f5c7f2bbee9cd99c570554fd48c0f47556` | 605 | YES | validated `MechanismRuleAuthorityBinding` |
| `rawlsing_next/sdtf_r4_world_response_redrive.py` | `9964a24e25467fa53cc9f5529b6f40be9f11f53a` | `9964a24e25467fa53cc9f5529b6f40be9f11f53a` | 624 | YES | bindings + `R4InvalidationRederivationRequest` |

All seven modules are stdlib-only except the two noted imports: `wsc_gt0_v3_runtime` imports `v3_psepf_zero_positive_guard` and `wsc_gt0_protocol`; `sdtf_r4_mechanism_rule_authority_binding` imports the PRE553 authority/objects modules; `sdtf_r4_world_response_redrive` imports `wsc_gt0_protocol`. None imports a person engine.

## 2. What the code itself says it does and does not do

Quoted from module docstrings at the blobs above:

- **U2:** “authenticates exactly one adopted OBL053 semantic object … preserves semantic opacity: semantic object bytes are never parsed, normalized, classified, or copied into materializer truth.” It emits a subject-ref receipt; it is a **nonactor** materializer.
- **S2:** “implementation substrate only … does not create semantic authority, classify entity type, infer fields, or create actor/encounter/exposure truth.” The U2 header calls S2 the “failed candidate evidence”; S2 remains immutable.
- **ADP-010 authenticated:** “does not materialize or classify subjects, infer contact from proximity, create EXPOSURE, mutate actor state, or create comparator/PSEPF/metabolism/CAN-008/V2/positive-V3 authority.” It implements `AVAILABLE -> OPPORTUNITY -> ENCOUNTER` and emits exact records.
- **PSEPF guard:** “has zero actor-state effect by default”; delegation only to a separately accepted positive transition authority; “this guard itself never mutates actor state, causal history, RNG state or scheduler state.” Production registry is empty.
- **GT0 V3 runtime:** binds the zero-positive guard; `after = before` is enforced; the actor sentinel is explicitly “not a generated-person identity.”
- **SDTF R4 mechanism binder:** “does not create an authority registry, select latest authority, mint concrete mechanism rules, execute rule bodies, write actor facts, choose numeric values, or close OBL062.”
- **SDTF R4 world redrive:** “never admits an event, authors a world response, writes a world, or mints D1' facts”; durable person mutation is forbidden.

## 3. Import and consumer custody (whole checkout)

Verified by source grep and import graph inspection:

- U2 and S2 are imported **only by tests** (`test_gt34_u2...`, `test_gt34_u3...`, `test_gt34_s2...`, `test_gt34_w1...`). No production module imports them.
- `v3_adp010_oee_executor_authenticated` is imported by three production modules: `v3_adp010_oee_executor_obl055_acceptance_bound.py`, `..._replay_canonical.py`, `..._replay_reconstructed.py`; those are themselves only test-imported and have no C9/C10 consumer.
- `v3_psepf_zero_positive_guard` is imported by `wsc_gt0_v3_runtime.py` (production) and by tests.
- `wsc_gt0_v3_runtime` is imported by `wsc_gt0_v2_mediation.py` and `wsc_gt0_end_to_end.py` (production modules, test-imported; no external/product consumer).
- `sdtf_r4_mechanism_rule_authority_binding` is imported by `sdtf_r4_d1_hosting_replay.py`.
- `sdtf_r4_world_response_redrive` has **no production import**.
- `m6_actor_safe_expression` is imported by `render_bounded_expression.py` and `wsc_gt0_v2_mediation.py`; `render_bounded_expression` is imported by `wsc_gt0_v2_mediation.py`.
- No production Python file imports any `WORKER_RETURNS/SOROK-20261019-*` candidate (C9P/C9R/C8O/C0X/G17/G18). Those are non-ancestor return branches and are absent from this checkout.

## 4. The decisive absence evidence

- `grep -rln "GeneratedPersonRecord\|DevelopmentalEventLedger\|V3RenderContext" --include="*.py" .` → **0 files**.
- No module in `rawlsing_next/` has `psyche`, `person_generator`, `developmental_engine` or `generate_person` in a module/class/function name. `person` occurs only as a field/string in M6's `source_generated_person_record_hash`.
- The V3 completion ruling (`49095f763c5c...`) itself says architecture is accepted but implementation is blocked and names 27 missing runtime-rule authorities (actor initialization; developmental phases; position; mobility; opportunity/encounter/exposure; V555/V556; response/metabolization; orientation; needs; frameworks/buffers; practice uptake; relationships; household; genealogy/child generation; rupture; causal memory; attractor; external event admission; LLM admission; randomness; scheduler; derived-state schedule). No compiled resource is named.
- Therefore the **person/psyche generator is missing software**, not merely unwired. The closest existing producers are a nonactor subject-ref materializer and an OEE encounter executor. A title, a subject_ref, an ADP opportunity fixture or a zero-positive guard is not a developed person.

## 5. The OBL053 adopted object preimage — reconstructed, not assumed

The adoption JSON (`f561765bad4fdad2bbf4591f35fe7f81f8486428`) contains the admitted semantic projection and the content-addressing law. The repair artifact blob `14ff405cfb77ccfe30adbce16e9c0ff14fa540f9` contains the exact projection under `prospective_semantic_object.semantic_projection`. Canonical JSON (`sort_keys=True, separators=(",",":"), ensure_ascii=False`) of that projection hashes to:

`9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`

which equals `OBL053_SEMANTIC_OBJECT_HASH`, the U2 `CURRENT_SEMANTIC_OBJECT_REF.sha256`, and the adoption JSON `semantic_object.object_content_hash`. This makes the **current accepted U2 materialization runnable from in-repo data** (smoke A). It remains a nonactor facility object.

## 6. Execution receipts

- 14 targeted test files (U2, S2, W2 ADP010 compatibility/repair/hostile, OBL055/OBL056 acceptance, PSEPF, WSC002R-B, WSC GT0 end-to-end, SDTF R4 binding/redrive/hosting/replay/witness, original ADP010 executor): **249 passed, 0 failed** at this checkout.
- The first 7-module subset: **154 passed**.
- The smoke consumer: exit 0, two positive invocations and six typed source-edge severances (see `06_...` and `evidence/smoke_run.json`).

## 7. Custody limits

- This atlas inspected the current Git checkout and the pinned return refs through the local object store. It did **not** read any private respondent data, credentials, or an external user Mac archive (no path/permission was supplied).
- Absence in this checkout is **not** global absence; `07_UNREAD_PRECISE_LOCAL_CANDIDATES.md` names the exact classes of artifact that could still carry an older implementation and the authority required to read them.
