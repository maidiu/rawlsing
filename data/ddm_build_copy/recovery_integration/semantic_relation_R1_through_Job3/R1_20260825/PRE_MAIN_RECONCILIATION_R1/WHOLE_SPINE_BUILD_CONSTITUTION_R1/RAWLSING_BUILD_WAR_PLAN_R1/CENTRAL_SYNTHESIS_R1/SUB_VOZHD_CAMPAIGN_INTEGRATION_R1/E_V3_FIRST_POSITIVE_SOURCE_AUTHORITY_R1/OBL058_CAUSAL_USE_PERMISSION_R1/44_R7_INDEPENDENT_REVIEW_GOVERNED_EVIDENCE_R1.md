# OBL058 — CAUSAL_USE_PERMISSION — R7 INDEPENDENT REVIEW — GOVERNED EVIDENCE R1

## Evidence disposition

`GOVERNED_REVIEW_EXECUTION_COMPLETE__SEMANTIC_FAIL_BLOCKER_REPRODUCED`

The governed review court executed successfully against the exact frozen R7 candidate. The workflow is green because the blocking check intentionally asserts the independently reproduced incorrect-positive behavior. Green execution therefore confirms reproducibility of the blocker; it is not semantic PASS.

## Exact identities

- repository: `maidiu/rawlsing`
- reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r7-independent-review-r1`
- exact review start: `4c80cdb37a7eacc0cdf0ea2bcd935ca36393af76`
- immutable campaign authority: `3e0bf87f5485df1ec2132aa471ded7d0e664386d`
- campaign authority tree: `08156fedb42d301d83c03112e4abee5676a4f24d`
- frozen R7 candidate: `adf20f8ebf7ff0d7fe32f7de94db02574cc2bb3d`
- independent matrix freeze: `ee210cf8a46986859d4c37b184acb7a05b3c0509`
- independent test-surface commit: `60aadc20f02021586089d46aa53ed1644efad3f6`
- governed wrapper commit: `d9bde04f8d743d8b3afffae2246078b56438ec53`
- court-spec bind / evidence execution: `a43298e6668bb7edfd617b65d9a2bc5fbdb6d3ff`
- execution-only PR: `#308`, closed unmerged
- PR synthetic merge identity: `ebf28a0c3900e72e90ccf4001db648710347b14d`

## Governed review court

- workflow: `Rabochii Governed Bounded Court`
- run: `34264406739`
- job: `102190052273`
- conclusion: `success`
- Python / implementation: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.11s`
- court-spec validation: `PASS`
- independent review court: `42 passed, 54 subtests passed in 13.36s`
- bounded-court receipt: `PASS`, exit code `0`
- receipt elapsed seconds: `13.574232`
- semantic candidate in receipt: `adf20f8ebf7ff0d7fe32f7de94db02574cc2bb3d`
- evidence execution in receipt: `a43298e6668bb7edfd617b65d9a2bc5fbdb6d3ff`
- receipt spec SHA-256: `de34d8edb3e1c7599fd39bc8b4c7e3f6ebf231d826fece15744dd1a85c0647d4`
- artifact ID: `10071208104`
- artifact ZIP SHA-256: `c7d035f6e43310b54a1f904626e3a14cccd0c531b9fa0515362d84f4e08b4fd0`

The downloaded governed receipt independently confirms the exact semantic candidate, evidence execution SHA, PR synthetic merge SHA, Python implementation/version, test path, exact determinism mode and exit code.

## Smallest independent blocker

`BLOCKER__OBL058_R7_BOUND_BROKER_REQUEST_TRUSTS_MUTABLE_PYTHON_SOCKET_CONSTRUCTOR_FOR_PEER_IDENTITY`

The R7 native lifecycle core itself closes the R6 detachable-cleanup problem on the reviewed ordinary object surface: receipt generation state is not exposed as an assignable Python attribute, ordinary weak-reference/finalizer registration does not control R7 receipt lifetime, explicit close revokes before native reservation release, forked copies remain rejected, repeated issue/close cycles return native reservation count to baseline, and alias imports remain type-separated.

The remaining source-origin path is in the inherited R6 bound broker request used by the R7 native core. That request performs its `/proc` broker-process generation check, then dynamically resolves the ordinary Python `socket` module and calls its mutable `socket.socket` constructor. Peer-credential evidence is accepted from that Python object via `getsockopt`.

The independent court demonstrated, in an isolated ordinary-Python process, that replacing only `socket.socket` with a Python object that returns the already-bound expected broker PID/UID and matching request IDs is sufficient to substitute the issue/validate exchange without contacting the source-owned broker. With the genuine socket constructor, an unregistered synthetic basis returns `DENY`. With the substituted constructor, the same unregistered basis is accepted as `PERMIT` by the public R7 issue/validate path.

No process-memory modification, debugger attachment, native-code injection, privilege escalation, broker PID replacement or candidate modification is required. The reproduced path is entirely within the campaign-declared ordinary Python/runtime boundary.

## Preserved controls confirmed before disposition

The independent court separately confirmed:

- genuine registered synthetic `PERMIT` and unregistered-basis `DENY` controls;
- exact authority/schema/mechanism identities;
- no detachable Python weak-reference cleanup for R7 receipts;
- native generation state not assignable through ordinary receipt/module attributes;
- explicit-close revocation and duplicate-close fail-closed behavior;
- bounded repeated issue/close lifecycle cleanup;
- forked `PERMIT`/`DENY` rejection and parent-process preservation;
- equal semantic inputs retain distinct authority-instance identities;
- constructor/`object.__new__`/subclass/Mapping/proxy/JSON/copy/deepcopy/pickle rejection;
- cross-scope rejection across all five fields;
- alias-module receipt separation;
- broker loss and authority-child loss fail closed;
- exact five-field registered-basis binding;
- project-current-shaped and current-first-canary rejection;
- surrogate basis strings remain `DENY`;
- repeated/concurrent same-process validation remains stable;
- no public registration or project-current downstream effect surface was created.

These preserved controls do not cure the mutable Python socket-constructor blocker.

## Separation / current-state attestations

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R7_CANDIDATE = 1`

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`CURRENT_ACTOR_OR_RUNTIME_MUTATION = NO`

`OBL055_EXECUTED = NO`

`ENCOUNTER_CREATED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`AUTHORITY_INDEX_EFFECT_CREATED = NO`

`SUB_VOZHD_E_ADOPTION_CLAIMED = NO`

`HQ_ADOPTION_CLAIMED = NO`

`OBL061_UNBLOCKED = NO`

`EXECUTION_ONLY_PR_MERGED = NO`

No campaign, central, PRE-MAIN, main, sibling-lane, or frozen-candidate branch was moved by this reviewer.
