# R61-R01 R3 author repair return — conditioned joint semantics and canonical identity

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted. R03 remains
NOT_STARTED.

## Exact identity

- Branch: `agent/opencode-pyat-r61-r01-generic-grammar-r1`
- R3 startup: `f0c602eddaee14a58d6f0935a587a46fcf96c6db`
- R3 code commit: `89774b01990a7d18c10cf4f6e819895776a1a633`
- R2 independent review: `3ac1e498a08648950d31df0bf52750f9335d24fa`
- R3 repair commission: `3470da602618b5c04b1f28885b5ad1835169e2d5`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01`

## A1 — conditioned JOINT / CO_TRAVEL now binds the exact condition natively

The R2 defect was real: conditioned joint/co-travel records carried the
condition atom but executed the all-response baseline. R3 now composes a derived
exact predicate from the actual condition predicate objects using the current
I05 owner primitives (`_combine_predicates`, `_xor_exactly_one`), adds its exact
ref/object to the lowering, and uses it as the `baseline_atom_id` for the
`JOINT_DEPENDENCE` rule. The current I05 `_compile_frontier` therefore binds the
derived condition predicate into the `JOINT` and every `MARGINAL_*` query role.

Proof in `test_conditioned_joint_and_cotravel_bind_condition_roles_natively`:

- Eight eligible SAMPLE conditioned `JOINT`/`CO_TRAVEL` operations on ordered
  targets `(q_alpha,q_beta)` with one condition from `q_gamma`/`q_delta` values
  `0/1` all lower `SUPPORTED`.
- Condition values `0` and `1` produce different derived predicate refs and
  different expected candidate identities; no role uses the all-response
  baseline.
- Actual imported `execute_exact_bounded_discovery` executes the grammar and
  every expected candidate ID is found exactly once by
  `native_receipt_anti_join`.
- A multi-condition `JOINT` control composes two condition atoms into one
  derived predicate, uses it in all joint/marginal roles, executes through the
  real I05 consumer, and passes the exact anti-join.

R03 consequence: the derived predicate object must be supplied to the I05
predicate catalog along with source predicates. `LoweringRecord.derived_predicates`
exposes it; this is an exact owner/catalog requirement, not a new engine.

## A2 — forged operation IDs are refused

`lower_operation` now requires
`operation.op_id == "urn:r61:op:" + operation.canonical_hash` before any
capability lookup. A forged ID returns typed `OPERATION_ID_NOT_CANONICAL` and
cannot retain `SUPPORTED`. Covered by the forged-direction test (separate
canonical-ID forgery assertion).

## A3 — unsupported is not VALID_EMPTY

`allow_empty_frontier` is now true only when the scientific frontier itself is
empty and there are no unsupported operations. An unsupported-only nonempty
frontier keeps its exact unsupported IDs and declares
`allow_empty_frontier=False`. Covered by
`test_unsupported_only_frontier_is_not_declared_valid_empty`.

## A4 — recursion/baseline limitation stated exactly, not claimed as D13 PASS

R01 does not invent a recurrence relation. FORK rows now carry
`recursion_depth=0` (conditioner `branch_depth` remains separate), the policy
`baseline_policy_ref` is carried on every operation identity, and the frontier
records an explicit deferred boundary:

```text
kind = RECURSION_BASELINE_NOT_ENUMERATED
state = EXACT_CONTRACT_GAP
reason = R01_DECLARES_FORK_OVER_CONDITIONERS_ONLY_NO_INDEPENDENT_RECURRENCE_CHAIN
```

D is no longer used as a disguised conditioner-depth bound. This is an explicit
finite contract/issuer gap; D13 is **not** claimed PASS. A future competent
issuer must supply the recurrence relation/baseline semantics before an
independent recurrence chain can be enumerated.

## Preserved R2 improvements

Typed bool/int/string/null/absent identities; typed native cells and injective
codec refusal; source/dataset/wave/edition/digest and full measure/clock identity;
separate eligibility/execution/result axes; budget PENDING; structured holds;
policy/role/risk/unit/form/topology/scope/administration and direction
revalidation; catalog-first topology; exact candidate/query-role receipt
anti-join; condition mutation/refusal/restoration; deterministic cold
recomputation. No prior report or reviewer file was edited.

## Tests and commands

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_grammar.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r3/junit.xml -o addopts=''
```

- Exit `0`; `20 passed`, `0 failed/errors/skips`; `10.19s`.
- JUnit: `junit.xml`; log: `pytest.log`.
- R2 reviewer A-probe replay (cold path artifact excluded):
  `4 passed, 1 deselected`, exit `0`, `reviewer_r2_a_probes.log`.
  The excluded cold probe has a path-derived module import artifact from the
  copied probe location; the committed cold recomputation test passes.
- Python `3.11.3`, pytest `9.0.2`, pyreadstat `1.3.2`.
- Imported current owner blobs:
  - `rawlsing_next/pre553_empirical_objects.py` = `a61365b994e5c3c50de0f598fcf40e90abf757b6`
  - `rawlsing_next/pre553_discovery_exact.py` = `905f24d114419dbdd93879ad2bee5b59dd2f23af`
  - `rawlsing_next/tests/test_pre553_discovery_exact.py` = `b53039aeb95e012993c5233a7575c1dad5a14929`
  - `rawlsing_next/tests/test_pre553_empirical_query.py` = `cc7d93db1f87d9c311170c229dbe3506937b404a`

## Capacity

- Tiny fixture: 22 operations, 8 eligible, 1 partition, `0.0111s`.
- Main synthetic fixture: 1,852 operations, 536 eligible, 29 partitions,
  `0.8953s`, peak RSS about 36 MB.
- No original data, credentials, external home reads, provider/model/session/
  subagent change, or unrelated branch.

## Exact changed paths and blobs

| Path | Blob |
|---|---|
| `rawlsing_next/universal_grammar/types.py` | `e7b196efe5b1f86134c27a80bfdd8f472be76e5d` |
| `rawlsing_next/universal_grammar/enumerate.py` | `fd9203a0b272f98771c24070d01a9e5287c9b099` |
| `rawlsing_next/universal_grammar/native_map.py` | `ea09c02efd273c92970b697397b78558647eb214` |
| `rawlsing_next/tests/test_universal_grammar.py` | `785ba9e13deba10ac72e1389add35c5914b4e7f2` |

Report artifacts are SHA256-listed in `manifest.json`, which explicitly excludes
itself and claims no hash for any future file/commit.

## Boundary

R03, R04 custody, original U/E_pre, F6/F7/F8, N11/N12, production/CI and
J52/W52 remain NOT_REACHED. A fresh distinct reviewer must qualify this exact
pushed candidate; the author does not self-adopt.
