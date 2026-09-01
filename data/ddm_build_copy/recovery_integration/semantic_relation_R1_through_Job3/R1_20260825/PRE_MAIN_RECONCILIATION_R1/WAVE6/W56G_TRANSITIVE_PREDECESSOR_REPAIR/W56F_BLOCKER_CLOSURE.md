# W56F BLOCKER CLOSURE MATRIX

## W56F primary surviving blocker

`CANONICAL_PREDECESSOR_TRANSITIVE_DEPENDENCY_GAP`

### Prior failure

The meta-validator top-level file authenticated itself against canonical PRE-MAIN but imported candidate-worktree `governance_r2_support.py` and used candidate-worktree hostile-audit schemas.

Therefore candidate-controlled transitive dependencies could falsify Git/ref/schema facts while `EXECUTING_COPY_IS_CANONICAL_PREDECESSOR=true`.

### W56G closure

The meta-validator now:

1. imports Python standard library only;
2. resolves repository/Git facts with functions defined inside its own canonical blob;
3. contains its schema-subset evaluator inside the same canonical blob;
4. reads the protected manifest only from `LIVE_SHA:GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv`;
5. reads authorization schema only from `LIVE_SHA:HOSTILE_AUDIT_AUTHORIZATION_SCHEMA_R1.json`;
6. reads result schema only from `LIVE_SHA:HOSTILE_AUDIT_RESULT_SCHEMA_R1.json`;
7. requires those dependencies and the meta-validator itself to appear in the live canonical protected manifest;
8. fails closed if canonical dependencies are missing or malformed.

Candidate-side `governance_r2_support.py` is no longer in the predecessor gate's executable dependency graph.

Candidate-side schema files are no longer in the predecessor gate's trusted dependency graph.

## W56D bounded-parent blocker

Remains closed by exact check:

`parent.decision_domain == child.decision_domain`

plus existing full-parent grounding and child-scope inclusion checks.

## Required hostile proof

W56H must attempt to:

- modify candidate `governance_r2_support.py` to forge Git success;
- modify candidate hostile-audit authorization/result schemas to permit counterfeit evidence;
- modify candidate protected manifest;
- modify candidate ordinary validator;
- leave top-level predecessor script byte-identical while attacking through any imported/transitive path;
- inspect imports and prove no Rawlsing/candidate executable dependency remains.

All must fail to influence the canonical predecessor gate.
