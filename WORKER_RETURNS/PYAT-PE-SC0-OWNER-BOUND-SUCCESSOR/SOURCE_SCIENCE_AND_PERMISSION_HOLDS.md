# Source, science and permission holds

**Candidate:** `PYAT_PE_SC0_OWNER_BOUND_SOURCEFREE_SUCCESSOR@1.0.0`

**Implementation blobs:** `owner_bound_successor.py`
`08f0bea429a8f35223db8acf757ef7b714805603`; `sourcefree_world.py`
`264c6092b5a151960779d0e610f2d964474da920`; `n10e_adapter.py`
`3c9f34fd4f629ccebd8e9efeb485f3a2d7c1c2c5`; `first_consumer.py`
`145977129dcacad6f8a7ec3d2888783a6ed0652c`.

**Exact source cuts:** original PE `e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65`
(blob `58484f4c...`), overlay `9c030bf4c239d2e14f2b5a8a02ff7b44906cd0c7`
(blob `1e4c0e63...`), issuer repair
`9647d851a2d9b6e93e6711eec7a65325fb83aaa1`, hostile review
`33b5363a20d44cfb42b3d1e86fdb9615710adb23`, current PRE-MAIN
`8e44ca9c751049d65e6def47600b5c073ee04b29`, current N10E provider blob
`23167aa25291fb148b1e3cf210ac33fe7769b783`.

**Session:** OpenCode `1.18.34`, agent `build`,
`opencode-go/deepseek-v4.1-flash`, variant `max`, session
`ses_e6f557010ffeVc8ejV937G5Ii9`, PID `28096`.

## What is actually proven

- The current N10E provider was actually invoked through
  `n10e_adapter.N10EProducer`; the forward and reverse source-free fixtures
  produce exact geometry denominators 60 and 62.
- The successor's positive court has 19 passes; the full candidate court has 33
  passes; the hostile court has 14 passes (twelve attacks plus two extra
  oracles). All exits are 0.
- The original author court remains 21 passes; the original strict court remains
  4 passes / 9 failures, exit 1. The published overlay courts reproduce 21 / 13
  / 9. The hostile predecessor court reproduces 12 attacks.
- The successor has no `sitecustomize.py`, no global monkeypatch and no
  production import.
- The selected-world owner/revision/digest, full world values, clocks,
  negative-status scope, refresh receipts, issuer scope and consumer output are
  bound into the receipt and result identities.

## What is not proven and cannot be claimed

### Source and science

The C1/N10E numbers are **synthetic source-free fixture arithmetic**. They are
not original survey responses, not a measured population, not an operative N9
world, not a causal effect, not an individual prediction, not a normative
recommendation, and not a scientific probability about real people. The
forward 54/60 and reverse 54/62 values are exact arithmetic at the declared
synthetic grain only.

No original U/E/source/SC0/N9 issuance was granted. The original strict court's
remaining nine failures are preserved; the successor does not claim to close
them by changing their assertions or by promoting fixture values into source
semantics.

### Named missing competent issuer

The required competent owner is the **original N9/world/source owner** with
authority to issue:

1. the selected-world owner identity, revision and digest;
2. the value-bearing world fields, absolute horizon and public sanctions;
3. the four clocks and observational/publication currentness;
4. the negative-status source/risk scope;
5. a positively scoped role-reversal/target-use grant for the exact target and
   risk set; and
6. any source-observation promotion right.

That owner and grant are **absent** in this worktree. The candidate's only issuer
is a `TEST_ONLY_SOURCEFREE` exact grant. It is not competent for source
promotion, model use, N9/world adoption, actor/person state, N11/N12 or
production.

### Exact missing operations

- `ISSUE_OWNER_BOUND_SELECTED_WORLD_GRANT`: not available.
- `ISSUE_OWNER_BOUND_ROLE_REVERSAL_GRANT`: only the test fixture version exists.
- `AUTHORIZE_SOURCE_OBSERVATION_PROMOTION`: no competent source issuer.
- `AUTHORIZE_MODEL_USE`: no competent model-use issuer.
- `ADOPT_ENRICHED_RECEIPT_AS_CURRENT_PRODUCTION_CONTRACT`: no production
  receiver.
- `INDEPENDENT_POST_RETURN_REVIEW`: not performed by this author.

## Permission matrix

| Permission | Status | Basis |
|---|---|---|
| Source-free local pytest | GRANTED / USED | user commission; no source read |
| Source observation | NOT GRANTED | no competent source issuer |
| Operative N9/selected world | NOT GRANTED | synthetic fixture world only |
| Model use / N10W joint use | NOT GRANTED | no model-use issuer |
| Sorok actor / person state | NOT GRANTED | no actor issuer |
| N11/N12 | NOT GRANTED | not issued |
| Production / deployment | NOT GRANTED | no adopter, no merge |
| Self-review / self-acceptance | FORBIDDEN / NOT PERFORMED | independent review required |
| PRE-MAIN merge | FORBIDDEN / NOT PERFORMED | no merge |

## Commands and outcomes

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/SOURCEFREE_CANDIDATE_AND_VERSIONED_API/tests
# 33 passed, exit 0

HQ297_EXACT_PE_ROOT=$PWD PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py
# 21 passed, exit 0

HQ297_EXACT_PE_ROOT=$PWD PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py
# 4 passed / 9 failed, exit 1
```

Overlay and hostile predecessor receipts are under
`SOURCEFREE_CANDIDATE_AND_VERSIONED_API/evidence/`.

## Explicit NOT_RUN / UNKNOWN

- Original respondent/source/U/E/N9/model/actor/N11/N12/Sorok operation:
  **NOT_RUN**.
- P41/E04L and #536 worker suites: **NOT_RUN**; source inspection only.
- Production adoption, deployment or merge: **NOT_RUN**.
- Independent post-return review: **NOT_RUN**.
- MAX beyond process argv `--variant max`: **UNKNOWN**.

## Verdicts

**ENGINEERING:** `ACCEPT_AT_TEST_ONLY_SOURCEFREE_SCOPE__ENGINEERING_ORACLES_AND_HOSTILE_ATTACKS_GREEN__PRODUCTION_ADOPTER_ABSENT`.

**SCIENTIFIC:** `HOLD__SYNTHETIC_C1_N10E_ARITHMETIC_ONLY__NO_ORIGINAL_RESPONDENT_EVIDENCE__NO_WORLD_OR_CAUSAL_MEANING`.

**AUTHORITY:** `HOLD__NO_COMPETENT_SOURCE_N9_WORLD_MODEL_ACTOR_N11_N12_OR_PRODUCTION_GRANT__TEST_ONLY_SOURCEFREE_ONLY`.
