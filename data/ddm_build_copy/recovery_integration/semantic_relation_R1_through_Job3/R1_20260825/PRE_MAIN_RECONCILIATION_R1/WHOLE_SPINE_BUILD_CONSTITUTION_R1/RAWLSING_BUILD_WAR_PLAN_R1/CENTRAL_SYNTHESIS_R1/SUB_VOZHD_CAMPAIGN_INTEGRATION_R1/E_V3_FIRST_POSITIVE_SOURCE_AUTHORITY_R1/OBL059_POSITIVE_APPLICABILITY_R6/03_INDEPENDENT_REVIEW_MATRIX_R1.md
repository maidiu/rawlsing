# OBL059 R6 — FRESH INDEPENDENT REVIEW MATRIX R1

Status: `FROZEN_BEFORE_GOVERNED_EXECUTION`

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r6-independent-review-r1`

Exact start:
`e4a42d77abfd6191025d4505ef9550700dd04e25`

Campaign authority consumed prospectively:
`2d0c274c28fdb16de5fbb731a90059184982d841`

Campaign tree:
`8f1c70c91ce9b94666005599e4ac3e01ea15847f`

Frozen target:
`5ca7380bd17b3dec271fe5a8c6bf22656f55b647`

Known producer evidence only:
`a21f7ba53a8f9e58a983b8f5c678ef66d1ad207a`
run `34250997854`

The commit containing this matrix, the independent test implementation, governed wrapper, and court spec is the independent matrix-freeze identity. No review execution is permitted before that freeze.

## Independent review families

1. Stable CPython threshold neighbors: positive and negative values immediately below, at, and above `10 ** sys.int_info.str_digits_check_threshold`.
2. Direct routing proof: malformed exact integers unsafe under any legal nonzero setting must be projected before inherited R5/R4/R3 evaluation; inherited evaluation is replaced with a deliberate failure sentinel for this check.
3. In-flight runtime-setting changes: controlled `0 -> minimum` change after R6 classification and before receipt completion, with process state restored.
4. Supported-setting invariance: `0`, minimum nonzero, and larger supported settings must yield the same deterministic negative receipt/proof for the same malformed oversized value.
5. Diagnostic correctness: sign, bit length, binary-magnitude SHA-256, positive/negative distinction, and nearby-value distinction.
6. Oversized exact integers at every required binding, including materially larger magnitudes.
7. Nested exact built-ins: oversized integer keys/values in dict/list/tuple/set/frozenset, cycles, mutual/shared references, and depth-boundary forms.
8. Adjacent primitives: exact-int subclasses, bool, ordinary floats, NaN, positive/negative infinity, bytes, sets/frozensets, opaque custom values.
9. Custom value protocols: malformed values whose display/hash/equality/iteration methods raise must still produce deterministic negative receipts without invoking those methods.
10. Custom Mapping packet forms with oversized required bindings: the malformed-input boundary must not depend on caller-controlled packet iteration/keys/display behavior where the public Mapping input form reaches inherited handling.
11. Repeated and concurrent evaluation while the supported runtime conversion setting changes.
12. Ordinary positive, ordinary negative, small malformed, scope, authority/evidence, adjacent-claim, and PROJECT_CURRENT preservation controls.
13. Deliberate unrelated programmer errors remain visible rather than being broadly converted into semantic negatives.
14. Every returned semantic receipt is checked for no project-current or downstream effects.

## Disposition law

Exactly one fresh independent review is authorized. If any case finds a blocker, return the smallest exact blocker, perform no repair, and do not run or commission a second review of this frozen candidate. A green workflow alone does not determine semantic PASS; the review result is based on the frozen matrix outcome.

`REPAIR_PERFORMED_BY_REVIEWER = NO`
`SECOND_REVIEW_COMMISSIONED = NO`
`PROJECT_CURRENT_STATE_CREATED = NO`
