# W31 INDEX SCHEMA

Status: `DOCUMENTATION_INDEX_SCHEMA__NO_RUNTIME_EFFECT`

All canonical index rows require immutable identity. An on-base source uses `source_ref_sha=daffee545fc60a8cd635aee9aafbe77a920f4c19` plus repository path and Git blob SHA. An off-tree source uses its exact commit SHA as both immutable ref and Git object identity; W31 does not copy the body merely to manufacture physical presence.

## Required dimensions

`authority identity` — stable row/object identifier.

`scope` — jurisdiction in which the authority is meaningful.

`grain` — smallest proposition/function/carrier/status unit at which the authority applies.

`authority_level` — authority state from `AUTHORITY_LEVELS.tsv` or a narrower W26-defined admitted-function class.

`currentness` — explicit selection/status. It is not derived from time or topology.

`source_ref_sha` / `source_path` / `source_object_hash` — immutable source identity.

`succession_or_supersession` — typed successor status, never inferred from noncontainment.

`physical_presence_status` — whether bytes/function are on `daffee545fc60a8cd635aee9aafbe77a920f4c19`, off-tree/index-only, or physically absent pending another Wave-3 owner.

`preservation_status` — whether W31 is indexing live law, preservation-only capital, history, or an implementation obligation owned elsewhere.

`delegated` / `exploratory` — independent flags. Delegation does not imply global sovereignty; exploratory does not imply adoption.

`open_state` / `blocked_state` — separate dimensions. OPEN may contain a BLOCKED substate but neither collapses into REJECT or false.

`consumer_permission` — what downstream use is authorized at exact grain.

`must_not_infer` — explicit anti-widening guard.

## Semantic identity classes

The semantic law index uses the following distinct classes where relevant:

- `RELATION_PROPOSITION_ID`
- `SEMANTIC_CLAIM_ID`
- `AUTHORITY_INSTANCE`
- `LIFECYCLE_CURRENT_SELECTION`
- `CONSUMER_PERMISSION`
- source-native / semantic-relation / respondent-composability / measurement / structural-admission boundary classes.

These are indexing dimensions, not a new ontology minted by W31; they expose P1/P2/P3/P4/Authority31 law already present on the selected base.

## Extension law for W33/W34/W35

A later lane may append or join a row only if:
1. exact immutable source identity is added;
2. the existing authority ceiling is preserved or narrowed;
3. no `OPEN` is closed without competent exact successor authority;
4. preservation/exploration does not become live promotion;
5. physical integration does not create semantic authority;
6. W31's anti-resurrection row remains representable and enforceable.

A later candidate may add physical-presence receipts to an existing authority row. That is a carrier-state update, not an authority widening.
