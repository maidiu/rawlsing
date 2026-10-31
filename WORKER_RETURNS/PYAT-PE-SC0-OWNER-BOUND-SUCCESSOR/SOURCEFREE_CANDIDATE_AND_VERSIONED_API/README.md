# TEST_ONLY_SOURCEFREE owner-bound PE/SC0 successor

Contract: `PYAT_PE_SC0_OWNER_BOUND_SOURCEFREE_SUCCESSOR@1.0.0`

This is a bounded source-free successor, not a production PE/SC0 module and not
an N9/source/model/actor issuer. It has no `sitecustomize.py`, no import hook and
no global monkeypatch. Every dependency is explicit:

- an actual N10E empirical provider result via `n10e_adapter.N10EProducer`;
- an explicit source-free world provider via `sourcefree_world.SourceFreeWorldProvider`;
- an exact scoped test-only issuer registry via
  `owner_bound_successor.ExactIssuerRegistry`;
- an explicit receiving consumer via
  `first_consumer.SourceFreeWorldRouteConsumer`.

The receipt binds the request, producer evidence, issuer grant, selected-world
owner/revision/digest, all world values, four clocks, negative-status rows,
generated-binding echo, both actually invoked refresh receipts, the exact
C1/N10E geometry, the consumer output and the full epistemic ceiling into one
semantic identity. A typed refusal carries no world, geometry or consumer
output.

## Run

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT-PE-SC0-OWNER-BOUND-SUCCESSOR/SOURCEFREE_CANDIDATE_AND_VERSIONED_API/tests
```

The positive court executes the actual N10E/C1 synthetic producer and checks
cold replay, world binding, all-fields result identity, geometry conservation,
refresh execution, issuer scope, consumer receipt and the TEST_ONLY grade.

The hostile court reproduces all twelve commissioned attacks and asserts each
fails closed with a typed refusal and no receipt.

## Non-adoption

The only issuer in this candidate is a test-only exact grant. It is not a
competent source, N9, world, model-use, Sorok actor, N11/N12 or production
issuer. The source-free world is synthetic fixture material. The in-candidate
consumer is a receiving test, not an operative production receiver. Any
production use requires a named competent owner grant and an independent
adopter; neither is present here.

## Provenance, receipts and verdicts

**Session:** OpenCode `1.18.34`, agent `build`,
`opencode-go/deepseek-v4.1-flash`, variant `max`, session
`ses_e6f557010ffeVc8ejV937G5Ii9`, PID `28096`, worktree
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pe-sc0-owner-bound-secure-successor-20261031-r1`.

**Exact cuts:** branch startup `d0342290b257f85c3e8931f9962e0aecabc84ed3`;
current PRE-MAIN `8e44ca9c751049d65e6def47600b5c073ee04b29`; current N10E
provider blob `23167aa25291fb148b1e3cf210ac33fe7769b783`; C1 composition blob
`604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`; F8 consumer blob
`62e5eced47b64512f47b004e3e13a6ef3fe21de7`.

**Implementation blobs:** `owner_bound_successor.py`
`08f0bea429a8f35223db8acf757ef7b714805603`; `sourcefree_world.py`
`264c6092b5a151960779d0e610f2d964474da920`; `n10e_adapter.py`
`3c9f34fd4f629ccebd8e9efeb485f3a2d7c1c2c5`; `first_consumer.py`
`145977129dcacad6f8a7ec3d2888783a6ed0652c`; `fixtures.py`
`6f3233945aadcf92730a7e77ad301e1a07c52414`; positive tests
`5a3558f7e60b1afc70210ef5cb1c69fd459049b1`; hostile tests
`37ad5b63ed2be6fa6b87ee4e93483e51de5b2865`.

**Actual outcomes:** candidate all `33 passed` exit 0; positive `19 passed`
exit 0; hostile `14 passed` exit 0; candidate at current PRE-MAIN `8e44ca9`
`33 passed` exit 0; original author `21 passed` exit 0; original strict
`4 passed / 9 failed` exit 1; fixture overlay `21 / 13 / 9` passed exit 0;
hostile predecessor `12` attacks reproduced exit 0. Receipts are in
`evidence/`.

**NOT_RUN / UNKNOWN:** P41/E04L and #536 worker suites NOT_RUN; original
survey/actor/N9/model/N11/N12/Sorok operations NOT_RUN; production adoption,
merge and independent post-return review NOT_RUN; MAX availability beyond the
verified process argv `--variant max` UNKNOWN.

**ENGINEERING:** `ACCEPT_AT_TEST_ONLY_SOURCEFREE_SCOPE__ORACLES_AND_HOSTILE_ATTACKS_GREEN__PRODUCTION_ADOPTER_ABSENT`.

**SCIENTIFIC:** `HOLD__SYNTHETIC_C1_N10E_ARITHMETIC_ONLY__NO_ORIGINAL_SOURCE_OR_WORLD_MEANING`.

**AUTHORITY:** `HOLD__TEST_ONLY_SOURCEFREE_GRANT_ONLY__NO_COMPETENT_SOURCE_N9_WORLD_MODEL_ACTOR_OR_PRODUCTION_AUTHORITY`.
