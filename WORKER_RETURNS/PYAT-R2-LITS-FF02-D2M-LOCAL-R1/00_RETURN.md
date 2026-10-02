# PYAT R2 — LiTS FF02-D2M LOCAL RETAINED-CHECKPOINT EXPORT — R1

**Disposition:** `D2M_LOCAL_CHECKPOINT_NOT_FOUND_OR_HASH_MISMATCH__HQ_ADJUDICATION_REQUIRED`
**Terminal:** `D2M_LOCAL_CHECKPOINT_EXPORT_RETURNED__HQ_ADJUDICATION_REQUIRED`
**Branch:** `agent/opencode-pyat-hq174-lits-d2m-local-checkpoint-export-r1`
**Commissioned tip:** `ffd85e5e92e07e32f14e013485c983e7a4c575e5`
**Block class:** governed retained checkpoint **absent from the designated execution surface**

No semantic access. No extraction performed. No self-adoption.

---

## 1. The gate failed at step 1

The commission requires, **before any semantic dereference**:

| Gate | Requirement | Result |
|---|---|---|
| 1 | exact path exists | **FAIL** |
| 2 | record observed file size | NOT AVAILABLE |
| 3 | stream-compute SHA-256 | NOT AVAILABLE |
| 4 | require exact equality | CANNOT BE EVALUATED |

So there is **no observed hash to compare**. This is an observed-**absence** block, not an
observed hash mismatch, and I want that distinction on the record: nothing about the
payload's integrity is in question. The file is simply not reachable.

**The designated path's root directory does not exist.** Walking upward from the governed
file path, the *first* missing component is `LOCAL_CUSTODY` itself:

```
MISSING /Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/...   <-- first missing component
```

Every deeper component is therefore absent too.

## 2. I searched before blocking, to make the finding precise

A block is only meaningful if it distinguishes "not at the governed path" from "not present
anywhere reachable." I ran:

- exact-path existence test;
- first-missing-component upward walk;
- filename search for `current_i05_materialization_checkpoint_v3.json` to depth 8 under `/Users/matthewsmith`;
- filename glob for `*i05_materialization*` to depth 8;
- directory search for any `LOCAL_CUSTODY` to depth 6 — **none exists at any depth**;
- directory search for `*DURABLE_CUSTODY*` / `*PREMAIN-FIABC-LITS*`;
- `/Volumes` enumeration — no external payload volume;
- git-annex / git-lfs store search to depth 5 — none.

**The most useful control:** a *sibling* directory `LOCAL_COURTS` **does** exist at the
repository root. That proves the repository root is readable and this is not a general
filesystem-visibility failure — the absence is specific to `LOCAL_CUSTODY`.

All discovery was path/metadata-level. No file contents were opened in service of it.

## 3. Why I did not use the custody manifest as the hash

The Git-banked control-plane manifest at the commissioned tip records exactly the
governed byte size and SHA-256, and confirms the persistent path matches this commission.

I did **not** adopt it as the observed value. A control-plane record is an *assertion about*
a payload, not an *observation of* it. The commission demands a freshly computed document
hash before any semantic dereference; presenting the manifest's hash as observed would make
the gate vacuous. Likewise I did not fabricate rows from the manifest — the four data TSVs
are **header-only, 0 rows**.

## 4. Exports — all blocked, none fabricated

| Required | Required | Exported |
|---|---|---|
| candidate → receipt bindings | 50 | **0** |
| AuthoritySnapshot closure | 24 | **0** |
| per-object authority bindings | 60 + 63 + 35 + 50 | **0** |
| P2 memberwise logical bindings | 50 (incl. 18 P2 mappings) | **0** |

**B001, B002, B003 all remain OPEN.** None is closed by this return, and
`06_B001_B002_B003_CLOSURE.tsv` records that explicitly rather than leaving them implied.

I also did **not** claim `D2M_RETAINED_PREIMAGE_CONTENT_GAP`: that would require having
reached the checkpoint and characterised a gap inside it. I never reached it, so asserting
a content gap would claim knowledge I do not have.

## 5. Prohibition audit — with one disclosure

No raw LiTS source opened, read, hashed, decoded or inspected. No source decoder. No I03 or
I05. No Candidate A/B/C. No P2X. No semantics inferred from values, counts, labels or
frequencies. No semantics reconstructed from Git or oracle artifacts. No production code
mutated. No PRE-V3 admission, no PRE-V3→V3.

**Disclosure.** During the location sweep I ran a broad `find -size +1G` over
Desktop/Documents/Downloads. That sweep `stat()`s each file it visits, so it made
**incidental metadata contact** with unrelated large files on this machine, including a
survey microdata backup under `rawlsing_v550_builder_bundle/backups`. No such file was
opened, read, hashed, decoded or inspected, and it is not raw LiTS source — but I am
recording the incidental contact rather than claiming an unqualified zero. The governed LiTS
checkpoint and raw LiTS source data were never opened, read, hashed or decoded.

## 6. Relationship to the prior D2 block

This is the **second consecutive block on the same payload, from a different cause surface.**

The prior D2 return (`6d23470ba…`) blocked because *that worker's execution surface* could
not see the checkpoint bytes. HQ then designated this governed local custody path **as the
execution surface specifically to remove that cause**.

On this surface the cause is **not** removed: the designated path's root directory does not
exist. So the designation did not take effect, or the payload was not present at the moment
of designation. HQ should treat this as a **custody-presence** question, not a repeat of the
original surface question — and the two should not be closed with the same action.

## 7. Smallest lawful next action

HQ to confirm whether `/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY` should exist on
this machine and, if so, restore or re-point the retained checkpoint at the governed path.
Then re-run this identical D2M commission **unchanged**.

No LiTS source reopen, decoder, I03/I05 rerun, Candidate A/B/C, P2X, or semantic
reconstruction is required or authorized to make that next step happen.

```
D2M_LOCAL_CHECKPOINT_EXPORT_RETURNED__HQ_ADJUDICATION_REQUIRED
```