# HIST-01 — Original `ddm_build_copy` authority-consumption trace

Status: `HANDOFF__PARTIAL_EVIDENCE_COURT__NO_CLOSURE_CLAIM`

Branch: `agent/vozhd-trii-hist01-original-ddm-authority-trace`  
Exact requested start: `299ef47a17fc96ea31589ea9e3c846e715e96d5d`  
Connected-GitHub branch comparison: `identical`, ahead 0, behind 0, total commits 0.

Task authority:
`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/CONTROL_ROOM_AUTHORITY_PRESERVATION_AND_DEDUP/AUTHORITY_CENSUS_CAMPAIGN/returns/BROWSER/AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/HQ/RECOVERY_TASKS/HIST01_ORIGINAL_DDM_BUILD_COPY_AUTHORITY_TRACE_TASK.md`

Intended repository destination:
`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/CONTROL_ROOM_AUTHORITY_PRESERVATION_AND_DEDUP/AUTHORITY_CENSUS_CAMPAIGN/returns/BROWSER/AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/returns/HIST-01/`

## Why this is a handoff rather than a sealed HIST-01 verdict

The connected GitHub interface was sufficient to prove the root transfer, inspect exact historical
objects, compare selected blob identities against the HIST01 start, and recover a material set of
producer/consumer dependencies. It was not sufficient to run a full local `git log --all --follow`,
`git rev-list`, `git ls-tree`/`git grep` court over every historical ref. The execution container
could not resolve the remote for a checkout.

Therefore this packet deliberately does **not** claim the exhaustiveness required by §8 of HIST01.
It preserves every material finding recovered in-session and gives Codex a precise continuation
protocol.

## Principal findings

1. **Historical root:** `a819fb35337ea28c4a83352d0040030b3da83a7a` (`Publish curated V550+ pipeline source`, 2026-08-13).
   The root commit describes itself as a curated transfer of an already-existing V550→V552J
   implementation, not the origin of that implementation. It explicitly excludes generated output
   trees, run logs, respondent-level data, database files, archives, caches, virtual environments,
   and environment files, while expecting runtime data and a database connection from the receiving
   environment.

2. **The repository root is therefore a transfer boundary, not an epistemic origin.**
   Some information-bearing inputs consumed immediately by the transferred code were already
   external/unversioned at first Git appearance.

3. **Proved missing-at-root external authority:**  
   `data/final_codebooks/questions_master_drivers.csv` is read by
   `apply_postgres_facet_ready_substrate.py`, but querying that exact path at `a819fb35337ea28c4a83352d0040030b3da83a7a` returned 404.
   The same is true of
   `data/final_codebooks/structural_registries/gss2010_structural_overlay.csv`, which is named by
   `ddm_v550_question_use.py`.

4. **Runtime database state is a historical input.**
   The root substrate expects `DATABASE_URL`, live Postgres relations such as
   `survey_microdata_respondents`, `survey_microdata_responses`, and `respondentsDemo*`, and
   respondent-level survey weights. Those bytes/state were intentionally not in Git.

5. **Authority resolution itself carries semantics.**
   `ddm_v550_family_overlay.py` makes authority selection depend on:
   - `DDM_AUTHORITY_ROOT` when set;
   - otherwise `data/ddm_build_copy/reports`;
   - canonical family stem ordering;
   - wave alias ordering;
   - suffix ordering;
   - "first existing candidate wins";
   - fail-closed source/wave validation.
   The root snapshot does not contain the generated `reports/` authority payloads, so exact
   historical overlay bytes used in a run cannot be recovered from the root tree alone.

6. **Survey identity is code authority.**
   `ddm_survey_identity.py` embeds family aliases, wave canonicalization, EVS year↔wave rules,
   Arab Barometer Roman/numeric wave equivalence, and fail-closed country behavior. Its blob
   `617e2b4f...` is unchanged between `a819fb35337ea28c4a83352d0040030b3da83a7a` and `299ef47a17fc96ea31589ea9e3c846e715e96d5d`.

7. **Question relation authority is a distinct, exact authority species.**
   `ddm_v550_question_relation_authority.py` reads
   `bindings/question_relation_registry_35wave_active_v1.csv`, with environment override support,
   and explicitly separates question-level structural authority from response-category semantics.
   The registry blob `daac001b...` is unchanged between `a819fb35337ea28c4a83352d0040030b3da83a7a` and `299ef47a17fc96ea31589ea9e3c846e715e96d5d`.

8. **Hidden code constants are historical authority.**
   The same resolver embeds source aliases and a country-alias table (`BF -> LS`, `LY -> YE`).
   Whether those mappings were intentional domain law or a defect must be adjudicated historically;
   they cannot be erased from the dependency graph merely because they are code.

9. **V550J execution is release-gated.**
   Root `ddm_v550j_registry_contract.py` hard-codes:
   - `P3-AUTHORITY-2026-08-02-R184`
   - `V550J-BOUNDED-AUTHORITY-2026-08-02-R1`
   - `V550J-LAYER1-AUDIT-AUTHORITY-2026-08-03-R1`
   and fails on unexpected release identity. At `299ef47a17fc96ea31589ea9e3c846e715e96d5d` the file has evolved to typed
   fail-closed registry states, but those release IDs remain conserved.

10. **Section 85 binding is semantic governance, not plumbing.**
    Root `section85_binding_authority.json` fixes canonical DB relation names, a forbidden stale QSM
    relation, preferred/fallback response-long relations, source aliases, stage order, compatibility
    rules, and privacy rules. `section85_stage_artifact_authority.csv` additionally binds concrete
    per-scope stage artifacts, paths, observed hashes, and semantic purposes.

11. **Generated/private carriers were treated as inputs by later stages.**
    `v550_shared_respondent_substrate.parquet` is explicitly runtime-private, while its schema
    includes source/wave/country/respondent identity, weights, response semantics, directionality
    provenance, source-structure provenance, mapping status, joint-configuration selection, etc.
    This is an authority-bearing derived carrier even though it must not be committed.

12. **Preliminary TIR crosswalk:** no new terminal information *class* outside the frozen 68 TIRs
    has yet been proved. However, several exact historical authority objects remain unrecovered.
    That is not closure. The strongest current disposition is
    `PRESUMED_BY_CONSUMER__EXACT_AUTHORITY_OBJECT_NOT_YET_RECOVERED`, especially for the
    transferred-but-unversioned question-master, live DB snapshot, generated overlay packets, and
    execution-time environment bindings.

13. **No `HISTORICAL_AUTHORITY_FOUND__TERMINAL_INFORMATION_NOT_YET_ACCOUNTED` row has been proved
    yet.** This is a provisional negative finding only; it cannot be promoted to a 68-TIR
    completeness verdict until the full consumer denominator and forward history are mechanically
    exhausted.

## Files in this packet

- `ROOT_COMMIT_PROOF.md`
- `ROOT_SNAPSHOT_MANIFEST.csv`
- `BACKWARD_PRODUCER_INPUT_EDGE_LEDGER.csv`
- `FORWARD_AUTHORITY_EVOLUTION_LEDGER.csv`
- `HISTORICAL_CONSUMER_DEPENDENCY_LEDGER.csv`
- `HISTORICAL_AUTHORITY_OBJECT_LEDGER.csv`
- `HISTORICAL_TO_CURRENT_TIR_CROSSWALK.csv`
- `POTENTIAL_TIR_ORPHAN_LEDGER.csv`
- `EVIDENCE_INDEX.md`
- `CODEX_CONTINUATION_INSTRUCTIONS.md`
- `HANDOFF_STATUS.json`
- `FILE_SHA256SUMS.txt`

The CSVs contain proved rows plus explicit unresolved/continuation rows. They are evidence ledgers,
not declarations that the denominator is complete.
