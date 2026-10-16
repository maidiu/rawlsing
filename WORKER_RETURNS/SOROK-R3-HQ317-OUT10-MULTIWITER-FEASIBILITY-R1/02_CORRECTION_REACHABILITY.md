# OUT10 CORRECTION — the OUT8 prototype IS reachable; my first return was wrong on this point

**Issued by the same worker, superseding the reachability claim in `00_RETURN.md` §2 and `01_FEASIBILITY_HOLD.json`.**

## What I got wrong

My first return stated the OUT8 journal prototype was "not reachable from the assigned branch" and framed the HOLD as *prototype not reachable*. **That was an error of my own investigation, not a fact about the repository.**

A `git ls-remote origin` check — which I ran **after** pushing that return — shows the OUT8 commit is the **tip of a real, fetchable branch**:

```
0e05c7dab8334b96f2b2b79e935eeebb1c0f0d11  refs/heads/agent/rabochii-sorok-r3-hq313-out8-restored-ack-ghost-repair-r1
```

I had checked out only the **assigned branch tip** and observed that commit `0e05c7da` *adds no Python relative to its parent* — and wrongly concluded the prototype was absent. The correct conclusion is the opposite: **`0e05c7da` is a branch tip whose tree carries the prototype**; the commit merely did not *add* new Python files.

I also failed to notice the sibling branches that plainly carry this lineage: `…hq298-sr-outbox-execution-r1`, `…hq300-outbox-authority-cold-repair-r1`, `…hq299-rsr-occurrence-outbox-independent-r1`, `…hq301-rto-outbox-cold-court-r1`, `…hq303-out3-outbox-independent-r1`.

## Corrected verdict

**`MULTIWITER_FEASIBILITY_HOLD__PROTOTYPE_REACHABLE_BUT_NOT_EXAMINED_BY_THIS_WORKER`**

The HOLD stands — but for a **reviewer-omission** reason, not an inaccessibility reason. I did not check out `agent/rabochii-sorok-r3-hq313-out8-restored-ack-ghost-repair-r1`, so I did **not** falsify the prototype, did **not** reproduce the two-writer stale-journal failure, and did **not** test any concurrency, crash, revocation or ACK property against it.

## The baseline smoke — also reported honestly

My three-process unlocked-append smoke found **600/600 lines, 0 lost, 0 duplicates**. I record that plainly: it **did not** reproduce the failure mode the commission names, and it is **not** evidence for or against the OUT8 prototype. A naive smoke that fails to break is not a safety proof, and I do not present it as one.

## What the next worker must do (corrected)

1. Fetch and check out **`agent/rabochii-sorok-r3-hq313-out8-restored-ack-ghost-repair-r1`** (`0e05c7da`) — that is where the prototype lives.
2. Locate the journal/outbox module and the accepted single-writer court (OUT9's scope).
3. Preregister interleavings, commit invariants, typed conflicts and crash expectations **before** running.
4. Execute **two and three genuine simultaneous processes** against the real prototype; test lost committed events, duplicate/stale identities, typed version conflicts with lawful retry, atomic cold recovery, revocation/ACK integrity across conflicting writes, and crashes before/after publication.
5. Only then investigate a minimal source-free multiwriter candidate (interprocess journal lock or versioned CAS).
6. **Preserve** all original source bytes, original test assertions and both historical REDs; do not convert the inherited two-writer RED into PASS by rewriting the old court.

## Preservation
No original source byte, original test assertion or historical RED was modified by this worker. No helper agents, no model/harness switch, no production ADP019 issuance, no V3 operation.
