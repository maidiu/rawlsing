# PYAT C1-01 — R8 EXECUTED AT07 RELEASE-SPINE REBASELINE + PREDICATE CUSTODY CLOSURE — R1

Status: ISSUED__CODEX_SOL_HIGH__USER_MAC_AUTHORIZATION_EXPECTED_IN_LAUNCH

Role: Codex implementation + source-free forensic execution worker.

Recommended model:
GPT-5.6 Sol High

Branch:
`agent/codex-pyat-hq137-c1-01-r8-release-spine-rebaseline-r1`

Exact branch base:
`f5c77a8a853c37a2f9fd9cb1e51f2fffb5dd136c`

This base contains:
- exact R7 returned patch and documentary closure;
- exact R7 source-free execution failure return.

Also read the independent R7 review at exact head:
`8d11504d576f2e96b0f7a7ab31795f88f0fe0cfa`

Required review files:
`WORKER_RETURNS/PYAT-C1-01-R7-INDEPENDENT-REVIEW-R1/**`

## Governing findings

R7 static closure succeeded for:
- exact CLOSED 16-key witness owner law;
- literal 16-key witness preimages;
- H1-H5 hostile/reidentification test semantics;
- authority ceiling.

R7 execution at exact tested head:
`0da3c9c13ffd91cf50ab93f6280949eb960792c0`

returned:

`FAIL_SOURCE_FREE_QUALIFICATION`

with:

`48 passed, 10 setup errors, 0 failed tests`

All ten setup errors arise at the shared AT07 fixture assertion:

`source["release_ref"].as_dict() == spine["release_ref"]`

Observed deterministic current C11 release hash:

`dfd6ca5e08d1abe0f1494b4dc0e38869925739cceb306c62a3540922b12ff5b3`

Historical documentary R3 expected release hash:

`8afa807cc06a3a10e660d13bbd831f4f758ae829e835a454c62831bfd8f4d939`

The exact source builder:
`rawlsing_next/tests/test_pre553_empirical_query.py`
has blob:

`cc7d93db1f87d9c311170c229dbe3506937b404a`

both at the historical R3 return and at R7.

The C11 release-owner modules are likewise byte-identical between R3 and R7:

- `rawlsing_next/pre553_c11_ingest.py`
  `37cd35fa2e3420a3eea272a2902e96ab9ba38aba`
- `rawlsing_next/pre553_c11_repository.py`
  `67c6eb6494522cd11aab1b93d0e73f9cef6036f3`
- `rawlsing_next/pre553_c11_integrity.py`
  `7c59aa13a2b7c8e3ab0dc90a1400df645b0b4bbd`
- `rawlsing_next/pre553_empirical_objects.py`
  `a61365b994e5c3c50de0f598fcf40e90abf757b6`

Therefore do **not** treat this as later production drift.

The R3 release identity was frozen at documentary-only grade and C1-01 was not executed there.

The independent R7 review additionally found one documentary custody defect:

the two literal `producer_predicate_hash` values cannot be independently audited from the frozen dependency locator set without reconstructing the producer from test code.

## Mission

Close both current C1-01 blockers in one bounded source-free correction:

1. establish the exact executed AT07 C11 release identity from the unchanged current owner and frozen synthetic fixture;
2. identify precisely why the historical documentary `8afa...` release identity diverges from actual owner output;
3. rebaseline only the synthetic AT07 current identity spine downstream of the executed release identity;
4. freeze immutable producer-predicate preimage custody sufficient to audit both `producer_predicate_hash` values without test-code archaeology;
5. update the active C1-01 source-free test/documentary packet to the executed spine;
6. execute the complete commissioned source-free court and return exact results.

This is a synthetic fixture identity correction.
It creates no real-source authority.

## Critical law: do not force the old release hash

Do not modify the C11 release owner, C11 ingest law, repository law, or shared `_build_source` helper merely to make the old documentary hash `8afa...` reappear.

The current owner is the authority for current executable synthetic release identity unless you discover an actual owner defect with an independent counterexample.

If the executed deterministic release remains:

`dfd6ca5e08d1abe0f1494b4dc0e38869925739cceb306c62a3540922b12ff5b3`

then treat `8afa...` as a historical documentary mis-freeze and supersede it explicitly.

Do not silently rewrite history.

## Stage 1 — exact release-owner forensic receipt

Using the exact frozen AT07 builder and unchanged owner, record the actual current release identity inputs/output.

At minimum record:

- exact source builder blob;
- exact C11 owner blobs above;
- exact universe ref;
- exact AuthoritySnapshot refs used by the candidate;
- source manifest content hash;
- candidate replay manifest semantic_projection_hash;
- replay manifest ref;
- exact M01-M18 coverage mapping;
- final `C11LogicalRelease.release_ref`;
- exact final release hash.

Compare these directly with the historical R3 documentary freeze, especially:

Historical R3 recorded:
- source manifest hash:
  `01ee5fa6db95efad3ce0acecd656f51beb6c2f2e21bc30e49bd358633f9ad6a1`
- candidate projection hash:
  `f0e42f9d04cac4a7f33abf2e3b5fd4392bc85ce3da4ab5489298b50c7ce2bf22`
- replay manifest ref hash:
  `e3791d5f5dfc70849789545e9d08e954c994feaef283953e84151c8f885fe76d`
- release hash:
  `8afa807cc06a3a10e660d13bbd831f4f758ae829e835a454c62831bfd8f4d939`

Do not merely say “different.”
Locate the first identity-bearing divergence and explain the exact missing/wrong documentary preimage assumption.

If the current executed owner unexpectedly reproduces `8afa...` under a complete exact checkout, stop and return the contradictory execution evidence.

## Stage 2 — determine the downstream identity closure

Do not assume every identity changes.

Recompute from actual objects and classify each frozen determinant as:

- unchanged;
- reidentified because release identity is a direct determinant;
- reidentified transitively because a release-bearing replay/fact/query/witness/evidence ref changed.

At minimum adjudicate both forward and reverse:

- producer predicate ref;
- producer predicate_hash;
- producer query ref;
- producer fact ref;
- producer replay ref;
- consumer query ref;
- condition-value witness ref;
- possibility-slice evidence ref;
- final composed result identity;
- any exact dependency/provenance/authority refs that change.

Expected structural fact from current code:
the producer predicate/query definitions do not obviously take `release_ref` as construction input, while I03 execution replay/fact provenance does. Verify rather than assume.

Preserve every unchanged identity exactly.

## Stage 3 — producer predicate custody closure

Create a new R8 documentary artifact that freezes for forward and reverse:

- exact producer predicate ref;
- exact `predicate_hash`;
- complete canonical predicate semantic projection;
- complete canonical predicate AST/preimage;
- all identity-bearing nested refs necessary to independently recompute both:
  - `predicate_hash`;
  - outer `EmpiricalPredicate.ref`.

Bind the source of these materials to immutable code/fixture inputs and the exact executed R8 receipt.

The independent reviewer must be able to audit both predicate hashes without reverse-engineering test helpers.

Do not invent semantic meaning beyond the existing synthetic fixture.

## Stage 4 — R8 current identity packet

Create:

`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8/**`

Required files:

- `00_RETURN.md`
- `01_EXECUTED_RELEASE_OWNER_RECEIPT.json`
- `02_RELEASE_DIVERGENCE_FORENSICS.json`
- `03_PRODUCER_PREDICATE_PREIMAGE_CUSTODY.json`
- `04_CURRENT_AT07_IDENTITY_SPINE.json`
- `05_SUPERSESSION_MAP.json`
- `06_RECOMPUTATION_RECEIPT.json`

The supersession map must preserve historical identities as historical and state why each is or is not superseded.

Never overwrite the R3/R6/R7 historical returns to pretend they had current executed truth.

## Stage 5 — active packet/test correction

Update only the current active C1 packet artifacts that actually contain stale AT07 identities.

You may edit, if required:

`WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/**`

and:

`rawlsing_next/tests/test_pre553_analytical_composition.py`

The test must no longer use the historical R3 documentary release hash as current executable truth.

Prefer loading the R8 current spine explicitly rather than scattering new hash literals.

Keep historical R3/R6/R7 identities available for explicit supersession/non-current assertions where useful.

Preserve:
- R7 exact CLOSED 16-key owner law;
- all H1-H5 hostile courts;
- fixture-only authority ceiling;
- AT07 arithmetic 54/60 and 54/62;
- public I03 producer -> analytical adapter -> public possibility consumer architecture;
- no preconstructed final slice;
- exact denominator/raw support law.

Do not change:
`rawlsing_next/pre553_analytical_composition.py`
unless execution reveals a new owner counterexample unrelated to stale fixture identity.

If any production-owner change appears necessary, stop and return:
`EXISTING_OWNER_CHANGE_REQUIRED`
with exact reproducer.

## Stage 6 — exact source-free execution

The user is expected to authorize Mac use in the launch message.

Use an isolated environment.
Do not open/materialize raw survey files.

Run exactly:

`python -m pytest -q rawlsing_next/tests/test_pre553_analytical_composition.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py`

Record:
- exact tested commit;
- exact relevant blobs;
- environment;
- clean/dirty status before and after;
- exact command;
- exit code;
- pass/fail/error/skip counts;
- full output;
- any failure preimage.

Do not edit tests after observing a failure without first preserving the exact failing run and explaining the correction.

A successful repair must eventually produce a clean exact-patch PASS of this court.

## Write allowlist

You may create/edit only:

1. `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8/**`
2. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/**`
3. `rawlsing_next/tests/test_pre553_analytical_composition.py`
4. `WORKER_RETURNS/PYAT-C1-01-R8-RELEASE-SPINE-REBASELINE-R1/**`

Do not edit historical R2/R3/R4/R5/R6/R7 return artifacts.
Do not edit production C11 owner/helper modules.
Do not edit `rawlsing_next/pre553_analytical_composition.py` absent a newly proved owner counterexample.

## Required worker return

Under:

`WORKER_RETURNS/PYAT-C1-01-R8-RELEASE-SPINE-REBASELINE-R1/**`

Required:

- `00_RETURN.md`
- `01_SCOPE_AND_CHANGED_FILES.json`
- `02_RELEASE_REBASELINE_AUDIT.json`
- `03_DOWNSTREAM_IDENTITY_CLOSURE.json`
- `04_PREDICATE_CUSTODY_AUDIT.json`
- `05_EXECUTION_RECEIPT.json`
- `06_FINAL_DISPOSITION.json`
- full pytest output if execution ran.

Allowed dispositions:

- `PASS_SOURCE_FREE_PATCH_READY__INDEPENDENT_REVIEW_REQUIRED`
- `FAIL_SOURCE_FREE_QUALIFICATION__PATCH_RETURNED_FOR_HQ`
- `EXISTING_OWNER_CHANGE_REQUIRED`
- `COUNTEREXAMPLE_TO_R8_REBASELINE`

## Prohibitions

No raw survey access or materialization.
No Candidate A/B/C.
No measured P2X.
No real-source C11.
No new survey semantics/comparability/model authority.
No C1-02.
No C4.
No PRE-V3 -> V3 actor implementation.

Terminal:

`C1_01_R8_RELEASE_SPINE_REBASELINE_RETURNED__HQ_ADJUDICATION_REQUIRED`
