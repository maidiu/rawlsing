# HQ188-A — explicit return-to-HQ protocol

This addendum is part of the worker commission and governs the meaning of **return to HQ**.

## Return means publication of the worker candidate to the worker's GitHub branch

When the commissioned work is complete:

1. Write the complete required return packet in the commissioned return directory.
2. Commit **all and only** authorized implementation/documentary changes and return evidence to your worker branch.
3. Ensure the working tree has no uncommitted commissioned work that is needed to understand or reproduce the return.
4. Push the worker branch to `origin`:
   `agent/rabochii-pyat-hq188-a-opencode-dispatcher-runtime-repair-r1`
5. Fetch/resolve the remote branch and verify that:
   - local `HEAD` is the intended final candidate;
   - `origin/agent/rabochii-pyat-hq188-a-opencode-dispatcher-runtime-repair-r1` resolves to exactly the same full 40-hex commit SHA.
6. Record that exact final SHA in the return packet's primary return file and final-disposition file.
7. Return to HQ with at minimum:
   - branch name;
   - exact final remote SHA;
   - final disposition;
   - terminal token from the main commission.

## Prohibited

- Do **not** merge, fast-forward, rebase, or otherwise publish the worker candidate into `integration/pre-main-reconciliation-r1`.
- Do **not** edit `HQ_HANDOFF/**`.
- Do **not** self-adopt.
- Do **not** force-push rewritten history after returning a candidate. If a correction is required after return, append a new commit and report the new exact SHA.

## HQ visibility

A local-only commit is **not returned**. HQ's review surface is the pushed GitHub branch.

Until the repaired dispatcher itself is independently accepted, automatic cross-session notification is not assumed. After the remote branch is verified, the user may notify HQ simply by providing the branch/final SHA (or by saying this named lane returned if the final SHA is included in the Space Bunny completion message).

Terminal addition:
`HQ188-A_REMOTE_BRANCH_RETURN_VERIFIED`
