# RABOCHII B21Q — HB04 COMMON DETERMINISTIC A/B/C HARNESS QUALIFICATION R1

Repository:
`maidiu/rawlsing`

Branch:
`agent/rabochii-subv-b-hb04-common-deterministic-abc-harness-qualification-r1`

Exact starting HEAD:
`64759ea0aa66c70f42dd7a61c85e150ac480d94a`

Do NOT create a new branch.
Do NOT rebase.
Do NOT merge main/PRE-MAIN.

Binding adjudication:
`51_B21_ACCEPTANCE_AND_HB04Q_QUALIFICATION_AUTHORIZATION_R1.md`

Authorized grain:
`B21Q_HB04_COMMON_DETERMINISTIC_ABC_HARNESS_QUALIFICATION_ONLY`

PASS terminal:
`AS4I_COMMON_DETERMINISTIC_ABC_HARNESS_QUALIFICATION_COMPLETE__HB04_CLOSURE_READY`

BLOCKER terminal:
`AS4I_COMMON_DETERMINISTIC_ABC_HARNESS_QUALIFICATION__EXACT_BLOCKER_PROVED`

No tracked implementation or test edits are authorized.

## Frozen qualification authority

HB04 implementation freeze:
`51A_HB04_COMMON_HARNESS_IMPLEMENTATION_FREEZE_R1.json`

Canonical JSON SHA-256:
`138482116b566482075e191800229f81357541d674646552e8c269e7640a755e`

Underlying qualified A/B/C intake freeze:
`49A_HB04_QUALIFIED_ABC_INTAKE_FREEZE_R1.json`

Canonical JSON SHA-256:
`906973f78cd82678f678a9a803bb3c3c7f9e13b30e39a5f8dc3ea093d4390e88`

B21 immutable return:
`4c4d52ec3d9673cbd74778cf60d9c8ac9fc3d714`

B21 semantic implementation:
`51f36497985ba2a0fdf3caae835832b3f66ea897`

B21 authoritative bounded court:
- workflow `34304376739`
- artifact `10086111518`
- digest `sha256:4954c7e2e7c2592704eb001dba3ceca5446c81a5446460c1137f5856ce97bcab`
- court-summary SHA-256 `a08f5e7d26507fc3022e38e890a75ce2801b60f20301228b4a4325b945209bce`

## Frozen implementation/test identities

Verify before every authoritative outer run:

- `rawlsing_next/as4/__init__.py`
  - blob `0a31d52e144e55e0bb0a0f1a637022c2f1536918`
  - SHA-256 `a8becc598142002a3f7c5e3c2fb0cfc80a0249537f84602a1c3237af686cb046`

- `rawlsing_next/as4/loader.py`
  - blob `f608f72f711610ef6d07fd7c96f450a6ba2cac2a`
  - SHA-256 `de31b14fcace34df3f1293e027f14f2c3c75bd942c9b7b27b3eef5b91d8a55c5`

- `rawlsing_next/as4/bounded_fixture.py`
  - blob `caa81812f31347826b9fc0279c0543b8b52c7b99`
  - SHA-256 `d4f5f8c1a3a51d773d5f6ac0b2f06ad8b99a402e1a4e3872d49e17e96d88fd01`

- `rawlsing_next/as4/protocol.py`
  - blob `590da3a2cc54666bd9786130409170b73310a700`
  - SHA-256 `f32bc76346565345042e742f05f195bf8c4ca36b98fd4e7996119e45883a595d`

- `rawlsing_next/as4/run_candidate.py`
  - blob `0acb4cd17906b1c316c5ae381d3214ea98ac5baa`
  - SHA-256 `027cda2dafc0785dbbe52ce83c7aab7c9c1d4b99ca432f632f734c1e30714bfb`

- `rawlsing_next/as4/run_all.py`
  - blob `b7b4c3e8782ac2dc85010e8b3a5afd8e40212edf`
  - SHA-256 `967ae15e54757190c72d2d0aca7b148ae7d1167df221e2719041f3683563ea3f`

- `rawlsing_next/as4/pins/discovery_frontier_authority_snapshot.json`
  - blob `2f2cbce9c9abaa61048424f2191b81b19847ccdd`
  - SHA-256 `bf4c1c3898d1405c1aa28f339fd14da051fc8b386db30f99b2a310aea0e89a24`

- `rawlsing_next/tests/test_as4_hb04_common_harness.py`
  - blob `0333f0133977fcb14d86d41c5d7386836a53aa99`
  - SHA-256 `ca11d17295d3436db08296dc8a9db4cf31c23c127170d2e967fea92d65e72521`

## Required environment

Use CPython 3.13 with:
- `pyarrow==25.0.1`
- compatible pandas

Record exact versions.

## Required outer qualification executions

Run at least TWO genuinely independent clean outer executions.

Each must use:
- a clean exact checkout of the commissioned HB04Q tree;
- distinct TMPDIR/work roots;
- distinct PYTHONPYCACHEPREFIX or equivalent fresh pycache state;
- a distinct Python process;
- no prior test artifacts.

For each outer execution:

### A. Identity gate
Verify:
- exact execution HEAD;
- both freeze canonical SHA-256 values;
- all eight frozen blob and SHA-256 pairs;
- clean pre-execution Git status.

### B. Full frozen pytest court
Run exactly:

`python -m pytest -q rawlsing_next/tests/test_as4_hb04_common_harness.py`

Require:
- 29 passed;
- 0 failed;
- 0 errors;
- 0 skipped;
- no xfail/xpass masking;
- exit 0.

### C. Direct candidate court
Execute separately:
- `run_candidate --candidate A --bounded-fixture`
- `run_candidate --candidate B --bounded-fixture`
- `run_candidate --candidate C --bounded-fixture`

Require all three to reproduce the exact governed semantic projection:

- source `9ced16d5f747b54408d8703e5ca61f485ce7e6e3e046147bdc4ec979a180b8b5`
- I03 fact `bae0b0dbdf5fec58305cbaf583c30e25aae8f07d219350d90425a02df48a2b75`
- I05 frontier `8be39b3ae9e8a2b849ce22480ad0eaea508c6416473d408f38e5652a5b701e85`
- DiscoveryResultReceipt `6704074278d90db80a35038175fa5c5a8598837a541f1322bf62eec93e9f7c36`

Whole candidate receipt hashes may differ because candidate identity and diagnostic measurements are receipted. Semantic/content-addressed projection must be exact.

### D. run_all court
Execute:

`python -m rawlsing_next.as4.run_all --workdir <fresh> --output <fresh>/receipt.json --bounded-fixture`

Require:
- exact order A -> B -> C;
- exactly 3 child processes;
- 3 distinct process IDs;
- sequential no-overlap true;
- every session closed;
- every cleanup PASS;
- scratch removed;
- persistent transformed payload files = 0;
- persistent transformed payload bytes = 0;
- result cache absent;
- ranking logic = 0;
- selection logic = 0;
- comparative early stop = 0;
- real LiTS-I open = 0;
- WVS7 open = 0;
- C09 execution = 0;
- HB05/HB06/HB07 execution = 0.

### E. Hostile court
The full frozen pytest suite must independently reprove all required fail-closed attacks, including:
- wrong intake freeze;
- wrong Route-A pin;
- wrong Route-B production seal/driver pin;
- wrong Route-C intake binding;
- stale/predecessor successor material;
- wrong DA/grammar/frontier/replay;
- missing predicate/query carriers or runtime objects;
- alias/cardinality violation;
- illegal candidate;
- source mismatch;
- extra accelerator/CACC3 request;
- ranking/selection directive.

No validator weakening.

### F. Post-run state
Record:
- clean tracked Git state after execution;
- raw stdout/stderr hashes;
- pytest output hash;
- direct candidate receipt hashes;
- run_all receipt hash;
- semantic projection hash;
- temp/work roots as diagnostic evidence only.

## Cross-run qualification law

Both outer runs must independently PASS.

They must agree exactly on:
- frozen identities;
- loader/successor package identities;
- semantic I03/I05 content-addressed results;
- candidate order/count;
- session/cleanup state;
- hostile dispositions;
- zero prohibited-execution counts.

They may differ only in explicitly diagnostic material such as:
- process IDs;
- filesystem roots;
- timing/RSS/resource observations;
- receipt fields that directly bind those diagnostic values.

Do not rewrite or normalize actual receipts merely to force equality. If useful, emit a separate semantic projection digest.

## Qualification-only hard stops

Do NOT:
- edit any frozen implementation/test file;
- edit A/B/C or shared engine code;
- repair any defect in place;
- open/decode real LiTS-I;
- open/decode WVS7;
- execute C09;
- benchmark or rank A/B/C;
- launch HB05/HB06/HB07;
- launch OBL037;
- select architecture/topology;
- enter positive V3;
- mutate central/PRE-MAIN/main.

If any defect appears, return exact blocker evidence to SUB-VOZHD B.

## Required outputs

Write only under:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B21Q_HB04_COMMON_HARNESS_QUALIFICATION_R1/`

Required:
- `00_RETURN.md`
- `01_FROZEN_IDENTITY_RECEIPT.json`
- `02_OUTER_RUN_1_QUALIFICATION_RECEIPT.json`
- `03_OUTER_RUN_2_QUALIFICATION_RECEIPT.json`
- `04_CROSS_RUN_SEMANTIC_PARITY_AND_HOSTILE_RECEIPT.json`
- `05_HB04_CLOSURE_HANDOFF.json`
- `CHANGED_FILES.txt`

If PASS, `05_HB04_CLOSURE_HANDOFF.json` must mark:
- HB04 qualification ready for SUB-VOZHD closure;
- C09 still not launch-authorized;
- remaining blockers HB01/HB05/HB06/HB07 unchanged unless separately superseded.

No implementation files may appear in the qualification branch net diff.

Return to SUB-VOZHD B.
