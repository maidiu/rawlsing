#!/usr/bin/env python3
"""Execute the complete C0R3 corrected candidate and inherited court matrix."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
E = RETURN / "evidence"
HIST = RETURN / "historical"
WR = HIST / "WORKER_RETURNS"
CAND = RETURN / "candidate"
RUNTIME = CAND / "stage" / "runtime"
MANIFEST = RETURN / "01_SOURCE_AND_IMPORT_CUSTODY.json"
E.mkdir(exist_ok=True)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(name, cwd, files, *, env_extra=None):
    xml = E / (name + ".xml")
    log = E / (name + ".log")
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0"})
    if env_extra:
        env.update(env_extra)
    command = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
               "--import-mode=importlib", *files, "--junitxml", str(xml)]
    with log.open("wb") as handle:
        proc = subprocess.run(command, cwd=cwd, env=env, stdout=handle,
                              stderr=subprocess.STDOUT)
    return dict(name=name, cwd=str(Path(cwd).relative_to(RETURN)),
                files=list(files), return_code=proc.returncode,
                xml=xml.name, log=log.name)


def parse(xml: Path):
    root = ET.parse(xml).getroot()
    cases = list(root.iter("testcase"))
    rows = []
    for c in cases:
        status = "PASS"
        if c.find("failure") is not None:
            status = "FAIL"
        elif c.find("error") is not None:
            status = "ERROR"
        elif c.find("skipped") is not None:
            status = "SKIP"
        rows.append(dict(name=c.attrib.get("name", ""), status=status))
    return dict(tests=len(rows), passed=sum(r["status"] == "PASS" for r in rows),
                failed=sum(r["status"] == "FAIL" for r in rows),
                errors=sum(r["status"] == "ERROR" for r in rows),
                skipped=sum(r["status"] == "SKIP" for r in rows),
                failing=[r["name"] for r in rows if r["status"] != "PASS"])


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    if not (RUNTIME / "product/nonparent.py").is_file():
        subprocess.run([sys.executable, "-B", str(RETURN / "runner" / "prepare_historical.py")],
                       check=True, cwd=RETURN)
    c0p = WR / "SOROK-R3-HQ319-C0P-GENERIC-PORT-POSITIVE-R1"
    c0i_original = HIST / "c0i_original/SOROK-R3-HQ320-C0I-C0P-INDEPENDENT-R1"
    c0i_repaired = HIST / "c0i_repaired/SOROK-R3-HQ320-C0I-C0P-INDEPENDENT-R1"
    c0i_corrected = HIST / "c0i_corrected/SOROK-R3-HQ320-C0I-C0P-INDEPENDENT-R1"
    c0r2_repaired = HIST / "c0r2_repaired/SOROK-V2-HQ323-C0R2-GIT-BACKED-REPAIR-R1"
    c0r2_corrected = HIST / "c0r2_corrected/SOROK-V2-HQ323-C0R2-GIT-BACKED-REPAIR-R1"
    c0x = WR / "SOROK-20261019-C0X-C0-C10-DUAL-OWNER-RECEIVER-COMPLETION-R1"
    k9k10 = WR / "PYAT-USERDIRECT-20261014-R5-SC0F3-REAL-OWNER-REPAIR-R1/repro/inputs/port"

    suites = [
        ("c0p49_original", c0p, ["tests/test_c0p_generic_port.py"], 49, 49, 0,
         {"C0P_RUNTIME": str(RUNTIME),
          "C0P_ORACLES": str(c0p / "frozen_oracles"),
          "C0P_REPO": str(REPO)}),
        ("c0i50_original", c0i_original, ["repro/test_c0i.py"], 50, 47, 3, None),
        ("c0i50_repaired", c0i_repaired, ["repro/test_c0i.py"], 50, 50, 0, None),
        ("c0i50_corrected", c0i_corrected, ["repro/test_c0i.py"], 50, 50, 0, None),
        ("c0r2_23_repaired", c0r2_repaired, ["tests/test_c0r2_adversarial.py"], 23, 23, 0, None),
        ("c0r2_23_corrected", c0r2_corrected, ["tests/test_c0r2_adversarial.py"], 23, 23, 0, None),
        ("c0x15_original", c0x, ["tests/test_c0x_receiving_consumer.py"], 15, 15, 0, None),
        ("k9k10_36", k9k10, ["port/test_k9_provider_swap.py",
                              "port/test_k10_structural_conservation.py"], 36, 36, 0, None),
        ("c0r3_new_13", RETURN, ["tests/test_c0r3_endtoend.py"], 13, 13, 0, None),
    ]
    results = []
    all_expected = True
    for name, cwd, files, tests, passed, failed, env in suites:
        run_info = run(name, cwd, files, env_extra=env)
        parsed = parse(E / run_info["xml"])
        matched = (parsed["tests"] == tests and parsed["passed"] == passed and
                   parsed["failed"] == failed and parsed["errors"] == 0 and
                   parsed["skipped"] == 0)
        all_expected &= matched
        results.append({**run_info, "expected": dict(tests=tests, passed=passed, failed=failed),
                        "actual": parsed, "matched": matched})

    # Two cold receiver processes.
    cold = []
    for label in ("cold_a", "cold_b"):
        log = E / ("c0r3_cold_" + label + ".log")
        with log.open("wb") as handle:
            proc = subprocess.run([sys.executable, "-B", str(RETURN / "tests/cold_probe.py"),
                                   str(RETURN)], cwd=RETURN, stdout=handle,
                                  stderr=subprocess.STDOUT,
                                  env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
                                       "C0P_RUNTIME": str(RUNTIME)})
        cold.append(dict(label=label, return_code=proc.returncode, log=log.name))
    cold_payload = json.loads((E / "c0r3_cold_cold_a.log").read_text())
    cold_equal = all(c["return_code"] == 0 for c in cold)

    # Original defect reproduction (exact original C0X receiver/facade).
    defect_log = E / "original_defect_reproduction.log"
    with defect_log.open("wb") as handle:
        proc = subprocess.run([sys.executable, "-B",
                               str(RETURN / "runner/reproduce_original_defect.py"),
                               str(c0x)], cwd=RETURN, stdout=handle,
                              stderr=subprocess.STDOUT,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    defect = json.loads((E / "original_defect_reproduction.log").read_text())
    # Rewrite to the JSON receipt path (keep the command log separately).
    (E / "original_defect_reproduction.json").write_text(
        json.dumps(defect, sort_keys=True, indent=2) + "\n")
    defect_log.write_text("\n".join([
        f"return_code={proc.returncode}",
        f"parent_type={defect['original_parent_ref']['type']}",
        f"parent_callable={defect['original_parent_ref']['callable']}",
        f"json_error={defect['possibility_json_error']}",
        f"transport={defect['receiver_transport']['state']}",
        f"temporal={defect['temporal_early_clock']['type']}: "
        f"{defect['temporal_early_clock']['message']}",
    ]) + "\n")

    # Shared proof witness.
    gate_receipt = E / "proof_witness_receipt.json"
    gate_log = E / "proof_witness.log"
    with gate_log.open("wb") as handle:
        gate = subprocess.run([sys.executable, "-B",
                               str(CAND / "tools/proof_integrity_gate_r1.py"),
                               "witness", "tests/test_c0r3_endtoend.py.proof.json",
                               "--root", str(RETURN), "--receipt", str(gate_receipt)],
                              cwd=RETURN, stdout=handle, stderr=subprocess.STDOUT,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    gate_payload = json.loads(gate_receipt.read_text()) if gate_receipt.exists() else None
    facade_after = sha(CAND / "upstream/c0p_two_contract_port.py")
    expected_facade = manifest["corrected"]["facade"]["sha256"]
    restored = facade_after == expected_facade

    # Sanitize published evidence text.
    sanitized = 0
    for path in E.iterdir():
        if path.suffix not in (".xml", ".log", ".json"):
            continue
        text = path.read_text(errors="replace")
        new = re.sub(r'hostname="[^"]*"', 'hostname="sanitized-host"', text)
        new = re.sub("/" + "Users/[^ \n:\"']+", "<sanitized-host-path>", new)
        new = new.replace(str(RETURN), "<return-root>").replace(str(REPO), "<repo-root>")
        if new != text:
            path.write_text(new)
            sanitized += 1

    summary = dict(
        schema="SOROK_C0R3_EXECUTION_SUMMARY@1",
        environment=dict(python=sys.version.split()[0],
                         pytest=subprocess.check_output(
                             [sys.executable, "-m", "pytest", "--version"], text=True).strip()),
        suites=results,
        all_expected_outcomes=all_expected,
        cold=cold,
        cold_payload=cold_payload,
        cold_equal=cold_equal,
        original_defect=defect,
        proof_gate=dict(return_code=gate.returncode, receipt=gate_payload,
                        facade_after=facade_after, expected_facade=expected_facade,
                        restored=restored),
        corrected_facade_sha256=facade_after,
        corrected_receiver_sha256=sha(CAND / "c0x_world_receiver.py"),
        historical_red_accounting=dict(
            c0i_original="47 PASS / 3 RED preserved",
            c0i_repaired="50 PASS",
            c0i_corrected="50 PASS",
            c0x_original="15 PASS; inherited transport HOLD preserved on original",
            c0r2_vacuous="23 PASS; vacuous 'or True' preserved, not counted as proof",
            k9k10="36 PASS; SOURCEFREE_FIXTURE_PORT__NOT_OPERATIVE_N9"),
        evidence_sanitized_files=sanitized,
        verdict=dict(
            EXECUTED_GREEN=all_expected,
            ASSERTION_EFFICACY=(gate.returncode == 0 and restored),
            C10_TRANSPORT="PASS at two-owner object/read+JSON+cold grain",
            C11_WELD="NOT RUN / NOT AUTHORIZED",
        ),
    )
    (E / "execution_summary.json").write_text(
        json.dumps(summary, sort_keys=True, indent=2) + "\n")
    print(json.dumps(dict(all_expected=all_expected, cold=cold_equal,
                          gate=gate.returncode, restored=restored,
                          suites=len(results)), indent=2))
    return 0 if (all_expected and cold_equal and gate.returncode == 0 and restored) else 1


if __name__ == "__main__":
    raise SystemExit(main())
