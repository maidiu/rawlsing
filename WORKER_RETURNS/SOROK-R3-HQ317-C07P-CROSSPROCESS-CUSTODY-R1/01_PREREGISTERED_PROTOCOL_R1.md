# SOROK HQ317 C07P — preregistered protocol, threat model and expectation matrix

**Status:** `FROZEN_BEFORE_ANY_ADAPTER_IMPLEMENTATION`.
**Frozen at commit:** `82ba75680f7cf296918c6236ef7c0e8df1756dde` (this file is committed before `c07_journal.py` or any
adversarial test exists).
**Author:** HQ317 C07P bounded source-free custody implementation experimenter.
**Native source under adaptation, unmodified:** OC6 blob `4c185c18dbee57603038e97886da8fc4aa834082`.
**Accepted independent review:** OC7 `6e7d85d28f82729a06ede32d0440b63d0452a634`.

Nothing in this document may be edited to match an observed result. Where an expectation turns out to be
wrong, the wrongness is reported as a finding and the expectation is amended in a **new** file with a
new freeze commit.

---

## 1. What C07 is, and what it is not

OC7 recorded C07 (cross-process custody durability) as **`NOT_REACHED`**, because the OC6 native
`EscrowState` keeps `_event_proofs`, `_capsule_seals` and the whole ledger **inside the same Python
process as the state they protect**. Nothing survives interpreter exit.

C07P's task is to build a real, bounded, source-free **prototype** that persists authorised escrow
state to a filesystem journal and restores it in a **genuinely separate OS process**, then to report
honestly how far that gets and where it stops.

**C07P is NOT, and will never claim to be:**

| Not claimed | Why |
|---|---|
| Real institutional / third-party escrow | there is no external institution, and none may be invented |
| A cryptographically protected or externally anchored journal | the journal is an ordinary local mutable file; see §5 |
| Anti-tamper against an attacker who controls both state and digest | see the explicit failure ceiling in §5.3 |
| Production durability | see the fsync/process-kill ceiling in §4.4 |
| Semantic non-leakage, semantic issuance, V3/N12, production admission | out of scope and unauthorised |
| Adoption of OC6 or OC7 | this is an experiment, not an acceptance |

## 2. Native API audit — done BEFORE implementation

Public `EscrowState` surface actually available (measured, not assumed):

```
authorize_holder(person_id: str, role: Role) -> None
commit(capsule: CustodyCapsule) -> None
unblind(capsule_id: str, holder_person_id: str) -> Dict[str, Any]
release(capsule_id: str) -> None
record_exposure(capsule_id: str, exposed_to: str, purpose: str) -> None
verify_ledger_integrity() -> bool
rollback_ledger(seq: int) -> None      # always raises; append-only by construction
```

There is **no** `export`, `snapshot`, `restore`, `load`, `save`, `to_dict`, `revoke_holder`, and **no**
method accepting a timestamp.

### 2.1 Measured facts that constrain the design

1. `capsule_envelope_commitment` is a **pure function of the capsule's 18 fields**. It contains no
   escrow timestamp. Therefore full 18-field envelope binding **survives a process restart unchanged**.
2. Replaying the same operations through the public API reproduces `committed`, `_capsule_seals`,
   `released`, `holder_roles`, `exposure_log` structure and `verify_ledger_integrity() == True`.
3. Replaying does **NOT** reproduce escrow event timestamps. `unblind` and `record_exposure` stamp
   `time.time()` internally, and there is no parameter to supply the original value.

### 2.2 Typed dependency holds declared up front

| Hold | Exact missing interface | Consequence |
|---|---|---|
| `C07_DEPENDENCY_TS` | a public way to restore escrow event timestamps (`unblind`/`record_exposure` need an optional `at` parameter, or an explicit `replay_event(at=...)`) | escrow event timestamps are **journal-faithful but not escrow-faithful** after restore; the reconstructed ledger re-stamps them |
| `C07_DEPENDENCY_REVOKE` | a public `revoke_holder(person_id)` | holder **revocation** cannot be expressed through the public API at all; only grant-and-refuse is testable |

These are **not** worked around by mutating internal dictionaries, by `object.__setattr__`, by pickling
live objects, or by re-signing. Doing any of those would forge authority.

## 3. Journal data model (preregistered)

One journal file. UTF-8 JSON Lines. One canonical record per line, newline-terminated.

```
record := {"v":1,"seq":<int>,"kind":<str>,"payload":<obj>,"prev":<hex64>,"rec":<hex64>}
rec    := sha256(canonical(record without "rec"))
prev   := "0"*64 for seq==1, else the previous record's "rec"
canonical := json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=True)
```

`kind` ∈ `AUTHORIZE | COMMIT | UNBLIND | RELEASE | EXPOSURE`.

`payload` per kind:

| kind | payload |
|---|---|
| `AUTHORIZE` | `{"person_id":str,"role":str}` |
| `COMMIT` | `{"capsule":{18 capsule fields},"commitment":<hex64>}` |
| `UNBLIND` | `{"capsule_id":str,"holder":str,"unblinded_at":float}` |
| `RELEASE` | `{"capsule_id":str}` |
| `EXPOSURE` | `{"capsule_id":str,"exposed_to":str,"purpose":str,"exposure_ts":float}` |

The capsule is stored as **plain JSON of its 18 declared fields**, never as a pickled object.
On restore the dataclass is reconstructed by `CustodyCapsule(**fields)` and then re-validated by the
native `capsule_envelope_commitment`, which re-derives the digest from the reconstructed object.

**Committed-data rule.** `commitment` is recorded in the record and re-checked on restore. A record
whose recomputed commitment disagrees is rejected as forgery. This is an unkeyed integrity check, not
authentication — see §5.3.

## 4. Write protocol and crash envelope matrix (preregistered)

Every append rewrites the whole journal to a temp file, then atomically replaces. Chosen over in-place
append because it yields a clean, decidable torn-record story.

```
write  tmp   = <journal>.tmp   (full new content)
flush  tmp
fsync  tmp
[CRASH POINT 1]  before os.replace
os.replace(tmp, journal)
[CRASH POINT 2]  after replace, before directory fsync
fsync  directory containing journal
[CRASH POINT 3]  after directory fsync  == clean
```

### 4.1 Preregistered expected fates

| Crash point | Expected on-disk journal after a *process* kill | Expected restore | Classification |
|---|---|---|---|
| 0 — before temp written | previous journal | previous state | `CLEAN_ROLLBACK` |
| 1 — after temp fsync, before replace | previous journal (temp is orphaned) | previous state | `CLEAN_ROLLBACK` |
| 2 — after replace, before dir fsync | **indeterminate under real power loss**; new content visible under process kill | new state under process kill | `NOT_SETTLED` |
| 3 — after dir fsync | new journal | new state | `COMMITTED` |

### 4.2 Preregistered honesty constraint on crash point 2

A `SIGKILL` of a process does **not** exercise power-loss semantics: the kernel page cache survives, so
the post-rename bytes remain visible regardless of whether the directory entry was fsynced. This
experiment therefore **cannot** validate durability at crash point 2, and C07P **must not claim it
does**. Point 2 is preregistered as `NOT_SETTLED` and is expected to *remain* unproven at the end. A
genuine test needs a machine-level power cut or a separate filesystem, neither of which is authorised
here.

### 4.3 Preregistered atomicity expectation

Under crash points 0 and 1 there must be **no torn or partial record** in the journal, and no record
whose `rec` digest fails to verify. A partially written last line is a *failure* of this protocol, not
an accepted state.

### 4.4 Durability ceiling to be stated in the verdict

`fsync` availability and the filesystem backing the journal are **observed and recorded**, not assumed.
The verdict must state the observed platform and that local file durability is not institutional
custody.

## 5. Threat model (preregistered)

### 5.1 In scope — detected by the prototype

| # | Threat | Expected detection |
|---|---|---|
| T1 | record payload tampered | `rec` digest mismatch → refused |
| T2 | record deleted from the middle | `seq` gap and `prev` chain break → refused |
| T3 | records reordered | `seq`/`prev` chain break → refused |
| T4 | duplicate record appended | non-monotonic `seq` / duplicate `seq` → refused |
| T5 | whole journal rolled back to an earlier valid state | **NOT detectable by this prototype** — see 5.2. Expected: restore succeeds and silently loses later events. This is a recorded limitation, not a defect claim. |
| T6 | forged capsule field substituted in a COMMIT record | recomputed `commitment` ≠ recorded → refused |
| T7 | forged signature used to unblind | native `require_second_signature` / escrow checks refuse |
| T8 | unauthorized purpose persisted | native `verify_purpose` refuses on commit |
| T9 | uncommitted capsule exposed / ghost commitment | native `_validate_capsule` refuses |
| T10 | unblind recorded without a prior COMMIT | replay order violation → refused |
| T11 | exposure for an uncommitted capsule | refused |
| T12 | inconsistent materialised unblind (e.g. holder mismatch) | native `verify_ledger_integrity` refuses |
| T13 | truncated final line | journal parse / digest refusal |
| T14 | stale snapshot replayed over a newer journal | `seq`/head mismatch → refused |

### 5.2 Out of scope — cannot be solved here

- **Whole-journal rollback to a previously valid state.** The chain is internally consistent at every
  prefix, so a prefix is indistinguishable from the truth without an external monotone counter. This
  is T5 and it is a **known accepted failure** of a local journal.
- **An attacker who can rewrite both the journal and its digest.** See 5.3.

### 5.3 Explicit bounded failure ceiling (preregistered, must appear in the verdict)

`rec` is an **unkeyed SHA-256**. Anyone who can write the journal can recompute the whole chain after
altering it. Therefore:

- This prototype detects **accidental corruption and naive tampering** (T1–T4, T6, T13, T14).
- It provides **zero cryptographic protection** against an adversary with write access to the journal
  directory. Such an adversary can also delete the journal, replay a valid old prefix (T5), or forge a
  consistent chain.

Any claim that this establishes anti-tamper custody would be false. Detecting it requires an **external
append-only anchor or a key held outside the journal's trust domain** — neither exists here, and
inventing one is outside this commission.

## 6. Preregistered positives (must all hold)

| # | Expectation |
|---|---|
| P1 | Process A commits, unbinds, releases, records exposure through the **native public API only**; `verify_ledger_integrity() == True`. |
| P2 | Journal written atomically; every record's `rec` verifies; `seq` is 1..N contiguous. |
| P3 | Process A is terminated with a real signal. |
| P4 | A **fresh, independent** Python process B, with its own interpreter and a **fresh import** of the pinned module, restores the escrow and obtains `verify_ledger_integrity() == True`. |
| P5 | Restored capsule's `capsule_envelope_commitment` is **bit-identical** to process A's, proving all 18 fields survived. |
| P6 | `committed` ids, `unblinded` ids, `released`, `holder_roles` and exposure count match process A. |
| P7 | Process B **safely continues** the authorised lifecycle (a second capsule commit, unblind, release). |
| P8 | Native `verify_ledger_integrity()` remains `True` in B after continuing. |
| P9 | `module.__file__` and the module's SHA-256/Git blob SHA-1 in B equal the pinned values. |
| P10 | Escrow event timestamps are journal-faithful; `C07_DEPENDENCY_TS` is reported as an open hold, not hidden. |

## 7. Preregistered negatives (must all hold)

| # | Expectation |
|---|---|
| N1 | A tampered record is refused at restore; escrow is not materialised. |
| N2 | A middle-deleted record is refused. |
| N3 | A reordered pair is refused. |
| N4 | A duplicated record is refused. |
| N5 | A COMMIT record whose capsule fields were altered is refused by the commitment check. |
| N6 | An EXPOSURE before any COMMIT is refused. |
| N7 | An UNBLIND for an uncommitted capsule is refused. |
| N8 | An unauthorised holder is refused by the native escrow. |
| N9 | A forged purpose is refused by native `verify_purpose`. |
| N10 | A truncated trailing line is refused. |
| N11 | A stale snapshot replayed over a newer journal is refused. |
| N12 | Whole-journal rollback to a valid earlier prefix is **accepted** — this is T5, recorded as a demonstrated ceiling, and the test asserts the ceiling exists rather than pretending it is caught. |

## 8. Preregistered preservation requirements

- The ten OC7 historical literal REDs remain **literal RED**. This experiment must not alter them.
- OC6's accepted controls remain green; the lexical/Unicode gate is **not widened**.
- `CustodyCapsule` / `EscrowState` source bytes are **never edited**. The adapter lives only in this
  return folder.

## 9. Preregistered verdict options

Only one of:

- `SOURCEFREE_C07_CROSSPROCESS_CANDIDATE_REQUIRES_I2` — if P1–P10 and N1–N12 all hold as written.
- `C07_EXECUTION_HOLD` — if a native interface gap prevents lawful reconstruction. The two gaps in §2.2
  are expected to be reported as **open typed holds alongside** a candidate, since they narrow but do
  not prevent the core A/B demonstration.

Either way: **no adoption, and a distinct future independent review is mandatory.**
