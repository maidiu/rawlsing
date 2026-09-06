# GT3/GT4 Q1 — PUBLIC-CLINIC SUBJECT SEMANTIC OWNER / O4 PREREQUISITE R1

## Terminal

`FAIL__GT34_Q1_O4_SUBJECT_REQUIREMENT_AUTHORITY_OVERLAP_DEFECT_PROVED__REPAIR_CANDIDATE_DEFINED`

## Exact execution boundary

- repository: `maidiu/rawlsing`
- branch: `agent/rabochii-gt34-q1-public-clinic-subject-semantic-owner-r1`
- exact working ancestry: `acfac12a4ca4b9efa010fd224094ac4dc55d37a8`
- governing instruction ref, evidence only: `f0bcc693ff44d7d4c4c6f84ec08af70f49a5059f`
- actor mutation: NONE
- comparator adoption: NONE
- PSEPF: NONE
- positive V3: NONE

## Holding

The current O4 subject requirement is not merely missing a concrete owner. It assigns the wrong proposition to that owner.

O4 currently requires the independently accepted owner of the exact actor `subject_ref` to authorize:

`PUBLIC_CLINIC_OR_HOSPITAL_CONTACT_OR_USE`

That crosses an already-frozen authority boundary.

ADP-010 owns the actor-specific realization chain:

`AVAILABLE -> OPPORTUNITY -> ENCOUNTER -> EXPOSURE`

and defines ENCOUNTER as the admitted contact occurrence. Its `OPPORTUNITY -> ENCOUNTER` rule requires an exact contact-occurrence witness and records the exact `subject_ref`.

Therefore the subject semantic owner may classify **what the exact subject is**, but it may not independently own the fact that the actor contacted/used it.

The correct decomposition is:

`SUBJECT OWNER: SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL`

PLUS

`ADP-010: ACTOR_ENCOUNTERED_EXACT_SUBJECT`

THEREFORE, and only inside the bounded comparator:

`PUBLIC_CLINIC_OR_HOSPITAL_CONTACT_OR_USE`.

This is a genuine ownership-overlap defect in O4's current v1.0.0 subject requirement. It must be repaired before comparator adoption.

## Current-owner discovery

No current accepted production subject-semantic owner was found that can bind an exact actor-side `subject_ref` to:

`SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL`.

The current repository contains no production subject/institution ontology surface that can lawfully substitute for that missing proof.

Historical taxonomy/ontology documents, survey question taxonomies, labels, institution/category similarity, and narrative names are not current semantic authority and were not promoted.

ADP-010 itself cannot fill this gap: it explicitly says labels and institution/category similarity are insufficient for ENCOUNTER and it does not own a universal institution taxonomy.

So the repaired O4 requirement below removes the authority overlap, but an exact subject classification owner/proof is still a future prerequisite for an operable positive comparator.

## Repaired O4 subject-requirement candidate

Candidate:

`GT34_ADP010_Q69B_PUBLIC_CLINIC_SUBJECT_SEMANTIC_REQUIREMENT@1.1.0`

semantic hash:

`219fe6714efbcda30b6d9ea69cec6b99f3fe86a92c43ae7122a68e404f795fca`

Exact semantic projection:

```json
{
  "actor_record_field": "subject_ref",
  "content_addressing_law": {
    "algorithm": "SHA-256",
    "derived_hash_field_rule": "EXCLUDE_ONLY_THE_OBJECTS_OWN_DERIVED_CONTENT_HASH_FROM_ITS_SEMANTIC_PROJECTION",
    "encoding": "UTF-8",
    "mapping_key_order": "LEXICOGRAPHIC_ASCENDING",
    "ordered_sequences": "PRESERVE_EXACT_ORDER",
    "separators": "COMPACT_COMMA_COLON",
    "set_like_collections": "SORT_BY_CANONICAL_JSON_AND_DEDUPLICATE_ONLY_WHERE_SCHEMA_MARKS_SET_LIKE"
  },
  "composition_law": [
    "SUBJECT_OWNER_PROVES_SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
    "ADP010_PROVES_ACTOR_ENCOUNTERED_THE_EXACT_SUBJECT",
    "COMPARATOR_MAY_COMPOSE_ONLY_THOSE_EXACT_PROPOSITIONS_INTO_PUBLIC_CLINIC_OR_HOSPITAL_CONTACT_OR_USE"
  ],
  "does_not_assert": [
    "CONTACT_OCCURRENCE",
    "MEDICINE_OR_SUPPLIES_PROBLEM",
    "EXPOSURE",
    "AWARENESS",
    "BELIEF",
    "MEMORY",
    "RESPONSE"
  ],
  "failure": "NONCOMPARABLE_SUBJECT",
  "owner_law": [
    "SUBJECT_REF_MUST_BE_EXACT_CONTENT_ADDRESSED",
    "SUBJECT_REF_MUST_RESOLVE_UNDER_ITS_OWN_SEPARATELY_ACCEPTED_CURRENT_SEMANTIC_OWNER",
    "THE_SUBJECT_OWNER_NOT_ADP010_AND_NOT_THIS_COMPARATOR_MUST_AUTHORIZE_ONLY_THE_EXACT_SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL_PROPOSITION",
    "ADP010_RETAINS_EXCLUSIVE_OWNERSHIP_OF_THE_ENCOUNTER_OCCURRENCE",
    "LEXICAL_LABEL_SIMILARITY_CATEGORY_SIMILARITY_COLOCATION_OR_INSTITUTION_CLASS_ALONE_IS_INSUFFICIENT",
    "THE_EXACT_SUBJECT_REF_OWNER_AUTHORITY_REF_AND_PROPOSITION_PROOF_HASH_MUST_ENTER_THE_COMPARATOR_RECEIPT"
  ],
  "positive_relation_ceiling": "SUBJECT_CLASSIFICATION_ONLY",
  "required_subject_proposition": "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
  "schema": "GT34_ADP010_Q69B_PUBLIC_CLINIC_SUBJECT_SEMANTIC_REQUIREMENT@1.1.0"
}
```

The hash is:

`SHA256(UTF8(CANONICAL_JSON(EXACT_PROJECTION)))`

using lexicographically sorted mapping keys and compact comma/colon separators.

## Why this is narrower

The repaired subject owner proves only:

`SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL`.

It does **not** prove:
- that the actor encountered the subject;
- that the actor used healthcare services beyond the exact ADP-010 contact occurrence;
- medicine/supplies problems;
- exposure;
- awareness;
- memory;
- belief;
- response.

The comparator may compose the subject classification with the exact accepted ADP-010 ENCOUNTER record because both bind the same exact content-addressed `subject_ref`.

No lexical/fuzzy/category inference is added.

## Receipt consequence

A future positive O4 receipt must bind separately:

1. exact ADP-010 ENCOUNTER record/ref/hash proving actor + exact subject + occurrence + time;
2. exact subject semantic owner authority ref;
3. exact subject classification proposition proof hash;
4. repaired subject requirement ref/hash;
5. then the existing Q69B temporal/predicate ancestry.

This preserves provenance of the two independent premises rather than hiding contact occurrence inside a subject classifier.

## What remains missing

No exact generated first-canary `subject_ref` plus accepted subject-classification proof is current.

Therefore this worker does **not** invent or adopt a subject taxonomy authority. A successor must either:
- identify a real already-authoritative generated-world subject object and bind it under a minimal subject-classification authority; or
- define that smallest authority only when exact subject evidence exists.

Until then, the O4 comparator remains candidate-only and inoperative.

## Authority ceiling

This return does not:
- change ADP-010 identity;
- change Q69B identity;
- adopt O4;
- create actor history;
- create PSEPF;
- create metabolism/CAN-008 authority;
- authorize positive V3.

## Final

The exact defect is proven and the smallest repaired O4 subject requirement is defined, but the concrete actor-side subject-classification authority/evidence remains absent.

Terminal:

`FAIL__GT34_Q1_O4_SUBJECT_REQUIREMENT_AUTHORITY_OVERLAP_DEFECT_PROVED__REPAIR_CANDIDATE_DEFINED`
