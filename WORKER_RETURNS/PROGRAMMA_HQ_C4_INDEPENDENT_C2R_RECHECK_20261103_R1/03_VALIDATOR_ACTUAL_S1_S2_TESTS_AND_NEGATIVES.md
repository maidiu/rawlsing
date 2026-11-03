# C4 validator exact-source inspection, S1 counterexamples and S2 NOT_RUN

**File:** CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_three_frontdoors.py@45f327a9086b4c95d0807da0774742b9ed8a626a; blob 9442c623a88d15ee5adfce21911ba4a14ee69afa.
**Manifest:** CROSS_HQ_CONTROL_ROOM/PROGRAMMA/SHARED_RULE_SOURCE_MANIFEST_R1.json@45f327a9086b4c95d0807da0774742b9ed8a626a; blob d99c2031eea888d1abbeba932cc1ed27fc0231c2.
**Scope:** connector-based S0–S1 GitHub source review only. **No Python compiler, pytest, validator invocation or authorized full local checkout was used.**

## Observed S1 source facts

1. Static check parses exactly tagged HQ-C1/C2R rules (Python lines 12, 23–29), compares manifest-defined shared/local sets and copied bodies (58–100). It checks eight manifest-defined untagged exact bodies (85–89), warm markers and three-court labels, and notices known G4 false-accept phrase.
2. Three-court parser (39–56) enforces ENGINEERING, SCIENTIFIC, AUTHORITY ordered headings and all five separate **nonempty** fields. It does not establish semantic falsifiability of arbitrary replacement text.
3. Selected-current-law mode (108–124) resolves selected ref as a Git commit, verifies the immutable pinned commit:path Git blob and compares **every entry present in manifest source_laws** against selected Git commit:path. Without --authoritative-ref, returns REVALIDATION_REQUIRED and main exits 2 (143–153). With --pinned-only, returns PASS and explicit LIVE_AUTHORITATIVE_HEAD NOT_VERIFIED (147–150).
4. GitHub separately returned PRE-MAIN branch tip 773bb412a820949f13a7178b6671327cd56a3bf1; all 15 listed immutable original source-law blobs were retrieved at that SHA, and the GitHub blob IDs match the manifest's 15 pinned_blob_sha1 values. This is an actual S1 connector identity result, not local git command execution.
5. The original source/validator change touched exactly five allowlisted files; later C2R report was only seven added return documents. The three repaired front-door blob IDs match C2R's reported SHA list.

## Material failing adversarial source-inspection counterexamples

**N1 — Omitted authority by synchronized manifest edit (material):** source_laws is defined by the same editable JSON and iterated with for source in manifest["source_laws"] (Python 112–120). No independently frozen expected paths or minimum/exact inventory check exists. If a changed manifest provides source_laws=[] while the 00s and Python remain unchanged, the loop performs zero original-law comparisons; with a valid selected ref, the function returns SELECTED_SOURCE_PARITY_PASS. In --pinned-only mode it still reports PINNED_SOURCE_ONLY PASS, merely displaying source_pins=0. This is a control-flow deduction from actual reviewed Python, **not** an executed S2 negative. More selectively, removing one of the original law paths silently excludes its revision from comparison. The selected 15 are verified today, but the validator does not guarantee 15 remain mandatory tomorrow.

**N2 — Synchronized untagged-body weakening:** if an editor weakens a required untagged operating section in a front door and changes that section's manifest exact_body to match, check_static's comparison (85–89) accepts the mutually changed pair. No external invariant commits the required section identity/body set independently of the edited manifest. Current eight are accurately represented; the no-drop guarantee against co-edits is not proved.

**N3 — Syntactically present but vacuous courts:** replacing each substantive ACCEPT_IF/HOLD_IF/FAIL_OR_RED_IF/etc with a nonempty placeholder consistently in all three doors keeps court_matrix's field presence test satisfied. Shared copied-text parity is likewise satisfied. Human semantic review currently finds complete genuine criteria, but script's claim cannot be broader than syntactic enforcement. Avoid claiming that arbitrary text with correct labels passes scientific acceptance.

**N4 — What is correctly blocked by current source logic:** a malformed/missing tagged individual ID or duplicate parsed ID is rejected (23–29, 58–73); a one-sided shared-rule copy drift is rejected (81–84); removing any manifest-enumerated required untagged section fails (85–89); removing a three-court field fails (39–56); no independently selected current source returns REVALIDATION_REQUIRED exit 2; changing one of the **listed** governing blobs at selected ref yields REVALIDATION_REQUIRED. These are S1 deductions only, not actual Python receipts.

**N5 — Distinguish two different checks:** Git commit SHA points to commit; pinned_blob_sha1 is the Git blob object for the source file. The code uses selected_sha:path and pinned_commit:path, not a simple equality of commit SHA with blob SHA, and is correct for *listed* paths. Weakness is completeness, not confusion of the two types.

## S2 mandatory negative suite — NOT_RUN

The following commands are **future owner-run procedures, not commands executed by C4**. Qualified prerequisite: independently verified authorized exact full local checkout of 45f327a9086b4c95d0807da0774742b9ed8a626a plus its governing original Git objects, selected current protected ref, isolated disposable mutation fixture and recorded host/clock/import/permissions.

1. python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_three_frontdoors.py --pinned-only → expect scoped PASS and LIVE_AUTHORITATIVE_HEAD NOT_VERIFIED.
2. python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_three_frontdoors.py → expect exit 2 REVALIDATION_REQUIRED.
3. python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_three_frontdoors.py --authoritative-ref <owner-selected-verified-PRE-MAIN-ref> → expect listed exact original-law blob comparison; exercise modified selected source law → exit 2.
4. Remove manifest-enumerated operating section (leave manifest unchanged) → FAIL; remove bilateral passport clause/00D ID → FAIL; omit single named court field → FAIL; drift shared rule copy → FAIL; missing/duplicate stable rule IDs → FAIL; commission missing a court field → FAIL.
5. **Add new M4 falsifier:** remove or substitute original governing law from manifest source_laws, and separately shrink required_untagged_sections while changing the same door: the current code is predicted falsely green. Make exact source-set completeness fail independently of the mutable manifest and rerun.
6. Require actual commands/exit/output/positive→fault→restore receipts under authorized checkout. Do not present C2R's five JavaScript in-memory S1 simulations as Python execution.

**S2_EXECUTION = NOT_RUN.** Actual command log: none. Actual stdout/stderr/exit code: none. Host/account/runtime/import/source-closure: UNKNOWN as local authorized runner. GitHub authenticated S1 source read is not a Python source import.
