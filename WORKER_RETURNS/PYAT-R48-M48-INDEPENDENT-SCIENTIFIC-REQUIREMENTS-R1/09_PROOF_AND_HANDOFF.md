# Sourcefree proof and handoff

Independent scientific freeze: `d58046079707417eddaeeed4343fc9e65a33eb20`. Requirements 00–08 and the frozen oracles precede proof implementation. No R48-A/H conclusions were read afterward either. Supplemental authority note below does not revise the freeze.

Reproduce from repository root:

```sh
python3 WORKER_RETURNS/PYAT-R48-M48-INDEPENDENT-SCIENTIFIC-REQUIREMENTS-R1/proof/verify_packet.py
python3 -m pytest WORKER_RETURNS/PYAT-R48-M48-INDEPENDENT-SCIENTIFIC-REQUIREMENTS-R1/proof/test_constitution.py -q
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint WORKER_RETURNS/PYAT-R48-M48-INDEPENDENT-SCIENTIFIC-REQUIREMENTS-R1/proof/test_constitution.py
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness WORKER_RETURNS/PYAT-R48-M48-INDEPENDENT-SCIENTIFIC-REQUIREMENTS-R1/proof/test_constitution.py.proof.json --root . --receipt /tmp/m48-proof-witness.json
```

The pinned off-base engineering commits must be present in the Git object store for anchor verification; exact full SHAs are in 08. Verification fetches nothing and never reads respondent files. It validates complete blob/SHA256 identity and quoted line spans, not just hash length.

Observed: 14 pytest cases PASS (12 test functions, one three-case topology parametrization); shared AST lint PASS; four named model mutations each baseline PASS → relevant TARGET_ASSERTION_FAILED, source restored by the shared checker. These are the same four model claims, not four extra scientific validation results. Evidence in `evidence/model_tests.xml` and `evidence/proof_witness.json`.

Actual claim: a bounded synthetic metadata grammar distinguishes legitimate composition from naive all-pairs meaning, retains an unlisted minority and zero-unary-signal XOR, and keeps its frontier independent of values. Same marginal tables with different joint configurations remain distinguishable. Unknown routing, no unit linkage, disjoint ballots, unsupported MR/rank/repeat, population measure hold, reverse role denial, empty denominator and unissued all35 counts have observable states. The toy scalar model deliberately reports topology obligations; it does not implement full MR/ranked/repeated native gathering. The complete requirements remain in 02/03 rather than disappearing from scope.

Proof coverage: C01–C04,C06–C08,C10–C16,C21,C23–C26,C28 have bounded model witnesses for at least one part of their stated claim. C05,C09,C17–C20,C22,C27 are specification canaries requiring a source/native or method-specific test during construction; **NOT EXECUTED by M48**. No row in 06 asserts that its named current module was executed here. Particularly, the model's NULL actor field does not prove the original E04/Sorok firewall; E04 is a pinned inspected original consumer, and the historical J42 proof retains its author TEST_ONLY grade.

Not tested by this worker: native I03/I05/E04 integration, original source execution, complete source-item coverage, valid population uncertainty, current source access, F6 target transport, observed temporal estimates, actor transition, N11/N12 acceptance. Existing suites were inspected where relevant, not recounted as freshly passed. No local model test changes original measured occupancy or authenticates a scientific issuer.

## Supplemental inherited evidence

After the requirements freeze, direct Ground R2 and central state inspection reinforced the proposed sample/population separation. The central `WVS7 / HB01 SOURCE-LOCAL 66/66 HQ ADOPTION` records source-local availability of 66 scopes and 97,220 respondent identity/replay at that historical grain, explicitly withholding weighted population, pooling and harmonization use. It retires the old 3/66 population-documentary ceiling **as a source-local runtime gate**. This is stronger evidence against a universal population-certification prerequisite than the S44-specific WVS precedent receipt, whose limit remains valid for its own inspected evidence. Neither record grants fresh M48 source access. Exact supplemental anchors are separate from the first freeze in `evidence/supplemental_anchors.json`.

Ground R2's historical physical no-winner statements predate the later HQD109 selected-B policy; do not revive them as a new A/B/C competition. M48 remains an independent requirements proposal, without project-decision/adoption/closure authority. Relevant inherited open fronts: complete vertical composition, measurement portability, Job3/O12 and claim-specific Field Forge authority. Central state/control files were not modified. No successor was spawned. Return destination is the authorized Pyat HQ's R48 intake, which owns reconciliation and banking; this push alone does not do so.

Highest-yield implementation is the decision-resource materializer plus generic compositional lowerer in 07, followed by one lawfully scoped original consumer effect. The remaining competent decisions are finite D1–D9 kinds, with existing exact decisions reused. No fourth passive permission socket or per-pair semantic signature is scientifically required.

Precision note for continuous variables in 03: a fixed metadata-defined threshold grid yields a fixed exact candidate set. A prospectively specified algorithm that **learns** thresholds can itself be an eligible operation template, but its fitted cutpoints are learned objects, not prospectively known source facts. Retain template identity, fitting/validation partitions and all applicable selection uncertainty. It cannot claim the fixed I05 frontier enumerated those numeric cutpoints before data. Outcome-based threshold fitting cannot secretly redefine eligibility or upgrade validation. The scalar proof covers fixed categorical domains only.

Uninspected capital: user-provided archive tree attachments were not attached to this worker; names alone were not treated as content. No claim of exhaustive Library/private-machine producer search or universal historical code absence is made. Recovery may still find an already complete component. HQ should match it to this function contract and prove the current consuming edge before choosing to rebuild.
