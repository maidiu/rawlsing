# M5 HOSTILE TEST ORACLE

**Contract:** `M5_V3_STRUCTURAL_PEER_PRIOR_SEAM@1.0.0`  
**Expected accepted token:** `M5_ACCEPTED__V3_STRUCTURAL_PEER_PRIOR_SEAM_CLOSED`

Each fixture is normative for the M5 seam.

| ID | Hostile construction | Required result |
|---|---|---|
| M5-H01 | No actual runtime RSC instance; only M4 handoff/signature is supplied | `M5_RSC_RUNTIME_INSTANCE_MISSING`; zero structural-peer effect |
| M5-H02 | Fabricate `context_id`/hash from M4 handoff | reject; stage-close cannot fabricate runtime RSC |
| M5-H03 | Runtime object uses a different RSC schema/version | `M5_RSC_SCHEMA_MISMATCH` |
| M5-H04 | `context_id` or `context_content_hash` mismatch | `M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH` |
| M5-H05 | Recomputed M4 signature differs from transported value | `M5_RSC_SIGNATURE_MISMATCH` |
| M5-H06 | Treat M4 signature as RSC semantic identity | reject; signature is checksum only |
| M5-H07 | Treat a valid M4 signature as permission | reject; signature grants no permission |
| M5-H08 | Repository presence or index/locator hit grants active use | reject |
| M5-H09 | Treat `ACTIVE_CAUSAL` structural eligibility as V3 mutation permission | reject; zero mutation absent owner authority |
| M5-H10 | Resolver use exceeds V557 or producer use | `M5_RSC_PERMISSION_PROOF_INVALID` |
| M5-H11 | Dependency inherits permission from its root | reject; permission is item-wise |
| M5-H12 | V557/V558 locator or governance ID replaces canonical producer ID | `M5_RSC_PRODUCER_BINDING_MISMATCH` |
| M5-H13 | Delete required negative/limit dependency but keep positive root | `M5_RSC_REFERENCE_CLOSURE_INVALID` |
| M5-H14 | Corrupt participant role/cardinality/multiplicity/order in closure | `M5_RSC_REFERENCE_CLOSURE_INVALID` |
| M5-H15 | Put PSEPF in structural repository/RSC semantics | `M5_RSC_FORBIDDEN_REFERENCE_CLASS_PRESENT` |
| M5-H16 | Embed `V3EmpiricalPossibilityInput` in RSC | reject |
| M5-H17 | Embed RSC inside EPI | reject under SCRV3 thin-input contract |
| M5-H18 | Merge RSC and EPI into `GenericPriorBag` | reject identity collapse |
| M5-H19 | Reduce both peers to one scalar/persona vector | reject hidden scalarization |
| M5-H20 | Synthesize PSEPF from structural context | reject structural->empirical synthesis |
| M5-H21 | Assign generated structural position from PSEPF/comparator coordinate | reject empirical->structural actor assignment |
| M5-H22 | Convert source disagreement into actor contradiction/belief conflict | reject |
| M5-H23 | Use provenance reachability as source pooling/composition authority | `M5_RSC_PROVENANCE_AUTHORITY_VIOLATION` |
| M5-H24 | Use matching respondent/display ID as cross-source linkage authority | reject |
| M5-H25 | Direct RSC/EPI to memory | reject; no actor mutation |
| M5-H26 | Direct RSC/EPI to belief or knowledge | reject; no actor mutation |
| M5-H27 | Direct RSC/EPI to relationship truth | reject; no actor mutation |
| M5-H28 | Direct RSC/EPI to action/response/persona/voice | reject; no actor mutation |
| M5-H29 | Named V3 transition consumes a peer with no `V3PeerPriorRequirementDeclaration` | fail closed |
| M5-H30 | Runtime chooses which peer to use merely because one is available/current | reject; availability is not branch authority |
| M5-H31 | Structural peer validates but empirical read permission is absent | structural eligibility remains independent; PSEPF effect is `NO_PSEPF_TRANSITION_EFFECT` |
| M5-H32 | Empirical peer is current but structural permission is denied for a transition requiring structural peer | fail closed for that transition; empirical availability cannot substitute |
| M5-H33 | Structural refresh automatically forces empirical requery | reject; independently governed |
| M5-H34 | Empirical requery/rebind automatically forces structural refresh | reject; independently governed |
| M5-H35 | Replace historical RSC/EPI references in an old receipt with refreshed peers | reject replay laundering |
| M5-H36 | Same RSC/EPI at branch; A gets lawful encounter, B lawful nonoccurrence | divergence permitted if exact causal parentage differs |
| M5-H37 | Same RSC/EPI and distinct recorded lawful ADP-020 decisions | divergence permitted inside preexisting lawful candidates |
| M5-H38 | Same exact authority/history/peer/RNG receipts replay twice | exact deterministic replay required |
| M5-H39 | `persona = f(RSC,EPI)` even with deterministic replay | reject deterministic same-prior same-life collapse |
| M5-H40 | Attempt current PSEPF actor-transition read using old SV3M/SV3F candidate-positive row | reject; current SCRV3 has zero positive actor-transition rows |
| M5-H41 | SCRV3 noncausal exact-geometry dereference at V3M002 | allowed only as validation/dereference; zero actor-transition effect |
| M5-H42 | Treat ActorComparatorReceipt as a peer prior | reject; provenance-only |
| M5-H43 | Treat ReplayReceipt as peer permission or causal prior | reject; audit/replay-only |
| M5-H44 | V2 dereferences RSC/EPI/opaque provenance to alter persona/voice | reject; remains an M6 firewall obligation |
| M5-H45 | Valid actual RSC, exact signature, valid permissions, declared structural use, no actor transition committed | receipt records consultation; actor state remains unchanged |

## Acceptance condition

M5 passes only if every hostile case preserves the three-type noncollapse, permission ceilings, independent currentness and exact-history replay law without inventing a runtime instance or actor-state semantics.
