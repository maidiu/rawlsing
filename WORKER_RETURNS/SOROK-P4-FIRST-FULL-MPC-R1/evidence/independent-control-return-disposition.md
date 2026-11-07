# Independent P4 control-return receiving

I independently reviewed runtime `9eacf50380176d617637489d04cab3a969dd0a29`, tree `4a3c78f03d4a1087507443439722db025b339221`, for the defect identified in [PR #751 review 5813377183](https://github.com/maidiu/rawlsing/pull/751#pullrequestreview-5813377183). I authored neither the runtime change nor its tests. I extracted the six P4 Python blobs at the reviewed SHA into scratch space and linked the unchanged received P2/P3 dependency tree. No code or repository state was changed by this review.

Runtime was `/usr/local/bin/python3`, CPython 3.11.3, ABI `cpython-311-darwin`, SQLite 3.40.1 on macOS 13.7.8 x86_64. The received sourcefree B1 file had SHA-256 `478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3`. No model provider was invoked by the runtime.

Commands from the repository root, with `exact_cut` pointing to the directory containing the extracted P4 Python files:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider -q "$exact_cut"
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/p4-independent-control-return.py "$exact_cut/run_p4.py"
```

The driver invokes the actual CLI in separate processes for every action. It reopens the received owner to verify persisted world state and event order. It restores a pre-action baseline at the same path for exact replay, tests source severance with an absent B1 path in the consumer subprocess, and injects distinct actor-private and user-private sentinels into scratch state for the public-surface control.

## Repaired decision boundary

- Caller-selected `say --request-edge` performed the exact utterance, recorded actor access, and returned the observed clock-230 invitation and a clock-230 choice. The reopened owner reported material 1 and zero ACTUAL intervals. The pre-user S46 agenda remained in scheduled history.
- Whitespace SAY was refused. A foreign invitation with `--then-wait` was refused. Neither changed the public view, advanced the clock, consumed material, or wrote an ACTUAL interval. The valid invitation remained available on cold reopen.
- Plain `inspect-edge` produced a user-perceived inspection at clock 230 with `changed=false`. Material stayed 1, the clock stayed 230, and there was no ACTUAL interval. Reusing the spent token with `--then-wait` was refused and still produced no work.
- From the restored invitation checkpoint, `inspect-edge --then-wait` first produced a real no-change inspection at clock 230. The received S46 actual repair event followed the inspection in persisted event order. Material changed 1 → 0 and control returned at 232. Cold reopen and request-ID retry retained one ACTUAL interval and the exact same user result.

## Continuing controls

1. The actual workshop agenda and P3 formation existed before the first user turn. The opening had one prior mediator and showed the arrival anchors and current controls.
2. The caller's exact speech and explicit request flag reached the performed event. Altered text changed the event hash in the actor readset. A decline and the same affirmative text without the flag opened no invitation.
3. Blank speech, forged invitation and spent invitation produced no requested act. Invalid temporal delegation produced no work.
4. Recognized and imposed antecedents yielded distinct actor responses under equivalent opening and material conditions. The imposed history offered no inspection.
5. Empty history had zero P3 records and remained executable. Plain inspection demonstrated valid material and clock no-change.
6. Severed B1 caused real CLI refusal `P3_B1_SOURCE_SEVERED` with exit 2 and left the pre-action ledger unchanged.
7. Restored B1 and same-path baseline replay reproduced the accepted invitation response exactly.
8. Cold reopen preserved root, actor, branch, source hash, utterance and outward-event identity. The persisted repair resolved by its event ID and hash and followed inspection in event order.
9. Actor-only and user-only sentinels remained absent from public CLI output. The checked private receipt, readset and mediator fields also remained absent.
10. The invitation was displayed before any relevant work, unlocked a caller-selected inspection and returned the supported choices. The sourcefree machine performed no automatic inspection. The explicit wait flag ran the preserved work only after a successful inspection.

## PR package equivalence

I compared `4eef0167e7a58d707cc406633af3336af5f3111c` with the reviewed runtime using `git diff --name-only` and an all-Python pathspec. The changed files are README, author manifest, public transcript, and internal receipts. All Python files are identical. The updated README documents plain inspection and explicit post-inspection waiting. The refreshed public transcript gives first observation/return 230/230, second observation/return 230/232, and cold view 232. The internal first turn has no interval and the second turn records caller `then_wait=true` plus the actual interval. The author manifest names the reviewed runtime SHA.

## Independent trace receipts

Root `3bcb21fc22df3255269382ad249f706dd6dd5378cb886af26542991ff516a4f7`, actor `TEST_ONLY_BP1_R26V_ACTOR_A`, branch `first_session`.

| Event | Persisted identity |
| --- | --- |
| Caller speech | `TEST_ONLY_BP4_WORLD_EVT_c06ae7f8bf20655e758ace8ef5d9bccbd0a24e20d74c890de2a778391f1e03f6` |
| Observed invitation at 230 | `TEST_ONLY_BP4_WORLD_EVT_ea29900c8f288d9736bbf9fca918dd522292176b26818e4a397c8fbf63eb1685` |
| Caller inspection in explicit wait branch at 230 | `TEST_ONLY_BP4_WORLD_EVT_f83d558ba474c4eb0b12be57cdf1535fcc38955e5b4688fc050dba3ea88bb614` |
| Subsequent ACTUAL repair during 230–231 | `TEST_ONLY_BP4_WORLD_EVT_235828ca824d3dbfb8f79eddaf6b094566cb80e7705a21e5ad4f75a53f125eec` |

The independently rerun exact-cut pytest suite passed all three tests in 128.82 seconds.
The independent CLI driver exited 0 after all ten continuing controls and both valid inspection paths. The separate plain-inspection branch produced `TEST_ONLY_BP4_WORLD_EVT_8f0a0a54b2d0b0f13ee77c8ecddf1f29b564c5eaa17e20bd915de479f3a3e652` and retained clock 230 and material 1.

## Disposition — ACCEPT for bounded sourcefree engineering

The review 5813377183 defect is corrected at the exact runtime. The actor's actionable intervention is returned before material work and remains available after cold reopen and refused actions. The preserved sourcefree repair executes in the explicit time boundary selected by the caller, after actual inspection. The existing MPC-1 through MPC-7 sourcefree chain, privacy, source severance and restoration remain operational. The reviewed sourcefree action vocabulary couples waiting to a successful invitation inspection. Material repair is established by the objective world receipt and event order. The observed inspection and outward speech have their own user perception. Native science, original rights, human participation, and protected integration remain with their respective owners.
