# REC-02 — Bounded Local Provider / Succession Evidence Recovery Task

Status: `BINDING__HQ_AUTHORIZED__LOCAL_CODEX_EVIDENCE_RECOVERY__WARRANT_PROTOCOL`

## 0. Purpose

This task does **not** create authority.

It performs bounded local evidence recovery for exact provider/succession questions that R08 could not close from Browser/Git/Library alone.

The worker is an evidence retriever operating under warrants. It must not decide that Rawlsing needs new authority merely because a search fails.

The governing rule is:

> `UNLOCATED` is not `MISSING_PROVED`.

## 1. Exact jurisdiction

Primary R08 warrants:

- `U003`
- `U004`
- `U005`
- `U006`
- `U007`
- `U008`
- `U009`
- `U010`
- `U011`
- `U012`
- `U013`
- `U014`

Additional evidence-access warrants:

- `EAD-V525B` — recover exact accepted V525b semantic/driver payload bytes referenced by R03;
- `EAD-D62-92` — recover the exact d62 singleton-92 delta keys/payload referenced by R03.

No other provider search is authorized by this task.

## 2. Environment and search law

Required environment:

`BOUNDED_LOCAL_CODEX_EVIDENCE_RECOVERY`

Permitted:

- checked-out Rawlsing repository and git history;
- named historical worktrees/packages/exports referenced by governing manifests or R08 warrants;
- named local source/authority package locations explicitly referenced by project authorities;
- direct child paths reached from those named roots when the project evidence itself points there.

Forbidden:

- `find ~ ...` style whole-home crawls;
- sweeping `/Users`, `/Volumes`, Desktop, Downloads, Documents, or arbitrary backup trees without a named governed reference;
- unrelated repositories;
- unrelated survey sources;
- searching for semantically similar filenames with no lineage connection;
- treating mtime/path recency as authority;
- authoring or repairing canonical authority;
- declaring `MISSING_PROVED`.

## 3. Preflight

### P0 — repository / HEAD / branch

Record repository path, branch and HEAD.

The launch message supplies the required exact start HEAD and branch.

If starting HEAD is wrong:

`STOP__WRONG_START_HEAD`

Do not hide divergence with merge/rebase/force-reset.

### P1 — governing reads

Read:

1. `HQ/AUTHORITY_REVALIDATION_FINAL_ADJUDICATION.md`
2. `HQ/CHETIRI_RECOVERY_AND_LOCAL_ESCALATION_QUEUE.csv`
3. this task file;
4. R08 `README.md`;
5. R08 `UNPROVED_SUCCESSION_AND_COEXISTENCE_LEDGER.csv`;
6. R08 `OPEN_HQ_QUESTIONS.md`;
7. R03 `FINDING_LEDGER.csv` and `OPEN_HQ_QUESTIONS.md` for V525b/d62 evidence debts;
8. R00 `R00_LOCAL_EVIDENCE_ESCALATION.md`.

### P2 — create the warrant register BEFORE searching

Create `WARRANT_REGISTER.csv` by copying each U003–U014 row's exact:

- `issue_id`;
- proposition/lineage;
- current evidence state;
- browser/git/library exhaustion state;
- `bounded_recovery_obligation` text;
- TIR IDs.

Also add EAD-V525B and EAD-D62-92 from R03's exact evidence-access statements.

For each warrant, record the initial **allowed root set**.

An allowed root must come from:

1. an exact path/root named by the warrant or governing authority; or
2. an exact historical package/export/worktree path referenced by a governed manifest cited by that warrant.

If a proposed root satisfies neither condition, it is forbidden.

## 4. Fixed search procedure — repeat independently for every warrant

For each warrant, perform steps W1–W8.

### W1 — restate the target

Write one sentence:

> I am looking for [exact provider/successor/evidence object], at [exact required grain], because [warrant ID].

Do not broaden the target during search.

### W2 — list positive proof requirements

Before searching, copy the warrant-specific `FOUND requires` checklist from section 6 below into the warrant log.

### W3 — search only root 1

Record:

- root/path searched;
- exact command/query;
- files/packages matched;
- whether each match is lineage-connected or merely lexical noise.

### W4 — inspect evidence fragments

For each lineage-connected match, record:

- exact path;
- git/blob/content hash where possible;
- producer/package identity;
- timestamp only as nonauthoritative metadata;
- predecessor/context references;
- acceptance/adjudication evidence;
- asserted scope/grain;
- relevant fields.

A matching filename is never enough.

### W5 — follow only explicit lineage pointers

If a inspected governed file points to another exact path/package/root, that referenced location may be added to the allowed root set.

Record:

- pointer source;
- exact referenced target;
- why following it remains within warrant jurisdiction.

Do not follow vague clues such as “maybe backups” or “old version somewhere.”

### W6 — exhaust remaining allowed roots

Repeat W3–W5 for each allowed root.

### W7 — apply the literal decision table

Use section 5. Do not use free-form verdict wording.

### W8 — freeze warrant result

Once the allowed roots are exhausted, record the terminal state and stop searching that warrant.

Do not use time left over to broaden the search.

## 5. Per-warrant decision table

| Situation | Required state |
|---|---|
| Exact provider/successor is located and **all** warrant-specific positive-proof requirements are met | `LOCATED_WITH_EXACT_RECEIPT` |
| A related artifact/helper/draft/interface is located but one or more required provider/succession conditions are missing | `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED` |
| All named/lineage-derived allowed roots were searched and no qualifying provider/successor was proved | `NOT_LOCATED_AFTER_BOUNDED_SEARCH` |
| A required named root cannot be accessed or does not exist and search therefore cannot be exhausted | `BOUNDED_SEARCH_BLOCKED__EXACT_ROOT_UNAVAILABLE` |

Forbidden result strings:

- `MISSING_PROVED`
- `NEW_AUTHORITY_REQUIRED`
- `PROBABLY_MISSING`
- `GOOD_ENOUGH`

Those are outside REC-02 jurisdiction.

## 6. Warrant-specific positive proof requirements

### U003 — global QSM negative-information same-grain successor

Target TIRs: `TIR-019; TIR-020; TIR-064`.

`LOCATED_WITH_EXACT_RECEIPT` requires ALL:

- same-question/same-assertion grain mapping from predecessor QSM information;
- preservation of `forbidden_inference` where present;
- preservation of `does_not_measure` where present;
- preservation of review/block state;
- preservation of evidence ceiling/provenance;
- explicit successor or retirement edge accepted by governed authority;
- current consumer compatibility / owner identity.

A later positive relation carrier alone fails this checklist.

### U004 — respondent source registry absorption/succession

Target TIRs: `TIR-006; TIR-064` plus source identity implications.

Requires ALL:

- explicit predecessor registry identity/hash;
- field-by-field preservation or governed transformation mapping;
- successor owner;
- acceptance receipt;
- explicit retirement/succession evidence.

### U005 — respondent semantics / response-contract succession

Target TIRs: `TIR-012; TIR-064`.

Requires ALL:

- predecessor semantics registry identity;
- category/value same-grain preservation;
- special-state preservation;
- successor owner;
- acceptance receipt;
- predecessor retirement/succession edge.

O07 measurement-use class alone is not enough.

### U006 — family/manual overlay + exception ownership

Target TIRs: `TIR-005; TIR-012; TIR-020; TIR-064`.

For each exact SEARCH_IN_PROGRESS family obligation, requires ALL:

- exact family/wave scope;
- exact manual/exception assertion grain;
- current owner or accepted same-grain successor;
- source/provenance receipt;
- explicit treatment of negative/unresolved states.

Do not invent a universal overlay denominator.

### U007 — production DiscoveryAuthority + DISCOVERY_FRONTIER

Target TIRs: `TIR-046; TIR-047; TIR-064`.

Requires ALL:

- accepted production package, not draft/test/interface only;
- exact `DiscoveryAuthority` identity;
- exact grammar/catalog/frontier identity;
- acceptance/adjudication receipt;
- governed program fields required by the current I08 contract;
- exact run/replay binding;
- predecessor/context where applicable.

A mechanism implementation with no accepted production authority is `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED`.

### U008 — branch/cohort predicate ancestry + membership replay provider

Target TIRs: `TIR-048; TIR-064`.

Requires ALL:

- exact predicate identity;
- ancestry/parentage;
- exact membership derivation or persisted governed membership;
- replay determinants;
- accepted owner/provider scope.

Aggregate subgroup distributions are insufficient.

### U009 — general post-discovery validation/admission owner

Target TIRs: `TIR-050; TIR-064`.

Requires ALL at the actual learned-product promotion grain:

- candidate state;
- validation state;
- accepted state;
- support/denominator handling;
- weight/design where applicable;
- uncertainty handling or typed unquantified state;
- robustness/specification/multiplicity treatment where governed;
- negative/rejected state;
- accepted owner/lifecycle authority.

Bounded I03/I05 examples alone do not prove a general owner.

### U010 — positive actor-fact comparator rules + objective fact owners

Target TIRs: `TIR-051; TIR-052; TIR-064`.

Step zero for this warrant:

- recover the exact missing fact-family list from the comparator feeder.

For each fact family, positive proof requires ALL:

- objective fact owner identity;
- fact temporal/source scope;
- comparator rule identity;
- exact empirical source/field/time coordinate binding;
- negative/no-comparator/ambiguous/noncomparable states;
- accepted authority receipt.

Semantic similarity is not a comparator.

### U011 — production PSEPF provider / positive V3 actor-transition owner

Target TIRs: `TIR-053; TIR-054; TIR-063; TIR-064; TIR-067`.

Requires ALL:

- accepted production authority identity/version/hash;
- source-indexed uncertainty-bearing PSEPF provider;
- positive owner binding for permitted V3 effect;
- read-permission matrix;
- effective-time/rebind lifecycle;
- replay receipt;
- preservation of the population-field vs actor-psyche noncollapse law.

Without positive binding, zero actor-transition effect remains governing; do not manufacture one.

### U012 — learned-product publish/version/supersede/withdraw lifecycle owner

Target TIRs: `TIR-064; TIR-065`.

Requires either:

- one universal accepted owner, OR
- a demonstrably complete family-scoped owner set.

Each covered product family must preserve:

- publication identity/version;
- predecessor/successor relation;
- supersession state;
- withdrawal state;
- historical retention;
- replay/provenance owner.

Immutable storage/repository mechanics alone are insufficient.

### U013 — end-to-end decoder/replay/completeness chain

Target TIRs: `TIR-002; TIR-064`.

Requires one governed chain binding ALL:

- source hash;
- decoder identity;
- decoder config/dependency determinants;
- predicate/authority identity;
- transformation identity;
- release/scenario identity;
- execution identity;
- explanation/provenance lineage.

Byte hashes alone do not prove semantic replay completeness.

### U014 — release/supersession history across learned products

Target TIRs: `TIR-064; TIR-065`.

Requires the U012 lifecycle evidence plus explicit historical predecessor/successor retention and withdrawal history rather than only current indexability.

### EAD-V525B — exact accepted V525b payload recovery

This is an evidence-access task, not a provider-succession proof.

Positive result requires:

- exact payload path/file;
- content hash matching the accepted hash(es) cited by R03 or an exact accepted manifest binding;
- readable bytes sufficient to execute R03's frozen row sample later.

Terminal states for this evidence-access warrant:

- `PAYLOAD_RECOVERED__HASH_BOUND`
- `PAYLOAD_FRAGMENT_FOUND__HASH_NOT_PROVED`
- `PAYLOAD_NOT_LOCATED_AFTER_BOUNDED_SEARCH`
- `PAYLOAD_SEARCH_BLOCKED`

### EAD-D62-92 — exact d62 singleton-92 delta recovery

Positive result requires:

- exact 92-row key set;
- exact before/after or current payload sufficient to audit the semantic change;
- content/hash/provenance binding to the H004/R03 referenced lineage.

Terminal states:

- `DELTA_92_RECOVERED__PROVENANCE_BOUND`
- `DELTA_FRAGMENT_FOUND__92_SET_NOT_PROVED`
- `DELTA_92_NOT_LOCATED_AFTER_BOUNDED_SEARCH`
- `DELTA_92_SEARCH_BLOCKED`

## 7. Evidence-fragment rule

Finding something interesting does not mean the warrant is solved.

Examples:

| Found item | Correct handling |
|---|---|
| file named `DiscoveryAuthority` with no acceptance receipt | evidence fragment only |
| old QSM export with negative fields but no successor edge | evidence fragment only |
| branch registry with predicates but no membership replay determinants | evidence fragment only |
| PSEPF interface without positive V3 owner binding | evidence fragment only |
| lifecycle code supporting delete/version but no semantic withdrawal authority | evidence fragment only |
| V525b payload whose hash cannot be bound to accepted authority | payload fragment only |

Never upgrade a fragment because it “looks clearly intended.”

## 8. Search exhaustion rule

`NOT_LOCATED_AFTER_BOUNDED_SEARCH` is allowed only when:

1. every initially named allowed root was searched;
2. every exact lineage pointer discovered inside those roots was either followed or explicitly inaccessible;
3. commands/queries are recorded;
4. false-positive matches are accounted for;
5. no permitted named root remains unsearched.

It means only:

> not located inside the exact bounded jurisdiction.

It does **not** mean the provider never existed.

## 9. Required outputs

Write only under:

`.../AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/returns/REC-02/`

Required:

1. `README.md`
2. `WARRANT_REGISTER.csv`
3. `BOUNDED_SEARCH_MANIFEST.csv`
4. `PROVIDER_RECOVERY_LEDGER.csv`
5. `SUCCESSION_RECEIPT_LEDGER.csv`
6. `EVIDENCE_FRAGMENT_LEDGER.csv`
7. `EXACT_PATH_AND_HASH_LEDGER.csv`
8. `V525B_PAYLOAD_RECOVERY_RECEIPT.md`
9. `D62_SINGLETON_92_RECOVERY_RECEIPT.md`
10. `UNLOCATED_AFTER_BOUNDED_SEARCH_LEDGER.csv`
11. `BLOCKED_ROOT_LEDGER.csv`
12. `REC02_ADJUDICATION_RETURN.md`

The adjudication return must contain one row/result for every U003–U014 plus EAD-V525B and EAD-D62-92.

No warrant may disappear from the final accounting.

## 10. Mutation law

Permitted committed writes:

- REC-02 return artifacts only.

Permitted temporary activity:

- read-only local filesystem/git inspection;
- scratch scripts needed to hash/index bounded roots.

Forbidden:

- canonical authority edits;
- runtime/compiler edits;
- source edits;
- new DiscoveryAuthority/frontier creation;
- new comparator rules;
- new PSEPF owner binding;
- new lifecycle law;
- QSM retirement;
- `MISSING_PROVED` declaration.

## 11. Stop condition

When all 14 warrants have a terminal result, validate the accounting, commit, push, and STOP.

Do not continue into C05R even if U007 is located. HQ must ingest REC-02 first and explicitly open C05R.

Final self-check:

> For every “found” claim, could another reviewer verify from path + hash + accepted receipt + exact grain that this is the governed provider/successor, rather than merely a related artifact?

If not, classify it as an evidence fragment rather than `LOCATED_WITH_EXACT_RECEIPT`.
