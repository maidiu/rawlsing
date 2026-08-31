# Context-bloat hostile test

Ruling: `SCOPED_PROGRESSIVE_GROUNDING_WORKS`.

A fresh Vozhd can begin from Ground + `00_STATE_NOW.md`, sweep exact state/obligation/reintegration rows, then descend only into campaign/deep evidence relevant to the decision. `NEXT_ACTIONS.tsv` supplies a dependency-derived queue.

A properly commissioned bounded executor can receive a frozen decision and narrower context rather than rereading the whole history.

Therefore the architecture does not intrinsically recreate the context-window overload that motivated the Ground.

Important separation: the validator currently fails to verify the bounded executor's parent inheritance. Fixing that does not require making every bounded executor read the corpus; it requires verifying an exact parent receipt/ref and ceiling.
