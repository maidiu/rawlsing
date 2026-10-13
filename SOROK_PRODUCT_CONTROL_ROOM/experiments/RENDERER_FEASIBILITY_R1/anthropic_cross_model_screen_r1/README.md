# RFA-06C — referent review correction and three-model renderer screening

**Commission state: SOURCE-AUDITED, HARNESS PREPARED, NOT EXECUTED.** Branch is based precisely on `4ce795413c2e77be04657a260cbda586610f4756`. The existing R1 diagnostic court is closed, R2 Opus receipts remain untouched, and all twenty RFA-05B WP/N inputs are unchanged.

## Two distinct pieces of work

1. **Local validation correction.** The R2 checker treated all atom `referent_ids` as physical scene objects. The source contracts allow actor-safe memory/history, differentiated relations, projects, organizational practice and other typed semantic grounds to be attached to a candidate atom. `referent_admission.py` compiles a case-and-arm-local allowlist from explicit actor-visible field locations. Object manipulation and physical world effects still require documented scene W references. Behavior-only source information does not become narratable by being a reference. R2 original warnings are preserved alongside corrected findings.
2. **New model comparison.** Twenty existing Opus 5.5 R2 observations are selected in advance, exactly replicate ordinal 1 for RF001–RF010 in both N/WP. The other forty existing Opus samples are secondary replication evidence. Exactly twenty new Sonnet 5.5 calls and twenty new Haiku 5.5 calls form a freshly shuffled, interleaved, forty-call schedule. Each new model has a separately required non-primary smoke. New requests are cloned from the exact R2 Opus request and differ only by `model`.

## Included artifacts

- `REFERENT_ADMISSION_ONTOLOGY_AUDIT_R1.md`: source-grounded decision, evidence categories, reasons R2 was overrestrictive.
- `REFERENT_ADMISSION_CONTRACT_R2.md`: bounded per-case referent classes and physical-world constraints.
- `referent_admission.py`: compiled typed allowlist and corrected post-generation candidate checker.
- `COMPARABILITY_AND_DESIGN_RECEIPT_R1.md`: exact R2 request parity, preselected Opus twenty, separate forty secondary, independent randomization, claim boundary.
- `MODEL_BINDING_RECEIPT_R1.md`: official current Claude model IDs and provider binding conditions.
- `OPUS_EXISTING_SAMPLE_SELECTION_R1.json`: fixed twenty selected Opus IDs plus secondary R2 IDs.
- `EXECUTION_MANIFEST_PRIVATE_R1.json`: forty new fixed provider calls, including model and arm; keep private.
- `BLIND_MAPPING_PRIVATE_R1.json`: all sixty source-to-blind-ID mappings; keep private.
- `BLINDED_SCORING_MANIFEST_R1.json`: opaque blind IDs only.
- `EXPERIMENT_CONFIG_R1.json`, `screen_common.py`, `run_cross_model_court.py`, `validate_cross_model_court.py`: source and request verification, local freeze, separate smoke gates, new model calls, Opus correction, blind export, offline regression checks.
- `score_and_unblind.py`: prepare score sheet, enforce all 15 inherited scoring dimensions, seal its SHA-256, verify and *separately* explicitly unblind/aggregate.
- `LOCAL_EXECUTION_INSTRUCTIONS_R1.md`: exact owner-local sequence.
- `results/`: five isolated, non-committed evidence/scoring directories.

## Important evidence boundary

The owner reports 60 Opus R2 provider generations and follow-up substantive scores, but **their raw response records are not in this GitHub branch**. This commission cannot reproduce those scores or the claimed 22 referent-only failures from absent private records. The separate owner-local build step requires all sixty exact R2 results, verifies original-versus-corrected issue codes, and refuses to create a complete blind bundle from summaries.

Results are append-only, ignored by Git and separated from the older R1/R2 directories. The new two smoke calls and 40 primary calls are **not made by this authoring commission**. No provider key or token usage is stored in tracked code. Blinded reviewers see only the RF case and raw candidate, never model/arm/replicate/source run or transport cost.

**This is a renderer-only, hand-surrogate upstream-state screening experiment.** It cannot establish Rawlsing production feasibility, lawful future V3 state generation, durable reentry, or user phenomenal projection.
