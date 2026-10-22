# R02 r2 — qualification commands, counts and hashes

All commands were run from
`/Users/matthewsmith/Desktop/Rawlsing/R56-R02-occurrence-projection-wt` with
`PYTHONDONTWRITEBYTECODE=1`. The repository proof checker was read from the
tracked reviewer worktree because this sparse author worktree excludes
`CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py`; the checker blob is
`e3125e121babb6f522688e050b1840f514e04796b47fdab81c5d40b140f858ed`.

## Commands and exit codes

| # | Command (abridged) | Exit | Result |
|---|---|---|---|
| 1 | Author 15 node IDs | 0 | 15 passed |
| 2 | Reviewer 9 node IDs (7 positives + 2 defects) | 0 | 9 passed |
| 3 | Full focused file | 0 | 26 passed |
| 4 | Retained facade + empirical-query | 0 | 42 passed |
| 5 | `proof_integrity_gate_r1.py lint rawlsing_next/tests/test_universal_source_projection.py` | 0 | `AST_LINT_PASS` |
| 6 | `proof_integrity_gate_r1.py witness rawlsing_next/tests/test_universal_source_projection.py.proof.json --root .` | 0 | 4 claims, baseline PASS, target assertion RED, adapter restored |
| 7 | `python3 evidence/build_r2_defect_resolution_receipt.py` | 0 | D1/D2 typed refusals; near positives SUPPORTED |

## Production/import hashes

| Path | Before (`236fd4d1`) | After repair |
|---|---|---|
| `rawlsing_next/pre553_source_native_preimage_adapter.py` | `2cf5e98bc29081678c364d3ff591c71f11ce7ebf3564419af8a26f5f04113b64` | `c9ea22ada390babf7b3a977352b784bcfeb498e738dcb0024fc7f4d793b90b95` |
| `rawlsing_next/tests/test_universal_source_projection.py` | `9b3cf0e23d9c675e3666bc52756cd7ade5770cef093773dbebf0e9e249d189a7` | `3673908c02b6066a10b985bd26106686dfbb0eba463551a3e6d3e21db5327b63` |
| `rawlsing_next/tests/test_universal_source_projection.py.proof.json` | `c8ee73c30f74d12fd44bb88710e4903bc3c04a1c89b76481378a712ce6e4c11c` | `39ba9ef15d0628d4a56877022d46db18a7403a9ab4a07a734c2743c2a0af72dd` |

The adapter diff is 80 added / 4 removed lines. No facade, C11, I03, decoder,
policy or foreign return was edited.

## Defect resolution receipt (exact run)

From `evidence/r2_defect_resolution_receipt.json`:

- D1 source SHA `21b28c1c...`; `DUPLICATE_RESPONDENT_KEY_MAPPING`, detail `1`.
- D2 source SHA `21b28c1c...`; `DUPLICATE_NORMALIZED_SOURCE_KEY`, detail `0`.
- Int source keys near positive: `SUPPORTED`, denominator 3, 6 events.
- Float source keys, reversed rows: `SUPPORTED`, denominator 3, 6 events.
- Numeric destination `{0:1,1:2,2:3}`: `SUPPORTED`, denominator 3, 6 events.
- Exact source/release/fact hashes are in the JSON receipt.

## Proof claims

1. `R56-R02-OCCURRENCE-TUPLES` — canonical-value fault; baseline PASS, target
   assertion RED.
2. `R02V-INDEPENDENT-SOURCE-DOMAIN` — respondent-assignment fault; baseline
   PASS, target assertion RED.
3. `R02-NORMALIZED-DESTINATION-REFUSAL` — disable the normalized destination
   duplicate check; baseline PASS, target `pytest.raises` assertion fails.
4. `R02-NORMALIZED-SOURCE-KEY-REFUSAL` — disable the normalized source-key
   duplicate check; baseline PASS, target `pytest.raises` assertion fails.

After the witness the adapter SHA-256 was verified equal to the repaired hash
`c9ea22ad...`, confirming restoration.

## Binding-envelope limitation

The transformed adapter `physical_stream` remains compatible with the tested
facade/C11/I03 route only. It is not a raw `PhysicalCell` replacement for
strict receiver APIs; no facade/strict receiver was changed and no general raw
compatibility is claimed.
