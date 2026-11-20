# P0 R3 finite handoff — native-stream court and actual two-estate cold admission

## Exact base

`3eee662d509fd78bc93d3ea26c3058d3199c960f` on
`agent/pyat-p0-two-saved-waves-native-i03-20261120-r3`.

## Tests

- New native-stream regressions: **8/8 PASS**
- Existing ANVIL-stream metadata tests: **18/18 PASS**
- Combined: **26/26 PASS**, no failures, no skips
- JUnit and logs in this directory.

First fault: the sparse checkout lacked the committed R2 typed-decision fixture,
so the first run was 24 PASS / 2 FAIL. The exact committed blob was restored
from the same HEAD (`git show HEAD:<path>`), and the complete rerun passed
26/26. This was a sparse-fixture checkout fault, not a sourcefree code failure.

## Actual saved estates

Both exact unmodified saved estates were opened sequentially through the new
native-stream admission, under the existing scoped R2 MainMac analytical
decisions and a live exact-current guard re-read on every check:

| Wave | Cold bridge admission | Governed issued query | Native I03 | Discovery | Downstream |
|---|---|---|---|---|---|
| SRC04 Arab Barometer Wave 1 | `VERIFIED` | `QUERY_NOT_ISSUED` | `NOT_ATTEMPTED_NO_LAWFUL_ISSUED_QUERY` | `NOT_ATTEMPTED_NO_COMPATIBLE_AUTHORITY_PATH` | `NOT_REACHED` |
| SRC16 GSS1972 | `VERIFIED` | `QUERY_NOT_ISSUED` | `NOT_ATTEMPTED_NO_LAWFUL_ISSUED_QUERY` | `NOT_ATTEMPTED_NO_COMPATIBLE_AUTHORITY_PATH` | `NOT_REACHED` |

The cold admission verified the independent stream identity, full member bytes,
Parquet body/locator schemas, family/footer counts and event/locator row-group
parity. No original `.sav` source was opened, rebuilt or reprojected. No
respondent values were emitted and no sensitive counts or private paths were
published.

## Why I03 did not execute

No lawful issued QUERY exists for either saved stream. The existing #1084 v2
issuer requires its original frozen bundle, SourceInventory, GrammarPolicy,
ScientificFrontier and a genuine eligible/supported compiled operation. Those
are absent for these saved streams. The R2 user decision is analysis permission,
not a scientific issuer decision. There is no query/predicate/authority
artifact in the held R2 custody. Inventing one would be a fake compiler/issuer;
therefore I03 stays at `QUERY_NOT_ISSUED` and no evaluator call was made.

No compatible exact discovery authority/path is present either, so no discovery
was run. R2 permission alone does not mint one.

## Next owner action

R03/scientific compiler-issuer owner: produce an exact lawful issued
QUERY/predicate/authority bound to each stream source/release/universe, or issue
a typed no-query hold. Discovery owner: supply an exact compatible discovery
authority/path if discovery is intended. Then the same P0 worker can rerun the
first actual I03, followed by I05/Batch/S04/DHIKR/FF01/C4–C6.

No PR #1185 branch, protected ref, source, grant, rebuild, extra wave, provider
or schema was changed.
