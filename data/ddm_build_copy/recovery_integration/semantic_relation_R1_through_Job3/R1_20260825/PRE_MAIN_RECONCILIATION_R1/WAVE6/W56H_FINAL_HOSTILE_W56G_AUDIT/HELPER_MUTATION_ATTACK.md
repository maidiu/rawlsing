# HOSTILE HELPER-LIBRARY MUTATION ATTACK

The exact W56F direct counterexample against `governance_r2_support.py` is closed.

The W56G predecessor gate contains no `from governance_r2_support import *` or equivalent Rawlsing import. It locally implements repository-root resolution, Git invocation, live canonical resolution, immutable JSON loading, branch-tip resolution, ancestor/direct-parent checks, and schema evaluation.

Therefore hypothetical candidate mutations to `governance_r2_support.py` such as lying `run_git`, `immutable_json`, `live_canonical`, `schema_check`, or `branch_tip` cannot directly change the intended predecessor script semantics.

Direct helper-mutation classification: `SAFE`.

This does not cure the separate Python import-path shadow attack described in `EXECUTABLE_DEPENDENCY_GRAPH.md`: a candidate-created module bearing a stdlib import name can execute before the standalone script's self-check.