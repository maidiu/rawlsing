# Universal35 D r11 — actual joint-engine/E connection review

**VERDICT: REVISE** at frozen D head `e4f336972c6c341451ba6e511a2f3c428fc7fb5f`.

- Code: `ca4ef1aa207859a7c93493a39f3a3571564df710`
- Prior head: `70c9ae198948d5ede69064eecbf8db2643317518`
- Prior G: `fce7443d21bf9f26bc8d4eb576ddb4a314a0408b`
- Review branch: `codex/pyat-universal35-d-r11-joint-review-20261106-r1`
- Published review head: the commit containing this directory; exact SHA reported in final delivery.

## FINDING

### Blocking — E profile has the F2 conditioner and target reversed

The actual two-target engine fact is genuine: 3 existing facts (2 one-target,
1 two-target), 4 joint cells, raw numerator/denominator 12/12, and an exact cold
E `CONDITIONAL_SUPPORT_PROFILE`. But the profile does **not** preserve the
selected F2 estimand.

Observed asymmetric sourcefree fixture:

- plan F2 target `fixture.B`, conditioner `fixture.A`;
- helper builds targets `(B, A)` and query target refs `[R56R02-B, R56R02-A]`;
- E default conditioner = first target (B), target = second (A);
- cold profile: condition B=0 denominator 8 target A `{0:6,1:2}`;
  condition B=1 denominator 4 target A `{0:0,1:4}`.

That is P(A|B). The requested F2 is P(B|A): condition A=0 denominator 6 target
B `{0:6,1:0}`; condition A=1 denominator 6 target B `{0:2,1:4}`. Calling the
existing API with explicit correct roles (`conditioner=A,target=B`) returns a
typed refusal because the query target order is already `[B,A]`. The cold
envelope cannot recover the requested direction. This is not a preserved F2
estimand.

The helper also sets `conditions=()` (an unconditioned JOINT fact), chooses the
first eligible F2 pair and `inventory.measure_plans[0]`, and provides no
caller-supplied target/conditioner/value/measure selector or accounting for
other requested F2 pairs. An unconditioned JOINT may be a legitimate existing
support producer, but it cannot be relabeled as the requested conditional.

### Other axes

- **Engine producer: PASS_SCOPED.** Existing `make_operation`/JOINT and current
  `compile_governed_frontier`/`execute_governed_frontier` produced the 3 facts;
  no marginal assembly or new compiler.
- **Numerical/risk direction: FAIL.** Condition/target order and denominators are
  reversed; explicit correct API roles do not yield the F2 profile.
- **Generic request selection: INCOMPLETE.** First-pair/first-measure selection,
  no conditions, no caller query/all-pair accounting.
- **Cold consumer: MECHANICAL_PASS / SEMANTIC_FAIL.** Cold CLI returns the
  two-target profile; 1-target envelopes remain typed arity refusals. Missing
  permission, tampered replay and tampered joint cell fail closed.
- **Changed input/restore: PASS from the focused R11 test.** Changed source cell
  changes fact refs; exact restore returns original refs.
- **R10 ordering: PASS_PRESERVED.** The joint helper consumes an already
  qualified bundle; it does not introduce source admission or alter the accepted
  final-decision/artifact ordering.

E codec blob remains exactly `6acba005…`. Actual original facts, authentic E
handshake, all35/native/S3/science and protected acceptance remain
**NOT_RUN/HOLD**. No original data, 650 s/full-estate run, code repair, or
A/C/E/guide/progress/controller edit.
