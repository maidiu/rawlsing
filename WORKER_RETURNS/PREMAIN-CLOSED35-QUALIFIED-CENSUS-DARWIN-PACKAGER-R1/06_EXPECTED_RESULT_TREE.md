# Expected Result Tree

The authoritative run uses a deterministic work root outside the repository by default:

```text
$HOME/Library/Caches/Rawlsing/closed35-qualified-census-r1/
├── package/
│   ├── 02_SOURCE_ESTATE_TO_PATH_MANIFEST.py
│   └── 03_POSTRUN_RECEIPT_COMMIT.sh
├── staged_sources/
│   ├── Afro Barometer Round 1.sav
│   ├── ...
│   ├── LiTS_I.dta
│   ├── ...
│   └── WVS Wave 7.sav
├── CLOSED35_SOURCE_PATH_MANIFEST.json
├── PACKAGER_RUN_BINDING.json
└── census_output/
    ├── source_receipts/
    │   ├── SOURCE_01_REPRESENTATION_RECEIPT.json
    │   ├── ...
    │   └── SOURCE_35_REPRESENTATION_RECEIPT.json
    ├── CLOSED35_REPRESENTATION_OBSERVATIONS.json
    ├── CLOSED35_TYPED_JOIN_MATRIX.csv
    ├── CLOSED35_EDGE_PRESERVATION_RECEIPT.json
    ├── CLOSED35_HISTORICAL_DEPENDENCY_PROVENANCE.json
    ├── CLOSED35_RUNTIME_RECEIPT.json
    └── CLOSED35_CENSUS_SUMMARY.json
```

The `staged_sources/` directory contains exactly 35 byte-verified canonical source files and is never placed in Git. Filename is transport only; each staged file is reverified by byte size and SHA-256.

The census is considered measurement-complete when exactly 35 immutable source receipts exist and all six aggregate outputs validate. Individual source receipts may lawfully have `status: BLOCKED`; 35 PASS source classifications are not required.

## Result branch tree

After the post-run helper succeeds, the dedicated local result branch contains only:

```text
WORKER_RETURNS/PREMAIN-CLOSED35-QUALIFIED-REPRESENTATION-CENSUS-RESULTS-R1/
├── source_receipts/
│   ├── SOURCE_01_REPRESENTATION_RECEIPT.json
│   ├── ...
│   └── SOURCE_35_REPRESENTATION_RECEIPT.json
├── CLOSED35_REPRESENTATION_OBSERVATIONS.json
├── CLOSED35_TYPED_JOIN_MATRIX.csv
├── CLOSED35_EDGE_PRESERVATION_RECEIPT.json
├── CLOSED35_HISTORICAL_DEPENDENCY_PROVENANCE.json
├── CLOSED35_RUNTIME_RECEIPT.json
└── CLOSED35_CENSUS_SUMMARY.json
```

That is exactly 41 committed files: 35 per-source receipts + six aggregates.

The commit helper rejects any raw survey source/archive, candidate output, measured-P2X output, or path outside this result directory. It never pushes automatically.
