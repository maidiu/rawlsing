# ZAK1057-REVIEW-02 — artifact retirement vs capability abandonment

**Review case ID:** `ZAK1057:R2:CASE:02`
**Reviewed T:** `ZAK02:T:0024` (preserved; no new canonical T minted)
**Frozen return:** `005ee95001439edd3e2f7f307d95bb546d6b6c2a::UNIFIED_LOG_R1/ZAK02S_CODEX_CAMPAIGN_R1`
**Verdict:** **ACCEPT_SCOPED_S1**
**Execution:** `NOT_RUN`; S0–S1 static source/documentary only.

## Claim under review

The return claims that the old V550 entropy-selected top-two tree was a diagnostic artifact that Trii and Chetiri-corpus treated as stranded/diagnostic/superseded implementation, while the broader branch-conditioned discovery capability remained a terminal requirement. It further claims that current exact discovery, adaptive discovery, and recursive handoff are different mechanisms, not a same-grain restoration, and that no current code reads the old `recursive_branch_nodes` artifact.

## Exact source checked

- `data/ddm_build_copy/ddm_v550_branching.py`, blob `8f6d40e0d016d66e5a3b334b31747eaef752873f`, `branch_nodes_rows` L372–L432. The function computes node and conditional entropy, selects the greatest positive gain, expands `value_counts().index[:2]`, stops on purity/depth/support/no-indicator/no-gain, and writes path-based node identity.
- Trii D11 blob `06a46105705d8beb159b16336eb671ee0381e726`, exact row L129: historical V548 branch-cohort meaning `STRANDED` because `recursive_branch_nodes` is `derived_determinicity` and excluded from canonical V551 v3.
- Trii D12 blob `e1b209e05945c6ea17f8dd73997da3d7bb2f40c0`, L192: `current_recursive_branch_nodes` = `LOSSY_INSUFFICIENT`; L45–L97 retains branch-conditioned distributions, recursive social-fork discovery, and exact branch/cohort predicate and membership reconstructibility as terminal capabilities.
- Trii D15 blob `48e802ce9689cf86d89b2f71429b4229de1b0cf0`, L150: `recursive_branch_nodes` = `SUPERSEDED_IMPLEMENTATION`; L30–L44 selects `AUTHORITY_BOUNDED_DISCOVERY_WITH_EXACT_BOUNDED_AND_ADAPTIVE_EXPLORATORY_MODES`.
- Chetiri-corpus N011 blob `4e2a97b83152d8f4fae8ef2c31cc8d0e17fc4119`, L446–L447: `DIAGNOSTIC_ON_DEMAND`, derived lane `RETIRE_FROM_CANONICAL_PRODUCTION`; L529 preserves the conditional-meaning stranded ruling.
- C08 crosswalk blob `c7aa757091336beec0158c5b99914ffcd039178a`, L665–L690: governed changes require the smallest lawful recomputation unit for affected products, including recursive branch discoveries; retention of compiled intermediates may be justified.
- Current exact blob `1b82b6df993bf14afa5e78782d988cba6e76b668`, L42/L72/L653–L654: declared-frontier coverage and refusal of diagnostic tokens as validation truth.
- Current adaptive blob `58e32770381fa8d901701d6a2c676f28261aa3e3`, L54–L55: `SEARCH_ORDER_ONLY__NEVER_EMPIRICAL_OR_STRUCTURAL_TRUTH`, `EXPLICIT_UNKNOWN_UNVISITED`.
- Current handoff blob `868f43bf9869af5501fd67c3de7a2703ba4cb1b4`, L572–L614: exact same-respondent membership replay from persisted predicate/source releases.

## Findings

1. **Artifact retirement is not capability abandonment.** The return keeps three separate things separate: the old table is diagnostic/stranded/superseded implementation; the capability class (branch-conditioned distributions, recursive forks, exact membership) remains terminally required; and the old table is not proof that the capability was restored. This is exactly what the cited records say. No conflation found.
2. **The diagnostic-vs-invalidation point is not a contradiction.** N011 says diagnostic-on-demand and retire from canonical production. C08 says recompute/possibly retain on governed changes. A noncanonical diagnostic can require recomputation and retention for replay; C08 does not promote it to canonical empirical ontology. The return already calls this a lifecycle/retention requirement, not canonical meaning. HQ’s own `02_DISPOSITION.json` concurs: “Diagnostic/on-demand status and invalidation/caching duties are not inherently contradictory; the worker has not established a design conflict requiring new architecture.” The phrase “real tension … must resolve” overstates the issue; it is a lifecycle duty and an owner retention decision, not a logical conflict.
3. **Current mechanisms are different.** Exact I05 enumerates a declared frontier and refuses entropy/MI/Cramér's V as truth. Adaptive discovery is order-only. Recursive handoff replays exact membership from a receipt-bound predicate. None reads the old table. The old artifact's absence from `rawlsing_next` is a bounded negative, not global absence.
   - **Scope clarification:** the retained historical V550 bridge (`data/ddm_build_copy/ddm_v550_bridge.py`, blob `29edd5e24f095334683035f2ce1ec95674fe274b`) still reads/carries `recursive_branch_nodes` as a historical adapter (`BRIDGE_TABLE_MAP` around L98–L112; table reads around L1141; iteration L1465–L1484). The return’s detailed claim is correctly “no `rawlsing_next` reader.” The plain-English “no current code reads the old table” must be read as no current operational/`rawlsing_next` reader, not a whole-tree historical-adapter absence. Optional wording fix; it does not change the verdict.
4. **Bounded omission.** `rawlsing_next/pre553_learned_world_composition.py`, blob `adbcc3316920c708580097dfe9f5aef4c9ca82fb`, L1748–L1761, calls C1 composition with `recursive_handoff=admitted.recursive_handoff`. This is a current non-test consumer of the handoff capability. It does not read `recursive_branch_nodes`; it reinforces the “different-input capability chain” claim rather than refuting it.

## Verdict and smallest revision

**ACCEPT_SCOPED_S1.** No blocking revision. Optional clarity edits: replace “real tension … must resolve” with “a separate lifecycle/recomputation duty compatible with diagnostic status; C08 decides retention/recompute, not canonical promotion,” and read “no current code reads the old table” as “no current operational/`rawlsing_next` reader” because the retained historical V550 bridge still reads the table as an adapter. The bounded omission should be added to the reverse-consumer narrative if the author revises for clarity.

## Evidence

`ZAK1057R2:EV:001`–`ZAK1057R2:EV:011` and `ZAK1057R2:EV:026`; searches `ZAK1057R2:S:001`–`S:006`; counterexample `ZAK1057R2:CE:002`.
