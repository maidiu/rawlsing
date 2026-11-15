# FIABC LiTS Banked Checkpoint Admissibility — R1

## Holding

**PASS — banked checkpoint is valid retained evidence, but is insufficient to satisfy the repaired ASTRA substantive-parity law without one fresh source-backed I05 execution.**

Accepted normalization/audit base:

`90aea0280bc31007241133d19154cc23c8cedc74`

Banked source-backed evidence commit:

`ed9bc0c9fd8a25e43719650b5cd5b39caa4d613c`

Banked checkpoint identity:

`8593814c51456015e5167cbe6f05037de7dbeadcc36ab857c72192b9087f9062`

Existing frozen LiTS oracle identity:

`eca0ce0ad4bf6299e3705899099c21a0d635e1828f7b4c7e2cee0be4e9f05db0`

Qualification:

- workflow run: `35892434569`
- job: `107287956002`
- protocol self-check: **20 passed**
- governed source-free court: **66 passed**
- conclusion: **success**

## What the banked checkpoint lawfully proves

It retains and verifies:

- exact LiTS source identity: SHA-256 `7cac43e2...`, 29,002 rows, 1,198 variables;
- exact 50-candidate / 77-query-role frontier and frontier seal;
- 49 supported / 1 valid-empty terminal envelope;
- 60 supported empirical fact refs;
- exact current PRE553 candidate identities and query-role predicate/query refs;
- execution identity and replay identity;
- authority/release/projection/replay closure;
- zero candidate processes and zero candidate outputs;
- zero-source checkpoint resume mechanics.

It is therefore admissible for identity, provenance, terminal-envelope, and source-free replay/freeze verification.

## Why it cannot close repaired P0–P4 parity

The newly accepted parity law requires exact empirical substance including complete cell projections and witness arithmetic.

The banked checkpoint, adjacent partial precheck, frozen oracle, and producer receipt contain no:

- `complete_cell_semantic_projection`;
- `raw_numerator_support`;
- P1 `first_exact_dependence_witness`;
- P2 `first_exact_difference_witness`.

The checkpoint's 60 precheck facts retain fact refs, typed state, denominator support, query/predicate refs, and target-domain/topology identity, but not the per-cell support projection needed to recompute P0/P1/P2/P3/P4 substantive parity.

The retained EmpiricalFact content hashes are cryptographic commitments to richer fact preimages, but those full preimages are not serialized in the banked artifacts and no repository serialization of the sampled fact preimages was found.

Therefore it would be unlawful to infer the missing cell arithmetic from historical ASTRA outcomes merely because the current fact refs/terminal states look consistent.

## Required transition

One fresh candidate-neutral source-backed LiTS I05 pass is required **after** the accepted cross-schema normalization is integrated with the source-backed representation/runtime/checkpoint repairs.

That fresh pass must persist the full `astra_shaped_empirical_summary` (or equivalently complete fact preimages) into the new checkpoint before oracle freeze so later finalizer-only recovery is genuinely zero-decode under the repaired parity law.

No Candidate A/B/C, measured P2X, P3, architecture selection, or governed execution-branch advance is authorized.

Terminal:

`PREMAIN_FIABC_LITS_BANKED_CHECKPOINT_ADMISSIBILITY_R1__CHECKPOINT_VALID_FOR_IDENTITY_AND_RESUME__INSUFFICIENT_FOR_REPAIRED_P0_P4_SUBSTANTIVE_PARITY__ONE_FRESH_SOURCE_BACKED_I05_PASS_REQUIRED__NO_CANDIDATES_RUN`
