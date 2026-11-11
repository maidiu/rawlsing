# GT12 E2B R3 — ADOPTED BINDING IMPLEMENTATION R1

## Terminal

`PASS__GT12_E2B_R3_ADOPTED_PUBLICATION_GOVERNANCE_BINDING_IMPLEMENTED__REAL_ENTRY_CALLER_NONSELECTABLE`

## Exact ancestry

Repository:

`maidiu/rawlsing`

Worker branch:

`agent/rabochii-gt12-e2b-r3-adopted-binding-implementation-r1`

Exact required working start, verified identical before implementation:

`8100f700737ce33706b4678974543f7bb8d33569`

Instruction evidence ref:

`0742e9771d559064838d0dad4898bd9f81cd550b`

## Write-ahead checkpoint

First coherent implementation checkpoint:

`257a62896c477a5fd626ed120c4e92bca2e5531c`

That checkpoint added the fixed repo-native adopted current provider before the real-entry/harness/test follow-on work.

## Courted semantic candidate

Exact semantic candidate:

`74011b0feaeca01eb6552c48584f12fc7d1a4c0d`

Court-spec governance commit:

`80c5ca28e65879cba5b3a710892d6061db320845`

## Implementation

### Fixed current provider

Added:

`rawlsing_next/gt12_e2b_publication_governance_binding.py`

Fresh-state blob:

`5c0e730972ca7f31c3be92564c299822c431ccc5`

The provider:

`load_current_gt12_e2b_publication_governance_binding()`

has no arguments.

It embeds the exact HQ-adopted semantic materials and recomputes/fail-closes on all five adopted hashes:

- V554 rule:
  `da431544e57ed4b418cd746be3f0a9aa486cd3c2fb2007a022005821b25e194b`
- publication authority:
  `1b2c1238139287e30acaa418e28967585a34a7fae9c937a9322b7c9e9a76322a`
- V557 current binding:
  `b071d9b34825b2c73fefa47cdef0ba23003d79cf5a2fa78cab802e02ee0cd6f4`
- immutable bundle:
  `f7d4d2313bcc70faf104cff205b0eb7aaa7d88556c895c8ea123a3725105cf14`
- adoption:
  `ff3c0db1ee346b176f240523f36048d88beb6216722988ea087040b4840cd492`

Exact bundle identity:

`GT12_E2B_R3_CURRENT_V554_V557_PUBLICATION_GOVERNANCE_BINDING@1.0.0`

Exact governed use:

`GT12_GT2_Q86B_CONDITIONAL_SUPPORT_Q86A_F1_CONTEXT_PUBLICATION@1`

Exact V554 rule:

`GT12_V554_SIG004_ADMITTED_RELATION_CONTEXT_PUBLICATION_RULE@1.0.0`

Exact publication authority:

`GT12_RELATION_V554_TO_V557_F1_CONTEXT_PUBLICATION_AUTHORITY@1.0.0`

Exact V557 current binding:

`GT12_CAN003_V557_F1_CONTEXT_ONLY_CURRENT_BINDING@1.0.0`

The provider derives:

- `governed_use_id`
- `v554_rule_ref`

from the adopted publication authority and constructs the exact M4 `AuthorityRef` for the adopted V557 binding.

No caller path, selector, rule, family set, permission tuple, or authority override exists.

### Exact publication law enforced

The fixed current provider enforces:

- producer: `V554`
- publisher: `V557`
- decision: `AUTHORIZED`
- allowed publication families: exactly `("F1",)`
- conditions: exactly empty
- route: `V554_TO_V557_DIRECT`
- relation M1 contract:
  `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`
- basis:
  `ADMITTED_FIELD_FORGE_RELATION`
- signature:
  `V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT`

F2/B1 are not authorized publication roots by this binding.

### Exact V557 law enforced

The current binding is exact:

- id:
  `GT12_CAN003_V557_F1_CONTEXT_ONLY_CURRENT_BINDING`
- version:
  `1.0.0`
- hash:
  `b071d9b34825b2c73fefa47cdef0ba23003d79cf5a2fa78cab802e02ee0cd6f4`

Narrowed jurisdiction remains:

- semantic source: accepted `CAN-003 / CAN-003.v1`
- producer family: `V554`
- semantic class: `F1`
- source stage: `M1_RELATION_V554_TO_V557`
- state: `ALLOW_CONTEXT_ONLY`
- allowed uses: exactly `("CONTEXT",)`
- exception: `NO_EXCEPTION_STATE`

The separately adopted PRE-V3->M4 permission translator remains unchanged and distinct.

### Real current entry caller-nonselectable

Updated:

`rawlsing_next/tests/gt12_e2b_actual_object_consumer_harness.py`

Fresh-state blob:

`21c353e9f6de908f95b340cdc49fc50d9af88d14`

Real current API is now exactly:

`run_current_r1c_e2b_actual_objects(query, fact)`

The real entry no longer exposes:

- `governed_use_id`
- `v554_rule_ref`
- `publication_authority`
- `v557_authority_ref`

It loads the fixed adopted current provider internally and mechanically projects all four values into the existing generic lower-level chain.

Generic low-level bridge APIs remain parameterized for generic/non-current contract tests.

## Astra representation repair

The commissioned repair was applied only in:

`require_current_r1c_actual_objects`

Before comparison:

- every element of `query.target_refs` is normalized through `exact_ref(...)`;
- every topology component `target_ref` is independently normalized through the same `exact_ref(...)` representation;
- ordered tuple equality is then required.

This preserves exact:

- kind;
- object ID;
- content hash;
- Q86B -> Q86A order.

No PRE553 semantic projection, canonicalization, identity law, constructor, or hash law was changed.

An actual repo-native current query/fact test loads via:

`load_current_gt2_query_fact()`

and passes only the current-object boundary:

`require_current_r1c_actual_objects(query, fact)`

It does **not** invoke the real E2B terminal chain.

Exact current query/fact identities remain:

- query:
  `e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0`
- fact:
  `540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46`

## Test delta

Added hostile/current-boundary test:

`rawlsing_next/tests/test_gt12_e2b_publication_governance_binding.py`

Fresh-state blob:

`88b3d526b324d53290bb6d161fc5c8b34d3e0acf`

Retired the obsolete R2 blocker expectation in:

`rawlsing_next/tests/test_gt12_e2b_real_current_authority_blocker.py`

Fresh-state blob:

`67107282d87b8c64be28118c6f0d6b204a8c2aa2`

The replacement test now proves the publication-authority seam is fixed at the real entry while generic lower-level APIs remain explicitly parameterized.

## Hostile coverage

The court proves, among other checks:

1. all adopted semantic hash inputs recompute exactly;
2. bundle hash recomputes exactly;
3. adoption hash recomputes exactly;
4. no-argument current provider returns the exact adopted bundle;
5. current provider has no authority/current/path override;
6. governed-use drift fails;
7. V554 rule id/version/hash drift fails;
8. publication-authority hash drift fails;
9. producer/publisher/decision drift fails;
10. empty families fail;
11. any publication family set other than exactly F1 fails;
12. nonempty conditions fail;
13. F2/B1 family injection fails;
14. V557 authority id/version/hash drift fails;
15. REVIEW/ACTIVE_CAUSAL drift fails;
16. V553/V555/V556 drift fails;
17. permission translator remains distinct from V557 authority;
18. real entry signature exposes only query/fact;
19. all four publication/governance values are internally projected from the provider without running the chain;
20. actual repo-native current query/fact pass the repaired current-object boundary;
21. exact current target refs and topology refs compare in Q86B -> Q86A order;
22. inherited reversed-target/risk/negative-state hostile tests remain present and green;
23. inherited M1/V554, D->M4, V557/V558, and current rehydration contracts remain green.

## Governed court evidence

Single proof owner:

`Rabochii Governed Bounded Court`

Draft PR:

`#176`

Base:

`agent/vozhd-gt12-r3-permission-translation-authority-constitution-r1`

Exact base SHA:

`8100f700737ce33706b4678974543f7bb8d33569`

Workflow run:

`33985710005`

Job:

`101358704145`

Protocol self-tests:

`20 passed in 0.09s`

Bounded implementation + hostile + inherited regression court:

`136 passed in 19.44s`

Receipt:

- schema:
  `RABOCHII_BOUNDED_COURT_RECEIPT@1.0.0`
- result:
  `PASS`
- exit code:
  `0`
- semantic candidate SHA:
  `74011b0feaeca01eb6552c48584f12fc7d1a4c0d`
- evidence execution SHA:
  `80c5ca28e65879cba5b3a710892d6061db320845`
- PR synthetic merge SHA:
  `d29cbd1df8e07ae13162108482aae4f82991a730`
- Python:
  `3.12.14`
- determinism:
  `EXACT`
- receipt elapsed:
  `19.66106s`
- spec SHA-256:
  `034cb8d311ddd7cb4421caaee42634cebab508b0dac3a4868a1cf9ec4ae47b27`
- artifact ID:
  `9975087645`

Exact court test files:

1. `rawlsing_next/tests/test_gt12_e2b_publication_governance_binding.py`
2. `rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py`
3. `rawlsing_next/tests/test_gt12_e2b_real_current_authority_blocker.py`
4. `rawlsing_next/tests/test_gt12_e2b_real_current_load_checkpoint.py`
5. `rawlsing_next/tests/test_pre553_repo_native_current_rehydration.py`
6. `rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py`
7. `rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py`
8. `rawlsing_next/tests/test_m4_v557_v558_publication_repository.py`

## Explicit non-actions

- Library access: NO
- source-data access: NO
- empirical reexecution: NO
- real E2B terminal execution: NO
- new authority: NO
- authority redesign: NO
- PRE553 identity-law change: NO
- V553/V555/V556 substitution: NO
- REVIEW grant: NO
- ACTIVE_CAUSAL grant: NO
- actor/V3/V2 authority: NO
- final real E2B terminal: NOT EXECUTED
- final independent GT12 hostile audit: NOT EXECUTED
- PRE-MAIN movement: NO
- main movement: NO

## Final

`PASS__GT12_E2B_R3_ADOPTED_PUBLICATION_GOVERNANCE_BINDING_IMPLEMENTED__REAL_ENTRY_CALLER_NONSELECTABLE`
