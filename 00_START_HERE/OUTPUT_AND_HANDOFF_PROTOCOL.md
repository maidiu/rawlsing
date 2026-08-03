# Output and cumulative-handoff protocol

For every response that reports newly completed Rawlsing work or supplies newly generated Rawlsing artifacts:

1. Put the link to the newly updated complete cumulative handoff package at the very top of the response.
2. The package must contain the entire prior governing state, every relevant task return, and the newly completed work.
3. Detached deltas may be supplied secondarily, never as the sole restart artifact.
4. Update CURRENT_STATE.json, EXACT_RESUME_POINT.md, SCOPE_LOCK.json, the master handoff, top-level validation, package index and hashes in the same package.
5. Apply ACCEPTANCE_STANDARD_NO_REVIEW_LOOP.md inside the tranche before reporting completion. A separate immediate review is not the default next task.
6. A new agent must be able to resume without reconstructing missing turns or requiring the user to re-explain the project.

Progress-only updates that introduce no completed artifact do not require a package link. The next completed-work response does.
