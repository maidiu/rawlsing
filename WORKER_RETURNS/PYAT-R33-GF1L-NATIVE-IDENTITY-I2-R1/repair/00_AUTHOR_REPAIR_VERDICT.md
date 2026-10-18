# GF1L author repair — native mapping key guard

**Repair implemented and author-validated. All four supplemental RED witnesses are closed. This is a new candidate, not a new independent acceptance.**

User instruction: “okay, repair it”, following GF1L's independent RED review. Work is on `agent/userdirect-pyat-20261017-gf1l-key-storage-repair-r1`, based on frozen review commit `d605d0b94c303d9ebfd4f57a0af880d958ad01e9`. Every tracked addition is confined to this `repair/` directory. The independent review, old candidate, frozen oracles, original failure identities and prior evidence remain unchanged.

Candidate: `gf1_pair_support_consumer.py`, version `GF1L_NATIVE_KEY_STORAGE_GUARD@1`. Git blob **`3761730d975f3281e69f8038b337da62824e0baf`**, SHA256 **`00a5cc6adc8b6a4074e9ae63d0a57384a8c227e9c88a719683cb0304691a4f9b`**. Derived from exact GF1K `1399a475e54ea33355cf641979829424625c511d`, blob `bbbda32facce0a3324498b88f4ba4bf0f79f18d2`.

## Change and behavior

Strict type/value membership now also requires that each declared domain survive both Python mapping storage and the existing result serializer without collision or exception. This check runs before profile aggregation or classification.

- `(0, False)` and `(0, 0.0)` collide as Python keys and are refused before support can be reduced from 2 to 1.
- Mixed string/integer keys are refused when the inherited canonical serializer cannot sort them. No `TypeError` escapes.
- Individually serialized key identities must also remain distinct; the pair must serialize together successfully.
- All unsupported cases return `CONSUMER_RELATION_INTEGRITY_REJECTED`, `separation_class=None`, `downstream_value_produced=False`. No support vector, total, separation signature or result hash is returned.
- Representable domains keep their native objects and values. There is no homogeneous-type whitelist: disjoint mixed numeric/Boolean keys such as `(0, True)` still compute correctly. New controls cover strings, integers, floats, booleans and noncolliding mixed numeric domains in both roles.

This preserves the existing result shape and inherited canonical hashing method. It does not cast categories, invent a domain mapping, change owners, or add a new result family. Unsupported combinations require a separately qualified representation or source-owner mapping before they can be computed; this patch does not silently reinterpret them.

## Actual full native execution

| Court | Result |
|---|---:|
| Exact GF1K before repair, unchanged supplemental10 | 6 pass / **4 fail** |
| Original44 | **44 pass** |
| GF1G26 | **26 pass** |
| GF1H26 | **26 pass** |
| Original GF1J native two hostiles + positive | **3 pass** |
| GF1L corrected frozen14 | **14 pass** |
| GF1K author12 | **12 pass** |
| Unchanged supplemental10 after repair | **10 pass** |
| New storage guard26 | **26 pass** |
| Historical GF1F100 | **96 pass / 4 fail**, same failed nodes |
| Historical GF1I19 | **17 pass / 2 fail**, same failed nodes |

**161 required/focused checks pass**. Historical courts retain their six pre-existing failures; they are neither skipped nor regraded. All four supplemental RED node identities are preserved. No skips or xfails. Raw logs, JUnit, exact commands/exits and before/after identities are retained under `evidence/`, `run_results.json` and `court_summary.json`.

All **74 native files (45 Python files)** match their original `commit:path` bytes, Git blobs, SHA256 and lengths. Nine inherited test files match their pinned originals byte for byte. Two fresh native cold processes **45279 / 45319** have identical non-PID receipts and **38 actual import paths/hashes**, checked physically while the repair is seated. Their legitimate baseline result, including its result hash, equals the unrepaired GF1K baseline exactly.

The replay seats the repair only in ignored fixture-stage consumers and restores their prior bytes in `finally`. Original producer, fixture machinery and accepted owners are untouched. Both the original source-native string positives and full constructor behavior are exercised on the real native tree. The supplemental mixed-domain and new typed-domain cases are TEST_ONLY self-rehashed constructor variants, not authenticated source-issued outputs.

## Reproduction and scope

Run `python3 WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1/repair/reproduce.py` from this checkout. Missing stage sources are reconstructed from exact Git pins without running or overwriting old review report writers. All raw outputs are written only under `repair/`; stage products remain ignored. Before testing, the runner reattests original source and inherited tests. After testing, it verifies exact historical node sets, cold imports and unchanged baseline hashes.

The author repair preserves GF1H arithmetic/risk/typed-state guards, original GF1J alias rejection, reverse grants, F2 noncopy and sourcefree ceilings. No original SAV/DTA, source35, canonical owner, Field Forge, OC05/N11/N12, actor, Sorok or V3 change is made. `production_owner_commit=False` remains mandatory. Structural self-hash does not authenticate an original signatory.

Because this session now authored a repair, these runs are author validation. The independent RED verdict remains valid for the old GF1K SHA. The new candidate is ready for a separate independent re-review; no self-adoption or new authority grant is asserted.

## Current qualification update

The tables above preserve the repair evidence recorded at `dd12505c81b9757ca70bb49806aaac494b9a61df`. The user subsequently authorized reconciliation of the six historical assertions and correction of the staging defect. The current gate is **282 PASS / 0 FAIL / 0 ERROR / 0 SKIP**, with no failure allowance; the nested original44 also runs successfully. Use `repair/qualify.py` for current qualification and see `current_qualification/00_CURRENT_QUALIFICATION.md` plus its six-node crosswalk. Historical originals remain unchanged, while versioned current successors qualify the repaired candidate. The consumer code is unchanged.
