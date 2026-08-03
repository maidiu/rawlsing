# Section 43 Assembly Provenance

## Source authority

The section was built from the verified cumulative v20 handoff:

`Rawlsing_J_Family_Authority_Strategy_Handoff_v20_20260731.zip`

The pre-v21 v20 verifier return is preserved under `PRE_V21_ROOT_CONTROLS`.

## Authorship and execution

The ChatGPT agent maintaining Rawlsing authored the central plan and machine-readable contract in the active runtime on 2026-07-31/2026-08-01. The work consolidates the complete P3 discussion and binds it to explicit schemas, vocabularies, algorithms, tests, and release controls.

## Inherited-state discipline

All inherited v20 files are required to remain byte-identical except explicitly superseded root and `00_START_HERE` controls. The v21 verifier checks this against the preserved v20 SHA-256 manifest.

## Document construction and QA

The central plan and v21 master handoff were generated as DOCX, rendered with `/home/oai/skills/docx/render_docx.py`, visually inspected page by page, and audited with `/home/oai/skills/docx/scripts/a11y_audit.py`.

## Authority limitation

The section authors the P3 plan only. It does not contain candidate-family execution returns or canonical J-family authority.
