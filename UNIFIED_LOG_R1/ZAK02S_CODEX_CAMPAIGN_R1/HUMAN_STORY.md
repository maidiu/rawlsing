# HUMAN_STORY — one old tree, three later judgments, and a current analogue

## What the old machine knew

V550 had a modest diagnostic ambition for a survey question: find the observed social position categories that reduce uncertainty about the answers, and describe the resulting subgroups. `branch_nodes_rows` in `data/ddm_build_copy/ddm_v550_branching.py` did this with a greedy recursive tree. At each node it measured the response entropy, tried each available position indicator, kept the indicator with the largest positive entropy reduction, and expanded **only the two most common values** of that indicator. It stopped after three levels by default, or when the subgroup became too small or no gain remained. The output, `recursive_branch_nodes`, was a table of nodes with parent links, split indicators and values, entropy, gain, dominant answer and a stop reason.

This was useful as a description of a few strong splits. It was not an exhaustive partition. A category ranked third or lower simply never became a child. A low-support child was skipped. The node path was descriptive, not a replayable respondent membership key.

## What happened to it

The V550 bridge admitted the table, but only under the broad lane `derived_determinicity`. The canonical V551 v3 atom compiler then admitted only `answer_distribution` and `country_answer_distribution`. So the old tree could exist in the bridge and still not be consumed as canonical empirical evidence. The predecessor return already found that the bridge’s source hash omitted indicator/category/branch coordinates, so different old rows could collide at the interface.

Trii looked at this later and made a sharp distinction. Trii D11 ruled the historical V548 branch-cohort meaning **`STRANDED`** at the canonical seam because `recursive_branch_nodes` was `derived_determinicity` and excluded from canonical V551 v3. Trii D12 graded the current tree output **`LOSSY_INSUFFICIENT`**, yet kept branch/cohort-conditioned distributions, branch-conditioned cotravel, recursive social-fork discovery and exact branch/cohort predicate and membership reconstructibility on its terminal capability list. Trii D15 dispositioned the old artifact as **`SUPERSEDED_IMPLEMENTATION`** while selecting an architecture with exact-bounded and adaptive exploratory discovery modes. In plain terms: the old table is not the required capability; the capability class is still required.

The Chetiri-corpus conditional-meaning synthesis went further. It graded V550 `recursive_branch_nodes` **`DIAGNOSTIC_ON_DEMAND`** — “Greedy bounded search tree; not empirical ontology” — and told the `derived_determinicity` bridge lane to retire from canonical production after successor/reference-closure gates. It also ruled that the old unary conditional meaning is **`STRANDED`** in the current canonical V551/V552 seam. The replacement it specified is not a better tree; it is a governed conditional-workload specification plus exact respondent-derived conditional evidence and same-respondent incidence for lawful conjunctions.

A Chetiri compiler-persistence crosswalk adds a lifecycle wrinkle. It lists **recursive branch discoveries** among the empirical learned-world products that C08 must invalidate and recompute when source, question binding, routing, weight, topology, validation or discovery-algorithm rules change, and says this may justify retaining some compiled intermediates. So the old tree can be noncanonical and still require retention/replay discipline. That is not a meaning grant; it is a warning that “diagnostic only” and “delete without proof” are different decisions.

## What the current machine actually has

The current PRE553 code has two distinct discovery modes and a recursive handoff:

1. **Exact bounded discovery** (`pre553_discovery_exact.py`) freezes a finite candidate frontier before examining data and evaluates every candidate. It can declare `RECURSIVE_SUBGROUP_FORK`, `BRANCH_CONDITIONED_DISTRIBUTION` and `BRANCH_CONDITIONED_COTRAVEL` families, but it explicitly refuses to let MI, entropy, Cramér’s V, tree score, cloud score or association strength become validation truth. Its coverage claim is `COMPLETE_FOR_EXACT_DECLARED_FRONTIER`. This is **bounded enumeration**, not entropy-selected top-two growth.
2. **Adaptive exploratory discovery** (`pre553_discovery_adaptive.py`) is the inherited second mode. It schedules only sealed evaluation units, lets heuristic rank affect search order only, and treats unvisited territory as `EXPLICIT_UNKNOWN_UNVISITED`. It cannot turn a partial search into a negative empirical claim, and it does not import or mutate exact I05 internals. This is **adaptive scheduling**, not the old tree.
3. **Recursive handoff** (`pre553_recursive_handoff.py`) persists a discovered `RECURSIVE_SUBGROUP_FORK` child to a canonical parent for the next discovery generation, with a PRESENT `DiscoveryBranchReplayBinding`, and replays the exact same-respondent cohort from the persisted predicate and source releases. This is the closest current analogue, but it is receipt-bound exact replay, not an entropy-ranked top-two tree.

`universal_grammar/native_map.py` imports the replay function and uses it in recurrence checks; two current workload modules import `native_map`. That is a real static consumer chain, but no execution was observed and nothing in that chain reads the old `recursive_branch_nodes` table. The PYAT function-parity record grades the old `branch_nodes_rows` against the current `pre553_recursive_handoff.py` as **`PARTIAL_ANALOG`**, with no declared first consumer and no full parity. The older V548/V549 cohort/cotravel first issuer is still unresolved.

## Worked example — same question, two different disciplines

Imagine a question with 1,000 respondents and three position indicators. The old function would compute an entropy reduction for each indicator, pick the best one, and split only its two commonest values. Suppose it picks `sex = female/male`; the `other` category, even if observed, is not expanded. At the next node it repeats, with `sex` removed from the available list. The output is a small tree with a root, two children, maybe four grandchildren, and a stop reason.

The current exact mode would not ask “which split maximizes entropy reduction?” It would require a declared candidate frontier — for example, a named list of subgroup forks, branch-conditioned distributions and branch-conditioned cotravel candidates — and evaluate all of them. Entropy could be reported as a diagnostic, but it could not validate a candidate. If a branch is supported, the MX01 handoff can persist the exact winning predicate and parent, and later replay the exact respondent cohort. The current machine’s question is “was this declared candidate supported by exact evidence, and can its membership be reconstructed?” not “which split looks most informative?”

That difference is the heart of this tranche: the old tree is a useful negative specification and a possible comparison oracle, not a current canonical method.

## What remains unresolved

- No actual populated `recursive_branch_nodes` run/checkpoint was inspected. We know the source algorithm; we do not know whether any real V550 run produced rows, how many, or whether the top-two rule materially excluded important categories.
- No direct current reader of the old table was found in `rawlsing_next`. The current recursive handoff is a capability analogue, not a proven successor.
- The pre-Vozhd, Vozhd, Verkhovod, full Dva and Long Memory treatment of this exact table was not inspected in this bounded tranche.
- ZAK-03 and ZAK-04 own the current C11/QSM and FF/V553/world/actor edges; this return does not claim their conclusions.

## One next question

**Does any retained V550 run/checkpoint contain actual `recursive_branch_nodes` rows whose `split_indicator`, `split_value`, `node_entropy`, `entropy_gain_from_parent`, depth and child set match a fresh static re-derivation from the pinned `branch_nodes_rows` function on the same source frame — or was the table empty/underpowered in practice?** Answering that would separate source capability from produced population and show whether the entropy/top-two discipline was materially exercised.
