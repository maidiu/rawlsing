# R2 SC0F — two-contract owner repair — implementation return

**Terminal:** `PYAT_R2_SC0F_TWO_CONTRACT_OWNER_REPAIR_COMPLETE__STRICT_SCHEMA_CONFORMANT__5_I2_REDS_CLOSED__115_TESTS_PASS__SOURCEFREE__NOT_ADOPTION__NOT_V3__NOT_N9_CURRENT__REVIEWER_REQUIRED`

Independent bounded implementation engineer return. NOT reviewer, NOT HQ, NOT
issuer. No canonical adoption, no original survey rights, no N12, no V3.

## Identity and sealed startup

- **Repository:** `maidiu/rawlsing` (private).
- **Branch:** `agent/userdirect-pyat-20261014-r2-sc0f-two-contract-owner-repair-r1`.
- **EXACT SEALED STARTUP:** `4d7255e9183fb11d1fd36258ff05429f5cffed40` (direct remote verified before edits).
- **Parent canonical:** `0d551d36ff19dc9806e0ad490ff33a1e4c25e381`.
- **Commission:** `WORKER_COMMISSIONS/PYAT-USERDIRECT-20261014-R2-SC0F-TWO-CONTRACT-OWNER-REPAIR-R1/00_COMMISSION.md` (read in full).
- **Write terrain:** `WORKER_RETURNS/PYAT-USERDIRECT-20261014-R2-SC0F-TWO-CONTRACT-OWNER-REPAIR-R1/` ONLY.

## Frozen adverse evidence read in full

| Evidence | Commit | What was read |
|---|---|---|
| Pyat I2 independent RED | `ec0567c4ca4138c479f41a6f7314161bbd3e6c8a` | 00_INDEPENDENT_VERDICT.md, 01-03, repro/test_i2_sc0_hostiles.py |
| Sorok HQ299 RC0 | `86bd2a54687b40401f7c4247607bd1873c585619` | 00_RETURN.md, 01-06, 05_OWNER_ACTION_REGISTER.json |
| Original SC0 port | `b15dbbc4f07ae79e9ffb71e88e91e3b28b35da59` | port/*, oracles/*, repro/*, staging/ |
| Frozen Draft 2020-12 envelope | blob `610ac870fde6cfe63796592b3c6b1e1bf1e37150` | Full $defs for WorldReceipt (17 fields) + PossibilityReceipt (20 fields) |

## What was repaired

### RED-01: strict Draft 2020-12 schema (CLOSED)

The old port emitted 8-field world_receipt and nonconformant possibility_receipt.
The SC0F candidate emits **WorldReceipt (17 required fields)** and
**PossibilityReceipt (20 required fields)** that pass `Draft202012Validator`
with `additionalProperties: false`. All enum values match the frozen vocabulary:
status codes (15), recoverability (6), decisions (4), grades (4), object_family
(14), composition_mode (5), direction (4), world_binding_requirement (2).

### RED-02: forged role-reversal (CLOSED)

Old `request_role_reversal` checked caller-supplied name equality. SC0F uses
**actual issuer-registry dereference**: grants must be registered in
`ISSUER_REGISTRY`; presented grant must match registered warrant; scope must
match world source/release; target must be the authorized reverse target;
risk_set and denominator must match. Forged grant_id, foreign scope, and foreign
target are all refused with `HELD_AUTHORITY`.

### RED-03: WORLD_READ revocation bypass (CLOSED)

Old `adapter.run` never called `provider.revoked_use`. SC0F **actively checks**
`WORLD_READ` in `revoked_atoms` and `use_atoms` at the top of `run()` before any
serving. `DENIED_USE` is raised before any values-read or consumer effects.

### RED-04: retroactive publication knowledge (CLOSED)

Old `validate_world` checked axis presence/distinctness but not availability
ordering. SC0F enforces: in `KNOWLEDGE_AS_OF` mode, `published > as_of` without
an `earlier_knowledge_evidence_ref` raises `NO_CURRENT_OR_NOT_KNOWN_ASOF`. The
2010 publication is not knowledge available at as_of 2009.

### RED-05: PARTIAL served as positive (CLOSED)

Old `adapter.run` didn't check `selection_state`. SC0F refuses any
`selection_state != COMPLETE` with `INCOMPLETE_SELECTION_NOT_POSITIVE` before
creating possibility or consumer effects.

### Additional I2/RC0 issues

- **I2#1 static support (CLOSED):** empirical support computed from empirical
  CELLS, not static `selection["world"]["support"]`. Test proves mutation of
  cells 54/6→50/10 changes the computed support.
- **I2#5 reader edge (CLOSED):** changing `fx:r:public.values.min_age` 14→18
  changes both consumer outputs; `fx:r:mutual` values remain invariant.
- **RC0#5 negative algebra (CLOSED):** full 12-state vocabulary enforced;
  `DENIED` renamed to `DENIED_USE`; `NO_CURRENT`, `PROXY_MODELLED`,
  `UNKNOWN_UNOBSERVED_GAP`, `UNBOUND_RUNTIME_BINDING` added.

## Real N10E/C1 call trace (integration gap closed)

RC0 found zero port→N10E/C1 calls. SC0F wires a `producer_bridge` that:
1. In SOURCEFREE_FIXTURE mode: computes from empirical CELLS (not static WORLD),
   recording `SC0F_FIXTURE_EMPIRICAL_COMPUTATION` in the call trace.
2. In REAL_N10E_C1 mode: imports and traces `provide_empirical_possibility_slice`,
   `compose_positioned_subject_possibility`, `evaluate_positioned_subject_possibility`.
   If imports fail → `NOT_EXECUTED` (not fictitious GREEN).

## Executed tests — 115 passed, 0 failed

| Suite | Command | Passed | Note |
|---|---|---|---|
| SC0F repair verification | `pytest repro/tests/test_sc0f_repair.py -q` | 10/10 | All 5 I2 REDs + I2#1 + mutation + negatives + call-trace + conservation |
| N10E+C1 | `pytest test_pre553_empirical_possibility_provider.py test_pre553_analytical_composition.py -q` | 56/56 | Accepted owner suites, unmodified |
| PE author | `pytest test_source_backed_positioned_subject_possibility.py -q` | 13/13 | Accepted PE consumer, unmodified |
| K9 8 + K10 28 frozen | `pytest port/test_k9_provider_swap.py port/test_k10_structural_conservation.py -q` | 36/36 | Unmodified frozen oracles, original SC0 port at `b15dbbc4` |

**No xfail/skips relabelled PASS. No frozen oracle modified. No original owner
code modified.**

## Deliverables

| File | Content |
|---|---|
| [00_RETURN.md](00_RETURN.md) | this return |
| [01_FROZEN_SCHEMA_AND_INDEPENDENT_RED_CLOSURE.json](01_FROZEN_SCHEMA_AND_INDEPENDENT_RED_CLOSURE.json) | schema conformance + RED closure ledger |
| [02_REAL_ACCEPTED_OWNER_CALL_TRACE.md](02_REAL_ACCEPTED_OWNER_CALL_TRACE.md) | N10E/C1 call tracing evidence |
| [03_EXECUTED_FROZEN_AND_NEW_HOSTILES.json](03_EXECUTED_FROZEN_AND_NEW_HOSTILES.json) | all suite results, 115 tests |
| [04_REMAINING_SOURCE_AND_ADOPTION_HOLDS.md](04_REMAINING_SOURCE_AND_ADOPTION_HOLDS.md) | remaining holds + next step |
| [repro/sc0f/](repro/sc0f/) | repaired adapter, strict receipts, producer bridge, world laws |
| [repro/tests/test_sc0f_repair.py](repro/tests/test_sc0f_repair.py) | 10-case repair verification suite |

## What is NOT established

No operative N9/N10W service, no real-source computation, no V3 actor/person,
no model behavioral trial, no canonical adoption, no source/model issuer.
**Independent reviewer required before interface evidence acceptance.**
Full semantic A/B equivalence (I2#2) and real source-boundary H2 (I2#3) remain
PARTIAL — see `04_REMAINING_SOURCE_AND_ADOPTION_HOLDS.md`.

## Invariants

```text
FROZEN_ORACLES_MODIFIED     = NO
XFAIL_RELABELLED_PASS       = NO
ORIGINAL_OWNER_CODE_MODIFIED = NO
NEW_ACTOR_RULE_INTRODUCED   = NO
MODEL_CALLS / ACTOR_RUNS    = 0 / 0
ORIGINAL_SURVEY_OPERATIONS  = 0
CANONICAL / N12 / V3        = NONE / NONE / NONE
INDEPENDENT_REVIEWER        = REQUIRED
```

## Verification

Exact startup `4d7255e9183fb11d1fd36258ff05429f5cffed40` reverified against direct
remote before edits. All changed paths inside assigned return terrain. Final
remote SHA reported in push verification, not embedded recursively here.
