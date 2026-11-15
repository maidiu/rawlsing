# FIABC RUN3 — LITS/B FROZEN OWNER TYPE-UNIVERSE FORENSICS — R1

Status: COMPLETE__FORENSIC_ADJUDICATION_ONLY

Terminal classification:

RUN3_LITSB_VOID_AS_CANDIDATE_EVIDENCE__FROZEN_OWNER_TYPE_UNIVERSE_DEFECT_PROVED

No raw survey artifact was opened or materialized. No Candidate A/B/C execution, measured P2X execution, source-semantic inference, production-code mutation, or governed execution/control branch mutation was performed.

## Executive holding

RUN3 LiTS/B S04 did not establish a Candidate-B architectural failure.

The measured court constructs the projection passed to B as an instance of the canonical current class:

rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection

but load_exact_owner_module("B") executes the exact frozen B owner bytes under the distinct synthetic module identity:

_rawlsing_ee_p2x_owner_b_7c509c2098d0

Those exact frozen bytes themselves define GovernedC11Projection. Therefore the class consulted by B's nominal projection checks is:

_rawlsing_ee_p2x_owner_b_7c509c2098d0.GovernedC11Projection

That class object is necessarily distinct from the canonical current class object used by pre553_carrier_execution.bind_governed_c11_projection. The object supplied by the court therefore fails frozen B's isinstance(projection, GovernedC11Projection) before B can test whether the governed projection or virtual source-backed C11 architecture can operate.

The observed exception text, SourceBackedC11FacadeError("explicit governed projection required"), is exactly the first nominal projection guard reached by build_validated_source_backed_c11_release when build_source_backed_c11_repository receives the current-universe projection.

This is a court deployment/type-universe defect. The S04 result is void as candidate evidence.

## 1. Exact runtime type seam

### 1.1 Measured driver and exact-owner loader

Measured head:

bc832181b4284ac110d2be44fc83504e04de081e

Current driver:

rawlsing_next/ee_p2x_darwin_court_driver.py

Current driver blob:

0c7ace08fc3e8b83c33be7ad795936b42a88fc8c

The owner registry binds Candidate B to:

- owner commit: 0b96b8de9aac774566f872cf0630ebd4ddeb70e6
- owner path: rawlsing_next/pre553_source_backed_c11_facade.py
- owner blob: 7c509c2098d0030f253344eb3f682471378812a8
- builder: build_source_backed_c11_repository

load_exact_owner_module copies the exact owner bytes to:

<work_root>/_exact_owner_modules/0b96b8de9aac774566f872cf0630ebd4ddeb70e6/B/pre553_source_backed_c11_facade.py

and executes them with importlib.util.spec_from_file_location under:

_rawlsing_ee_p2x_owner_b_7c509c2098d0

This behavior is at driver lines 828-842. The synthetic name is not the canonical package name.

### 1.2 Current binder constructs the other class

The accepted P2R1 seam is:

rawlsing_next/pre553_carrier_execution.py

P2R1 seam blob:

e7cda773e6a2426bfa12b22790fd8e005fe75153

That file imports GovernedC11Projection from the canonical current module rawlsing_next.pre553_source_backed_c11_facade. Its bind_governed_c11_projection function enumerates dataclass_fields(GovernedC11Projection), requires an exact complete field set, and returns GovernedC11Projection(**projection_fields).

DriverServices.compose_p2r1_binding, driver lines 820-826, first calls this current bind_governed_c11_projection and only afterward resolves accepted_repository_builder(candidate), which loads frozen B synthetically. It then injects the already-constructed current projection into B's builder kwargs.

Thus the object passed to B is constructed by the canonical current class, not by the frozen owner's class.

### 1.3 LiTS backend confirms the call chain

Current measured backend:

rawlsing_next/ee_p2x_darwin_stage_backend.py

Blob:

1bb84723b2f9c33eedae87736564d36cc9504ff0

For LiTS, _lits_projection deploys the banked LiTS projection builder from commit 3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f, builds the accepted LiTS projection, and verifies cache identity:

84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872

The backend then converts that object to projection_fields using dataclasses.fields. For Candidate B, _compose_lits passes source=incidence and those projection_fields into services.compose_p2r1_binding. The service re-instantiates the fields as the canonical current GovernedC11Projection before invoking frozen B.

There is no path in this call chain that reconstructs the projection as frozen B's synthetic GovernedC11Projection.

### 1.4 Frozen B's nominal requirements

Frozen B blob 7c509c2098d0030f253344eb3f682471378812a8 defines its own GovernedC11Projection at approximately lines 159-215.

Projection-specific nominal guards are:

1. project_c11_candidate_from_physical_cells, lines 295-297:
   if not isinstance(projection, GovernedC11Projection), raise "explicit governed projection required; no semantic inference permitted".

2. build_validated_source_backed_c11_release, lines 348-351:
   if not isinstance(projection, GovernedC11Projection), raise "explicit governed projection required".

3. build_validated_source_backed_c11_release_from_stream, lines 354-357:
   the same nominal requirement.

For a PhysicalSourceIncidence, build_source_backed_c11_repository reaches build_validated_source_backed_c11_release, so the exact RUN3 text "explicit governed projection required" is consistent with the nominal type guard at that boundary.

The frozen B owner also imports PhysicalSourceIncidence and PhysicalCell from the canonical shared physical-decoder module; those types are not redefined in B. The anomalous duplicate is specifically the boundary class that B itself defines.

### 1.5 Class-object proof

The two class objects are distinct under the actual loader by construction.

Current court object:

rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection

Frozen owner guard:

_rawlsing_ee_p2x_owner_b_7c509c2098d0.GovernedC11Projection

Executing the frozen class statement in a second module creates a second Python class object. Neither class subclasses the other. Structural equality of dataclass fields cannot make isinstance(current_projection, frozen_owner_class) true.

Therefore:

- current GovernedC11Projection is frozen B GovernedC11Projection: false;
- isinstance(current_projection, frozen B GovernedC11Projection): false;
- the observed exception is deterministic under the actual deployment design.

No empirical source execution is needed to establish that fact.

## 2. Frozen/current genealogy and a second latent compatibility seam

Frozen Candidate-B facade:

- commit: 0b96b8de9aac774566f872cf0630ebd4ddeb70e6
- blob: 7c509c2098d0030f253344eb3f682471378812a8

Current facade at measured head:

- path: rawlsing_next/pre553_source_backed_c11_facade.py
- blob: 8a761119e4a8d68eb291fc4edfadb52e027f8284

Relevant history:

- 91315bd3df9bd7f5e710d9791cc8be0bb96173fb — initial explicit source-backed C11 facade.
- d37e1d4dc66a9c7bdaa4c14f0ed693d6ce3c89c1 — linear membership/check optimization.
- 0b96b8de9aac774566f872cf0630ebd4ddeb70e6 — accepted A/B owner freeze; B blob remains 7c509c2....
- 7ac1b44a49e54cdd07bbc038fe5d378008e4fbf5 — later current facade adds governed physical-slot owner sets and multi-family owner authority.
- 43c5c937e166a4888201fe73d9d7e057e2629b1d — later current facade adds exact typed physical-value material/binding law using the R5 codec; current blob becomes 8a76111....

The current projection class adds slot_owner_sets. The frozen class does not have that field and rejects any duplicate physical slot across response/coordinate/weight families.

For the accepted LiTS projection actually used here, the banked builder emits q301_2/q301_7 response slots, country/city/region/tablec/tabled coordinate slots, no weight slots, and no slot_owner_sets. Those slot families do not overlap, so the new slot-owner-set field is empty for this LiTS projection. That specific schema extension is therefore not itself evidence that LiTS/B architecture is incompatible.

There is, however, a second latent mixed-version seam that a lawful repair must test rather than hide. Frozen B's physical_value_binding_key hashes canonicalized raw/state/declaration material under the old rule. Current facade code now uses PRE553_PHYSICAL_VALUE_BINDING@2.0.0 plus R5TypedValueCodec material and exact canonical bytes. The current banked projection builder imports physical_value_binding_key from whichever canonical facade is active when it is loaded.

Consequently, merely taking the current projection object's fields and wrapping them in frozen B's top-level GovernedC11Projection class would cure the first isinstance but could leave ResponseValueRule.physical_key values minted by the current helper while frozen B computes cell keys with its frozen helper. That is not a lawful complete repair.

This latent seam does not rescue RUN3 as candidate evidence. RUN3 stopped at the earlier nominal type mismatch and never adjudicated physical-key compatibility.

## 3. Intended frozen-owner law

The repository authority does not support a full transitive freeze of every dependency type, a new serialization protocol, or a structural/duck-typed projection boundary.

The governing arrangement is best classified as E, operationally A-prime:

**Exact candidate-owner bytes are frozen, while the owner composes to the common P2R1 governed projection/runtime seam; owner deployment itself must be semantically transparent and must not create a second incompatible identity for the boundary object.**

Authority:

### P2R1 commission

WORKER_COMMISSIONS/EE-P2R1/00_COMMISSION.md lines 49-57 requires a generic deterministic mechanism that binds an exact GovernedC11Projection from already-accepted semantic/authority objects, with no semantic inference.

Lines 103-113 specify Candidate B composition as:

- exact physical source incidence;
- exact governed C11 projection;
- existing source-backed virtual C11 facade;
- exact runtime object catalog;
- generic I03/I05 runner;

and directs the court to use the current accepted source-backed owner lineage directly.

### P2R1 return

WORKER_RETURNS/EE-P2R1/00_RETURN.md lines 24-37 describes one carrier-neutral contract with complete explicit GovernedC11Projection binding and accepted-owner repository-builder to common-runner composition. It explicitly states that no candidate semantic rule is encoded in the generic seam.

### P2XD commission

WORKER_COMMISSIONS/EE-P2XD/00_COMMISSION.md lines 99-113 fixes the composition order as:

exact preimages -> RuntimeObjectCatalog.from_documents -> bind_governed_c11_projection -> accepted owner -> bind_repository_builder -> CarrierNeutralResearchExecutor

and separately requires an exact deterministic import method for accepted owner bytes. It expressly permits checkout/worktree/PYTHONPATH or another mechanically exact byte mechanism.

The HQ adoption immediately preceding it states at HQ_HANDOFF/EE_P2X_CONTINUATION_REDUCER_ADOPTION_AND_EE_P2XD_COMMISSION_20260918.md lines 54-60 that missing historical owner paths are a **non-semantic deployment issue only**, and that exact owner blobs must be exposed without editing or reproducing their logic.

That language is incompatible with treating a synthetic module-name choice that changes a nominal boundary contract as candidate semantics.

### What is not authorized

A. Frozen owner source sharing common dependency modules/types: substantially yes, but only if the boundary is coherent. This is exactly how frozen A and frozen C imports behave.

B. Full transitive dependency freeze: no repository authority found. P2R1 is explicitly a mixed common seam above frozen candidate-specific physical/C11 owners.

C. Serialize/deserialize the governed projection across the owner boundary: no adopted serialization contract found.

D. Structural protocol/duck typing instead of Python class identity: no authority found. Frozen B explicitly uses nominal isinstance and the commission forbids semantic redesign.

E. Exact owner bytes + common P2R1 seam + semantically transparent deployment: this is the actual adopted law.

## 4. Why RUN3 B is not architecture evidence

The distinction is exact:

A lawful candidate-local architecture failure would require Candidate B to receive the governed projection in the type universe its accepted owner contract requires and then fail while executing its accepted source-backed C11 behavior.

RUN3 did not reach that state.

RUN3 supplied a current-module GovernedC11Projection to a frozen synthetic module that checks against its independently created GovernedC11Projection class. The object is rejected before source-backed projection semantics are exercised.

That makes the failure analogous to a bad ABI boundary: the court handed the candidate an object that is semantically intended to be the required projection but is nominally not an instance of the required boundary type because the court duplicated the type owner during deployment.

The historical P2R6O "A/B owner-seam requalification" does not cure this proof gap. Its return claims both A and B PASS against the common seam, but WORKER_RETURNS/EE-P2R6O/09_AB_OWNER_SEAM_REQUALIFICATION_TEST.py lines 174-186 verifies owner/seam blob identities, preserved historical receipts, matrix labels, and the presence of source-code strings such as build_source_backed_c11_repository and bind_repository_builder. It does not dynamically load frozen B and pass a P2R1-bound projection through B's isinstance guard.

Likewise, the P2XD driver qualification proves exact-byte deployment and blob-drift rejection. The current test at tests/test_ee_p2x_darwin_court_driver.py lines 315-318 deliberately substitutes bad A bytes and confirms rejection; it contains no positive frozen-B/current-projection interoperability test.

So the nominal split was never positively qualified.

## 5. Minimal lawful repair contract

Do not change frozen B semantics. Do not delete or weaken isinstance. Do not monkeypatch its class globals. Do not pass None. Do not infer source semantics. Do not opportunistically alias modules.

The smallest lawful repair is an **exact-owner execution-universe boundary repair** in court deployment infrastructure, with current impact limited to B.

Required contract:

1. Preserve the exact frozen B owner bytes, blob 7c509c2098d0030f253344eb3f682471378812a8.

2. Establish one coherent B owner class universe before repository construction. The accepted B builder and the governed projection supplied to that builder must refer to the same GovernedC11Projection class object.

3. Because B itself owns the class and the physical binding helper, the repair must also establish one coherent B-local facade law for nested projection rules and physical_value_binding_key. Re-wrapping only the top-level current object is insufficient.

4. Construct the B-local projection only from already-accepted LiTS projection authority/preimages. No raw-value inspection, label inference, frequency inference, missingness inference, or outcome-derived repair is permitted.

5. A principled deployment mechanism is a fresh isolated B execution/import environment in which the exact frozen facade bytes occupy their canonical module path before the accepted LiTS projection builder and P2R1 composition components import that path. The P2XD commission explicitly permits mechanically exact checkout/worktree/PYTHONPATH-style deployment. Isolation is mandatory so the repair does not replace the canonical current facade in the parent A/C court process.

6. If current P2R1 code requires an interface member absent from the frozen B facade, that mismatch must fail as a common owner/seam compatibility blocker pending explicit authority. It must not be hidden with setattr, monkeypatching, default insertion, duck typing, or field dropping.

7. Before measured I03 resumes, prove that the reconstructed B projection preserves the accepted LiTS projection identity 84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872 and that the B repository/release closes to the governed C11/oracle identities required by the current court. Any post-repair mismatch is a new adjudicative fact; the present RUN3 failure cannot be reused as that fact.

8. T2/T3/T5, oracle truth, candidate order, candidate semantics, and source authority remain untouched.

This contract is intentionally narrower than freezing all transitive dependencies. It repairs the nominal/physical helper universe at the exact owner boundary and leaves the common PRE553 object/runtime universe shared.

## 6. Candidate A spillover

Frozen A owner:

rawlsing_next/pre553_r5_source_backed_adapter.py

Frozen A blob:

d4915e7e6755ba1850756aebff72f982f73a332b

Unlike B, A does not define GovernedC11Projection. At frozen A lines 20-24 it imports ExactPhysicalCellStream, GovernedC11Projection, and build_source_backed_c11_repository from the canonical rawlsing_next.pre553_source_backed_c11_facade module.

Its builder at lines 336-347 performs isinstance(projection, GovernedC11Projection) against that imported class.

When A is executed under the current synthetic owner name, that import resolves the already-loaded canonical current facade. The current P2R1 binder imports the same canonical current class. Therefore A's nominal projection class and the court's projection class are identical under the current design.

The B type-universe defect is not automatically an A defect.

Mandatory caveat: a B repair must not globally replace the canonical facade in the shared parent interpreter. Doing so could create the very class-universe problem for A that is absent today. This is why B isolation is part of the repair contract.

After A's independent provenance failure is repaired, A still needs a positive regression proving exact class identity and accepted projection passage; current P2XD qualification did not prove that end-to-end boundary.

## 7. Candidate C spillover

Frozen C owner:

rawlsing_next/pre553_route_c_accelerators.py

Frozen C blob:

abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889

The frozen file, like A, imports GovernedC11Projection from the canonical facade rather than defining it.

More importantly, current measured production C does not route the current six-cell source-backed path through the frozen C repository builder. In ee_p2x_darwin_stage_backend._compose_current_candidate_c, the court calls services.load_exact_owner_module("C") to prove/deploy the frozen owner identity, then imports current rawlsing_next.pre553_candidate_c_production_binding and obtains candidate_c_repository_builder_for_source.

That current production binding imports current GovernedC11Projection and current build_source_backed_c11_repository. Its own nominal checks therefore operate in the same current module universe as the current projection.

The module explicitly documents the arrangement: Candidate C's frozen policy identity remains bound in the receipt while empirical semantics stay with the common source-backed C11 facade.

Therefore the observed B defect is not a current C projection-type defect.

Fix classification:

**common court infrastructure, with present runtime impact B-only.**

The exact-owner deployment mechanism is common infrastructure; B uniquely exposes the defect because B's frozen owner file itself defines the nominal boundary class. A and C import that class from the shared canonical facade, and current C production uses a current successor binding.

## 8. Required regression tests

A lawful repair should add all of the following before RUN3/B is re-adjudicated:

1. **Exact B owner byte identity**
   - load/deploy exact commit 0b96... / blob 7c509...;
   - fail on any byte drift.

2. **Positive class identity**
   - prove the projection supplied to frozen B is an instance of the exact GovernedC11Projection class object consulted by B;
   - do not satisfy this by monkeypatching a global.

3. **Negative split-universe reproduction**
   - fixture-load B under the present synthetic identity, construct a canonical-current projection, and prove the nominal mismatch is detected as a court deployment defect, not candidate-local failure.

4. **Complete projection-schema compatibility**
   - compare the exact owner-universe dataclass field contract against the accepted LiTS authority material;
   - extra/missing governed fields must fail closed as common compatibility authority, never be silently dropped/defaulted.

5. **Physical binding-law coherence**
   - with tiny synthetic/fixture physical values only, prove every owner-universe ResponseValueRule.physical_key is generated by the same exact physical_value_binding_key law B uses to classify incoming cells.

6. **Accepted projection identity**
   - owner-universe LiTS projection cache identity must equal 84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872.

7. **Repository-builder boundary**
   - fixture composition through exact P2R1 RuntimeObjectCatalog -> governed projection -> exact B owner -> bind_repository_builder must return a C11Repository and exact release without tripping nominal type guards.

8. **Historical B identity conservation**
   - where the current authority still requires the historical accepted base C11 object, verify C11 logical release e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26, replay identity 6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd, and repository snapshot hash ff8a49d2560fe3cf229f4d5a0f87a14c52d08086a74649968d8c9c9d0225aa77, or explicitly prove the currently governed successor identity where supersession authority says otherwise. No silent substitution.

9. **Parent-process isolation**
   - B deployment must leave the parent process canonical rawlsing_next.pre553_source_backed_c11_facade module and class identity unchanged.

10. **A regression**
    - synthetic frozen A must import the same current GovernedC11Projection class as P2R1 and pass its nominal boundary before its independent provenance logic is assessed.

11. **C regression**
    - current Candidate-C production binding must retain current-class identity; loading the frozen C owner for provenance must not replace or duplicate the class used by current C production.

12. **Qualification depth**
    - replace source-text/grep-only owner-seam evidence with an actual tiny dynamic owner/binder interoperability court. The previous R6O qualification gap must not recur.

No test in this lane may use real source bytes or measured timing.

## 9. Forbidden shortcuts

The following are not lawful repairs:

- deleting or weakening frozen B's isinstance checks;
- duck typing without a new explicit authority;
- passing None;
- skipping projection validation;
- editing/thawing frozen B merely to match the current class;
- assigning frozen B.GovernedC11Projection = current_class at runtime;
- opportunistic sys.modules aliasing in a live shared A/B/C interpreter;
- silently dropping current governed fields to fit the frozen dataclass;
- re-hashing physical keys from observed real source values;
- accepting a different oracle/C11 result merely because the court reaches green;
- changing T2/T3/T5, Lock semantics, candidate definitions, source order, or oracle truth.

## 10. Adjudication

The current court's exact-owner loader preserved B's bytes but changed the nominal identity of a class B itself owns. That deployment choice was not part of B's accepted algorithm and contradicts the governing characterization of owner deployment as non-semantic.

RUN3 LiTS/B therefore has not yet tested whether virtual source-backed C11 can execute the governed LiTS workload. It has tested whether a current-module projection is an instance of an independently redefined synthetic-module class. The answer to that accidental question is no.

Terminal classification:

RUN3_LITSB_VOID_AS_CANDIDATE_EVIDENCE__FROZEN_OWNER_TYPE_UNIVERSE_DEFECT_PROVED
