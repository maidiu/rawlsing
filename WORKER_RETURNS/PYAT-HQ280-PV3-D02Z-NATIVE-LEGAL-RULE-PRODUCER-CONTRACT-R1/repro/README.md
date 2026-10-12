# D02Z source-free candidate contract test runner

Nonissuing, isolated return-only Python. Does not import/patch accepted PRE-V3 modules.

From this folder run:

```bash
python -m unittest -v test_d02z_documentary_rule_contract.py
```

Or from repository root run:

```bash
cd WORKER_RETURNS/PYAT-HQ280-PV3-D02Z-NATIVE-LEGAL-RULE-PRODUCER-CONTRACT-R1/repro
python -m unittest -v test_d02z_documentary_rule_contract.py
```

Tests are **source-free local validation**, never an original Ghana PDF read. A green test means only that a caller-stipulated known §7-shaped preimage cannot obtain producer/issuer/current permissions from this contract. Exact official byte custody, independent issuer signatures, legal commencement/amendments, M4 publication, N9 and V3 remain held. Execution grade is tracked in manifest; do not infer source authenticity from tests.
