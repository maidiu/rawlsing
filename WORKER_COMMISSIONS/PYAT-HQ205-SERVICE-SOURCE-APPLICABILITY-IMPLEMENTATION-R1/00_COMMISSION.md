# PYAT HQ205 — service-source applicability source-free implementation — R1

Repository: maidiu/rawlsing
Role: source-free authority implementation worker — Space Bunny

Branch:
agent/rabochii-pyat-hq205-hc-impl-r1

Exact base:
0e8d5bcd98e5aba63cd7312f778dedbfe8b6b646

Ratified documentary derivation:
6c0d4739dc56a957a8bdd2512b24756cf466511b

HQ205 adjudication:
0e8d5bcd98e5aba63cd7312f778dedbfe8b6b646

Checkout:
SPARSE_REQUIRED

## Binding authority

Implement ONLY the HQ-ratified minimal form:

`ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED`

Ratified design decisions:

- candidate_class_ref is mandatory;
- SERVICE_SOURCE_APPLICABILITY_STATE is a distinct state family;
- public positive state is APPLICABLE;
- incomplete candidate-class coverage may be represented truthfully but may not masquerade as a complete admissible set;
- any downstream operation requiring exhaustive applicability must fail closed or remain unresolved unless coverage is COMPLETE;
- admission provenance is required;
- no selection-reason record exists because comparative source selection is not authorized;
- candidate-class bound is part of the request key.

## Mission

Implement the smallest generic source-free authority owner/resolver consistent with the derived form.

Do NOT implement ranking, weights, scores, preferences, or source priority.

Do NOT implement source relations, pooling, estimand composition, currentness, or target-use permission grants inside this owner.

Those remain separate powers.

## Required contract

At minimum define a request key carrying exact governed scope needed by the derivation:

- service ref;
- target question/coordinate/structural-use ref(s);
- candidate_class_ref;
- population/universe scope ref(s);
- geography scope ref(s);
- effective-time-or-interval ref(s);
- candidate source universe ref;
- release identity ref;
- target-use permission refs as BOUND INPUT, never as permission grants.

Use current exact-ref idiom.

No fuzzy/latest/default lookup.

## Decision states

Implement a distinct family whose exact decisions include at minimum:

- APPLICABLE;
- NOT_APPLICABLE;
- NONCOMPARABLE;
- OUT_OF_SCOPE;
- UNDETERMINED_NO_POSITIVE_AUTHORITY;
- CONFLICTING_AUTHORITY.

If the documentary derivation contains a stricter exact state vocabulary, preserve it.

Do not alias these to source-relation or empirical-fact states merely because words overlap.

## Candidate-class result

The resolver must produce an exact candidate-class applicability receipt that preserves:

- candidate_class_ref;
- canonical replay-only ordering of candidate entries;
- per-source decision;
- exact authority/provenance refs;
- candidate_class_coverage = COMPLETE or INCOMPLETE;
- admissible_source_universe_refs as a set-like output;
- no_applicable_source as a typed COMPLETE-coverage outcome only.

If coverage is INCOMPLETE:
- preserve known positive/negative per-source findings;
- do not call the resulting set complete;
- do not emit NO_APPLICABLE_SOURCE merely because no known positive exists.

## Provenance

Each APPLICABLE result must carry exact positive admission authority/provenance.

Negative/refusal results must carry exact basis/refusal refs where required by the derived contract.

Canonical serialization order must be deterministic for replay only and explicitly non-semantic:
it grants no rank, priority, preference, weight or fallback order.

## Power noncollapse

Courts must prove that this authority cannot:

- rank or select among applicable sources;
- authorize pooling;
- authorize source semantic equivalence;
- authorize respondent linkage;
- authorize overlap/nonduplication;
- authorize estimand composition;
- authorize backfill;
- infer applicability from currentness;
- grant target-use permission merely because a permission ref is bound;
- infer source priority from locality/country;
- transform F8 geometry/distribution;
- infer person-level state.

## Evidence distinction

Prove structurally:

NO_APPLICABLE_SOURCE
!=
APPLICABLE_SOURCE_WITH_MISSING_INTERNAL_EVIDENCE

This owner only decides applicability.

It must not inspect or reinterpret internal empirical sufficiency as applicability.

## Placement

Prefer the smallest current PRE553 authority/registry pattern compatible with:
- exact-key immutable authority;
- no latest/default/fuzzy lookup;
- deterministic replay;
- fail-closed conflicts.

Do not edit unrelated owners unless strictly required.

## Source-free courts

Required hostile cases include:
- exact positive applicability;
- exact negative applicability;
- noncomparability;
- out-of-scope;
- no positive authority;
- conflicting authority;
- incomplete candidate class;
- complete class with zero applicable sources;
- complete class with multiple applicable sources, preserving an UNRANKED set;
- deterministic serialization under permuted input order;
- attempt to smuggle priority/ranking metadata refused;
- attempt to silently broaden candidate class refused;
- attempt to use applicability receipt as pooling/selection authority refused;
- no internal-evidence state changes applicability;
- replay identity stable.

## Output

Production owner/module and focused tests, plus:
00_RETURN.md
01_OWNER_AND_STATE_CONTRACT.json
02_REQUEST_KEY_AND_REPLAY.json
03_POWER_NONCOLLAPSE_RECEIPT.json
04_COURT_RESULTS.json
05_FINAL_DISPOSITION.json

Allowed dispositions:
- SERVICE_SOURCE_APPLICABILITY_IMPLEMENTED__READY_FOR_INDEPENDENT_REVIEW
- SERVICE_SOURCE_APPLICABILITY_PARTIAL__NAMED_DEFECT_REMAINS
- SERVICE_SOURCE_APPLICABILITY_OWNER_COLLISION__HQ_REQUIRED
- SERVICE_SOURCE_APPLICABILITY_QUALIFICATION_FAILURE
- MATERIAL_NEW_AUTHORITY_CONFLICT

No source access.
No warrant.
No live C4.
No C7.
No actor/person implementation.
No self-adoption.

Commit, push, re-fetch, verify.

Terminal:
HQ205_SERVICE_SOURCE_APPLICABILITY_IMPLEMENTATION_RETURNED__HQ_REVIEW_REQUIRED
