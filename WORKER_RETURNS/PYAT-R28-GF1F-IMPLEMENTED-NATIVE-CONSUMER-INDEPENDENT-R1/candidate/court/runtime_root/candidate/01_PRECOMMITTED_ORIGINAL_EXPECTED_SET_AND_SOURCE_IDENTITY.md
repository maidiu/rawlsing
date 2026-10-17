# R10 PV2 — precommitted original expected set and source identity

**Committed:** before any accepted-owner Route B / I03 / I05 / P01 call.
**Committed root:** `49f0f51866d3327aca2b7d8910517c0317a85c6b7fd3f011c9ffd6634c6218bf`
**Source-inventory root:** `904f30758890a1a68e6f1ef943e01cd80434ebe6c261e16406a54e19a21ddb16`
**File:** `freezes/01_PRECOMMITTED_ORIGINAL_EXPECTED_SET_AND_SOURCE_IDENTITY.json`
**SHA256 of the frozen payload:** `aa0f5b573fbba3261340210fed7457832073ccdb6b216b136d7143a813a2ba28`

## Shape

* Schema `R10_PV2_ORIGINAL_SCOPE_REGISTER@1.0.0`, origin
  `INDEPENDENT_SOURCEFREE_BEFORE_EXECUTION`, source kind
  `TEST_ONLY_SYNTHETIC_NOT_OBSERVED`.
* 8 obligations = 2 synthetic namespaces × 4 slots.
* 6 RUNNABLE (`PAIR`, `B`, `DISCOVERY` per namespace) and 2 HELD (`ORDERED`,
  hold reason `ORDERED_OWNER_NOT_ISSUED`).
* Every obligation carries the trusted original metadata (form `F1`,
  respondent unit `TEST_ONLY_ADULT`, language `PV2-LANGUAGE`,
  instrument release `INST-<namespace>/F1`, administered occurrence
  `PV2-FIRST-ADMINISTRATION`, option scope), the declared semantic roles and
  condition order, the source-native item order, and the four authorized
  test-only issuer refs.
* The independently spelled source-native inventory covers every native item
  (`X`, `Y`, `O`, `R`) for every respondent (`R1`, `R2`, `R3`) in every
  namespace, including occurrence multiplicity, and is rooted in
  `source_inventory_root`.
* `fixture_use_grant` is TEST_ONLY (`grant`, `issuer`, `SOURCE_FREE_DEV`
  ceiling, `revoked` flag), never a genuine prospective issuance.

## Why a caller cannot relabel or suppress it

1. The register is authored by `author_sourcefree_original_scope_register()`
   from independently spelled literals; it is never reconstructed from an owner
   result or from the candidate fixture.
2. `repro/emit_pv2_register.py` writes the freeze **before** execution and
   self-checks that the committed root reproduces from the authored binding.
3. `run_sourcefree_with_register(expected=..., selected_scopes=..., register=...)`
   takes the register as a **separate** argument, so a candidate supplying its
   own `expected` cannot also supply its own register.
4. `reconcile_expected_against_register` then refuses, before any durable owner
   call, if the complete obligation multiset, per-obligation trusted metadata,
   authorized issuer refs or the declared source inventory differ.

## Gates enforced before execution

| Gate | Error |
|---|---|
| register digest / committed-root reproducibility | `PV2_REGISTER_COMMITTED_ROOT_MISMATCH` |
| fixture-use revocation | `PV2_FIXTURE_USE_REVOKED_BEFORE_EXECUTION` |
| complete obligation multiset (incl. HELD) | `PV2_ORIGINAL_EXPECTED_SCOPE_ANTI_JOIN` |
| trusted metadata binding | `PV2_{FORM,RESPONDENT_UNIT,LANGUAGE,INSTRUMENT_RELEASE,ADMINISTERED_OCCURRENCE,OPTION_SCOPE,SEMANTIC_ROLES,CONDITION_ORDER,SEMANTIC_OP_CLASS,TARGET,SLOT_ITEM,STATE,HOLD_REASON,SOURCE_NATIVE_ITEMS}_BINDING_MISMATCH` |
| authorized issuer refs | `PV2_{ORIGINAL_U,INDEPENDENT_E,CUSTODY,OPERATION_SCOPE}_ISSUER_NOT_AUTHENTICATED` |
| declared source inventory | `PV2_ORIGINAL_SOURCE_INVENTORY_ANCHOR_MISMATCH` |

## Post-execution

* `PV2_SEMANTIC_ROLE_MASK_TOPOLOGY_MISMATCH` /
  `PV2_ROLE_ORDER_TARGET_TOPOLOGY_MISMATCH` — declared roles against the real
  query target order.
* `PV2_CONSUMER_{REVERSED_CONDITIONER_ROLE,CONDITIONER_ITEM_MISMATCH,TARGET_ITEM_MISMATCH,
  UNDECLARED_PARTICIPANT_ITEM,BASE_TOPOLOGY_ORDER_MISMATCH}` — roles against the
  actual Field Forge consumer material.
* `read_current_consumer_material` dereferences current fixture-use permission
  at consumer read.
