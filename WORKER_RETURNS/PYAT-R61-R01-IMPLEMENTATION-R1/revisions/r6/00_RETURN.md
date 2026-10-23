# R61-R01 R6 author return — retained recurrence campaign owner

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted. R03 stays
NOT_STARTED.

## Identity

- Branch: `agent/opencode-pyat-r61-r01-generic-grammar-r1`
- Startup: `4b5fd7a240a6e2d007ba1df2424780e6b5612ea9`
- API contract commit (before code): `e2b87e6c33364e5361ed3c0b10ba5c13e34efbba`
- Code commit: `3d60f9cb6f43830244fbd79699d1cf4041622d05`
- Governing decision: `8c03f95ca77a4c874449fff67a4032f83d9d0a02`
- Defect review: `537bd3985d8a3825186e41cab9308d8150cac848`

## Delivered owner

`RetainedRecurrenceCampaign` is the accepted recurrence owner. It internally
retains campaign root/policy/context, issuance, execution, lineage and activation
records. Public methods are `issue`, `execute`, `activate`, `inspect`,
`snapshot`, and `RetainedRecurrenceCampaign.restore`.

- Issue resolves parents only from retained lineage refs, derives producer
  generation, binds prior issuance/count from retained records, commits exact
  grammar/expected operations before execution, and returns explicit
  `STOPPED_BUDGET` with unissued entries for zero/exhausted caps.
- Execute resolves the retained issuance/plan/lineage again, validates the
  predecessor chain, root/policy/source/ancestry/handoff/receipt bindings,
  calls the pinned existing I05+recursive-handoff path, reconciles exact
  receipts/handoffs, and only then commits execution. Completed-issue retry is
  idempotent.
- Activate derives the next generation from the producing execution, rejects a
  caller label that disagrees, and commits lineage/activation records from actual
  receipts/handoffs. Nonwinning exploratory parents remain receipt-free.
- Inspect returns deep-detached material. No public registration path accepts a
  caller plan, parent, execution, generation or counter.
- Snapshot/restore require a separately supplied checkpoint pin; rewritten
  bytes with internally recomputed hashes fail. Fresh-process restore runs an
  actual N+1 issue/execute from retained lineage.
- Run-local `RLock` serializes mutation. Trust scope is the configured local
  campaign host; no protected issuer/signing service/global durable uniqueness
  or R09 capture is claimed.

Legacy `build_recurrence_issue_plan` / `execute_recurrence_generation` /
`activate_next_generation` remain explicitly unqualified utilities for old
R4/R5 proof adapters; they cannot register campaign history. R03 must use the
campaign facade.

## Qualification

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_grammar.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r6/junit.xml -o addopts=''
```

- Exit `0`; `28 passed`, `0 failed/errors/skips`; `11.96s`.
- JUnit `junit.xml`; log `pytest.log`.
- Campaign D3 measured separately: 3 generations, 12 issued operations,
  `0.3674s`, peak RSS about 39 MB.
- Preserves R3 A1-A3, changed-data D3, root/parent contrasts, hidden minority,
  nonwinning exploration, conditioned JOINT/CO_TRAVEL and cold persisted-parent
  proofs. H1-H7 successor attacks are refused through the retained owner:
  forged lineage, requested-generation relabel, altered predecessor, wrong root,
  zero cap, wrong activation label and mutated inspect views.
- Fresh-process campaign snapshot/restore with pinned checkpoint runs actual
  generation N+1; altered rehashed snapshot fails the unchanged pin.
- Imported owner blobs: `pre553_discovery_exact.py`
  `905f24d114419dbdd93879ad2bee5b59dd2f23af`, `pre553_recursive_handoff.py`
  `868f43bf9869af5501fd67c3de7a2703ba4cb1b4`,
  `pre553_empirical_objects.py`
  `a61365b994e5c3c50de0f598fcf40e90abf757b6`.

## Changed paths and blobs

| Path | Blob |
|---|---|
| `rawlsing_next/universal_grammar/types.py` | `e7b196efe5b1f86134c27a80bfdd8f472be76e5d` |
| `rawlsing_next/universal_grammar/enumerate.py` | `fd9203a0b272f98771c24070d01a9e5287c9b099` |
| `rawlsing_next/universal_grammar/native_map.py` | `b59db6d90d6f8bf6c07722877f655a5c851334b9` |
| `rawlsing_next/tests/test_universal_grammar.py` | `91dd47f9ca511ecdc4a7f6e25bad812744deec85` |

Report artifacts are SHA256-listed in `manifest.json`, which excludes itself.

## Limits

No R03/U43/Batch, R04 custody, R05 grades, original 35/1890, global F6/F7/F8,
N11/N12, Sorok, production/CI or J52/W52. The campaign owner is local trusted
runtime, not distributed anti-fork or protected issuer. Legacy utilities are
unqualified. A distinct native reviewer must qualify this exact candidate.
