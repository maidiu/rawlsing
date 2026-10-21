"""Intended real-port integration: run only with immutable BP2P4J vendor staged.
Actual source: private maidiu/rawlsing BP2P4J commit 5b3e6577400ea1d88971ae6b48e41a118b8059ae.
Port blob: 38751f36785fd935a7817483e2ef019c746e818a.
Do not replace unavailable BP2 code with an impersonation module.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'source'))

from generative_resource import candidate_resource, bp2_test_only_resources


def test_bp2_original_native_ready_port_bind_a_t_no_grant():
    from bp2_joined import bootstrap
    bootstrap.install()
    from bp2_joined import ports
    before = ports.production_registries()
    obj = bp2_test_only_resources(ports, candidate_resource(), 'TEST_ONLY_R29M_A', 10)
    assert obj['rule_a'].test_only is True
    assert obj['rule_t'].test_only is True
    assert obj['grant'] is None and obj['actual_target_mutations'] == 0
    assert obj['production_registry_writes'] == 0
    after = ports.production_registries()
    assert before['response_rule_count'] == after['response_rule_count'] == 0
    assert before['target_rule_count'] == after['target_rule_count'] == 0


def test_bp2_original_revocation_and_no_native_permission():
    from bp2_joined import bootstrap
    bootstrap.install()
    from bp2_joined import ports
    result = bp2_test_only_resources(ports, candidate_resource(), 'TEST_ONLY_R29M_A', 10)
    revoked = ports.revoke(result['rule_a'], now=10)
    try:
        ports.CAN008RulePort().bind(rule=revoked,subject='TEST_ONLY_R29M_A',
                                   conditioning_class='ResolvedStructuralContext',now=10)
    except ports.PortRefusal as err:
        assert err.code == 'RESOURCE_REVOKED'
    else:
        raise AssertionError('Revoked resource was accepted')
