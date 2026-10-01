# PYAT N10E — PROOF / PROVENANCE CORRECTION — NARROW INDEPENDENT REREVIEW R1

Status: ISSUED__BROWSER_ECONOMY__NARROW_REREVIEW

**LAUNCH IN: Browser — GPT-5.6 Sol High**

Repository:
`maidiu/rawlsing`

Review branch:
`agent/reviewer-pyat-hq145-n10e-proof-provenance-rereview-r1`

Exact correction return under rereview:
`52e41a41e8bc3b77390016a049095b5aea1721d0`

Correction commission tip:
`a7f7eecdeaee58e4d8021b7c571b4956e6301464`

Prior N10E independent review:
`b89268d1824409d20a91a37a0a3ff7751a7ae75a`

Original N10E return:
`58ba4320635162e8103ed38681ea5ae3e3bac014`

Governing blockers:
- `REV-N10E-001`
- `REV-N10E-002`

Nonblocking documentary correction:
- `REV-N10E-003`

This is a narrow rereview. The provider implementation itself previously passed independent review at the declared AT07/AT17 R1 grain and must not be reopened absent a concrete counterexample.

## Mission

Independently determine whether the correction fully closes REV-N10E-001/002 and correctly handles REV-N10E-003.

### A. Scope / ancestry / allowlist

Verify:
- correction branch is a descendant of the original N10E return;
- correction stays inside the commissioned proof/test/packet allowlist;
- `rawlsing_next/pre553_empirical_possibility_provider.py` is byte-identical to the reviewed provider blob:
  `23167aa25291fb148b1e3cf210ac33fe7769b783`;
- accepted analytical and possibility owners remain byte-identical;
- prior independent review artifacts are not modified.

### B. REV-N10E-001 — changed-source proof

Review:

`test_p6_geometry_is_recomputed_not_fixed_when_the_empirical_slice_changes`

and any supporting fixture changes.

Require the new court to prove a **genuinely changed empirical input** reaches the real public provider.

Independently verify:
- canonical case has 100 rows and forward denominator 60 with 54 yes / 6 no;
- changed case has 110 rows with 10 additional P1/no respondents;
- changed forward denominator becomes 70;
- changed forward cells become 54 yes / 16 no;
- exact fractions become 27/35 and 8/35;
- generated evidence is the composition-generated evidence object;
- generated evidence support equals the changed producer fact denominator;
- changed provider / evidence / producer identities reidentify appropriately;
- no geometry is handwritten inside the provider.

Verify the reverse-direction control is meaningful:
- the changed law's reverse conditioning cohort remains 62;
- its reverse cell counts remain unchanged;
- this distinguishes source-law-specific geometry change from “any second case returns a different result.”

### C. Changed-source authority

The worker reports the canonical synthetic query authority is explicitly universe-scoped and correctly refused the new universe.

Verify:
- the refusal was real and typed;
- the changed-source fixture creates only the minimum test authority needed for the changed universe;
- that authority is explicit and fixture-local;
- no `latest`, `default`, universal, widened, or production authority is invented;
- no provider or owner behavior is changed to coerce the new universe.

### D. REV-N10E-002 — final execution provenance

Verify the exact commissioned four-file court has one final authoritative run:

`python -m pytest rawlsing_next/tests/test_pre553_analytical_composition.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py rawlsing_next/tests/test_pre553_empirical_possibility_provider.py -v`

Require consistency across:
- `00_RETURN.md`
- `06_EXECUTION_RECEIPT.json`
- `08_FINAL_PYTEST_OUTPUT.txt`

Expected final:
- 88 passed;
- 0 failed;
- 0 errors;
- 0 skipped;
- 15.14s;
- per-file counts 13 + 32 + 13 + 30 = 88.

Older durations may remain only as clearly superseded historical runs, never as competing final results.

### E. REV-N10E-003 — provenance wording

Verify the final packet no longer presents “commission tip unavailable” as a standing limitation.

Historical provenance may state:
- early local phase lacked the remote commission tip / credentials;
- credentials later became available;
- commission tip was fetched;
- branch was rebased onto it;
- final ancestry is lawful.

This must be context, not a current blocker or ancestry ambiguity.

### F. Accepted findings remain intact

Do not reopen already accepted findings unless this correction contradicts them:
- provider seam, not duplicate calculator;
- no handwritten-evidence provider bypass;
- owner blob preservation;
- P1/P2;
- P3;
- receipt identity;
- P5 fail-closed;
- P7 replay;
- authority ceiling.

### G. Authority ceiling

No AT33 claim.
No real-source qualification.
No structural-world admission.
No actor/person/V3 state.
No smoothing/proxy authority.
No provider broadening.

## Return terrain

Write only:

`WORKER_RETURNS/PYAT-N10E-PROOF-PROVENANCE-REREVIEW-R1/**`

Required:
- `00_REVIEW.md`
- `01_CHANGED_SOURCE_AND_AUTHORITY_AUDIT.json`
- `02_EXECUTION_PROVENANCE_AUDIT.json`
- `03_CLAIM_AND_AUTHORITY_AUDIT.json`
- `04_FINAL_DISPOSITION.json`

Allowed dispositions:
- `APPROVE_AT_DECLARED_GRAIN`
- `CHANGES_REQUIRED`
- `ESCALATE_WITH_COUNTEREXAMPLE`

Do not modify implementation, tests, fixtures, worker returns, or prior review artifacts.
Do not merge or self-adopt.

Terminal:

`N10E_PROOF_PROVENANCE_REREVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`
