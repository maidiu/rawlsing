# R91 R05 R8 admitted-original closure return

**Verdict: CANDIDATE_FOR_INDEPENDENT_REVIEW. The R7 request-association rewrite defect is fixed; existing coordinator/native positives remain. Full live J42/P41/E04 remains NOT_REACHED.**

## Identity

- Startup `65f7acf226b7b21a1a8f3be23f14a93b3f3cfbcc`; same OpenCode author.
- Contract commit `06751e285c75f401cacb43cade74e22c3a1cb826`.
- Code commit `3db59b71ba771291f67e16a2575f6d28f9566fce`.
- Review read/preserved: `ea2920e73c4a064c94fb77937362a44871fc6602`.

## Repair

`TrustedNativeGraphCoordinator.execute` now uses the independently admitted slot
as the sole source for every retained original/slot association. Requests may
select admitted ids/base metadata but cannot rewrite M1 disposition, M2 release,
B5/currentness, target arity/order, discovery/recursive/E41 inputs or witnesses;
all such retained records come from admitted slots. The R7 dynamic alternate-M1
attack now refuses against the fixed original, while the original admitted
discovery/recursive/joint/E41 learned consumer restores.

Base source/release/query/predicate/consumer/model mismatch still refuses before
execution. Existing actual discovery/recursive/joint/E41 coordinator positives,
learned association checks, actual changed-evidence trusted refusal/restore,
typed axes/Z16 and prior custody remain.

## Evidence

Author: `40 passed`, 0 failed/errors/skipped, `8.34s`.

R05V R1/R2/R3/R5/R6/R7 exact probe replay: `23 passed`, 0 failed/skipped, `2.90s`.
This includes the R7 dynamic request-slot alternate-learned attack, which now
returns non-exact refusal.

## Blobs / scope

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_learned_world_composition.py` | `adbcc3316920c708580097dfe9f5aef4c9ca82fb` |

Only the authorized path plus own r8 return changed. Prior evidence immutable.

## Limits

Full live J42/P41/E04, original science/source, F6/F7, CI/prod, N11/N12, Sorok,
J52/W52 and R04.joined remain NOT_REACHED/HOLD. Local coordinator only; no
OS/R09 protection. Distinct review follows; no self-adoption.
