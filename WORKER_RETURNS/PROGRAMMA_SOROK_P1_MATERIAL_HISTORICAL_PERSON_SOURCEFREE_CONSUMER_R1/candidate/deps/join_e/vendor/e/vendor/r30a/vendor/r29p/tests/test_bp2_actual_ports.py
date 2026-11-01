"""Run ONLY with the exact BP2P4J vendor/bp2 staged from commit
5b3e6577400ea1d88971ae6b48e41a118b8059ae.
Do NOT treat this test as evidence of native rules or original science.
"""
from test_n1_eligibility import fixture
from n1_eligibility import compile_test_only_bp2_resources

def test_real_bp2_ports_contract_no_native_registry_mutation():
    from bp2_joined import bootstrap
    bootstrap.install()
    from bp2_joined import ports
    before = ports.production_registries()
    result = compile_test_only_bp2_resources(fixture(), ports, now=10)
    assert result["status"] == "TEST_ONLY_PORTS_BOUND_NOT_ISSUED"
    assert result["rule_a"].test_only and result["rule_t"].test_only
    assert result["grant"] is None
    after = ports.production_registries()
    assert before["response_rule_count"] == after["response_rule_count"] == 0
    assert before["target_rule_count"] == after["target_rule_count"] == 0

def test_real_ports_expired_rule_fails_closed():
    from bp2_joined import bootstrap
    bootstrap.install()
    from bp2_joined import ports
    import dataclasses
    import pytest
    result = compile_test_only_bp2_resources(fixture(), ports, now=10)
    expired = dataclasses.replace(result["rule_a"], expires_at=10)
    with pytest.raises(ports.PortRefusal, match="RESOURCE_EXPIRED"):
        ports.CAN008RulePort().bind(rule=expired, subject=fixture()["actor_id"],
                                   conditioning_class="ResolvedStructuralContext", now=10)
