# 09 — Executable engineering blueprint: persistence, retrieval, compilation, owner calls and display

**STATUS** `PROPOSED_SOURCEFREE_ENGINEERING_BLUEPRINT`. No adopted CAN/ADP/Pyat scientific rule, no original actor person, production code, real user A5 or provider integration. The following SQL/pseudocode is illustrative, independent of actual adopted DB contracts; Codex HQ must map each component onto the live C12/ADP/V2 APIs and rewrite where those schemas already provide equivalent functions. **Never create a new canonical second psychological ledger.**

## 1. Minimal cut and dependency sequence

```text
SOURCE EVENT and source-granted actor/person snapshots (existing)
              │
              ├─> exact language/speech occurrence event (existing writer)
              │      └─> language encounter projection/index
              │
              ├─> actor-only knowledge + competence refs (existing ADP16/17 where granted)
              │
              └─> actor branch current state + model-of-user + history (existing)
                         │
                         ▼
        sparse nonauthoritative concept-sense relation index
                         │
                         ▼
      versioned multi-world linguistic repertoire cache
                         │
                         ▼
       relevant context projection (whole person + bounded tail)
                         │
                         ▼
         V2 actor realization: EXACT SOURCE-LANGUAGE SPEECH
                         │
                         ▼
       source-validated objective utterance admission
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       display-only translation    persisted actor/objective history
       + lawful user attention       ↳ later indexing/qualified mediation
```

**Gate note:** the source event ledger is not a derived lexicon's private ledger. The tables below store *indexes and caches* referencing existing immutable event IDs, not alternate copies of event truth. The genuine event's writer and branch rights remain elsewhere.

## 2. Bounded SQLite projection (candidate DDL)
Use as a single app-local module namespace, or views/indexes over existing SQLite. NEVER apply to canonical repo DB until owner authorization and migration qualification. Prefixes mark derivative scope.

```sql
CREATE TABLE IF NOT EXISTS lme_concept_sense (
  concept_id TEXT NOT NULL,
  sense_id TEXT NOT NULL,
  discourse_ref TEXT NOT NULL,
  source_grain TEXT NOT NULL CHECK(source_grain IN
    ('REFERENCE_ONLY','TEST_ONLY','OWNER_ATTESTED')),
  source_version_ref TEXT NOT NULL,
  gloss TEXT,
  contested INTEGER NOT NULL DEFAULT 0 CHECK(contested IN (0,1)),
  PRIMARY KEY(concept_id, sense_id, discourse_ref, source_version_ref)
);
CREATE TABLE IF NOT EXISTS lme_lexeme_index (
  lexeme_id TEXT PRIMARY KEY,
  language_tag TEXT NOT NULL,
  surface_text TEXT NOT NULL,
  sense_id TEXT NOT NULL,
  discourse_ref TEXT NOT NULL,
  source_event_ref TEXT NOT NULL,
  source_event_hash TEXT NOT NULL,
  branch_id TEXT NOT NULL,
  index_epoch INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS lme_lexeme_source
  ON lme_lexeme_index(branch_id, source_event_ref);

CREATE TABLE IF NOT EXISTS lme_actor_relation_index (
  relation_id TEXT PRIMARY KEY,
  actor_id TEXT NOT NULL,
  branch_id TEXT NOT NULL,
  concept_id TEXT NOT NULL,
  sense_id TEXT NOT NULL,
  discourse_ref TEXT NOT NULL,
  context_scope_json TEXT NOT NULL,
  relation_label TEXT NOT NULL,
  epistemic_grade TEXT NOT NULL CHECK(epistemic_grade IN
    ('OBSERVED_UTTERANCE','ACTOR_REPORTED','OTHER_ATTRIBUTION',
     'INFERRED_HYPOTHESIS','EXISTING_OWNER_REF','UNKNOWN')),
  source_event_refs_json TEXT NOT NULL,
  contrary_event_refs_json TEXT NOT NULL,
  owner_state_ref TEXT,                     -- NULL unless independently authorized
  effective_from TEXT NOT NULL,
  effective_to TEXT,
  source_digest TEXT NOT NULL,
  index_epoch INTEGER NOT NULL,
  CHECK(effective_to IS NULL OR effective_to >= effective_from)
);
CREATE INDEX IF NOT EXISTS lme_actor_context
  ON lme_actor_relation_index(actor_id, branch_id, discourse_ref);

CREATE TABLE IF NOT EXISTS lme_compiled_repertoire (
  snapshot_id TEXT PRIMARY KEY,
  actor_id TEXT NOT NULL,
  branch_id TEXT NOT NULL,
  person_snapshot_digest TEXT NOT NULL,
  relevant_source_set_digest TEXT NOT NULL,
  compiler_version TEXT NOT NULL,
  model_and_config_ref TEXT,                -- NULL if deterministic compiler
  compiled_context_json TEXT NOT NULL,
  evidence_manifest_json TEXT NOT NULL,
  contradiction_manifest_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  invalidated_at TEXT,
  status TEXT NOT NULL CHECK(status IN ('CACHE_VALID','CACHE_INVALID')),
  CHECK(status='CACHE_VALID' OR invalidated_at IS NOT NULL)
);
CREATE INDEX IF NOT EXISTS lme_repertoire_lookup
  ON lme_compiled_repertoire(actor_id, branch_id, status);
CREATE TABLE IF NOT EXISTS lme_cache_dependency (
  snapshot_id TEXT NOT NULL REFERENCES lme_compiled_repertoire(snapshot_id),
  source_ref TEXT NOT NULL,
  source_digest TEXT NOT NULL,
  dependency_role TEXT NOT NULL,            -- person, actor history, lexical, milieu
  PRIMARY KEY(snapshot_id, source_ref, dependency_role)
);
CREATE INDEX IF NOT EXISTS lme_dep_reverse
  ON lme_cache_dependency(source_ref, snapshot_id);
```

**No** free-floating `trust`, `autonomy`, `ideological_heat`, `foreignness`, `magnetism_weight`, `trauma`, `habit_strength` or default CAN011 practice numerical column. Retrieval ranking (token similarity, nearest-neighbor ranking, source salience, recency) is **engineering selection metadata**, not psychological magnitude or probability. If a priority score is stored, annotate algorithm+version and disallow its use as a causal premise.

**Speaker utterance and translation projections** should normally reuse existing `ADP19/C8/V2/Sorok101` event and display tables. If unavailable at the allowed test-only seam, use separate `lme_speech_projection` and `lme_translation_projection` test views keyed to genuine `admitted_event_ref/hash`. Do not duplicate authoritative exact utterance, invent a writable speech truth in the cache, or let UI display change source hashes.

**Schema note:** `concept_id/sense_id/discourse_ref` are globally stable when a legitimate registry supplies them, otherwise branch-local TEST_ONLY namespaced IDs. Source events cannot be joined across branches merely by similar text. Content digests must use canonical encoded input/version, not unqualified pretty text.

## 3. Minimal interface adapters (proposals, not current imports)
```python
class SourceBoundLanguageIndexer:
    def observe_admitted_event(
        self, exact_event_ref, event_digest, actor_access_receipts, branch
    ) -> "IndexDelta | Reject":
        # 1 Verify exact event owner+digest, branch clock and actor audience.
        # 2 Extract lexeme/context candidates (possibly semantic model suggestion).
        # 3 Mark every proposed relation with actual evidence/epistemic grade.
        # 4 Write ONLY derivative index, never source-event/actor/psychological truth.
        # 5 Emit dependency invalidation list, or typed invalid-source refusal.
        ...

class RepertoireCompiler:
    def compile(self, actor_id, branch_id, current_person_snapshot,
                owner_read_permissions, evidence_index, config) -> "RepertoireSnapshot":
        # Read actor-appropriate whole-person expressive substrate (Sorok101 §19).
        # Select multiple milieus, conflicting senses, adverse evidence, scope exceptions.
        # Build cache from SOURCE, not previous cache output.
        # Return evidence/source digests and a 'NOT_PSYCHOLOGICAL_AUTHORITY' tag.
        ...

class SituatedExpressionProjector:
    def project(self, admitted_event, actor_only_state, model_of_user,
                repertoire, world_slice) -> "ActorExpressionContext | Reject":
        # Explicitly exclude Rawlsing-private user model, unavailable B motive,
        # user-preferred translation language and user attention filter.
        # CAN008/owner outputs only if separately lawful.
        ...

class ActorUtteranceAdmission:
    def admit(self, native_or_multilingual_speech_candidate,
              actor_competence_receipts, world_feasibility) -> "AdmittedSpeech | Refusal":
        # Verify actual language ability/access and provenance at permitted scope.
        # Freeze exact spans, actor, addressee, timing and objective co-event.
        # If no owner-approved speech write available, return TEST_ONLY/HOLD.
        ...

class TranslatedPhenomenalProjection:
    def project(self, exact_admitted_speech, user_linguistic_access,
                display_locale, permitted_observations) -> "UserPhenomenalView | Unknown":
        # Translation is a read-only labeled display derivative with source digest.
        # Optional dual display. Never turn English gloss into actor source speech.
        # Use only objective admitted cue refs, never actor-private state.
        ...
```
The names are API-shape placeholders. Existing types/functions must be discovered before adding code. Actor speech choice belongs **before** objective occurrence; user attention/display locale belongs **after**. A model proposal can request retrieval/interpretation without becoming a CAN008 result.

## 4. Compilation is a materialized view, not an autonomous narrator
```python
def compile_repertoire(actor, branch, state, source_index, context):
    assert exact_branch_rights(actor, branch)
    whole = permitted_whole_person_expression_projection(state, actor)
    candidates = find_source_attested_social_language_worlds(source_index, actor, branch)
    relevant = retrieve_by_context_and_actual_person_history(candidates, context)
    contrary = fetch_disconfirming_and_suppressed_contexts(relevant, source_index)
    # Preserve at least one unresolved contradiction when the source has one;
    # do not artificially create contradiction when the source has none.
    scoped = compile_several_registers_with_exceptions(
        whole, relevant, contrary, no_universal_personality_synthesis=True
    )
    return cache_with_manifest(scoped, hashes_of(whole, relevant, contrary),
                               epistemic_grade="DERIVED_CACHE")
```
**Engineering budget**: start 3–7 salient register entries, 10–30 indexed charged relations, 2–4 source exemplars, ~300–600 cache tokens, then measure. No constraints on the person's actual repertoire or living lexicon. Rare contexts must still be retrievable; absence from cache is **not** absence from actor. Contexts may be retrieved lazily from source.

**Cache dependency:** initialize with source event IDs/digests, actor current-snapshot digest, owner-authorized state refs and discourse-version refs. Invalidate only affected actor+branch+dependency indexes when a source event is appended/corrected, a concept interpretation receives new evidence, language competence changes through allowed owner, a context/milieu changes, user relation/actor-model-of-user changes in ways relevant to expressive rendering, or a source permission/retention revocation occurs. `invalidate(snapshot_id, reason, changed_ref)` must be atomic with dependency write, and stale hashes cannot be silently used.

**Cold/replay:** Reconstruct index from exact source events permitted at that historical checkpoint; the same readset produces the same factual claims, regardless of stochastic prose variation. On model/compiler version change, keep old cache manifest and compile a new snapshot; do not update past source events. Two branches descended from one root have independent post-contact concept acquisitions and distinct caches.

## 5. Authoritative turn atomicity
Do **not** implement the full causal turn as one improvised LLM JSON file. Use existing transaction boundaries.
```text
STAGE A: user input / attempted activity parsed; no world writes from intent.
STAGE B: actual user event/actor access admitted by competent owner.
STAGE C: current needs/history/receiver considered with proper readset.
STAGE D: response and selected independently performed actor action (or no-action)
         under existing lawful semantics; NO_CHANGE if A/T not actually issued.
STAGE E: exact source-language/multilingual speech + gestures proposed,
         validated, committed as objective outward occurrence.
STAGE F: read-only user projection/English translation from the exact commit.
STAGE G: later event/index/cache updates; no LLM-source psychological write.
```
Transaction law: no partial source event/actor action/target/branch publication on invalid candidate, writer failure, invalid concept access or translation failure. Translation failure **cannot roll back already admitted actor speech**: source event is still true; display may show original or typed unavailable translation. This is a critical distinction between causal commit and UI post-commit failure.

**Failure examples:** unauthenticated “Nadia learned Spanish” proposal => no competence change; actor-native utterance unproven => bounded TEST_ONLY or refusal; unexpected word spoken by real bilingual after qualified registration => lawful event; translation guesses emotion => reject gloss or add ambiguity annotation; user changes English locale => recompute derivative only, exact speech/event hash unchanged.

## 6. Selection and output quality guards — never schedule regular ideological performance
Expose rhetorical/expressive affordances **conditionally**, not mandated counts:
- Audience-conditioned register, metaperception and interlocutor-related stakes, using only actor-held evidence;
- specific social discourses, family sayings, institutional vocabulary and domain practical language with source links;
- actor's actual reasons/unknown, non-conscious habit and possible misjudgment; no always-perfect accommodation;
- tension of unmarked in-group speech versus marked out-group framing; often ordinary/silent/unremarkable speech;
- concepts as relations rather than global topic biases; ideologies shape plausible distinctions/judgments, not forced keywords.
A speaker may deliberately quote or emphasize marked vocabulary. Do not replace authentic expression with culture-free beige text merely to pass an anti-caricature test. Evaluate both stereotype excess and erasure.

## 7. Minimum genuine consumer before declaring the subsystem built
**Positive**: generated person at actual sourcefree JOIN-E/Sorok C12 receiver; same person with two legitimate social-language histories; actor utterance committed in source/mixed language; English display does not mutate actor, provenance survives cold restart; different user viewing conditions do not change source speech.

**Independent negative**: remove an actually required prior language encounter (or revoke knowledge read) while fixing world/person/clock; the **same receiver** must no longer claim actor knew/quoted/used that unavailable expression—without requiring different greeting if speech action legitimately unchanged. Separately remove one contradictory source and assert that the compiled repertoire updates its source-backed relation rather than deleting the other. Corrupt source hash => typed refusal. Cold restore original source => precise readset restored; if model output stochastic, compare admissible assertions rather than exact prose.

**Comparison**: cheap existing whole-person expressive projection with no lexicon module versus source-bound multi-world compiler; require evidence that it improves specificity/contradiction/ordinary ideological plausibility without drift, extra repetitive markers or unacceptable turn latency. If negligible, preserve simple baseline; **do not force adoption because design is intellectually attractive**.

## 8. Integration reservations and allowed stopping point
- Sorok101 §13 currently says actor exact utterance remains exact in phenomenal view. English translation as a read-only *labeled* alternative is a precise compatibility decision; native utterance remains in objective ledger regardless. HQ should amend/clarify only that scope if necessary.
- The actual current JOIN-E host must be inspected for where exact utterance and translation attach. No new canonical memory/actor identity/CAN module, no generated native psychology and no duplicate world source are authorized.
- Complex cross-lingual pragmatics may require additional translation model budget, but default ordinary turn target remains 1 semantic proposal + 1 actor realization LLM, with exceptional additional translation call only after measured necessity.
- Sourcefree evaluation can use fabricated test worlds and language histories while clearly labeled TEST_ONLY, never as evidence validating real culture/person developmental laws.
- If sourcefree JOIN-E targetless atomicity/fork repair is still under review, do not modify it; finish its existing lane and integrate afterwards via Codex HQ's actually delegated qualified owner.

**Engineering acceptance is conditional** on actual API binding and runtime receipts. This blueprint does not claim those receipts.
