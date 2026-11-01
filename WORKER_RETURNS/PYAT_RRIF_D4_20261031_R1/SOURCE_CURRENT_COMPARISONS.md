# Source-to-current comparisons

**Current source of truth:** PRE-MAIN `8e44ca9c751049d65e6def47600b5c073ee04b29`.
**Method:** read the six RRIF-C rows, the named source-cut commits and their returns, RRIF-V corrections, current blobs at PRE-MAIN, current tests and static callers. No raw survey, native P07, protected source or actor execution.

Exact blob identity is source identity only. It is not behavioral equivalence, adoption or a live consumer.

## 1. `LIN-F6_HETEROGENEOUS_SYNTHESIS` — ADAPT_REPAIR_CANDIDATE

### Historical source

| Cut | Branch tip | Evidence |
|---|---|---|
| S03 | `69a1686528bb46c2db3051a75710989a46fe5c45` | `rawlsing_next/pre553_heterogeneous_synthesis.py` sha256 `68aba5645bf0b1fa9c26f5a546b6df29a70a9c13a499fae7768a03b59e1de2e0` |
| S03F | `bb739fb6d60b40876566ec6320ff6eec2388e8cf` | joint-domain and leakage repair |
| S03FO | `1428c2e92bce1a49efd87378cb23df936d646dc5` | corrected blob `fc5e37fa5b2f0eb689593b42d95479d1327cb94c`, 22,257 bytes |
| S03R independent | `34cc7bdb28664ecbc707528470c2b4397aa96f12` | complete-tree run 8 pass / 3 fail |
| R26 owner continuation | `6d99650bed01eed8365ec38bd888741a88888a45` | custody correction: actual `fc5e37fa` vs reported `182cc797` |
| R35 F6C | `c1ebe091f` | A vs A0 vs F6M; support-gate defect |
| F6M | `1f1c72f88`; blob `2df811d76db258d98d89ffb43c830cb221ff9a7d` | repaired decision/admission |
| F6P consumer | `7d7ed1cb0`, `016870e86` | sourcefree partial-bound evidence consumer |
| R40 independent F6P | `2e00c8c9e` | ACCEPT at TEST_ONLY grain |

### Current ownership

- `rawlsing_next/pre553_heterogeneous_synthesis.py` is **ABSENT** at `8e44ca9c`.
- No current production import of F6 was found.
- The RRIF-C row's `TEST_IMPORT` at `rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py:15` imports the progressive candidate, not F6. It is not an F6 receiver.
- Current F6 owner and current F6 consumer: **UNKNOWN**.

### Original negative cases

1. **S03R test_01_independent_four_cell_oracle** — failed on the complete S03 tree.
2. **S03R test_07_missing_native_joint_cell_must_not_be_silent_zero** — failed; a missing native joint cell could be manufactured as zero.
3. **S03R test_08_outcome_predicate_requires_tautology_warning** — failed; outcome-as-predicate returned a tautological distribution under a generic supported label.
4. **R35 support-gate renormalization** — A's mixture denominator is taken over eligible sources only. A source stratum failing the support gate has its planned share renormalized onto survivors and the stratum is reported fully covered. W2: A reports uncovered 0 and point `7/10` where F6M reports unknown mass `1/4` and refuses. W7: A reports 0 and `3/5` where F6M reports `1/2` and refuses. A also lacks `PARTIAL_IDENTIFICATION_ONLY` and mislabels W3.
5. **R26 custody correction** — the actual pinned S03FO blob is `fc5e37fa`, not `182cc797`; 250 lines differ and the inherited 24-test suite passes on both, so it is not a custody discriminator.

### Comparative merit

F6M is strictly better than A on support-gate positivity, incomplete-target mass and partial identification. F6P independently tested F6M as a sourcefree consumer. Nonetheless F6M/F6P have no real admitted two-source pair, no real target and no current consumer. A must not be revived. The smallest forward path is an HQ fan-in decision on the exact F6M blob plus F6P, not a re-merge of S03FO.

## 2. `LIN-F7_P07_NATIVE_STAGE_B` — HOLD_UNPROVED

### Historical source

| Cut | Branch tip | Native stage B blob |
|---|---|---|
| HQ244 stage A | `85144216e9ceb58f306d5624620ee42df34d1718` | stage A `c749fb4d6c5c8f1e625c7bed27ede59f7ba80079`; stage B absent |
| HQ245 stage B parity | `0dd0a503882ef777141092d7678285462214a600` | `2d8ffc686fcdb3f7108f0c8bafe7f60273fcf304` |
| HQ246 memory repair | `f09bc827c1a4d77dd2b51834cd5eeeb8969f5b96` | `586f859a4a8710738987f92e5b356451e2390fdd` |
| HQ247 parity/trust repair | `c2c0ab7335a3bcfeabb4297139378e3e657cd432` | `fb5ed13af78672b9d9870b3132787a29d44b928a` |
| HQ248 refcount repair | `8df99878f7947ac7966f0182ddb2c18424c1c9ae` | `253fbafeb5b6596a5afec0354b76b5ca9444baee` |

### Current ownership

- `rawlsing_next/_p07_native_owner_stage_a.c` and `rawlsing_next/_p07_native_owner_stage_b.c` are **ABSENT** at `8e44ca9c`.
- The current Python P07 owner is `rawlsing_next/pre553_source_relations.py` blob `5b67e3f98a5faf95a6c82700af2346fef6e306a5`.
- No current native import, receiver or caller was found.

### Original negative cases

- **HQ246-OPEN-001:** Stage B `decide()` leaked about 15 allocated blocks per call, bisected to the source-ref ordering block; must fix before any adoption.
- **HQ248-OPEN-001:** admission leaks about 10 blocks per admitted relation and about 1 per snapshot; empty construction is clean. Bounded per owner construction, not per decision.
- **HQ246-OPEN-002:** two-candidate `CONFLICTING_AUTHORITY` and precedence ties remain unexercised.
- **HQ246-OPEN-003:** module-init OOM injection was not performed.
- **HQ248:** trusted callables remain **ASSUMED**, not an authentic sealed production TCB. `F7-RR-04G` remains OPEN.

### Comparative merit

Stage B has byte-exact parity on the exercised corpus and stronger in-method checks than stage A, but the admission leak, absent authenticated TCB and unexercised conflict ladder prevent cutover. Native execution/TCB/refcount authority is HELD. The Python owner remains the only current P07 implementation.

## 3. `LIN-F7_SOURCE_RELATIONS` — HOLD_UNPROVED

### Historical source

| Cut | Branch tip | Current path blob |
|---|---|---|
| HQ231 sealed owner state | `d6734e0150e91a60965e7db244ed2ef519ec831c` | `d9fb2c48ff6f2b68b2b8b06a47402c65cf6b7737` |
| HQ235 non-forgeable repair | `c86ae335eaf70e82b5764c46754b16ca7e1587ce` | `8053d30d306a3654ebf563043088311ff390bb2b`; BLOCKED |

### Current ownership

- `rawlsing_next/pre553_source_relations.py` current blob `5b67e3f98a5faf95a6c82700af2346fef6e306a5`.
- Current code is the base Python P07 owner, not the HQ235 hardened variant: HQ235-to-current diff is 240 insertions / 799 deletions. Current is the shorter base and lacks the HQ235 custody anchoring and authenticated entrypoint.
- `rawlsing_next/fiabc_succession_producer.py:59` maps `F008` to the path as a **string only**; it does not import or call the module.
- Only `rawlsing_next/tests/test_pre553_source_relations.py` imports and executes it. No production caller was found.

### Original negative cases

- **HQ235 witness 7:** a caller who substitutes all live anchors and rebinds the ledger in one coordinated step still mints custody. The test `test_hq235_coordinated_multi_anchor_substitution_still_mints_custody` is deliberately asserted `True`. `F7-RR-04G` remains OPEN.
- **Impossibility argument:** only C-level values resist an admitted caller. Custody is an owner-to-material mapping, so it must live in a container; every Python-visible container is caller-rebindable. Anchoring N containers raises the attack from one primitive to N coordinated primitives but does not establish non-forgeability.
- The current blob does not contain the HQ235 custody-anchoring repair. No native opaque handle, IPC boundary or explicit risk downgrade has been adopted.

### Comparative merit

HQ235 closes every single admitted reflection primitive and preserves all five lawful positive paths, but the coordinated substitution still forges custody, so it is not a valid non-forgeable successor. The current base owner is the actual current code but lacks the hardening. The smallest real change is a native opaque capability handle, process/IPC isolation, or an explicit downgrade to "adversarial-single-primitive".

## 4. `LIN-F7_TEMPORAL_COMPARABILITY` — HOLD_UNPROVED

### Historical source

| Cut | Branch tip | Temporal artifact |
|---|---|---|
| HQ211 implementation | `c3db090ff0503963e7914fee740c4b1d17e66cde` | `pre553_temporal_comparability.py` blob `1f0939411a517711d927dd78ef9df81bb22a3176` |
| HQ214 bounded repair | `684a1b202767ad393bcead671a7ad239dabcdb14` | repaired authority binding |
| HQ217 final bounded repair | `136223506eaaf8d7c031a2822f2bfb6ac5bd420e` | six blocking defects closed |
| HQ219 authority chain | `9adc8cc9ba0942db974dddf809206de2a2fd231b` | three authority-chain defects closed |
| HQ222 final authority closure | `a190988b58ae1fe5d6a714e0691b19f84eb4e00e` | four findings closed |
| HQ225 resolver authenticity | `45b721ee13209b9c0d9ecce3023cd1902de21302` | exact concrete resolver type |
| HQ227 full owner path | `d8a03fcdf77ca791d7f66ce58e2ed3b3d894bbb1` | blob `6f6b462b1cdef54d7989f15452473383c1661594` |
| R3 S04 temporal policy | `9ae87f2227384e0567190c6a2d5f3a33a60d4b4c` | `s04_temporal_policy.py` blob `ba0fc3898207d18e177dc33bf929d68739f864f2`; nearest-anchor backoff |
| HQ285 L02 runtime court | `d396b9b3d9bbb4f3b763bb0f00d79276b845ccfe` | S04 17/17 technical; S04R has no runnable suite |

### Current ownership

- `rawlsing_next/pre553_temporal_comparability.py` is **ABSENT** at `8e44ca9c`.
- `rawlsing_next/s04_temporal_policy.py` is **ABSENT** at `8e44ca9c`.
- Current `rawlsing_next/pre553_empirical_authority.py` blob `ca65a7fd4d52f0c44447434559b1d09412e7aa39` has `TEMPORAL_EVIDENCE` at lines 42 and 86. It does **not** have the historical `TEMPORAL_COMPARABILITY` authority kind.
- `rawlsing_next/_pre553_query_common.py:27` imports the current empirical-authority module, not the historical temporal module. This is not a comparability consumer.
- No current consumer of the historical module or S04 was found.

### Original negative cases

- **HQ213:** five pre-repair bypasses minted `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED / INCREASE` with empty authority provenance. HQ214–HQ227 closed them; the final dispositions remained "ready for rereview", not adopted.
- **HQ235 / F7-RR-04G:** lexical custody remains caller-rebindable; temporal custody inherits the same pure-Python owner-boundary limit.
- **S04:** nearest-anchor backoff with an uncalibrated `gap_years * 0.05` drift uncertainty, plus a polarity/3x-jump break heuristic. This is not a population/cohort/weight-comparable trend, has no real-source qualification and was not independently reviewed as a scientific method.
- **S04R:** documentary-only; HQ285 L02 explicitly found no runnable independent temporal hostile suite. The 17/17 S04 result is technical only, not scientific acceptance.
- Preserve the rule: time labels, nearest anchors and interpolation are not comparable trends; missingness and non-comparability remain explicit.

### Comparative merit

The HQ211–HQ227 exact authority chain is materially stronger than S04's interpolation/backoff policy, but it is still blocked by custody and has no consumer. S04 is not fit for population/cohort/weight-comparable trend claims. The smallest next action is a separate decision on exact comparability versus retirement of S04; do not integrate S04 as trend authority.

## 5. `LIN-F8_SERVICE_SOURCE_SCOPE` — CURRENT_RETAINED

### Historical source

| Cut | Branch tip | Binder blob |
|---|---|---|
| HQ254 candidate | `23438ab52f16abda5960a075dfca3f4d3396eab5` | `848d2d0eedb04b792747e9d6aaa49bb39d108a2c` |
| HQ258 exact integration candidate | `f1b65dfaf71e521d3f47c6ba2922a72f60df31f7` | `848d2d0eedb04b792747e9d6aaa49bb39d108a2c` |
| R01 independent review | `f31c6d1394a877d7fa3eec89b678aa0d0f47f6a5` | 16 new / 199 baseline / 215 combined PASS |
| HQ259 adoption | `36c371078edfa3b01e41f38f338ea044f5ee9d1e` | exact reviewed blob adopted |

### Current ownership

- `rawlsing_next/pre553_service_f8_source_scope_binding.py` current blob `848d2d0eedb04b792747e9d6aaa49bb39d108a2c` — exact current and exact reviewed candidate.
- Guard `BINDING_PERMISSION_IDENTITY_MISMATCH` at line 723.
- `rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py:90` imports the binder; calls at lines 659, 879 and 895.
- EE14 ingress has no production caller and remains under `KEEP_EE14_T1_HOLD`. Actual service consumer: **UNKNOWN**.

### Original negative cases

- Pre-adoption mismatch defect: the binder accepted `bound_target_use_permission_refs` that contradicted the receipt `request_key` and copied the divergent set into canonical material. The guard now refuses with `BINDING_PERMISSION_IDENTITY_MISMATCH`.
- R01 OBS_01 duplicate insensitivity remains OPEN. Order-insensitive set equality was deliberately reviewed; duplicate behavior is not settled.
- HQ253 T01 provenance/authority custody gap remains OPEN; this guard does not address it.
- EE14 service use / model-use permission remains HOLD. T1 serving adoption is not claimed.
- The in-file comment still calls the code a quarantined correction. That label is stale relative to the HQ259 exact adoption; the behavior is the reviewed blob.

### Comparative merit

The current blob is byte-identical to the independently reviewed candidate and the exact HQ259 adoption. No divergence or competing successor was found. The guard is refusal-only and grants no permission, ranking, selection, pooling or model use. Retain the exact blob at the narrow binding-coherence grain.

## 6. `LIN-LEARNED_WORLD_PRODUCT` — ADAPT_REPAIR_CANDIDATE

### Historical source

| Cut | Branch tip | Lifecycle blob | Release blob |
|---|---|---|---|
| S06F native B5/M2 | `6187d0a25f98370a3d78371fcdf1752a3b1ec80f` | `1ebf7f9302c46a8e957529b92e60c78493364d78` | `1072fdd2f5d11ebe6e4cffb7df8819af679f0174` |
| S06G atomic repair | `0ff13995cc55db00d02b08004e62f75d4c5cb36e` | `dadf2362f3195c28ebaf97655e28cdba72c04fb3` | `1cb7692399aad8fb272c8c9ce956719527829007` |
| S06FR independent review | `1b5b6072f855a74864c82d0f1b3923327bfb8b99` | test `test_hq284_s06fr_native_review.py` | 111 passed / 3 failed; 12 OBSERVED defect tests |

### Current ownership

- `rawlsing_next/pre553_learned_product_lifecycle.py` current blob `a11c9eb73abab9be118ef4f0b6e325e676059f27` (HQ118).
- `rawlsing_next/pre553_learned_product_release.py` current blob `f76c390665f06ef126968ccf1a6b2d816f43ae92` (HQ118).
- `rawlsing_next/pre553_learned_world_composition.py:33` and `:40` import both owners.
- The composition module has **no production caller**; only its tests import it. Actual consumer: **UNKNOWN**.
- S06G-to-current diff: lifecycle 4 insertions / 545 deletions; release 10 insertions / 155 deletions. Current is the pre-hardening base, not S06G.

### Original negative cases

S06FR is the independent review. Its P1/P2 findings:

1. **Mutable event payload:** `events` and `release_history` expose frozen event objects whose nested `payload` mapping is mutable. Mutating `executor.events[-1].payload` changes the event's content-derived reference while `_events_by_ref` keeps the old key. Reproduced through the public property.
2. **Checkpoint semantic binding:** independently rehashed checkpoints are accepted after changing publication `replay_root_ref`, `determinant_set_hash` or `producer_permission_ceiling` inconsistently with the subject. A rebuild eligibility receipt for release B can link release A's event because only event kind is checked.
3. **Unserialized selection:** two `select_current` calls can both validate the same stale predecessor and both succeed; the resulting history fails cold restore.
4. **Torn mutation:** an injected exception after `_append_events` in `publish_product` leaves a committed publication event with an `UNPUBLISHED` projection and an unrestorable checkpoint.
5. **Helper bypass:** saved `_append_events` accepts an unregistered `PRODUCT_PUBLISHED` event; saved M2 `_insert` inserts a non-`ReleaseCore` without preflight.
6. **M2 check-then-write race:** controlled two-thread scheduling makes both colliding preimages read absence and write; the later value wins.
7. **External authority HOLD:** no independent issuer, authenticated epoch, revocation stream or custody root. `LOCAL_UNAUTHENTICATED` is not protected custody.

S06G repairs the twelve S06FR `OBSERVED` defect-presence assertions. Unfiltered S06G: 187 passed / 14 failed, with 12 obsolete defect assertions and 2 accepted M2 fixture incompatibilities; a separately labeled 14-deselected acceptance selection is green. S06G is not independently reviewed and not adopted.

### Comparative merit

S06G genuinely repairs the twelve observed defects and adds recursive immutability, transactional mutation, serialized selection/M2 writes and checkpoint semantic replay checks. It is the strongest repair candidate, but it is larger than a limited patch and is not independently reviewed. The current owners remain the actual runtime at LOCAL_UNAUTHENTICATED scope. Adapt/repair before any stronger integrity, atomicity or external-custody claim.
