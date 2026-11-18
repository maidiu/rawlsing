# SRC04 q217 bounded field mapping

## Verdict

**EXACT RESIDUAL IDENTIFIED: 38 observed q217 cells are source code `7.0`.**

There is **no source-corroborated label for code `7.0`**. It is not in the source
codebook labels and not in the physical SAV value labels; it has no declared
missing range or user-missing value. It is therefore preserved as an explicitly
unknown observed numeric code, not inferred to be “other”, “don’t know”,
“refusal”, or a label from another wave.

No canonical, scientific, permission, product, or config-custody file was
changed. The accepted construction witness remains held exactly as before.

## Exact pins

- SRC04 repaired-v2 config:
  - commit `da23c65d1e211cb7e8ce416e98757f321b78d25e`
  - path `rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json`
  - file SHA-256 `5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5`
  - canonical SHA-256 `28630f26b491dcbce411667e3ad285ea42b40abf2d0176056a8a15d1ecad768d`
- Accepted C11 receipt: `ba41253681212be14a0cde009afb99d77e14935e`
- Earlier full construction grant: `303a57851785557fff8229e29a5554717168cbd1`
- Accepted grant SHA-256: `d8f13c67af276175266168e9af1a91e28fd543fcecadc1e79112a9854b4a8139`
- Verified reader/grant route: `dbeada9a272ff94a9bff68cf4352b6f1e5a01594`
- Source SHA-256: `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`
- Source shape: 7,337 rows × 181 columns; q217 ordinal 27.

## Exact prior residual recovered

`evidence/existing_construction_residual.json` preserves the prior construction
return at `2b9f0e768:campaign_src04_completion/bindings/RETURN.json`:

- field `q217`
- status `UNRESOLVED_EXACT_VALUE_LABELS_MISSING`
- `campaign_a_unbound_cells = 38`
- native field `response_slots[q217].values`
- reason: codebook/physical labels only declare 1,2,3,4,5,6,10,97,98,99.

The accepted receipt/accounting is pinned in
`evidence/accepted_receipt.json`: q217 held at **38** cells, 177 selected
responses, 3 coordinates, 1,298,649 response positions.

## One bounded aggregate check

No active original-source writer was present. One local aggregate check was run
through the exact existing grant route with `ExistingGrantResolver` and
`decode_with_source_read_permission`, using the exact grant/config pins above.

Command:

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/ANVIL_SRC04_Q217_MAPPING_20261118/q217_gate_check.py
```

The program emits only exact pins, q217 codes/counts and physical states. It
does not emit respondent records, IDs, row values, combinations, or samples.

Result — `evidence/q217_aggregate.json`:

| source code | count | classification |
|---:|---:|---|
| 1 | 4,719 | television |
| 2 | 440 | radio |
| 3 | 860 | local newspaper |
| 4 | 67 | weekly magazines and papers |
| 5 | 345 | internet |
| 6 | 37 | sms messages |
| 10 | 18 | others |
| **7** | **38** | **unlabeled observed numeric code — unresolved** |
| 97 | 72 | not clear |
| 98 | 335 | can't choose/don't know |
| 99 | 219 | decline to answer |
| None / no stored value | 187 | system missing |
| **total** | **7,337** | |

The 38-cell residual is therefore exactly code `7.0`, not a missing/refusal
state. It is an observed storage code with no source label. Without a source
resolution, it remains a possible source-specific code or import/representation
artifact; neither is asserted.

## Source-exact evidence

- Codebook: `evidence/source_codebook_q217.json`
  - `data/FINAL CODEBOOKS/FINAL FINAL CODEBOOKS/Arab Barometer Wave 1 codebook.csv`
  - SHA-256 `8ad1af17b782d1ff3beb84c2d2331977195ac3bb48dbcc94a94a08ca725b288f`
  - exact `var_name=q217` row; 10 declared labels; no code 7.
- Physical metadata: `evidence/physical_metadata_q217.json`
  - q217 `F8.0`, double, value-label set `labels25`
  - labels exactly 1,2,3,4,5,6,10,97,98,99
  - `missing_ranges = null`, `missing_user_values = null`
  - metadata witness content hash `6b98d33a8c7598934fcad38cecb3b23e0db7a3031990b302c3df113d295351fb`.
- Current config q217: `evidence/config_q217.json`
  - physical slot and exact current response-state rules.
- Questionnaire: `evidence/source_questionnaire_pin.json`
  - `data/Arabbarometer/ABI_Questionnaire_ENG.pdf`
  - SHA-256 `0814f77bcfdad3c78d5e46f49012437f25ddcbfe8bea3e565d7a26874bab4118`
  - q217 text extraction: **not obtained** (scanned/no text layer); no label was
    inferred from the questionnaire.

The exact source publisher identity is not established beyond the source
family/wave and artifact pins; no publisher label is invented.

## Mapping candidate — proposed, not applied

`q217_mapping_patch.json` proposes two minimal operations:

1. Add code `7.0` as `INVALID_UNRESOLVED` with no canonical value and no label.
2. Correct source-labeled code `99.0` (“decline to answer”) from the current
   `SUBSTANTIVE_RESPONSE` mapping to `REFUSAL`.

`evidence/q217_candidate_validation.json` records:

- candidate loaded by the existing current `load_source_config` validator;
- candidate canonical SHA-256 `b5e3ac84d407901daf79ee7fdd4d2e6f63edf4f440d5bdca33aba71edf224c82`;
- code 7 remains unlabeled and non-substantive;
- code 7 labeled/substantive candidate is refused by the mapping policy;
- code 97/98 remain `DK`; code 99 becomes `REFUSAL`; `None` remains
  `SYSTEM_MISSING`;
- no canonical/scientific/source right is promoted;
- accepted config and product files are untouched.

This is a **possible separately reviewed successor**, not an accepted config.

## Reusable residual check

`residual_check.py` is a pure function/CLI for aggregate codes + declared labels.
It separates known labels, special labeled states, unlabeled observed codes, and
system missing states without source access, wave launch, inventory, frequency,
or cross-wave inference.

Run:

```bash
python3 -B WORKER_RETURNS/ANVIL_SRC04_Q217_MAPPING_20261118/residual_check.py \
  --aggregate WORKER_RETURNS/ANVIL_SRC04_Q217_MAPPING_20261118/evidence/q217_aggregate.json \
  --out WORKER_RETURNS/ANVIL_SRC04_Q217_MAPPING_20261118/evidence/q217_residual_check.json
```

## Boundaries

- Source access was local, within the existing SRC04 full grant, through the
  accepted gate; no source path or bytes were published.
- No raw respondent records, individual values, IDs, row combinations or
  arbitrary samples were emitted to the model, Git, or stdout.
- No new source rights, canonical promotion, scientific frontier, product or
  config-custody edits.
- No large build and no second inventory.
- Existing construction witness pins are unchanged.

## Evidence

- `evidence/existing_construction_residual.json`
- `evidence/accepted_receipt.json`
- `evidence/source_codebook_q217.json`
- `evidence/physical_metadata_q217.json`
- `evidence/config_q217.json`
- `evidence/source_questionnaire_pin.json`
- `evidence/q217_aggregate.json`
- `evidence/q217_residual_check.json`
- `evidence/q217_candidate_validation.json`
- `q217_mapping_patch.json` (candidate at return root)
- `evidence/gate_route.json`
- `evidence/no_active_original_writer.txt`
- `evidence/tests.txt`

**Stop with exact unresolved held code: q217 = 7.0 (38 cells), no source label.**
