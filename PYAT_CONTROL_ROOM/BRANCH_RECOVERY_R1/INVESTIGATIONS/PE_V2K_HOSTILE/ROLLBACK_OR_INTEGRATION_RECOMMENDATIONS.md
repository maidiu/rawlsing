# Rollback or integration recommendations

## Bottom line

**Do not integrate the PE-SC0 overlay as production semantics.** Keep it as
sourcefree fixture evidence only. **Uphold current R61 and the historical V2K
retirement at sourcefree scope**, but preserve the original item/namespace C4
anti-join HOLD for a future real-source consumer.

No merge is recommended from this court.

## PE-SC0: reject production integration; retain as fixture evidence

### Why the 13/13 green is not enough

The strict court checks field presence and distinctness. It does not validate:

- world values against a pinned provider/selection digest;
- cell sums versus denominator;
- actual H2 refresh execution;
- enriched receipt identity (`result_hash`);
- source-promotion contradictions;
- negative-status scope/measure consistency;
- replay/currentness.

The hostile court reproduced altered-world acceptance, inconsistent
denominator acceptance, synthesized refresh receipts and a result-identity split.

### Minimum repairs before any successor

1. **Remove `sitecustomize.py` from the integration path.** Install the overlay
   explicitly through a test plugin or owner adapter with a fail-closed
   `TEST_ONLY` guard. Provide uninstall/restore in the same process.
2. **Bind world values to the provider and selection.** Include the exact
   provider commit/blob, selection digest and value digest. Reject any bundle
   whose world values do not hash to that binding. Never copy a selection digest
   alongside altered values.
3. **Validate numeric geometry completely.** Require all cells' numerators and
   exact fractions to sum to the denominator; validate denominator membership,
   denominator record and target-cell direction. Reject inconsistent geometry.
4. **Execute H2 refresh or drop the fields.** If the contract requires
   `structural_publication_refresh_receipt` and
   `generated_binding_refresh_receipt`, call the actual provider refresh
   operations and carry their returned channel/generation/predecessor refs. Do
   not synthesize receipts from `selection_digest`.
5. **Fix result identity.** `EnrichedResult.result_hash` must hash the enriched
   receipt ref and enabled material, not delegate to the original receipt.
6. **Fail closed on source promotion.** A provider
   `may_use_as_source_observation=True` must be refused, not overwritten.
7. **Validate negative status scope/measure.** Require a nonempty source/risk
   scope for HELD/DENIED/MISSING and consistent measure semantics.
8. **Add replay/currentness law if currentized.** A sourcefree pure function can
   be deterministic; a current issuer path cannot accept silent replay.
9. **Keep the test-only reversal snapshot out of production.** If a real
   reversal path is needed, require exact issuer, target, risk/denominator and
   time scopes. The current fixture snapshot is unrestricted and `ALL_TIME`.

### Acceptable PE disposition now

- Preserve the original PE refusal law and exact C1/N10E geometry as evidence.
- Preserve the 13/13 fixture reproduction as evidence that the field set can be
  carried.
- Do not call it production semantics, an operative N9 world, or a real consumer.
- Route to the PE/SC0 owner for a new owner-bound contract, not an overlay merge.

## V2K: uphold retirement at current sourcefree scope

### What is upheld

- Current R61 `NativeWorkload`/`IssuedWorkloadRecord`/`CurrentDecisionResolver`
  is a different ABI from historical V2K.
- Current 8 negative oracles pass; 105 universal tests pass; the independent
  sourcefree positive completes a full Batch at `TEST_ONLY_SOURCEFREE` scope.
- Historical V2K old exact symbols are absent and have no current import.
- The 38-function decision is upheld with one explicit HOLD.

### What must not be done

- Do not transplant the old V2K module.
- Do not claim 63/63 current ABI or 111/111.
- Do not grandfather the prior 2/2 severance claim; exact `9647d851` is
  **1 pass / 1 fail**.
- Do not treat the missing dependency as a silent green.
- Do not use the historical 63 pass as a current consumer proof.

### Preserve the one HOLD

`_validate_original_against_c11` is the old item/namespace/release/routing
anti-join. It is absent from current `admit`. Current sourcefree positive does
not exercise it. If a real original-source consumer appears:

1. preserve the anti-join semantics in a small current adapter, not a wholesale
   historical transplant;
2. bind exact original release, universe, native item refs, routing/risk refs,
   respondent namespace/unit/form/language/occurrence/option scope;
3. run positive and fault-negative tests against the current consumer;
4. keep source/U-E authority HOLD until the source owner grants it.

### Historical dependency provenance correction

The prior `V2K_DEPENDENCY_RESTORATION.json` lists five modules but omits
`pre553_governed_batch_checkpoint_integration_candidate.py`. Without that
module, collection still fails. Adding it from `5eb51c686` produces the 63
historical passes. Any future historical replay must include the missing module
and exact blob in its manifest; otherwise the 63-pass claim is not reproducible
from the declared list.

## Order of operations for a legitimate successor

1. Owner decision: PE overlay retired as production candidate; V2K retirement
   upheld at current scope.
2. If PE semantics are still wanted, build a new owner-bound value contract with
   real source/N9 values, executed refresh and enriched identity.
3. If an original-source V2K consumer appears, build the small anti-join adapter
   under separate U/E/source authority.
4. Rerun current negative suite, 105 universal, sourcefree positive and the new
   negative court.
5. Independent I3 review at exact SHA.
6. Incumbent HQ adoption decision. No self-adoption.

## Rollback

### This review branch

This branch changes only the investigation directory. Rollback is to delete the
branch/worktree or leave it unmerged; no production source or PRE-MAIN state
changes.

```bash
git worktree remove --force /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pe-sc0-v2k-hostile-20261031-r1
```

Do not remove the worktree while retaining uncommitted review artifacts.

### If `sitecustomize.py` was accidentally placed on a production path

1. Remove that directory from `PYTHONPATH` and from any installed `sitecustomize`
   location.
2. Restart the process; `install()` has no uninstall.
3. Verify `rawlsing_next.pre553_postastra_pe_generic_world_possibility` no longer
   has `_original_serve` and `serve_generic_world_situated_possibility.__module__`
   is the PE module, not `sc0_pe_overlay`.
4. Re-run the original PE strict court: it must return 4/13, not 13/13.

### If a PE overlay candidate was merged

Revert the merge commit only through the owner’s review process. Do not
force-push or delete historical evidence. Re-run the original PE strict court and
the current repository tests.

### If a V2K historical transplant was attempted

Revert the transplant, retain the old blobs as evidence, and re-run current R61
negative/positive tests. The old item/namespace anti-join remains a HOLD, not a
reason to restore the whole module.

## Readback requirements

- Remote branch SHA equals local HEAD.
- Only the seven required files are added.
- `git diff --name-only HEAD~1..HEAD` contains no production source.
- Original PE strict remains 4/13.
- Overlay strict remains 13/13 but the hostile defects are recorded.
- Current R61 8 negatives, 105 universal and 9 independent positive/negatives
  remain reproducible.
- Historical V2K original remains collection error; exact repair remains 1/1;
  63 pass only with complete dependencies.

## Final recommendation

**PE: HOLD/RED, do not integrate; keep fixture evidence and repair identity,
binding, refresh and injection boundaries. V2K: uphold current R61 and scoped
retirement; preserve anti-join HOLD; no old transplant. Overall: no production
merge.**
