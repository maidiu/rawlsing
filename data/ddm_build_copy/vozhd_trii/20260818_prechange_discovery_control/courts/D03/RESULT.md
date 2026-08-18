# D03 — V526e / V549 / V549b → Current Co-Signature & Attitude-Cloud Lineage Court

**Court:** VOZHD TRII D03  
**Repository:** `maidiu/rawlsing`  
**Audited base:** `bf9a0434eb2096d5c4725cf483ec757fd319b6af`  
**Work branch:** `agent/vozhd-trii-d03-v549-cloud-lineage`  
**Frozen VT3 comparison base:** `8c87f7725ba58202b5377c974548140420709fa9`  
**Disposition:** `PASS_WITH_MATERIAL_LINEAGE_SPLIT_AND_LOSS`  
**Production code modified:** no

## 1. Finite verdict

Historical V526e named one broad capability family: **branch co-signature and profile covariance**. Its explicit purpose was to compute “what else travels with each branch” and preserve covariance for later profile generation, with three expected outputs: `branch_co_signature_summary`, `profile_cluster_summary`, and `profile_relation_vector`.

Executable V549 implemented only the first slice of that design. It reconstructed respondent membership in V548 recursive branches and measured association between the resulting **binary branch-membership indicator** and another question’s categorical responses, using Cramér’s V and a branch-enrichment/depletion description. That is genuine **branch-conditioned cotravel**, but it is neither a conditional empirical distribution nor a realized profile covariance object.

Executable V549b broadened the anchor family. It supported (a) a particular response to a question, (b) binary answer-presence/absence anchors, and (c) V548 branch-node anchors. It still measured each anchor against another question’s categorical response using pairwise Cramér’s V. It explicitly marked anchors as eligible for the historical profile-posterior/strata-tension design, but it still did not materialize the V526e `profile_cluster_summary` or `profile_relation_vector`.

Current V550 has split the old vocabulary across three different computations:

1. `build_position_signature_rows` = **within-current-question association between position-coordinate columns and that question’s response**.
2. `build_co_signature_rows` = **within-current-question-frame association between permitted non-position feature columns and that question’s response**.
3. `build_attitude_cloud_rows` = **same-respondent, cross-question pairwise cotravel**, currently reduced to one selected modal joint response cell plus pairwise NMI/Cramér’s V.

Only (3) performs a cross-question respondent join. Neither (1) nor (2) receives recursive branch membership. Current `branch_id` / `branch_key` fields in those two builders are therefore **synthetic question-scope identifiers, not proof of a V548-style branch cohort**.

The historical V526e “profile covariance” capability is consequently classified:

> **SPLIT_INTO_MULTIPLE_OBJECTS, with material information loss.**

No current object is transformation-equivalent to the historical profile-covariance design. Historical profile clusters and profile relation vectors are absent from this lineage. Historical branch-conditioned cotravel existed in V549/V549b but is not preserved by the current native cloud/signature functions. Current same-respondent question cotravel is a successor capability, not an identity-preserving rename.

The current `ddm_v550_clouds.py` blob is identical at frozen VT3 base `8c87f7…` and the audited D03 base `bf9a043…` (`dfc878e87d984a1a3d7000a0c726bdc444f9945f`). The lineage split described here therefore predates the frozen VT3 baseline and remains present at the current base.

## 2. Governing evidence and authority order

The court read the full D03 control surface before lineage reconstruction:

- `data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/README.md`
- `00_FULL_MACHINE_VISION.md`
- `01_FINDINGS_LEDGER.md`
- `02_RESOURCE_INDEX.md`
- `03_ASSUMPTION_AND_UNKNOWN_REGISTER.md`
- `04_DISCOVERY_COURTS_REGISTER.md`
- `05_DECISION_PROTOCOL.md`
- `06_FIRST_WAVE_LAUNCH_REGISTER.md`
- `DISCOVERY_REGISTER.json`
- `evidence/HISTORICAL_DESIGN_EXTRACTS.md`

and current governing law:

- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md`
- `TERMINAL_DEMAND_ENVELOPE.md`
- `ARCHITECTURE_PASS_LAW.md`

The decision protocol’s non-collapse rules govern this result. In particular:

- population association is not actor psychology;
- same-respondent survey cotravel is not a psyche or persona;
- a historical branch cohort is not a biography;
- an association diagnostic is not a conditional empirical distribution;
- a field name such as `branch_id`, `profile`, or `cloud` does not establish semantic identity.

Historical extracts are used only for genealogy. Current authority and current executable code outrank them.

## 3. No-conflation ontology

| Concept | Exact meaning in this court | What it is not |
|---|---|---|
| **Demographic/position signature of a branch** | Distribution or association of position coordinates among respondents actually belonging to a defined branch cohort. | Merely associating demographics with a question response while calling the question a branch. |
| **Relation co-signature associated with a branch** | Association between actual branch membership and other relation/attitude responses in the same respondent universe. | Generic co-resident feature association inside one question frame. |
| **Same-respondent question-response cotravel** | Cross-question association computed by matching the same respondent IDs across question frames. | Metadata similarity, shared driver IDs, or population marginals from different respondents. |
| **Branch-conditioned cotravel** | Same-respondent response association in which the anchor cohort is defined by membership in a branch, normally reconstructed from branch conditions. | Question-level scope or a synthetic `branch_id`. |
| **Historical profile covariance** | V526e design family intended to preserve branch co-travel plus cluster/vector structure for profile generation. | Any one pairwise association score; current table names do not establish identity. |
| **Generic within-frame feature association** | Association between two columns already co-resident in one row frame, here NMI/Cramér’s V against the current question response. | Cross-question cotravel unless the frame itself lawfully contains cross-question response variables. |
| **Conditional empirical distribution** | A full governed distribution `P(response topology | exact governed empirical predicate, scope)` with support/provenance. | A single association score, a modal joint cell, or one conditional event probability selected after looking at the joint table. |

These seven objects must remain separate throughout downstream review.

## 4. Historical V526e intent

Controlled historical evidence in `evidence/HISTORICAL_DESIGN_EXTRACTS.md` records:

- pack: `V526e_BRANCH_CO_SIGNATURE_AND_PROFILE_COVARIANCE`;
- purpose: compute what else travels with each branch and preserve covariance for profile generation;
- required outputs:
  - `branch_co_signature_summary`;
  - `profile_cluster_summary`;
  - `profile_relation_vector`;
- stop if branch membership cannot be computed or all co-signatures are underpowered;
- prohibit an independent-random-draw parent generator.

The historical Attitude Cloud Access Contract separately distinguished:

1. position determinant = demographic/structural predictor;
2. anchor response = immediate question-response or branch;
3. attitude cloud = other non-demographic opinion/attitudinal responses associated with the anchor among the same respondent universe.

This establishes intended conceptual separation between **position**, **anchor**, and **attitude cotravel**. It also establishes that V526e’s word “covariance” referred to preservation of co-variation for a broader profile-construction design. It does **not** prove that a covariance matrix, cluster model, or relation vector was ever executable.

The current repository at the audited base does not contain the historical generated V549/V549b review YAMLs at the builder-declared pack paths. Those historical output destinations are therefore treated as executable declarations, not as independently inspected result payloads. The controlled extract contains an exact V547 review extract but not equivalent V549/V549b generated-result extracts.

## 5. Executable V549: what it actually computed

**Source:** `data/ddm_build_copy/build_branch_co_signature_summary_v549.py`

### 5.1 Anchor and respondent universe

V549 loads V547 question determinicity summaries and V548 recursive tree nodes. For each V548 node, `build_branch_mask` reconstructs respondent membership recursively.

Root membership is:

`anchor question response is non-null`.

Child membership is inherited from the parent mask and refined using the **parent node’s** stored conditions:

- `majority_position_conformity`:
  `parent AND position == indicator_value AND response == majority_answer`
- `majority_position_deviation`:
  `parent AND position == indicator_value AND response != majority_answer`
- `minority_position_convergence`:
  `parent AND position != indicator_value AND response == majority_answer`
- `minority_position_divergence`:
  `parent AND position != indicator_value AND response != majority_answer`

That is actual branch-cohort reconstruction, not a branch-name proxy.

### 5.2 Candidate question and association computation

For every eligible candidate item other than the anchor question:

- candidate values are the candidate question’s categorical responses;
- branch membership is a Boolean vector over respondents;
- rows with missing candidate response are dropped for the Cramér’s-V contingency calculation;
- minimum branch and candidate support gates apply (`MIN_BRANCH_N = 25`);
- core score = Cramér’s V of:

`branch_membership ∈ {0,1}` × `candidate_response_category`.

The output grain is approximately:

`source × declared canonical_wave × anchor_question × branch_node × candidate_question`.

The output does **not** preserve a candidate answer category as part of the primary grain.

`effect_direction` is a descriptive enrichment/depletion statement. It chooses the candidate response mode among branch members and compares that mode’s share in the branch with its share among all observed candidate responders.

### 5.3 What V549 did not compute

V549 did not materialize:

- `profile_cluster_summary`;
- `profile_relation_vector`;
- a respondent profile posterior;
- a full branch-conditioned candidate response distribution;
- a covariance matrix over a vector of responses;
- a k-way response topology.

Thus executable V549 is **branch-conditioned pairwise association**, not the whole V526e profile-covariance design.

### 5.4 Scope defect in executable V549

`load_source_frame` filters respondents by `source`, and response rows by `source` plus selected variables. It does not filter the fetched respondent/response substrate by wave or country. `canonical_wave` is carried from V547/V548 metadata into output, but the live row universe is source-wide.

Therefore:

- **historical intent/label:** wave-specific branch co-signature;
- **executable guarantee:** source-wide respondent substrate with question/tree metadata carrying a wave label.

If variable codes are reused across waves, this can admit cross-wave respondents. This is an implementation-semantic mismatch, not evidence that cross-wave pooling was intended.

Repeated responses are pivoted with `aggfunc="first"`, so duplicate/multi-response observations were also flattened to one value per respondent/question.

## 6. Executable V549b: what it added and what remained

**Source:** `data/ddm_build_copy/build_question_response_attitude_cloud_summary_v549b.py`

V549b retained branch-node anchoring and added answer-level anchor forms.

### 6.1 Anchor families

1. **single-answer anchor**
   - anchor = respondent answered question A with one of its top two observed answer codes;
   - minimum anchor n = 50.

2. **answer-presence / answer-absence anchor**
   - intended for multi-select / split-block items;
   - executable anchors are literal code `"1"` and `"0"`;
   - minimum anchor n = 50.

3. **branch-node anchor**
   - reconstructs V548 respondent branch masks;
   - minimum branch n = 25.

Historical V549b anchor rows set:

- `allowed_for_profile_posterior = True`;
- `allowed_for_strata_tension = True`.

Those are historical permission claims. They are not current V550 authority.

### 6.2 Same-respondent semantics

V549b constructs a wide respondent×question response frame. Anchor masks and candidate question responses therefore refer to the same respondent index. It is genuinely same-respondent cotravel.

For each anchor and another candidate question, V549b computes:

`CramérV(binary_anchor_membership, candidate_question_response_category)`.

For single-answer anchors, the binary anchor membership means `A = a`; for branch anchors it means membership in the reconstructed recursive branch.

The candidate side remains question-level categorical response. `candidate_answer_code` is blank in the output; V549b does not emit `P(B=b | A=a)`.

### 6.3 Directionality versus symmetry

V549b’s **anchor construction** is directional: a particular answer or branch is the anchor and another question is the candidate.

Its **core association score**, Cramér’s V, is symmetric with respect to the two variables in the contingency table. It does not itself encode causal or psychological direction.

`effect_direction` is branch/anchor enrichment or depletion of the candidate’s modal category. It is not a reverse-conditional probability.

### 6.4 Candidate eligibility

V549b’s candidate registry excludes metadata-scope material and restricts to structure/relation-registry rows intended for the `attitude_cloud` channel. This continues the historical distinction: position variables are not attitude-cloud candidate questions merely because they co-occur with responses.

### 6.5 Historical scope defect retained

The final report says V549b is a “same-source, same-wave, country-scoped practical proxy,” but executable data loading is weaker:

- respondent loading contains `source` and `country` fields but not wave filtering;
- wide response loading filters by `source` and variables, not wave;
- later country slicing is real;
- wave constrains candidate-registry selection, not respondent-row selection.

Thus **same-source and country scoping are executable; same-wave respondent scoping is only partially represented by selected variable metadata**.

As in V549, the wide pivot uses `aggfunc="first"`, flattening repeated/multi-response rows.

### 6.6 Pairwise/top-k truncation

V549b ranks candidate questions per anchor and retains only top candidates (`TOP_N_CANDIDATES = 10`). Even historically, therefore, the artifact was a truncated pairwise association surface, not a lossless higher-order covariance representation.

## 7. Current V550 cloud lineage

**Primary current module:** `data/ddm_build_copy/ddm_v550_clouds.py`  
**Current shard integration:** `data/ddm_build_copy/build_determinicity_wave_shard_v550.py`

The shard builder:

1. fetches one question frame at source + wave + country + question/var scope;
2. harmonizes response semantics;
3. resolves source-structure metadata;
4. builds and joins current question-use authority;
5. creates ordinary `branch_df = prepare_question_frame(df)`;
6. separately computes `recursive_branch_nodes`;
7. passes only the ordinary per-question `branch_df` into all three cloud/signature builders.

`recursive_branch_nodes_df` is **not passed** to `build_position_signature_rows`, `build_co_signature_rows`, or `build_attitude_cloud_rows`.

That disconnect is decisive for the branch-lineage question.

### 7.1 `build_position_signature_rows`

**Input frame:** one question’s respondent rows in one current source/wave/country scope.  
**Anchor:** current question response variable.  
**Candidate universe:** columns classified as `POSITION_COORDINATE`, principally V550 indicator/demographic fields.  
**Respondent matching:** none across questions; candidate and target are columns in the same frame.  
**Exclusions:** non-position feature roles; blank candidates.  
**Metric:** `max(normalized_mutual_information, Cramér’s V)` between candidate position column and current response; a `presence_only` zero-score fallback can be emitted when an association statistic cannot be formed.  
**Output grain:** top five position features per current question-scope pseudo-branch.  
**Support:** unweighted row count, current support-tier functions.  
**Authority gate:** `allowed_as_branch_position_signature`; current authority derives this from lawful demographic-predictor eligibility.  
**Persistence:** `clouds/branch_position_signature` in the V550 shard/repository outputs.  
**Current semantic status:** diagnostic, cloud-lane, not direct evidence.  
**Direct consumer found:** V550→V551 bridge indexes it as `position_context`, not as direct relation evidence.

The function sets:

- `branch_id = anchor_question_id`;
- `branch_key = source::canonical_wave::country::anchor_question`.

No branch cohort is reconstructed. Therefore this object is more precisely:

> **question-response position signature**, not “position signature of a recursive branch.”

### 7.2 `build_co_signature_rows`

**Input frame:** same one-question respondent frame.  
**Anchor:** current question response.  
**Candidate universe:** explicit relation-feature allowlist if supplied; otherwise non-excluded, non-technical, non-demographic, non-position columns already present in the same frame.  
**Respondent matching:** no cross-question respondent join.  
**Metric:** `max(NMI, Cramér’s V)` of candidate column vs current response.  
**Output grain:** top five candidate columns per current question-scope pseudo-branch.  
**Authority gate:** current question must allow `allowed_as_branch_relation_cosignature`; candidate columns are also role-filtered.  
**Persistence:** `branch_relation_co_signature`; `branch_co_signature` is later created as an alias copy of this table.  
**Current semantic status:** diagnostic, cloud-lane, not direct evidence.  
**Direct consumer found:** bridge lane `disabled_artifact`; not V551 direct relation evidence.

Because the ordinary question frame is fetched for one `var_code`, this function cannot become historical V549 cross-question branch cotravel merely by calling a column “relation evidence.” Unless another lawful varying relation feature is genuinely co-resident in that same question frame, it has no other-question response to compare.

Therefore current co-signature is:

> **generic within-frame feature association against the current question response**, not proven branch-conditioned cotravel.

### 7.3 `build_attitude_cloud_rows`

This is the only current cloud function that actually preserves the “same respondent, another question” operation.

#### Scope and state

State key:

`(run_id, source, wave, canonical_wave, country_code)`.

Each current question frame is prepared into one row per respondent, then stored in `_ATTITUDE_CLOUD_STATE` if it is allowed as an anchor and/or feature.

#### Cross-question matching

For an emitted pair, `_emit_attitude_cloud_pair` performs an **inner join on `respondent_id`** between anchor question frame A and candidate question frame B.

This proves same-respondent semantics.

#### Current position exclusion

Current attitude-cloud code blocks position/context material in multiple independent ways:

- question-use authority grants attitude-cloud anchor/feature use from relation-evidence eligibility, not position-coordinate eligibility;
- `_attitude_cloud_semantics_blocked` rejects position-coordinate and structural-context semantic roles/classifications and numerous coordinate subroles;
- final pair emission requires both anchor and candidate `semantic_role == "RELATION_EVIDENCE"`;
- both sides require their respective `allowed_as_attitude_cloud_anchor` / `allowed_as_attitude_cloud_feature` gate.

Therefore position coordinates are intentionally separated from the current attitude-cloud candidate lane.

The lawful distinction is:

> position = structural conditioner/context coordinate;  
> attitude cloud = same-respondent cotravel among governed relation-response questions.

Neither permits conversion of population association into actor belief.

## 8. Exact current same-respondent probability law

Let:

- `A` = prepared anchor question frame;
- `B` = prepared candidate question frame;
- each contains at most one row per respondent after preparation;
- `J = A ⋈ B` on `respondent_id`, restricted to nonblank responses.

Current code builds the complete-case cross-tabulation of anchor response category × candidate response category over `J`.

It then chooses **one cell only**:

`(a*, b*) = the most frequent joint response cell in J`.

Define:

- `N_ab = # {r ∈ J : A_r = a* AND B_r = b*}`
- `N_a = # {r ∈ A : A_r = a*}`
- `N_b = # {r ∈ B : B_r = b*}`
- `N_B = # {r ∈ B}`

Current persisted measures are:

`n_overlap = N_ab`

`n_anchor = N_a`

`n_candidate_baseline = N_b`

`p_cotravelling_given_anchor = N_ab / N_a`

`p_cotravelling_baseline = N_b / N_B`

`difference_from_baseline = (N_ab / N_a) - (N_b / N_B)`

`lift = (N_ab / N_a) / (N_b / N_B)` when baseline is nonzero.

### 8.1 Missing-candidate treatment

This denominator law is not complete-case conditional probability.

If a respondent has `A = a*` but no usable B response:

- the respondent remains in `N_a`;
- the respondent cannot enter `N_ab`.

Thus current code computes an event probability equivalent to:

> probability of observing `B = b*` among all respondents with `A = a*` in the prepared anchor frame,

not:

> `P(B=b* | A=a*, B observed)`.

The baseline denominator is all prepared candidate responders, `N_B`.

That asymmetry must be preserved in D04 tests unless governing authority says the formula itself is wrong.

### 8.2 Pairwise association diagnostics

On the **complete-case joined response vectors**, current code also computes:

- normalized mutual information;
- Cramér’s V;
- `association_strength = max(NMI, Cramér’s V)`.

The output column named `mutual_information` receives the result of `normalized_mutual_information`, not raw mutual information.

These pairwise statistics use all response categories in the complete-case overlap, while the persisted conditional probability fields refer only to the selected modal joint cell.

### 8.3 Directionality

The probability fields are directional because their denominators distinguish anchor from candidate.

The NMI and Cramér’s-V diagnostics are symmetric association measures.

`directional_alignment` compares response-direction/polarity metadata. It does not turn the population association into a causal direction, actor belief, or psychological relation.

## 9. Current pair coverage is processing-order dependent

Current state iteration is asymmetric:

1. when the current question is anchor-eligible, it emits current-anchor → **previously stored** candidate questions;
2. only after that does it store the current question.

It never revisits earlier anchors when a later feature arrives.

Consequences:

- if A and B are both anchor+feature eligible and A is processed before B, current code emits **B→A** but not A→B;
- reversing question order emits **A→B** but not B→A;
- if A is anchor-only and B is feature-only, A→B exists only if B was stored before A;
- a feature-only question arriving after an anchor-only question cannot trigger the earlier anchor.

Therefore the current executable output set is not invariant to question iteration order.

This court does not modify that behavior. D04 must test it against the semantic oracle below.

## 10. Duplicate and multi-select behavior

Current `_prepare_attitude_cloud_frame`:

1. filters blank respondent IDs and blank normalized responses;
2. executes:

`drop_duplicates(subset=["respondent_id"], keep="first")`.

Therefore current executable semantics are:

> at most one response row per respondent/question; when duplicates exist, the first surviving row wins.

No ordering authority is supplied to this function.

For repeated-response or long-form multi-select questions, this can erase selected values. It can also make results depend on input row order.

The control register explicitly leaves respondent/question uniqueness and duplicate/multi-select semantics unresolved. Therefore:

- **executable fact:** first-row collapse;
- **governed intended semantics:** unknown until D04/D05/D06 establish authority.

The correct D03 action is to expose the collapse, not invent a fix or declare all duplicates invalid.

## 11. Is current attitude cloud pairwise only?

Yes.

At persistent output level, one row represents one ordered question pair and only the **single most frequent joint response cell** selected from that pair’s complete-case contingency table.

The artifact does not preserve:

- all response-pair cells even for the same two questions;
- complete pairwise joint distributions;
- respondent-level cross-question vectors;
- triplets or higher-order response conjunctions;
- interaction-only structure such as XOR;
- conditional reversals that appear only after conditioning on a third attitude;
- cluster membership;
- historical branch membership;
- k-way multimodal profile structure;
- a reconstructible `profile_relation_vector`.

NMI/Cramér’s V summarize the full pairwise contingency table but are not sufficient statistics for reconstructing that table.

Thus current attitude cloud preserves a narrow pairwise diagnostic and one selected conditional event, not historical higher-order profile covariance.

## 12. Historical PROFILE COVARIANCE outcome

### Court outcome: `SPLIT_INTO_MULTIPLE_OBJECTS`

The split is:

- historical position/identity-predictor concern → current position-signature and broader position/determinicity lanes;
- historical branch-node structure → current recursive-branch artifact, separately;
- historical branch co-travel → present in executable V549/V549b, absent from current native cloud/signature computation because branch membership is not passed;
- historical question-response cotravel → current `question_response_attitude_cloud`, transformed;
- historical `profile_cluster_summary` → **LOST in this lineage**;
- historical `profile_relation_vector` → **LOST in this lineage**;
- historical profile-posterior eligibility flags → **not current cloud authority** and not present as equivalent current output permission.

No current table may lawfully be called “profile covariance” on the evidence inspected.

## 13. Status and consumer audit

| Current object | Direct evidence? | Diagnostic? | Cloud-lane? | Explicit current profile status? | V551 direct-atom eligible? | Proven current consumer |
|---|---:|---:|---:|---|---:|---|
| `branch_position_signature` | no | yes | yes | none; historical profile relation is genealogy only | no | V550 bridge as `position_context` |
| `branch_relation_co_signature` | no | yes | yes | none | no | V550 bridge as `disabled_artifact` |
| `branch_co_signature` alias | no | yes by inherited rows | yes by inherited rows | none | no | V550 bridge as `disabled_artifact` |
| `question_response_attitude_cloud` | no | yes | yes | none; `artifact_status=prototype_diagnostic` | no | V550 bridge as `disabled_artifact` |

Important distinction:

- the **questions** entering a current cloud may need the same strong question-use authority that also makes a question eligible for V551 relation evidence;
- the resulting **cloud artifact row** is nevertheless not a V551 direct relation-evidence atom.

`ddm_v550_bridge.py` explicitly maps attitude cloud and relation co-signatures to `disabled_artifact`. `ddm_v551_atoms.py` accepts direct candidates only from `answer_distribution` and `country_answer_distribution` on the `direct_relation_response` lane.

This establishes non-consumption as V551 direct evidence. D11 still owns exhaustive downstream-consumer archaeology beyond the directly inspected V550→V551 path.

## 14. No-conflation lineage crosswalk

| Historical concept | Executable historical artifact | Current artifact/function | Information preserved | Information lost/transformed | Current governed semantic status | Current consumer |
|---|---|---|---|---|---|---|
| Position determinant / demographic signature | position inputs used in V548/V549 branch construction | `build_position_signature_rows` | association of current response with position-coordinate columns | actual branch cohort; branch-conditioned position distribution; historical branch path | diagnostic position context, not direct evidence | bridge `position_context` |
| Branch relation co-signature | `V549_branch_co_signature_summary` | `build_co_signature_rows` / `branch_relation_co_signature` | generic feature↔response association machinery and ranked relation-lane vocabulary | V548 branch membership; cross-question respondent cotravel; branch-conditioned candidate response association | diagnostic; contract-gated; not direct evidence | bridge `disabled_artifact` |
| Same-respondent question cotravel | V549b single-answer/presence anchors | `build_attitude_cloud_rows` | respondent-ID cross-question join; pairwise response association; anchor/candidate distinction | historical top-anchor form replaced; only modal joint cell persisted; current order-dependent pair surface | prototype diagnostic; not direct evidence | bridge `disabled_artifact` |
| Branch-conditioned cotravel | V549 branch co-signature and V549b branch-node anchors | no equivalent current cloud function | recursive branch nodes still exist separately | branch membership is not supplied to current cloud/signature functions; cotravel conditioned on recursive branch is lost from this path | no proven current equivalent | none proven in this lineage |
| Historical profile covariance | V526e design only; partially approximated by pairwise V549/V549b | split across position signature, recursive branch nodes, relation co-signature, attitude cloud | some marginal/pairwise association components | profile clusters, relation vectors, k-way covariance/topology, branch-conditioned cotravel integration | no current object has this identity | none as profile covariance |
| Generic within-frame feature association | not the defining V526e concept | `_candidate_association_stats`; used by position/co-signature builders | NMI, Cramér’s V, support/cardinality, dominant categories | no cross-question respondent proof; no branch condition | diagnostic only | persisted signatures → bridge |
| Conditional empirical distribution | not V549/V549b output | separate governed distribution concept; current cloud exposes only one conditional event | one selected `P(B=b* observed | A=a*)` plus baseline | full conditional response topology and all cells | current cloud is not a CED | cloud row only as disabled diagnostic |

## 15. Information-gain / information-loss ledger

### Preserved or strengthened in current V550

- current source/wave/country/question frame scoping is materially stronger than V549/V549b source-wide loaders;
- same-respondent join is explicit in current attitude cloud;
- anchor and candidate authority/provenance fields are explicitly carried;
- position/context questions are explicitly separated from relation-response cloud eligibility;
- cloud rows explicitly self-identify as diagnostic and not direct evidence;
- support/status metadata is explicit.

### Lost or weakened relative to historical executable V549/V549b

- recursive branch membership is disconnected from cloud/co-signature computation;
- branch-conditioned question cotravel is not present in current native cloud/signature functions;
- historical response-anchor coverage is replaced by one stateful pair-generation path whose pair set depends on processing order;
- current attitude cloud stores one modal joint response cell rather than the V549b anchor→candidate-question association surface;
- duplicate/multi-select rows are collapsed to first response;
- no historical profile cluster or profile relation vector survives.

### Transformed rather than simply lost

- V549/V549b Cramér’s-V anchor association becomes current modal-cell conditional probability + pairwise NMI/Cramér’s V;
- historical branch naming is retained in `branch_position_signature` / `branch_relation_co_signature`, but the executable anchor is now the question-scope response frame;
- historical profile-posterior eligibility is superseded by current question-use and bridge lane authority; there is no equivalent profile-permission field in the current cloud row.

## 16. Weighting

Historical V549b writes `weighted_anchor_n` and `weighted_candidate_valid_n`, but executable values are direct float copies of unweighted counts.

Current position/co-signature and attitude-cloud metrics are also unweighted. The current cloud code does not accept a weight vector.

This court does not infer that unweighted cloud computation is lawful or unlawful for every survey family. Weighting requirements for this diagnostic lane remain an authority question. D04 should test executable unweighted behavior and treat normative weighting as unresolved unless a governing contract supplies the rule.

## 17. Terminal starvation implications, without deciding D09

Directly inspected current downstream wiring treats relation co-signatures and attitude clouds as disabled bridge artifacts. Therefore their information does not become V551 direct relation-evidence atoms through the standard compiler.

At the same time, the historical branch-conditioned cotravel capability is no longer produced by the current native cloud functions.

This creates a proven lineage fact:

> if a later terminal requirement needs branch-conditioned or same-respondent cotravel, it cannot be assumed to survive merely because V550 still persists tables named `branch_*signature` or `attitude_cloud`.

Whether any such cotravel is terminally required, and what same-answer/different-cloud meaning should do, are explicitly outside D03 and remain for D09/D11/D12.

## 18. Unresolved questions handed forward

The following remain unknown rather than being silently resolved here:

- global uniqueness/meaning of `respondent_id` across all current survey substrates (D05);
- whether every eligible question truly has one substantive response per respondent (D05/D04);
- lawful multi-select/repeated-response representation (D04/D05/D06);
- whether the current cloud lane should be weighted, and by which weight (authority unresolved);
- exact tie law when multiple joint response cells have equal maximum frequency;
- whether all current R1/question-use cloud permissions are correct for every source/wave (D06);
- whether any downstream path outside the directly inspected V550→V551 bridge consumes cloud rows (D11);
- whether retained microdata/substrate is sufficient to recreate any lost pairwise or branch-conditioned topology (D13);
- whether terminal meaning needs cloud distinctions at all (D09);
- statistical significance is not implied by current support tiers (control unknown U080).

## 19. Follow-on questions closed by D03

D03 closes these lineage questions:

1. **Does current `branch_relation_co_signature` prove branch-conditioned cotravel?** No.
2. **Does current `branch_position_signature` describe an actual recursive branch cohort?** No; not from the native function inputs.
3. **Does current attitude cloud perform same-respondent cross-question matching?** Yes, by `respondent_id`.
4. **Are position coordinates intentionally excluded from the current attitude-cloud response lane?** Yes.
5. **Did V549/V549b genuinely use recursive branch membership?** Yes.
6. **Did executable V549/V549b realize historical profile covariance in full?** No.
7. **Does any current single object equal historical profile covariance?** No.
8. **Is current attitude cloud a full conditional empirical distribution?** No.
9. **Is current attitude cloud pairwise and lossy?** Yes.
10. **Are current cloud/co-signature artifacts V551 direct relation evidence?** No.

## D04 TEST ORACLE

D04 must test the current cloud code against the following semantics. These are the D03 lineage-derived expectations; unresolved authority cases below must remain UNKNOWN rather than be converted into false failures.

### A. Exact current cloud semantic claim

For any two distinct question frames A and B within the exact same:

`(run_id, source, wave, canonical_wave, country_code)`

scope, a lawful ordered cloud pair is:

`A → B`

when A is a lawful cloud anchor and B is a lawful cloud feature.

For a fixed emitted ordered pair A→B:

1. prepare each question to nonblank `respondent_id` + nonblank normalized response;
2. under current executable behavior, retain first row per respondent/question;
3. inner-join A and B by `respondent_id`;
4. build the full complete-case response cross-tab;
5. choose the globally most frequent joint cell `(a*, b*)`;
6. define:
   - `N_ab = count(A=a* AND B=b*)` in the joined overlap;
   - `N_a = count(A=a*)` in the full prepared A frame;
   - `N_b = count(B=b*)` in the full prepared B frame;
   - `N_B = len(prepared B frame)`;
7. expect:
   - `n_overlap = N_ab`;
   - `n_anchor = N_a`;
   - `n_candidate_baseline = N_b`;
   - `p_cotravelling_given_anchor = N_ab / N_a`;
   - `p_cotravelling_baseline = N_b / N_B`;
   - `difference_from_baseline = N_ab/N_a - N_b/N_B`;
   - `lift = (N_ab/N_a)/(N_b/N_B)` when baseline is nonzero;
8. compute NMI and Cramér’s V over **all complete-case joined response categories**, not only `(a*,b*)`;
9. `association_strength = max(NMI, Cramér’s V)`;
10. output `mutual_information` currently means normalized mutual information.

This is a directional conditional-event diagnostic plus symmetric pairwise association diagnostics. It is not a full conditional empirical distribution and must not be interpreted as person-level psychology.

### B. Exact directional pairs expected

The semantic pair set for a scope is:

`{ (A,B) | A != B AND anchor_eligible(A) AND feature_eligible(B) }`.

If A and B are both anchor-eligible and feature-eligible, **both A→B and B→A are expected semantic directional pairs**.

For the reverse pair:

- complete-case NMI and Cramér’s V should be identical apart from numerical tolerance;
- the selected modal joint cell should transpose;
- `n_overlap` should be the same for that transposed cell;
- conditional and baseline probabilities generally differ because anchor/candidate denominators swap.

D04 must not mistake symmetric NMI/Cramér’s V for symmetric conditional probability.

### C. Question-order permutation invariance

Permuting the order in which otherwise identical question frames are presented must not change:

- the lawful ordered pair set;
- the fixed-pair respondent overlap;
- the selected joint cell for a fixed pair;
- the fixed-pair NMI/Cramér’s V;
- the fixed-pair conditional/baseline counts and probabilities.

Current implementation is known from code inspection to emit only current-anchor→previously-stored-feature pairs, so D04 should explicitly test this invariant. Missing or reversed pairs caused solely by question processing order are a genuine semantic failure against this oracle, not a reason to redefine the expected pair set.

### D. Lawful anchor / feature eligibility cases

A row is expected only when both sides satisfy current executable gates:

**Anchor A**
- passes `valid_cloud_feature`;
- is not blocked by `_attitude_cloud_semantics_blocked`;
- has a nonempty prepared respondent-response frame;
- has response-semantics contract hash;
- response-semantics status is accepted by the cloud helper;
- question-use contract is joined;
- source-structure fields are joined;
- `semantic_role == RELATION_EVIDENCE`;
- `allowed_as_attitude_cloud_anchor == True`.

**Candidate B**
- same scope as A;
- distinct question ID;
- nonempty prepared respondent-response frame;
- not blocked as position/context/admin/missingness;
- has response-semantics contract hash;
- accepted response-semantics status;
- question-use contract joined;
- source-structure fields joined;
- `semantic_role == RELATION_EVIDENCE`;
- `allowed_as_attitude_cloud_feature == True`.

Position-coordinate, structural-context, administrative, missingness, and explicitly blocked coordinate-subrole questions are not lawful attitude-cloud sides.

D04 should test anchor-only, feature-only, dual-eligible, and ineligible cases separately.

### E. Denominator law

D04 must include a case where some respondents have `A=a*` but no B response.

Expected current executable result:

- those respondents count in `n_anchor`;
- they do not count in `n_overlap`;
- the denominator of `p_cotravelling_given_anchor` is still full `N_a`.

D04 must also verify:

`p_cotravelling_baseline = count(B=b*) / count(any prepared B response)`.

Do **not** silently replace either denominator with complete-case overlap. If a later authority says complete-case conditioning is the lawful formula, that is a separate authority finding/change request, not the current-code oracle.

### F. Duplicate / multi-select behavior

**Executable current behavior:** after filtering, `_prepare_attitude_cloud_frame` keeps the first row for each `respondent_id` and discards later rows.

D04 should therefore construct duplicate/repeated-response fixtures and establish:

- current results can change when duplicate row order changes;
- long-form multi-select can be flattened to one selected value;
- no multi-select set semantics are implemented in this helper.

However, the control register leaves the lawful intended duplicate/multi-select representation unresolved. Therefore D04 must classify the normative question as `UNKNOWN_AUTHORITY` unless it finds governing law. Do not fail merely because a hypothetical alternative representation was not implemented; fail only proven violations of a current governed rule, while separately reporting executable first-row sensitivity.

### G. Support and weighting

Current cloud counts/metrics are unweighted. D04 should reproduce unweighted counts exactly.

Whether the cloud lane is normatively required to use survey weights is unresolved here. Treat `WEIGHTING_LAW_UNKNOWN` as unknown unless an explicit governing authority establishes the requirement.

Support tier is not statistical significance. D04 must not treat support-status labels as a significance test.

### H. Unresolved cases that are UNKNOWN, not test failures

Unless D04 independently proves governing authority, treat these as unknown:

- global respondent-ID uniqueness across every substrate;
- respondent/question uniqueness before current first-row collapse;
- lawful repeated-response and multi-select set/order semantics;
- normative weighting requirement for cloud diagnostics;
- modal-cell tie-breaking law;
- exhaustive correctness of R1/question-use eligibility assignments;
- whether a co-resident column in `build_co_signature_rows` is ever a lawful relation-evidence feature in each source substrate;
- exhaustive downstream consumers beyond the directly proven bridge path;
- whether retained substrate can reconstruct discarded higher-order or branch-conditioned topology;
- terminal meaning of “same answer, different cloud”;
- any claim that population cotravel reveals an individual actor’s belief, identity, motive, or psychology.
