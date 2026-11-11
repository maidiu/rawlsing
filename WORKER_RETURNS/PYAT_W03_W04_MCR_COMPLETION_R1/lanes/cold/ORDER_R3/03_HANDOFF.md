# CC-F01 handoff

Status: `DELIVERED_PENDING_RECEIVING`.

- Exact repair: cold respondent groups now sort row indices by the frozen event
  ref key, matching eager `_compact_public_objects` order.
- Streaming memory economy preserved: only small integer row tuples are sorted;
  no full event graph, selector lane or compressed body duplication was added.
- Existing historical RED and prior W04 F01/F02/F03 repairs were not reworked.
- CC-F02 (benchmark cold scenario), CC-F03 (CI path selection), CC-F04 (proof
  sidecar), and CC-F05 (frozen contract validator) remain outside this lease.
- Final same-SHA all-12 code and economic receiving, final 100k benchmark and
  protected adoption remain mandatory and are not claimed here.
- No source/native/science/actor/protected merge; PR895 untouched.
