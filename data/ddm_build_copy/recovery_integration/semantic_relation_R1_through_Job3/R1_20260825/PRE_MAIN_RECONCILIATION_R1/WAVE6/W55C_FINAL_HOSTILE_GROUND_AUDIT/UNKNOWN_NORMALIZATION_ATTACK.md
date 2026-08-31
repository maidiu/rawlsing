# Unknown-normalization attack

Central-state ruling: PASS.

N036/K001-K010 and OBL026/046/047 preserve unknowns as sweepable `UNKNOWN_REQUIRES_SYNTHESIS`; unknown need not be resolved immediately and cannot be merged by label/theme resemblance.

Machine ruling: `BYPASS_FOUND`.

The validator accepts any nonempty obligation `disposition`. It therefore cannot mechanically prevent a packet from converting an unknown obligation into `NOT_IMPORTANT`, `NOT_FOUND`, `CLOSED`, `FALSE` or `SUPERSEDED` without competent synthesis.

Five representative normalization bypasses are recorded. The defect is not central-state visibility; it is unchecked disposition semantics.
