# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C1-03R — GENERIC OWNER FAIL-CLOSED CORRECTION — R2
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq155-c1-03r-owner-failclosed-r2`

Exact base:
`eb02332c93c6c3927303eefde9dd9ed768bb3480`

Independent review:
`agent/reviewer-pyat-hq154-c1-03r-astra-a-r1 @ 380a79cde63d9ee239e5812f89283e997e16da96`

Disposition:
`CHANGES_REQUIRED`

This is a narrow generic owner fail-closed repair. Do not reopen Astra Option A, the sealed-successor repair, AuthorityCandidate identity, mixed-witness topology, AT18 grade law, replay audit, or analytical composition.

## Blocking review findings

### RVW-001 — duplicate positive replacement rows

`AuthorityInvalidationReceipt.__post_init__` must reject duplicate source `old_ref` rows in `recompilation_pairs` BEFORE any dict/set canonicalization can silently overwrite one.

Required:
- one affected old ref -> exactly one replacement row OR one noncurrent row;
- duplicate positive source rows reject even if replacement targets are identical;
- duplicate positive source rows reject if targets differ.

### RVW-002 — serialized negative fields/schema ignored

`NoncurrentDependentOutcome.from_dict` must:
- require the `replacement_ref` field to be present;
- require it to be exactly null;
- reject non-null;
- never synthesize null for missing/forged input.

`AuthorityInvalidationReceipt.from_dict` must enforce compatibility boundary:
- if noncurrent rows exist, exact `receipt_schema == PRE553_AUTH40_SEMANTIC_AUTHORITY_INVALIDATION_NONCURRENT@1.0.0` is required;
- missing/forged schema rejects;
- legacy positive-only receipts must continue to deserialize under the historical exact field set and identity;
- incompatible new-schema fields/schema presence on positive-only legacy material must fail closed rather than silently reinterpret.

Embedded record-ref validation remains required but is not sufficient by itself.

### RVW-003 — owner-unknown dependent reported CURRENT

`dependent_lifecycle_status` and therefore `resolve_current_analytical_product` must never grant CURRENT to a dependent ref absent from the owner's `known_dependent_refs`.

Introduce the narrowest typed owner-unknown failure/state consistent with the current owner contract.

Approval law:
- known unaffected/current -> CURRENT;
- known replacement -> exact replacement currentness;
- known explicit noncurrent -> typed noncurrent refusal;
- owner-unknown -> fail typed / NOT GOVERNED, never CURRENT.

Do not infer currentness from cache/object presence.

### RVW-004 — checkpoint replay trusts serialized U

During `AuthorityMaintenanceExecutor.from_checkpoint`, independently recompute BOTH:
- `A = graph.affected(changed)`;
- `U = graph.unaffected(A)`.

Require exact equality with serialized:
- affected_dependent_refs;
- unaffected_dependent_refs.

Thus A and U are disjoint and cover K at replay, not merely at initial production.

A self-consistently rehashed checkpoint with a shrunk/altered U must be rejected.

## Required hostiles

At minimum add courts for:

1. duplicate positive replacement rows, same target;
2. duplicate positive replacement rows, different targets;
3. negative row missing `replacement_ref`;
4. negative row forged non-null `replacement_ref`;
5. negative receipt missing `receipt_schema`;
6. negative receipt forged `receipt_schema`;
7. positive-only legacy receipt remains byte/hash compatible and deserializes;
8. incompatible schema/new-negative fields on positive-only legacy receipt fail;
9. arbitrary owner-unknown dependent lookup does not return CURRENT;
10. cache/object presence does not change owner-unknown result;
11. tampered checkpoint U omits known sibling and is rejected even with self-consistent rehashing;
12. tampered checkpoint U adds/changes unknown sibling and is rejected;
13. promotion normal mixed outcome still passes;
14. rollback normal mixed outcome still passes;
15. sealed-successor/decoy courts remain green;
16. AT18 grade courts remain green.

## Preserve

Must remain accepted:
- exactly one generic noncurrent disposition;
- non-empty exact grounds;
- no DEFERRED/UNAVAILABLE/DELETED split;
- errors never auto-convert to noncurrent;
- positive-only historical receipt identity strategy;
- promotion/rollback shared owner law;
- current vs historical exact distinction;
- sealed successor exact binding;
- decoy is not successor;
- AuthorityCandidate untouched;
- mixed AT19 witness;
- omitted-edge hostile;
- AT18 replay-grade separation;
- `pre553_replay_audit.py` unchanged;
- `pre553_analytical_composition.py` unchanged.

## Write terrain

Modify only:
- `rawlsing_next/pre553_authority_maintenance.py`
- `rawlsing_next/pre553_analytical_replay_dependency.py`
- `rawlsing_next/tests/test_pre553_authority_maintenance.py`
- `rawlsing_next/tests/test_pre553_analytical_replay_dependency.py`
- `rawlsing_next/tests/c1_at18_at19_fixture.py`
- `WORKER_RETURNS/PYAT-C1-03R-OWNER-FAILCLOSED-R2/**`

Do not modify replay audit, analytical composition, C1-03A, AT17, C5/C7, or AuthorityCandidate owner terrain outside the authorized maintenance module.

## Court

Rerun exactly:
- `test_pre553_analytical_replay_dependency.py`
- `test_pre553_authority_maintenance.py`
- `test_pre553_replay_audit.py`
- `test_pre553_analytical_composition.py`

Historical R1:
`144 passed, 0 failed, 0 errors, 0 skipped`.

Record exact new counts and runtime.

## Return

Write:
`WORKER_RETURNS/PYAT-C1-03R-OWNER-FAILCLOSED-R2/**`

Required:
- `00_RETURN.md`
- `01_REVIEW_BLOCKER_DISPOSITION.json`
- `02_SERIALIZATION_AND_COMPATIBILITY_RECEIPT.json`
- `03_CURRENTNESS_AND_CHECKPOINT_RECEIPT.json`
- `04_EXECUTION_RECEIPT.json`
- `05_FINAL_DISPOSITION.json`

Allowed:
- `PASS_C1_03R_OWNER_FAILCLOSED_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`
- `BOUNDED_OWNER_OR_BINDING_GAP__HQ_ADJUDICATION_REQUIRED`
- `ARCHITECTURE_WARRANT`

No merge/self-adoption. No raw source access. No C4/C7. No C1-03 join. No V3.

Terminal:
`C1_03R_OWNER_FAILCLOSED_RETURNED__HQ_ADJUDICATION_REQUIRED`
