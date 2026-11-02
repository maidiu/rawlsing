# SOROK PROGRAMMA — living reference candidate R3

**Status:** `WORKING_CANDIDATE_NOT_HQ_ADJUDICATED__WHOLE_SCOPE_NOT_YET_PROVEN`.

This is the one bounded living reference for the whole Sorok undertaking: original
purpose, explanations and alternatives, exact source/code cuts, actual consumers,
negative evidence, maturity gaps, owners and next lawful work. It is not the
developmental person. No native, human A5, PRE-MAIN or owner adoption is issued.

## Current cut

| Item | Exact value |
|---|---|
| Engineering base | `a89e5ccbe67400168aaea8367f7aa00ca0de7625` |
| Inherited O-LIVE source cut | `67f667421fc90b22aad95cfc253a16feabc92348` |
| Governing W1 synthesis | `e5a25cbc4f2b9d7476a72637d3e371ee3254742e` |
| Sorok product cut | `865b5b01e1a27e99020cf2bb389af8cd4c874b57` |
| Original/Astra cut | `4f2ce6f9bdfdd2232a23d839905cb386cde96dcd` |
| CAN008/CAN011 cut | `25830fe7462bb9e29bc4087e6ae14f3f84cec377` |
| P1 sourcefree return | `b65c75a9e62618690f7d02265bc9e850af549161` |
| JOIN-V review | `4387dc818a96fda2d5271672505fbd9da1059703` |
| RRIF F2 | `cf578514434532b48e86c76c1d38d6250323a1ce` |
| PRE-MAIN observed | `8e44ca9c751049d65e6def47600b5c073ee04b29` |

## Persisted reference

| Item | Value |
|---|---:|
| Nodes | 288 |
| Edges | 741 |
| Sorok source rows | 144 + 3 references |
| Workstreams S0–S16 | 17 |
| Whole-Program Gaps | 56 (50 program gaps + 6 current source-witness gaps) |
| Journal events | 4 (GENESIS, O-SCIENCE candidate, quarantine, W1-A real return) |
| External boundary | 1 Pyat contract node only |

Exact counts are derived in `state.json`; do not use this table as a completeness
denominator.

## Trust boundary

- `r2_live_transaction.py` is disposable by default. It writes only a temporary
  state, snapshot and receipt, and proves the operating files are byte-identical
  before/after.
- The contaminated R2 state, snapshot and historical receipt are preserved under
  `quarantine/historical_demo_contamination/` with a manifest and SHA-256.
- Excluded historical demo/self-review events are inventoried in that manifest;
  they are not replayed or relabelled as acceptance.
- Canonical change evidence is the append-only `evidence/journal.jsonl` hash
  chain. `state.json` and `SNAPSHOT.json` are derived by deterministic replay.
  A valid journal prefix shorter than the known state/snapshot head is refused;
  `recover` is the explicit, recorded recovery path.
- O-SCIENCE replay recomputes the actual patch digest and fails closed on a
  mismatch, including duplicate-import paths.
- Promotion of review/engineering/consumer requires an existing competent
  immutable review record that is one of the node's own source refs. The
  reviewer, subject, assertion, verdict and appointment seal are parsed from
  that record; the node must carry the exact reviewed subject. Caller-written
  principals, wildcard scopes, unrelated genuine commits/documents and the
  JOIN-V record applied to another node do not qualify. JOIN-V remains at its
  exact historical `7bf2da3` subject/scope and does not certify this repair.
- Source withdrawal requires qualified absence/withdrawal evidence or an
  explicit authorized exclusion. A present source record cannot prove absence.
  Restoration recomputes source, review, engineering, science and authority
  negatives for the exact required causal predecessors; a second independent
  RED remains. Unrelated holds, mention, hypothesis, association, alternative
  and source-location edges are not blockers.
- Returned-artifact intake requires a real exact return SHA bound to the source
  commit. Requirements/gaps/node updates are source-backed only with a verified
  locator/quote inside the return; otherwise they remain visible as
  `CALLER_CLAIM_UNVERIFIED` or explicitly labelled `HQ_INFERENCE`.
- Source-read depth is derived per node from current witness verification. A
  local external ref with no present bytes is `UNREAD`, not `SOURCE_EXACT`, and
  the exact missing-witness negative reaches home, focus, maturity and gaps.

## Main commands

```sh
python3 living_reference.py home
python3 living_reference.py focus Q_HEALTH_001 --depth 2
python3 living_reference.py lateral CAN011_RULE_T_MISSING
python3 living_reference.py maturity Q_HEALTH_001
python3 living_reference.py whole-gaps --stage T
python3 living_reference.py whole-gaps --domain S14
python3 living_reference.py owners
python3 living_reference.py code V3_RUN_ONE_YEAR
python3 living_reference.py evidence JOIN_V_4387
python3 living_reference.py work-now
python3 living_reference.py html --output programma_home.html
python3 living_reference.py journal
python3 living_reference.py verify-journal
python3 living_reference.py verify-sources
python3 verify_source_manifest.py
python3 r2_live_transaction.py
python3 probe_faults.py
python3 repair_probes.py
```

Existing `overview`, `zoom`, `gaps`, `blocked-chain`, `source`, `consumer`,
`alternatives`, `history`, `workers`, `coverage`, `export`, `intake-return` and
`apply-authorized-transition` remain available. `critical-path` remains only a
legacy DAG illustration. Home begins with source-qualified unchosen-neighbor
purpose, intended Astra B/D experience and 100/101 constraints before terminal
obligations or implementation status.

## Scope limits

- O-SCIENCE evidence is `UNREVIEWED_CANDIDATE_EVIDENCE`; its links are candidate
  hypotheses, not issued original propositions.
- W1-A is a real returned artifact at an exact SHA, ingested as candidate
  evidence. It does not become owner adoption or independent whole-estate proof.
- P1, JOIN-E/7bf, RRIF F2, C9/C12 and M6/GT0 remain at their exact sourcefree,
  scoped or held grades. No acceptance migrates across versions or roots.
- Native CAN008/CAN011/ADP/SCI05, C8/C9/C11/C12, Pyat N11/N12, human A5 and
  PRE-MAIN integration remain external work.
- Library continuity is dated reported evidence, `NOT_ACCESSED_NOW`; a branch is
  not a running process; queued High is not observed High.
- Broader estate population remains incomplete: `WHOLE_SCOPE_NOT_YET_PROVEN`.
