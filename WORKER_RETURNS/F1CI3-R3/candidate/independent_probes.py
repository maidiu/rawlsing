"""Independent F1CI3 probes; findings are observations, not candidate repairs."""
import copy
import dataclasses
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import f1c as F


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()).hexdigest()


def prior(life):
    return {
        "A": {"snapshot": life.a_snapshot, "events": [dataclasses.asdict(e) for e in life.a_ledger.events]},
        "B": {"snapshot": life.b_snapshot, "events": [dataclasses.asdict(e) for e in life.b_ledger.events]},
        "shared": {"material": life.material, "witness": life.witness, "objective": life.objective},
    }


def main():
    replay = json.loads((HERE / "replayed_results.json").read_text())
    authored = json.loads((HERE / "01_FIXED_A_B_WORLD_AND_MATERIAL_CONSERVATION_MATRIX.json").read_text())
    assert replay["frozen"] == authored["frozen"]
    assert digest(replay["frozen"]) == replay["frozen_hash"] == authored["frozen_hash"]
    roots = {key: digest(value) for key, value in replay["frozen"]["prior"].items()}
    rows = {r["case"]: r for r in replay["results"]}
    for name, row in rows.items():
        original = next(x for x in authored["results"] if x["case"] == name)
        assert row["observed"] == original["observed"]
        assert row.get("hold") == original.get("hold")
        if row.get("receipt"):
            assert row["receipt"]["baseline_hash"] == replay["frozen_hash"]
    baseline, cut, restored = [rows[n]["receipt"] for n in ("SHARE", "B_SOURCE_SEVERED", "B_SOURCE_RESTORED")]
    assert baseline["world_after"] == cut["world_after"] == restored["world_after"]
    assert baseline["terminal_tool_ledger"] == cut["terminal_tool_ledger"] == restored["terminal_tool_ledger"]
    assert baseline["terminal_material_ledger"] == cut["terminal_material_ledger"] == restored["terminal_material_ledger"]
    assert baseline["p01"] and not cut["p01"] and restored["p01"]
    assert cut["action"]["admitted"] and not cut["B_source_admitted"]
    assert rows["E2_OMITTED"]["receipt"]["terminal_tool_ledger"] == {"A": 1, "B": 0, "spent": 0}
    assert rows["E2_OMITTED"]["receipt"]["terminal_material_ledger"] == {"A": 4, "B": 0, "spent": 0}
    assert rows["UNOBSERVED_SHARE"]["receipt"]["access"]["A_tool"]
    assert not rows["UNOBSERVED_SHARE"]["receipt"]["access"]["A_B_act"]
    assert rows["REFUSE"]["source_context"]["test_intervention"]["kind"] == "TEST_ONLY_INTERVENTION"
    assert rows["SILENCE"]["source_context"]["test_intervention"]["kind"] == "NON_EVENT_CONDITION"
    assert rows["SILENCE"]["source_context"]["test_intervention"]["performer"] is None
    observations = []
    with tempfile.TemporaryDirectory(prefix="f1ci3-probes-", dir=HERE) as tmp:
        root = Path(tmp)
        # A fresh baseline externally checks complete live history preservation.
        life, frozen, frozen_hash = F.freeze()
        before = copy.deepcopy(prior(life))
        positive = F.same_receiver_assertion(root / "full_prior_positive", life, frozen, frozen_hash)
        assert prior(life) == before == frozen["prior"] and positive["p01"]
        observations.append({"id": "FULL_LIVE_PRIOR_BASELINE", "preserved": True, "roots": roots})
        # The sealed frozen record and the live consumer inputs are separate objects.
        for actor in ("A", "B"):
            life, frozen, frozen_hash = F.freeze()
            ledger = life.a_ledger if actor == "A" else life.b_ledger
            event = next(e for e in ledger.events if e.kind == "RELATION_VIEW")
            old = copy.deepcopy(event.payload)
            event.payload["perceived_state"] = "F1CI3_POST_FREEZE_DRIFT"
            valid, errors = ledger.verify()
            row = {"id": f"LIVE_{actor}_LEDGER_DRIFT", "frozen_root_unchanged": digest(frozen) == frozen_hash,
                   "live_prior_matches_frozen": prior(life) == frozen["prior"],
                   "ledger_valid": valid, "ledger_errors": errors, "before_payload": old,
                   "after_payload": event.payload}
            try:
                receipt = F.same_receiver_assertion(root / actor, life, frozen, frozen_hash)
                row.update(consumer="ACCEPTED", p01=receipt["p01"], cold_effect_equal=receipt["cold_effect_equal"])
            except Exception as error:
                row.update(consumer="REFUSED", refusal=type(error).__name__ + ":" + str(error))
            observations.append(row)
        life, frozen, frozen_hash = F.freeze()
        life.witness["status"] = "F1CI3_POST_FREEZE_NOT_WITNESSED"
        row = {"id": "LIVE_SHARED_WITNESS_DRIFT", "frozen_root_unchanged": digest(frozen) == frozen_hash,
               "live_prior_matches_frozen": prior(life) == frozen["prior"], "live_witness_status": life.witness["status"]}
        try:
            receipt = F.same_receiver_assertion(root / "shared", life, frozen, frozen_hash)
            row.update(consumer="ACCEPTED", p01=receipt["p01"], cold_effect_equal=receipt["cold_effect_equal"])
        except Exception as error:
            row.update(consumer="REFUSED", refusal=type(error).__name__ + ":" + str(error))
        observations.append(row)
        for action in ("REFUSE", "SILENCE"):
            life, frozen, frozen_hash = F.freeze()
            _, post, source, record = F.intervene(frozen, action)
            producer = F.Receiver(root / ("c9_" + action), life, frozen, post, source)
            try:
                producer.stage_world(); producer.stage_c8(); producer.stage_out9()
                pipeline = producer.stage_c9()
                decision = pipeline.decision
                row = {"id": "TARGETLESS_C9_" + action, "committed": pipeline.committed,
                       "branch": decision.branch.value, "reason": decision.reason.value,
                       "target_id": decision.target_id, "c8_state_digest": producer.out9.readset["state_digest"],
                       "typed_intervention": record, "world_after": post}
                try:
                    producer.stage_e2()
                    row["later_e2"] = "ACCEPTED"
                except Exception as error:
                    row["later_e2"] = type(error).__name__ + ":" + str(error)
                from bp4.c10 import _read_c9
                try:
                    _read_c9(SimpleNamespace(c9_path=producer.c9.path, c9_target_id=""))
                    row["original_c10_targetless_read"] = "ACCEPTED"
                except Exception as error:
                    row["original_c10_targetless_read"] = type(error).__name__ + ":" + str(error)
                observations.append(row)
            finally:
                producer.close()
    imports = []
    for name, module in sorted(sys.modules.items()):
        filename = getattr(module, "__file__", None)
        if filename:
            path = Path(filename).resolve()
            if path.is_relative_to(HERE) and path.suffix == ".py":
                data = path.read_bytes()
                imports.append({"module": name, "path": str(path), "sha256": hashlib.sha256(data).hexdigest(),
                                "git_blob": hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()})
    output = {"schema": "F1CI3_INDEPENDENT_PROBES@1", "original_cases_compared": len(rows),
              "full_frozen_input_equal": True, "source_cut_physical_transfer_preserved": True,
              "omission_distinct_from_silence": True, "event_access_distinct_from_tool_access_metadata": True,
              "probes": observations, "physical_imports": imports}
    (HERE / "independent_probe_results.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    for row in observations:
        print(row["id"], row.get("consumer", row.get("branch", "PRESERVED")), row.get("p01", ""))
    print("13 exact original outcomes compared; independent observations saved (candidate defects are retained).")


if __name__ == "__main__":
    main()
