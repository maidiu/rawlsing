# CC-F01 exact repair — cold respondent event order

Status: `DELIVERED_PENDING_RECEIVING`.  This is a bounded repair of the
independent `REVISE` at `2959dda3c95b05db40a399d6d746401f434f5a38`, not whole
W03/W04 or 12-ID acceptance.

- Intake head: `26f70635e8493c7759fa087b17da269104bd8922`
- Implementation commit: `f9aedf8e2b570174881cef627dc6a24b78031ed7`
- Finding: CC-F01 (P2), cold/eager event sequence parity.
- Production write: `rawlsing_next/_pre553_w03_cold_compact.py` only.
- Test write: `rawlsing_next/tests/test_pre553_w03_w04_cold.py` only.

## Exact defect

`ColdCompactBuilder.finish` built each `_RespondentEvents` from
`tuple(rows)` in physical stream insertion order.  The eager
`_compact_public_objects` path builds groups from `release.public_objects`,
which is exact ref-key order.  The real I03 selector reads
`public.by_respondent` directly, so the cold selector/yield sequence differed
even though aggregate facts and consumer material matched.

## Exact repair

`finish` now constructs each respondent sequence as:

```python
tuple(sorted(rows, key=lambda row: self.event_keys[row]))
```

This sorts only integer row indices by the already-frozen exact event ref key.
The selector/body lane, refs, semantic identities, topology, compressed bodies
and streaming memory economy are unchanged.  No new engine, oracle, semantic
rule or cache format was introduced.

## RED and GREEN

Independent review probe copied to `probes/cold_parity_probe.py` and run at the
intake head before the repair:

```text
event_sequence_parity = false
selector_yield_parity = false
selector_yield_differences = 3
consumer_material_parity = true
```

After the repair:

```text
event_sequence_parity = true
selector_yield_parity = true
selector_yield_differences = 0
consumer_material_parity = true
```

All three fixtures (`routed-ordered-repeated`, `missing-optional-weight`,
`valid-empty`) report exact sequence, selector-yield, public-object and full
typed I03/I05 consumer material parity.  Files:
`probes/cold_parity_probe_RED.json`, `probes/cold_parity_probe_GREEN.json`.

## Boundary

No original35/SAV/DTA/DB/source bytes, no source/science/native/actor/FF/N11/
Sorok issuance, no protected merge, no PR895 edit, no 100k benchmark, no
install/model/provider/account/effort change.  CC-F02 through CC-F05 are outside
this lease and remain with their owners/HQ.
