# K04 — PRE-V3 objective-position owner-preserving V557/V558 publication implementation — governed return

Status: **PASS — production candidate implemented and producer-side governed court 24/24 PASS**

Terminal:

`K04_PASS__OWNER_PRESERVING_PREV3_OBJECTIVE_POSITION_V557_V558_CARRIER_IMPLEMENTED__24_OF_24_PRODUCER_COURT_PASS__READY_FOR_FRESH_INDEPENDENT_HOSTILE_REQUALIFICATION`

Exact grain:

`PREV3_OBJECTIVE_POSITION_FACT_OWNER_PRESERVING_V557_V558_PUBLICATION_IMPLEMENTATION_R1_ONLY`

Branch:

`agent/rabochii-prev3-w9-k04-position-publication-implementation-r1`

Commission tip:

`e20028326cdf4fa653a54f25b5cf40692799cd90`

Commission blob:

`616c604f75530b16eac8ae9fe5b2c1c831d153b3`

Commission parent / J04 authority commit:

`ed237d2fe31485019b39cd710f117dcdd7e56114`

HQ authority:

`a93e3717d9bea1857937a3fa278a933283948acc`

## 1. Holding

PASS.

K04 implemented J04's exact owner-preserving publication carrier for the independently qualified positive fact:

`PREV3POS:c823a816ce6f71431c99b1a466c7313f3766e5d1e7832fc36b6a31f15835dd02`

No generic M4 root-family whitelist expansion was performed. The shared M4 builder remains closed to `PREV3_OBJECTIVE_POSITION_FACT`; the K04 suite explicitly proves that the generic `build_v557_publication_bundle()` still rejects this root family. The new route is a distinct guarded carrier under the exact J04 authority.

Production candidate:

- commit: `895285f1bff8b5d7c37e52e26e3aed7233097839`
- path: `rawlsing_next/prev3_objective_position_v557_v558_publication.py`
- Git blob: `7d2a5dbb3e0979c599632645867aa48a336a8e79`
- carrier contract: `PREV3_OBJECTIVE_POSITION_FACT_OWNER_PRESERVING_V557_V558_PUBLICATION@1.0.0`
- carrier contract hash: `cb608401080b164ab0c8d9dbb0ffd0efb39b8a1713ac3ca840c279f696f04737`

## 2. Exact owner-preserving carrier law

The carrier preserves without re-identification:

- producer family: `PREV3_OBJECTIVE_POSITION_FACT`;
- semantic class: `PREV3_OBJECTIVE_POSITION_FACT`;
- producer schema: `PREV3_OBJECTIVE_POSITION_FACT@1.0.0`;
- positive state only: `POSITION_FACT_AUTHORIZED`;
- object id: exact `PREV3POS:<semantic_hash>`;
- producer content hash: exact canonical fact-material hash;
- canonical producer dependency set;
- exact negative ceiling as the negative dependency;
- exact valid-time and currentness refs in closure;
- exact evidence/provenance bytes inside the canonical producer payload.

Relabeling as V552/V553/V554/V555/V556 is rejected.

The exact J04 authority remains:

- id: `urn:rawlsing:prev3:authority:v557-publication-family:objective-position-fact:r1`;
- version: `J04@1.0.0`;
- authority material SHA-256: `7cd66ca4f8a413c3ad9bf5559a9b83d34103c421251081dad31aac580813c630`.

## 3. Permission law

The qualified proving fact carries exactly one source-domain use token:

`SECOND_CANARY_CONTRAST_AND_CONDITIONING_POSITION_OPERAND__NATIVE_0_VS_1`

K04 maps that exact token to the coarse M4 atom:

`CONTEXT`

under:

- V557 state `ALLOW_CONTEXT_ONLY`;
- exception state `NO_EXCEPTION_STATE`;
- exact J04 governance authority.

The adapter separately content-addresses the source-domain-use binding. Bare M4 `CONTEXT` is rejected if that exact binding is absent. `REVIEW` is not inferred from M4's coarser state ceiling, and `ACTIVE_CAUSAL` is rejected.

No other source-domain use receives authority in K04 R1.

## 4. V558 / closure behavior

The positive PREV3POS object is the publication root. Its canonical producer dependencies are preserved as exact metadata-only reference objects with exact CAS locators:

`cas://sha256/<dependency-content-hash>`

K04 does not invent immutable dependency payloads from hashes. The repository uses exact dependency-role authentication, exact required reference edges, and exact negative-limit designation. If a dependency body is unavailable or hash-mismatched at actual resolution time, the inherited V558 resolver remains fail-closed.

Exact-resolution only is retained. No latest/default/fuzzy/raw-stage/network repair path is introduced.

Deterministic carrier replay reproduces the exact producer root, governance, publication, root locator, repository, source-domain binding, dependency locators and CAS binding identities.

## 5. Governed producer-side court

Exact test suite:

`J04_PREV3_OBJECTIVE_POSITION_FACT_V557_PUBLICATION_HOSTILE_QUALIFICATION_R1`

Test path:

`rawlsing_next/tests/test_prev3_objective_position_v557_v558_publication.py`

Git blob:

`bf48e285d716d06c2dcedbc4c72231be7c5935cc`

The suite implements the exact J04 H00-H23 requirements as 24 explicit test nodes.

Governed bounded-court execution:

- production semantic candidate: `895285f1bff8b5d7c37e52e26e3aed7233097839`;
- evidence execution SHA: `7258cf26e7820692bc7d1dd0ef284577f9873d52`;
- GitHub Actions run: `34804935155`;
- job: `103854846316`;
- CPython: `3.12.14`;
- deterministic mode: `EXACT`;
- `PYTHONHASHSEED=0`;
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`;
- result: **24 passed in 0.32s**;
- failed: `0`;
- bounded-court receipt result: `PASS`;
- court spec SHA-256: `42889cb033200b3b04ec813888378d7270805fe99b593252c07c520ffe524653`;
- receipt artifact id: `10332598181`;
- receipt artifact ZIP SHA-256: `263ae377deb09f7673d7b982c216679f251504df2637049cfff53662dcfc8e72`.

The court protocol self-test also passed `20/20` before the K04 suite ran.

The temporary draft PR used only to trigger governed execution was PR `#367`. It was closed unmerged after evidence capture. MAIN was not mutated.

The temporary `.rabochii/court_spec.json` trigger was removed after the governed receipt was captured; its historical Git blob is `0d0d1e7958186e19c19c650be3f9b5acc0e479e5` and removal commit is `16ba948a300eb98dc7d258cbd1fdaab1bf3a55d4`.

## 6. H00-H23 disposition

All 24 J04 producer-side requirements passed:

- H00 exact proving fact publishes with unchanged PREV3POS identity and deterministic replay;
- H01-H02 all V552-V556 relabel attempts reject;
- H03-H06 schema/ref/id/hash mutations reject;
- H07 nonpositive position outcome cannot become a positive root;
- H08 source-domain use widening/substitution rejects;
- H09 bare CONTEXT without exact domain-use binding rejects;
- H10 ACTIVE_CAUSAL rejects;
- H11 REVIEW inference rejects;
- H12-H14 dependency/negative-ceiling corruption rejects;
- H15 runtime-clock temporal surrogate rejects;
- H16 present-day persistence substitution rejects;
- H17 evidence/provenance stripping rejects;
- H18 authority-ref mutation rejects;
- H19 latest/default/fuzzy resolution rejects;
- H20 person/V3/psychological use rejects;
- H21 M2/M3 authority inference rejects;
- H22 set-like reordering replays identically;
- H23 V558 locator re-identification rejects.

Exact case ledger:

- `03_J04_H00_H23_CASE_LEDGER.tsv`
- Git blob: `feeba3d11ae233e2a80d5fa81f9134af1a2b84cf`

## 7. Governed return artifacts

- `01_IMPLEMENTATION_RECEIPT.json` — blob `167273cf420424d6bd8e7be19909d0c866980371`
- `02_GOVERNED_TEST_COURT_RECEIPT.json` — blob `33e1f56f89b3b9e4e7c870a0fd290524adc1cf62`
- `03_J04_H00_H23_CASE_LEDGER.tsv` — blob `feeba3d11ae233e2a80d5fa81f9134af1a2b84cf`

## 8. Preserved ceilings

K04 did not:

- mutate MAIN or PRE-MAIN;
- consume sibling ninth-wave returns;
- widen generic M4 root-family authority;
- relabel the fact as V552/V553/V554/V555/V556;
- create a universal position classifier;
- authorize M2 or M3;
- authorize causal use or population generalization;
- infer present-day persistence from current project representation;
- create person-state, belief, motive, trait, preference or psychological semantics;
- revive OBL063 driver/type/person-terminal semantics.

PRE-V3 remains objective-world only.

## 9. Successor gate

K04 is producer implementation + producer-side qualification only.

Central integration is **not** authorized by this return.

The exact candidate is ready for the separately required fresh independent hostile qualification at the J04 authority ceiling. That court must have zero repair authority. Only after independent qualification and HQ adoption may the owner-preserving carrier be centrally integrated.

Terminal:

`K04_PASS__OWNER_PRESERVING_PREV3_OBJECTIVE_POSITION_V557_V558_CARRIER_IMPLEMENTED__24_OF_24_PRODUCER_COURT_PASS__READY_FOR_FRESH_INDEPENDENT_HOSTILE_REQUALIFICATION`
