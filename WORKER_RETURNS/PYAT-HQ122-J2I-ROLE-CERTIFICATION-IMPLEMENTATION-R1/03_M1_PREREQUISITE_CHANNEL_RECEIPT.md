# HQ122 J2I — M1 PREREQUISITE CHANNEL RECEIPT

Builder:

`build_j_family_item_role_channel(...)`

Channel id:

`j_family_item_role_vector`

Channel kind:

`PRE553_J_FAMILY_ITEM_ROLE_VECTOR`

Exact relation kinds:

- `GOVERNED_FAMILY_ITEM_ROLE_FOR_COMPONENT_SET`
- `ROLE_VECTOR_PREMISE_FOR_J_CERTIFICATION`

## Bound material

The channel binds:

- exact role-vector ref and serialized exact preimage;
- role contract ref;
- mapping contract ref and exact per-component mapping refs;
- exact replay-contract/ref closure;
- exact adopted role authority;
- exact current subject/family authority;
- exact per-value authority refs;
- exact governed component IDs/order;
- exact six-token vocabulary/version;
- mapping mode;
- role-vector coverage proof hash;
- J-family-role semantic ceiling.

## State law

`SATISFIED` requires exact subject, component-set/order, role contract, role authority, one-to-one coverage, all required bindings VALUE, every VALUE digest resolving to the exact six-token vocabulary, required mapping closure, and replay-root inclusion in the exact replay refs.

Missing/unresolved required role or missing required succession mapping -> `UNRESOLVED` / `J_ROLE_PREREQUISITE_UNRESOLVED`.

Denied/noncomparable/authority mismatch/duplicate ambiguity -> `BLOCKED` / `J_ROLE_PREREQUISITE_BLOCKED`.

Unknown positive role token -> `INTEGRITY_FAILURE` / `UNKNOWN_ROLE_TOKEN_CONTRACT_FAILURE`.

Component-set/order mismatch -> `INTEGRITY_FAILURE` / `J_COMPONENT_SET_MISMATCH`.

Serialized/replay mismatch -> `INTEGRITY_FAILURE` / `J_ROLE_VECTOR_REPLAY_MISMATCH`.

Generic M1 now preserves these exact channel-local terminal reason codes when the prerequisite terminates before family-validator dispatch.
