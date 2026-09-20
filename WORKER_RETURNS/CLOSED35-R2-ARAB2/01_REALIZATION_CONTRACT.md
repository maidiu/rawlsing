# CLOSED35-R2-ARAB2 — Realization Contract

Schema: CLOSED35_R2_ARAB2_SOURCE_REALIZATION@1.0.0

Semantic owner: ARAB2_SEMANTIC_OWNER_V1

## 1. Court object

This contract defines the one candidate-neutral source-specific semantic realization for the exact canonical source Arab Barometer Wave 2.sav with SHA-256 6529841b97bd56463490d810ad24ceaa4866066d12e4651a7081682d413606a1.

Physical delivery may later differ among A/B/C, but source identity, replay identity, physical/semantic missing-state separation, ranked topology, documentary routing jurisdiction, bounded unknown behavior, and weight authority are invariant.

This implementation is not a real-source execution or physical-equivalence court.

## 2. Canonical source and replay identity

Canonical filename: Arab Barometer Wave 2.sav

Canonical SHA-256: 6529841b97bd56463490d810ad24ceaa4866066d12e4651a7081682d413606a1

Format: SAV

Accepted physical mode: SAV_NATIVE_GOVERNED

Source-declared text mode: UTF-8 / character code 65001

Replay identity: SOURCE_SHA256+ROW_ORDINAL

QID is documented as Questionnaire ID number. Accepted source evidence shows QID is not by itself injective, while COUNTRY+QID is empirically injective in this frozen snapshot. Empirical injectivity is not semantic identity authority. Neither may replace the hard replay key.

## 3. Missing-state jurisdiction

Physical missingness and semantic missingness are independent dimensions.

For Q2062 the accepted packet proves coexistence of:

- a true SYSTEM_MISSING state;
- an ordinary stored numeric 0;
- source dictionary metadata labeling 0 as "0. missing".

The source dictionary label must remain attached to the ordinary value as metadata. It does not convert raw 0 into SYSTEM_MISSING and it does not by itself establish an exact documentary semantic reason.

Therefore the governed projection for code 0 is:

physical state = ORDINARY_STORED_VALUE

raw storage value = 0

source dictionary label = "0. missing"

documentary semantic state = BOUNDED_UNKNOWN

semantic refinement = BOUNDED_UNKNOWN

A true SYSTEM_MISSING cell remains physically separate and likewise does not acquire a routing or response reason merely from absence.

## 4. Exact documentary code semantics

The realization admits exact source-native questionnaire authority only where the Authority71 packet closed the code meaning.

Currently admitted:

Q101 / 8 -> I don't know

Q101 / 9 -> Declined to answer

Q2062 / 99998 -> I don't know

Q2062 / 99999 -> Declined to answer

Not admitted:

Q101 / 0

Q2062 / 0

The latter remain BOUNDED_UNKNOWN. No neighboring variable, repeated concept, another Arab Barometer wave, equal frequency, source dictionary wording, or missingness pattern may fill the gap.

## 5. Ranked challenge topology

Q2061 and Q2062 are an ordered two-slot documentary structure.

Q2061 has rank 1 and role MOST_IMPORTANT_CHALLENGE.

Q2062 has rank 2 and role SECOND_MOST_IMPORTANT_CHALLENGE.

This is repeated-ranked-slot topology, not an unordered set and not a native SPSS MR-set claim.

The accepted packet records zero native SPSS MR metadata for this snapshot. That does not erase the questionnaire's ordered challenge topology.

A candidate must preserve exact slot identity, rank, multiplicity, and row association.

## 6. Routing and applicability

Routing is documentary-led.

The accepted source-native questionnaire establishes that Lebanon recorded only the most important challenge. The owner therefore admits one exact rule for Q2062 in Lebanon:

SECOND_RANK_NOT_RECORDED_BY_INSTRUMENT

That rule is not inferred from a missing Q2062 cell.

For country-specific challenge options and other country modules, applicability may be projected only after an exact documentary rule is joined to the exact source variable/country scope.

Absent that join, routing state is BOUNDED_UNKNOWN.

Forbidden routing sources include:

- SYSTEM_MISSING incidence;
- ordinary zero incidence;
- observed/nonobserved frequency;
- source variable naming;
- another wave's routing;
- physical layout alone.

## 7. Weight and sample authority

WT must be retained as a source-local carrier.

Current authority does not close:

- WT estimand;
- WT normalization;
- relation between WT and SAMP;
- a universal/default use of WT.

All remain BOUNDED_UNKNOWN.

The source-native questionnaire does close SAMP codes 1 and 2 as Main sample and Additional sample. That distinction is preserved without upgrading it into an estimand, weighting rule, or identity rule.

Any weighted analytical use requires a later governed authority and a new/superseding semantic contract if it changes this realization's current unknown state.

## 8. S35 edge-class binding

Exact applicable edge classes:

EC01 — FORMAT_FAMILY_SAV_DTA

Preserve exact source identity, variable order, raw storage values, physical metadata, and row replay identity.

EC05 — PHYSICAL_MISSINGNESS_MULTICLASS

Preserve SYSTEM_MISSING separately from ordinary stored values that look semantically missing. Missing-state class does not establish response semantics.

EC09 — ORDERED_REPEATED_SLOT_TOPOLOGY

Preserve Q2061/Q2062 rank and multiplicity. No flattening or deduplication.

EC10 — FORM_MODULE_SKIP_ROUTING_CARRIERS

Preserve routing/module carriers while requiring explicit documentary authority for applicability.

EC12 — WEIGHT_DESIGN_MULTIPLICITY_AND_DOMAIN

Preserve WT and relevant sample/design carriers. Presence or name cannot select a default estimand.

EC14 — COMPOUND_EDGE_INTERACTION_COURT

All applicable atomic invariants must survive simultaneously. It adds no special Arab2 physical adapter.

## 9. R35 physical hooks

R35-I01 schema:

PRE553_PHYSICAL_METADATA@1.0.0

R35-I02 schema for non-direct realizations:

FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0

R35-I03 schemas:

FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0

FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0

FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0

FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0

Arab2 required physical dimensions include physical metadata, variable order, raw storage values, physical missing states, missing declarations, row replay identity, ordered ranked-slot topology, routing carriers, and weight/design variables.

These hooks have no semantic authority and have not been executed here.

## 10. Candidate-neutral handoff

Future qualification order must preserve one semantic owner:

SOURCE IDENTITY FREEZE

then ARAB2_SEMANTIC_OWNER_V1 FREEZE

then independent physical candidate realization

then R35 physical receipts

then source-specific hostile semantic tests

then common A/B/C comparison.

A/B/C must carry one deterministic source-specific realization identity computed from this complete source law.

Candidate-local semantic reinterpretation is nonconforming.

## 11. Fail-closed and bounded-unknown law

Wrong source SHA:

BLOCKED__CANONICAL_SOURCE_ROOT_UNPROVED

Replay key changed from source SHA + row ordinal:

BLOCKED__REPLAY_IDENTITY_DIVERGENCE

Ordinary zero promoted to SYSTEM_MISSING:

BLOCKED__PHYSICAL_MISSING_STATE_COLLAPSE

Source dictionary label promoted to exact code-0 meaning:

BLOCKED__UNAUTHORIZED_SEMANTIC_PROMOTION

Ranked slots flattened/reordered/deduplicated:

BLOCKED__RANKED_TOPOLOGY_LOSS

Routing inferred from missingness:

BLOCKED__ROUTING_AUTHORITY_INVENTED

WT selected without estimand/default-use authority:

BLOCKED__WEIGHT_AUTHORITY_INVENTED

Candidate semantic law divergence:

BLOCKED__SEMANTIC_OWNER_DIVERGENCE

The following remain lawful bounded unknowns rather than blockers:

- exact Q2062 code-0 semantic reason;
- exact Q101 code-0 semantic reason;
- WT estimand and normalization;
- WT relation to SAMP;
- native identifier jurisdiction beyond its documented local label;
- country/module applicability not closed by an exact documentary join;
- cross-wave semantic equivalence.

## 12. Claim boundary

This realization proves source-specific implementation only.

It does not prove real-source execution, whole-source physical equivalence, A/B/C execution, I05, measured P2X, or certification beyond the accepted documentary/physical authority.
