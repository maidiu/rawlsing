# Exact acbba91 recovery payload

This directory embeds the exact historical Git bundle needed to recover the fused executable ancestry required by Phase D M6.

- required base: `d49e55c9f2df86c5412be8759b9ad6ca86778262`
- bundle target: `acbba91de28b9cee20af05e81e4d8bfdaa876298`
- reconstructed bundle SHA-256: `7ed342080215ed605551b96c1d0e0ec2b90a83f53e0a913fc35a3d299eb528fa`
- original historical wrapper ZIP SHA-256: `01353d215617a5337b183952587837dd52ded11c603cf3b1e1b2cbfd940bba52`

The binary Git bundle is stored losslessly as eight base64 parts because the GitHub connector used for this handoff only accepts UTF-8 file writes.

Reconstruct it with:

```bash
python3 phase_d/recovery/acbba91/reconstruct_and_verify.py
```

Then, from a clean checkout/worktree containing the exact base commit:

```bash
BUNDLE="$PWD/phase_d/recovery/acbba91/Rawlsing_PreV553_Wiring_Contract_Repair_acbba91.bundle"
BASE=d49e55c9f2df86c5412be8759b9ad6ca86778262
TARGET=acbba91de28b9cee20af05e81e4d8bfdaa876298

git cat-file -e "${BASE}^{commit}"
git bundle verify "$BUNDLE"
git fetch "$BUNDLE" refs/heads/pre553-wiring-contract-repair-r1
test "$(git rev-parse FETCH_HEAD)" = "$TARGET"
git merge --ff-only FETCH_HEAD
test "$(git rev-parse HEAD)" = "$TARGET"
```

This payload is for **exact ancestry recovery only**. Do not run the historical repair packet's old nine-scope matrix as the current M6 canary. After recovering `acbba91`, install/use the current `phase_d/` M6 contract and execute only the current bounded V550/shared-substrate/V550J/V551/V551J gate.

No respondent data, database extract, `.env`, credential, or secret is contained in this recovery payload.
