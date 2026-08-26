# C3 Register A/B Exact-Byte Supplemental Recovery

Status: `C3_REGISTER_AB_PORTABILITY_SUBSTRATE_RECOVERED_EXACT`

Scope is limited to recovery and mechanical validation of the two commanded historical `question_structure_register.csv` payloads. No builder was run. No semantic comparison, succession judgment, currentness inference, or C3 adjudication was performed.

## Recovered objects

| Object | SHA-256 | Bytes | Data rows | Columns | Installed path |
|---|---|---:|---:|---:|---|
| Register A | `f47c8adb65546b1c0a06dcd31dc0b827b59f8975a3806646f41a0742966c3d84` | 23,612,534 | 18,792 | 62 | `03_C3_REGISTER_LINEAGE/REGISTER_A/question_structure_register.csv` |
| Register B | `15f7b5613b7cb106c2d2db233925891d5392917b66eee19c1a5eff8e0655585b` | 26,582,348 | 18,792 | 69 | `03_C3_REGISTER_LINEAGE/REGISTER_B/question_structure_register.csv` |

Register A was recovered as a loose file from the historical universality handoff path. Register B was recovered as a loose file from the August 24 authority archive path. The same generic filename was treated only as a locator; each installed payload was accepted solely after its own SHA-256 and byte count matched the commanded identity.

The excluded Register C SHA-256 `9139c1ab77bf47a872f63ccae7784f3631f03a3e02a936b4ac41e75580c45219` was encountered during loose-file search but was neither installed nor used as a substitute.

## Mechanical validation

- SHA-256: exact for both installed files.
- Byte count: exact for both installed files.
- CSV parse: successful for both installed files.
- Row convention: header excluded; both have exactly 18,792 data rows.
- Shape: Register A has 62 columns on header and every data row; Register B has 69 columns on header and every data row.

Exact source locations, receipt hashes, and installed-file hashes are recorded in `99_PROVENANCE/SOURCE_PROVENANCE.tsv`, `99_PROVENANCE/SHA256SUMS.txt`, and `PORTABILITY_C3_REGISTER_AB_SUPPLEMENTAL_VALIDATION.json`.

`C3_REGISTER_AB_PORTABILITY_SUBSTRATE_RECOVERED_EXACT`
