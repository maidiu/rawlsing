# Authorization lineage and recovery noncircularity

Authorization ref:

`a1146aac4d19777a7074d478aac3b7fcfa76837b:data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/AUDIT_AUTHORIZATIONS/W56O_W56N_OBJECT_IDENTITY_REF_PROVENANCE_AUDIT_AUTHORIZATION_R1.json`

Challenge nonce: `625c222d53eed61b4b172809503d5008`

The authorization binds exact candidate `5bfcb9ddfc30a9f0958e675a5af6c611978284bf`, exact expected audit branch `agent/rabochii-premain-w6u-final-hostile-w56n-object-ref-review-r1`, exact write prefix for W56O, and only the two authorized PASS rulings.

Independent topology checks establish:

- `b53f8843092e776fb83ec584399641f5f2fc3de3 -> a1146aac4d19777a7074d478aac3b7fcfa76837b` is `ahead_by: 1` with the canonical base as merge base;
- that one authorization commit changes exactly the W56O authorization JSON and no protected path;
- W56N candidate `5bfcb9ddfc30a9f0958e675a5af6c611978284bf` and authorization `a1146aac4d19777a7074d478aac3b7fcfa76837b` are diverged with merge base exactly `b53f8843092e776fb83ec584399641f5f2fc3de3`;
- W56N is 24 commits ahead of the recovery base;
- W56M terminal is a separate 2-commit sibling lineage from the same recovery base;
- W56N is 16 commits ahead of W56L candidate `a94c5613dba1f3d3121be244296d0d3733003507`, while W56M remains external negative evidence rather than an ancestor that could manufacture W56N authority.

The W56O worker branch was created from the returned authorization SHA, not from W56N. W56N was not modified, merged, cherry-picked, rebased, or integrated.

Therefore:

`RECOVERY_AUTHORIZATION_IS_EXTERNAL_TO_CANDIDATE = TRUE`

`W56N_CANNOT_SELF_AUTHORIZE = TRUE`

`W56N_CANNOT_SELF_INTEGRATE = TRUE`

`BOOTSTRAP_REUSED = FALSE`

This is the required post-bootstrap external-review structure, not a second bootstrap and not candidate-generated evidence.