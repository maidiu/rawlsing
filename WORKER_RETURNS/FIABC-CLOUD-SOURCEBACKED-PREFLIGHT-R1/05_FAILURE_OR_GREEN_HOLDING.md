# Failure / Green Holding

## Holding

**BLOCKED — no false green.**

Both exact source byte gates passed. The cloud court did **not** reach the real current candidate-neutral production functions because two independent execution prerequisites were unavailable:

1. the qualified runtime could not be reproduced; and
2. the only recent Library checkout located for this court could not be materialized as executable raw bytes.

The first unmet prerequisite is therefore:

`QUALIFIED_RUNTIME_UNAVAILABLE`

with an independent second blocker:

`CURRENT_EXECUTABLE_CHECKOUT_MATERIALIZATION_BLOCKED`

This is **not** `LIBRARY_SOURCE_MATERIALIZATION_BLOCKED`: both commissioned source carriers were successfully materialized and SHA-verified.

## Source admission passed

- LiTS-I: exact SHA `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- WVS7: exact inner SAV SHA `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

WVS7 was correctly admitted from `WVS Wave 7.sav.zip`; the loose inner SAV was extracted only in the cloud worker runtime and was never substituted from another source.

## Runtime failure

Observed cloud:

- CPython 3.13.5
- Linux/x86_64
- pyreadstat: missing
- pyarrow: missing

Required diagnostic-package runtime:

- CPython 3.11.3
- pyreadstat 1.3.6
- pyarrow 25.0.1

Required final attestation additionally requires Darwin/x86_64.

Exact CPython acquisition failed after three retries because the runtime could not resolve the GitHub release host. Exact package acquisition failed because pip could not resolve PyPI. No version substitution was made.

## Checkout failure

A recent `FIABC-QF1-qualification-checkout.zip` exists in Library, but raw materialization returned exactly:

`This Project file does not have an authorized raw-byte materialization path.`

Older materializable Rawlsing archives were inspected only as availability probes and were rejected as stale substitutes.

## Production-path classification

Because no real current production function was invoked, it would be false to classify this as a source representation, transport-adapter, legacy-dependency, physical-key-owner, launch-defect, or other production-path failure.

Those classifications remain **NOT REACHED**.

The historical dependency audit did establish that non-hermetic dynamic loading exists structurally, but it did not establish a new production defect. The latest physical-key repair is statically coherent: the legacy key primitive's critical hash dependency is byte-identical, and current typed rules are explicitly rebound to legacy keys inside a closed q301_2/q301_7 successor scope. Runtime provenance and real-source join remain unproved.

## Candidate boundary

Candidate A/B/C: **not run**.

Measured P2X: **not run**.

P3: **not run**.

Architecture selection: **not run**.

## Minimal unblock surface

No production repair is justified from this court.

The smallest lawful next execution environment needs:

- an executable checkout at exact dispatch head `7b38c22dd469735eed0b0c01c304a028dd3046cf` (or a proven descendant permitted by the governing launch law);
- CPython 3.11.3;
- pyreadstat 1.3.6;
- pyarrow 25.0.1;
- the already-admitted exact LiTS-I and WVS7 source bytes;
- import-provenance instrumentation that records `__file__`/module origin and blob identity for every historical module's participating `rawlsing_next.*` dependency before key-producing work;
- then the exact underlying current pre-candidate production calls, stopping before candidates.

No Darwin claim may be made unless the host is actually Darwin/x86_64.

## Terminal

`FIABC_CLOUD_SOURCEBACKED_PREFLIGHT_R1__BLOCKED__QUALIFIED_RUNTIME_AND_CURRENT_CHECKOUT_UNAVAILABLE__STOPPED_BEFORE_CANDIDATES`
