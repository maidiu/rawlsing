#!/usr/bin/env python3
"""Changed-test hygiene and claim-specific negative-control proof (stdlib + pytest runtime).

Usage:
  python proof_integrity_gate_r1.py changed --base SHA --head SHA --root PATH
  python proof_integrity_gate_r1.py lint path/to/test.py
  python proof_integrity_gate_r1.py witness path/to/test.py.proof.json --root PATH
This is a necessary enforcement check, NOT a certificate of scientific meaning.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

SCHEMA = "RAWLSING_PROOF_INTEGRITY_R1"
INTEGRATION_WORDS = re.compile(r"(?:join|integration|lifecycle|consumer|weld|end_to_end)", re.I)


def is_test(path: Path) -> bool:
    return path.suffix == ".py" and (
        path.name.startswith("test_")
        or path.name.endswith("_test.py")
        or "tests" in path.parts
    )


def _constant_true(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value is True


def _weak_check(expr: ast.AST) -> list[str]:
    errors = []
    for n in ast.walk(expr):
        if isinstance(n, ast.BoolOp) and isinstance(n.op, ast.Or):
            if any(_constant_true(c) for c in n.values):
                errors.append("truth-bypass: 'or True' in assertion")
        if isinstance(n, ast.IfExp) and (
            _constant_true(n.body) or _constant_true(n.orelse)
        ):
            errors.append("conditional unconditional-success branch in assertion")
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Slice):
            if isinstance(n.slice.upper, ast.Constant) and n.slice.upper.value == 0:
                errors.append("zero-length slice in assertion; no identity check")
        if isinstance(n, ast.Compare) and len(n.ops) == 1 and len(n.comparators) == 1:
            if isinstance(n.ops[0], (ast.Eq, ast.Is)) and (
                ast.dump(n.left) == ast.dump(n.comparators[0])
            ):
                errors.append("self-comparison in assertion")
    if _constant_true(expr):
        errors.append("unconditional assert True")
    return sorted(set(errors))


def lint_text(code: str, filename: str = "<test>") -> list[str]:
    try:
        tree = ast.parse(code, filename=filename)
    except SyntaxError as e:
        return [f"{filename}:{e.lineno}: syntax error: {e.msg}"]
    errors = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Assert):
            errors.extend(f"{filename}:{n.lineno}: {problem}" for problem in _weak_check(n.test))
        if isinstance(n, (ast.For, ast.AsyncFor, ast.While)) and n.body and all(
            isinstance(child, (ast.Pass, ast.Expr))
            and (
                isinstance(child, ast.Pass)
                or isinstance(child.value, ast.Constant)
            )
            for child in n.body
        ):
            errors.append(f"{filename}:{n.lineno}: verification loop with no operative body")
    return sorted(set(errors))


def claimed_integration(code: str, filename: str) -> bool:
    if INTEGRATION_WORDS.search(Path(filename).stem):
        return True
    tree = ast.parse(code, filename=filename)
    return any(
        isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        and n.name.startswith("test_")
        and INTEGRATION_WORDS.search(n.name)
        for n in ast.walk(tree)
    )


def safe_file(root: Path, relative: str) -> Path:
    p = (root / relative).resolve()
    if not p.is_relative_to(root.resolve()) or not p.is_file():
        raise ValueError(f"missing or out-of-tree file: {relative}")
    return p


def _run_node(root: Path, node: str, junit: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        sys.executable, "-B", "-m", "pytest", "-q",
        "-p", "no:cacheprovider", "--junitxml", str(junit), node,
    ]
    return subprocess.run(command, cwd=root, env=env, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          timeout=180)


def _case_state(junit: Path, name: str) -> tuple[bool, bool, bool]:
    if not junit.is_file():
        return False, False, False
    x = ET.parse(junit).getroot()
    cases = [c for c in x.iter("testcase") if c.attrib.get("name") == name]
    if len(cases) != 1:
        return False, False, False
    c = cases[0]
    return c.find("failure") is not None, c.find("error") is not None, c.find("skipped") is not None


def witness(contract_file: Path, root: Path) -> dict:
    root = root.resolve()
    contract = json.loads(contract_file.read_text(encoding="utf-8"))
    if contract.get("schema") != SCHEMA or not isinstance(contract.get("claims"), list) or not contract["claims"]:
        raise ValueError("proof contract must contain schema and nonempty claims")
    out = []
    for claim in contract["claims"]:
        for k in ("claim_id", "actual_consumer", "claimed_dependency", "positive_node", "fault"):
            if not claim.get(k):
                raise ValueError(f"missing claim field: {k}")
        node = claim["positive_node"]
        test_relative = node.split("::", 1)[0]
        test_file = safe_file(root, test_relative)
        if contract_file.resolve() != Path(str(test_file) + ".proof.json"):
            raise ValueError("witness contract must belong to the exact named test module")
        if not is_test(test_file) or "::" not in node:
            raise ValueError("positive_node must name a specific Python test")
        target_name = node.split("::")[-1].split("[")[0]
        mutation = claim["fault"]
        file = safe_file(root, mutation.get("path", ""))
        if is_test(file):
            raise ValueError("mutation must alter actual implementation, not its tests")
        before = file.read_text(encoding="utf-8")
        old, new = mutation.get("old"), mutation.get("new")
        if not isinstance(old, str) or not isinstance(new, str) or len(old) < 8 or old == new or before.count(old) != 1:
            raise ValueError("mutation requires exactly one concrete exact source occurrence")
        with tempfile.TemporaryDirectory(prefix="rawlsing-proof-") as d:
            base_xml = Path(d) / "base.xml"
            mutant_xml = Path(d) / "mutant.xml"
            baseline = _run_node(root, node, base_xml)
            b_fail, b_error, b_skip = _case_state(base_xml, target_name)
            if baseline.returncode != 0 or b_fail or b_error or b_skip:
                raise AssertionError(f"{claim['claim_id']}: baseline must PASS named test; result:\n{baseline.stdout[-2500:]}")
            try:
                file.write_text(before.replace(old, new, 1), encoding="utf-8")
                mutated = _run_node(root, node, mutant_xml)
            finally:
                file.write_text(before, encoding="utf-8")
            m_fail, m_error, m_skip = _case_state(mutant_xml, target_name)
            if mutated.returncode == 0 or not m_fail or m_error or m_skip:
                raise AssertionError(
                    f"{claim['claim_id']}: exact target test did not fail by assertion "
                    f"(failure={m_fail}, error={m_error}, skipped={m_skip});\n"
                    + mutated.stdout[-2500:]
                )
        out.append({"claim_id": claim["claim_id"], "positive_node": node,
                    "fault_path": mutation["path"], "baseline": "PASS",
                    "fault_probe": "TARGET_ASSERTION_FAILED", "grade": "BOUNDED_MUTATION_DETECTED"})
    return {"schema": SCHEMA, "status": "MECHANICAL_WITNESS_PASS_NOT_SEMANTIC_ADOPTION", "claims": out}


def changed_files(root: Path, base: str, head: str) -> list[Path]:
    p = subprocess.run(
        ["git", "diff", "--diff-filter=ACMRT", "--name-only", base, head, "--"],
        cwd=root, capture_output=True, text=True, check=True,
    )
    return [root / s for s in p.stdout.splitlines() if s]


def run_changed(root: Path, base: str, head: str) -> dict:
    examined, contracts = [], []
    problems = []
    for path in changed_files(root, base, head):
        if not path.is_file() or not is_test(path):
            continue
        rel = path.relative_to(root).as_posix()
        code = path.read_text(encoding="utf-8")
        examined.append(rel)
        problems.extend(lint_text(code, rel))
        try:
            integration = claimed_integration(code, rel)
        except SyntaxError:
            continue
        if integration:
            proof_path = Path(str(path) + ".proof.json")
            if not proof_path.is_file():
                problems.append(f"{rel}: material integration-claim test requires {proof_path.name} with executable severance witness")
                continue
            contracts.append(proof_path)
    if problems:
        raise AssertionError("\n".join(problems))
    receipts = [witness(c, root) for c in contracts]
    return {"examined_tests": examined, "witness_contracts_run": len(contracts),
            "receipts": receipts, "state": "MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION"}


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)
    a = sub.add_parser("changed")
    a.add_argument("--root", type=Path, default=Path("."))
    a.add_argument("--base", required=True)
    a.add_argument("--head", required=True)
    a = sub.add_parser("lint")
    a.add_argument("test_file", type=Path)
    a = sub.add_parser("witness")
    a.add_argument("contract", type=Path)
    a.add_argument("--root", type=Path, default=Path("."))
    a.add_argument("--receipt", type=Path)
    args = p.parse_args()
    try:
        if args.mode == "lint":
            errors = lint_text(args.test_file.read_text(encoding="utf-8"), str(args.test_file))
            if errors:
                raise AssertionError("\n".join(errors))
            result = {"state": "AST_LINT_PASS", "file": str(args.test_file)}
        elif args.mode == "witness":
            result = witness(args.contract, args.root)
            if args.receipt:
                args.receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        else:
            result = run_changed(args.root.resolve(), args.base, args.head)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, AssertionError, OSError, subprocess.SubprocessError) as e:
        print(f"PROOF_INTEGRITY_GATE_RED: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
