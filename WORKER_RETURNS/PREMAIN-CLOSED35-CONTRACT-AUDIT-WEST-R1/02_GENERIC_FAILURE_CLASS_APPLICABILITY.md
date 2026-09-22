# Generic failure-class applicability — Worker A

This matrix maps the **question** exposed by each cross-wave failure class to the four assigned realizations. It does not import any WVS7 or LiTS substantive answer. “Applicable only after runtime packaging” means the present source-specific realization is not defective for lacking the runtime object; the class becomes enforceable when a current PRE553 package is actually constructed.

| Failure class | EVS 1999 | EVS 2008 | WVS Wave 1 | Latinobarometro 2011 |
|---|---|---|---|---|
| `DECODER_RUNTIME_TYPE__GOVERNED_KEY_NONINTERSECTION` | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING |
| `LAWFUL_AUTHORITY_REPRESENTATION__CONSUMER_IGNORES_FORM` | APPLICABLE_NOW | APPLICABLE_NOW | APPLICABLE_NOW | APPLICABLE_NOW |
| `DYNAMIC_QUERY_REF__STATIC_CATALOG_ONLY_RESOLUTION` | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING |
| `I05_FACT_EXISTS__POSTCONSUMER_PREIMAGE_MISSING` | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING |
| `HISTORICAL_FILE__AMBIENT_CURRENT_DEPENDENCY` | APPLICABLE_NOW | APPLICABLE_NOW | APPLICABLE_NOW | APPLICABLE_NOW |
| `HISTORICAL_SUCCESSOR__RUNTIME_CATALOG_SCOPE_NOT_ENFORCED` | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING |
| `SOURCE_SPECIFIC_TERMINAL_DOMAIN__GENERIC_FIELD_SUBSTITUTION` | APPLICABLE_NOW | APPLICABLE_NOW | APPLICABLE_NOW | APPLICABLE_NOW |
| `RISK_SET_DECLARED__MEMBERSHIP_PREIMAGE_UNAVAILABLE` | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | UNKNOWN_AUTHORITY_ABSENT | NOT_APPLICABLE |
| `QUESTION_VALUE_BINDING__EXACT_RESPONSE_REF_UNAVAILABLE` | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING |
| `CURRENT_PRODUCT_SHAPE_MATCHES__SUBSTANTIVE_PRIOR_TRUTH_NOT_PROVED` | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING |

## Why these rows differ

### Decoder runtime type / governed key

Current PRE553 response admission is exact-form: the source-backed facade computes each physical binding key from the decoder-observed raw value, physical missing state, and source missing declaration using the R5 typed-value codec. Host-language equality is deliberately insufficient: an integer and a numerically equal float are different keys. None of the four realization modules is itself a current runtime package, and none freezes a per-value decoder-host-type/R5-key table. The failure class therefore becomes concrete only when a runtime package is built, after a qualified representation observation.

### Lawful representation / consumer form

This is already applicable because each source exposes at least one representation boundary that must survive later consumption:

- **EVS 1999:** latin1 compatibility decoding is physical-only while producer documents own semantics.
- **EVS 2008:** the same physical-only compatibility boundary exists; additionally the rendered v372 date witness is many-to-one over the producer negative-missing domain.
- **WVS Wave 1:** S007 raw storage and F2.0 display metadata are explicitly nonidentical; system/user missing states are typed.
- **Latinobarometro 2011:** questionnaire response codes and released-SAV storage/missing states are distinct authority layers.

The source packages already prohibit the dangerous inference. A future runtime consumer must preserve that prohibition mechanically.

### Historical/current dependency provenance

All four are historical sources. Their exact source roots and documentary release scopes are source-law inputs, not permissions to consult an ambient “current” document, schema, catalog, or successor. EVS 1999 pins ZA3811 v3.0.0; EVS 2008 pins ZA4800 v5.0.0; WVS1 freezes exact W1 source/documentary bounds; LAT2011 freezes the v2011.1 source and its questionnaire/codebook/methodology layer separation. A current PRE553 package must convert those historical bounds into immutable authority snapshots rather than silently following a latest/current dependency.

### Source-specific terminal domains

This question is applicable before runtime because source-domain distinctions already exist. EVS2008 has the producer -1..-5 domain plus an intentionally unresolved v372 subreason; WVS1 uses physical missing-state classes and explicit BOUNDED_UNKNOWN; EVS1999 has DOCUMENTARY_ALIGNMENT_UNKNOWN plus documentary routing outcomes; LAT2011 separates released physical missing state, questionnaire coding, coordinate authority and WT authority. PRE553 generic response/routing/coordinate/weight state families are not license to erase those distinctions. The runtime package must provide exact authority-backed projection or leave an unresolved grain unprojected/explicitly absent.

### Risk-set membership

EVS1999 and EVS2008 already contain documentary routing/applicability law, so a runtime package that emits PRE553 routing facts will need exact risk-set ownership and replayable member-set preimages. WVS1 is different: the accepted realization explicitly says routing/applicability remains BOUNDED_UNKNOWN where authority is absent; a risk set may not be manufactured from missingness or all-system incidence, hence `UNKNOWN_AUTHORITY_ABSENT`. LAT2011's current realization does not claim a PRE553 respondent risk-set surface at all; its questionnaire routing is retained as a documentary layer, so the LiTS-style declared-risk-set failure is `NOT_APPLICABLE` at the present source-realization grain. Any later runtime package that newly declares such a risk set must re-open this check.

## Source-specific applicability notes

**EVS 1999.** The most immediate source-free issue is not one of the ten matrix labels but the common missing-state check: `user_missing=True` is frozen while typed missingness is absent from the package's R35 required physical dimensions. That must be closed without guessing source semantics.

**EVS 2008.** MR set identity and routing are unusually explicit. Exact aliases and overlaps must remain separate native topology; producer negative codes cannot be treated as a universal generic terminal domain; v372's rendered sentinel cannot manufacture a row-level negative subcode.

**WVS Wave 1.** This package is deliberately authority-limited. Its strength is preservation: raw/display separation, all-system columns, typed missingness, 13 weight carriers, and bounded unknowns. The audit must not convert those bounded unknowns into a “gap” merely because a future workload would like more semantics.

**Latinobarometro 2011.** P1ST is the key hostile boundary: instrument-layer coding cannot rewrite released-storage state and vice versa. WT is a preserved carrier, not a default analytical measure; PRE553 WeightMeasureFact admission would require exact design and estimand authority that the realization intentionally does not synthesize.
