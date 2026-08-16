from __future__ import annotations

import data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke as smoke


def test_all_wave_scope_is_governed_closed_35() -> None:
    assert len(smoke.ALL_WAVES) == 35
    assert ("Asian Barometer", "W6", "") not in smoke.ALL_WAVES
    assert smoke.validate_explicit_scope(smoke.ALL_WAVES) == []


def test_scope_rejects_asian_barometer_w6() -> None:
    issues = smoke.validate_explicit_scope(smoke.ALL_WAVES + [("Asian Barometer", "W6", "")])
    assert any("W6" in issue or "outside_CLOSED_35_WAVES" in issue for issue in issues)


def test_joint_default_is_applicability_scoped_auto() -> None:
    assert smoke.DEFAULT_CONFIG.joint_mode == "auto"


def test_missing_joint_registry_is_typed_not_applicable(monkeypatch) -> None:
    monkeypatch.setattr(
        smoke,
        "_ORIGINAL_RESOLVE_JOINT",
        lambda config, family, wave, selected_vars=None: {
            "applicable": False,
            "reason": "no_explicit_joint_registry_for_family_wave",
            "registry_path": "",
        },
    )
    authority = smoke.resolve_joint_authority(smoke.DEFAULT_CONFIG, "EVS", "1981")
    assert authority["coverage_state"] == "NOT_APPLICABLE"
    assert authority["downstream_permission_status"] == "NOT_APPLICABLE"


def test_nonexecutable_joint_registry_is_coverage_debt(monkeypatch) -> None:
    monkeypatch.setattr(
        smoke,
        "_ORIGINAL_RESOLVE_JOINT",
        lambda config, family, wave, selected_vars=None: {
            "applicable": False,
            "reason": "joint_registry_status_not_executable",
            "registry_path": "registry.yaml",
        },
    )
    authority = smoke.resolve_joint_authority(smoke.DEFAULT_CONFIG, "GSS", "2010")
    assert authority["coverage_state"] == "APPLICABLE_UNRESOLVED"
    assert authority["downstream_permission_status"] == "DENY"
