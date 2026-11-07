# Independent P4 engineering receiving

I did not author the runtime changes. I extracted the six P4 Python blobs for each reviewed cut with `git show <SHA>:<path>` into separate scratch directories and linked the existing P3 import entry into each scratch parent. Git comparison showed the received dependency tree unchanged. I made no branch, protected, production, or original-source changes.

- Original runtime `b6c9170cab7403ffc14cad2ab95b6dc969c24e3e`, tree `46d84358fa0579eded24581bfe6ff05c5930a9e0`.
- Repaired runtime `0fde115bf8adb6d3929ea2a6e98bbd5cb6274274`, tree `c1031f105be084d5fc7ec562ded8aca0ff9b4149`.
- Evidence commit `8de1369f8` changes README and three evidence files only. Its README uses the explicit `--request-edge` argument. Its Python files match the repaired runtime.
- Runtime `/usr/local/bin/python3`, CPython 3.11.3, ABI `cpython-311-darwin`, SQLite 3.40.1, macOS 13.7.8 x86_64, Darwin 22.6.0. The runner uses the received sourcefree dependencies and no model provider.
- B1 source SHA-256 `478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3`.

## Commands

With `exact_original` and `exact_repaired` set to the two directories containing the extracted files, I ran:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider -q "$exact_original"
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/p4-independent-review.py "$exact_original/run_p4.py"
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/p4-independent-review-fixed.py "$exact_repaired/run_p4.py"
```

The original suite returned 3 passed in 123.65 s. The separate drivers execute actual CLI subprocesses for `new`, `view`, `say`, and `inspect-edge`, restore scratch baseline state at its original path, and use the actual store API to verify persisted events and introduce two private sentinels. The RED subprocess redirects the P3 B1 lookup to a nonexistent file without editing the received file. A fresh unmodified subprocess restores the source path.

## Original cut disposition — REVISE

The exact original cut performed a real sourcefree chain. It also made every perceived nonblank utterance an invitation trigger under recognized history. At the same cold pre-action checkpoint, “Do not invite me to inspect. I am leaving the edge.” produced the same “Come look at this edge with me.” outward speech as a request to examine the bench. Altering caller text changed the performed speech hash and actor readset. The uptake context treated the performed utterances identically.

The original opening also projected root language training exemplars as ordinary speech, including conflicting invitations and time, material, and tool refusals. The provenance is `s45.fixtures.root_bundle`, which adds the HELP templates as evidence attributed to B, and S44's initialization hook in `s44/session.py`, which admits the examples as language encounters. The generic S45 projection renders perceived events without identifying that training role. P4's use of the unfiltered feed compromised the actionable footing required by MPC-2.

## Repaired cut controls

1. **Antecedent.** Before any caller turn the stored root had a P3 formation and one prior mediator. The S46 workshop agenda was already present as a scheduled interval from 228 to 230 with no performed work. Opening and first cold view matched. The opening displayed perceived arrivals, workshop location, available tool and the two supported speech controls. The stock training utterances were absent.
2. **Altered user action.** Restoring the same cold baseline and changing caller input changed the performed speech event and actor readset. The explicit decline stayed exact in the speech event and produced no inspection response. Submitting the same affirmative text without the explicit flag also produced no invitation. The positive flag was bound into the attempt and performed event.
3. **Refusal.** A whitespace SAY returned `EMPTY_SPEECH`, performed no speech and left the public surface unchanged. A fabricated invitation could not perform inspection before a real invitation, and a spent invitation could not perform again.
4. **History contrast.** With the same explicit request, stable opening footing and equal objective material state before work, recognized history activated joint checking and imposed history activated private checking. Only joint checking offered inspection.
5. **Valid empty and no change.** The empty antecedent had zero P3 records and remained executable through an actor-alone response. Actual subsequent inspection returned `changed=false` at clock 232.
6. **Severance RED.** The actual first consumer refused with exit 2 and `P3_B1_SOURCE_SEVERED`. The opening ledger was unchanged.
7. **Restoration.** The unmodified-source subprocess accepted. A second cold replay from the same-path baseline reproduced the entire accepted public response, including its invitation event ID.
8. **Cold reopen.** The actual P2 store reopened on the same root, actor and branch. The P3 snapshot matched the ledger and persisted user speech, repair and outward expression resolved by their recorded event IDs and hashes. The actor readset bound the performed speech and B1 hash. After inspection the cold public view matched the prior return.
9. **Privacy.** An actor-only event and a user-only note were persisted with distinct sentinels. Neither appeared in cold CLI `view`. Public output omitted the checked internal receipt, attempt, readset and response-mode fields.
10. **Returned choice.** The jointly conditioned actor utterance offered a choice whose token was that observed speech event ID. No inspection was performed before the caller submitted it. Inspection resolved to an actual visible event and removed the spent choice. Caller SAY and request controls remained available. The alternate actor-history cells refused the same inspection token.

The repaired independent driver passed all assertions. Its timed CLI subprocesses completed in about 3–11 seconds each on this runner. The repaired positive trace used root `3bcb21fc22df3255269382ad249f706dd6dd5378cb886af26542991ff516a4f7`, actor `TEST_ONLY_BP1_R26V_ACTOR_A`, and branch `first_session`. Admitted speech ran at clock 230, with material 1 → 0 during the actual interval and control returned at clock 232. The actor mode and event access were read separately from this objective change.

| Receipt | Identity |
| --- | --- |
| Caller speech event | `TEST_ONLY_BP4_WORLD_EVT_c06ae7f8bf20655e758ace8ef5d9bccbd0a24e20d74c890de2a778391f1e03f6` |
| Caller speech event hash in actor readset | `22ba70b18215e289eb6ce105ab08fe0877c8dd19014bbf13ea7bca6757f99230` |
| Observed invitation | `TEST_ONLY_BP4_WORLD_EVT_ea29900c8f288d9736bbf9fca918dd522292176b26818e4a397c8fbf63eb1685` |
| Caller-selected inspection | `TEST_ONLY_BP4_WORLD_EVT_54f9937b3b6fd11670f13cf8bd86f4ce5ee9370ee7f4d9a3eb1d048d7f7d7877` |

## Repaired cut disposition — ACCEPT for bounded sourcefree engineering

The repaired cut satisfies MPC-1 through MPC-7 together within one executable, cold-reopenable root, actor, branch, clock, and source lineage. P2 persists the caller-authored speech and actor access. The reader consumes the already committed P3 activation only when the caller explicitly selects the edge request. The Other can respond differently under controlled prior history with the same material footing. P2 commits the observed expression and the caller may perform a separate inspection on the resulting world. The material repair is an actual internal world consequence. The public trace establishes observation of the speech and inspection. It supplies no evidence that the user perceived the repair itself.

This acceptance covers the workshop fixture's bounded action vocabulary, local public CLI surface, and same-path reopen. The explicit flag is a caller-selected operation, with free text retained as supplied and no general interpretation claim. The local audit ledger is private audit material. The source severance used the B1 filesystem lookup as exercised in the driver. Original-rule science, native psyche or memory, independent B, live source/actor grants, human participation, and protected integration remain outside this engineering receiving decision.
