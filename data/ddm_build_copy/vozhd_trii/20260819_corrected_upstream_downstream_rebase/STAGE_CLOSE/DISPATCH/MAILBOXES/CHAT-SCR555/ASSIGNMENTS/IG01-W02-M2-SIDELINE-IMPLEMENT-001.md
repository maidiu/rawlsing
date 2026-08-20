# VOZHD TRII — IG-M2 CLEAN SIDELINE IMPLEMENTATION

Assignment ID: `IG01-W02-M2-SIDELINE-IMPLEMENT-001`

Worker #2 — `CHAT-SCR555`  
Worker class: **SUB-VOZHD**  
Most recent submitting agent: `IMPLEMENTATION_GATE_REGENERATION_HARMONIZATION`  
New agent: `IG_M2_SIDELINE_IMPLEMENTATION`

Mission branch: `agent/vozhd-trii-ig-m2-atomic-route`  
Exact branch base / accepted prerequisite: `IG-M1@e5f4871fbdea74bdb1b19067d9161e381ca359ba`  
Original production baseline behind the sideline chain: `main@0777a34e50221bde6801dbaca26c058a7350c9e8`

## Mission

Implement ONLY frozen IG-M2 / V555 atomic-route behavior in the clean sideline machine. Build on the accepted IG-M1 sideline head. Do not modify legacy Rawlsing runtime trees.

Exact frozen route identity, in order:
1. `EXACT_V554_F1_REF`
2. `route_rule_id@route_rule_version`
3. `route_shape_id@route_shape_version`
4. `channel_structural_role_id`
5. `EXACT_STRUCTURAL_CHANNEL_REF`
6. `receiving_constraint_kind`
7. `EXACT_TARGET_RECEIVING_POSITION_REF`

Preserve:
- B1 and F2 are outside route identity and reference-only where governed;
- exactly one accepted V554 F1 per route;
- actor-independent route semantics;
- only `ROUTE_CANDIDATE_AUTHORIZED` is positive route-bearing eligibility for V556;
- typed route states and route-born valid-empty predicates;
- exact canonical route identity reused by V556; no downstream re-ID/reconstruction;
- direct V555 -> V557 path remains lawful when no V556 higher-order meaning is semantically required and permissions permit;
- replay/reference locality and fail-closed exact authority handling.

## Binding authorities

- accepted IG-M1 sideline head: `e5f4871fbdea74bdb1b19067d9161e381ca359ba`
- accepted IG-M1 runtime blob: `e8bd6376720a2de132b384e7771d71d8d39cf261`
- accepted semantic M2 package head: `92128619122886d0ced877a29b42fdb453765246`
- semantic M2 RESULT.json blob: `15ddb28e9fe036f9e5ea5a60a924f549adcccc05`
- semantic M2 contract blob: `cd974b514da5811feab5f7407b64e35cbde0a72c`
- accepted SCR555 local head: `49a9ce7cd830eb670cf1f9d381d4d33e56ddf682`
- harmonized implementation campaign head: `c450fa64cd4da2c15d915fb483cb559840d09dc9`
- implementation DAG blob: `7c02b1af4bd8a2661a56e2e8235a6a080c3a524f`
- final hostile reclosure: `c4a3524f54af368a67ca50ccc85f5d5dca3d803b`
- sideline implementation law blob: `1619b9cf57db8ef4f2d584f998d6faa51b49d688`

## Exact write allowlist

Write ONLY:
- `rawlsing_next/m2_v555_atomic_route.py`
- `rawlsing_next/tests/test_m2_v555_atomic_route.py`

Existing accepted IG-M1 files on the branch are read-only prerequisites.

## Hard prohibitions

- no writes under `data/ddm_build/**`;
- no runtime/test writes under `data/ddm_build_copy/**`;
- no imports of legacy semantic/runtime machinery from either legacy tree;
- no modification of accepted IG-M1 files;
- no IG-M3/M4/M5/M6/render implementation;
- no situated phenomenology/disclosure/salience/inhibition/interlocutor/register invention;
- no semantic-contract or authority changes;
- no deployment, cutover, source retirement, or legacy wrapping;
- no fuzzy/latest/default authority repair.

## Required verification

Run the exact new M2 test file and the accepted M1 test file from this branch. Report command(s), pass counts, and any skipped tests. Verify branch delta against `e5f4871fbdea74bdb1b19067d9161e381ca359ba` contains exactly the two allowed M2 files.

## Finite return tokens

Return exactly one:
- `IG_M2_SIDELINE_IMPLEMENTATION_COMPLETE`
- `IG_M2_SIDELINE_IMPLEMENTATION_RETURN_FOR_HARMONIZATION`
- `IG_M2_SIDELINE_IMPLEMENTATION_AUTHORITY_CONFLICT`
- `BROAD_TOPOLOGY_CONTRADICTION_FOUND`

Return with exact HEAD SHA and concise test/scope evidence. Do not self-launch IG-M3.
