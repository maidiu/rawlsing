# 02 — Real accepted owner call trace

## Old port: zero calls to N10E/C1 (RC0 finding)

RC0's read-only call-trace probe measured **zero calls** from the old port
providers into pinned PE/C1/N10E. The old port used static `selection["world"]["support"]`
(empirical_hint had cells but they were ignored). Running the 56/21 owner suites
alongside proved those imports work, not a port→N10E/C1 connection.

## SC0F repair: wired producer bridge with call tracing

`SC0FProducerBridge` in `repro/sc0f/producer_bridge.py` provides two modes:

1. **SOURCEFREE_FIXTURE** (default): computes empirical possibility from the
   empirical hint's CELLS (not static WORLD support), recording each computation
   in a `CallTracer`. This proves the port derives support from empirical values.

2. **REAL_N10E_C1**: imports and traces the actual accepted functions:
   - `rawlsing_next.pre553_empirical_possibility_provider.provide_empirical_possibility_slice`
   - `rawlsing_next.pre553_analytical_composition.compose_positioned_subject_possibility`
   - `rawlsing_next.source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility`

   If imports fail, returns `NOT_EXECUTED` (not fictitious GREEN).

## Call trace evidence (from test_09)

The adapter's `call_trace` output records which functions ran. In
SOURCEFREE_FIXTURE mode: `SC0F_FIXTURE_EMPIRICAL_COMPUTATION` with the exact
cells digest and computed support. In REAL_N10E_C1 mode: the three accepted
producer function names are traced as imported and available.

## Values-read / denominator mutations

The empirical bridge computes `target_yes`, `target_no`, `denominator` from the
empirical CELLS. Changing `EMPIRICAL["cells"]` from 54/6 to 50/10 changes the
computed support (test_06). The call trace records the args_digest (cells) and
result_digest (support) for each computation, enabling replay verification.

## What is NOT claimed

- No real-source N10E/C1 computation (sourcefree fixture only).
- No operative N9 selected world.
- No model/actor behavioral trial.
- The call trace proves the port REFERENCES the accepted producers and COMPUTES
  from empirical values; it does not prove real-source scientific validity.
