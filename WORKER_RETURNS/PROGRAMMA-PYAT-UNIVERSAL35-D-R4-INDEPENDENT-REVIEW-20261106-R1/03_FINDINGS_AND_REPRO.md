# D r4 — independent governed-wrapper review

## 1. Actual sourcefree positive wrapper works — positive

The production `execute_native_compiler_source` was run on a minimal faithful sourcefree SAV/config, using the actual native fixture bundle, current resolver/decision machinery and current compiler/fact path. The harness supplies only the config/resolution; the compiler and facts are not mocked.

```text
positive PASS {
  selected: ["A","B","Y"], facts: 30, expected_ops: 15,
  expected_candidates: 18, anti: true, op_anti: true,
  native: false,
  compilation_hash: "fdc6f3f98eb7aa1dd7189337106a5444fa1c375449d61e6debc50e708b19eef0",
  ledger_hash: "233d22727027b21a382267422a5f3311ce0b82d0d183e6d2a6023af56f4a66be"
}
```

This is TEST_ONLY_SOURCEFREE, not original facts. It exercises F1 and planned F2/F3H through `bind_governed_frontier` and `execute_governed_frontier`, with typed facts/ledger and no compiler/fact mock.

## 2. Post-execution changed exact decision is accepted — REVISE/HOLD

The resolver call sequence was: same valid decision before decode and after decode, then a third valid-current decision with changed `host` and `metadata_freeze_refs` after the consumer.

```text
positive PASS
changed_after PASS {same compilation/facts/ledger}
revoked_before REFUSED SourceReadAdmissionRefusal SOURCE_READ_REVOKED
revoked_after REFUSED Original35ExecutionError SOURCE_READ_DECISION_NO_LONGER_CURRENT
```

Only currentness/revocation flags are checked after execution (`pre553_original35_execution.py` post-consumer block). They do not prove exact decision equality: changed host/metadata/permission metadata still current is accepted. This is a consequential source-read boundary defect. Pre-IO absent/revoked is refused; post-consumer changed decision is not.

## 3. Held/unselected physical code causes false missing-alias failure — REVISE

`_bundle_with_plan_aliases` loops the **full plan**, while the native bundle contains only selected route-qualified codes. A plan with held `Y` and a selected A/B bundle produces:

```text
HELD_ALIAS_REFUSED Original35OperationError PHYSICAL_CODE_NOT_IN_BUNDLE:Y
```

Unselected/held physical columns must not cause a false missing-alias failure or silently disappear. The alias pass must be limited to selected exact operations, or held/unselected codes must be carried as typed absences without requiring native question refs.

## 4. Extra unplanned frontier is now refused — positive

The earlier extra-operation defect is fixed on this cut:

```text
EXTRA_REFUSED Original35OperationError GOVERNED_FRONTIER_NOT_EXACTLY_PLAN_DERIVED
```

The supplied frontier must exactly match the plan-derived frontier; extras are refused. This is a positive closure.

## 5. Actual 7/694 scope verified; 28 sources have no explicit route frontier

Independent sourcefree R157 full-config measurement:

```text
load_s 27.042; plan_s 5.859; frontier_s 0.799
cpu_user_s 30.569; cpu_system_s 1.122; rss_max_bytes 954,146,816
plan: 35 sources / 18,276 items / 18,413 slots / 18,467 operations
frontier: 7 sources / 694 operations / 683 eligible / 11 held
28 sources: NO_EXPLICIT_PLANNED_FRONTIER
```

Frontier sources: SRC09, SRC10, SRC11, SRC12, SRC13, SRC14, SRC15. This is a different, narrower scope from the prior 991-operation/20-source non-F1 account; the prior historical scope is retained, not falsified. The 35-source no-drop plan and counts remain explicit. No actual all35 candidate facts follow from the symbolic frontier.

## 6. Tests / limits

```text
B operations: 8 passed in 30.56s
D execution: 3 passed in 117.58s
```

The 3 D tests are manifest/path/no-resolver negatives; they do not prove positive wrapper execution. The independent sourcefree positive above does. D actual original facts remain `NOT_COMPLETED`; original source-read decision not supplied; C accepted module unchanged and not rerun.

No original respondent data read, no 600s decode rerun, no whole-estate fixture floor, no product/guide/protected write, no native/science/actor issuance.
