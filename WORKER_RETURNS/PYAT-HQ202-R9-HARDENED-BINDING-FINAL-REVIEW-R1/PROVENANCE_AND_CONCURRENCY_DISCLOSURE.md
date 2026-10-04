# Provenance and concurrency disclosure

## Duplicate concurrent commissioned run

While this review was executing, a **second agent ran the identical HQ202 commission** in the same
sparse worktree (`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq202-r9-binding-final-review`) on
the same branch (`agent/reviewer-pyat-hq202-r1`). It finished first and pushed
`0deb64784829661780ee3957f8070ccc2c241722` to `origin/agent/reviewer-pyat-hq202-r1`.

Timeline observed from this session:

| time (EDT) | event |
|---|---|
| 08:59 | the commissioned sparse worktree already existed at `217f96b5d9f7b767a7cfb11e5c2c3c7c75d77b4f` |
| 09:04 | this reviewer created its return directory; it was empty apart from that directory |
| 09:05–09:06 | an unattributed 7-file packet plus 5 evidence scripts appeared in that directory |
| 09:06:16 | this reviewer's own evidence script was written there |
| 09:07:12 | the other agent committed |
| ~09:09 | origin moved to `0deb6478`; the other agent's commit message documents this reviewer's file as an unattributed provenance hazard and excludes it |

Both agents behaved defensively: the first return excluded the file it could not attest to, and this
reviewer isolated its own work rather than overwriting the first return.

## Handling

- `origin/agent/reviewer-pyat-hq202-r1` is **untouched** at `0deb6478`, by explicit HQ instruction.
- This packet is published on `agent/reviewer-pyat-hq202-r1-independent-corroboration`, based on the commissioned startup SHA
  `217f96b5d9f7b767a7cfb11e5c2c3c7c75d77b4f`, so the return directory on that branch contains exactly
  this reviewer's packet.

## Independence statement

Every number in this packet is read back out of this reviewer's own run logs under `evidence/logs/`.
The evidence programs were written from the commission text and do not import or reuse the
candidate's court.

Disclosed caveat: the other return's disposition line was read at approximately 09:07, before this
reviewer's proofs finished. That is a possible anchoring influence and is stated rather than hidden.
The substantive evidence — the 29 A–D claims, the 9 warrant checks, the pre-hardening defect
reproduction and the court runs — is this reviewer's own and was produced independently.

## Reproducing

    cd <worktree root>            # deea4054 rawlsing_next
    VENV=/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python
    PYTHONHASHSEED=0 PYTHONPATH=$PWD $VENV evidence/01_independent_proofs.py
    PYTHONHASHSEED=0 PYTHONPATH=$PWD $VENV evidence/02_warrant_compatibility.py \
        warrant/01_SEVEN_SOURCE_PLAN_BINDING.json warrant/03_SRC27_OUTER_AND_LOWER_ACCOUNTING.json
    PYTHONHASHSEED=0 PYTHONPATH=$PWD $VENV evidence/03_adversarial_observations.py

The warrant JSON inputs are the blobs at `89054b882c04cf0541b6f9f4abdb555c808ad94d`:

| file | blob |
|---|---|
| `01_SEVEN_SOURCE_PLAN_BINDING.json` | `4fcc10bcc978a0c6b943bd0bf115a26a5b8f41a6` |
| `03_SRC27_OUTER_AND_LOWER_ACCOUNTING.json` | `1a932a0dec35ddbc0416ddbe08287cb9f0125b95` |

The pre-hardening control was run against a read-only tree extraction, never a clone:

    git archive 35ffa48204672e6c7180cd010a7c1adde9f18cd7 rawlsing_next | tar -x -C <tmp>
    PYTHONHASHSEED=0 PYTHONPATH=<tmp> $VENV evidence/04_prehardening_control.py
