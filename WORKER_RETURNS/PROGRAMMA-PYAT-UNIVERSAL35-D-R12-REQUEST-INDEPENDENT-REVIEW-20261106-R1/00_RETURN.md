# Universal35 D r12 — exact F2 request/direction review

**VERDICT: REVISE** at frozen D head `cca6f2b0b46029b0684f539dd58b0f6b0e6a0d6d`.

- Code: `70d0f0fe45e0b383879ae625526cee6af03f2572`
- Prior head: `e4f336972c6c341451ba6e511a2f3c428fc7fb5f`
- Prior G: `e81c71c798c579227039f5b4b371159fc40fde73`
- Published review head: the commit containing this directory; exact SHA reported in final delivery.

## FINDING

### Joint support/direction: PASS_SCOPED

The conditioner-first direction is genuinely repaired in the actual engine:

- requested F2 `B <- A` produces `target_order=[A,B]` and cold E profile
  A=0 denom 6 target B `{0:6,1:0}`; A=1 denom 6 target B `{0:2,1:4}`;
- reverse F2 `A <- B` produces `target_order=[B,A]` and cold profile
  B=0 denom 8 target A `{0:6,1:2}`; B=1 denom 4 target A `{0:0,1:4}`;
- actual cold CLI returns `CONDITIONAL_SUPPORT_PROFILE`;
- engine result: 3 facts (2 one-target, 1 two-target), 4 joint cells,
  raw numerator/denominator 12/12.

This uses the existing `make_operation`/JOINT and current governed
compile/execute path, not marginals or a new compiler. Changed-cell/restore
focused proof passes; missing permission/replay/tampered joint cell refuse.

### Conditional request realization: INCOMPLETE / blocking

`_joint_frontier_for_pair` still sets `conditions=()` and ignores
`pair.conditioner_values`. The result mapping contains requested/conditioner/
target/joint refs but not the requested conditioner values or selected E profile
rows; `write_requested_joint_transport` likewise publishes no value filter.

Concrete probe: two explicitly requested F2 IDs with identical target/conditioner
but `conditioner_values=("0",)` and `("1",)` both return `status=OK` with the
**same joint fact/query ref** and the same full profile. The differently valued
conditional requests are not distinguished; the unconditioned supporting joint
table is being presented as both conditional estimands. That is the exact
documentation/claim mismatch: R12 says conditioner-value rows survive, but the
code does not carry or filter them.

The helper also selects the first raw `SAMPLE` measure rather than an exact
requested measure mapping; current sourcefree input happens to be RAW, but the
generic selection is not complete.

## AXES

- **Engine producer: PASS_SCOPED.** Existing JOINT engine produced the facts.
- **Numerical/risk direction: PASS_SCOPED.** Asymmetric B|A and A|B cold profiles
  have the correct condition/target order and counts.
- **Generic/conditional request: INCOMPLETE.** Requested operation IDs are
  explicit and one-per-ID, unknown/ineligible/weighted requests refuse, but
  conditioner values and selected profile rows are not preserved or filtered;
  two value-distinct IDs share one fact/profile.
- **Cold consumer: PASS_MECHANICALLY.** Two-target cold CLI profile and 1-target
  typed arity refusals work; semantic conditional-value realization remains
  incomplete.
- **R10 ordering/permission/no-drop: PRESERVED.** The joint helper consumes an
  already qualified bundle; prior artifact-ordering and permission proofs remain.
- **End-to-end: HOLD.** Actual original facts/E handshake, all35/native/S3/
  science and protected acceptance remain NOT_RUN.

No code repair or A/C/E/guide/progress/controller edit. No original data,
full-estate or 650 s run.
