# Reproduce D2R in an isolated source-free Python host

The tests here execute real `D2P` and `N9C` pinned Python code; they are **not** an issued external field or real N9. To make a clean worktree:

1. Fetch exact historical blobs from private `maidiu/rawlsing@af128002ddc334ab5f3494a3b9488fd5b53e90d8` into a scratch directory:
   - `WORKER_RETURNS/PYAT-USERDIRECT-20261014-R2-D2P-OBJECTIVE-SOURCEFREE-PRODUCER-R1/repro/d2p/external_fields.py` ⇒ scratch `d2p/external_fields.py`, SHA-1 `583f60559bb04232a1165e85b708079247ceb5f6`.
   - `.../repro/d2p/n9c_reader.py` ⇒ scratch `d2p/n9c_reader.py`, SHA-1 `03eb46efccadd6880cb34b2e2ac609ffc9b16c59`.
   - `.../repro/n9c_fields.json` ⇒ scratch `n9c_fields.json`, SHA-1 `1a1bec6e2fc5a89e2ea1b589832801a43933a632`.
2. Copy this return's `repro/exact_ref_lineage.py`, `repro/test_d2r_sourcefree_hostiles.py`, `repro/test_d2r_required_integrity_red.py` into `scratch/repro/`.
3. From scratch root run:
```sh
PYTHONPATH="$PWD" python repro/exact_ref_lineage.py
PYTHONPATH="$PWD" python -m pytest -q repro/test_d2r_sourcefree_hostiles.py --junitxml=repro/positive_junit.xml
PYTHONPATH="$PWD" python -m pytest -q repro/test_d2r_required_integrity_red.py --junitxml=repro/negative_junit.xml
```
Expected actual result: reference-lineage script prints a RED record and exits 0; 35 PASS exit 0; 7 mandatory failures exit 1. The test files are **exactly** those executed in the isolated Python 3.13.5/pytest 9.0.2 host; uploaded blob identities equal the local Git object hash:
- lineage script `ab9c22a26cc111e0d55aa3893c09f6e2cd5c52b8`;
- 35-check suite `65ffd5f37e10b1f7563568027d6411873898e4ca`;
- seven strict-RED suite `323beb9216dc81ad4f8efc0cdca772c995d497a8`.

The original binary PDF bytes are not in this execution. The reconstructed D2P/N9C code/fixture is the *test only* pinned source. Historical author `116=29+47+40` tests are not recounted as independently rerun here. Independent XML/stdout was generated locally and its exact SHA/Git object identities are in `../03_INDEPENDENT_HOSTILE_EXECUTION.md`. Raw code and reproducible assertions are committed; no source PDF, original respondent rows, or user machine worktree is included.

**No live issuer/EE13/OC05 source grant or V3 action.**
