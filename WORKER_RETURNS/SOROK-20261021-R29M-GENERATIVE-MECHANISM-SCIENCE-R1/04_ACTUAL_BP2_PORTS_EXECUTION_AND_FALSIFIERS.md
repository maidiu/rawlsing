# R29M / actual receiving-port mapping and test execution

## Bound source and port
At pinned BP2P4J commit `5b3e6577400ea1d88971ae6b48e41a118b8059ae`, the **actual** `vendor/bp2/bp2_joined/ports.py` blob `38751f36785fd935a7817483e2ef019c746e818a` declares immutable `Resource`, `CAN008RulePort.bind`, `CAN011TargetPort.bind_rule`, `CAN011TargetPort.bind_grant`, and `production_registries`. This file was read through authenticated private GitHub. R29M's callable `bp2_test_only_resources(ports, resource, subject, now)` provides a *TEST_ONLY* candidate A and independently sourced T with `NO_CHANGE` as its only allowed operation. It passes actual method arguments and exact SHA256 `rule_semantics` fingerprints to port bind calls. It DOES NOT call `bind_grant`; grant remains `None`; no production registry can be populated and no actor or CAN011 state is written. It is an adapter, not a concrete issued source rule.

## Physical executed tests — bounded Python only
Verified available isolated runtime: Python 3.13.5, pytest 9.0.2, source-neutral local root `/mnt/data/r29m_work`. Command:

```bash
cd /mnt/data/r29m_work
PYTHONPATH=source python -m pytest -q tests/test_generative_resource.py
# 29 passed in 0.06s (fresh rerun after earlier 29/29)
```

Exact source and tests are Git-blobs `d8aac69144610e1a546bbeb02f239e10682ca857`, `1e57772b4c0e85f3a6a335a473d2b731de67326b` and separately the unrun BP2 integration test `65873440e596b323431c12083c207a078882c6c8`, all independently checked with local `git hash-object` and remote `fetch_file`. No original respondent data, native person module or user Mac was accessed.

**R29M dynamic real BP2 import tests NOT_RUN/BLOCKED:** `PYTHONPATH=source python -m pytest -q tests/test_bp2_actual_ports.py` requires `bp2_joined` and its pinned candidate dependency from a staged private BP2P4J vendor checkout. Attempt in the isolated runtime failed on missing `bp2_joined` / package. Do not claim its two test cases passed. Qualified future run from a detached exact clone, with source closure verified:

```bash
ROOT=WORKER_RETURNS/SOROK-20261021-R29M-GENERATIVE-MECHANISM-SCIENCE-R1
BP2=WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1/vendor/bp2
PYTHONPATH="$ROOT/source:$BP2" python3 -m pytest -q "$ROOT/tests/test_bp2_actual_ports.py"
```

Even if those import tests pass, they prove candidate receiving **syntax/currentness/no-grant preservation**, not CAN008/CAN011 scientific authorization or C12 user behavior.

## Four required executed causal source-neutral contrasts
1. **B agency:** B SHARE_TOOL actual separately performed transfer changes feasibility from false to true with A own initial tool=0; B refusal/removal keeps false. With B share but NO A performed E2: feasibility true, world inspection still NO_CHANGE, V3 psyche unchanged.
2. **A historical enacted-source severance:** removing A's prior action changes H1 evidence status from past action present to absent; even when B restores feasibility and A later actually acts, no durable practice is created. A source removal must defeat a claim of *acquisition* but need not negate a separately legitimate objective act. No simplistic actor history→trait shortcut.
3. **Contradictory projects:** with contrary project and no later A action, result is UNCERTAIN_CONTRADICTORY_PROJECTS + NO_CHANGE; with a later independently performed A action the contradiction remains recorded, not cancelled by a compulsory scalar/trait.
4. **Demographic / role / type intervention:** with exact actor events, material world and action unchanged, perturb class/role/Enneagram/type tags and receive identical output fingerprint; category cannot change person psychology.

Additional tests cover missing/invalid world or E1, wrong A/B roles, duplicate or forged evidence preimages, foreign owner or clock, attempted future action, tampered or native-upgraded candidate resource, revoked source rule, missing actual A performed action, no material for action, stable result ordering and test-only zero production registries. Their passes are **logical sourcefree falsifiers only**; TEST_ONLY source IDs and content hashes are not independent source-owner signature, an issuer, or observational evidence for the acquired learned disposition.

## First real product falsifier — NOT_RUN
R29P, separate sibling integrator, owns cold C12 and same A0/A2 target assertion. R29M does not run or overwrite its branch. Future original A/B independently generated actor history → legitimate material world and B independent act → ADP010/ADP019 actual event → *original* issued CAN008 immediate response → *separately original* CAN011 NO_CHANGE/eligible target → later own E2 → C9/C10/C12 same root → truthful actor-limited A0/A2 must be source-severed on the same assertion. For the currently narrower proposed rule, objective B sharing should affect feasibility but not invent durable practice. Cutting a fixture constructor is not this consumer proof.
