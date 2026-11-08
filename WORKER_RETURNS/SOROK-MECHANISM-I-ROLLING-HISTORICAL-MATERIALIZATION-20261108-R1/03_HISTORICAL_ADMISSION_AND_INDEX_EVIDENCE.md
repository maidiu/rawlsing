# Historical admission and index evidence

This trace uses the actual P4 owner and inspector on sourcefree fixture data
at published implementation `b9880a4568605ccce703a611acdf428dccaa925f`.
The mock provider receipt is in [02](02_MODEL_PROVIDER_AND_JOB_RECEIPTS.md).

| State boundary | P4 owner snapshot hash |
|---|---|
| Opening after durable demand | `f26ceeff198e0a9a5c0b15e2681977a6af6b45a634d20d40183e0685cc12462a` |
| After background admission, before inspection | `d1a4b53288adadded971b4cbc40025f54dff46a169a668300c498925b132bfda` |
| After actual inspection event | `1e365b7bd5f4d8da9b76e7e37677af845f8847a71b1d3bd76dd3a22431885cfc` |

All three use clock 230, branch `first_session`, root
`3bcb21fc22df3255269382ad249f706dd6dd5378cb886af26542991ff516a4f7`.
The admitted group `physical` returned `INDEX_READY` and moved the target
to version 2. Admission used world readset
`8d2f1052114f53db6cddbb6960b9d5abd2bfc62c1a901a931ef00fe2f09f7f7d`.
The actual inspector retrieved `texture=matte` with ID
`history-fact:bb52b812d27e032fdb1e958a85cf0d2b55b300d93a837021de3180f41d6d25ce`.
Reopening again and repeating the inspection read 300 times returned the
same complete response. The index exercised here is the owner's target
physical-predicate map.

The owner test also offers a contradictory replacement for an existing
surface condition in a separate group alongside a compatible texture.
Only the compatible group is admitted and the result is `PARTIAL_HELD`.
The admission evaluator separately exercises H3 actor effects and H2
without eligible slack. These are controlled tests. Actor/history reverse
queries and branch-shared index replay still require evidence.

The owner now records an event-to-target reverse index in the same
checkpoint as target admission. P4's actual foreground surface consumes
it through `HistoricalWorld.visible_surfaces`, using only the current
observer's perceived event IDs and filtering by location. Checkpoints
written before this index derive it from canonical target parents on read.
The foreground test binds an artifact and a collection to one actual
movement event, verifies both are returned, removes the derived index in
the fixture to verify rebuild parity, and leaves the location to verify
neither remains visible. It does not establish actor-history linkage.

The received BP4 fork copies checkpoint bytes. The historical owner now
recognizes a verified direct fork and starts an empty child history view
when the copied resource belongs to its parent. The fork test confirms the
child cannot read or lease the parent's target or in-flight job, can admit
a distinct branch-local target, and recovers that child target after a cold
open. The existing S39 reader accepts the sealed inherited generation
receipt only after the store verifies a direct fork and its shared prefix.
This proves branch-local isolation on the received direct-fork path.
Shared pre-contact historical writes and deeper fork chains remain open.

The same proof now covers a second fork and cold reopen. S39 and the
historical owner reuse one C12 prefix check that verifies each recorded
parent-child edge. The nested branch receives its own target ID and cannot
read either ancestor's historical jobs. This does not authorize shared
pre-contact historical writes.

A P4 inspection can now select a visible physical predicate with
`inspect-particular TARGET --property color`. After the initial job settles,
the owner records a durable follow-up for a selected missing property in
the inspection transaction. A repeated request reuses its job identity.
The model receives the prior physical facts by exact admitted reference and
the selected predicate. The owner holds a group that proposes a different
property. This is an explicit T3 physical-depth request. A newly discovered
historical link that independently triggers T2 remains unverified.

A second ingress now uses the existing S46 interval producer. A confirmed
world receipt with one completed unit binds an occurrence-scoped artifact
and its job before P4 publishes the turn. The owner checks the exact
source-owned REPAIR event and retains the event's coarse resolution. It
does not infer a durable workpiece identity, provenance, or observer access.
The focused test runs the actual repair without inspection, verifies
deduplication and wrong-hash refusal, and reopens the target and job.
This proves independent world activity can introduce a target. Whether
an independent activity can consume newly materialized depth is separate
and remains unverified.

On reopen, the worker can recover a missed repair obligation directly from
the same branch's event journal and committed world checkpoint. Both must
agree on the event hash. The copied prefix of a fork is excluded. The test
commits an actual interval without calling the history adapter, closes the
owner, and reopens through the worker with no model configured. The target
and job are recovered and a repeated scan leaves the same job intact.

New repair-output leases carry one objective participation link in their
constraint packet. The actor is resolved from the performed event and
checked against the sealed root actor identities. The chronology record
binds the typed actor reference to that exact event as `PERFORMED_REPAIR`.
The packet carries identity and the observed role, with no actor-state
payload. H0 remains the write ceiling. Existing leased packets retain
their original digest inputs. The focused repair and provider tests verify
the exact actor and event references and unchanged authority ceiling.

The owner now persists the objective repair link in a reverse index keyed
by the existing actor identity. The trusted read revalidates the current
branch's target and original event before returning the link. The repair
constraint packet uses the same link derivation. The recovery test removes
the derived index and rebuilds the exact link from the committed journal.
No user-facing reader receives this reverse index.

Repair leases can now consume the reverse index. A later repair packet
includes at most two earlier verified repair links for the same actor
and branch. The selected links are sealed with that lease. They appear as
context only, outside the packet's admissible parent references. The
two-repair sourcefree test uses real S46 actions with controlled stock
replenishment. It checks that the first repair is context and the second
repair remains the only event parent of its output.
