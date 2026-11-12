# PYAT R3 S1-C — Agent B adversarial construction return

**Role:** B, implementation challenger/repair author, not independent G5 reviewer. **Parent:** P1-04 / #918 / #909 R3/R3C/R3S. **Sourcefree only.**
**Opponent frozen HEAD:** `5a6eb73158479a3bf4cead70b0d36cca43d902b6`; A tested `9a539024f3d2a23f96e4e4fa50a0e749b0d6b56f`. **B tested code candidate:** `e15ccaedaa54155fc3855f821565e2794c946a68`. **B PR:** #955 against A's branch, not protected. **Upstream sourcefree integration:** #948 `7064daa14d93109211629e72d08f3a6e705a0d57` (unmerged); protected PRE-MAIN at inspected cut `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## Independently reconstructed mission, not A's narrower framing

P1-04/S1-C must preserve the *supplied* source-qualified candidates and independently supplied scientific U_item/U_unit/U_app/E_pre operation/fate declarations through the existing `ScientificFrontier`, `compile_governed_frontier`, real issued test-only Batch/C11/I05 first consumer, and complete explicit positive/negative/unknown/inapplicable/held/pending execution fates. Both per-operation anti-joins and *non-operation* source/inventory disposition records matter. Never promote historical 18,467 preparatory fates or synthetic operations to issued original35 science; protected merge, original source permission and independent G5 are separate.

## What A got right — preserve it

A reused existing R03 compiler and `execute_governed_frontier` rather than cloning the scientific engine; independently caller-supplied source/scientific operation lists are content-addressed and crosschecked to the typed frontier before opening source; exact source identity, edition, universe, occurrence roles, inventory/current-source authority reference, operation canonical hash and U/E_pre root/disposition consistency are checked. It correctly refused duplicate ID/count-preserving substitutions, wrong source/edition, false native-grade promotion, routing UNKNOWN as administered, and invalidly weighted population issuance while preserving optional-weight SAMPLE/RAW. Native I05 receipts, facts and checkpoint restore are real within sourcefree grade. A correctly disclosed shared synthetic-input-census weakness and the absence of S1-D normal/resume proof in this specific packet. B retains these interfaces and 11 original tests without altering `pre553_universal_workload.py` or `pre553_issued_workload.py`.

## Reproduced-by-source defect: frozen negative axes can disappear silently

Original A module at Git blob `1f68dc6ff60e68d72cee284cb8232f659100b8f6`, `verify_frozen_inputs`: source/scientific operation set parity and `frontier.deferred` parity are checked, but **`frontier.unknown`, `frontier.excluded`, and `frontier.inventory_ledger` are not in `FrozenInputCensus.material` and are not checked anywhere in the verifier**. These are separately typed components of `ScientificFrontier.material` and `InventoryLedgerEntry.material` (at the frozen source). Removing a declared routing-unknown/excluded record or changing one inventory occurrence disposition while keeping all `frontier.operations` unchanged cannot trigger any original A pre-source-open refusal. Original operation IDs, census hashes, eligibility counts and the R03 first-consumer set remain identical. Thus A's operation anti-join is valid but its *claim of exhaustive fate conservation* is overbroad. This is an existing G1/G3 failure, not optional hardening.

## Concrete B patch and three executable hostile probes

1. Extend the original `FrozenInputCensus` (not a new authority or scientific compiler) with `unknown_scope_records`, `excluded_scope_records`, and `inventory_ledger_records`. Include them in immutable census hashing. Verify each independently against the actual `ScientificFrontier` before compiling and before calling `source_factory`. Fail with typed `UNKNOWN_CENSUS_DRIFT`, `EXCLUDED_CENSUS_DRIFT`, `INVENTORY_LEDGER_CENSUS_DRIFT`.
2. Return counts, exact hashes and negative records alongside the existing candidate/fate/result census so the reviewer can identify the conserved axes. Preserve existing operation outputs and physical semantics unchanged.
3. Test an independently supplied frozen sourcefree unknown record then remove it from the frontier; an excluded source record likewise; and mutate a per-occurrence inventory fate while holding all operation IDs, eligible counts and declared source/science hashes constant. Assert refusal before source opening, and after restoring original frontier rerun the actual R03→Batch/C11/I05 result with identical native checkpoint, unchanged frozen census and true candidate/operation anti-joins. Rehashing the operation lists alone must not launder the missing non-operation evidence.

**Patch commits:** `11a22528aceca852e7b39198c550280f7ec08e6b` (implementation) and `e15ccaedaa54155fc3855f821565e2794c946a68` (hostile tests). Changed files only S1-C module and its existing test module. Source/test exact new blobs are retrievable by `git rev-parse <tested-commit>:<path>`.

## Proof and grade

GitHub Actions run `43278463747` is the B S1-C focused and inherited regression court; `43278466894` is the stacked #948 combined integration court. At drafting the focused S1-C test step completed successfully while inherited/combined steps were still in progress; the machine receipt and the final handoff must report the actual terminal conclusions, not assume them. Full command:
`PYTHONPATH=. python -B rawlsing_next/tests/pyat_r3_s1c_rss_runner.py rawlsing_next/tests/test_pyat_r3_s1c_source_operation_fates.py`
and inherited R03/R61 `pytest` test modules. This is a CI runner, not a locally inspected Mac process. B's 3 additional hostile tests extend A's 11; do not confuse prior A's 309/150/330 measurements with newly measured original35 production results. No original respondent source read, no protected integration, no native source/science/current issuer.

## Refuted attacks, own risks, and withheld claims

**Refuted:** Claim that A's compiler/fact implementation should be replaced; no reproduced reason, existing native first reader is appropriate at this grade. Claim that 18,467 historic candidate fates must be directly executed; not scientifically issued. Claim that absence of original35 source rights blocks sourcefree corrective work; false. Claim that a changed synthetic physical cell with unchanged source SHA proves authorized byte-identity; A never claimed it.

**Self attack / new risk:** This fix preserves frontier-declared negative records, not an *externally authoritative proof that the source supplied every possible negative*. A dishonest supplier can still omit a row from *both* the frozen and the live frontier; neither content hashing nor a better local adapter can manufacture original35 source completeness. The additional frozen typed ledger is O(declared inventory occurrences) memory, already comparable to the inherited typed frontier/operation census; no production-scale bound is established. `frontier.unknown` and `excluded` can contain evidence not directly mirrored in the operation ledger; their content must remain qualified by source/science owners. A post-fix sourcefree pass does not mean S1-D CURRENT normal/resume and S1-E full source→I02 are integrated.

## Four-court judgment and R3S stopping

- **Finding:** A's operation conservation is correct for the tested operation universe but omitted three independent non-operation negative/fate surfaces; B now binds them to frozen pre-compilation inputs and introduces real downstream restoration tests.
- **Interpretation:** In-scope SEV-1/semantic-conservation failure at *declared sourcefree frontier*; not evidence that original35 science/host is issued.
- **Action:** A must attack B's exact changed code/tests, try count-preserving exclusion/unknown/occurrence drift, assert positive first reader unaffected; only fix reproduced original-contract defects, then freeze for distinct G5.
- **Owner:** A/B are construction authors; distinct G5 reviews; scientific source issuer, source-host owner, and protected PRE-MAIN owner keep separate jurisdictions.

**G1:** B patch preserves supplied source + fate universe including non-operation axes; engineering scoped candidate awaiting final CI and A counterattack.
**G2:** A actual R03→Batch/C11/I05 demonstrated; B uses restored same real consumer; no S1-D normal/resume claim.
**G3:** Targeted refusal cases added; terminal CI evidence must be read.
**G4:** Stateless adapter reuses existing durable/issued reader; no new CAS; original hosted fixture 309 / 150 / 330 and ~260 MB is A's historical run, B not claiming a new 100k/6GiB measurement.
**G5:** NOT_RUN — neither A nor B is qualified independent receiving.
**Scientific:** ORIGINAL35_HOLD_EXTERNAL. **Authority:** SOURCE/HOST/PROTECTED_INTEGRATION_HELD. **R3S:** no speculative further hardening; after A's counterattack and any genuine reproduced defect repair, submit frozen shared HEAD once to independent G5.

## Strongest challenge back to Agent A

Freeze an independent source-qualified `unknown`/excluded/administration-eligibility snapshot, remove or alter a record without changing operation IDs, and try to make B's new verifier issue a positive first consumer anyway. Then attack whether a source/fate packet **independently** excludes a previously unvisited but eligible operation (not just one in current `ScientificFrontier.operations`). If that latter proof requires an unavailable competent external issuer, record precisely that limitation rather than inventing a science root or reopen this sourcefree engineering packet. Try to show the additional O(n) frozen negative inventory actually violates the declared G4 bound at the same sourcefree scope; reproduce it before calling it a blocker.