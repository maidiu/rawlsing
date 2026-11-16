# VMESTYE — P0 seed-field fidelity readback (author-side, not independent acceptance)
**Read at:** source immutable commits `bb0814fa39de335558a11fec2b9d085e68216c9a` (D01), `aed1a0ae13c58f11f4dabd07c818b62f72adf989` (#777 C6), VMESTYE source `62e3cbb7713006d69f0567fa63c9ca96d7b2452d`. Authored 2026-11-08, authenticated GitHub `fetch_file` readbacks, deterministic in-memory CSV/TSV parsing. **No local Python, original/native respondents, semantic source/issuer review or S2 execution.**

| Source set | Frozen source rows | VMESTYE rows | Compared fields | Result |
|---|---:|---:|---|---|
| D01 Long Memory LMX | 44 | 44 | `obligation_id`, `historical_obligation`, prior disposition, semantic owner, Trii/Chetiri disposition, prior residual debt | 44/44 exact selected-field match |
| D01 Long Memory LMQ | 30 | 30 | `queue_id`, class, proof/resource, original current status, why it matters | 30/30 exact selected-field match |
| #777 C6 FUNCTION | 29 | 29 | C6 original ID, label, grade, selected/unresolved release IDs | 29/29 exact selected-field match |
| #777 C6 RELEASE | 58 | 58 | C6 AR ID, label, function IDs, selected status/version/document/digest, grade | 58/58 exact selected-field match |
| #777 C6 auxiliary | 7 | 7 | source type (6 denominator, 1 cross-reference), ID, label, grade | 7/7 exact selected-field match |

Original #777 C6 source table contains **94 total rows**, partitioned 29+58+7 with **no unclassified/drop row at this source cut**. This is not 94 disjoint functions. No underlying selected authority-release files were separately reissued or read by this VMESTYE comparison. Git blob pins are embedded in `validation/validate_vmestye.py` so a silent mutation of imported seed bytes fails a bootstrap check.

**Current source fidelity limit:** The five pinned *projected seed files* are field-consistent with the available inherited D01/C6 registers. That does not attest all columns of the original source were physically copied (they were not), all authority usages executed, nor the correctness of any reconstructed semantic successor. The P0 independent reviewer must source-qualify the projection and full no-drop across prior historical/modern/SR-01 registers.
