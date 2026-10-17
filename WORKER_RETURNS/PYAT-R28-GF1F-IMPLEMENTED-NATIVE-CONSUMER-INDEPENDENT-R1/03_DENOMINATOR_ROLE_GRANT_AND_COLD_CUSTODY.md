# GF1F — denominator, role, grant and cold custody

## Denominator custody

The consumer decodes the ordered 2x2 `conditional_count_profile` into
`support_vectors[c][t] = joint_support_count` and derives
`condition_states_with_positive_denominator` from each row's declared
`condition_denominator_support`. `joint_support_total` is the sum of every cell,
and `eligible_joint_risk_total` is surfaced from the relation.

Independently verified across the 81-element universe: the produced
`support_vectors` equal the reviewer's own cells, the positive-denominator list
equals the reviewer's own row-total derivation, and the joint total equals the
cell sum. The classification uses `eligible_joint_risk_total <= 0` for
`UNDETERMINED_ZERO_SUPPORT_RISK`, a zero condition row for
`UNDETERMINED_NO_ELIGIBLE_RISK`, and otherwise the per-condition target winners.

Limit: a relation whose declared per-condition denominator disagrees with its
cell sum (and whose content hash was recomputed) is not cross-checked; the real
producer never emits one, and this is outside the commissioned
mutation-without-recompute attack.

## Role and direction custody

The consumer reads the relation's own ordered profile: `conditioner_state` rows
and `target_state` columns. For the real reverse X|Y operation the producer
issues a DIFFERENT relation under `REVERSE_PAIR_GRANT_ID` with
`operation_role_order="REVERSE_GRANTED"` and swapped conditioner/target refs;
the consumer computes from that relation's own order, producing a distinct
`separation_signature` (which embeds variable names and role order) and a
distinct `result_hash`. The forward relation remains
`FORWARD_NATIVE_ORDER`. The swap without the reverse grant is refused by the
producer, unchanged.

## Grant and permission custody

The consumer does not widen any permission: it carries
`producer_permission_ceiling` and `relation_permission_ceiling` verbatim, and the
relation's own `__post_init__` still refuses a relation ceiling that is not a
subset of the producer ceiling. The frozen producer remains the sole authority
for `REVERSE_PAIR_GRANT_ID` and for rejecting non-native role refs.

F2 non-copy: the seven computed consumer fields are absent from
`relation.as_dict()` and present in the consumer output. The consumer is a
genuine compute step, not a fixture or oracle echo.

## Cold custody

`repro/cold_child.py` rebuilds the whole 81-relation universe and runs the
consumer in a fresh OS process. Two runs produce bit-identical serialized
results with distinct PIDs; every separation class is exercised; the imported
consumer file is `gf1_pair_support_consumer.py` (sha256 `06dd484b…`). The
reviewer's independent court also runs the reverse operation through the real
native producer and the real baseline relation through the full native chain.

## Source identity

* `gf1_pair_support_consumer.py` sha256
  `06dd484b0e9b4b2c9fb0a1583453ac7ffa8c052135304eaaee167a34127cb402`.
* Frozen44 test file sha256
  `2bbb54aa7b1ea990705fc6edf51895a2ea7ec6192abd90acf062940aeff87ef5`
  (byte-unchanged from GF1/GF1I).
* Frozen oracle sha256
  `c5bdc14aec82e7df042594d8f2df1d8130b89345d305de5f73830828a0257790`
  (byte-unchanged).
* The staged native closure and the sibling
  `generic_native_pair_relation.py` are unchanged from the GF1 R17 bytes.
