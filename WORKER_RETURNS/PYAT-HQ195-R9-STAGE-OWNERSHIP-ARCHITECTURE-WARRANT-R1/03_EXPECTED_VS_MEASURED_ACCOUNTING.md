# Expected versus measured accounting — and why the distinction decides R9

Lane: `PYAT-HQ195-R9-STAGE-OWNERSHIP-ARCHITECTURE-WARRANT-R1`

## The distinction the commission forbids collapsing

Omega-1 stages O1-C07 at `DURING_EXECUTION_AND_RETURN`, and its acceptance sentence says:

> `Freeze expected budgets and instrumentation before launch; retain measured counts.`

Read as one obligation these contradict each other. Read as three separable obligations
they do not, and the apparent contradiction dissolves without weakening anything:

| Obligation | Stage | Owner | Nature |
|---|---|---|---|
| **Expected budget** | S2 pre-launch | HQ | a number fixed in advance |
| **Instrumentation** | S2 pre-launch | HQ + execution owner | a *mechanism*, verified to exist before launch |
| **Measured count** | S3/S4 during execution and return | C4 execution owner | an observation retained after the run |

So the staging conflict is **not** the problem. The problem is that for one account both
halves are missing, and for different reasons.

## Why the expected budget cannot be frozen

No frozen artifact carries an expected path-opens figure for any of the seven permitted
sources. What O1-C07 actually freezes per source is *workload*-shaped:

```
SRC02  expected_full_reads 0, expected_selected_reads 1
SRC08  expected_metadata_reads 1
SRC26  expected_header_prefix_bytes 176
SRC27  expected_full_route_passes 1 (max 1)
```

None of these is an open count. The closest thing is the SRC27 hardened note, which supplies
a **floor expressed in account terms**:

> "The run will require at minimum: one existence/access check, one full SHA-256 hash pass,
> one metadata read, and one full compatibility read."

and then immediately says:

> "It does NOT license assuming one file open. The pass will involve multiple path-level
> opens, a hash pass, a metadata pass and a full read."

A floor in account terms is not an exact open count, and the same paragraph warns against
converting it into one. Deriving a number here would be inventing a count.

Note also which frozen *zeroes* touch opens: `WVS_SRC35_fresh_source_opens: 0` and
`excluded_source_fresh_opens: 0`. Both are zero **by construction** — SRC35 is a retained
comparator with no fresh access, and excluded sources are not opened at all. Neither
constrains the seven permitted sources. Reading either as covering them would be a
category error.

## Why the measured count cannot be taken

The count happens inside pyreadstat's compiled extension. On the bound surface
(macOS 13.7.8, CPython 3.11.3, pyreadstat 1.3.6):

- `DYLD_INSERT_LIBRARIES` with plain symbol definitions loaded but captured **zero** events,
  *including for a direct `ctypes libc.open` control*;
- `__DATA,__interpose` made CPython fail at startup on both available interpreters, even for
  a cold `getpid`;
- privileged tracing is outside the no-sudo authority.

The direct-libc control is what makes this rigorous. Because a control call that certainly
did open a file also produced zero observations, the zero is a **mechanism failure**, not
evidence of zero opens. HQ192 recorded the governing rule:

> "Zero is a record of what this lane could OBSERVE, not a count of what the reader did.
> The read succeeds, so the reader certainly opens the file."

HQ194 accepted this and added the second half: the runtime can neither **measure** the
literal count nor **enforce** a maximum at that layer.

## The two failures are independent — this is the analytical core

An expected budget and a measured count ordinarily compensate for each other: if you cannot
predict the value, you measure it; if you cannot measure it, you budget it. Here **neither
compensation is available**, and they fail for different reasons:

- the budget fails because **no authority has ever stated the figure** (a documentary gap);
- the measurement fails because **no lawful mechanism exists on this host** (a capability gap).

That distinction matters for what HQ can do. A documentary gap is closed by a decision. A
capability gap is closed only by a runtime change or by new authority. Because the account
needs both, closing either one alone leaves the obligation unmet — which is precisely why
"pair a pre-launch budget with a during-run measurement" (the option the mission lists
second) cannot work here.

## The tempting substitution, and why it is forbidden

A Python-level open count now **exists and is enforceable**: HQ192 measured **2 opens per
decode** (whole-file hash pass + bounded header prefix), and an excess header-prefix read was
refused before execution. HQ191 separately established a reader-invocation ceiling and
demonstrated abort before the unauthorised operation.

Both are real, lawful and useful. Neither is the account O1-C07 names. The frozen authorities
forbid the substitution four separate times:

1. **O1-C07** `measurement_basis_requirement`: "A count of 'opens' is meaningless without
   stating whether it means OS-level path opens, reader invocations, or decoder calls. These
   are different quantities and C4B froze them as separate accounts."
2. **O1-C07** hardened note: misreading the single SRC27 pass as one open "would be an
   accounting failure and is expressly forbidden by Omega-1."
3. **HQ191**: the reader-invocation ceiling "is an upper bound on accesses, **NOT** an account
   of opens, and is not relabelled as one."
4. **HQ194**: "R9 is not closed by replacing path opens with reader invocations or
   Python-level opens."

The reader-invocation ceiling remains lawful as an **upper bound on logical accesses**. It is
simply not the required account. The existence of an enforceable near-miss is exactly the
condition under which a redefinition becomes tempting, and the commission's instruction not
to weaken "path-level opens" into "reader invocations" is aimed precisely at this moment.

## What a bound runtime does and does not buy

C4B's template left `execution_surface` as `<HQ_TO_BIND_EXACT_RUNTIME_AND_C3_EQUIVALENT_HEAD>`.
The adopted candidate resolves it to a concrete stack and tree identities. That is real
progress — but it does not close R9, and the reason is worth stating precisely:

> **Determinism of a value is not observability of it.**

Binding the runtime guarantees the count *would* be reproducible if it could be observed.
Observability is the missing precondition. This forecloses the argument that R9 is "just an
unfilled placeholder" — it is not.

## Lawful reporting form when the value is unknowable

The frozen law already answers this, and the answer is not discretion:

> "Unreached stages and metrics are reported as null WITH A TYPED REASON."
> "**Never** a fabricated zero or a fabricated PASS."

So the correct publication for this account is:

```json
{ "account": "path-level opens", "value": null,
  "basis": "OS layer, compiled pyreadstat 1.3.6 extension, no lawful unprivileged interposition on the bound surface",
  "reason": "UNOBSERVABLE_ACCOUNT__NO_LAWFUL_MEASUREMENT_MECHANISM_AT_ANY_AVAILABLE_LAYER",
  "near_miss_not_substituted": "python_level_opens_measured_2_per_decode" }
```

The obligation does not become optional. It becomes a **typed absence**, and the near-miss is
disclosed rather than promoted. Note that a fabricated zero is forbidden for the same reason
a fabricated count is: both assert a measurement that was never made.
