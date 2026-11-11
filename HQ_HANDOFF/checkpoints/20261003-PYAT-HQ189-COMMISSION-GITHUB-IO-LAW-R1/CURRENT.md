# Pyat HQ189 — mandatory GitHub commission I/O law

Status: `COMMISSION_STARTUP_AND_RETURN_PROTOCOL_HARDENED__HQ188_TWO_SLOT_WAVE_REBOUND`

Every issued worker/reviewer commission must now explicitly bind both ends of cross-machine Git state.

Startup:
- fetch `origin`;
- resolve the exact remote worker/reviewer branch;
- verify it equals the exact commissioned startup SHA supplied by HQ;
- read the commission from that exact fetched tip;
- use an isolated worktree at that tip;
- stop before editing if local/remote/commissioned identities differ;
- do not use a blind `git pull` as synchronization.

Return:
- write and commit the complete return packet and authorized changes;
- push the worker/reviewer branch to `origin`;
- re-fetch/resolve the remote branch;
- verify local HEAD equals the exact remote return SHA;
- report that branch/SHA/disposition to HQ.

A local-only commit or chat completion is not a return. A commission missing equivalent startup or remote-return binding is malformed and must not launch.

The standing template and operating design carry this law for future commissions.

HQ188 active lane A is rebound to:
`agent/rabochii-pyat-hq188-a-opencode-dispatcher-runtime-repair-r1 @ ff7a06694b0391471b8e1223b2f881b3288f529e`.

HQ188 active lane B is rebound to:
`agent/rabochii-pyat-hq188-b-c4-current-consolidation-r1 @ 9001be646305036e493eea3dbce427f62f91c9ae`.

Both tips include `00_COMMISSION.md`, `01_RETURN_PROTOCOL.md`, and `02_STARTUP_GIT_PROTOCOL.md`.

All source/warrant/live-execution holds remain unchanged.
