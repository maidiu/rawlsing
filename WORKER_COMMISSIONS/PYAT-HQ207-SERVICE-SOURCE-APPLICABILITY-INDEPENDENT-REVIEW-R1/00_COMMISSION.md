# PYAT HQ207 — service-source applicability independent hostile review — R1

Repository: maidiu/rawlsing
Role: independent hostile source-free reviewer
Preferred model: DeepSeek V4.1 Flash

Branch:
agent/reviewer-pyat-hq207-hc-r1

Exact base:
cfe648bd462ddf6fc1252182c5e784ec43bf4405

Candidate:
e7d3598494472a9aea7dd2c69f6aacb11585905c

Ratified derivation:
6c0d4739dc56a957a8bdd2512b24756cf466511b

HQ205 adjudication:
0e8d5bcd98e5aba63cd7312f778dedbfe8b6b646

HQ207 adjudication:
cfe648bd462ddf6fc1252182c5e784ec43bf4405

Checkout:
SPARSE_REQUIRED

## Mission

Independently attack whether the candidate faithfully implements:

ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED

Do NOT modify code.

### A — exact request-key contract

Verify all ratified scope components are mandatory and exact.

Attack:
- missing component;
- ambiguous component;
- candidate-class broadening/narrowing;
- fuzzy/latest/default selector;
- permission-ref confusion;
- temporal-scope ambiguity.

### B — state-family separation

Verify SERVICE_SOURCE_APPLICABILITY_STATE is genuinely distinct and cannot be confused with:
- source-relation state;
- empirical-fact state;
- structural-admission state;
- authority state.

Check exact-decision to public-state mapping and precedence.

### C — COMPLETE / INCOMPLETE honesty

Attack every route by which:
- unresolved candidate;
- missing authority;
- conflicting authority;
- integrity failure

could still produce COMPLETE coverage.

Verify:
NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS
is impossible under INCOMPLETE coverage.

### D — unranked set law

Prove canonical ordering is replay-only.

Attack for hidden:
- first-source wins;
- ordering preference;
- score;
- rank;
- priority;
- locality preference;
- release recency preference;
- implicit fallback order.

Multiple APPLICABLE sources must remain an unranked set.

### E — power noncollapse

Try to use the applicability receipt as authority for:
- selection;
- pooling;
- semantic equivalence;
- respondent linkage;
- overlap/nonduplication;
- estimand composition;
- backfill;
- currentness;
- target-use permission grant;
- F8 conditioning;
- geometry/distribution transformation;
- individual inference.

All must fail structurally.

### F — evidence distinction

Attack:
NO_APPLICABLE_SOURCE
!=
APPLICABLE_SOURCE_WITH_MISSING_INTERNAL_EVIDENCE

Verify no internal evidence field can alter applicability.

### G — replay/provenance

Verify:
- deterministic replay under permuted candidate order;
- exact authority/provenance bound per positive source;
- negative/refusal basis preserved;
- semantic hash changes when any governed determinant changes.

### H — court quality and regression

Re-run the 60-test focused court.

Independently inspect whether all 15 commissioned hostile cases genuinely test behavior rather than constants.

Re-run a suitable regression slice or validate the candidate's before/after failure-ID proof.

## Output

00_REVIEW.md
01_REQUEST_KEY_ATTACK.json
02_STATE_AND_COVERAGE_ATTACK.json
03_UNRANKED_SET_REVIEW.json
04_POWER_NONCOLLAPSE_REVIEW.json
05_EVIDENCE_AND_REPLAY_REVIEW.json
06_COURT_AND_REGRESSION_RECEIPT.json
07_FINAL_DISPOSITION.json

Allowed:
- ACCEPT_SERVICE_SOURCE_APPLICABILITY__SOURCE_FREE_FORM
- SERVICE_SOURCE_APPLICABILITY_PARTIAL__BOUNDED_REPAIR_REQUIRED
- SERVICE_SOURCE_APPLICABILITY_AUTHORITY_OVERREACH
- SERVICE_SOURCE_APPLICABILITY_QUALIFICATION_FAILURE
- MATERIAL_AUTHORITY_CONFLICT

No source access. No self-adoption.

Commit, push, re-fetch, verify.

Terminal:
HQ207_SERVICE_SOURCE_APPLICABILITY_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED
