# PYAT HQ205 — R9 fan-in independent adjudication — R1

Repository: maidiu/rawlsing
Role: independent hostile documentary/runtime reviewer
Preferred model: DeepSeek V4.1 Flash

Branch:
agent/reviewer-pyat-hq205-r9-r1

Exact base:
0e8d5bcd98e5aba63cd7312f778dedbfe8b6b646

Candidate under review:
dfdf5659fd78e9bc996b07383349094059a5553d

Accepted R9 runtime:
deea40541cda0627d129dcb7d30e06e0682e0fed

Final R9 acceptance:
0deb64784829661780ee3957f8070ccc2c241722

HQ205 adjudication:
0e8d5bcd98e5aba63cd7312f778dedbfe8b6b646

Checkout:
SPARSE_REQUIRED

## Mission

Independently adjudicate the two blockers returned by the R9 control fan-in candidate.

Do NOT repair code in this lane.

### A — exact R7 denominator provenance

The fan-in says 30/55 R7 tests are absent from current control because three accepted C3 closed35 court files live on a separate accepted lineage.

Trace exactly:
- introduction commits;
- adoption/acceptance status;
- relationship to the canonical R7 six-file gate;
- whether those three court files are merely historical qualification artifacts or accepted current-control dependencies;
- whether importing the court files requires any production dependencies absent from current control;
- whether the exact 55-test R7 gate remains binding on a current-control fan-in candidate.

Choose one:
1. RESTORE_ACCEPTED_R7_COURT_DEPENDENCIES_TO_CONTROL;
2. R7_GATE_SHOULD_BE_REBASED_TO_CURRENT_CONTROL_COURT_SET;
3. MATERIAL_AUTHORITY_CONFLICT__HQ_REQUIRED.

Do not choose based on convenience.

### B — SR06 decoder regressions

Reproduce/inspect exactly these two regressions:
- test_expected_source_identity_is_hashed_once_before_reader_decode
- test_normal_decode_uses_chunk_path_and_compatibility_uses_full_read

Compare:
- current-control SR06 test authority;
- accepted decoder semantics;
- broker-governed source identity path;
- accepted source-session semantics;
- historical/adopted authority controlling normal decode routing and compatibility routing.

Determine whether:
1. the tests assert a stale implementation detail superseded by accepted R9 semantics;
2. the tests encode a still-binding invariant that the accepted decoder must preserve;
3. there is a narrower compatibility invariant that both can satisfy.

Do not retire tests merely because the new code passes its own courts.

### C — environment qualification

Assess whether the reconstructed CPython 3.11.3 + exact 13-package freeze is sufficient evidence for source-free review, or whether governed-environment reconstitution is required before adoption.

Do not weaken the pyreadstat 1.3.6 pin.

## Required output

00_REVIEW.md
01_R7_DENOMINATOR_PROVENANCE.json
02_SR06_AUTHORITY_ADJUDICATION.json
03_ENVIRONMENT_QUALIFICATION.json
04_REPAIR_REQUIREMENT.json
05_FINAL_DISPOSITION.json

Allowed dispositions:
- R9_FANIN_ADJUDICATED__BOUNDED_REPAIR_AND_R7_RESTORE_REQUIRED
- R9_FANIN_ADJUDICATED__TEST_RETIREMENT_AND_R7_RESTORE_REQUIRED
- R9_FANIN_READY_AFTER_DOCUMENTARY_GATE_REBASE
- R9_FANIN_MATERIAL_AUTHORITY_CONFLICT
- R9_FANIN_REQUIRES_GOVERNED_ENVIRONMENT_RECONSTITUTION

No code changes. No source access. No self-adoption.

Commit, push, re-fetch, verify.

Terminal:
HQ205_R9_FANIN_INDEPENDENT_ADJUDICATION_RETURNED__HQ_DECISION_REQUIRED
