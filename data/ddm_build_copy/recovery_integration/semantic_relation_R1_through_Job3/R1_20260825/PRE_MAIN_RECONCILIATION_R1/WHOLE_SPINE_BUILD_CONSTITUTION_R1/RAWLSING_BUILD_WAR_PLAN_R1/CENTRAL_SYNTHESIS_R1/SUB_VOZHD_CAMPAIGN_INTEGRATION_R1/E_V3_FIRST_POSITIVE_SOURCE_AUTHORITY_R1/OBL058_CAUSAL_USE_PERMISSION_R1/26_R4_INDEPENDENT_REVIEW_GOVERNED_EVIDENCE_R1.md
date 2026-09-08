# OBL058 — CAUSAL_USE_PERMISSION — R4 INDEPENDENT REVIEW — GOVERNED EVIDENCE R1

## Review status

`SEMANTIC_RECOMMENDATION = FAIL`

Frozen candidate reviewed:
`f02509a25b23365596ccedc7c8bc3a973dce3468`

The candidate was not modified by this reviewer.

## Reviewer-owned identities

- exact reviewer start: `a57f2efdc1b3130b62b60381cf0950a3e817230e`
- campaign instruction/adjudication: `f7618257604c362097edb3c78dae8480a9499c4a`
- independent matrix freeze: `979428d6ec4d61d8a39fadd12704a06304ec3383`
- independent test-surface commit: `a97450535b232ae31da6d6fa6c531cb36aafbbdf`
- initial governed wrapper commit: `f60deb82451d87cb99bf7d1e4481081976c1a3e2`
- court-spec binding commit: `da75787175cbd0c6a5fee7629bd86961fc2bd55b`
- final wrapper correction / governed evidence execution: `73ed58b10595ecfca32009e44758e4fee7daf372`

The wrapper correction changed only one reviewer-side discovery assertion: `REGISTERED_*` constants had been mistaken for a callable registration surface. No candidate code or semantic expectation was changed.

## Governed execution

Corrected governed run/job:
`34238219350` / `102101357437`

Result:
`success`

Protocol self-tests:
`20 passed in 0.08s`

Court-spec validation:
`PASS`

Independent court:
`26 passed, 28 subtests passed in 1.61s`

Bounded-court receipt:
- result: `PASS`
- exit code: `0`
- semantic candidate: `f02509a25b23365596ccedc7c8bc3a973dce3468`
- evidence execution: `73ed58b10595ecfca32009e44758e4fee7daf372`
- Python: `3.12.14`
- implementation: `CPython`
- spec SHA-256: `48a390e86a5fc6fb96d1f77ad2c2317d7287676ff849f464a3d088ab7dff8b36`

Artifact:
- ID: `10060789925`
- name: `rabochii-court-receipt-34238219350`
- ZIP SHA-256: `129c8a0629722742751df0799cf7fc06431badbe5073f2ab07bff2174e6a10a4`

Execution-only PR:
`#289` — closed unmerged.

### Non-semantic first attempt

The first governed attempt `34238066249` / `102100831836` failed because one reviewer assertion rejected any exported name containing `register`; this incorrectly matched non-callable `REGISTERED_*` constants. The source-origin blocker tests and all other executed tests passed. The assertion was narrowed to callable registration surfaces and the corrected governed run above is the review evidence of record.

## Independent blocking finding

Smallest blocker:

`BLOCKER__OBL058_R4_VALIDATOR_TRUSTS_CALLER_REBINDABLE_PARENT_TRANSPORT_RESPONSE`

The R4 child process itself is one-shot and correctly rejects caller-built authoritative body injection and duplicate initialization. The remaining defect is in the parent validation boundary.

`IssuedReceipt` exposes parent-visible, caller-rebindable slots:

- `_body_json`
- `_write_fd`
- `_read_fd`
- `_proc`

`validate_receipt` trusts those fields after checking only that `_proc` is a live `subprocess.Popen` and the file-descriptor fields are nonnegative integers. It does not prove that `_write_fd` and `_read_fd` belong to that process, that the process is the source-owned receipt authority child for this receipt, or that the response came from that authority.

The independent court therefore reproduced two blocking paths:

1. Construct an exact `IssuedReceipt`, assign any nonempty parent-visible body string, point its read/write descriptors at caller-created pipes, assign `_proc` to an unrelated live `subprocess.Popen`, and have the caller-side responder return `{"ok":true,"decision":"PERMIT"}`. `validate_receipt` returns `PERMIT` even though no source-owned receipt authority child issued that receipt.
2. Start with a genuine source-issued `DENY` receipt, terminate its child, rebind the same parent-visible transport fields to the caller-side responder above, and `validate_receipt` returns `PERMIT` for the formerly denied receipt.

These are not child semantic decisions. They are parent-side response substitution. Accordingly, caller-visible runtime state can cause an unissued positive receipt to validate, which directly violates the commissioned source-origin property.

A green governed test run does not make this a semantic PASS: the blocking tests intentionally assert that the incorrect-positive behavior is reproducible.

## Preservation findings

The independent court also confirmed the material already-correct controls remain present on the frozen candidate:

- the child initialization protocol rejects caller-supplied body content;
- validate-before-initialize is rejected;
- duplicate initialize/reinitialize is rejected;
- the launcher has semantic scope/basis/fixture inputs rather than caller body input;
- valid registered synthetic `PERMIT` remains functional;
- valid unregistered-basis `DENY` remains functional;
- ordinary mapping/proxy/copy/deepcopy/pickle/exact-type/subclass paths do not validate through the real child authority;
- parent body mutation does not change a real child's fixed authority;
- cross-receipt body substitution fails against the real children;
- repeated real validation is stable;
- terminated real child fails closed;
- malformed caller response values fail closed;
- exact five-field scope binding and cross-scope replay rejection hold;
- field-specific `NONCURRENT_SYNTHETIC` namespace, empty-suffix, exact first-canary, and project-current-shaped rejection hold;
- project-current fixture is rejected;
- inference-like surrogate basis strings yield `DENY`;
- authority/schema/fixture/scope/proof/integrity mutations fail closed;
- no callable public registration surface or current-effect API was found in the reviewed module surface.

## Separation / no-current-effect attestations

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`ENCOUNTER_CREATED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`OBL061_UNBLOCKED = NO`

`HQ_ADOPTION_CLAIMED = NO`
