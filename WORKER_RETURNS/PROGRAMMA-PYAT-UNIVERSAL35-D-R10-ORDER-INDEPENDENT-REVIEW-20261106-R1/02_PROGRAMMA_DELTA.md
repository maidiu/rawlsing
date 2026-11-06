# PROGRAMMA_DELTA — D r10 refused-artifact ordering

| Field | Delta |
|---|---|
| `VERDICT` | **ACCEPT_SCOPED_ENGINEERING** at target `70c9ae19…`, code `0b38f3c7…`, prior `0d48fc73…`, prior G `e693359b…`; published review head reported in final delivery. |
| `ARTIFACT_ORDER` | PASS_SCOPED: actual wrapper publishes only after final decision; changed `A,A,B` leaves no new artifact and preserves an existing valid artifact unchanged; no staged temp. |
| `TRANSPORT_PERMISSION` | PASS_SCOPED: no state-root-only envelopes; explicit ceiling unchanged; missing/empty/invalid permission fails before artifact. |
| `NO_DROP` | PASS_SCOPED: 30 facts / 30 envelopes / 15 operations / 18 candidates; no partial new output on failure. |
| `POSITIVE_SUPPORT` | NOT_RUN/MISSING: 30 one-target facts -> 30 typed E arity refusals, 0 profiles, structural grant false; 2-target joint producer absent. |
| `FAILURES` | Missing query/permission and forced atomic-replace failure preserve prior valid artifact; missing replay remains typed E refusal. |
| `PRESERVED` | Changed actual sourcefree input identity proof; E codec `6acba005…` exact; plan/frontier/route floors retained. |
| `LIMITS` | Actual original facts, authentic E handshake, A/C scale, full estate and 650 s NOT_RUN; no code repair or authority promotion. |
