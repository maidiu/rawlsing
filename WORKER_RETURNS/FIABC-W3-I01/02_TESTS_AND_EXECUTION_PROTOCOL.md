# FIABC-W3-I01 — Tests and Execution Protocol

## Status in this worker

Tests added: yes.  
Tests executed here: **no**.

Reason: this commission is restricted to GitHub/browser repository tools. That surface exposes file/ref/status operations but no shell Python/pytest runner. The commission also forbids local-machine Codex and measured P2X execution. The current implementation tip has no attached GitHub CI status checks to reuse as execution evidence.

No PASS result is fabricated.

## Focused syntax/test commands for the integrated checkout

Run from repository root:

```bash
python -m py_compile   rawlsing_next/pre553_diagnostics.py   rawlsing_next/tests/test_pre553_diagnostics.py
```

Then:

```bash
python -m pytest -q rawlsing_next/tests/test_pre553_diagnostics.py
```

Expected collected I01 cases after parameter expansion: **21**.

## Neighbor regression command

Because I01 consumes I03 and is hostile-tested against I05 and I04 boundaries, run:

```bash
python -m pytest -q   rawlsing_next/tests/test_pre553_empirical_query.py   rawlsing_next/tests/test_pre553_discovery_exact.py   rawlsing_next/tests/test_pre553_structural_admission.py   rawlsing_next/tests/test_pre553_diagnostics.py
```

## Optional PRE553 regression sweep

After Wave-3 fan-in, before any P2X measurement:

```bash
python -m pytest -q rawlsing_next/tests/test_pre553_*.py
```

## Acceptance conditions

The I01 focused test is acceptable only if all cases pass without changing expected typed states or weakening existing I03/I05/I04 guards.

Specifically:

1. perfect binary association yields entropy reduction ~= 1 bit, MI ~= 1 bit, NMI ~= 1, Cramér's V ~= 1, and exact rational uplift/lift;
2. replaying unchanged exact determinants yields the same product and replay refs;
3. changing a confidence determinant changes product/replay identity and cannot satisfy replay against the old product;
4. missing confidence determinant refs fail closed rather than defaulting effective-N or another component;
5. negative I03 states produce no numerical diagnostic;
6. underpowered state remains typed and determinant-bound;
7. non-joint positive facts are NOT_APPLICABLE rather than zero;
8. malformed claimed joint input raises an integrity error;
9. wrong release, missing authority, or fact/query mismatch fail closed;
10. diagnostic material cannot be made into EmpiricalFact truth;
11. the real I04 admission service rejects a diagnostic product as its empirical fact input;
12. the real I05 authority verifier rejects computed diagnostic score control of frontier reachability;
13. reporting and non-controlling ranking remain the only accepted diagnostic uses.

## Explicitly forbidden during this test step

- measured P2X;
- source-semantic regeneration;
- effective-N guessing/defaulting;
- candidate-specific diagnostic semantics;
- modifying frozen candidate identities;
- treating test agreement as the independent parity oracle.

The later Wave-3 integrated qualification and measured-court gates remain owned by HQ/Q02 and the other assigned workers.
