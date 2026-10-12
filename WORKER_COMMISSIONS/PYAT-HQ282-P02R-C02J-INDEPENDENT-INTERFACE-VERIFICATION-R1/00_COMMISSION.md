# Pyat HQ282 P02R — Independent C02J interface verification

**Status:** Prepared for assignment; the secondary-Mac worktree and runtime still require local confirmation. This is a replacement for the earlier P02 reviewer assignment, not an additional independent review to run alongside it.

**Repository:** `maidiu/rawlsing`  
**Review branch:** `agent/reviewer-pyat-hq282-p02r-c02j-independent-interface-verification-r1`  
**Exact starting commit:** Use the complete GitHub commit containing this file, confirmed in the accompanying launch message.  
**Reviewer:** Independent local Python/code reviewer; not the C02J implementation author.  
**Model:** GPT-6.1 Sol, **Low** reasoning effort. Do not automatically increase it.  
**Computer:** Secondary Mac.  
**Existing scientific/program authority:** `HQD-2026-10-10-280`. This review does not adopt or change authority.

## Communication style and platform access

Use plain software-engineering language in discussions, code comments, terminal summaries, and the final review. Explain the expected behavior, the actual behavior, and how the result was verified. Examples of helpful labels are "repository consistency", "release identity", "permission reference", "saved-state loading", "revocation", "event reference", "independent expectation source", and "normal publication path".

Preserve the substance of all required checks; do not suppress failing outcomes or weaken cases merely to change wording. This is a bounded test of the user's existing local project using synthetic test material, not an attempt to gain access to any external system.

Do not create an external account or use a separate hardware security key merely to carry out this commission. If an actual platform requires additional authentication, permissions, or produces a safety/access warning, describe the request accurately and stop the affected operation. Do not try to circumvent platform restrictions.

## Preflight before any coding or tests

Confirm the existing review branch HEAD, actual secondary-Mac worktree, clean repository status, correct shared Git object store, Python/pytest availability, exact code objects, and current available model/quota. Use an already prepared, isolated sparse worktree for this new branch. If one does not exist, report `WORKTREE_SETUP_REQUIRED`; an authorized infrastructure operator can prepare it from the existing secondary shared Git repository. Do not use another worker's worktree, create another repository clone, reset local work, or assume the primary Mac's paths exist on the secondary.

This review must remain independent of the C02J implementation. Read the candidate at the following **unchanged exact source commit**:

`895980397cc0533043c7ca0e493ebbb455666c1e`

Inspect the following Git-tracked files and their imports at that commit:
- `rawlsing_next/pre553_b5_owner_held_verifier_candidate.py`
- `rawlsing_next/repro/c02j_owner_court.py`
- `rawlsing_next/repro/c02j_mandatory_overlay.py`
- `rawlsing_next/pre553_learned_product_lifecycle.py`
- `rawlsing_next/pre553_learned_product_release.py`
- `rawlsing_next/pre553_empirical_objects.py`
- `WORKER_RETURNS/PYAT-HQ281-C02J-REAL-B5-M2-PRODUCER-TRUST-R1/` (original source-free review evidence)

Use exact Git objects rather than copying files from the primary Mac. These synthetic C02J tests do **not** require raw survey `.sav`/`.dta` files, personal documents, external accounts, or live credentials.

## Review objective

Determine, with fresh local tests and exact code inspection, which identity and permission checks the **C02J test-only verifier** actually enforces at M2/B5 owner entrypoints, and which decisions still require an independent producer, permission or expectation authority.

The implementation report contains 24 source-free cases, including normal use and invalid inputs. Reproduce the relevant baseline cases and add independent cases where they reveal a real untested boundary. Check both ordinary calls to the accepted unmodified owner and calls made through the candidate's verification layer; clearly identify which code was in effect for each result.

### Required review scenarios

1. **Ordinary operation:** A correctly prepared product with matching identifiers reaches the expected development-grade publication result through the reviewed test-only interface. State whether the result is marked `authorizing=false`.
2. **Independent expectations:** The expected identity and allowable scope are prepared separately from the object under review. Check what happens if the repository and its expected identity are both replaced consistently *before* verification begins. Distinguish the candidate's internal consistency from an external authority decision.
3. **Release and permission consistency:** Supply mismatched release, expected-product, authority-snapshot or permission references in local fixtures. Record whether the candidate rejects each mismatch and why.
4. **Event reference consistency:** Check whether owner method calls verify event authority and rule references, rather than merely preserving their well-formed structure.
5. **Saved state and currentness:** Check saved-state loading and restoration, obsolete replay grades, incomplete saved records, selected-current publication state, and the distinction between a previously saved claim and a freshly checked fact.
6. **Revocation:** Confirm behavior when a release is recorded as revoked or no longer eligible for selection, including relevant as-of scope.
7. **Object lifetime and aliases:** Where the implementation supports them, check a changed object after the expected state was recorded, alternate references to the same repository, and concurrent calls. Clearly distinguish supported cases from cases not exercised.
8. **Owner coverage:** Inspect the candidate's documented eight lifecycle/release method wrappers and identify any actual owner entrypoint that can still change M2/B5 state without passing through the proposed check.

Run local synthetic tests only. Do not connect to real publishers, production credentials, external services, or private respondent files. In the return, count PASS, FAIL, SKIP and untested cases separately. If the local Python environment or exact Git objects are unavailable, give a precise setup report instead of claiming that tests executed.

## Limits and review conclusions

- Do not change the frozen C02J implementation or accepted M2/B5 owner code.
- Proposed code adjustments belong in the review report or new reviewer-owned tests, not the implementation tree.
- The reference design itself reports unresolved independent permission ceiling, expected-identity issuer, event provenance, replay completeness and source-of-revocation questions. Verify rather than silently treating those as solved.
- An internal consistency check is not the same as a separately authorized producer or permission identity.
- Passing local tests establishes only the declared **source-free test scope**. It does not establish a current production publisher, G0b permission, whole-project acceptance, or permission to activate a new actor/world service.
- No new source-read, scientific, model-use, release or integration adoption is issued here.

## Resource allocation

The user identified **primary Mac Codex at 85% weekly remaining** in the 12 October screenshot, reserved for Astra requiring the full local repository. The **secondary Mac showed 98% remaining**, used for ordinary coding/review. GitHub-only Astra may use either account at the user's direction. Both percentages are historical observations, not live meter readings.

Run this review on secondary Codex **GPT-6.1 Sol Low** only after checking actual allowance and confirming the separate local worktree. Keep a provisional secondary weekly floor of 95% across ordinary Codex jobs, with a suggested two-percentage-point maximum for one bounded job and three points total before the weekly reset. These are manually observed limits, not guarantees about model consumption. Run after P01's usage check unless available capacity has been explicitly confirmed. Do not use reset credits, paid overflow or automatic model escalation. Stop when the available allowance or machine requirements are insufficient.

Apply the RCM01 resource and worktree procedures from the working HQ branch and the sealed original RCM01 source at `c71f83c731fe1465b59f5ad701a5e1bb3018b34a`.

## Return and independent review decision

Produce a complete, easy-to-read return under:

`WORKER_RETURNS/PYAT-HQ282-P02R-C02J-INDEPENDENT-INTERFACE-VERIFICATION-R1/`

Include:
- `00_RETURN.md`: one-page conclusion, tested scope, remaining holds.
- `01_TEST_RESULTS.md`: exact Python commands, actual exits, case-by-case results and skipped cases.
- `02_INTERFACE_FINDINGS.md`: method coverage, good and problematic behaviors, and concrete follow-up requirements.
- `03_ENVIRONMENT_AND_USAGE.md`: secondary environment and consumption snapshots, or explicit unavailable values.
- `04_SOURCE_IDENTITIES.md`: exact pinned Git commits/blobs and reviewer branch SHA.
- `repro/`: reviewer-owned small synthetic tests or scripts where useful.

Commit and push only the designated P02R branch. Verify the remote return SHA. Do not report the candidate as accepted or ready for production by virtue of this review.

**If the secondary worktree is not prepared, the first and only outcome is:** `WORKTREE_SETUP_REQUIRED — no local review executed`.

**Success:** Independent evidence showing exactly which source-free C02J interface properties pass, which do not, and what separate authority or owner work is still needed.