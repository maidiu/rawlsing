# PYAT PE/SC0 — owner-bound source-free successor return

**Role:** independent PYAT PE/SC0 scientific-contract, producer/consumer and
issuer-security implementation engineer at I3+. Not the PE overlay author,
hostile reviewer, original SC0/N9/source issuer, PRE-MAIN integrator or own
reviewer.

**Branch:** `agent/pyat-pe-sc0-owner-bound-secure-successor-20261031-r1`

**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pe-sc0-owner-bound-secure-successor-20261031-r1`

**Write scope:** only `WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/`.
No production source, PRE-MAIN, original return or existing worker worktree was
modified.

## Fresh session provenance

| Item | Exact value |
|---|---|
| Harness | OpenCode CLI `1.18.34` |
| Agent | `build` |
| Model | `opencode-go/deepseek-v4.1-flash` |
| Variant | `max`; verified from running process argv `--variant max` |
| Session ID | `ses_e6f557010ffeVc8ejV937G5Ii9` |
| PID | `28096` |
| TERM_SESSION_ID | `DD7A2E8F-1277-4BB4-8EDD-27F566D94660` |
| Independence | Fresh session, not the PE author/overlay/hostile sessions, S7-FIX session, S7 session or S1/H1/H03 session |
| Runtime claim | Source-free pytest only; no original survey, respondent, actor, model-use, N9 or PRE-MAIN operation |

## Exact source cuts

| Artifact | Exact value |
|---|---|
| Branch startup | `d0342290b257f85c3e8931f9962e0aecabc84ed3` |
| Current PRE-MAIN rechecked | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| PRE-MAIN `rawlsing_next` tree | `1d88d3fbb1d18dadfda946d9cd7f309d84afa479` |
| Startup `rawlsing_next` tree | `1d88d3fbb1d18dadfda946d9cd7f309d84afa479` |
| Original PE | `e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65` |
| PE issuer repair | `9647d851a2d9b6e93e6711eec7a65325fb83aaa1` |
| Fixture overlay | `9c030bf4c239d2e14f2b5a8a02ff7b44906cd0c7` |
| Independent hostile review | `33b5363a20d44cfb42b3d1e86fdb9615710adb23` |
| Pinned PE module blob | `58484f4c3d9aae148d4116dcf00420c432aefcbd` |
| Original author court blob | `92f59875583bf513c6fdbcd3ad7fe2b49e45e212` |
| Original strict court blob | `d2fe653dadf94893b0fdfd268f36683f8dfed9af` |
| Original fixture blob | `c9674d5fe9d01621eda0fdb4a999391eba422d92` |
| Patched fixture blob | `83984e7b3719f350cb735a9d80b0a83560576a47` |
| Overlay implementation blob | `1e4c0e63b34192f77bf6554d43afb3c56828b29c` |
| Overlay `sitecustomize.py` blob | `3bac38dde1cc49d3a2f85a21ba7984410688d3ff` |
| Overlay fixture patch blob | `50eb18e5d2272f13b9cb41cad14464a8b5378e3e` |

**PRE-MAIN delta:** `origin/integration/pre-main-reconciliation-r1` is
`8e44ca9c751049d65e6def47600b5c073ee04b29`, four commits ahead of the branch
startup. The `rawlsing_next` tree is identical at both cuts
(`1d88d3fbb1d18dadfda946d9cd7f309d84afa479`). No merge was performed. The
delta is documentation/integration evidence only for this candidate.

## Finding

The published PE value-bearing overlay is not a secure successor. It closes
eight strict field-presence gaps at fixture scope but accepts altered world
values with an unchanged selection digest, accepts inconsistent denominators,
synthesizes refresh receipts without executing provider refresh, leaves
enriched fields outside the result identity, silently overwrites a
source-promotion flag, accepts a negative-status row with no scope, uses an
unrestricted test authority, and can be auto-injected through `sitecustomize.py`
and `PYTHONPATH`. Those attacks were independently reproduced at the exact
overlay cut.

The pinned original PE request/refusal law and the exact synthetic C1/N10E
geometry are recoverable. The overlay's world, refresh, issuer and enriched
identity semantics are not production-recoverable. The successor therefore
does **not** wrap or patch the pinned PE module. It builds a separate versioned
source-free contract around the current N10E/C1 producer and explicit
owner/provider dependencies.

## What was built

`SOURCEFREE_CANDIDATE_AND_VERSIONED_API/` implements:

- `PYAT_PE_SC0_OWNER_BOUND_SOURCEFREE_SUCCESSOR@1.0.0`, request schema
  `PYAT_PE_SC0_OWNER_BOUND_REQUEST@1`, receipt schema
  `PYAT_PE_SC0_OWNER_BOUND_RECEIPT@1`.
- `owner_bound_successor.py`: request, world, producer, issuer, refresh,
  geometry, consumer, receipt and replay contracts.
- `sourcefree_world.py`: source-free fixture world provider with an audited
  refresh invocation count and exact test-only scoped grants.
- `n10e_adapter.py`: explicit adapter over the actual current N10E provider
  (`pre553_empirical_possibility_provider.py`,
  `N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER@1.0.0`).
- `first_consumer.py`: in-candidate `TEST_ONLY_SOURCEFREE` receiving consumer.
- `fixtures.py`: deterministic source-free forward/reverse fixture assembly.
- `tests/`: positive, cold-replay, all-field identity and hostile courts.
- `README.md` and `evidence/`.

The candidate contract binds:

- selected-world owner, revision, full value-bearing world material and
  recomputed selection digest;
- the four clocks, negative-status source/risk scope and generated-binding
  echo;
- issuer identity, version, operation, target, risk, world owner and validity;
- both refresh receipts returned by actually invoked provider methods, with
  invocation audit counters and deterministic successor identities;
- the exact C1/N10E cell numerators, denominator, reduced exact fractions,
  role direction and target cell;
- the receiving consumer output; and
- the full provenance and epistemic ceiling.

Any mutation of a value-bearing field changes the receipt identity and the
result identity. A refusal has no world, no geometry and no consumer output.

## Preserved original courts and exact applicability

The original author and strict courts were run unmodified at the exact original
PE tree. They are **not** rewritten and not silently weakened.

| Court | Exact result | Exit |
|---|---|---|
| Original author 21 | **21 passed** | 0 |
| Original independent strict 13 | **4 passed / 9 failed** | 1 |
| Fixture overlay author 21 | **21 passed** | 0 |
| Fixture overlay strict 13 | **13 passed** | 0 |
| Fixture overlay fault court 9 | **9 passed** | 0 |
| Hostile predecessor 12-test court | **12 passed as attacks** | 0 |

The original 21/13 courts import the pinned module blob
`58484f4c...` from `e61a26ce...`; their exact applicability to the successor is
source-baseline/refusal-law evidence, not a drop-in successor acceptance. The
successor deliberately uses the current N10E/C1 producer and a new versioned
schema. The successor court preserves the same direction/denominator/refusal
distinctions and adds the owner-bound world, issuer, refresh, enriched identity
and consumer checks.

The hostile predecessor court passing 12/12 is **not** a success for the
predecessor: each test demonstrates an attack that the predecessor accepted.
The successor court makes the corresponding attacks fail closed.

## Successor test receipts

Commands were run from the repository root unless stated. Full logs and JUnit
XML are in `SOURCEFREE_CANDIDATE_AND_VERSIONED_API/evidence/`.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/SOURCEFREE_CANDIDATE_AND_VERSIONED_API/tests
# 33 passed, exit 0

PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/SOURCEFREE_CANDIDATE_AND_VERSIONED_API/tests/test_owner_bound_successor.py
# 19 passed, exit 0

PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/SOURCEFREE_CANDIDATE_AND_VERSIONED_API/tests/test_twelve_hostile_attacks.py
# 14 passed, exit 0 (12 commissioned attacks + 2 extra geometry/issuer oracles)
```

Candidate at the actual current PRE-MAIN `8e44ca9...`:

```bash
CAND=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pe-sc0-owner-bound-secure-successor-20261031-r1/WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/SOURCEFREE_CANDIDATE_AND_VERSIONED_API
PYTHONPATH="$CAND" python3 -m pytest -q -p no:cacheprovider "$CAND/tests"
# 33 passed, exit 0
```

Original and overlay commands:

```bash
HQ297_EXACT_PE_ROOT=$PWD PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py
# 21 passed, exit 0

HQ297_EXACT_PE_ROOT=$PWD PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py
# 4 passed / 9 failed, exit 1

WORK=/tmp/opencode/pe-sc0-successor-20261031-r1/overlay-court KEEP_WORK=1 \
  ./WORKER_RETURNS/PYAT-R3-PE-SC0-EIGHT-STRICT-REPAIR/repro/run_overlay_courts.sh
# 21 passed + 13 passed + 9 passed, exit 0

HQ297_EXACT_PE_ROOT=$PWD PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  /tmp/opencode/pe-hostile-review/hostile_pe_tests.py
# 12 passed as attacks, exit 0
```

## Twelve hostile attacks

All twelve fail closed in the successor with a typed refusal and no receipt.
Exact test names and exits are in `ALL_TWELVE_HOSTILE_TESTS_WITH_EXITS.md`.
The predecessor hostile 12/12 reproduction is retained as hostile evidence, not
as a green production result.

## Engineering verdict

`ACCEPT_AT_TEST_ONLY_SOURCEFREE_SCOPE__POSITIVE_AND_FAULT_NEGATIVE_EXITS_GREEN__TWELVE_HOSTILE_ATTACKS_FAIL_CLOSED__FIRST_CONSUMER_EXERCISED_IN_CANDIDATE__PRODUCTION_ADOPTER_ABSENT`

This is a scoped engineering acceptance of the source-free candidate, not a
production, scientific or authority acceptance. The current first consumer for
the new contract is genuinely exercised in-candidate. No existing production
current receiver of the enriched contract is lawfully present; that is an
explicit HOLD, not a fabricated green result.

## Scientific verdict

`HOLD__SYNTHETIC_C1_N10E_GEOMETRY_ONLY__NO_ORIGINAL_RESPONDENT_SOURCE_OR_SCIENTIFIC_ISSUANCE`

The 54/60 forward and 54/62 reverse geometry is exact synthetic arithmetic from
the source-free N10E fixture. It is not original respondent evidence, not an
operative world, not a causal effect and not a population estimand.

## Authority verdict

`HOLD__TEST_ONLY_SOURCEFREE_ISSUER_ONLY__NO_COMPETENT_SOURCE_N9_WORLD_MODEL_ACTOR_OR_PRODUCTION_GRANT__NO_ADOPTION__NO_MERGE`

The only issuer in the candidate is an exact test-only grant. It cannot
authorize source promotion, model use, N9/world adoption, Sorok actor state,
N11/N12 or production. No self-review or PRE-MAIN merge was performed.

## NOT_RUN / UNKNOWN

- P41/E04L historical suite integration under this successor: **NOT_RUN**.
  Source/contract inspection only.
- #536 P41/R08 worker suite: **NOT_RUN**. GitHub issue 536 is OPEN; the
  dispatch branch tip equals its base
  `750548ddbb9b4392a16ce93097b856f349e16182` and no worker return existed to
  inspect at dispatch.
- Original survey/respondent/actor/N9/model-use/N11/N12/Sorok operation:
  **NOT_RUN**, not authorized.
- Production adoption, deployment, PRE-MAIN merge, independent post-return
  review: **NOT_RUN**.
- Runtime proof of MAX beyond the verified process argv: **UNKNOWN**; the
  process argv records `--variant max`, and no downgrade was performed.

## Owner actions

1. Treat this candidate as isolated `TEST_ONLY_SOURCEFREE` engineering evidence.
2. Do not merge it into PRE-MAIN or install any `sitecustomize.py`.
3. A named competent N9/world/source owner must issue the selected-world
   owner/revision/digest, values, sanctions, clocks, negative-status scope and
   source-promotion rights for any operative successor.
4. A named production receiver must adopt the versioned receipt contract before
   any production consumer claim.
5. Route the candidate, original 4/13 strict baseline and hostile predecessor
   findings to an independent post-return reviewer at the exact pushed SHA.

## Candidate implementation blobs

| Path | Blob |
|---|---|
| `SOURCEFREE_CANDIDATE_AND_VERSIONED_API/owner_bound_successor.py` | `08f0bea429a8f35223db8acf757ef7b714805603` |
| `SOURCEFREE_CANDIDATE_AND_VERSIONED_API/sourcefree_world.py` | `264c6092b5a151960779d0e610f2d964474da920` |
| `SOURCEFREE_CANDIDATE_AND_VERSIONED_API/n10e_adapter.py` | `3c9f34fd4f629ccebd8e9efeb485f3a2d7c1c2c5` |
| `SOURCEFREE_CANDIDATE_AND_VERSIONED_API/first_consumer.py` | `145977129dcacad6f8a7ec3d2888783a6ed0652c` |
| `SOURCEFREE_CANDIDATE_AND_VERSIONED_API/fixtures.py` | `6f3233945aadcf92730a7e77ad301e1a07c52414` |
| `SOURCEFREE_CANDIDATE_AND_VERSIONED_API/tests/test_owner_bound_successor.py` | `5a3558f7e60b1afc70210ef5cb1c69fd459049b1` |
| `SOURCEFREE_CANDIDATE_AND_VERSIONED_API/tests/test_twelve_hostile_attacks.py` | `37ad5b63ed2be6fa6b87ee4e93483e51de5b2865` |
| `SOURCEFREE_CANDIDATE_AND_VERSIONED_API/README.md` | `9724566a085dca5074f5baf1134fab328f0fd6c9` |

The exact final pushed branch SHA is reported externally after commit and
push/readback; it is not self-referenced inside its own commit.

TERMINAL: `OWNER_BOUND_SOURCEFREE_SUCCESSOR_BUILT__ORIGINAL_21_AND_STRICT_4_OF_13_PRESERVED__OVERLAY_21_13_9_REPRODUCED__HOSTILE_PREDECESSOR_12_REPRODUCED__SUCCESSOR_ALL_33_PASS__TWELVE_ATTACKS_FAIL_CLOSED__FIRST_CONSUMER_TEST_ONLY_EXERCISED__ENGINEERING_ACCEPT_SCOPED__SCIENCE_HOLD__AUTHORITY_HOLD__NO_MERGE`.
