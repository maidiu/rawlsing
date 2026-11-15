# FIABC-LM2-R1D-A — P2F2 Predicate-to-C11 Mapping Provenance Court

Status: `PASS__P2F2_SUPPLIES_INDEPENDENT_MAPPING_PREMISES`

Repository: `maidiu/rawlsing`

Integrated LM2 R1 base:

`agent/vozhd-premain-fiabc-lm2-r1-fanin-r1@f5ccf2b2f12fcfe02842a2aefcacdc972b598c57`

P2F2 evidence branch:

`agent/rabochii-prev3-ee-p2f2-wvs7-mechanical-pre553-issuer-r1@22667bd395e7293f99b285daddad36fe3a4377ef`

Current N1 physical-boundary law:

`agent/rabochii-premain-fiabc-lm1-r1e-c11-boundary-recovery-r1@827cc8457acaf8289ee8c70f54348008cd4f1b36`

## Court question

Do the accepted P2F2 WVS7 predicate objects merely demand downstream string values `"1"` through `"5"`, or do they positively and independently bind exact accepted WVS7 response semantic objects to those exact program-value representations?

Holding:

**They positively bind them.**

P2F2 is not itself a `NATIVE_CANONICAL_MAPPING_HARMONIZATION` authority and cannot be consumed by C11 as such. But the accepted P2F2 semantic objects supply all independent semantic premises required to parent a later, tightly bounded derived native→canonical response-value mapping authority.

The decisive evidence is not lexical equality between native code `1` and token `"1"`. It is the exact accepted semantic graph constructed and frozen by P2F2 before R6S existed.

## 1. Provenance starts from accepted source-native response semantics

P2F2 imports the accepted R6A source-native response court at:

`4b141b8b5748175e34c9286eba36f53d8df1e9d5`

and materializes:

`WVS7ResponseStateSemantics@1.0.0`

content hash:

`8aaa37c601f0dac74870c585567403520ce77287feae525832c59841dac1b710`

Its semantic material explicitly contains:

- Q291G5 and Q291P5;
- substantive native codes:
  - `1 = Agree strongly`
  - `2 = Agree`
  - `3 = Neither agree nor disagree`
  - `4 = Disagree`
  - `5 = Disagree strongly`;
- special source states `-5/-4/-2/-1`;
- exact R6A authority commit.

P2F2 also issues the positive source semantics authority:

`EE-P2F2-WVS7-SOURCE-SEMANTICS-TOPOLOGY@1.0.0`

hash:

`c7336ce479b8625b71e33743a05e43525c387dd50e4be1bb7af313667f9c341f`

kind:

`SOURCE_SEMANTICS_TOPOLOGY`.

That establishes requirement 1: exact native source semantic identity.

## 2. P2F2 creates exact response-value semantic identities before any predicate comparison

The P2F2 verifier does not identify a response merely by integer/string coincidence.

For every Q291G5/Q291P5 substantive code it constructs a distinct exact:

`WVS7ResponseValue@1.0.0`

from semantic material:

`{qid, value, label, response_semantics_ref}`.

Thus the response-value ref already binds:

- exact accepted question identity;
- exact native code;
- exact accepted source-native label;
- exact response-semantics object.

The ten exact refs are:

| Atom | Source question | Native code | WVS7ResponseValue content hash |
|---|---|---:|---|
| Q0_STATE_1 | Q291G5 | 1 | `fe59b34a25ac4a76a08f7507a71294c3569826d6cc4408a7fe9a9109145e3be2` |
| Q0_STATE_2 | Q291G5 | 2 | `2a15f85f601f5dd145351cc5179247fe18f13b707dcb88addbd33caa56781094` |
| Q0_STATE_3 | Q291G5 | 3 | `6566a9353a7bc1268019e70b5fc7ebae88efb3d7d70cd54bf87de9b5875d1b3d` |
| Q0_STATE_4 | Q291G5 | 4 | `1bd0d39d693860453e8164e55396c1101a6e0c4c26b27fee2565598e7c567f9e` |
| Q0_STATE_5 | Q291G5 | 5 | `d28bbdfa0022613de2f6c43bf8fa7aec233936901d4967df1e994586ca038ec8` |
| Q1_STATE_1 | Q291P5 | 1 | `4f34da6a78e75c9c00125dfd7e5cd1469a094646b8362260d83ea56c4ebaa9fc` |
| Q1_STATE_2 | Q291P5 | 2 | `45459f3e76a19bdc19b38a78491b62acc577977ed11b04eefd813bb162f3eb81` |
| Q1_STATE_3 | Q291P5 | 3 | `d9a9bb8f35fef19aada7e209137a7bc92b1d52a475483b6cb9f7cb6b76f92e64` |
| Q1_STATE_4 | Q291P5 | 4 | `bf2d8543a920854a958b5f5109507fda099e364e84955be4fb938c1fb5e5bc57` |
| Q1_STATE_5 | Q291P5 | 5 | `d97b6d0287bf0002fcc6e8c433bf3d9ec823468de18a90b4088b34b4b3f0a967` |

These are source-local semantic identities, not candidate outputs and not C11 canonical-value grants.

## 3. The accepted predicate AST binds each response object to one exact program value

For each response object, P2F2 constructs a `SURVEY_RESPONSE_EVENT` predicate leaf containing simultaneously:

- `question_semantic_ref = exact accepted WVS7 question ref`;
- `response_value_or_state_ref = exact WVS7ResponseValue ref`;
- `response_semantic_authority_ref = exact SOURCE_SEMANTICS_TOPOLOGY ref`;
- `response_topology_authority_ref = same accepted source authority`;
- `operator = "EQ"`;
- `exact_value = str(native_code)`;
- exact universe;
- exact event selector;
- exact program/risk scope.

It then seals that AST inside an `EmpiricalPredicate@1.0.0` with typed state:

`PREDICATE_RESOLVED_AUTHORIZED`

and positive exact grammar authority:

`EE-P2F2-WVS7-PRE553-I03-PREDICATE-GRAMMAR@1.0.0`

hash:

`92fc0bf93937b8e38cd181df7915c8786abdc16465833d731daa90ca1218dec5`.

The ten exact predicate hashes are:

| Atom | Exact token | Predicate content hash |
|---|---|---|
| Q0_STATE_1 | `"1"` | `afe05c229c77cafeb3b2147e3f52d033f370845dc7ab6e97526a2b3c0135d5d8` |
| Q0_STATE_2 | `"2"` | `8c0e8cce557bb71adb99ba9ee9835594fb643032fe39e11a1d8c319316028f48` |
| Q0_STATE_3 | `"3"` | `b19ca77ef63dccef9236d0bf73d4914f042cb0cd28ca9cec6fdd4a20678fecf3` |
| Q0_STATE_4 | `"4"` | `361ffc5a51d93e23321ab9cf7ae9a6918ac6d3fc151daac8db893fd0648d328d` |
| Q0_STATE_5 | `"5"` | `59d3ffbdd5dc937319d2f9f44493303047095240351bdba06fd4e2959f12c73c` |
| Q1_STATE_1 | `"1"` | `55a652713bf0827fc701b3dc05a9e26d7375b4be6792e230dd65f8e8bc3d1e93` |
| Q1_STATE_2 | `"2"` | `85cb7e47ce083deb8614a31bb1b7738c81103e5c81171a931965348338a53766` |
| Q1_STATE_3 | `"3"` | `5a239598cf7408de9c588c50e009b873e9a5025092206684ef8f84720ec32dd5` |
| Q1_STATE_4 | `"4"` | `2db758ac0c9100292621d7db3ee9f8fe91c1aa60e897f3513577c11571929365` |
| Q1_STATE_5 | `"5"` | `880b8cdb115581e231708da4209f6bd9bb469b6288aa4246491d7a9b4d848b99` |

This pairing is part of each predicate's semantic hash. Changing either the response-value ref or the exact token changes the predicate identity.

Therefore the relation is not:

> downstream happens to expect a token that resembles the source code.

It is:

> under the accepted WVS7 source semantics and accepted PRE553 predicate grammar, this exact WVS7 response semantic object is the response object tested by equality against this exact semantic comparator value.

## 4. PRE553 gives `exact_value` semantic comparator meaning

The generic PRE553 evaluator closes the key interpretive question.

For a `SURVEY_RESPONSE_EVENT` leaf it:

1. requires exact `question_semantic_ref`;
2. requires exact `response_value_or_state_ref`;
3. requires positive response/topology authority;
4. canonicalizes `exact_value`;
5. selects the matched WVS7 response events;
6. compares:

`canonicalize(_semantic_value(event)) in exact_values`.

Thus `exact_value` is not inert serialization metadata. It is the semantic comparison representation of the response predicate.

That makes the accepted predicate object positive semantic evidence of the relation between its exact WVS7 response-value object and the exact token.

The fact that generic execution does not dereference the response-value object to *derive* the token does not erase the accepted relation. The predicate semantic object itself contains, hashes, and authorizes both sides of that relation.

## 5. P2F2 separately freezes the target-value representation

The same representation is independently objectized in the query/domain layer.

P2F2 constructs:

`WVS7TargetDomainReplay@1.0.0`

hash:

`5d0a1ca4cc23c198a6afd4b935d425d51c7dd5cd143d056b351740c059608ef4`

from exact semantic material:

- domain = `["1","2","3","4","5"]`;
- `response_semantics_ref = 8aaa37c6...`.

Each Q291 query component then freezes:

- exact WVS7 question ref;
- topology `SCALAR_SINGULAR`;
- domain `["1","2","3","4","5"]`;
- that exact target-domain replay ref;
- exact source response semantic authority;
- included state `SUBSTANTIVE_RESPONSE`.

The candidate grammar independently uses the same exact target cells.

This proves requirement 2: there is an accepted target semantic value representation independent of candidate output.

It is **program-local WVS7 P2 semantic representation**, not a cross-source harmonized ontology.

## 6. P2F2 predates R6S and does not depend on its canonical-value construction

Exact timestamps:

- R6A source-native response court:
  `4b141b8b5748175e34c9286eba36f53d8df1e9d5`
  — 2026-09-16T21:46:08Z.
- P2F2 sealed Lock2:
  `22667bd395e7293f99b285daddad36fe3a4377ef`
  — 2026-09-17T23:36:29Z.
- R6S later materializer:
  `48887a2b1523c9d20933e4d6c5e341e80d7a0ff6`
  — 2026-09-19T05:04:09Z.

P2F2's accepted verifier names R6A, P2F1, generic PRE553, the accepted I03 producer, and Node5B as construction inputs. It does not consume R6S.

P2F2 also records:

- source access during materialization = false;
- empirical outcomes computed = false.

Therefore P2F2's exact source-response→program-token relation is independent of:

- the later R6S `canonical_value=str(code)` implementation choice;
- any Candidate A/B/C output;
- any oracle outcome;
- any measured P2X result.

This proves requirement 5.

## 7. Independence is genuine, but the P2F2 object is still not itself C11 mapping authority

The sequence is important.

P2F2 first accepted and froze a semantic predicate relation:

`WVS7ResponseValue(X) EQ exact semantic comparator Y`.

R6S later chose to make C11 produce Y as:

`canonical_response_value_if_authorized`.

R6S used the wrong authority kind for that producer transformation.

The later producer error does not retroactively make the earlier predicate relation circular.

Conversely, the earlier predicate relation does not make its source-semantic authority magically become a mapping authority.

The lawful conclusion is therefore intermediate but decisive:

- **P2F2 is accepted semantic evidence sufficient to parent a derived mapping authority.**
- **P2F2 is not itself the mapping authority C11 requires.**

A future authority issuer must still issue/adopt an exact positive `NATIVE_CANONICAL_MAPPING_HARMONIZATION` object before C11 may populate the canonical response field.

This worker does not issue or adopt that object.

## 8. N1 current physical-boundary law strengthens, rather than defeats, this provenance holding

Current sealed R1E/N1 law makes:

`raw_response_value`

an opaque:

`PRE553_RAW_PHYSICAL_VALUE_WITNESS@1.0.0`

carrying exact typed physical material.

The generic facade now writes that opaque witness to `RespondentEvent.raw_response_value`.

Therefore the frozen P2F2 string tokens cannot be reinterpreted as "whatever raw physical representation happens to be present."

Under current law they are visibly a separate semantic program representation.

This court does not adjudicate the full Lock2 cost of a native-only alternative; Worker R1D-B owns that hostile comparison. But N1 removes the old shortcut by which an untransformed raw numeric value could be casually treated as the semantic token.

## 9. Exact source/use scope is already independently frozen

The accepted relation is scoped by exact refs including:

- WVS7 source SHA:
  `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- universe:
  `f9b1cdffc5783ace87d258ebe2ae1c75040ce786c373e255f53da4be4259d95e`;
- risk set:
  `0bf6a655a35617bec3e54f4d547e89282920e7835e406dcb43b3456774ab87d7`;
- exact program scope:
  `ed669953b33512f0032abc40973f85be1bede1993f6d520f901c11bcd7e8666e`;
- Q291G5:
  `4574aecc9db3ec15ba255a5e6f6ce17304ccb610c7d7d9f4b7baddc6d4a77176`;
- Q291P5:
  `304fbead4df5035bd97c02ff04000363cc5041129456555e3047ff3ff2efc185`;
- target-domain replay:
  `5d0a1ca4cc23c198a6afd4b935d425d51c7dd5cd143d056b351740c059608ef4`.

This proves requirement 4.

## 10. No cross-source equivalence premise is present or needed

P2F2's value objects and target-domain replay are explicitly WVS7-local.

The predicate relation is between exact WVS7 response semantic objects and exact WVS7 P2 program tokens.

No `SOURCE_EQUIVALENCE`, pooling, respondent linkage, backfill, or other-source semantic relation is part of the graph.

Integrated LM2 R1 law also retains the source-local/no-cross-source boundary.

Therefore requirement 6 is proved: the derivable claim can remain exact WVS7 P2 response-value transformation only.

## 11. Authority test

| Requirement | Classification | Reason |
|---|---|---|
| 1. accepted native source semantic identity | `PROVED` | R6A/P2F2 response semantics + exact WVS7ResponseValue refs |
| 2. accepted target semantic identity/value representation | `PROVED` | exact predicate `exact_value` plus independently frozen WVS7TargetDomainReplay |
| 3. exact native→target relation | `PROVED` | each accepted predicate AST hashes exact response-value ref + `EQ` + exact token |
| 4. source/use scope | `PROVED` | exact source SHA, universe, risk set, program scope, question refs |
| 5. provenance independent of candidate output | `PROVED` | P2F2 predates R6S; no R6S/candidate/outcome input; Lock2 issuance source-free |
| 6. no cross-source equivalence claim | `PROVED` | relation is WVS7-local; no source-equivalence authority or foreign source identity enters graph |

## 12. Court conclusion

The accepted P2F2 objects do more than state:

> "if some downstream producer happens to emit `Y`, compare against `Y`."

They state, at semantic predicate grain:

> "for this exact WVS7 question, this exact accepted WVS7 response semantic object is the response object tested under `EQ` against this exact program semantic value `Y`, under this exact source semantic authority, grammar authority, universe, risk set, and program scope."

That is sufficient accepted semantic provenance for a later exact derived response-value mapping authority.

It does **not** authorize:

- canonical question mapping;
- special-state mapping for `-5/-4/-2/-1`;
- cross-source equivalence;
- broader WVS response mapping;
- another wave/source;
- another program;
- any candidate-specific output.

Terminal:

`FIABC_LM2_R1D_A_P2F2_MAPPING_PROVENANCE_PASS__DERIVED_MAPPING_AUTHORITY_LAWFULLY_PARENTABLE`
