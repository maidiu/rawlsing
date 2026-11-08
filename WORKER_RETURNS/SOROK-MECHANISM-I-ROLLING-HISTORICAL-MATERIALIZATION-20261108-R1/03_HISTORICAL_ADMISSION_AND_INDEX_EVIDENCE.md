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
