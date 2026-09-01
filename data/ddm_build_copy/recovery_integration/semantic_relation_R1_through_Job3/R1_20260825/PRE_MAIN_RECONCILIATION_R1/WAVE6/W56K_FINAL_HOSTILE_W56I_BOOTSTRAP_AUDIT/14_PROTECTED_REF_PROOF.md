# Protected ref proof

## G15 — FAIL: required pre-bootstrap protected-ref state was already absent before this audit

Command-required values:
- `integration/pre-main-reconciliation-r1` = `8b13b67df8f055761b432191eca564c1840250ec`;
- `main` = `0777a34e50221bde6801dbaca26c058a7350c9e8`.

Observed before audit write:
- `integration/pre-main-reconciliation-r1` = `b53f8843092e776fb83ec584399641f5f2fc3de3`;
- `main` = `b53f8843092e776fb83ec584399641f5f2fc3de3`.

Commit `b53f8843...` is a direct child of candidate `6e50b535...`; the protected refs therefore already traversed the candidate before W56K began.

This audit made no PRE-MAIN/main update. Its only intended ref movement is its own worker branch from the immutable authorization SHA to the audit terminal commit.

The court cannot truthfully certify the command's requested G15 values. This is a fatal state/precondition failure independent of the executable-closure blocker.