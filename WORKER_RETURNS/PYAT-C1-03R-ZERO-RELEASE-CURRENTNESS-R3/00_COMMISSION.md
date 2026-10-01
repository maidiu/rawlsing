# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C1-03R — ZERO-RELEASE CURRENTNESS CORRECTION — R3
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq157-c1-03r-zero-release-currentness-r3`

Exact base:
`7f64493758f6b3b77d7e9ce1486c1324ff709edc`

Independent rereview:
`agent/reviewer-pyat-hq156-c1-03r-r2-rereview-r1 @ 08b53e8b62ce4dbd04bd47dc2798229ea7dbe0c4`

Disposition:
`CHANGES_REQUIRED`

All prior R2 blockers except one are independently APPROVED. Do not reopen them.

## Sole blocking issue

Reviewer finding:
`F-1`

A dependent ref that appears only in `SemanticDeterminantGraph.known_dependent_refs`, with **zero releases recorded**, is currently returned as:

`CURRENT`

with `governing_release_ref=None`, and `resolve_current_analytical_product` serves it as a current analytical product.

The rereviewer independently established the structural fact:
after any real release, `A ∪ U = K`, so every owner-known dependent is covered by the release and takes an affected/replacement/noncurrent/unaffected branch.

Therefore the `known + latest is None -> CURRENT` branch is reachable only in the zero-release state, exactly where no governing release has established currentness.

## Required correction

In `AuthorityMaintenanceExecutor.dependent_lifecycle_status`:

- owner-unknown ref -> existing typed `NOT_GOVERNED`;
- owner-known ref but **no governing release exists at all** -> typed `NOT_GOVERNED`, not CURRENT;
- current-product resolver must raise the existing typed `OwnerUnknownDependent`/not-governed failure for that zero-release case, unless a more precise already-existing typed not-governed surface is required by current code;
- after a governing release exists, preserve the accepted law:
  - explicit noncurrent -> typed noncurrent refusal;
  - replacement -> CURRENT with exact replacement ref;
  - unaffected -> CURRENT identity-stable.

Do not infer currentness from:
- mere membership in known_dependent_refs;
- cache/object/evidence residency;
- absence of a transition.

The correction must remain attributable to owner governance: CURRENT requires a governing release/outcome.

## Required hostiles

At minimum:

1. known dependent + zero releases -> NOT_GOVERNED;
2. current-product resolution of that case raises typed not-governed failure;
3. same known ref placed in snapshot cache remains NOT_GOVERNED;
4. same known ref placed in evidence cache remains NOT_GOVERNED;
5. unknown ref remains NOT_GOVERNED;
6. after a real release, known unaffected sibling remains CURRENT;
7. after a real release, lawful replacement remains CURRENT with exact replacement;
8. after a real release, explicit noncurrent remains typed noncurrent;
9. mixed promotion witness remains green;
10. mixed rollback witness remains green;
11. RVW-001 duplicate replacement courts remain green;
12. RVW-002 serialization/schema courts remain green;
13. RVW-004 checkpoint A/U replay courts remain green;
14. sealed-successor/decoy courts remain green;
15. AT18 replay-grade courts remain green.

## Preserve as accepted

Do not reopen:
- Astra Option A;
- exactly one generic noncurrent disposition;
- DEFERRED/UNAVAILABLE/DELETED refusal;
- error→noncurrent prohibition;
- duplicate replacement-row rejection;
- negative row/schema fail-closed serialization;
- positive-only historical receipt identity;
- owner-unknown typed NOT_GOVERNED;
- checkpoint A/U exact re-derivation;
- strict refusal of new-schema-with-zero-noncurrent rows;
- sealed-successor repair;
- decoy correction;
- mixed AT19 topology;
- omitted-edge hostile;
- shared promotion/rollback owner law;
- AuthorityCandidate identity;
- AT18 replay grades;
- replay_audit and analytical_composition owner modules.

Record F-2 (unknown extra top-level field dropped/unhashed) as a nonblocking residual; do not broaden into schema-version redesign.

## Write terrain

Modify only:
- `rawlsing_next/pre553_authority_maintenance.py`
- `rawlsing_next/tests/test_pre553_authority_maintenance.py`
- `rawlsing_next/tests/test_pre553_analytical_replay_dependency.py` only if resolver behavior needs a direct court;
- `WORKER_RETURNS/PYAT-C1-03R-ZERO-RELEASE-CURRENTNESS-R3/**`

Do not modify fixture unless genuinely necessary. No replay-audit/composition/C1-03A changes.

## Court

Rerun exactly the same four commissioned suites:
- analytical replay dependency
- authority maintenance
- replay audit
- analytical composition

R2 baseline:
`160 passed, 0 failed, 0 errors, 0 skipped`.

Record final exact counts and runtime.

## Return

Write:
`WORKER_RETURNS/PYAT-C1-03R-ZERO-RELEASE-CURRENTNESS-R3/**`

Required:
- `00_RETURN.md`
- `01_F1_DISPOSITION.json`
- `02_CURRENTNESS_RECEIPT.json`
- `03_EXECUTION_RECEIPT.json`
- `04_FINAL_DISPOSITION.json`

Allowed:
- `PASS_C1_03R_ZERO_RELEASE_CURRENTNESS_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`
- `BOUNDED_OWNER_OR_BINDING_GAP__HQ_ADJUDICATION_REQUIRED`
- `ARCHITECTURE_WARRANT`

No merge/self-adoption. No C1-03 join.

Terminal:
`C1_03R_ZERO_RELEASE_CURRENTNESS_RETURNED__HQ_ADJUDICATION_REQUIRED`
