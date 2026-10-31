#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path("/Users/matthewsmith/Desktop/rawlsing_r02v_r2_canonical")
BASELINE = "750548ddbb9b4392a16ce93097b856f349e16182"
ROSTER_COMMIT = "becf0bfb04705b8fe0927dd56e7290e1dcd180a8"
ROSTER_PATH = "PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/SCOPED_ROSTER/11_S2_HEAD_ONLY_ROSTER.json"
ART = Path("/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/pyat845_s2_artifact")
CURRENT = Path("/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/pyat845_s2_analysis/current")
STDLIB = set(sys.stdlib_module_names)


def git(*args: str, text: bool = False) -> bytes | str:
    cmd = ["git", "-c", "gc.auto=0", "-C", str(REPO), *args]
    out = subprocess.check_output(cmd)
    return out.decode(errors="replace") if text else out


def blob_content(blob: str) -> bytes:
    return git("cat-file", "blob", blob)


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Normalize(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        node.name = "F"
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node):
        node.name = "F"
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        node.name = "C"
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        node.id = "V"
        return node

    def visit_arg(self, node):
        node.arg = "A"
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node):
        node.attr = "A"
        self.generic_visit(node)
        return node

    def visit_keyword(self, node):
        node.arg = "K"
        self.generic_visit(node)
        return node

    def visit_alias(self, node):
        node.name = "M"
        node.asname = "M"
        return node


def strip_docstrings(tree: ast.AST) -> None:
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0], ast.Expr):
                value = node.body[0].value
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    node.body = node.body[1:] or [ast.Pass()]


def function_records(text: str) -> dict[str, dict]:
    try:
        tree = ast.parse(text)
    except Exception:
        return {}
    out: dict[str, dict] = {}
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append("." * node.level + node.module)
            else:
                imports.append("." * node.level)
    module_imports = sorted(set(imports))

    def visit(body, prefix=""):
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix + node.name
                exact = sha256(ast.dump(node, include_attributes=False).encode())
                clone = copy.deepcopy(node)
                strip_docstrings(clone)
                Normalize().visit(clone)
                norm = sha256(ast.dump(clone, include_attributes=False).encode())
                doc = (ast.get_docstring(node) or "").strip().splitlines()
                out[name] = {
                    "symbol": name,
                    "kind": type(node).__name__,
                    "line": node.lineno,
                    "exact": exact,
                    "norm": norm,
                    "body": len(node.body),
                    "doc": doc[0][:240] if doc else "",
                    "signature": ast.unparse(node.args),
                    "imports": module_imports,
                }
            elif isinstance(node, ast.ClassDef):
                visit(node.body, prefix + node.name + ".")
    visit(tree.body)
    return out


def meaningful(symbol: str, rec: dict, path: str) -> bool:
    base = symbol.split(".")[-1]
    if base.startswith("__"):
        return False
    if "/tests/" in path or Path(path).name.startswith("test_"):
        return False
    keywords = (
        "verify", "validate", "auth", "refuse", "deny", "allow", "commit",
        "seal", "hash", "digest", "source", "owner", "admit", "restore",
        "rollback", "gate", "check", "prove", "receipt", "custody", "issue",
        "grant", "permission", "bind", "witness", "court", "consumer",
    )
    if base.startswith("_") and not any(k in base.lower() for k in keywords):
        return False
    if rec["body"] < 5:
        return False
    return True


def module_name(path: str) -> str:
    if path.endswith(".py"):
        path = path[:-3]
    if path.endswith("/__init__"):
        path = path[: -len("/__init__")]
    return path.replace("/", ".")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    roster = json.loads(git("show", f"{ROSTER_COMMIT}:{ROSTER_PATH}", text=True))
    branch_index = {
        x["branch"]: x
        for x in (
            json.loads(line)
            for line in (ART / "S2_branch_code_return_index.jsonl").read_text().splitlines()
            if line.strip()
        )
    }
    variants = {
        x["variant_key"]: x
        for x in (
            json.loads(line)
            for line in (ART / "S2_function_variant_index.jsonl").read_text().splitlines()
            if line.strip()
        )
    }

    current_by_path: dict[str, dict[str, dict]] = {}
    current_text: dict[str, str] = {}
    current_module_set: set[str] = set()
    current_package_roots: set[str] = set()
    current_refs: dict[str, set[str]] = defaultdict(set)
    for path in sorted(CURRENT.rglob("*.py")):
        rel = path.relative_to(CURRENT).as_posix()
        text = path.read_text()
        current_text[rel] = text
        current_by_path[rel] = function_records(text)
        current_module_set.add(module_name(rel))
        current_package_roots.add(module_name(rel).split(".")[0])
        for token in set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", text)):
            current_refs[token].add(rel)
    current_norm: dict[str, list[tuple[str, str]]] = defaultdict(list)
    current_name: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for path, funcs in current_by_path.items():
        for symbol, rec in funcs.items():
            current_norm[rec["norm"]].append((path, symbol))
            current_name[symbol].append((path, symbol))
            current_name[symbol.split(".")[-1]].append((path, symbol))

    # Return evidence cache
    ev_cache: dict[tuple[str, str], dict] = {}

    def return_evidence(tip: str, root: str) -> dict:
        key = (tip, root)
        if key in ev_cache:
            return ev_cache[key]
        try:
            files = git("ls-tree", "-r", "--name-only", tip, root, text=True).splitlines()
        except subprocess.CalledProcessError:
            files = []
        files = [f for f in files if f.startswith(root + "/")]
        if not files:
            rec = {
                "root": root,
                "files": [],
                "purpose": "",
                "verdict_tokens": [],
                "test_counts": {},
                "negative_tokens": [],
                "positive_tokens": [],
                "snippet": "",
            }
            ev_cache[key] = rec
            return rec
        key_files = []
        for f in files:
            name = Path(f).name.lower()
            if name in ("00_return.md", "return.json") or re.search(
                r"(verdict|review|result|handoff|summary|decision|return)", name
            ):
                key_files.append(f)
        key_files = key_files[:3]
        texts = []
        for f in key_files:
            try:
                texts.append(git("show", f"{tip}:{f}", text=True))
            except subprocess.CalledProcessError:
                pass
        text = "\n".join(texts)
        heading = ""
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("#"):
                heading = s.lstrip("# ").strip()
                break
            if s.startswith("**") and len(s) > 4:
                heading = s.strip("* ").strip()
                break
        tokens = set(re.findall(
            r"\b(ACCEPT_SCOPED|REVISE|RED|HOLD|REJECT|INVALID|TRASH|OBSOLETE|DUPLICATE|"
            r"SUPERSEDED|PASS|FAIL|FAILED|ADOPTED|MERGED|READY|BLOCKED|COMPLETE|SUCCESS)\b",
            text.upper(),
        ))
        counts = {}
        for n, kind in re.findall(r"\b(\d+)\s+(passed|failed|failures|errors|skipped)\b", text, re.I):
            counts[kind.lower()] = int(n)
        negative = sorted(tokens & {"REVISE", "RED", "HOLD", "REJECT", "INVALID", "TRASH", "OBSOLETE", "DUPLICATE", "SUPERSEDED", "FAIL", "FAILED", "BLOCKED"})
        positive = sorted(tokens & {"ACCEPT_SCOPED", "PASS", "ADOPTED", "MERGED", "READY", "COMPLETE", "SUCCESS"})
        rec = {
            "root": root,
            "files": key_files,
            "purpose": heading[:240],
            "verdict_tokens": sorted(tokens),
            "test_counts": counts,
            "negative_tokens": negative,
            "positive_tokens": positive,
            "snippet": re.sub(r"\s+", " ", text)[:500],
            "text": text[:20000],
        }
        ev_cache[key] = rec
        return rec

    # Branch evidence cache
    branch_evidence: dict[str, dict] = {}
    for branch, row in branch_index.items():
        tip = row["tip"]
        roots = row["changed_return_roots"]
        evs = [return_evidence(tip, root) for root in roots]
        tokens = sorted({t for e in evs for t in e["verdict_tokens"]})
        neg = sorted({t for e in evs for t in e["negative_tokens"]})
        pos = sorted({t for e in evs for t in e["positive_tokens"]})
        counts = Counter()
        for e in evs:
            for k, v in e["test_counts"].items():
                counts[k] += v
        purpose = next((e["purpose"] for e in evs if e["purpose"]), "")
        branch_evidence[branch] = {
            "return_roots": roots,
            "return_files": sorted({f for e in evs for f in e["files"]}),
            "purpose": purpose or branch,
            "verdict_tokens": tokens,
            "negative_tokens": neg,
            "positive_tokens": pos,
            "test_counts": dict(counts),
            "snippet": next((e["snippet"] for e in evs if e["snippet"]), ""),
            "evidence_text": "\n".join(e.get("text", "") for e in evs)[:40000],
        }

    # Changed all paths cache
    changed_all: dict[str, list[str]] = {}
    for branch, row in branch_index.items():
        try:
            changed_all[branch] = git("diff", "--name-only", row["merge_base"], row["tip"], text=True).splitlines()
        except subprocess.CalledProcessError:
            changed_all[branch] = []

    # Build function rows
    function_rows: dict[tuple[str, str, str], dict] = {}
    branch_function_keys: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    blob_cache: dict[str, bytes] = {}
    mb_cache: dict[tuple[str, str], bytes | None] = {}

    def tip_funcs(blob: str) -> dict[str, dict]:
        if blob not in blob_cache:
            blob_cache[blob] = blob_content(blob)
        return function_records(blob_cache[blob].decode())

    def mb_funcs(mb: str, path: str) -> dict[str, dict]:
        key = (mb, path)
        if key not in mb_cache:
            r = subprocess.run(
                ["git", "-c", "gc.auto=0", "-C", str(REPO), "show", f"{mb}:{path}"],
                capture_output=True,
            )
            mb_cache[key] = r.stdout if r.returncode == 0 else None
        data = mb_cache[key]
        return function_records(data.decode()) if data else {}

    for branch in sorted(branch_index):
        row = branch_index[branch]
        ev = branch_evidence[branch]
        for src in row["changed_source_paths"]:
            path = src["path"]
            variant = variants[src["variant_key"]]
            tip = tip_funcs(variant["historical_blob"])
            mb = mb_funcs(row["merge_base"], path)
            for symbol, rec in tip.items():
                old = mb.get(symbol)
                if old is not None and old["exact"] == rec["exact"]:
                    continue
                if not meaningful(symbol, rec, path):
                    continue
                key = (path, symbol, rec["exact"])
                if key not in function_rows:
                    function_rows[key] = {
                        "function_id": f"F{len(function_rows)+1:04d}",
                        "path": path,
                        "symbol": symbol,
                        "kind": rec["kind"],
                        "historical_blob": variant["historical_blob"],
                        "ast_exact_sha256": rec["exact"],
                        "ast_no_identifier_sha256": rec["norm"],
                        "body_statements": rec["body"],
                        "doc": rec["doc"],
                        "purpose": rec["doc"] or symbol,
                        "signature": rec["signature"],
                        "imports": rec["imports"],
                        "branches": [],
                        "tip_dates": {},
                        "existed_at_merge_base": {},
                    }
                fr = function_rows[key]
                if branch not in fr["branches"]:
                    fr["branches"].append(branch)
                    fr["tip_dates"][branch] = next(
                        (x["author_time_utc"] for x in roster["branch_heads"] if x["branch"] == branch), ""
                    )
                    fr["existed_at_merge_base"][branch] = old is not None
                branch_function_keys[branch].append(key)

    def unresolved_imports(imports: list[str], path: str) -> list[str]:
        bad = []
        for mod in imports:
            if mod.startswith("."):
                base = Path(path).parent
                rel = mod.lstrip(".")
                candidate = (base / rel.replace(".", "/")).as_posix() if rel else base.as_posix()
                if candidate + ".py" not in current_text and candidate + "/__init__.py" not in current_text:
                    bad.append(mod)
                continue
            root = mod.split(".")[0]
            if root in STDLIB:
                continue
            if mod in current_module_set:
                continue
            if any(m.endswith("." + mod) for m in current_module_set):
                continue
            if mod == root and root in current_package_roots:
                continue
            bad.append(mod)
        return sorted(set(bad))

    def current_equiv(fr: dict) -> dict:
        path = fr["path"]
        symbol = fr["symbol"]
        hist_norm = fr["ast_no_identifier_sha256"]
        same = current_by_path.get(path, {}).get(symbol)
        if same:
            if same["exact"] == fr["ast_exact_sha256"]:
                return {"status": "EXACT", "path": path, "symbol": symbol, "rec": same}
            if same["norm"] == hist_norm:
                return {"status": "REBUILT_SAME_PATH", "path": path, "symbol": symbol, "rec": same}
            if same["body"] >= fr["body_statements"]:
                return {"status": "SUPERSEDED_SAME_PATH", "path": path, "symbol": symbol, "rec": same}
            return {"status": "CURRENT_SAME_SYMBOL_SHORTER", "path": path, "symbol": symbol, "rec": same}
        for cpath, csym in current_norm.get(hist_norm, []):
            return {"status": "REBUILT_CROSS_PATH", "path": cpath, "symbol": csym, "rec": current_by_path[cpath][csym]}
        names = current_name.get(symbol, []) + current_name.get(symbol.split(".")[-1], [])
        if names:
            cpath, csym = names[0]
            return {"status": "CURRENT_SAME_NAME_OTHER_PATH", "path": cpath, "symbol": csym, "rec": current_by_path[cpath][csym]}
        return {"status": "NONE"}

    def classify(fr: dict) -> tuple[str, list[str]]:
        equiv = current_equiv(fr)
        branches = fr["branches"]
        evs = [branch_evidence[b] for b in branches]
        neg = sorted({t for e in evs for t in e["negative_tokens"]})
        pos = sorted({t for e in evs for t in e["positive_tokens"]})
        counts = Counter()
        for e in evs:
            for k, v in e["test_counts"].items():
                counts[k] += v
        reasons = []
        if equiv["status"] == "EXACT":
            return "EXACT_ALREADY_IN_PREMAIN", ["current PREMAIN exact AST match at same path/symbol"]
        if equiv["status"] in ("REBUILT_SAME_PATH", "REBUILT_CROSS_PATH"):
            return "INDEPENDENTLY_REBUILT_EQUIVALENT", [
                f"current PREMAIN normalized AST match at {equiv['path']}:{equiv['symbol']}"
            ]
        if equiv["status"] == "SUPERSEDED_SAME_PATH":
            return "SUPERSEDED_BETTER", [
                f"current PREMAIN same path/symbol has different larger AST at {equiv['path']}:{equiv['symbol']}"
            ]
        if equiv["status"] == "CURRENT_SAME_SYMBOL_SHORTER":
            return "EVIDENCE_UNKNOWN", [
                f"current PREMAIN same path/symbol is shorter; not proven better at {equiv['path']}:{equiv['symbol']}"
            ]
        if equiv["status"] == "CURRENT_SAME_NAME_OTHER_PATH":
            return "EVIDENCE_UNKNOWN", [
                f"current PREMAIN has same name at another path {equiv['path']}:{equiv['symbol']}; equivalence not proven"
            ]
        # no current equivalent
        bad = unresolved_imports(fr["imports"], fr["path"])
        base = fr["symbol"].split(".")[-1].lower()
        texts = [branch_evidence[b].get("evidence_text", "").lower() for b in branches]
        symbol_seen = any(base in t or fr["path"].lower() in t for t in texts)
        explicit_negative = sorted(set(neg) & {"INVALID", "TRASH", "OBSOLETE", "DUPLICATE", "REJECT", "SUPERSEDED"})
        if explicit_negative and symbol_seen and not pos:
            return "INVALID/TRASH_WITH_GROUNDS", [
                "symbol/path-specific return text contains explicit negative token and no positive token",
                f"negative tokens: {explicit_negative}",
            ]
        basename = Path(fr["path"]).name.lower()
        tooling = (
            "/repro/" in fr["path"]
            or "/scripts/" in fr["path"]
            or any(k in basename for k in ("audit", "court", "probe", "patch", "witness", "runner", "bootstrap", "stage", "install", "repro"))
        )
        if tooling:
            return "EVIDENCE_UNKNOWN", [
                "reproduction/court/tooling helper at a missing or changed current path; not a production component",
                "branch return/test evidence is read-only; no independent execution or current consumer proven",
            ]
        if pos:
            if bad:
                return "UNIQUE_USEFUL_NEEDS_ADAPTATION", [
                    "original return provides positive evidence but current imports are unresolved",
                    f"unresolved imports: {bad}",
                ]
            base_refs = sorted(p for p in current_refs.get(fr["symbol"].split(".")[-1], set()) if p != fr["path"])
            if counts and base_refs and not (set(neg) & {"FAIL", "FAILED", "RED", "REJECT", "INVALID", "BLOCKED"}):
                return "UNIQUE_USEFUL_READY", [
                    "positive return/test evidence, imports resolve, current text reference exists, and no direct negative token",
                    f"text references: {base_refs[:5]}",
                ]
            return "UNIQUE_USEFUL_HELD_BY_ACTUAL_SOURCE_AUTHORITY", [
                "no current equivalent; positive return/test evidence; original source/owner/consumer authority not established",
                f"positive tokens: {pos}",
            ]
        return "EVIDENCE_UNKNOWN", [
            "no current equivalent and no decisive symbol-specific positive/negative original-return evidence",
        ]

    # Build final function rows
    final_functions = []
    for key in sorted(function_rows):
        fr = function_rows[key]
        equiv = current_equiv(fr)
        classification, reasons = classify(fr)
        evs = [branch_evidence[b] for b in fr["branches"]]
        neg = sorted({t for e in evs for t in e["negative_tokens"]})
        pos = sorted({t for e in evs for t in e["positive_tokens"]})
        counts = Counter()
        for e in evs:
            for k, v in e["test_counts"].items():
                counts[k] += v
        base = fr["symbol"].split(".")[-1]
        refs = sorted(p for p in current_refs.get(base, set()) if p != fr["path"])
        proven_current = equiv["status"] in ("EXACT", "REBUILT_SAME_PATH", "REBUILT_CROSS_PATH", "SUPERSEDED_SAME_PATH")
        fr.update({
            "current_equivalent": {
                "status": equiv["status"],
                "proven_current_receiver": proven_current,
                "path": equiv.get("path"),
                "symbol": equiv.get("symbol"),
                "body_statements": equiv.get("rec", {}).get("body") if equiv.get("rec") else None,
                "signature": equiv.get("rec", {}).get("signature") if equiv.get("rec") else None,
            },
            "classification": classification,
            "classification_reasons": reasons,
            "inherited_repetition": (
                "MULTI_BRANCH_REPETITION" if len(fr["branches"]) > 1 else "SINGLE_BRANCH"
            ),
            "origin_branch_candidate": min(fr["branches"], key=lambda b: fr["tip_dates"].get(b, "")),
            "origin_proof": "TIP_DATE_ONLY__CREATION_ORDER_NOT_PROVEN",
            "historical_review": {
                "negative_tokens": neg,
                "positive_tokens": pos,
                "test_counts": dict(counts),
                "evidence_roots": sorted({r for b in fr["branches"] for r in branch_evidence[b]["return_roots"]}),
            },
            "tests_evidence": {
                "changed_test_paths_in_branches": sorted({
                    p["path"] for b in fr["branches"] for p in branch_index[b]["changed_test_paths"]
                }),
                "reported_test_counts": dict(counts),
                "branch_tests_executed_by_this_worker": False,
                "original_execution_claimed": bool(counts),
            },
            "compatibility": {
                "imports": fr["imports"],
                "unresolved_imports": unresolved_imports(fr["imports"], fr["path"]),
                "schema_or_abi": "NOT_ASSESSED",
                "time_ff_n9_n12": "HOLD_OR_NOT_APPLICABLE",
            },
            "first_consumer": {
                "current_equivalent": f"{equiv.get('path')}:{equiv.get('symbol')}" if proven_current else None,
                "current_candidates": (
                    [f"{equiv.get('path')}:{equiv.get('symbol')}"]
                    if (not proven_current and equiv.get("path")) else []
                ),
                "text_reference_candidates": refs[:8],
                "consumer_proof": "TEXT_REFERENCE_ONLY__NOT_EXECUTED" if refs else "NOT_IDENTIFIED",
            },
            "successor": f"{equiv.get('path')}:{equiv.get('symbol')}" if proven_current else "NONE_FOUND",
            "integration_steps": (
                "No integration: current PREMAIN equivalent already exists."
                if classification == "EXACT_ALREADY_IN_PREMAIN"
                else "No integration: current normalized equivalent exists."
                if classification == "INDEPENDENTLY_REBUILT_EQUIVALENT"
                else "No integration: current PREMAIN same-path implementation is larger/superseding; verify no lost branch-specific behavior."
                if classification == "SUPERSEDED_BETTER"
                else "Do not integrate: explicit negative original evidence."
                if classification == "INVALID/TRASH_WITH_GROUNDS"
                else "Original owner/source review; resolve missing imports and interface/time/FF/N9-N12; run exact tests plus fault negatives; protected owner CAS."
                if classification == "UNIQUE_USEFUL_NEEDS_ADAPTATION"
                else "Original owner/source/consumer authorization required; adapt only after exact review."
                if classification.startswith("UNIQUE_USEFUL_")
                else "Locate original return/reviewer/source owner and current consumer before any disposition."
            ),
            "scientific_authority": "HOLD_ORIGINAL_CAN_ADP_PYAT_SCIENCE",
            "actor_permission_authority": "HOLD_ORIGINAL_PYAT_SOROK_OWNER",
            "independent_reviewer": "NOT_ASSIGNED__NEW_HOSTILE_REVIEW_REQUIRED",
            "contradictions": (
                "positive return/tests but no current equivalent"
                if pos and not equiv.get("path") and classification != "UNIQUE_USEFUL_READY"
                else "negative original evidence but current text references exist"
                if neg and refs
                else ""
            ),
        })
        final_functions.append(fr)

    function_by_key = {(fr["path"], fr["symbol"], fr["ast_exact_sha256"]): fr for fr in final_functions}

    # Build branch rows
    branch_rows = []
    for br in roster["branch_heads"]:
        branch = br["branch"]
        row = branch_index[branch]
        ev = branch_evidence[branch]
        keys = sorted(set(branch_function_keys.get(branch, [])))
        funcs = [function_by_key[k] for k in keys]
        cls_counts = Counter(f["classification"] for f in funcs)
        unique_classes = {k: v for k, v in cls_counts.items() if k.startswith("UNIQUE_USEFUL_")}
        if not row["changed_source_paths"] and not row["changed_return_roots"]:
            disposition = "NO_CODE_NO_RETURN_EVIDENCE"
        elif not row["changed_source_paths"]:
            disposition = "EVIDENCE_ONLY_RETURN"
        elif unique_classes:
            disposition = "UNIQUE_FUNCTIONS_PRESENT__HOLD_OR_ADAPT"
        elif cls_counts.get("INVALID/TRASH_WITH_GROUNDS"):
            disposition = "INVALID_OR_TRASH"
        elif cls_counts and all(c in ("EXACT_ALREADY_IN_PREMAIN", "INDEPENDENTLY_REBUILT_EQUIVALENT", "SUPERSEDED_BETTER") for c in cls_counts):
            disposition = "NO_UNIQUE_ACTION__CURRENT_EQUIVALENT_OR_SUPERSEDED"
        elif cls_counts.get("EVIDENCE_UNKNOWN"):
            disposition = "UNRESOLVED_SOURCE_EVIDENCE"
        else:
            disposition = "REVIEWED_NO_MEANINGFUL_FUNCTION"
        test_names = []
        for t in row["changed_test_paths"]:
            tv = variants[t["variant_key"]]
            ttext = blob_content(tv["historical_blob"]).decode(errors="replace")
            for tname in function_records(ttext):
                base = tname.split(".")[-1]
                if base.startswith("test") or base.endswith("_test"):
                    test_names.append(f"{t['path']}::{tname}")
        fault_keywords = (
            "fault", "negative", "refuse", "forbid", "reject", "invalid",
            "mismatch", "stale", "tamper", "forged", "rollback", "fail",
            "missing", "unauthorized", "unknown",
        )
        fault_count = sum(1 for n in test_names if any(k in n.lower() for k in fault_keywords))
        branch_rows.append({
            "schema": "PYAT_S2_BRANCH_DISPOSITION@1",
            "branch": branch,
            "tip": row["tip"],
            "tip_date_not_creation_date": row["tip_date_not_creation_date"],
            "merge_base": row["merge_base"],
            "current_premain_compared": BASELINE,
            "cohort": row["cohort"],
            "changed_paths": {
                "source": [{"path": p["path"], "blob": p["blob"], "current_blob": p["current_blob"], "status": p["status"]} for p in row["changed_source_paths"]],
                "tests": [{"path": p["path"], "blob": p["blob"], "current_blob": p["current_blob"], "status": p["status"]} for p in row["changed_test_paths"]],
                "returns": row["changed_return_roots"],
                "other_changed_paths": [p for p in changed_all.get(branch, []) if not p.startswith(("rawlsing_next/", "WORKER_RETURNS/"))][:20],
            },
            "historical_review": {k: v for k, v in ev.items() if k != "evidence_text"},
            "meaningful_function_count": len(funcs),
            "function_dispositions": [
                {
                    "function_id": f["function_id"],
                    "path": f["path"],
                    "symbol": f["symbol"],
                    "classification": f["classification"],
                    "current_equivalent": f["successor"],
                    "reason": " ".join(f["classification_reasons"])[:500],
                }
                for f in funcs
            ],
            "classification_counts": dict(cls_counts),
            "branch_disposition": disposition,
            "original_purpose_summary": ev.get("purpose") or branch,
            "scientific_assumption": (
                "STATED_OR_IMPLIED_IN_RETURN__NO_ORIGINAL_ISSUANCE_VERIFIED"
                if ev.get("return_roots") and any(
                    k in (ev.get("purpose", "") + " " + ev.get("snippet", "")).lower()
                    for k in ("world", "actor", "person", "survey", "science", "empirical", "native", "causal", "calibration", "psycholog", "developmental", "practice", "human"))
                else "NOT_STATED__SOURCEFREE_CONTROL_ONLY"
            ),
            "historical_review_verdict": ",".join(ev.get("verdict_tokens", [])) or "NO_VERDICT_TOKEN",
            "compile_status": "STATIC_AST_ONLY__NOT_COMPILED_OR_EXECUTED",
            "abi_schema_status": "NOT_APPLICABLE_PYTHON_OR_NOT_ASSESSED",
            "scientific_authority": "HOLD_ORIGINAL_CAN_ADP_PYAT_SCIENCE",
            "actor_permission_authority": "HOLD_ORIGINAL_PYAT_SOROK_OWNER",
            "source_authority": "HOLD_ORIGINAL_SOURCE_OWNER",
            "first_consumer": sorted({f["first_consumer"]["current_equivalent"] for f in funcs if f["first_consumer"]["current_equivalent"]})[:5] or ["NOT_IDENTIFIED"],
            "successor": sorted({f["successor"] for f in funcs if f["successor"] != "NONE_FOUND"})[:5],
            "origin_vs_inherited": dict(Counter(f["inherited_repetition"] for f in funcs)),
            "tests": {
                "changed_test_paths": len(row["changed_test_paths"]),
                "test_function_count": len(test_names),
                "fault_witness_count": fault_count,
                "test_function_sample": test_names[:20],
                "reported_counts": ev["test_counts"],
                "tests_executed_by_this_worker": False,
                "tests_not_run": "ALL_BRANCH_TESTS_AND_ORIGINAL_SOURCE_EXECUTION_NOT_RUN",
            },
            "original_owner_locator": row["changed_return_roots"] or ["UNKNOWN"],
            "current_equivalents": sorted({f["first_consumer"]["current_equivalent"] for f in funcs if f["first_consumer"]["current_equivalent"]})[:8],
            "current_owner": "PREMAIN@750548" if any(f["first_consumer"]["current_equivalent"] for f in funcs) else "NONE_IN_CURRENT_PREMAIN",
            "independent_reviewer": "NOT_ASSIGNED__NEW_HOSTILE_REVIEW_REQUIRED",
            "evidence_limitations": [
                "Static Git/AST and return-text read only; no branch executables/tests/source-native runs",
                "Tip date is not branch creation date",
                "Textual consumer search is not an executed callgraph",
                "Reviewer verdict tokens are evidence locators, not acceptance",
            ],
        })

    branch_row_by_name = {b["branch"]: b for b in branch_rows}
    for fr in final_functions:
        brs = [branch_row_by_name[b] for b in fr["branches"]]
        fr["original_owner_locator"] = sorted({r for b in brs for r in b["original_owner_locator"]})[:10] or ["UNKNOWN"]
        fr["owner"] = fr["original_owner_locator"][0] if fr["original_owner_locator"] != ["UNKNOWN"] else "UNKNOWN_ORIGINAL_SOURCE_OWNER"
        fr["accountable_owner"] = "ORIGINAL_PYAT_SOURCE_OWNER_OR_CAN_ADP_ISSUER"
        fr["current_owner"] = "PREMAIN@750548" if fr["successor"] != "NONE_FOUND" else "NONE_IN_CURRENT_PREMAIN"
        fr["branch_signature"] = fr["signature"]
        fr["historical_review_verdict"] = ",".join(sorted(set(
            fr["historical_review"]["negative_tokens"] + fr["historical_review"]["positive_tokens"]
        ))) or "NO_VERDICT_TOKEN"
        evidence_text = " ".join(
            (branch_evidence[b].get("purpose", "") + " " + branch_evidence[b].get("snippet", ""))
            for b in fr["branches"]
            if branch_evidence[b].get("return_roots")
        )
        fr["scientific_assumption"] = (
            "STATED_OR_IMPLIED_IN_SOURCE_OR_RETURN__NO_ORIGINAL_ISSUANCE_VERIFIED"
            if any(k in (fr.get("doc", "") + " " + evidence_text).lower()
                   for k in ("world", "actor", "person", "survey", "science", "empirical", "native", "causal", "calibration", "psycholog", "developmental", "practice", "human"))
            else "NOT_STATED__SOURCEFREE_CONTROL_ONLY"
        )
        fr["compile_status"] = "STATIC_AST_ONLY__NOT_COMPILED_OR_EXECUTED"
        fr["abi_status"] = "NOT_APPLICABLE_PYTHON_OR_NOT_ASSESSED"
        fr["schema_status"] = "NOT_ASSESSED"
        fr["authority"] = f"SCIENTIFIC={fr['scientific_authority']}|ACTOR={fr['actor_permission_authority']}"
        fr["test_fault_witness_occurrences"] = sum(b["tests"]["fault_witness_count"] for b in brs)
        fr["tests_positive_negative"] = {
            "reported_test_counts": fr["tests_evidence"]["reported_test_counts"],
            "fault_witness_occurrences_across_associated_branches": fr["test_fault_witness_occurrences"],
            "tests_executed_by_this_worker": False,
            "status": "SOURCE_AND_RETURN_EVIDENCE_ONLY__NOT_EXECUTED",
        }

    assert len(branch_rows) == 175, len(branch_rows)
    assert len({x["branch"] for x in branch_rows}) == 175

    # Write provisional files
    with (out / "BRANCH_DISPOSITIONS.jsonl").open("w") as fh:
        for row in branch_rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    with (out / "FUNCTION_COURT.jsonl").open("w") as fh:
        for row in final_functions:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    summary = {
        "branch_rows": len(branch_rows),
        "function_rows": len(final_functions),
        "function_classes": dict(Counter(f["classification"] for f in final_functions)),
        "branch_dispositions": dict(Counter(b["branch_disposition"] for b in branch_rows)),
        "branches_with_source": sum(1 for b in branch_rows if b["changed_paths"]["source"]),
        "branches_without_source": sum(1 for b in branch_rows if not b["changed_paths"]["source"]),
        "branches_with_returns": sum(1 for b in branch_rows if b["changed_paths"]["returns"]),
        "source_path_occurrences": sum(len(b["changed_paths"]["source"]) for b in branch_rows),
        "test_path_occurrences": sum(len(b["changed_paths"]["tests"]) for b in branch_rows),
        "return_roots": sum(len(b["changed_paths"]["returns"]) for b in branch_rows),
    }
    (out / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
