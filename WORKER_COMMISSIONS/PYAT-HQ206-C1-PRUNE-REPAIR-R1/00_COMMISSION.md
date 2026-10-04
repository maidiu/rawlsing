# PYAT HQ206 — C1 over-import prune repair — R1

Repository: maidiu/rawlsing
Role: bounded repair worker — Space Bunny High

Branch:
agent/rabochii-pyat-hq206-c1-prune-r1

Exact repair base:
88f262b94bbe94cd3e2a8113c8b17d0872c5089c

Independent review:
7f33fdd7964ed9cd4d2a85aaafec79903395a304

HQ206 adjudication:
ee8e7a1aef1b1eba19b8ca0304186636cd3f874e

Checkout: SPARSE_REQUIRED

## Mission

Perform ONLY the blocking/documentary repairs identified by the independent C1 review.

Do not redesign analytical semantics.
Do not change the five accepted production owner blobs unless the review explicitly proves one is wrong. It did not.

Read exactly from the review commit:
- WORKER_RETURNS/PYAT-HQ205-C1-CONTROL-RECONCILIATION-INDEPENDENT-REVIEW-R1/02_IMPORT_NECESSITY_AUDIT.json
- .../05_COURT_AND_REGRESSION_REVIEW.json
- .../07_FINAL_DISPOSITION.json

### Required repair

1. Remove exactly the 54 authority-material files classified UNNECESSARY_OVERIMPORT.
2. Preserve exactly the 9 authority-material files actually opened/required by the accepted 454-test court.
3. Preserve the five accepted production owners, accepted tests/support, and all already-control-resident lawful dependencies.
4. Correct return documentation:
   - remove the false "unreconstructed record" claim;
   - cite the two historical machine-readable exact per-file court maps identified by review;
   - state dependency necessity at FILE grain, not directory grain.
5. Do not import or remove anything else.

### Qualification

Re-run the exact accepted 15-file 454-test court.
Required:
- 454 collected;
- 454/454;
- twice if practical using the same governed source-free environment.
Re-run the before/after regression comparison or a review-equivalent exact-ID check sufficient to show the prune introduces no new failures.

Also prove:
- the 54 removed files are not opened by the accepted court;
- removing any of the preserved 9 required authority files still causes the expected fail-closed qualification break (a bounded sensitivity check; one representative is sufficient if the review already proves all nine collectively).

## Output

00_RETURN.md
01_PRUNE_MANIFEST.json
02_REQUIRED_NINE_PRESERVATION.json
03_COURT_AND_REGRESSION_RECEIPT.json
04_DOCUMENTATION_CORRECTIONS.json
05_FINAL_DISPOSITION.json

Allowed:
- C1_PRUNE_REPAIR_COMPLETE__READY_FOR_FINAL_ACCEPTANCE
- C1_PRUNE_REPAIR_INCOMPLETE__NAMED_DEPENDENCY
- C1_PRUNE_REVEALS_ACCEPTED_GRAIN_CONFLICT
- C1_QUALIFICATION_FAILURE

No source access. No self-adoption.

Commit, push, re-fetch, verify.

Terminal:
HQ206_C1_PRUNE_REPAIR_RETURNED__HQ_FINAL_REVIEW_REQUIRED
