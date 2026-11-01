# Selective fan-in proposals — sourcefree candidates only

**Status:** proposals only. No merge, adoption, source-native execution, permission issuance, actor wake or PRE-MAIN mutation. Each proposal requires an independent reviewer distinct from the author and this reconciler. Exact blob identity is not behavioral equivalence.

## P-01 — C3 D01/D02/R5/G01 reconciliation

- **Source cut:** `integration/pyat-hq130-c3-source-free-accepted-r1 @ 30686b185d4ceb2c94f61815ef70d8c8e76255d6`; historical C3/R9 return `24847592f6a40fde3c4932d0f26173012c037078`.
- **Affected paths:** `rawlsing_next/pre553_physical_decoder.py` (modified current), `rawlsing_next/pre553_r5_codec.py` (modified), `rawlsing_next/closed35_g01_sav_numeric_representation_authority.py` (absent); tests for D01/D02/G01 absent.
- **Current receiver:** `rawlsing_next/ee_p2x_darwin_stage_backend.py:713` imports the current decoder; it is not a G01/R9 receiver.
- **Negative tests:** wrong source SHA, held authority, malformed encoding, opaque datetime, G01 numeric representation, D02 traversal, R9 broker/session substitution.
- **Reviewer:** independent C3/physical-source reviewer, not the C3 author or R5 author.
- **Conditions:** sourcefree fixture only; no raw survey/source execution; preserve current R61 decoder if it is the lawful successor; decide whether G01/D01/D02/R9 is missing or superseded before any code proposal.

## P-02 — C1-01 predecessor vs C1-02 current composition

- **Source cuts:** C1-01 `integration/pyat-hq139-c1-01-source-free-accepted-r1 @ 5fafb499d53dddadaf8a7b4fd46506e91a09d270`; C1-02 `integration/pyat-hq145-c1-02-source-free-accepted-r1 @ bc661188b51e995d9f5d74e55c4e37d2ba358a17`.
- **Affected paths:** `rawlsing_next/pre553_analytical_composition.py` (C1-01 not exact; C1-02 exact), `rawlsing_next/tests/test_pre553_analytical_composition.py` (C1-01 absent; C1-02 exact).
- **Current receiver:** `rawlsing_next/pre553_analytical_state_and_route.py:939` imports the current composition owner. This is a real static import, not a behavioral proof.
- **Negative tests:** preimage inversion, wrong release identity, missing predicate custody, C1-02 regression, hash-only synthetic preimage.
- **Reviewer:** independent C1 analytical owner reviewer, not the C1-01/C1-02 author.
- **Conditions:** sourcefree only; no source science or actor authority; decide supersession or retained predecessor before proposing any replacement.

## P-03 — C5/N5 structural-context receiver decision

- **Source cut:** `integration/pyat-hq151-c5-n5-source-free-accepted-r1 @ 151d39260a803635f622323b14e42d96c7976d25`.
- **Affected paths:** `rawlsing_next/current_gt2_structural_context.py` (absent), `rawlsing_next/tests/test_current_gt2_structural_context.py` (absent).
- **Current receiver:** none found. Do not revive the module until a current consumer is named.
- **Negative tests:** context substitution, denominator drift, missing current consumer, source-authority widening, structural-context collapse.
- **Reviewer:** independent GT2/structural-context reviewer plus the actual receiver owner.
- **Conditions:** sourcefree fixture; no raw source; if current service supersedes C5/N5, record supersession with comparative evidence rather than re-merge.

## P-04 — N10E AT17 provider partial retention

- **Source cut:** `integration/pyat-hq147-n10e-at17-source-free-accepted-r1 @ 52e41a41e8bc3b77390016a049095b5aea1721d0`.
- **Affected paths:** `pre553_empirical_possibility_provider.py` (exact), `pre553_analytical_composition.py` (modified/absent), provider test (absent/modified).
- **Current receiver:** `rawlsing_next/pre553_n9_n10w_progressive_candidate.py:55` imports the provider.
- **Negative tests:** wrong source, wrong authority, provider replay/cache tamper, missing live producer pin, status reduction.
- **Reviewer:** independent N10E/AT17 provider reviewer, not the author.
- **Conditions:** sourcefree; no N10W live world or source science; compare provider contract and composition/test surface before any merge.

## P-05 — R157 source configuration, not native U/E

- **Source cuts:** `agent/pyat-pre553-r157-final-review @ d81bc2c67baf933461ae6cfca468f24779cc7e44`; foundation/handback `agent/pyat-pre553-r157-foundation @ 519355ec2215409b40d566ef13c3b21f611e0726`; integration `agent/pyat-pre553-r157-integration @ 056849e23a83d7f4fa33fe4dc8eb65eaf7e2a102`.
- **Affected paths:** 34 code paths, only 4 exact-current, 6 modified, 24 absent; `rawlsing_next/source_configuration/` is the dominant lineage.
- **Current receiver:** `rawlsing_next/source_configuration/cli.py` is an entrypoint; no external current consumer found. This is configuration preparation, not original U/E_pre issuance.
- **Negative tests:** wrong lane routing, unsupported question, unbound source, fixture-as-original, weight authority absent, native U/E absent.
- **Reviewer:** original R157 source-configuration owner plus independent sourcefree reviewer.
- **Conditions:** configuration-only; no raw source or native U/E execution; do not treat 13 inherited lane branches as separate missing capabilities.

## P-06 — SRC04 empirical query / observed response

- **Source cuts:** `agent/pyat-src04-observed-empirical-20261028 @ b6be405899be7fc78a96680f22244aa5b50a2d1e`; carrier review `agent/pyat-src04-actual-carrier-review-20261028 @ 751fece9bf86bd3b1da54b2915876d3e73cea682`.
- **Affected paths:** `rawlsing_next/_pre553_query_common.py`, `_pre553_query_eval.py`, `_pre553_query_predicate.py`, `pre553_empirical_query.py`, `pre553_observed_response.py`; mixed exact/modified/absent.
- **Current receiver:** `rawlsing_next/pre553_carrier_execution.py:21` imports `_pre553_query_common`; this is a real static import.
- **Negative tests:** wrong release, held authority, fixture-as-original, malformed carrier, denominator drift, observed-response promotion.
- **Reviewer:** independent source-native C11/query reviewer, not the SRC04 author.
- **Conditions:** source-native source may be read only within existing authority; no raw respondent data or model-use grant; sourcefree tests first.

## P-07 — HQ282-P01 durable/batch consumer

- **Source cut:** `agent/rabochii-pyat-hq282-p01-v2-durable-consumer-integration-r1 @ 3f91dc22d2eb863bc1d2facccfd33e6c05349503`.
- **Affected paths:** six candidate modules under `rawlsing_next/` are absent: `pre553_batch_durable_checkpoint_candidate.py`, `pre553_governed_batch_checkpoint_integration_candidate.py`, `pre553_original_workload_binder_candidate.py`, `pre553_original_workload_contract_v2_candidate.py`, `pre553_original_workload_v2_verifier_candidate.py`, `pre553_v2_durable_consumer_integration_candidate.py`.
- **Current receiver:** test-only reference; no production consumer found.
- **Negative tests:** duplicate replay, crash/restart, partial checkpoint, forged idempotence, missing real consumer, v2 verifier divergence.
- **Reviewer:** independent HQ282-P01/batch reviewer plus a named receiver owner.
- **Conditions:** sourcefree; no production adoption until the receiver and failure semantics are proven; do not treat all 17 inherited branches as separate candidates.

## P-08 — P07 native owner (hold; do not execute)

- **Source cuts:** `agent/space-bunny-pyat-hq242-f7-t1-native-p07-owner-implementation-r1 @ d6ce7101c76c85bd358b7c59568935ec69dfa912`; stage B `agent/space-bunny-pyat-hq245-f7-native-stage-b-full-p07-parity-r1 @ 0dd0a503882ef777141092d7678285462214a600`.
- **Affected paths:** `pre553_temporal_comparability.py` absent; `pre553_empirical_authority.py` and `pre553_source_relations.py` modified.
- **Current receiver:** no static production receiver found; native P07 remains under authority hold.
- **Negative tests:** OOB, leak, refcount, native parity, decide leak, TCB alias/reliance, forged native stage.
- **Reviewer:** original P07 native owner plus independent native security reviewer; no self-review.
- **Conditions:** no native code execution in this reconciliation; do not merge or revive P07 solely from historical evidence.

## P-09 — B5 owner trust and C1/M2 release binding

- **Source cuts:** `agent/c02e-b5-mandatory-ingress-6b98a6e @ 20213bef82de0f53ef96953ab5dc5c495fdc0257`; `agent/rabochii-pyat-hq282-n04-b5-owner-interface-correction-r1 @ b5a6b6409c765d2aecb8c2f9c9ef9bd8fc6473c2`; `agent/rabochii-pyat-hq280-f8d-c1-m2-owner-binding-candidate-r1 @ 69bb0fc69175b2f6048b00cfa47dc852593798c0`.
- **Affected paths:** B5 mandatory/issuer/separate-principal/owner-held verifier candidates; `pre553_c1_immutable_release_binding.py`. Most are absent; no production receiver found.
- **Negative tests:** forged issuer, cache/token substitution, separated-principal swap, stale release binding, unauthorised M2 registration, self-sealed provenance.
- **Reviewer:** independent security/authority reviewer, distinct from the candidate author.
- **Conditions:** sourcefree only; no issuer permission is created by a code proposal; a real issuer/root remains an owner decision.

## P-10 — F7 temporal and source-relations reconciliation

- **Source cuts:** `agent/rabochii-pyat-hq214-f7-temporal-implementation-repair-r1 @ 684a1b202767ad393bcead671a7ad239dabcdb14`; `agent/rabochii-pyat-hq231-f7-sealed-owner-state-custody-r1 @ d6734e0150e91a60965e7db244ed2ef519ec831c`; `agent/rabochii-pyat-hq235-f7-nonforgeable-custody-binding-repair-r1 @ c86ae335eaf70e82b5764c46754b16ca7e1587ce`.
- **Affected paths:** `pre553_temporal_comparability.py` and `pre553_source_relations.py`; current source relations and temporal authority differ.
- **Current receiver:** `rawlsing_next/_pre553_query_common.py:27` imports empirical authority; source-relations path is referenced from `fiabc_succession_producer.py`.
- **Negative tests:** temporal direction reversal, missing authority chain, resolver authenticity, cross-unit source relation, forged owner state.
- **Reviewer:** independent F7 temporal/source-relations reviewer.
- **Conditions:** sourcefree; no causal/temporal adoption from exact blobs; compare current owner and negative history before any fan-in.

**All proposals:** no production adoption, no merge, no source-native execution, no semantic equivalence claim. A proposal advances only after a named real receiver, exact negative tests and an independent reviewer are present.
