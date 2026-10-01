# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C1-03R — ASTRA OPTION-A GENERIC LIFECYCLE OWNER EXTENSION — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq151-c1-03r-astra-a-owner-extension-r1`

Exact branch base / Astra decision head:
`b346bd9f7f18b582173a47ca337d468816270c84`

Corrected C1-03R implementation underneath it:
`1f270880f7e3353003ef6199d76d7ff28303301d`

Astra E03 decision:
`WORKER_RETURNS/PYAT-C1-03R-ASTRA-E03-OWNER-GAP-R1/00_DECISION.md`
and
`01_DECISION.json`

Selected decision:
`A__MINIMAL_GENERIC_LIFECYCLE_OWNER_EXTENSION`

This is an implementation commission under the Astra E03 decision. It is not permission for a general lifecycle redesign.

## Reconciled C1 law

Astra correctly reported that the C1 execution spec is absent from this branch ancestry. HQ reconciles that documentary gap here.

Authoritative source:
`integration/pre-main-reconciliation-r1:PYAT_CONTROL_ROOM/OMEGA_VOZHD_ORCHESTRATION_R1/05_C1_EXECUTION_SPEC.md`

Pinned blob:
`f6f0e6624f87c631e3c65b9242cc2c2e7203a61b`

The controlling C1-03 law from that exact blob is:

- AT14–AT19 remain mandatory at the declared C1 scope.
- Register actual determinants across producer and consumer boundaries through the existing lifecycle owner where applicable.
- Mutate one exact determinant and show all and only dependent products invalidate or reidentify; unaffected products remain usable.
- Serialization replay, explanatory replay and fresh empirical recomputation are separate claims.
- Changed meaning, required unavailable authority, or an unrepresentable essential grain routes to Astra with a minimal counterexample.

HQ has now completed that escalation. Astra retained AT19's explicit `replacement or NO_CURRENT` obligation and authorized the bounded generic owner extension below.

## Mission

Implement the smallest generic lifecycle-owner change that can honestly represent:

`AFFECTED_DEPENDENT + NO_LAWFUL_REPLACEMENT => EXPLICIT_NONCURRENT_OUTCOME`

while preserving all existing positive replacement behavior and the corrected C1-03R replay/dependency work.

This must close BOTH:
1. the accepted-owner representational gap; and
2. Astra's newly identified sealed-successor / old-ref-selection defect.

## A. Generic owner-level noncurrent outcome

Modify the accepted owner, not the analytical adapter, to own the negative lifecycle meaning.

The owner contract must support exactly one generic negative lifecycle disposition for an affected dependent with no lawful replacement.

Minimum semantic shape for each noncurrent row:
- exact `old_ref`;
- one fixed typed noncurrent disposition;
- bounded reason code;
- exact supporting evidence/policy refs;
- `replacement_ref: null`.

Do not create C1-specific product vocabulary.
Do not create separate "deferred", "unavailable", "deleted", or similar semantic classes unless Astra explicitly authorized them. It did not.

Meaning:
- the historical artifact remains historically addressable;
- it is not current under the new governed authority release;
- the governing authority itself is not withdrawn merely because the dependent is noncurrent.

### Coverage invariants

For owner-known dependents K, owner-computed affected A and unaffected U, replacement-source set R, and noncurrent-source set N:

- A and U are disjoint and cover K at the owner's declared graph grain;
- R and N are disjoint;
- R union N covers A exactly;
- every affected old ref has exactly one outcome;
- no duplicate, overlap, unknown, or missing affected source is accepted;
- a noncurrent row cannot carry a replacement ref;
- a replacement target must be a lawful materialized exact ref distinct from old ref.

Reject malformed or incomplete outcome sets before committing any release/current-selection mutation.

### Error law

These are NOT automatically noncurrent:
- missing callback;
- callback exception;
- unchanged-ref callback result;
- absent cache/object bytes;
- arbitrary adapter refusal.

They remain errors unless the domain adapter explicitly supplies the bounded reasoned no-lawful-replacement outcome required by the owner contract.

## B. Receipt / serialization / compatibility

Extend the versioned `AuthorityInvalidationReceipt` owner contract with noncurrent-dependent outcomes alongside `recompilation_pairs`.

Canonical owner serialization/hashing must bind:
- changed authorities;
- affected/unaffected refs;
- replacement pairs;
- noncurrent rows and exact grounds.

Preserve existing positive-only receipt identity/behavior through an explicit compatible path if possible. If that is impossible, document and test an explicit migration. Never silently reinterpret historical hashes.

`from_dict(as_dict(x))` and owner checkpoint/export/import must reproduce the negative rows exactly.

Promotion AND rollback share the same outcome law.

Atomicity:
- invalid/missing outcome data commits no release;
- no current authority change;
- no partial dependent-state change.

Later restoration of a noncurrent dependent requires a later lawful transition/receipt; cached bytes alone do not restore currentness.

## C. Current-vs-historical dependent visibility

Provide the minimum owner-owned/publicly auditable mechanism needed for the analytical adapter to distinguish:
- current replacement;
- explicit noncurrent dependent;
- unaffected/current dependent;
- historical exact artifact.

The analytical current-product path must refuse stale historical use as current when the owner recorded noncurrent.

Do not build a new artifact repository. Historical exact lookup may remain with its existing owner; lifecycle currentness must come from the lifecycle owner/receipt, not object presence.

## D. Fix Astra's sealed-successor defect

Astra identified a real defect in the corrected adapter:

Current logic selects changed refs by consumed `(authority_id, authority_version)`, which can select the OLD consumed v1 ref during a v1→v2 transition and pass that old ref to recomposition as though it were the successor.

Repair it.

For the bounded AT19 single-authority transition:
- identify the exact consumed prior authority ref;
- require it to be present in the owner's changed set;
- resolve the unique governed successor/selected ref from the same transition as the exact other ref for that authority identity, not by tuple position and not merely by version label;
- preserve the owner's promotion parent/supersession validation and rollback target-release validation;
- assert the recomposition callback receives the exact sealed/released successor.

Do not change `AuthorityCandidate` hashing or identity semantics.

## E. Repair the AT19 fixture identity proof

`build_model_authority_transition` currently exposes both a separately synthesized revised-model ref and the candidate-derived revision/proposed authority ref. They are not interchangeable.

The corrected court must:
- use the actual candidate→adjudication→seal→release successor;
- bind exact prior parentage/supersession;
- build the consumer model rule from that exact governed successor;
- prove the model-rule hash binds it;
- recompute through the accepted analytical composition path;
- produce the expected new exact product identity even if numerical geometry is unchanged.

Expected-output oracle material must remain separately frozen from candidate output.

If this exposes another genuine owner binding obstruction, stop and return the minimal counterexample. Do not widen AuthorityCandidate or analytical model law.

## F. Required AT19 mixed-outcome witness

In ONE governed source-free release, prove:
- at least one affected dependent receives a real lawful replacement;
- at least one affected dependent receives explicit noncurrent/no-lawful-replacement;
- at least one registered sibling is unaffected and remains identity-stable/current.

Also prove:
- missing cross-owner edge fails closure even if bytes remain cached;
- stale noncurrent historical product cannot be served as current;
- historical exact evidence remains retrievable;
- downstream registered dependents do not receive a replacement built from a noncurrent required input.

## G. Hostiles required by Astra

At minimum:
- forged or missing noncurrent grounds;
- noncurrent row carrying a replacement ref;
- fabricated/stale replacement ref;
- replacement equal to old ref;
- duplicate affected outcome;
- affected outcome missing;
- replacement/noncurrent overlap;
- unknown source ref;
- tampered graph/receipt/release binding;
- callback omission;
- callback exception;
- unchanged callback output;
- partial transition failure proves atomic no-commit;
- cache presence does not restore currentness;
- future authority pre-binding remains forbidden;
- adapter does not compute affected/unaffected or construct the lifecycle receipt itself.

Exercise both promotion and rollback.

## AT18

AT18 replay-grade obligations remain intact.

Do not collapse:
- historical explanation;
- serialization replay;
- fresh-process product replay;
- fresh empirical recomputation.

Fresh owner checkpoint replay is not automatically fresh analytical recomputation.

Preserve the already-correct runner-input/oracle separation.

## Write terrain

You MAY modify only:
- `rawlsing_next/pre553_authority_maintenance.py`
- `rawlsing_next/tests/test_pre553_authority_maintenance.py`
- `rawlsing_next/pre553_analytical_replay_dependency.py`
- `rawlsing_next/tests/test_pre553_analytical_replay_dependency.py`
- `rawlsing_next/tests/c1_at18_at19_fixture.py`
- `rawlsing_next/tests/c1_at18_at19_fresh_process_runner.py`
- `WORKER_RETURNS/PYAT-C1-03R-ASTRA-A-OWNER-EXTENSION-R1/**`

Do NOT modify:
- `rawlsing_next/pre553_replay_audit.py`
- `rawlsing_next/pre553_analytical_composition.py`
- C1-03A terrain;
- N10E/AT17 terrain;
- C5/C7 terrain;
- semantic PRE-MAIN/MAIN.

If the unchanged replay-audit or analytical-composition owner itself blocks the exact Astra-required behavior, return the minimal exact blocker instead of modifying it.

## Required execution

Run exactly the relevant four suites, including all new cases:
- `rawlsing_next/tests/test_pre553_analytical_replay_dependency.py`
- `rawlsing_next/tests/test_pre553_authority_maintenance.py`
- `rawlsing_next/tests/test_pre553_replay_audit.py`
- `rawlsing_next/tests/test_pre553_analytical_composition.py`

Record:
- exact command;
- runtime;
- pass/fail/error/skip counts;
- exit status;
- exact branch/commit;
- independent oracle identity;
- input/implementation/public path/actual output/consumer refs;
- claimed proof grades.

The historical 109-pass run is evidence only and is not the acceptance court for this extension.

## Return

Write only:
`WORKER_RETURNS/PYAT-C1-03R-ASTRA-A-OWNER-EXTENSION-R1/**`

Required:
- `00_RETURN.md`
- `01_OWNER_CONTRACT_AND_COMPATIBILITY.json`
- `02_MIXED_OUTCOME_AT19_RECEIPT.json`
- `03_SUCCESSOR_BINDING_AND_IDENTITY_RECEIPT.json`
- `04_REPLAY_AND_SERIALIZATION_RECEIPT.json`
- `05_HOSTILE_MATRIX.json`
- `06_EXECUTION_RECEIPT.json`
- `07_FINAL_DISPOSITION.json`

Allowed dispositions:
- `PASS_C1_03R_ASTRA_A_OWNER_EXTENSION__INDEPENDENT_REVIEW_REQUIRED`
- `BOUNDED_OWNER_OR_BINDING_GAP__HQ_ADJUDICATION_REQUIRED`
- `ARCHITECTURE_WARRANT`

No merge/self-adoption.

## Absolute prohibitions

No raw survey access.
No new survey/model/comparability authority.
No AuthorityCandidate identity-contract change.
No C1-specific sentinel product.
No fabricated replacement.
No future authority pre-binding.
No inferred dependency.
No adapter-owned lifecycle.
No automatic error→noncurrent conversion.
No C4/C7 work.
No live-occupancy or real-source claim.
No AT33 or multi-conditioner closure claim.
No V3 actor/person implementation.

Terminal:
`C1_03R_ASTRA_A_OWNER_EXTENSION_RETURNED__HQ_ADJUDICATION_REQUIRED`
