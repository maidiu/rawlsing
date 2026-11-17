# FIRST CONSUMER HANDOFF — QUERY lane

**Status:** bounded handoff to the integrated architect and the actual owners.
No final architecture acceptance; no protected adoption.

## Minimal real first-consumer operation

One authorized, exact release/universe is admitted once by
`PreparedSavedC11Admission.open(...)` (or the accepted `SavedC11Admission` path);
one `PreparedI03Session` is entered; the existing
`CarrierNeutralResearchExecutor`/`execute_empirical_query` is used unchanged for
**one issued I03 query** (e.g. the selected F1 marginal or F2 forward query in
the owner's workload), and the exact `QueryExecutionResult` fact refs plus
`replay_ref` are emitted. The same session then executes the 10th and 100th
distinct issued operation (including weighted/unweighted, F2 reverse, true F4
3+ same-person, and one I05 with multiple roles), and a fresh process repeats
the admission + one operation. Each operation must produce exact fact/replay
parity with the one-shot baseline and must refuse after revocation.

This is the smallest real operation that tests the actual first consumer. It
does **not** create a new evaluator, a new evidence issuer, or a new scientific
contract.

## What the owner must approve or measure

1. **Forward-wiring (recommended minimum):** use the existing
   `PreparedI03Session` in the actual first consumer and in saved Batch units.
   The current `SavedC11Admission.execute_i03`/`execute_i05` open a new
   `DirectEstateI03Session` per unit; `execute_saved_batch` therefore pays the
   index build per unit. Wiring the prepared session is a bounded integration
   change, not a new backend. Batch/NORMAL/resume shared-file handoffs remain
   the existing typed owner holds; do not silently claim them.
2. **Measurement before new index format:** decompose `H` (admission/member
   hashes), `S` (index build), `Q` (scientific counting) and `O` (evidence
   output) using the #1006 G2 protocol on one authorized real-width workload.
   The 562.362 s selected-query figure is undecomposed; the 1.69–1.70× prepared
   factor is an author report and cannot be extrapolated to 100.
3. **Conditional durable index:** only if `S` is measured material, qualify the
   derived locator index with an independent digest/binding to the estate
   manifest, I02 roots, release/replay/universe, family censuses and row-group
   topology; validate on open and refuse on any change. It must not store
   canonical bodies, must not be a second evidence source, and is not
   “disposable by declaration.” The cited 1.30 GB SQLite index is 4.19× the
   310.16 MB estate and conflicts with compact TOTAL retention unless a much
   smaller exact encoding is proven.
4. **Conditional pushdown:** only if `Q` is measured dominant; any typed/
   columnar/posting/mask/bitmap acceleration must feed the existing evaluator
   with exact candidate streams and preserve all-universe risk states, typed
   missingness, repeated occurrences, weights, F2 directions, F3
   minority/recursive/signed/neutral and F4 true joint. It needs S04/I03
   scientific+physical owner qualification and parity facts; it is not a second
   scientific evaluator.

## Exact constraints the handoff must carry

- one index per exact universe/release; no cross-wave/country pooling;
- `check_current` before/after each operation; revocation refuses;
- facts/replay/authority snapshots recomputed per distinct operation; caching
  is nonauthoritative;
- F6 numeric is not derived from the I07 guard; FF01/FF02 remain separate;
  SEAM/SOROK actor rights are not granted; F26 caller hold remains;
- 6 GiB process-tree cap and the 100k/6 GiB/1/10/100 gate remain NOT_RUN;
- no native/source/actor rights or wave-join promotion from this handoff.

## Owner map (actual code, not a new authority)

- Physical writer/reader and cold estate: S2-C/D owner (#1006/#997).
- Existing I03/I05 evaluators: S04/I03 scientific owner (#998).
- F1–F4 composition: #998 empirical science owner.
- Batch/NORMAL/resume: existing shared-file owners; typed ACKs in
  `pre553_saved_workload_integration.py`.
- Derived-index proof/invalidation: S05/Long Memory plus S2-C/D owner.
- Evidence/output contract: S05/Long Memory and the relevant science owner.

**Stop point:** this handoff is for architect adjudication and user/Browser
decision. No worker launch, no NATIVE run, no protected write.
