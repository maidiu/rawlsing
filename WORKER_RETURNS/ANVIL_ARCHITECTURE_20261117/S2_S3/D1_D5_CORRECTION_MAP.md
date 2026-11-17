# D1–D5 CORRECTION MAP — same architect, exact documentary correction

**Predecessor candidate:** `98b8d261accfcc7834c86d3f0d52f23e4524f666` (tag
`anvil-architecture-candidate-20261117-r1`, untouched).
**Review:** independent C `a352626dc05a03072c04954bfae6a42c0ece7dfa`,
`REVISE_EXACT_DEFECT`; direction conditionally competent, package not coherent.
**Correction status:** documentary only; no product/native/engineering change.
**Reviewer limit preserved:** source-lineage inspection was sampled, not an
exhaustive recensus; no source-lineage recensus is claimed here.

| Defect | Correction path | Evidence/witness | Remaining limit |
|---|---|---|---|
| **D1** stale `specialist_dependency.status=PENDING` while frozen | `S2_S3/FINAL_DECISION.json` now has `specialist_dependency.status=BOTH_RETURNS_RECEIVED_AND_ADJUDICATED`, `final_selection_frozen=true`; old plan only under `historical_plan_only`; provisional plan docs carry `SUPERSEDED_BY_FINAL` | `GUARDS/v2_supplementary_guard.py` checks status; `RUNS/v2_guard_baseline.txt` PASS 20/118; negative `stale_pending_dependency` REFUSE in `RUNS/v2_guard_negatives.txt` | No new specialist dependency; both exact returns already consumed |
| **D2** selected strategy vs stale SC-ESTATE machine fields | `FINAL_DECISION.json` `selected_design`, `physical_architecture`, layers, `implementation_sequence`, all 16 `per_requirement_candidate_effect`, and `FINAL_OBLIGATION_CROSSWALK.tsv` regenerated for prepared-session-first + conditional construction/recovery + held durable index | Guard checks selected/held/conditional; negatives `stale_sc_estate_name`, `stale_requirement_effect`, `unconditional_durable_index`, `unconditional_one_certificate` all REFUSE | One-certificate and durable index remain conditional/held, not implemented |
| **D3** 16/16 guard cannot see 4 V2 requirements | Added `GUARDS/v2_supplementary_guard.py`; calls accepted instrument guard, then checks 4 V2 addendum requirements, 4 dispositions, 4 crosswalk rows, 118 identities, D1/D2 coherence. Baseline **20/20 + 118/118** | `RUNS/v2_guard_baseline.txt` PASS; 12 omission negatives + stale/unconditional negatives REFUSE; accepted guard omission still PASS then supplementary REFUSE; exact restore PASS (`RUNS/v2_guard_negatives.txt`) | Local structural guard only; not independent C/H1/native |
| **D4** prepared subclass rejected by named first-consumer/Batch; execution grade overstated | Wrapper/Batch handoff relabeled **PROPOSED_NOT_WIRED**; direct prepared path separately **EXECUTED_SOURCEFREE_DIRECT_PATH_3_OF_34**. Exact boundaries recorded: `pre553_saved_workload_integration.py` lines 42/54/94 and `pre553_batch_runner.py` line 406; `SavedC11Admission.execute_i03/i05` still open fresh sessions. Minimal owner-routed explicit prepared mode/protocol recorded; no generic `isinstance` relaxation recommended. | C `WITNESS/test_prepared_abi.py` 2 passed (exact-type rejection); direct prepared 3-test and 34-test sourcefree court cited separately | Actual wrapper/Batch one-`_build`/four-op proof remains a separate owner-gated implementer step; not claimed |
| **D5** provisional artifacts ambiguously live | `SPECIALIST_CONSUMPTION.md`, `PROVISIONAL_STATUS.md`, `PROVISIONAL_INTEGRATED_ANALYSIS.md`, `RESOURCE_MODEL.md`, `BUILDER_CARDS.md` carry `HISTORICAL / SUPERSEDED_BY_FINAL` headers; `DECISION_GUARD.txt` carries `SUPERSEDED_BY_FINAL`; `PROVISIONAL_DECISION.json` status `HISTORICAL_SUPERSEDED_BY_FINAL_DECISION`; manifest roles separate authoritative vs historical | Manifest `document_roles`; final paths named in each banner | Historical files preserved, not deleted; no conflicting live state |
| **N3** Q2 source-vs-transport ambiguity | `FINAL_DECISION.construction_source_transport` requires Q2 built from source-derived typed stream, never re-parsed JSONL; journal is transport/parity only; if unproved, keep second certificate | Guard checks `q2_must_originate_from_source_stream=true`; construction gate text | No one-certificate implementation or proof claimed |

## Authority and limits

- Accepted instrument remains READONLY; no product tests/guards edited.
- The supplementary guard is a local structural check under this return root; it
  calls the accepted guard, does not fork the controller and does not weaken the
  old guard.
- No native/original35/source/science/actor rights, 100k/6 GiB/1–10–100,
  Batch/NORMAL/resume wiring, independent C or H1 is claimed.
- Same distinct reviewer session is asked to recheck this exact correction.
