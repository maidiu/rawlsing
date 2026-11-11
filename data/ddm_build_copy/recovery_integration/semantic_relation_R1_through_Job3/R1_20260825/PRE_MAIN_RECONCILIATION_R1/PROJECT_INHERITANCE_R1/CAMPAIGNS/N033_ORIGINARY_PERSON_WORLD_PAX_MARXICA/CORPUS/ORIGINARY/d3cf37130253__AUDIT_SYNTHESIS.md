# R01 Early Foundations / Person-World — Whole-History Conservation Audit Synthesis

## Return status

R01 is **complete for the accessible assigned corpus**, with two explicitly declared Pax-package availability limits rather than silent omission. The worker branch was verified at the required starting HEAD `2e6f39b0c2465e3d2a15788c06ec0ec37f764688` before audit work. The three primary recoverable R01 packages and the sealed historical tree were byte-hashed against the corpus register. All **73/73** pre-April authority-inventory entries are represented in `ARTIFACT_AUDIT_LEDGER.csv`; the May repair pack, harmonized package, relevant historical executable modules, and both Pax lineages are separately inventoried.

This return does **not** select architecture, create a stage, adjudicate Trii versus Chetiri, or enter P10.

## 1. The early Rawlsing capital is real, but it is not one thing

The early lineage contains at least three different kinds of earned capital that later systems can easily conflate:

1. **Empirical/semantic discipline** — exact source/question identity, semantic content identity, driver/content mappings, demographic versus attitudinal classification, sparse-cell handling, proxy/source coverage, and the recognition that scale direction/missingness must be explicit.
2. **Generated developmental and relational machinery** — age-gated drivers, parent/household generation, caregiver relations, needs/strategy feedback, yearly life-course recursion, additive/palimpsestic history, and present-life attention/container state.
3. **Structural-persona ontology** — nested strata/positionality, plural frameworks, awareness/solidarity/viscerality separation, buffers/cracks, derived alienation, and the distinction between structural load and expression.

These layers have different epistemic status. The strongest conservation rule from R01 is therefore not “keep the old person model.” It is: **never let measured social position, generated biography, structural framework availability, awareness, belief, and expression collapse into one another merely because a later compiler can serialize them into the same row.**

## 2. Early semantic-content identity: conceptually important, physically fragmented

The pre-April corpus contains a genuine semantic-content layer:

- `content_keys.csv`: 135 content identities;
- `item_content_map.csv`: 417 item→content mappings, including exact/close/functional relations;
- `questions_master.csv`: 15,615 source-question rows;
- a manually verified WVS7 subset (`WVS7_ITEM_CONTENT_VERIFICATION.md`).

But the implementation is not a coherent universal authority surface. The content map has no populated `scale_transform_id`; many mapped item IDs do not resolve into the archived question master; WVS7 verification is strong but bounded; and `questions_master.content_key` is a source-row identity-like field, not the same ontology as `content_keys.content_id`. A separately required `driver_content_map.csv` is absent from the selected 73-item archive but is recovered in the historical March snapshot, and a later changed copy is present in the sealed tree.

The capital to conserve is therefore the **identity separation and explicit mapping/provenance rule**, not the exact early tables as canonical truth.

## 3. The driver audit is a major negative discovery, not merely an old QA note

`DRIVER_QUESTION_AUDIT.md` demonstrates that a nontrivial set of legacy WVS driver mappings carried the wrong question meanings. It reconstructs WVS7 semantics and explicitly identifies invalid or weak proxies. This matters because it invalidates any conservation strategy that simply preserves driver field names and numeric outputs while losing source-item meaning.

The later WVS item-content verification provides a bounded corrective line, but R01 did not locate a single receipt proving that every corrected driver definition was rerun and promoted across the whole source universe. Accordingly:

- **preserve**: driver-to-source semantic provenance and construct-validity review;
- **do not preserve as authority**: the old WVS driver pairings disproved by the audit;
- **HQ-later burden**: prove the current driver/construct layer descends from corrected source semantics rather than old field labels.

## 4. Sparse demographic inference: preserve loss-of-specificity law, not speculative weights

The early project correctly discovered the sparse-cell problem. `WVS_WEIGHTED_SIMILARITY_SCHEMA.md` proposed dimension weights, but explicitly described them as educated estimates requiring empirical validation. R01 found no evidence that those numerical weights became validated authority.

A different mechanism did become real code: the historical `data_access.py` uses a deterministic microdata-first broadening/walkback path with an explicit minimum-N logic and proxy/fallback behavior. The unified demographic schema also carries an explicit broadening order, although several non-WVS mappings remain TBD/wave-specific.

The conserved function is thus **visible specificity degradation + deterministic fallback/proxy provenance**. The old numeric similarity weights should be treated as unvalidated historical hypotheses unless an independent successor proves them.

## 5. Developmental and relational machinery moved from identified defect to actual implementation

The November unmet-needs analysis is unusually valuable because it records a concrete failure: the child simulation had zero parent relations, needs collapsed, and strategies did not activate adequately. It explicitly says family generation was not implemented in that snapshot.

By the later historical snapshot, that defect had a real implementation lineage:

- `generate_parent_identities()` constructs household context and coupled parent ages;
- `parent_age_model.py` uses explicit priors, plausibility checks and story-reason flags;
- birth-state logic creates parent relational nodes;
- WVS/driver context is mapped into caregiver behavior dimensions;
- `relational_roles.yaml` defines age-indexed caregiver/peer/institution roles;
- needs and strategies use age, relation and structural context;
- `driver_age_schema.py` machine-gates 38 drivers by developmental stage.

R01 replayed the age-gating module in the recovered historical snapshot and observed the staged activation counts expected by its configuration. `test_config_loader.py` also passes 6/6 in that historical snapshot.

This is **real historical implementation evidence**. It is not empirical biography. The code itself contains useful epistemic restraint—for example, parent-age logic says its defaults are global priors rather than country-specific spouse-age truth. That distinction must survive any physical redesign.

## 6. Psychologically rich schemas are the place where Rawlsing most needs epistemic brakes

The Enneagram etiology and parent-child schemas are sophisticated and historically integrated into heuristic code. That does not make them empirical authority. `parent_type_inference.py` explicitly calls its mapping heuristic and converts warmth/authority plus optional driver values into type probabilities.

R01 therefore separates two things:

- **valuable capability**: a generated life may carry provisional developmental hypotheses, and the system can preserve uncertainty rather than assign an unexplained flat type;
- **non-authority**: theory-derived parent→child type causality is not source-bound fact about a person merely because it is coded and numerically normalized.

Any successor must either keep such mechanisms explicitly generative/provisional or retire them. Silent promotion to “known personality” would be information laundering, not conservation.

## 7. Palimpsestic whole-history state is one of the strongest early functions

The recovered `recursion_schema.py` and pipeline wiring show a genuine attempt to prevent the generated person from collapsing into a final-state vector. `RecursionDelta` and `Palimpsest` retain age-indexed layers including needs, strategies, thought rails, authority reception, roles and events. The life-simulation schema then derives current container/season/attention/interactions from that accumulated history.

The strongest underlying obligation is **causal/history accessibility**: a present state should remain intelligible through the generated history that produced it. A modern DAG may represent that history differently, but deleting the dependency/history information because a current scalar can be recomputed would lose person-world capital.

## 8. Structural Persona is conceptually strong, but its historical implementation was not mature enough to canonize

`STRUCTURAL_PERSONA_SCHEMA.md` is explicitly **Provisional v5**. Its strongest conceptual distinctions are nonetheless clear:

- nested material/power strata;
- multiple frameworks with different origins and weights;
- awareness ≠ solidarity ≠ viscerality;
- buffers/cracks between conditions and consciousness;
- alienation as an interpretable vector rather than a free-floating pathology;
- structural load/position does not mechanically determine expression.

Historical v3 code did implement strata/framework/buffer/domain/alienation machinery, and multiple recovered tests pass. It also genuinely executed end-to-end: the recovered snapshot contains 17 numeric `persona_store` runs; inspected store 013 records an 18-year run with parent identity, `year_000` through `year_017` recursion snapshots, final backbone state, derived indices and persona projection. Execution existence is therefore stronger than file-presence inference. But the executable snapshot is internally drifting: the architecture invariant test expects an “immutable” step spine that the config had already expanded by five steps, and another wave4 test has a formatting-contract mismatch. The historical alienation implementation is itself revealing: it simply applies event deltas to the alienation vector and sets structural/affective/institutional dimensions together. The May V503 gate explicitly sought the stronger rule that alienation be derived from A/S/V domains and buffers rather than remain a decorative/free-floating metric. The May repair pack also blocks V5 work on known strata defects and gates framework/load-expression work behind tests.

So R01’s conclusion is intentionally asymmetric: **the conceptual distinctions are stronger than the old implementation’s authority status**. HQ should test whether modern machinery preserves the distinctions, not resurrect the old nine-strata object graph because it existed first.

## 9. `repair_replacement_pack.zip`: strong governance capital, zero completion credit

The May 7 repair pack is internally disciplined. It says:

- v2 remains active runtime until a tested replacement exists;
- v3 is the then-current simulation backbone;
- v5 is a gated trajectory, not a completed engine;
- DONE requires implementation + local tests + relevant full regressions + persisted status evidence;
- generated artifacts cannot become source truth;
- broad exception/fallback behavior at identity/data/LLM/session boundaries must be diagnosed;
- active ontology must have a writer, reader, serializer/use path and tests;
- politically/theologically contested classification requires human authority.

Its own status ledger is decisive: **FX00–FX10 are not started; V500–V508 are locked, blocked, audit-required, or future-decision states.** Therefore the pack is not evidence that those repairs were executed. It is evidence that Rawlsing had learned a governance lesson: conceptual richness without runtime/provenance/test liveness is a defect.

That “no decorative ontology” rule is among the strongest conservation obligations in R01.

## 10. `harmonized.zip` closes V506’s missing-file condition, not V506

The package contains exactly the artifacts V506 had said were missing in the uploaded snapshot:

- `construct_registry.json` — 23 constructs;
- `driver_model.json` — 8 drivers;
- `survey_construct_map.csv` — 91 mapping rows / 22 constructs;
- `questions_master.csv` — 2,690 source-question rows;
- WVS7 source codebook and guide.

So the narrow statement **“survey_construct_map.csv does not exist”** is no longer true for this recovered package.

But the package does not establish runtime integration or promoted authority. More seriously, its guide says Arab Barometer W1/W8, Asian Barometer W1/W6 and Latinobarómetro 1995/2024 were added, while the actual `survey_construct_map.csv` contains only WVS7 W7, Afrobarometer R1/R9 and EVS TREND. The accompanying question master contains the other survey families, so this is not merely a filename mismatch: the guide overstates the map that actually survives.

Therefore R01 records:

> **V506 absence-of-map blocker: partially closed. V506 integration/provenance/coverage/validation gates: not closed.**

There is no packaged construct-coverage validator receipt, runtime import/binding receipt, DriverVector migration proof, reviewer approval, or status-ledger transition.

## 11. Pax Marxica material remains terminal-intent evidence under R01

The first Pax package’s exact zip bytes were not recoverable in the accessible Library/current inputs, but the sealed tree preserves its directory and member hashes: master doctrine, completed-system architecture, strata pressure, absolute horizon, relation-axis target, temporal pressure, and two seed registries. The second V550→Pax execution pack is even better identified: the sealed tree contains an unsuffixed zip with the exact corpus-register SHA plus a complete design-member tree covering sharding, merge, bridge, promotion, tests and a do-not-infer list.

None of this is a completed execution receipt. R01 therefore obeys the mission’s special caution: Pax is historical intent/design unless later evidence proves execution. The concepts can be compared by HQ to modern capabilities; the physical design must not be imported merely because it is ambitious.

## 12. Internal contradictions and currentness failures found

R01 found several concrete reasons not to trust historical “completion” language at face value:

1. `STATUS.md`, `BUILD_STATUS.md`, and `PHASE_STATUS.md` use different readiness frames; formal phases remain not-started/partial while other surfaces say runnable/ready.
2. `DRIVER_QUESTION_AUDIT.md` disproves numerous legacy WVS driver mappings.
3. Early content identity tables are fragmented, and the item-content map has no scale transforms.
4. `harmonized/guide.md` claims mappings absent from the actual mapping CSV.
5. Historical v3 architecture/config tests show step-spine drift; another test shows a formatting-contract mismatch.
6. Independent SES replay in this audit environment cannot proceed because `psycopg2` is absent; the historical reported validation therefore remains bounded recovery evidence, not independently replay-certified by R01.

These are not reasons to discard the lineage. They are exactly why function-level conservation is necessary: the project repeatedly learned that **status, provenance, semantics, implementation and validation are different facts**.

## 13. Strongest R01 conservation obligations for HQ-later testing

Without making a Trii/Chetiri coverage judgment, R01 returns these as the strongest historical demands:

1. Preserve distinct source/question/content/construct identities and explicit alias/transform provenance.
2. Preserve objective-status versus attitude distinctions in demographic/slice authority.
3. Make sparse-slice broadening/proxy use deterministic, typed and visible; never present lower-specificity inference as exact data.
4. Keep developmental availability age-conditioned or provide an explicitly justified successor.
5. Preserve relational and event history sufficient to explain generated person state; a person is not a final vector.
6. Keep population-level source evidence separate from generated individual biography and psychological priors.
7. Preserve the distinction between social position, framework availability, awareness, solidarity/viscerality, belief and expression.
8. Keep buffers/mediation so structure does not mechanically become consciousness or utterance.
9. Derive interpretive fields such as alienation from traceable inputs; do not add free-floating decorative scores.
10. Require every active ontology field to have runtime use, serialization/conservation, provenance where user-visible, and tests.
11. Treat LLM narrative as embodiment of governed/generated state, never as an authority source that backfills missing life history.
12. Treat old Pax designs as intent unless execution is positively proved.

## 14. Exact residual queue

R01 has inventoried the assigned lineage rather than stopping at interesting artifacts. Remaining items are explicit and bounded:

- recover `rawlsing_pax_marxica_2_0_MAX_androidic_pack(1).zip` only if HQ needs content-level intent archaeology beyond the sealed member census;
- retrieve the exact suffixed V550→Pax zip only if filename-level custody matters; its byte identity is already proved by the unsuffixed sealed-tree zip with the same SHA;
- trace later execution receipts for FX/V500–V508, especially V506, only as a **successor proof task**, not as unperformed R01 inventory work;
- trace the corrected driver-set rerun / semantic-master / scale-transform successor chain if HQ needs field-level modern succession proof;
- perform modern Trii/Chetiri coverage adjudication only at HQ, outside R01.

R01 is therefore returning **complete historical archaeology with declared unavailable/deferred successor proofs**, not a claim that all historical functions are live today.
