# D02Z — minimum native source producer, exact type/authority court

## 1. Contract executed as a nonissuing source-local specimen

**Code candidate** `repro/pre553_documentary_rule_source_contract_candidate.py`, contract identifier `PREV3_ORIGINAL_DOCUMENTARY_LEGAL_RULE_SOURCE@0.1.0-CANDIDATE`. Not imported by `rawlsing_next`, not in an accepted authority registry and not an original Ghana legal data downloader. This provides a genuine *data-only native component* with two pure entrypoints and a typed result:

```python
inspect_source_preimage(value: Any) -> SourcePreimageDecision
evaluate_requested_operation(value: Any, operation: str) -> dict[str, Any]
```

Input is an exact-key dict of **34** Ghana Act 591 §7 documentary semantic/source/version and explicitly negative fields, recorded in `01_DOCUMENTARY_SOURCE_IMMUTABLE_PREIMAGE.json#source_local_input`. Invalid types, absent/extra keys or mismatched literal semantics fail closed. Source URI is a known government reproduction and statute §7 is an externally inspected positive *documentary source*, but a caller can still clone the input: **schema validation makes no cryptographic source-authentication claim**.

The Python `SourcePreimageDecision` is frozen and contains `state`, `reasons`, `canonical_input_sha256` (SHA-256 of stable JSON serialization), `source_document_pdf_sha256=None`, `issued_fact_ref=None`, `competent_issuer_ref=None`, `permitted_externally_active_uses=()`, `proposed_rule_class="RULE_TEXT_DOCUMENTED"`, `candidate_only=True`. Output state on good inputs is `LOCAL_PREIMAGE_SHAPE_POSITIVE__NOT_ISSUED`; on bad source is `REFUSED_LOCAL_PREIMAGE`. This is deliberate **nonissuance**, not simulated production.

Direct requests for `ISSUE_RULE_TEXT_DOCUMENTED` return `HELD_COMPETENT_ORIGINAL_SOURCE_ISSUER_AND_PRODUCER_ADOPTION`; `RULE_IN_FORCE_AT_TIME` returns `HELD_ACT_COMMENCEMENT_AND_AMENDMENT_ASOF_AUTHORITY`; `BIND_V557_V558`, `SERVE_N9_HISTORICAL`, `SERVE_N9_CURRENT` are separately HELD. Person citizenship, enforcement, service access, causality, empirical fact, forged V554, G0b/V3 are REFUSED. None return a producer fact ref.

No variable is called `official_pdf_sha256` unless it is **null**. No synthetic deterministic hash of normalized JSON is mistaken for the original legal artifact hash.

## 2. Scientific source-provenance and legal meaning fields (do not collapse)

| Dimension | Concrete Ghana §7 candidate | Unknown or forbidden |
|---|---|---|
| Issuer / authority | Parliament of Ghana (legislative body), Act 591, Part I §7 | Actual software `competent_issuer_ref=null`; historical state/corpus authenticity not cryptographically signed |
| Government witness | BRR govt-hosted DataCenta PDF, PDF indices 1–2; GIS government handbook copy PDF index 36; Parliament official catalog | Signed Gazette original / Parliament original byte SHA `null`; independent editorial ancestry between reproductions not certified |
| Original legal subject class | Conditional citizenship-by-birth category; nation-state Ghana | No citizen/person observation, adjudication or individual ID |
| Text predicate | birth on/after 1993-01-07, in/outside Ghana, parent **or grandparent**, Ghanaian citizen status original wording '**was or is**', birth-context preserved | No normalization to parental status only, no all-Ghana-residents eligibility |
| Constitutional overlay | Art. 6(2) from OSP original scan, **after Constitution commencement**; Constitution commencement 1993-01-07 (promulgation) | No exact automatic identity with §7's *on or after* boundary or statute effective date |
| Historical text/version | assent 2000-12-29, explicitly `AS_ENACTED...RECONSTRUCTION__NOT_CERTIFIED_GAZETTE` | Act actual legal commencement `null`; unknown amendment chain; 2012/2026 operative as-of `null` |
| Publication metadata | BRR PDF Gazette notification 2001-01-05; HTML registry labels 2000-12-29 date of Gazette | No silent reconciliation; no effective-date derivation |
| Type | `PRESCRIPTIVE_RULE_TEXT` and prospective `RULE_TEXT_DOCUMENTED` | Not I01 `EmpiricalFact`, attitude, administrative enforcement, objective causal effect |
| Use ceiling | `INSPECT_UNISSUED_DOCUMENTARY_PREIMAGE` now; future issuer may license `DOCUMENTARY_RULE_TEXT_CONTEXT` | No current N5/N6 published native fact, V557, V558, N9, G0b or V3 authority |

**Important scope:** the programmer-specified predicate is a transcription-informed documentary **representation**, not a judicial determination of the rule's case-level effect. In particular, the original 'was or is' phrase is not coerced into an independently resolved citizen-ancestor-at-birth boolean.

## 3. Exact next, owner-adoptable producer (not secretly implemented)

Proposed future type name `OriginalDocumentaryRuleTextFact@1`; proposed source contract `PREV3_ORIGINAL_DOCUMENTARY_LEGAL_RULE_SOURCE@1` — **subject to competent issuer decision**. For a real positive original-source product, the first new producer must:

1. Accept independently verified institutional source provenance: original official issuer/edition, exact **retrieved bytes**, SHA-256, URL, original page/clause selector, and reproduction distinction; if official bits impossible, an issuer must define a separate lower-confidence text-witness use ceiling, never mislabeling it.
2. Accept **separate** `text_version_anchor`, `legal_commencement`, `amendment_chain_at_query_time`, `legal_interpretation_warrant`. Only `text_version_anchor` can presently be populated positively; effective law and contemporary status remain unknown.
3. Accept an **externally issued** `source_science_authority_ref` and `rule_semantics_issuer_ref`; validate exact source, clause, text, semantics, signatory and target-use ceiling. No caller-supplied string can serve as its own credential.
4. Emit immutable *actor-independent* `RULE_TEXT_DOCUMENTED` fact and exact dependency references **only if** competent source/scientific issuer grants it. Negative objects must preserve: `UNKNOWN_SOURCE_BITSTREAM`, `UNRESOLVED_STATUTORY_COMMENCEMENT`, `UNRESOLVED_ASOF_AMENDMENTS`, `UNPROVED_OPERATIONAL_APPLICABILITY`, `REFUSED_WRONG_SEMANTIC_OBJECT`.
5. Do not register a new V554 family or employ P06, M1 or J04 as a surrogate original law owner. External-law documentary carrier needs explicit owner ruling. Any implementation extending the existing M4 whitelist requires separate M4 law authorization, not simple schema acceptance.
6. Expose no `RULE_IN_FORCE_AT_TIME`, individual-status or causal operation absent further original source, version, population and mechanism evidence plus independent issuer/consumer demand.

**Shortest technical owner patch after approval:** implement a `DocumentaryRuleTextFact` source materializer with typed source acquisition+provenance, exact clause predicate, version/negative-status object and local deterministic hash; bind source original/issuer refs; add source-free hostile tests, approved issuer integration checks, then a separate *read-only* `N6DocumentaryRuleContext` consumer. This candidate's pure validation and 35 vectors supply a start, not final issuer integration.

## 4. Existing source-owner compatibility court

Checked first-party modules at exact D02Z seal `36314fca8ae98c1ddc9311bf194762e151ce5b10`:

| Existing owner | Pinned Git blob | Result |
|---|---|---|
| `pre553_source_local_universe_admission.py::DocumentaryField` | `b968fa16c6620cd06b191ebdb5da7da86f524393` | 'Documentary' names empirical respondent field metadata only; no legal original source |
| `pre553_structural_admission.py` | `fe8f706afbb5739d026846952681081b2937e9a8` | P06 strictly empirical query/fact/authority; law not admissible as EmpiricalFact |
| `m1_admitted_field_forge_relation_v554_ingress.py` | `0aeacd9e66c7e4340b36e1b622bb5c9bf2865fd5` | Relation admission consumer, not source producer |
| `m4_v557_v558_publication_repository.py` | `8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360` | Only V553/V554/V555/V556 roots; generic StructuralObject is not original-source authority |
| `prev3_objective_position_v557_v558_publication.py` | `7d2a5dbb3e0979c599632645867aa48a336a8e79` | Single J04 Q73A qualified CONTEXT, not law |
| `gt12_d_to_m4_typed_bridge.py` | `ca3d6b8d832d7ca8d959bd19e19a23b08cabde76` | Bridge for an already admitted FF relation, cannot produce Act text |
| `objective_consumer_bounded_evidence.py` | `f30fca20e7b56e00348e82765d95f974b4b6a195` | Caller-declared PolicyInput; OC05 terminal N9 not yet applicable |
| `PYAT_CONTROL_ROOM/.../N5.md` | `125c564fed077d0899cd4768236e3cb9270f1948` | Demand/claim specific admission; none adopted for this new source family |
| `PYAT_CONTROL_ROOM/.../N6.md` | `1664b22620d715c111eb7386dd18509de587c008` | Populated concrete products/permissions still demanded |
| `PYAT_CONTROL_ROOM/.../N9.md` | `20827a3187f83f32228fcaceee07e4bdf4847b22` | Selected world, version/currentness and replay not satisfied |

**Adoption decision to HQ:** commission dedicated external documentary original-source custodian + scientific rule-text semantic issuer + consumer/carrier integration owner, initially **archival rule text only**, with a separate choice whether lower-confidence government reproduction is sufficient for candidate science; postpone all actual current-law application. No semantic owner self-adopted.
