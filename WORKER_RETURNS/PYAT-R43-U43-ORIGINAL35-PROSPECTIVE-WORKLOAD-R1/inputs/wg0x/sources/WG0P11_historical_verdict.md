# WG0P11 independent clean replay — final verdict

**INDEPENDENT_SELFCONTAINED_NATIVE_COURT_PASS — bounded sourcefree transport replay.**

The completed P10 artifact at **`c9f876788dea5770563f0c1ac3354ec745cfa59c`**
works from a fresh isolated checkout with no manual repair overlay. D1–D5 are
closed by the unchanged, independently frozen acceptance tests. The historical
five unconstructible controls and two characterisation failures remain NOT GREEN.
This is an independent reviewer finding, not HQ acceptance or source/issuer adoption.

## Independence and exact checkout

Commission/startup: `75a4c331124ffd762e1a7f900b0a9c73897f9bd3`.
Phase A oracle, original hashes and independent tests were pushed first at
`cb5484c96325e06b981dea22207e4dadc3d83558`, while P10 still had no implementation.
Phase A baseline evidence was banked at `bb48510ccff801c417b216890bfc0363e51b3f99`.
The frozen oracle and test bytes remain identical to that first remote commit.
The earlier HOLD is superseded by this actual Phase B execution.

Direct `git ls-remote` identified the completed P10 head above, and a final check
confirmed the same head. The decisive isolated clone is
`/tmp/wg0p11-remote-filtered-p10`, fetched directly from GitHub with
`--filter=blob:none --no-checkout`, then sparsely checked out at that exact
commit with all 1,272 artifact files materialized. Initial status was empty;
there are no local-object alternates or inherited worktree files. All runtime
subprocesses had further Git fetching disabled. Host: Darwin x86_64,
Python 3.11.3, pytest 9.1.1.

The published bootstrap reads the frozen register at historical Git commit
`bec9a128922e4e431ce2ed862aa7802c902813ed`. Repository Git history is therefore
part of this transport's runtime contract. In the direct remote clone that
historical read matched the already-staged original bytes, before the replay
with Git fetching disabled. The tested contract retains this Git metadata.
The earlier detached local-object clone was an initial complete screening;
its separate evidence remains in `phase_b_p10/`. The decisive replay and final
completion audit are in `phase_b_remote/`.

Only published candidate entrypoints prepared the fixture:
`python3 -B repro/wg0p10_regenerate_cold.py`, then
`python3 -B repro/wg0p8_publication.py run`. Versioned directory markers provide
the required parents at checkout. The published regeneration script provisions
the owner and runs genuine crash/resume processes; the published conftest resolves
the repository-relative cold path. No manual mkdir, owner reconstruction, file
restore or path edit was used to make positive tests pass.

## Independent custody evidence

- **187/187 original source preimages** match the Phase A freeze for SHA-256,
  Git blob and length, including **11/11 restored inherited files**.
- Source manifest: `2e7d47d2a14fe1fec12fd574c1183fadf50ee25b6f10a62ffae8858e29885418`.
- Repaired P5: SHA-256 `89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643`,
  Git blob `62895078908ff748771da9a9fbcec6b36d34a803`, actual version
  `WG0P6_RELEASE_VIEW_SOURCE_SNAPSHOT_BINDING@1`, loaded from the nested repaired path.
- **1,272/1,272 tracked P10 artifact files** were independently hashed in the
  initial clean clone and matched directly against the immutable P10 Git tree.
  No symlinks. The missing WG0N verdict matches SHA-256
  `839adc7508fcd81bd0a59af8f0fc8793b8ea075c80661683b776124cb90a228b`
  from `6cd28b429504ad47e1bbc0fbcc6c4ef91db59ccd`.
- All original frozen test and oracle preimages survive. The two changed original
  Python files are the disclosed transport bootstrap and publication runner;
  the D4 conftest and cold-regeneration script are added transport. Productive
  P5 and frozen tests are unchanged. P10 also discloses D6: the runner now sets
  the existing required adapter environment variables.
- Final custody verification passed after all execution and hostile stimuli;
  all 187 original inputs and all tracked P10 Python source bytes remain exact.

See `02_CLEAN_CLONE_MODULE_AND_INPUT_SHA.json` for the full closure and deltas.

## Actual fresh tests, not inherited tallies

| Court | Actual result |
| --- | --- |
| WG0O original authority seam | 17 passed |
| WG0Q authority-body/epoch | 36 passed |
| Mandatory inherited | 236 passed: 33 + 65 + 3 + 55 + 80 |
| Fresh source-view | 42 passed, no teardown errors |
| Pointer forgery in a new process | 1 passed |
| Published transport guards | 9 passed |
| Immutable independent acceptance suite | 6 passed |

The published native runner accounts for **331 passed / 0 failures / 0 errors /
0 skips** (17 + 36 + 236 + 42). Transport9 and pointer1 are additional courts.
The six independent acceptance checks include another execution of fresh42 and
pointer1; those reruns are not counted as additional distinct scientific cases.
Real JUnit, commands, exits and stdout/stderr are in
`03_ALL_ACTUAL_FROZEN_NATIVE_AND_COLD_JUNIT/phase_b_remote/`.

The same six acceptance checks gave **1 pass / 5 failures** on the defective P8
baseline before P10 was available. Against P10 all six pass without changing
one test byte. D1 accepts the exact repaired module; D2 observes a newly written
atexit receipt; D3 has no directory/teardown failure; D4 executes the unchanged
pointer test against a genuinely regenerated owner; D5 verifies the exact missing
historical verdict. Twenty-four newly observed import audits, including the
fresh cold-resume process, identify the native modules. Archived receipts were
excluded from the fresh-audit count. The abrupt-exit crash intentionally does not
run atexit callbacks.

## Native outputs and true cold OS boundaries

The raw authority receipts independently show **42 supported cells / 4 I03** for
pristine P1, own-identity P2 and identical-body P4. All have effects SHA-256
`4b9d03246167c93df6dde8d590fac33c24c51ef158d60abd8ee33601ca059550`.
P3 replay returns the same cells/receipts with **0 new I03**. The original
frontier remains **25 = 3 PRODUCED / 16 HELD / 6 INADMISSIBLE**; the ordinary
conditional remains yes1/no1 over R2 and R3, denominator2.

The published cold regeneration actually exited **23 then 0**, PIDs
**66149 / 66162**, with **1 then 2 I03**. Both processes used the original
three-unit manifest `bcd255228ef35edcb9b59436b76e1eb78947c07180f2936779572f510981c140`.
The original native `UnitExecutionReceipt` preimage is restored byte-for-byte,
receipt hash `caac243fc25c521acc10b2e082b55bdb854921dff8f730680d82eeaf2dcabcbd`.
Measured file-fsync, replace and directory-fsync calls are retained. The original65
suite separately made a genuine pair, PIDs **66505 / 66516**, exits **23 / 0**.
These prove process-death recovery; they do not prove machine power-loss durability.

Fresh pointer-forgery PID **66616** differs from crash PID 66149. It reports
`IdentityError`, **0 new I03**, 0 restored receipts, unchanged owner journal and
custody, and the same three-unit manifest.

## Hostiles and historical limits

All **40 authority negatives** (11 original + 29 new) were independently checked
from this clone's actual receipts: no supported original fact served and zero
new I03, including wrong epoch and foreign authority. Typed exceptions/HOLDs are
recorded per case. This does not invent an issuer from a matching source hash.

Supplementary actual-source probes omitted a restored input, changed its bytes,
and replaced repaired P5 with the pristine direct module. In every case both
verifier and bootstrap exited **86**, before even the first payload statement,
so no payload I03 occurred. Each hostile file was restored to its exact initial
bytes, with successful custody verification between probes. These deliberate
attacks happened after positive replay; they were not repair overlays. Their
supplementary driver was written after P10 inspection and is not represented as
part of the pre-P10 frozen test set.

Unmodified historical tests were rerun against P10: **five construction failures**
remain UNCONSTRUCTIBLE/NOT GREEN; the characterisation file remains **1 passed /
2 failed** with `COMPLETE_BOUND_SOURCE_DESCRIPTOR_CHANGED`. These seven failures
are required preserved historical statuses, outside the passing mandatory court.
They are retained in JUnit without skip/xfail or relabelling.

No original surveys, U/E_pre, independently signed institutional issuer,
source-artifact revocation grant, new temporal-owner rule, N11/N12/OC05,
V3/actor adoption, production grant or HQ self-adoption is established.
No required Phase B execution remains unrun; the explicit non-grants remain.
