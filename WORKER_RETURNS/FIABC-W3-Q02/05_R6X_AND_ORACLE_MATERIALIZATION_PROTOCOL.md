# FIABC-W3-Q02 — R6X reconciliation and parity-oracle materialization protocol

This is a deterministic LOCAL protocol. Q02 did not execute it.

## 0. Operator inputs

The operator supplies only physical paths; no architecture choices are left open.

```bash
export REPO=/absolute/path/to/rawlsing
export OLD_WORK_ROOT=/absolute/path/to/exact/stopped/p2x/work-root
export QUAL_ROOT=/absolute/path/to/new/wave3/qualification-root
export LITS_PATH=/absolute/path/to/exact/lits-i/source
export WVS_PATH=/absolute/path/to/exact/wvs7/source
cd "$REPO"
```

`OLD_WORK_ROOT` is the exact stopped work root whose ledger SHA-256 is frozen below. `QUAL_ROOT` is a fresh root for Wave-3 oracle/premeasurement receipts. Do not reuse candidate scratch from the old court as the fresh qualification root.

## 1. Runtime/source identity gate

```bash
python - <<'PY'
import importlib.metadata, platform, sys
assert platform.python_implementation() == 'CPython'
assert '.'.join(map(str, sys.version_info[:3])) == '3.11.3'
assert platform.system() == 'Darwin'
assert platform.machine() == 'x86_64'
assert importlib.metadata.version('pyreadstat') == '1.3.6'
assert importlib.metadata.version('pyarrow') == '25.0.1'
print('PASS__EXACT_DARWIN_RUNTIME')
PY

test "$(shasum -a 256 "$LITS_PATH" | awk '{print $1}')" = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
test "$(shasum -a 256 "$WVS_PATH" | awk '{print $1}')" = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
```

Verify immutable candidate owners and the P2R1 seam with the exact commands in `03_INTEGRATED_TREE_TEST_PLAN.md` before continuing.

## 2. Seal a read-only copy of the pre-reconciliation stopped state

Before mutation, retain an operator-controlled snapshot or filesystem snapshot of `OLD_WORK_ROOT`. The repository-tracked historical receipts are already immutable; this copy protects the local mutable stage ledger and candidate-local state.

The exact pre-reconciliation ledger must be:

```bash
test "$(shasum -a 256 "$OLD_WORK_ROOT/ee_p2x_stage_ledger.json" | awk '{print $1}')" = \
  "7de7c91d539dd267e31098fd47285b3f4a7873e1c9ec7b542c45cac3908b8671"
```

Any mismatch is a hard stop. Do not edit the ledger by hand to make the hash match.

## 3. R6X audit-only dry run

```bash
python WORKER_RETURNS/EE-P2R6X/03_RECONCILE_LOCAL_P2X_INFRASTRUCTURE_STOPS.py \
  --work-root "$OLD_WORK_ROOT" \
  --repo-root "$REPO" \
  --audit-only \
  > "$QUAL_ROOT/r6x_audit_before.json"
```

Required status: `AUDIT_ONLY__READY`.

The dry run must validate exactly the four infrastructure-misclassified historical blockers:

- `LITS_I/A/S02_C11_REACHABILITY`;
- `LITS_I/B/S03_PARITY_ORACLE_GATE`;
- `WVS7/A/S01_CANDIDATE_PREPARATION_BUILD`;
- `WVS7/B/S01_CANDIDATE_PREPARATION_BUILD`;

and the orphan running `COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION` entry. It must not open a source carrier or delete a candidate root.

## 4. R6X single governed mutation

Only after the dry run passes:

```bash
python WORKER_RETURNS/EE-P2R6X/03_RECONCILE_LOCAL_P2X_INFRASTRUCTURE_STOPS.py \
  --work-root "$OLD_WORK_ROOT" \
  --repo-root "$REPO" \
  > "$QUAL_ROOT/r6x_reconciled.json"
```

Required status: `RECONCILED`.

Required next stage in the historical ledger: `LITS_I/A/S02_C11_REACHABILITY`.

The reconciler may clear only exact failed-attempt backend state and scratch for LiTS-A, LiTS-B, WVS-A, WVS-B, plus the orphan court scratch/state described by R6X. It must preserve source identities, continuation-map identity, unrelated terminal stages, preserved LiTS-A/LiTS-B historical milestones, durable transformed carriers, and all repository-tracked evidence.

## 5. R6X post-mutation audit

```bash
python WORKER_RETURNS/EE-P2R6X/03_RECONCILE_LOCAL_P2X_INFRASTRUCTURE_STOPS.py \
  --work-root "$OLD_WORK_ROOT" \
  --repo-root "$REPO" \
  --audit-only \
  > "$QUAL_ROOT/r6x_audit_after.json"
```

Required status: `AUDIT_ONLY__ALREADY_RECONCILED`.

A second mutating invocation must be refused. Preserve `OLD_WORK_ROOT/ee_p2r6x_reconciliation_receipt.json` and both Q02 audit outputs.

## 6. Historical-C warning after R6X

R6X correctly preserves the historical LiTS-C and WVS-C stops because they were lawful under the old continuation reducer. **Do not interpret that preservation as current Wave-3 capability law.** I03 implements the now-adjudicated current successor: LiTS-C has exact-source fallback outside CACC scope, and WVS-C has a lawful zero-accelerator source-backed realization.

Therefore:

- do not resume measured six-cell P2X directly from the old reducer after R6X;
- do not let the old WVS-C preserved failure satisfy current I07 source×candidate capability;
- do not delete or rewrite the old C receipts;
- require the Wave-3 integrated execution binding/preflight to classify those receipts as historical and to admit current C execution separately.

If the integrated I03/I06/I07 stack does not provide a current six-cell execution binding that supersedes the old current-capability assumptions without mutating historical evidence, stop. Measured P2X is unlawful.

## 7. Candidate-neutral oracle freeze boundary

Create a fresh qualification root and forbid candidate-owned output roots before oracle freeze:

```bash
mkdir -p "$QUAL_ROOT/oracle/LITS_I" "$QUAL_ROOT/oracle/WVS7"
```

The I05 final worker return must provide deterministic local materialization commands. Run those exact commands now, not after any Candidate A/B/C process starts. If I05 omits those commands, stop.

### 7A. LiTS-I oracle materialization contract

Inputs that must be verified before the I05 LiTS materializer runs:

- source SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- LiTS projection identity `84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872`;
- immutable ASTRA-D04-R2 truth-surface commit `e631de162c582423639b7067a4f36b29f8aa4d89`;
- truth-surface file `WORKER_RETURNS/ASTRA-D04-R2/01_TYPED_LEARNED_EMPIRICAL_PRODUCT.json`;
- 50-candidate / 77-role closure;
- frontier seal `ca47c52f925b126878cd9e0be433bd6a28bec5a8623784bfbf5eaf7523b21bea`;
- reference learned-product identity `47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d`;
- reference semantic replay `301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5`;
- current candidate-neutral exact-ref and transitive authority closure.

The ASTRA product is oracle/reference evidence only. The later candidate execution must still produce a fresh I05 product; `historic_product_substitution` must remain false.

Required LiTS freeze receipt properties:

- complete fixed frontier;
- exact constituent I03 fact identities and typed states;
- exact refs, semantic identity, replay determinants, and negative-state distinctions;
- `candidate_outputs_seen = 0` (or exact equivalent required by I05 contract);
- no candidate-owned root consulted;
- immutable/canonical oracle content hash recorded before Candidate A starts.

### 7B. WVS7 oracle materialization contract

Inputs that must be verified before the I05 WVS materializer runs:

- source SHA-256 `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- Lock2 `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`;
- Lock2 replay `b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490`;
- discovery authority `24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab`;
- exact 46 ordered candidates from `WORKER_RETURNS/EE-P2F2/05_WVS7_DISCOVERY_AUTHORITY_AND_FRONTIER_BINDING.json` at accepted P2F2 commit `22667bd395e7293f99b285daddad36fe3a4377ef`;
- candidate grammar identity and exact 11-predicate/3-query catalogs;
- family shape `10 unary + 1 pair-cotravel + 10 directed branch-conditioned + 25 joint-support`;
- exact 13-country risk set;
- RAW/unweighted basis and no default estimand/weight;
- accepted WVS projection/coordinate authority identities.

The WVS oracle must be computed from exact source bytes plus candidate-neutral frozen authority. It may not use Candidate A, B, or C output as expected truth.

Required WVS freeze receipt properties are the same independence properties as LiTS and must explicitly record zero candidate output visibility.

## 8. Oracle independence hostile check before preflight

Before I07 preflight is allowed to PASS, verify that the two I05 freeze receipts prove:

- both were created before any candidate-owned output or scratch exists in the fresh qualification lifecycle;
- no candidate implementation module was invoked to derive expected truth;
- A agreeing with itself cannot satisfy the oracle;
- A/B pairwise agreement cannot substitute for oracle agreement;
- partial frontier closure cannot pass;
- typed negative-state collapse cannot pass;
- stale authority/replay roots cannot pass.

If any property is missing, stop before six-cell premeasurement qualification.
