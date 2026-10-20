# PA0 — SOURCE-TO-CONSUMER CALL GRAPH

**Checkout:** `7623742bb9acd113d21de2d4528a1d5a35017989`.
**Rule:** an edge is listed as LIVE only where an actual Python import exists in the checkout; return-branch candidates are marked and are not imported outside their own subtree.

## 1. C12-backward graph (what the consumer would need → what exists)

```text
A0–A5 human-facing outcome                     [DOC ONLY; no Python endpoint]
        ^
C12 generated continuing person                [NO CONSUMER; no Python endpoint]
        ^
C11 native world/actor weld                    [NO CODE; separately held]
        ^
C10 coupled actor+world consumer               [NO COUPLED CONSUMER]
        +-- world side: C0X receiver (RETURN b02deee1/a0f7ab5f; not imported)
        +-- actor side: C9R CandidateStore/later_action (RETURN 6fa29399; not imported)
        ^
C9 E1 → RULE_A → RULE_T → E2                   [HEAD: ADP010 OEE precursor only]
        +-- HEAD: v3_adp010_oee_executor_authenticated
        |         admit_available → admit_opportunity → admit_encounter
        |         (PARTIAL; CURRENT_ACCEPTED actor evidence not compiled)
        +-- RETURN: C9R candidate package (TEST_ONLY; not imported)
        +-- RETURN: C9P historical candidate (non-ancestor)
        ^
C8 durable occurrence + writer/read             [HEAD: none]
        +-- RETURN: C8O c8o_trusted_outbox + read-only consumer
        +-- C8OI holds: D1 old writer, D2 external anchor, D3 ADP019
        ^
C4 historically formed person / genuine other   [HEAD: none]
        +-- RETURN: G17 lab_sgi1 (sourcefree method; G17I RED)
        +-- G18 repair lane assigned
        ^
V3 person/psyche development engine             [MISSING SOFTWARE]
        +-- authority: V3_COMPLETION_IMPLEMENTATION_RULING 49095f763c5c...
        +-- 27 named runtime authorities; no compiled resource
        ^
ADP resources (authority docs)                  [EXISTING RECORDS, NOT COMPILED]
        +-- ADP007 actor init: 28813c57...
        +-- ADP008 phase: 6428e26f...
        +-- ADP010 OEE: f17e2b6b...
        +-- ADP016 memory: 0b7bbe29...
        +-- ADP019 external admission: 5c38772e...
        +-- ADP020 RNG: 1911352f...
        ^
PFF interaction specialization                  [DOC ONLY]
        +-- formal freeze candidate 1d7474ac... says NO_RUNTIME
        +-- File-64 prework d40d19f7...
```

## 2. Actual import edges in the checkout

| From (consumer) | To (producer) | Kind | Status |
|---|---|---|---|
| `rawlsing_next/wsc_gt0_v3_runtime.py` | `v3_psepf_zero_positive_guard` | import | LIVE |
| `rawlsing_next/wsc_gt0_v2_mediation.py` | `wsc_gt0_v3_runtime` | import | LIVE |
| `rawlsing_next/wsc_gt0_end_to_end.py` | `wsc_gt0_v3_runtime` | import | LIVE |
| `rawlsing_next/wsc_gt0_v2_mediation.py` | `m6_actor_safe_expression`, `render_bounded_expression` | import | LIVE |
| `rawlsing_next/render_bounded_expression.py` | `m6_actor_safe_expression` | import | LIVE |
| `rawlsing_next/v3_adp010_oee_executor_obl055_acceptance_bound.py` | `v3_adp010_oee_executor_authenticated` | import | LIVE |
| `rawlsing_next/v3_adp010_oee_executor_obl055_replay_canonical.py` | `v3_adp010_oee_executor_authenticated` | import | LIVE |
| `rawlsing_next/v3_adp010_oee_executor_obl055_replay_reconstructed.py` | `v3_adp010_oee_executor_authenticated` | import | LIVE |
| `rawlsing_next/sdtf_r4_d1_hosting_replay.py` | `sdtf_r4_mechanism_rule_authority_binding` | import | LIVE |
| tests only | `gt34_u2_v3p1_authenticated_subject_materializer`, `gt34_s2...` | import | TEST ONLY |
| tests only | `sdtf_r4_world_response_redrive` | import | TEST ONLY |
| no importer | C9P/C9R/C8O/C0X/G17 candidates | — | RETURN ONLY |

## 3. First actual downstream consumer per candidate

| Candidate producer | First actual consumer found | Is it a person consumer? |
|---|---|---|
| U2 subject materializer | none outside tests; ADP010 `SubjectIngressEvidence` is the designed consumer of a subject_ref but has no CURRENT_ACCEPTED builder | NO — nonactor subject |
| ADP010 OEE executor | OBL055 acceptance/replay modules; tests; no C9/C10 | NO — actor event precursor |
| PSEPF guard | GT0 V3 runtime | NO — safety gate |
| GT0 V3 runtime | V2 mediation and end-to-end harness | NO — zero-effect binding |
| SDTF R4 binder | R4 D1 hosting replay | NO — rule-currentness binder |
| SDTF R4 world redrive | no production consumer | NO — world-response socket |
| M6 actor-safe expression | bounded renderer; V2 mediation | NO — expression, blocked positive |
| Bounded renderer | V2 mediation | NO — blocked positive plan authority |
| U2/S2/ADP010/M6/render | no C12/C10/C9 consumer | — |
| C9R candidate | none | internal test-only pipeline |
| C8O candidate | none | read-only receipt |
| G17 candidate | none | sourcefree lab |

## 4. Exact missing edges (the atlas conclusion)

1. **`GeneratedPersonRecord` producer missing.** No Python object, module or function emits it; no consumer reads it. The M6 field `source_generated_person_record_hash` is an opaque input with no producer.
2. **V3 developmental transition engine missing.** The V3 ruling names the authorities; no implementation applies them to a durable actor state.
3. **C4 independent-person/genealogy producer missing.** No production code; G17 is a sourcefree method candidate and G17I rejected three of its source edges.
4. **C9 native E1/RULE_A/RULE_T/E2 chain missing at HEAD.** ADP010 OEE is a precursor; the C9R full chain is TEST_ONLY and unimported.
5. **C10 coupled consumer missing.** World-only and actor-only receivers exist separately on return branches.
6. **C12 consumer missing.** No code endpoint exists.
7. **C8 production writer/read missing at HEAD.** C8O is a candidate; C8OI holds writer exclusivity, external anchor and ADP019.
8. **PFF runtime missing.** Only conceptual/interface material exists.
9. **Native rule/ADP issuance missing.** CAN008 R2 semantic body is adopted; concrete RULE_A, CAN011 RULE_T, ADP007/010/016/019/020 engines are authority documents without compiled producers (the ADP010 executor is a partial executor, not the issuer).

## 5. Where a lawful first positive could start today

- **Runnable today:** U2 current nonactor subject materialization (exact adopted preimage) and ADP010 asynchronous OEE mechanics with NONCURRENT synthetic evidence. Neither is a person positive.
- **First lawful positive that would change a real consumer:** a source-qualified person/actor state from an implemented V3 developmental engine entering `admit_available` as CURRENT_ACCEPTED, then C9 E1/RULE_A/RULE_T and a named E2 consumer. That producer does not exist; the first required missing function and consumer contract are in `05`/`06`.
