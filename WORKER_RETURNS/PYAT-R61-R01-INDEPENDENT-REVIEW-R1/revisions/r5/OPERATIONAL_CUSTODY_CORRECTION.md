# Operational custody correction — R61-R01V R5 independent review

This note is separate from the reviewer oracle and does not alter
`EXPECTATIONS.md`, whose bytes were recovered unchanged from
`1738231a9ede56ada79861dac83130aa55285520` (SHA-256
`394238be34b98431f819020997061df7fd96817913d7ad696ed7be4e94cca39b`).

## Acknowledged defect in the original freeze custody

The original R5 reviewer session froze and committed its EXPECTATIONS while
its persistent session directory was the director checkout
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-flight-director`, not the
commissioned review worktree
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r5`. That
wrong-worktree freeze is acknowledged as an operational custody defect. This
note records the defect; it does not authorize the wrong-worktree behavior,
does not validate any product conclusion from that session, and does not make
the prior failed sessions product evidence.

Coordinator correction
`3249eb333e1288362af649242d17f5ae9e689817`
(`WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R61S_REVIEWER_DIRECTORY_CORRECTION.md`)
authorized exactly one bounded replacement execution session for the same
logical review job. This replacement session passed the mandatory first tool
preflight with:

- working directory `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r5`
- repository top level `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r5`
- branch `agent/opencode-pyat-r61-r01v-r5-independent-review-r1`
- no tracked modifications

The failed prior session `ses_e963b8f69ffeP1AvmCps3aYigs` remains terminal
`FACILITY_CWD_MISMATCH`; its records are preserved. This session is not the
author session `ses_e98c905cbffekusoHURfKyEUKG`, uses no subagents or extra
sessions, and keeps write scope to
`WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r5/`. The
candidate/startup `4b5fd7a240a6e2d007ba1df2424780e6b5612ea9` remains
unchanged; candidate production and historical evidence are immutable.
