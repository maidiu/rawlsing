# SPECIALIST CONSUMPTION — exact dependency for the synthesis owner

**Status:** both returns are `PENDING`; this document defines what will be
consumed and how. It is not a launch order, not a duel authorization, and not an
independent acceptance path. The two specialists are not rival whole-backend
authors; they answer the same whole frame on two bounded economic questions.

## Common inputs (identical for both)

- Frozen common frame: `S1/FRAME.json`,
  canonical digest `7e7bfb9638f23894fd244a703e8a6b88d361f90fafa5b2b10ac78c1f24229913`,
  author checkpoint commit `5a619ff9fa79be9183eb4d4378d42f040ef2bd9b`.
- HQ-frozen source inputs: `evidence/S1_FROZEN` + pins (external).
- Product cut: `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`.
- Protected currentness read: `31291d08179890852246c8742700e055168e9933`.
- Accepted S2-C/D sourcefree code, #997 bridge, #998 saved integration, P0
  prepared session; exact paths in `S1/FRAME.json` `actual_code_pins`.
- Current cost witness (#1097): 3033.723 s writer, 310.16 MB retained, 5.26 GB
  staging, 4.39 GB temporary I02, 1.30 GB session index, 562.362 s selected
  query. This is sourcefree/cut-specific, not native 100k proof.
- Holds: native 100k 600–1,300 slots, process-tree ≤6 GiB, 1/10/100, F26,
  original35/source/science/actor, independent C/H1 all unchanged.

## Specialist 1 — construction/storage/proof/recovery economics

**Single question:** Does the single-certification canonical estate plus
per-row-group physical digest and manifest-bound I02 roots preserve the current
attacker resistance while removing the second I02, 13 JSONL journals, per-row
object re-encode and per-session full scan? What are the exact retained/scratch/
writer/recovery costs and failure dispositions?

Required return:

1. Exact code path at `cea2d4d` and accepted S2-C/D cuts; which symbols are
   changed, which are reused, which are untouched.
2. A sourcefree measurement or a precise bounded hold for: writer wall,
   retained bytes, peak staging, peak process-tree RSS, object reconstructions,
   source reads, I02 builds, JSONL bytes.
3. Attacks: changed body byte, changed locator, changed row-group bytes, changed
   member, changed release/I02/source root, revoked member, crash before/after
   manifest link, rebuild from canonical estate. Each must be `REFUSED` or
   `EXACT_RESTORE`.
4. Whether the per-row-group digest is equivalent to the current full per-row
   `_row` re-encode for the defined threat model; if not, the second-pass
   fallback and its cost.
5. Strongest reverser and smallest falsifier.
6. Any material new requirement or source contradiction (must be returned to S1).

## Specialist 2 — native repeated-query/shared-preparation/evidence-output economics

**Single question:** Can the manifest-bound immutable selector/denominator index
plus prepared native session deliver economical 1/10/100 distinct native
I03/I05/Batch/F1–F4 operations and bounded evidence/replay output without a
second evaluator or a stale authority? Where does native risk enumeration
dominate?

Required return:

1. Exact native I03/I05/F1–F4 call path and risk/denominator behavior; what is
   indexed, what must still enumerate the full risk population.
2. A sourcefree model or measured run for cold open, 1/10/100 distinct
   operations, repeated same-process vs fresh-process, selected row-group reads,
   native risk enumeration, F4 joint, evidence output.
3. Evidence/fact/replay output amplification accounting: what is shared, what is
   per-operation, what is deduplicated by content address.
4. Index invalidation: changed source/frame/current/revocation, missing/corrupt
   index, rebuild path; proof that the index is not authority.
5. Whether a columnar accelerator is necessary; if so, the smallest exact
   native-equivalence falsifier. It is a separate decision, not a default.
6. Strongest reverser and smallest falsifier.
7. Any material new requirement or source contradiction (must be returned to S1).

## Adjudication rule (synthesis owner)

- No majority vote, no peer-count acceptance.
- If either return introduces a material new requirement or exact source
  contradiction, **version S1** with a transparent diff; do not hide it in a
  specialist appendix.
- If the returns agree, integrate the exact measurements/limits and update the
  provisional decision.
- If they disagree on one named choice, resolve analytically with the exact
  evidence; a targeted duel is optional only if the question is single,
  consequential and cannot be settled from the returns.
- If a return is absent/incomplete at the finite job boundary, publish the
  provisional package and the exact missing dependency; do not poll or wait.
- Final decision remains `CONDITIONAL_DIRECTION`/unfrozen until both returns are
  consumed and independent C is separately commissioned.

## Consumption checklist

- [ ] Return 1 exact code/cost/attack matrix received.
- [ ] Return 2 exact query/evidence/index matrix received.
- [ ] Material new requirement check against S1 completed.
- [ ] Any S1 version diff published before decision update.
- [ ] Provisional decision updated with exact evidence and limits.
- [ ] Final selection frozen only after both; independent C remains separate.
