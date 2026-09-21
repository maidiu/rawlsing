# PREMAIN GUARANTEED-NOT-USED VARIABLE EXCLUSION FRONTIER — R1

**AGENT TYPE: BROWSER / GITHUB / CODEBOOK RESEARCH ONLY**

**MODEL: GPT-5.6 Sol High**

Repository: `maidiu/rawlsing`

Exact sealed base: `445c2fd534db61de0d0d348a6d77a11faa419cc3`

Branch: `agent/rabochii-premain-variable-exclusion-frontier-r1`

Return directory:

`WORKER_RETURNS/PREMAIN-VARIABLE-EXCLUSION-FRONTIER-R1/`

## Hard prohibitions

Do not use the user's Mac/local runtime.
Do not open or materialize raw respondent-level LiTS/WVS SAV/DTA/ZIP/CSV data.
Do not inspect raw response distributions/frequencies to infer semantics.
Do not run Candidate A/B/C.
Do not run measured P2X.
Do not alter FIABC workloads or current semantic authorities.
Do not infer "unused" merely because a variable is absent from the current FIABC proving slice.

You MAY read:
- codebooks;
- variable dictionaries;
- source metadata registries;
- source/question mapping CSVs;
- semantic authority ledgers;
- questionnaire/instrument documentation;
- Long Memory / PRE-MAIN / Field Forge / V3-boundary documents;
- public codebook/instrument documentation if repository material is incomplete.

## Mission

Independently determine, with conservative proof standards, which LiTS and WVS variables are **guaranteed not to be needed by Rawlsing's present foreseeable empirical architecture envelope**, without pretending the positive/use frontier is final.

The desired result is the complement-side optimization:

> We may not yet know every variable Rawlsing WILL use, but can we prove that some variables WILL NOT be used for any lawful current/foreseeable PRE-V3, Field Forge, V3-border, routing, design, discovery, replay or audit function?

Priority:
1. LiTS-I (1,198 variables)
2. WVS7 (613 variables)
3. If methodology and repository assets make it cheap, note portability to the rest of the 35-source estate, but do not delay LiTS/WVS completion.

## Critical correction — semantic relevance does NOT imply retaining every repeated physical instance

The exclusion court must reason at both:

- **semantic family / battery level**, and
- **physical variable-instance level**.

A question family may be substantively relevant to Rawlsing while many of its repeated member-indexed / roster-indexed / iteration-indexed physical columns are still provably unnecessary.

This is especially important for LiTS, where some instruments repeat the same battery separately across many household/family members and can inflate source width by an order of magnitude.

Do NOT apply this false rule:

```
QUESTION FAMILY IS PLAUSIBLY RELEVANT
→
KEEP EVERY PHYSICAL INSTANCE OF THAT FAMILY
```

Instead identify repeated-template families such as:

- household-member / family-member roster expansions;
- the same attribute repeated for member 1, member 2, ... member N;
- the same substantive battery repeated across enumerated relatives;
- repeated source slots whose only difference is member/iteration index;
- mechanically expanded maximum-cardinality placeholders;
- duplicated administrative or derived views of the same underlying source-native object.

For each repeated family, determine separately:

1. **family-level semantic relevance** — could Rawlsing use the concept at all?
2. **required consumption grain** — respondent-level, household-summary, relationship-type, member-level, distributional, or other;
3. **whether distinct member identity/order is itself needed** by any current/foreseeable PRE-V3 / Field Forge / V3-border function;
4. **minimum physical instance set**, if any, needed to preserve that lawful information;
5. **cardinality-excess instances** whose only contribution is repeated source enumeration beyond the consumption grain;
6. whether the information can be represented by an already-governed aggregate/summary/relationship object without retaining every physical repeated slot.

A repeated variable may therefore be class A even when its question family is class B/C, if there is affirmative evidence that the particular physical instance is cardinality-redundant for Rawlsing.

Required exclusion-proof types must include, where applicable:

- `SEMANTICALLY_OUTSIDE_ENVELOPE`
- `REPEATED_TEMPLATE_CARDINALITY_EXCESS`
- `DUPLICATE_PHYSICAL_INSTANCE`
- `SUPERSEDED_DERIVED_OR_ADMIN_VIEW`
- `SOURCE_PLACEHOLDER_OUTSIDE_REQUIRED_GRAIN`

Do not infer redundancy from naming patterns alone. Use codebook/questionnaire structure, mapping registries, Long Memory / Field Forge / PRE-V3-V3 grain requirements, and exact source documentation.

For repeated families, add these fields to the per-variable frontier outputs when applicable:

- `template_family_id`
- `instance_index_or_member_slot`
- `family_semantically_relevant`
- `required_consumption_grain`
- `distinct_instance_identity_required`
- `minimum_retained_instance_basis`
- `exclusion_proof_type`

Also produce:

`08_REPEATED_BATTERY_AND_CARDINALITY_AUDIT.md`

This must identify the largest width-inflating repeated families in LiTS-I and WVS7, show their physical instance counts, explain the Rawlsing-relevant information grain, and distinguish:

- family relevant / all instances required;
- family relevant / only bounded subset or summary required;
- family relevant / individual indexed instances not required;
- family irrelevant;
- unresolved.

The goal is specifically to avoid a naive semantic-text classifier preserving 10x physical width merely because each repeated column has a substantively interesting label.

## Required broad preservation envelope

A variable is NOT guaranteed-excludable merely because it could plausibly support a role at the **family/concept level**. First determine whether the **particular physical instance** contributes information at the consumption grain Rawlsing could lawfully use. Preserve the role envelope below, but do not let it force retention of cardinality-redundant repeated instances.

Relevant roles include:

- attitude / disposition / value / belief response;
- social-position or demographic coordinate;
- household/family/relationship context;
- education, occupation, employment, resources, deprivation, class/status;
- religion/sect, ethnicity/race/caste, migration, language;
- geography, urban/rural, country/region/city;
- age, sex/gender, cohort or temporal context;
- routing, questionnaire exposure, form, ballot, split, module, applicability;
- respondent identity / record linkage required by exact replay;
- survey design, strata, cluster/PSU, weights, estimands;
- question topology, multi-response, ranking, repeated/component structures;
- same-respondent/J/coadministration authority;
- comparator/discovery/relation construction;
- Field Forge position geometry;
- Field Forge disposition geometry;
- position↔disposition pressure/conditional topology;
- PRE-V3 learned-world production;
- PRE-V3 → V3 interface requirements;
- source authority, missingness, scale, transformation, provenance, replay, invalidation or audit.

Do not exclude a variable solely because today's code does not consume it.

## Classification system

Every source variable must receive one of these dispositions:

### A. `GUARANTEED_EXCLUDE_CURRENT_ENVELOPE`

Only when affirmative documentary/semantic evidence proves either (a) it cannot participate in any preserved role above, **or (b) its semantic family may participate but this particular physical instance is provably redundant/excess relative to the lawful Rawlsing consumption grain**.

This class must have a concrete exclusion proof, not "looks irrelevant."

### B. `CURRENTLY_UNUSED_BUT_FUTURE_PLAUSIBLE`

Not currently consumed by live workloads, but semantically capable of supporting a foreseeable Rawlsing role.

### C. `KEEP_REQUIRED_OR_PLAUSIBLY_CONSUMABLE`

Current authority/use or clear prospective relevance.

### D. `UNRESOLVED__DO_NOT_PRUNE`

Insufficient authority to exclude safely.

Unknown defaults to D, never A.

## Evidence hierarchy

Prefer, in order:

1. current source/semantic authority;
2. current machine-readable relation/mapping registries;
3. current PRE-MAIN/HQ governance;
4. current/admitted Field Forge / V3-border requirements;
5. bounded historical source mappings/codebooks;
6. public codebook/instrument documentation;
7. lexical inference only as a search aid, never final exclusion proof.

Exploratory Field Forge documents may enlarge the conservative KEEP envelope when they preserve a plausible architecture requirement, but cannot by themselves prove source semantics.

## Required repository assets

At minimum inspect and reconcile:

- `data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/question_structural_mapping_live_PLUS4_FINAL_APPLIED_R1.csv`
- `data/ddm_build_copy/bindings/question_relation_registry_35wave_active_v1.csv`
- `data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.csv`
- `data/ddm_build_copy/manifests/question_wave_itinerary.csv`
- `data/ddm_build_copy/manifests/country_source_mapping_registry.csv`
- source/wave codebook material and codebook builders
- LiTS 1,198-slot ownership/projection/exclusion ledger
- LiTS accepted semantic-response authorities and any broader active semantic slots
- WVS current mapping/authority package
- O11/T15 wave capability atlas and relevant relation/J/routing authority
- Field Forge codebook-grounded observability stress test
- Field Forge PRE553 observatory / position/disposition requirements
- current PRE-V3/V3-border authority and V3/PFF convergence documents
- GitHub issue #421

Search for additional master variable/codebook inventories. The 7.6MB full question structural mapping and 35-wave relation registry are expected to be central.

## Special LiTS law

Do not use the current two-response FIABC proving scope as the positive frontier.

The 1,198-slot ledger's "nonparticipating in accepted projection" status is evidence only about that bounded projection, not permanent Rawlsing irrelevance.

Specifically preserve the distinction between:
- bounded proving response slots;
- broader accepted semantic response slots;
- Field Forge/PRE-V3 plausible positional/dispositional variables;
- routing/design/weight/identity/audit variables;
- truly provable exclusions.

## Special WVS law

Do not reduce WVS to Q291G5/Q291P5/B_COUNTRY merely because FIABC uses that proving pair.

Rawlsing's historical/current project purpose includes broad WVS cultural/value drivers and later PRE-V3/Field Forge empirical work.

## Exclusion proof requirements

A class-A exclusion row must contain:
- source/wave;
- variable code/name;
- codebook/source meaning;
- current semantic disposition where known;
- why it cannot support any preserved Rawlsing role;
- exact evidence path/ref;
- authority ceiling;
- exclusion proof type;
- confidence must be categorical `PROVED_WITHIN_CURRENT_ENVELOPE`, not a probability.

Examples of potentially excludable classes may exist, such as pure export/processing artifacts or source-local administrative duplicates, but do NOT assume even these are excludable: form/routing/design/identity/provenance fields can look administrative and still be essential.

## Required outputs

1. `00_RETURN.md`

2. `01_LITS_I_VARIABLE_FRONTIER.csv`
   - all 1,198 variables if the authoritative inventory permits complete enumeration.

3. `02_WVS7_VARIABLE_FRONTIER.csv`
   - all 613 variables if the authoritative inventory permits complete enumeration.

4. `03_EXCLUSION_PROOF_LEDGER.csv`
   - only class-A guaranteed exclusions, each with exact proof and exclusion-proof type.

5. `04_KEEP_ENVELOPE_ROLE_SUMMARY.md`
   - what role classes force conservative retention.

6. `05_UNRESOLVED_AND_STALE_SEMANTICS.md`
   - variables/classes that cannot yet be safely adjudicated.

7. `06_PROJECTED_SAVINGS_WITHOUT_RAW_EXECUTION.json`
   - counts only:
     - total variables
     - class A/B/C/D counts
     - guaranteed-exclusion percentage by source
   - NO runtime/time savings estimate unless supported by already-recorded measurements.
   - NO raw source processing.

8. `07_METHOD_PORTABILITY_TO_35_SOURCES.md`
   - bounded note on whether the same exclusion court can later run across all source waves.

9. `08_REPEATED_BATTERY_AND_CARDINALITY_AUDIT.md`
   - largest repeated-template width multipliers, required semantic grain, and provable per-instance excess.

## PASS law

PASS does NOT mean "we know the final positive variable set."

PASS means:
- every LiTS-I/WVS7 variable is either conservatively classified or explicitly unresolved;
- every guaranteed exclusion has affirmative evidence;
- no proving-slice absence was promoted to permanent exclusion;
- the result can safely tell HQ how much width can be removed **without foreclosing current foreseeable Rawlsing functions**.

If the documentary estate cannot support a guaranteed exclusion for many variables, return that honestly. A small proven class-A set is better than a large guessed one.
