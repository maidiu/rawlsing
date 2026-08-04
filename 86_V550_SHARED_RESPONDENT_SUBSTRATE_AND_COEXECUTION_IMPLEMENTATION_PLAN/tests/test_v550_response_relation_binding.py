from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_CODE = REPO_ROOT / "35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE" / "runtime_reproducibility_code"
if str(RUNTIME_CODE) not in sys.path:
    sys.path.insert(0, str(RUNTIME_CODE))

from data.ddm_build_copy.ddm_v550_response_relation import (  # noqa: E402
    choose_response_relation,
    scope_manifest_from_response_rows,
)
from data.ddm_build_copy import build_determinicity_repository_v550 as repo_builder  # noqa: E402
from data.ddm_build_copy import run_20var_allwaves_v550_552j_smoke as smoke  # noqa: E402


def test_auto_prefers_authority_enriched_response_relation() -> None:
    available = {
        "public.v_ddm_response_long_facet_ready",
        "public.v_ddm_response_long_facet_ready_authority",
    }
    assert choose_response_relation(available, "auto") == "public.v_ddm_response_long_facet_ready_authority"


def test_explicit_historical_response_relation_is_respected() -> None:
    available = {
        "public.v_ddm_response_long_facet_ready",
        "public.v_ddm_response_long_facet_ready_authority",
    }
    assert (
        choose_response_relation(available, "v_ddm_response_long_facet_ready")
        == "public.v_ddm_response_long_facet_ready"
    )


def test_missing_explicit_response_relation_fails_closed() -> None:
    with pytest.raises(RuntimeError, match="V550_RESPONSE_RELATION_MISSING"):
        choose_response_relation(
            {"public.v_ddm_response_long_facet_ready"},
            "public.not_a_real_relation",
        )


def test_response_relation_scope_fallback_normalizes_source_and_wave_aliases() -> None:
    rows = pd.DataFrame(
        [
            {
                "source": "World Values Survey",
                "wave": "Wave 1",
                "canonical_wave": "W1",
                "country_code": "SE",
                "respondents": 987,
            },
            {
                "source": "GSS",
                "wave": "2010",
                "canonical_wave": "2010",
                "country_code": "US",
                "respondents": 2044,
            },
        ]
    )
    scoped = scope_manifest_from_response_rows(
        rows,
        requested_source="WVS",
        requested_wave="W1",
        countries=["SE"],
    )
    assert scoped.to_dict("records") == [
        {"source": "WVS", "wave": "W1", "country_code": "SE", "respondents": 987}
    ]


def test_question_mapping_retries_with_canonical_source_family_alias(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(repo_builder, "question_structural_mapping_select_columns", lambda conn: [
        "source", "wave", "var_code", "question_id", "loaded_at"
    ])
    monkeypatch.setattr(
        repo_builder,
        "cached_query_frame",
        lambda namespace, payload, query_fn, **kwargs: query_fn(),
    )
    calls: list[dict] = []

    def fake_read_sql(sql, conn, params=None):
        calls.append({"sql": sql, "params": params})
        if "WHERE source =" in sql:
            return pd.DataFrame(columns=["source", "wave", "var_code", "question_id", "loaded_at"])
        return pd.DataFrame(
            [
                {
                    "source": "World Values Survey",
                    "wave": "W1",
                    "var_code": "A001",
                    "question_id": "WVS.W1.A001",
                    "loaded_at": "2026-08-03",
                },
                {
                    "source": "GSS",
                    "wave": "W1",
                    "var_code": "OTHER",
                    "question_id": "GSS.W1.OTHER",
                    "loaded_at": "2026-08-03",
                },
            ]
        )

    monkeypatch.setattr(repo_builder.pd, "read_sql_query", fake_read_sql)
    frame = repo_builder._load_wave_question_mapping(object(), "WVS", "W1")
    assert len(calls) == 2
    assert frame[["source", "wave", "var_code"]].to_dict("records") == [
        {"source": "WVS", "wave": "W1", "var_code": "A001"}
    ]


def test_smoke_runner_forwards_auto_response_relation_to_v550(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    captured = {}

    def fake_invoke(cmd, timeout_sec=None, config=None):
        captured["cmd"] = cmd
        return {"exit_code": 0, "stdout_tail": "", "stderr_tail": "", "elapsed": 0.0}

    monkeypatch.setattr(smoke, "_invoke_run", fake_invoke)
    config = smoke.RuntimeConfig(
        repo_root=REPO_ROOT,
        env_file=tmp_path / ".env",
        response_long_relation="auto",
    )
    smoke.run_v550_shard(
        "run",
        "WVS_W1_SE",
        "WVS",
        "W1",
        "SE",
        str(tmp_path / "filter.json"),
        str(tmp_path / "out"),
        None,
        config,
    )
    cmd = captured["cmd"]
    index = cmd.index("--response-long-relation")
    assert cmd[index + 1] == "auto"
