# WG0P11 independent clean replay

**PHASE_A_BANKED / PHASE_B_HOLD_NO_P10_IMPLEMENTATION. No SELFCONTAINED_PASS.**

The commission at sealed startup `75a4c331124ffd762e1a7f900b0a9c73897f9bd3`
expressly permits banking Phase A while P10 is unavailable. Direct remote checks
before freezing and after execution found the P10 branch still at startup
`90e6b5cc713780df0fb617d9357feed14c00ed24`. This is an unavailable repair,
not a failed repair. No future P10 implementation was inspected or evaluated.

Independent oracle and executable acceptance tests were pushed first at
`cb5484c96325e06b981dea22207e4dadc3d83558`, before their baseline execution.
They derive from the commission, pinned P9 review
`c2bfed5b2e11d229068dfdf78a3df16467704d14`, and original P8 source, not P10 output.
The reviewer has not authored the repair or assumed HQ/issuer/semantic authority.

## Actual isolated execution

Fresh clone `/tmp/wg0p11-independent-p8`, made with `git clone --no-hardlinks
--no-checkout`, detached at exact P8 `e1d82971f8c07147550ce53ef3c4bc52f349fed3`.
Its object source was this repository after fetching the exact remote P8 commit;
it is a separate checkout, not a reused reviewer directory or manual file overlay.
Initial `git status --porcelain` was empty. Darwin x86_64, Python 3.11.3,
pytest 9.1.1. Actual subprocesses and JUnit were used. No raw survey data.

All **187/187 original input files** were independently read and checked for
SHA-256, Git blob SHA-1 and byte length, including the **11 restored inputs**.
The source manifest is `2e7d47d2a14fe1fec12fd574c1183fadf50ee25b6f10a62ffae8858e29885418`.
The repaired P5 remains
`89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643`,
Git blob `62895078908ff748771da9a9fbcec6b36d34a803`.

| Actual P8 baseline check | Result |
| --- | --- |
| Independent original-187 custody test | PASS |
| D1 published probe-import | FAIL, exit 86: correct repaired module rejected |
| D2 direct bootstrapped fresh-process import | Import exit 0, acceptance FAIL: swallowed atexit FileNotFoundError, no audit receipt |
| D3 unchanged fresh-42 suite | 42 test cases, no assertion failures, 1 teardown error; acceptance FAIL |
| D4 unchanged pointer test | 1 failure at missing runtime parent; fixture use not reached |
| D4 independent fixture inspection | Placeholder cold path, no usable owner at that path; no manual repair |
| D5 exact historical verdict at required candidate path | FAIL: absent |
| Historical five WG0N controls, unmodified | 5 failures during construction; remain UNCONSTRUCTIBLE, not green |
| Historical characterisation file, unmodified | 1 pass / 2 failures with COMPLETE_BOUND_SOURCE_DESCRIPTOR_CHANGED |

The independent acceptance suite therefore reports **1 passed / 5 failed** on
the defective P8 baseline. These failures are intentional evidence that the
frozen checks discriminate the predecessor; they are neither xfailed nor
reported as repaired results. The pointer check's D3 dependency is disclosed:
its failure alone does not isolate D4; separate path inspection records D4.

The exact WG0N historical verdict was retrieved from
`6cd28b429504ad47e1bbc0fbcc6c4ef91db59ccd`, verified as
`839adc7508fcd81bd0a59af8f0fc8793b8ea075c80661683b776124cb90a228b`,
and frozen in this reviewer return only. It was **not** overlaid into the candidate.

## Phase B remains untested

No P10 clean clone, source closure, import receipts, WG0O17, WG0Q36,
mandatory236, fresh42, positive42/4I03, genuine crash23/resume0 process pair,
pointer refusal, transport9 or malicious-input checks were executed against
P10. P9's published positive results are expectations, not this reviewer's
observations. No inherited XML was presented as a new run.

The pending replay must start from the exact completed remote P10 commit with
no overlay. The published runner must create its own directories and cold
owner fixture. Record both cold OS PIDs, exits, I03 counts, original manifest and
receipt preimages; confirm pointer forgery makes zero new I03 calls. Verify all
original source bytes and disclose any transport-only changes separately from
the frozen original source manifest; do not silently rebaseline the strict
original-187 acceptance test. Run all required native suites and hostile cases,
including omission/hash change/wrong epoch/foreign authority, before acceptance.

No issuer can be inferred from source hashes; no temporal-owner rule,
source-artifact revocation grant, original-source U/E_pre, N11/N12/OC05,
V3/actor adoption or HQ acceptance follows from this packet.
