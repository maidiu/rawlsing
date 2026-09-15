# Recover the required fused ancestry (`d49e55c` → `acbba91`)

The historical governed recovery package is preserved in Rawlsing Library as `Rawlsing_PreV553_Wiring_Contract_Repair_acbba91_SMALL.zip`.

Verified package SHA-256: `01353d215617a5337b183952587837dd52ded11c603cf3b1e1b2cbfd940bba52`.

The enclosed Git bundle SHA-256 is `7ed342080215ed605551b96c1d0e0ec2b90a83f53e0a913fc35a3d299eb528fa` and declares:

- required base: `d49e55c9f2df86c5412be8759b9ad6ca86778262`
- target/head: `acbba91de28b9cee20af05e81e4d8bfdaa876298`
- ref: `refs/heads/pre553-wiring-contract-repair-r1`

The original package's fresh base-to-target `git fetch` + fast-forward-only application test passed.

On a clean worktree at the exact base, verify the ZIP hash, extract it, and run its packaged `scripts/apply_and_validate.sh <real-local-repo>`. Do not replace this with file copying or a synthetic equivalent. After HEAD is exactly `acbba91...`, install the additive Phase-D sidecar commits and proceed with the M6 instructions. If the local working tree is dirty, preserve it and use an isolated worktree rather than resetting user work.
