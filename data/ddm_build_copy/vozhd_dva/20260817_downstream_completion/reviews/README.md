# Vozhd Dva Reviews

This directory contains the control-room assessment of returned Rabochii work.

Worker self-report is evidence, not acceptance.

For each returned assignment, Vozhd Dva should assess:

1. scope compliance;
2. assignment completeness;
3. preservation of upstream authority;
4. satisfaction of downstream obligations;
5. semantic information loss;
6. interface compatibility with neighboring prongs;
7. test/evidence sufficiency;
8. newly exposed cross-hooks or blockers;
9. integration consequences.

## Terminal review states

- `ACCEPT`
- `ACCEPT_WITH_FOLLOWUP`
- `RETURN_FOR_FIX`
- `DEFER`
- `REJECT`

An accepted worker result is not considered synchronized until any cross-prong consequences are reflected in `integration/` and the current-state snapshot.
