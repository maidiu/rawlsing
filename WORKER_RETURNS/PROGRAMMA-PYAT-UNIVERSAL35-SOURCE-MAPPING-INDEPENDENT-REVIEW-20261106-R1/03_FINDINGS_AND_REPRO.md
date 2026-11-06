# A SRC31 source-mapping review — findings and exact reproductions

## 1. Factual mapping is correct at the selected SRC31 boundary — ACCEPT_SCOPED

The existing bounded probe was rerun against the authorized SRC31 source root (selected affected columns only; aggregate output only):

```text
affected slots: c10ai, c12, c17, c18a, c18b, c18d, c18e, d3, d7, d12, d13
corrections_applied: 31
old_config_refusal: SourceBackedC11FacadeError: unbound response value/state; no label/frequency/missingness inference
corrected_candidate_events: 92,862
states: DK 13,497; MISSING 6,387; NOT_ASKED 1,111; INVALID_UNRESOLVED 325; SUBSTANTIVE_RESPONSE 71,542
c10ai: 98=DK; 99=NOT_ASKED
candidate_seconds: 73.75
```

The old pinned config is the mapping-severed case; the corrected config is the restored positive. No rows, native keys or raw bytes were emitted or committed.

The 31 changes are exactly 14 replacements plus 17 additions across the 11 named slots. `INVALID_UNRESOLVED` remains a typed non-substantive state (325 events), not a label/frequency inference. The SRC31 fixture has 0 corrections; only SRC31 original has 31; estate counts remain 35 sources / 18,276 items / 18,413 slots.

## 2. Actual SAV labels support the declared states

Metadata-only probe against the exact SRC31 source SHA:

- `c10ai 98` -> `98: DK`; `99` -> `99: NA`
- `d3 9`, `d13 9` -> `NA`; `c12/c17/c18a/b/d/e 8` -> `No opinion`
- `c18a/b/d/e 0` -> `Could not understand`
- all 17 `d7`/`d12` additions have no SAV label and no declaration, so they remain `INVALID_UNRESOLVED` with `OBSERVED_STORAGE_VALUE`.

The declared labels and missing declarations match the correction resource. See `evidence/a_labels.log`.

## 3. Binding contract does not enforce base path/commit — REVISE

The registry carries:

```text
base_commit: 1924499e...
base_config_path: rawlsing_next/source_configuration/data/SRC31/source.config.json
base_config_canonical_sha256: 9c00ebc...
source_sha256: de7b51f...
```

`apply_source_config_corrections` matches only `source_id`, `source_sha256`, `base_config_canonical_sha256`, `config_purpose` and `identity_class`. It does not compare `base_commit` or `base_config_path`, and `load_source_config_bytes` does not pass its `path` into the correction binding.

Concrete repro:

```text
path_variant_corrections 31
changed_commit_path_corrections 31
```

A byte-identical config loaded as `different/path/SRC31/source.config.json` still receives corrections, and a scratch registry with a different `base_commit`/`base_config_path` but the same canonical hash also applies all 31.

This does not change the factual mapping (the canonical hash is exact), but it does not satisfy the claimed base-path/base-commit authority binding. Required correction: enforce both fields, or narrow the claim to exact source SHA + base canonical hash. Owner A/HQ.

## 4. Generic source-neutral mechanism and unchanged estate — ACCEPT_SCOPED

- `corrections.py` contains no survey-name branch; it applies versioned resource entries only.
- Correction applies only to `ORIGINAL_SOURCE / SOURCE_PREPARATION`.
- SRC31 fixture corrections: 0.
- Only SRC31 original has corrections: 31; all other 34 originals: 0.
- Denominators preserved: 35/18,276/18,413; no fixture or unrelated source change.
- `SourceConfig.corrections_applied` and library `select`/`validate_source` expose the applied list.

## 5. Tests and limits

- Correction tests: 5 passed in 1.59s.
- Current port/library/foundation/source-read admission: 38 passed in 109.11s.
- Total 43 passed, matching the author evidence.
- Full release validation remains `NOT_RUN__POSITIVE_AUTHORITY_DEFER_EXPECTED`; no native/science/actor acceptance.
- The probe reads only authorized SRC31 selected columns; no rows or native keys are output/committed.
- No all35 decode, 600s rerun, product repair, guide/protected write or source edit was performed.

## 6. Preserved boundaries

- Source custody SHA remains `de7b51f9abf455b072555a84c5592e3ac46bb32c4f9f61bc055160f7d871e571`.
- No original data root is embedded in product/Git evidence.
- Existing source-read admission is not turned into native scientific acceptance.
- F/D/G lanes remain independent; this review does not wait for or accept their new outputs.
