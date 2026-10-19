# F43 replay

Run from the F43 branch root with Python 3.11, pytest and pandas already available.
No source files, respondent rows, network call or package installation is needed.
The explicit archives reconstruct only exact sourcefree/retained owner code.

```bash
python3 -B WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1/bootstrap_f43.py
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1/tests
python3 -B WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1/f43_product.py
python3 -B CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1/tests/test_bounded_world.py.proof.json --root . --receipt /tmp/f43-proof.json
python3 -B WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1/bootstrap_f43.py
```

The bootstrap verifies exact restoration; it does not overwrite changed files.
Run mutation proofs sequentially with captures/tests: they intentionally alter
the isolated dependency copies and restore them. `deps/` is ignored and cold
reconstruction is explicit. Do not point this worker at J42/U43/B43 files.

`world_products.json` contains original unchanged E04 TEST_ONLY output, retained
context reads, actual F6M/F6P products and new bounded views, V553/EE1 probes,
the full prospective all35 accounting and the finite source/method decisions.
`A42_RECEIPT_BANK.json` pins the exact committed product evidence. To validate
the bank against A42 without changing its estate or rerunning its assembly:

```bash
python3 -B -c "import sys; sys.path.insert(0,'WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1'); import a42_intake,json; print(json.dumps(a42_intake.validate_bank(json.load(open('WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1/A42_RECEIPT_BANK.json'))),indent=2))"
```

The A42 validator needs its exact A41 scope and R42 startup Git objects, plus
the receipt's implementation commit. A shared object-store worktree preserves
them; a new clone must explicitly fetch the pinned owning branches/objects.
Hashes identify evidence; they never grant permission or independent acceptance.

For the full cold scientific comparison, capture the same committed package in a separate worktree and run `check_cold_replay.py /absolute/path/to/cold/WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1`. It validates each inherited native path-derived hash before removing exactly the 14 documented hash fields for the scientific comparison.

The subsequent U43 metadata reconciliation is independently replayable without
source access or native runtime execution:

```bash
python3 -B WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1/reconcile_u43.py
```

It verifies the exact published metadata archive and matches all35 identities,
175 issuer-decision IDs and 595 unchanged prospective pair candidates. Historical
country overlap remains candidate metadata; zero new original manifests or
scientific permissions follow. Existing scientific product bytes are unchanged.
