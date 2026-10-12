Initial independent reviewer examined commit 88fe9c165f238ecae470037d22d559cb34d61367.

1. Full checkpoint transaction lock: new run_integrated entry point acquires a separate nonblocking outer lock before planning, keeps it through owner execution, journal/commit, verification and consumer output. New second-process court proves another P01 writer is refused before any durable intent/execution. Calling imported G.run_to_completion directly is outside the supported P01 entry point; the pinned baseline is preserved unchanged and carries the original review limitation.
2. DEFERRED/FAILED scheduling: existing new adapter drives one unit per call and replans after each commit; direct multi-unit baseline calls remain unsupported for P01. Both states are tested as pinned with no repeat execution.
3. Multiplicity: P01 explicitly rejects runnable multiplicity other than one before execution. Field Forge owns single exact RAW two-target facts; unsupported multiplicity is not silently accepted.
4. Unknown/non-success states: candidate guards any claimed success against the verifier measured-result classes, and discovery consumption requires its actual DISCOVERED_RESULT_SUPPORTED receipt. Source-free owner identity and saved receipt checks remain required.
5. Standard discovery: new test conftest relocates exact imported workers under ordinary pytest; historical environment/branch checks are explicit SKIP and replaced by the exact-object/A05 courts. Original test/module bytes remain unchanged.

These fixes apply to the supported P01 orchestration. They do not self-adopt or modify accepted owners or silently repair the banked baseline files. A second independent review is required for the resulting immutable candidate revision.
