# Test receipts

**Environment:** macOS Darwin, Python 3.11.3, Git 2.43.0.
**Pattern:** `PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -m pytest -q -p no:cacheprovider ...`
**Sourcefree:** no raw survey/respondent data, no native extension, no production import.

## Current baseline

| Suite | Command / scope | Result |
|---|---|---|
| Current source relations | `rawlsing_next/tests/test_pre553_source_relations.py` | 24 passed, exit 0 |
| Decoder/custody | `test_universal_source_byte_custody.py`, `test_universal_source_projection.py`, `test_pre553_sr06_decoder_carrier.py` | 73 passed, 1 skipped, exit 0 |

Logs:
`test_receipts/source_relations.log`,
`test_receipts/decoder_custody.log`.

## Historical F7 sourcefree suites

| Cut | Suite | Result |
|---|---|---|
| `caf6644a6033fb27c981ff0deb8d6e1b7d3d824e` (HQ211 original) | `test_pre553_temporal_comparability.py` | 49 passed, exit 0 |
| `c86ae335eaf70e82b5764c46754b16ca7e1587ce` (HQ235 final paired) | `test_pre553_temporal_comparability.py` | 163 passed, exit 0 |
| `f90b29ce1b1f043e4f5a3972fef5b2f4dee74b3c` (HQ227 intermediate) | `test_pre553_temporal_comparability.py` | 134 passed, 7 failed, exit 1 |

The HQ227 failures are all cross-universe positive expectations; the later
HQ235 source-relations/test pair supersedes them. They are retained to avoid
claiming that the method blob alone is self-sufficient at HQ227.

Logs:
`test_receipts/historical_hq211_49.log`,
`test_receipts/historical_hq235_163.log`,
`test_receipts/historical_hq227_141.log`.

Historical worktrees were created under
`/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/` with sparse
`rawlsing_next` checkout. No `data/` directory was present in those worktrees.

## Candidate

| Suite | Result |
|---|---|
| `candidate/test_temporal_method_candidate.py` | 24 passed, exit 0 |
| `candidate/mutation_check.py` | PASS, 2/2 mutations detected, 0 failures |

Mutation receipt:
`test_receipts/mutation_receipt.json`.

Named mutation checks:

```text
disable_attestation_binding_check
  test_route_attestation_bound_to_wrong_refs_is_refused
  mutated_exit=1, restored_exit=0

accept_nonpositive_authority
  test_denied_temporal_evidence_authority_is_insufficient_authority
  mutated_exit=1, restored_exit=0
```

## Probe receipts

| Probe | Result |
|---|---|
| `test_receipts/current_surface_probe.py` | F7 path absent; 18 authority kinds; `TEMPORAL_EVIDENCE` present; `TEMPORAL_COMPARABILITY` absent; nested owner absent; authenticated entrypoint absent; source-relations production importers empty |
| `test_receipts/historical_probe.py` | F7 method blob 79,679 bytes / 28 functions / 6 classes; test blob 129 test functions; historical source-relations blob has nested owner and authenticated entrypoint; method has no timestamp/as-of selector and no native import |

JSON receipts:
`test_receipts/current_surface_probe.json`,
`test_receipts/historical_probe.json`.

## NOT_RUN

- Native P07 Stage A/B compilation, import or execution.
- Raw EVS or other survey/respondent source reads.
- EVS pair measurement or sign calculation.
- R40/R41/R52/F43 implementation/consumer runs (no current return/code in this baseline).
- S7FIX 47 MB membership validator (cited from existing S7FIX/I3 returns; not rerun).
- Any PRE-MAIN integration, merge or production adoption.
