# M1 — Hostile seam test oracle

**Contract:** `M1_TEMPORAL_V554_INGRESS_SEAM@1.0.0`  
**Evaluation mode:** contract-level adversarial adjudication against accepted SCR553/SCR554 authorities; no production implementation executed.

| ID | Hostile case | Required result | Adjudication |
|---|---|---|---|
| `M1-H01` | Exact SIG-001 admission; no new V553 operation; all direct gates positive. | Direct basis only; one F1. V553_NOT_REQUIRED is corroborative routing state, not direct permission. | `PASS` |
| `M1-H02` | Same admission U1 static; U2 later requires persistence with exact participants/rule. | U1 direct if SCR554 gates pass; U2 requires V553 relation/limit. No admission-global temporal class. | `PASS` |
| `M1-H03` | Timestamp/history metadata present but exact invocation requests no new temporal semantics. | No forced V553 transit; SIG-001 may proceed only under SCR554 direct gates. | `PASS` |
| `M1-H04` | V553_NOT_REQUIRED_FOR_THIS_USE but SCR554 direct static authority is missing. | No F1; K06. NOT_REQUIRED does not grant direct eligibility. | `PASS` |
| `M1-H05` | SIG-002 exact point use with KEY+OBSERVATION refs. | V553 basis required; direct admission contributes zero support. | `PASS` |
| `M1-H06` | SIG-003 exact relation use with positive comparability but no pooling authority. | Temporal relation may be basis if all rule gates pass; pooling/respondent composition remains forbidden. | `PASS` |
| `M1-H07` | Cross-source temporal operation requires comparability but authority is missing/unknown. | V553 limit/no positive temporal object; SCR554 no direct comparative fallback; K06/K07 as applicable. | `PASS` |
| `M1-H08` | Exact NONCOMPARABLE relation state plus physically present direct admission copy. | No F1 for same temporal demand; K08; no signature downgrade. | `PASS` |
| `M1-H09` | Required temporal support absent/gapped plus direct copy. | No F1 for same temporal demand; K09; absence != zero. | `PASS` |
| `M1-H10` | No-op/compatibility V553 object physically coexists with lawful SIG-001 direct basis. | Count direct once; V553 zero support; F1 identity unchanged. | `PASS` |
| `M1-H11` | V553 object contains extra temporal semantics irrelevant to exact SIG-001 invocation. | Extra material is reference/provenance only; cannot create independent support. | `PASS` |
| `M1-H12` | Direct and V553 paths overlap collision probe but one material equivalence component is unresolved. | EQUIVALENCE_UNKNOWN; affected set emits no F1. | `PASS` |
| `M1-H13` | Same proposition text but different source universes/estimands/measures. | Preserve as distinct candidates if independently eligible; no text-based collapse. | `PASS` |
| `M1-H14` | Same invocation arrives under two unresolved required authority snapshots. | K07 before duplicate/support counting; zero F1; no two-support split. | `PASS` |
| `M1-H15` | One authority snapshot is newer semver/commit date but no governed precedence exists. | K07; no latest/semver/recency winner. | `PASS` |
| `M1-H16` | Direct/V553 physical path differs but semantic support and all material authority are identical. | At most one support; path difference preserved only as provenance/alias refs. | `PASS` |
| `M1-H17` | Two admission lineage IDs differ only by reissue/receipt path and materiality is explicitly provenance-only. | One support if other material equivalence fields match; aliases preserved. | `PASS` |
| `M1-H18` | Lineage differs and governing authority says the difference changes lawful-use permission/source-risk-set/estimand. | Distinct support identities/candidates; no collapse. | `PASS` |
| `M1-H19` | Lineage role cannot be determined as material vs provenance-only. | EQUIVALENCE_UNKNOWN; fail closed. | `PASS` |
| `M1-H20` | Negative governs U2; same admission has distinct U1 outside negative scope. | U2 blocked; U1 independently evaluated. No global poisoning. | `PASS` |
| `M1-H21` | Observed temporal value 0 versus missing observation. | Zero remains measurement; missing remains typed negative/limit. | `PASS` |
| `M1-H22` | V553 ref resolves only by label/fuzzy/latest because exact hash-bound target is missing. | Projection fails closed; no V554 positive basis. | `PASS` |
| `M1-H23` | Relation participant order reversed under ordered rule. | Different/rejected semantic identity; no silent sorting. | `PASS` |
| `M1-H24` | Same exact inputs reordered by file/row enumeration. | Identical routing/projection/support count/IDs; replay invariant. | `PASS` |

## Required aggregate invariants

```text
EXACT_HASH_BOUND_PROJECTION_ONLY
SIG001_DIRECT__SIG002_003_V553
USE_SCOPED_NOT_OBJECT_GLOBAL
V553_NOT_REQUIRED != DIRECT_V554_ELIGIBLE
PROVENANCE != COMPARABILITY_OR_COMPOSITION
NEGATIVE_FOR_SAME_DEMAND -> NO_DIRECT_DOWNGRADE
NOOP_OR_IRRELEVANT_V553 -> ZERO_EXTRA_SUPPORT
EQUIVALENCE_UNKNOWN -> FAIL_CLOSED
UNRESOLVED_AUTHORITY_SNAPSHOT_CONFLICT -> K07_BEFORE_SUPPORT_COUNT
PROVENANCE_ONLY_LINEAGE -> NO_SUPPORT_SPLIT
UNKNOWN_LINEAGE_MATERIALITY -> EQUIVALENCE_UNKNOWN
NO_LATEST_SEMVER_RECENCY_SCORE_OR_ORDER_PRECEDENCE
```
