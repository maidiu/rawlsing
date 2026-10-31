# S6 NEGATIVE, DEFECT AND SOURCE-AUTHORITY REGISTER

**Return branch:** `agent/pyat-rabochii-845-s6-successor-consumer-crosswalk-20261030-r1`  
**Baseline PRE-MAIN:** `750548ddbb9b4392a16ce93097b856f349e16182`  
**Actual PRE-MAIN:** `5fc1d43e3d5412194d1f1eaa30ff448f84635e99`; identical `rawlsing_next` tree `1d88d3fbb1d18dadfda946d9cd7f309d84afa479`.  
**Rule:** a negative is retained against the exact scope where it was reproduced. A test pass, a larger body, a path absence or a branch-level token does not erase it.

---

## 1. Reproduced engineering negatives

| Case | Exact negative | Evidence | Current status |
|---|---|---|---|
| R61-R09 D1 | Parent seals a child-authored observation; actual return 41 can be sealed as 42 through a monkeypatched `json.dump`. | `agent/opencode-pyat-r61-r09v-r2-independent-review-r1@25510c8d84f0ae5e452b301b017bdedf46f40b5c`, `revisions/r2/00_RETURN.md` blob `c2632d2c…` | No current capture owner; deployment hold. |
| R61-R09 D4 | Child-reported loaded bytes: fabricated `loaded_sources` digest carrying the benign tree digest is accepted while loaded code returns 41. | same | same |
| R61-R09 D7 | Malformed non-JSON expectation raises `TypeError` instead of typed refusal. | same | same |
| Selected-world seam | Author-reported 18/60 contradicted by actual `26 passed / 1 failed`; `test_s00c_change_source_owned_synthetic_numeric_values_changes_result` fails with `KeyError: 'exact_probabilities'`. | S3 actual sourcefree receipt at `ed34944e253b78714a28d72b8ca2a6521ce15930` | Current E03 exact only; selected-world contract absent; RED. |
| PE `_auth` | Reverse-scoped issuer forgery is not refused; independent strict court `4 passed / 9 failed`. | S3 actual receipt at `e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65`, PE blob `58484f4c…` | `_auth` `PROVEN_DEFECTIVE_AT_DECLARED_SCOPE`; RED. |
| V2K collection | Exact branch cannot collect: missing `pre553_original_workload_contract_v2_candidate`; reported 24+111 passes not reproduced. | S3 receipt at `694fb45085cd5e4891949921a44edb77c3f603f2` | Collection error; science hold. |
| R56 consumed-byte custody | Source identity can be attached to C11/I03 facts built from replacement bytes through the content-verification-to-reader window; post-addition 2 failed / 17 passed. | R56-R04BYTEV review; S2/S4 rows | Current decoder is a different implementation; no current behavioral equivalence proof. |
| F7/P07 RR-04F/G | Live authenticated owner state exposed/post-construction replaceable; lexical custody cell caller-rebindable; narrower coordinated substitution reproduced. | HQ228, HQ232, HQ236; S4/S5 rows | Sealed-owner functions `DEFECTIVE_BLOCK`; current resolver `5b67e3f98a5f…` retained. |
| F7/P07 TCB | Writable module-global `_authenticated_source_relation_decide`; terminal receipt content-addressed but not issuer-authenticated. | HQ240; S4/S5 rows | F7 path absent; TCB/science hold. |
| Native Stage A/B | Constructor OOB/SIGSEGV; malformed `PyObject_Call`; `PyErr_Fetch` NULL traceback; non-str replay crash; positive parity; caller-selected trusted callables; decide leak; Stage B quarantined. | HQ245–HQ248; S5 rows | Native C not adopted; no build/import by S6. |
| B5 exact holds | Ceiling, tautology, replay, authority and event-attribution holds; no issuer; test-only overlay. | HQ281 C02J return; S2 rows | Sourcefree candidate with exact holds, not current. |
| Learned lifecycle | Branch receipts report 194 failed / 1690 passed / 30 skipped (and 40 failed / 2 passed in another carrier). | S2 rows | Review-revise; current same-symbol shorter comparison unproven. |
| R8 binder limits | Full live J42/E41, live P41 progressive and repaired live E04 are NOT_REACHED. | R61-R08V R8 return | Scoped-local acceptance only. |
| R9 current conflict | R9 branch decoder `b406d45fae41…` routes through broker/session but lacks PR526 `_SourceSnapshot` read-only/stable/TOCTOU custody. | S5 function/import comparison | Do not drop current custody. |
| C3 current drift | Current decoder `8732e34d…` / R5 `72f8f3c0…` lack C3 G01/D01/D02; C3 branch lacks PR526 source custody. | S5/S4 rows; current blobs | Port required; no wholesale replacement. |

---

## 2. Scientific and source-authority holds

| Operation | Required authority | Status in S6 | Lawful sourcefree work |
|---|---|---|---|
| Source-native read of original survey/response bytes | Competent source custodian / original source owner, exact source identity, purpose, target operation | `REQUIRED_UNGRANTED`; issuer not named in the recovered evidence | Sourcefree synthetic decode/ABI/schema/fault-negative tests remain allowed. |
| Original scientific rule/estimand/method issuance | CAN/ADP/Pyat/SCI05 competent original-science owner | `REQUIRED_UNGRANTED` for F7, PE/V2K, selected-world, R157 original U/E_pre, R61 full universe | Sourcefree arithmetic/schema/diagnostic tests remain allowed. |
| Model use | Model-use owner with exact model/use/permission tuple | `REQUIRED_UNGRANTED` for PE/selected-world/N9/N10W implications | Sourcefree interface tests allowed; no model-use claim. |
| World structural admission / N9 / N10W | N9/N10W world authority + HQ; exact retained products and consumer | `REQUIRED_UNGRANTED` | P41/E03/selected-world sourcefree service tests allowed. |
| N11/N12 acceptance / wake | Competent N11/N12 court | `NOT_GRANTED`; no claim | No sourcefree substitute for N11/N12. |
| Sorok actor/person authority | Sorok actor owner; actor firewall | `NOT_GRANTED`; no actor/person inference | Actor-free sourcefree tests only. |

The S6 return does **not** grant, infer or self-issue any source, science, model, world, actor, N11/N12 or Sorok permission.

---

## 3. Sourcefree work that is not blocked by the holds

The following may proceed under an independent sourcefree court without an original-source grant:

- R61-R08 binder ABI/schema/descriptor diff and sourcefree positive/fault-negative replay against current C1/N10E/J42/P41 receivers.
- R61-R03 current code contract comparison and mutation witnesses on the current receiver.
- P41 service port and 19-test/3-witness replay on current E03/C1/N10E/M4/M5 (N10W/N9 claims still held).
- C3 G01/D01/D02 and R5 carrier port with synthetic SAV/date-time fixtures; native source read still held.
- R9 broker/session/binding integration and broker/session/binding/R7 tests on synthetic sources; native source-path read still held.
- F7 temporal arithmetic/scope helper tests and HQ232/HQ236 negative replay; sealed P07 owner promotion is not allowed.
- Selected-world seam repair and 27-test replay; N9/N10W/actor claims still held.
- PE typed/schema helper tests and `_auth` repair tests; PE/science adoption still held.
- V2K dependency restoration and exact four-suite replay; original identity/science adoption still held.
- R157 mapping of 35 configurations to current source-local-universe/source-equivalence; original U/E_pre execution still held.

S6 did not execute any of these tests.

---

## 4. Original reviewer negatives preserved as testimony

- S1: all 73 `SUPERSEDED_BETTER` claims downgraded to `DIFFERENT__COMPARISON_REQUIRED`; 331 blanket holds replaced by operation-specific axes; 299 adaptation claims downgraded to hypotheses; 34 unknown rows retained; 542 exact rows code-presence only.
- S2: 10 `SUPERSEDED_BETTER` downgraded; 67 HELD split; 22 NEEDS split; 105 UNKNOWN assigned explicit causes; 106 evidence-only branches preserved; R56 defect preserved; D02ZR resolved as nonissuing evidence.
- S3: seam 26/1, PE 4/9, V2K collection error, selected-world 24 pass, E03 18 pass; 288 test rows `NOT_PRODUCT_CODE`; `_auth` defective at declared scope.
- S4: 171 original trash reduced to evidence-only or review-revise; 121 blanket holds replaced with sourcefree candidates/permission axes; 202 unknown retained; 326 exact rows presence-only; F7/P07 negative preserved.
- S5: 119 READY downgraded to historical accepted/current untested; 6 SUPERSEDED downgraded; 11 F7/P07 invalid preserved; 101 adaptation split; 86 code-identity rows no-action; 249 path-absent unresolved; 228 permission-required rows.

---

## 5. Unresolved and insufficient evidence

- 442 groups remain `CURRENT_UNKNOWN`; 348 `CURRENT_PATH_ABSENT_UNRESOLVED`; 65 `CURRENT_REFERENCE_ONLY_UNPROVEN`; 49 `CURRENT_TEST_REFERENCE_ONLY`.
- 841 groups are evidence-only/test/repro/reviewer material and are not production recovery candidates.
- Origin order is unproven for groups without a dated branch tip; earliest tip is a candidate, not proven authorship.
- Current first consumers are text-reference candidates only; no executed callgraph was produced.
- Historical test receipts are branch-level; where function-scope attribution was not proved, it is marked accordingly.
- The two external priority cases (P41 service, R61-R09 negative) are not part of the 3,135 original function rows and are identified as external.

---

## 6. Independent review condition

This register is not an H1/S7 acceptance. H1 #534 independent review and S7 #538 hostile reviewer must inspect the exact S6 return SHA and the specific priority cases. No author self-review, no PRE-MAIN merge and no authority self-grant.
