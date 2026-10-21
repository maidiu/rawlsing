# N1 / execution and consumer contract — what was actually run

## Physical execution
Executed isolated Python 3.13.5 / pytest 9.0.2 / git available. Local staging path /mnt/data/n1_worker, **not user's Mac** and not a full private Git checkout. Source file n1_eligibility.py locally has Git blob 03b7e092c87c7133313598ca024948ef030b70bb (same remote blob); test_n1_eligibility.py has Git blob bff019ef8ab01c9429c7c4b41096d305c8adc8d9 (same remote blob). Remote GitHub fetch confirmed exact parity after publication. One directly executed command: cd /mnt/data/n1_worker && python3 -m pytest -q test_n1_eligibility.py; **21 passed, 0 failed, 0 skipped, 0.04s** on final rereun. Observed Python native stdout 21 dots and result. Testing a source-neutral deterministic method does NOT prove original scientifically meaningful acquired practice.

Local source sha256: 803ede6090b520b9d64d4fc7e541602481e41581cc15dcedc1b146a843533993.
Local 21-test sha256: 199d6ce71eb37e21435073465845cba3494f48daf8d69cea4bf45654fd84c181.

Exact notable tests: positive screen **OWNER_REVIEW_CANDIDATE** with *all native-rule and actor fact flags false*; E1 removal REQUEST_EVIDENCE; no encounter REQUEST_EVIDENCE; one enacted action REQUEST_EVIDENCE; missing other offer NO_CHANGE; no action NO_CHANGE; same owner duplicated action cannot qualify; role prior and self-narration do not qualify; contrary action COMPETING rather than synthesized; unknown self-knowledge remains UNKNOWN_WITHOUT_ADP017; wrong actor/foreign owner/tampered hash/duplicate receipt/future cause/bad clock DENY; record order invariance; positive screen without actual BP2 ports raises ACTUAL_BP2_PORTS_REQUIRED. A refusal or request for evidence in the screen is NOT a CAN008 valid-empty transaction nor CAN011 persisted NO_CHANGE; these latter statuses belong to the actual owner engine.

### Contract to the REAL BP2 native-ready receiver
The existing immutable BP2P4J vendored physical file vendor/bp2/bp2_joined/ports.py Git blob 38751f36785fd935a7817483e2ef019c746e818a (read at BP2P4J return 5b3e6577400ea1d88971ae6b48e41a118b8059ae) defines:
- Resource with exact source_owner, issuer_grade, content_hash, version, effective_from/expires_at/revoked/currentness_as_of and readset_refs; native_grant remains NOT_GRANTED.
- CAN008RulePort.bind(rule,subject,conditioning_class,now) checks exact rule_semantics digest/issuer/subject/readset and currentness.
- CAN011TargetPort.bind_rule(rule,now) independently requires rule_t_content_hash and response_rule_content_hash dependency plus a DISTINCT source owner.
- CAN011TargetPort.bind_grant(grant,rule,actor_id,response_hash,before_target_hash,now) requires external owner grant and exact readset.
- E2OwnerPort.bind separately requires real performed receipt bound to consumed_state_hash and target clock.
- production_registries() checks both current production rule registries EMPTY.

Our source/n1_eligibility.py::compile_test_only_bp2_resources(case,ports,now=...) is an actual callable adapter written for these exact names and content hashes. It creates only separate TEST_ONLY sourcefree methodology A/T resources (TEST_ONLY_N1_CAN008_OWNER / TEST_ONLY_N1_CAN011_OWNER), passes them through CAN008RulePort.bind and CAN011TargetPort.bind_rule, returns grant=None, native_registry_mutation=False, downstream_state_change=False. It never invokes CAN011TargetPort.bind_grant, writes a target, issues current rule authority, promotes source identities, or sets native_grant to GRANTED. Actual future producer must inject independently accepted current A/T and grant; test-only science method alone may not clear the release gate.

**NOT_RUN**: tests/test_bp2_actual_ports.py physically imports the EXACT vendor/bp2/bp2_joined package (with bootstrap.install()) and calls these ports, proving empty production registries and a revoked-resource fail-closed when executed. That private vendored source was not staged into the isolated container; no misleading claim that this integration was locally executed. To run in a real qualified clone/copy with exactly the pinned vendor tree:
PYTHONPATH=WORKER_RETURNS/SOROK-20261020-N1-NATIVE-ELIGIBLE-PSYCHE-SCIENCE-R1/source:WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1/vendor/bp2 python3 -m pytest -q WORKER_RETURNS/SOROK-20261020-N1-NATIVE-ELIGIBLE-PSYCHE-SCIENCE-R1/tests/test_bp2_actual_ports.py
The BP2P4J vendor and source manifest must first be verified byte-for-byte at the pinned BP2P4J commit, and Python packages actually import; otherwise NOT_RUN/typed execution failure, not pseudo-green. This integration tests *port compatibility*, not whether the packet ought scientifically to produce person change.

## Empirical/fault grade matrix
| Original tested dependency | Actual N1 screen status | What physical end-user consumer still needs |
| --- | --- | --- |
| all TEST_ONLY typed ref/history/currentness props | OWNER_REVIEW_CANDIDATE, native false | current original CAN008/CAN011 source/actor grant; C9 actual response, A0/A2 real |
| remove ADP019 E1 | REQUEST_EVIDENCE | cannot create native C9 causal response |
| remove ADP010 encounter | REQUEST_EVIDENCE | co-presence does not equal contact |
| remove A history / B independent offer | NO_CHANGE | current CAN011 NO_CHANGE must be owner decided |
| contradictory independent action | COMPETING | two contradictory CAN011 states may coexist if duly issued; not compulsory effect |
| duplicate act or actor ID, forged hash/source, reversed time | DENY | no owner admission or time-travel |
| later E2 not independent | Outside N1 screen; BP2P4J physically proved TEST_ONLY E2 source severance | actual separate performer/ADP019 native event and C8 |
| RULE_A response row / RULE_T authorization / committed target cut | N1 test does not exercise persistence | existing BP2P4J seven same assertion severances are inherited and reported at L1 only |
| actor-access withheld | N1 does not render | BP2P4J M6/A0 access severance inherited at L1 only |

## Critical limits and correction target
The current sourcefree evidence screen checks exact technical namespace+content hash, but DOES NOT authenticate the original owner of a real act: a TEST_ONLY caller can coherently produce all those names. It also checks merely that two independently named technical source owners recorded distinct events; this is a **test methodology precondition**, not proof that two humans or two truly independent instruments existed, nor proof of acquired practice. The primary original-scientific bottleneck is competent independent causal-use source evidence and a substantiated practice-formation rule, not deterministic hashing. No true actor, native psychogenesis, scientific calibration, Pyat original source, C8 production key/anchor, L2 native person, C11 weld or A4/A5 tested.

## Test plan for full original owner lane
Run the real owner source→BP2 ports and the unchanged bp2p4.assertion.joined_downstream_a0_a2_assertion in one qualified state. For each source edge: (a) positive actual owner receipt and currentness; (b) selective physical source mutation that must turn SAME A0/A2 assertion RED; (c) restore exact source PASS; (d) valid NO_CHANGE with E1 retained, target unchanged and downstream no artificial practice; (e) independently false B offer and performed E2 denials. Separately compare H1/H2/H3/H0 on matched opportunities; do not claim empirical scientific validity from tests alone.
