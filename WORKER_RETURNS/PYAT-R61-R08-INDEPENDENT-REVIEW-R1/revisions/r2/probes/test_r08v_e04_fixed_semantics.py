from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace


def _load_actual_e04():
    path = Path(__file__).with_name("e04_nonparent_actual.py")
    spec = importlib.util.spec_from_file_location("r08v_e04_nonparent_actual", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class _FixedService:
    def __init__(self):
        self.value_reads = []

    def structural(self, snapshot, key, consumer):
        values = {
            "training_access": True,
            "training_fee": 2,
            "exit_cost": 2,
            "civil_open": True,
            "civil_sanction": False,
        }
        self.value_reads.append(
            {
                "consumer": consumer,
                "channel": "structural",
                "scope": key,
                "state": "SUPPORTED_TEST_ONLY",
                "value_read": values[key],
            }
        )
        return {"state": "SUPPORTED_TEST_ONLY", "value": values[key]}

    def possibilities(self, snapshot, *, consumer):
        return {
            "state": "PRODUCTIVE_TEST_ONLY",
            "steps": [
                {
                    "target": "POSITIONED_SUBJECT_TARGET",
                    "conditioners": [["POSITION", {"tag": "STRING", "value": "P3"}]],
                    "state": "ZERO_SUPPORT",
                    "denominator": 0,
                    "cells": [],
                    "evidence_ref": None,
                }
            ],
        }

    def _record(self, material):
        return {"material": material}


def test_actual_unchanged_e04_top_level_success_survives_zero_support_step():
    e04 = _load_actual_e04()
    receipt = e04.consume(
        _FixedService(),
        SimpleNamespace(snapshot_hash="r08v-e04-fixed-snapshot"),
        budget_tokens=5,
    )
    material = receipt["material"]
    assert material["state"] == "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
    assert material["source_balance_reads"][0]["support_state"] == "ZERO_SUPPORT"
    assert material["source_balance_reads"][0]["denominator"] == 0
    assert material["empirical"]["steps"][0]["state"] == "ZERO_SUPPORT"
