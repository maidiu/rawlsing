# GROUNDING DELTA — S1 current-code reconciliation

This is the author's independent read of actual code and currentness at the
start of the campaign. It is not a source-rights grant, not an independent
review, and not a claim that the prepared instrument selected an architecture.

## A. What changed relative to the preparation-only return

1. The preparation return correctly refused to select a physical architecture.
   The current mission requires one. This delta therefore treats the accepted
   S2-C/D physical code, the #997 bridge, the #998 saved integrations and the
   `cea2d4d` prepared session as **actual engineering objects to be traced**, not
   as fixture rows to be copied.
2. The prepared package's `DECISION.json` still says "no production backend"
   and "authored instrument fixture only". That decision is superseded for
   architecture purposes by this S1/S2/S3 work. Its 16 requirement rows and 118
   identity rows remain the reviewed common-frame narratives.
3. The accepted source inventory is genuine: 118 mixed identities, 95 Git rows,
   23 ZIP objects/scalars, 26 NOT_ADOPTED, 14 HELD. The old R5/R6 P2 SPINE is
   **not** a prerequisite. No new K3 recensus was performed.
4. Current protected `31291` is later than the `b830` R03/W05 snapshot and later
   than the `cea2d4d` product cut. The `cea2d4d` prepared session is a product
   candidate, not protected. The `b830` snapshot is used only for the exact
   issued-role/preimage route it actually pins.

## B. Actual code path traced (exact files)

- `rawlsing_next/pre553_source_i02_handoff.py`: Q2 one-source-decode typed
  family projection. It builds a direct I02 certificate and emits family
  bodies through a caller-supplied sink. It is not a persisted body store.
- `rawlsing_next/pre553_source_saved_body_bridge.py`: `SourceSavedBodySink`
  writes 13 temporary JSONL family journals, then replays them into the frozen
  S2-C writer. Its own stats disclose `source_decodes_by_sink=0` and
  `second_i02_certification_in_frozen_writer=True`. This is the double-work
  seam.
- `rawlsing_next/pre553_source_direct_parquet_estate.py`: `write_direct_estate`
  consumes all 13 typed family iterators, writes Parquet/Zstd with
  `body_json` + typed columns + `event_locator.parquet`, builds a temporary
  SQLite direct I02, re-reads every row and reconstructs `_row` for physical
  parity, then publishes an atomic manifest.
- `VerifiedDirectEstate`: hashes every member against an independently held
  manifest, checks family counts and locator count, and refuses changed or
  revoked roots. It does not trust a writer-returned digest.
- `pre553_direct_estate_i03.py`: `DirectEstateI03Session._build` scans all
  event and side-family row groups to build a temporary SQLite `events` /
  `members` index. This is O(total events) per new session, even for one narrow
  question. The index is disposable and stores locators, not bodies.
- `pre553_prepared_saved_i03.py`: `PreparedI03Session` reuses one such index
  across many I03/I05 operations. The test asserts exactly one `_build` for
  four distinct operations. This is the correct direction but is still
  process-local and ephemeral.
- `pre553_saved_c11_admission.py`: exact saved admission over the S2-C estate;
  binds release, manifest, I02 roots, catalog, and current authorizer. It is a
  consumer admission, not a second scientific engine.
- `pre553_saved_workload_integration.py`: `execute_saved_i03/i05/batch/normal/
  resume` adapters. Batch/NORMAL/resume require explicit owner ACKs; those are
  typed holds, not silently claimed complete.
- `pre553_empirical_query.py`, `pre553_discovery_exact.py`: the authoritative
  native I03/I05 evaluators. The physical layer must feed these, not replace
  them with a second semantic evaluator.
- `pre553_analytical_composition.py`, `field_forge_conditional_support.py`,
  `pre553_learned_world_composition.py`: F1–F4/FF/learned consumers. They are
  downstream of the native facts; no survey→actor or opinion→power promotion.
- `sorok_history/owner.py`: separate actor/world reader; not a consumer of a
  survey vector as private knowledge.

## C. Actual measured cost witness

From current #1097 body (sourcefree, cut-specific, not production acceptance):

| Measure | Value | What it means |
|---|---:|---|
| writer wall | 3033.723 s | one 100k-shape sourcefree write |
| retained estate | 310.16 MB | the published Parquet estate |
| staging peak | 5.26 GB | stage + I02 + uniqueness scratch |
| temporary writer I02 | ~4.39 GB | SQLite proof scratch |
| native session index | 1.30 GB | per-session `events`/`members` SQLite |
| pre-W05 selected query | 562.362 s | one selected query after the above |
| prepared-session factor | 1.69–1.70× | author report, `cea2d4d`; no independent G5 |

The numbers are **not** comparable to native 100k merely because both say
100k. The frame holds native dense 100k/6 GiB/1-10-100 as `NOT_RUN`.

## D. What is actually preserved, what is not

**Preserved at sourcefree scoped grade:** exact 13-family body/identity/locator
parity; event occurrence; typed state; cold native I03/I05; true same-person
F1–F4 native code; FF01/FF02 separation in sourcefree scoped code; I02
independent root validation; revocation refusal; atomic publish; prepared
session reuse.

**Not preserved/issued:** native original35 source rights; original35 all-wave
execution; native F4/FF02/N9/N10W actual first reader; SOROK actor/consent;
F5/F8/N11/N12 actual consumers; F26 caller; 100k/6 GiB/1-10-100; independent C;
protected H1. The 26 and 14 statuses remain.

## E. Source pointers

- `EVIDENCE/SOURCE_IDENTITY_INVENTORY.json` — 118 source-authenticated rows.
- `EVIDENCE/SOURCE_118/K3_CAP_29.tsv`, `K3_PC_26.tsv`, `K3_P4R_14.tsv` —
  exact K3 rows.
- `EVIDENCE/SOURCE_118/ANVIL_15.md`, `SEAM_25.md`, `SEAM_26.md` — B/S/L
  source material.
- `EVIDENCE/BOUNDARY_CONTRACTS.json` — seven typed boundaries.
- `EVIDENCE/RELEASE_REGISTER.json` — current/revoked release state.
- `SNAPSHOTS/*.txt` — exact small code excerpts with source file SHA-256.
- `S1/SOURCE_SNAPSHOTS.json` — excerpt/source hashes.
