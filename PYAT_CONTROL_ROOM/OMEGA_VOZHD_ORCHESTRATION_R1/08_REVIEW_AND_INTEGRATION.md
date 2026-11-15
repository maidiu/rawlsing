# Independent review, integration and acceptance

[Start](README.md) · [Reviewer prompt](prompts/REVIEWER.md) · [Return template](templates/worker_return.template.json)

## Review sequence

1. Reviewer reads the commission's requirements and frozen oracle first. Identify missing/ambiguous success conditions before consuming the worker's success narrative.
2. Inspect the exact base-to-return diff, input identities and write terrain. List unexpected files and semantic contract changes. A new commit invalidates prior approval of changed portions until reviewed.
3. Reproduce the most decision-critical positive and hostile cases on the returned commit using a competent execution route. Inspect all required case mappings. Tests that merely reproduce implementation branches are insufficient.
4. Check negative preservation, exact consumer use, lineage, dependencies and replay at the claimed grade. Review unsupported claims as carefully as crashes.
5. Return APPROVE_AT_DECLARED_GRAIN, CHANGES_REQUIRED, TYPED_RESIDUAL or ESCALATE_WITH_COUNTEREXAMPLE. Name exact paths/lines/blobs or runtime artifacts and the failed requirement. Never give unexplained numeric confidence as an adoption basis.

A separate Sol High reviewer gives useful independence but is not proof against shared model errors. Deterministic oracles, hostile fixtures, preserved evidence and final cross-owner validation carry the proof. Author self-checks remain useful but do not satisfy independent acceptance.

## Retry and repair economy

Ordinary first-run failures return to the same worker with a minimal reproducer. After two substantively unchanged diagnosis/repair cycles, HQ requests an independent diagnosis and checks the contract/environment rather than restarting another broad implementation. This is a triage threshold, not a hard limit on well-justified progress. Escalate to Astra only if that diagnosis exposes an E-class problem or still cannot distinguish the competing required behaviors. Existing governed no-retry/failure-preservation laws override these defaults.

## Single integration owner

Integrate accepted commits onto a named source-free integration branch based on a verified current implementation snapshot. Preserve both the originally tested worker commit and the actual integration commit. Resolve conflicts by contract and test evidence; do not choose whichever patch is newer. Re-run affected tests and the small cross-owner suite after integration. Do not repeat all unrelated historical suites.

No worker updates the control branch. HQ may promote accepted source-free work within the user's authorized scope only after independent review, combined proof and a precise decision record. No automatic merge into semantic PRE-MAIN or change to survey authority follows. If branch protection requires a PR, use that mechanism; never force-push around it. Attach immutable implementation/proof identities to the HQ decision and seal the checkpoint.

## Minimal combined join

The join must exercise actual components together: empirical input → query/discovery → composed analytical output → actual consumer, with required lifecycle/replay context. Include different-condition/same-label collision, incompatible risk/measure, non-scalar joint preservation, a negative state, a recursive ancestry witness and one changed determinant. If C3 is in the intended live route, include its accepted code in the integration identity and relevant source-free facade interaction. C2 supplies only authority cells needed by the declared workload; unrelated unresolved estate cells remain visible.

Keep proof labels separate: STATIC_INSPECTION, SOURCE_FREE_EXECUTED, HISTORICAL_REAL_SOURCE_RETAINED, CURRENT_REAL_SOURCE_EXECUTED, POPULATED_PRODUCT, COMPOSED_CONSUMER and DECLARED_ESTATE_ACCEPTANCE. They are dimensions, not a single ascending count. A hundred unit tests cannot substitute for an absent final consumer or exact authority.

## Rollback and preservation

Record previous implementation/control heads and revertable commits. Preserve failed logs, oracle hashes and partial outputs under the assigned return directory; label them failed/incomplete. Do not erase evidence to obtain a clean return. Revert an integration defect through ordinary reviewed Git history, not destructive reset of shared history. Retained historical proof remains retained evidence even when its current applicability fails.
