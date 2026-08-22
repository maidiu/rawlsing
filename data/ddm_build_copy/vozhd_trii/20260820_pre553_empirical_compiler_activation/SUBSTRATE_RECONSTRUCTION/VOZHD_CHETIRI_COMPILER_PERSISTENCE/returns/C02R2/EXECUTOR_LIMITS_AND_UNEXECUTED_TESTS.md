# Executor limits and unexecuted tests

The following were not executed because the controlling order permits measurement only against frozen authority and no such executable semantic surface was available in this cell:

- source-to-canonical-question/component mapping across all 35 sources;
- event-group and deterministic event-index constructors;
- semantic occurrence/slot constructor and C11 identity/content-hash/ExactRef projection;
- repeated-event authority and row-level repeated-event scan;
- routing/not-asked/inapplicable applicability semantics;
- post-carrier-deletion replay;
- source-backed C11 ingest or database/runtime/R5 validation.

The native SR03 manifests and narrow WVS7/LiTS I reads were completed. `NOT_TESTABLE_FROM_AVAILABLE_FROZEN_AUTHORITY` and `NOT_TESTABLE_UNDER_FROZEN_AUTHORITY` are execution statuses only. They do not imply impossibility, sparsity, nonderivability, or a persistence requirement.

No helper script was committed or used as a persistent artifact; the checked-in SR03 probe and two direct narrow-read commands were the only execution code paths.
