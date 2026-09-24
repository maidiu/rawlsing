"""Fail-closed functional-succession preflight for the PRE-MAIN FIABC court.

This module implements the Wave-2 B05 succession-manifest contract without
creating semantic authority.  It verifies the exact Wave-2 L01 comparison
boundary and L02 claim-scoped authority closure, then mechanically checks the
chain

    inherited obligation -> accepted authority -> current owner
    -> executable binding -> live consumer -> A/B/C invariant + cost class

before any measured comparison may proceed.

The JSON Schema is byte-preserved beside this module as
``fiabc_succession_manifest_schema.json``.  P10 lifecycle/failure-scope facts
are supplied as a separate governed receipt context because the adopted B05
1.0.0 manifest schema has no lifecycle-context slot; omitting that context is
therefore a blocking condition, never an implicit PASS.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Protocol, Sequence, TypeVar


MANIFEST_SCHEMA_ID = "RAWLSING_FIABC_SUCCESSION_MANIFEST@1.0.0"
PREFLIGHT_CONTRACT_ID = "RAWLSING_FIABC_SUCCESSION_PREFLIGHT@1.0.0"
PROFILE_SCHEMA_ID = "RAWLSING_FIABC_SUCCESSION_GOVERNING_PROFILE@1.0.0"
PHASES = tuple(f"P{i:02d}" for i in range(11))
ZERO_SHA256 = "0" * 64
_RE_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_RE_SHA64 = re.compile(r"^[0-9a-f]{64}$")

_SCHEMA_PATH = Path(__file__).with_name("fiabc_succession_manifest_schema.json")
_PROFILE_PATH = Path(__file__).with_name("fiabc_succession_governing_profile.json")
REQUIRED_CURRENT_EXECUTION_PROVENANCE_PATHS: tuple[str, ...] = (
    "rawlsing_next/ee_p2x_darwin_stage_backend.py",
    "rawlsing_next/fiabc_lits_common_representation.py",
    "rawlsing_next/fiabc_lits_i_representation_authority.py",
    "rawlsing_next/fiabc_final_oracle_freeze_producers.py",
)


@dataclass(frozen=True)
class ResolvedEvidence:
    commit_sha: str
    blob_sha: str
    content_sha256: str


class EvidenceResolver(Protocol):
    """Resolve one exact evidence ref without changing its declared meaning."""

    def resolve(self, evidence_ref: Mapping[str, Any]) -> ResolvedEvidence:
        ...


class GitEvidenceResolver:
    """Resolve manifest evidence against a local checkout using exact git refs.

    No network, checkout mutation, branch movement, or content normalization is
    performed.  The preflight itself already rejects floating/fuzzy refs; this
    resolver verifies the declared commit/path/blob/content relation.
    """

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root).resolve()

    def _git(self, *args: str, binary: bool = False) -> bytes | str:
        proc = subprocess.run(
            ["git", "-C", str(self.repo_root), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode != 0:
            message = proc.stderr.decode("utf-8", errors="replace").strip()
            raise ValueError(message or f"git command failed: {' '.join(args)}")
        if binary:
            return proc.stdout
        return proc.stdout.decode("utf-8").strip()

    def resolve(self, evidence_ref: Mapping[str, Any]) -> ResolvedEvidence:
        commit = str(evidence_ref.get("resolved_commit_sha", ""))
        path = str(evidence_ref.get("path", ""))
        if not _RE_SHA40.fullmatch(commit):
            raise ValueError("resolved_commit_sha is not a full commit SHA")
        if not path or path.startswith("/") or ".." in Path(path).parts:
            raise ValueError("evidence path is not repository-relative")
        resolved = str(self._git("rev-parse", "--verify", f"{commit}^{{commit}}"))
        if resolved != commit:
            raise ValueError("declared commit does not resolve exactly")
        blob = str(self._git("rev-parse", "--verify", f"{commit}:{path}"))
        raw = self._git("show", f"{commit}:{path}", binary=True)
        assert isinstance(raw, bytes)
        return ResolvedEvidence(
            commit_sha=resolved,
            blob_sha=blob,
            content_sha256=hashlib.sha256(raw).hexdigest(),
        )


class _SchemaValidator:
    """Small deterministic validator for the JSON-Schema features B05 uses."""

    def __init__(self, root_schema: Mapping[str, Any]) -> None:
        self.root = root_schema
        self.errors: list[str] = []

    def validate(self, instance: Any) -> list[str]:
        self.errors = []
        self._validate(instance, self.root, "$")
        return list(self.errors)

    def _resolve_ref(self, ref: str) -> Mapping[str, Any]:
        if not ref.startswith("#/"):
            raise ValueError(f"unsupported nonlocal schema ref: {ref}")
        node: Any = self.root
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            node = node[part]
        if not isinstance(node, Mapping):
            raise ValueError(f"schema ref does not resolve to object: {ref}")
        return node

    @staticmethod
    def _type_matches(value: Any, expected: str) -> bool:
        if expected == "object":
            return isinstance(value, dict)
        if expected == "array":
            return isinstance(value, list)
        if expected == "string":
            return isinstance(value, str)
        if expected == "boolean":
            return isinstance(value, bool)
        if expected == "null":
            return value is None
        if expected == "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        if expected == "number":
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        return False

    def _matches(self, value: Any, schema: Mapping[str, Any]) -> bool:
        nested = _SchemaValidator(self.root)
        nested._validate(value, schema, "$")
        return not nested.errors

    def _validate(self, value: Any, schema: Mapping[str, Any], path: str) -> None:
        if "$ref" in schema:
            self._validate(value, self._resolve_ref(str(schema["$ref"])), path)

        if "allOf" in schema:
            for index, sub in enumerate(schema["allOf"]):
                self._validate(value, sub, f"{path}.allOf[{index}]")

        if "if" in schema and self._matches(value, schema["if"]):
            then_schema = schema.get("then")
            if isinstance(then_schema, Mapping):
                self._validate(value, then_schema, path)

        if "const" in schema and value != schema["const"]:
            self.errors.append(f"{path}: expected const {schema['const']!r}")
        if "enum" in schema and value not in schema["enum"]:
            self.errors.append(f"{path}: value not in enum")

        expected_type = schema.get("type")
        if expected_type is not None:
            types = expected_type if isinstance(expected_type, list) else [expected_type]
            if not any(self._type_matches(value, str(item)) for item in types):
                self.errors.append(f"{path}: wrong type")
                return

        if isinstance(value, str):
            if "minLength" in schema and len(value) < int(schema["minLength"]):
                self.errors.append(f"{path}: string shorter than minLength")
            pattern = schema.get("pattern")
            if pattern is not None and re.search(str(pattern), value) is None:
                self.errors.append(f"{path}: string does not match pattern")

        if isinstance(value, list):
            if "minItems" in schema and len(value) < int(schema["minItems"]):
                self.errors.append(f"{path}: too few items")
            if schema.get("uniqueItems"):
                seen: set[str] = set()
                for item in value:
                    token = json.dumps(item, sort_keys=True, separators=(",", ":"))
                    if token in seen:
                        self.errors.append(f"{path}: duplicate item")
                        break
                    seen.add(token)
            item_schema = schema.get("items")
            if isinstance(item_schema, Mapping):
                for index, item in enumerate(value):
                    self._validate(item, item_schema, f"{path}[{index}]")

        if isinstance(value, dict):
            required = schema.get("required", [])
            for key in required:
                if key not in value:
                    self.errors.append(f"{path}: missing required property {key!r}")
            properties = schema.get("properties", {})
            if isinstance(properties, Mapping):
                for key, sub in properties.items():
                    if key in value and isinstance(sub, Mapping):
                        self._validate(value[key], sub, f"{path}.{key}")
            if schema.get("additionalProperties") is False and isinstance(properties, Mapping):
                unknown = sorted(set(value) - set(properties))
                for key in unknown:
                    self.errors.append(f"{path}: additional property {key!r} forbidden")


@dataclass(frozen=True)
class PreflightResult:
    status: str
    checks: tuple[Mapping[str, Any], ...]
    evaluated_manifest_sha256: str

    @property
    def failure_codes(self) -> tuple[str, ...]:
        codes: list[str] = []
        for check in self.checks:
            code = check.get("failure_code")
            if isinstance(code, str) and code not in codes:
                codes.append(code)
        return tuple(codes)

    def as_dict(self) -> dict[str, Any]:
        return {
            "contract_id": PREFLIGHT_CONTRACT_ID,
            "status": self.status,
            "checks": [dict(check) for check in self.checks],
            "evaluated_manifest_sha256": self.evaluated_manifest_sha256,
        }


class SuccessionPreflightBlocked(RuntimeError):
    pass


class _Accumulator:
    def __init__(self, manifest_digest: str) -> None:
        self.manifest_digest = manifest_digest
        self._failures: dict[str, list[tuple[str, tuple[Mapping[str, Any], ...]]]] = {
            phase: [] for phase in PHASES
        }
        self._pass_evidence: dict[str, list[Mapping[str, Any]]] = {phase: [] for phase in PHASES}

    def evidence(self, phase: str, *refs: Any) -> None:
        for ref in refs:
            if _is_evidence_ref(ref):
                if _ref_key(ref) not in {_ref_key(item) for item in self._pass_evidence[phase]}:
                    self._pass_evidence[phase].append(ref)

    def fail(self, phase: str, code: str, *refs: Any) -> None:
        clean = tuple(ref for ref in refs if _is_evidence_ref(ref))
        token = (code, tuple(_ref_key(ref) for ref in clean))
        existing = {(item[0], tuple(_ref_key(ref) for ref in item[1])) for item in self._failures[phase]}
        if token not in existing:
            self._failures[phase].append((code, clean))

    def build(self) -> PreflightResult:
        checks: list[Mapping[str, Any]] = []
        any_failure = False
        for phase in PHASES:
            failures = self._failures[phase]
            if failures:
                any_failure = True
                for code, refs in failures:
                    checks.append(
                        {
                            "check_id": phase,
                            "status": "BLOCK",
                            "failure_code": code,
                            "evidence_refs": [dict(ref) for ref in refs],
                        }
                    )
            else:
                checks.append(
                    {
                        "check_id": phase,
                        "status": "PASS",
                        "failure_code": None,
                        "evidence_refs": [dict(ref) for ref in self._pass_evidence[phase]],
                    }
                )
        return PreflightResult(
            status="BLOCK" if any_failure else "PASS",
            checks=tuple(checks),
            evaluated_manifest_sha256=self.manifest_digest,
        )


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object at {path}")
    return value


def load_governing_profile() -> dict[str, Any]:
    profile = _load_json(_PROFILE_PATH)
    if profile.get("profile_schema") != PROFILE_SCHEMA_ID:
        raise ValueError("invalid FIABC succession governing profile")
    return profile


def _normalized_manifest_for_digest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Return the deterministic freeze preimage.

    B05 requires a content hash inside the manifest and also requires the
    evaluator output inside that same manifest.  A literal self-hash is
    impossible.  The governed implementation therefore hashes the complete
    preflight input with only the self-hash field and evaluator-output block
    normalized to fixed sentinels.  Candidate output never participates in
    this preimage.
    """

    value = copy.deepcopy(dict(manifest))
    identity = value.get("manifest_identity")
    if not isinstance(identity, dict):
        identity = {}
        value["manifest_identity"] = identity
    identity["manifest_content_sha256"] = ZERO_SHA256
    value["preflight_evaluation"] = {
        "contract_id": PREFLIGHT_CONTRACT_ID,
        "status": "BLOCK",
        "checks": [
            {
                "check_id": "UNEVALUATED",
                "status": "BLOCK",
                "failure_code": "PF_UNEVALUATED",
                "evidence_refs": [],
            }
        ],
        "evaluated_manifest_sha256": ZERO_SHA256,
    }
    return value


def compute_manifest_digest(manifest: Mapping[str, Any]) -> str:
    normalized = _normalized_manifest_for_digest(manifest)
    encoded = json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def seal_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy carrying the deterministic pre-execution freeze digest."""

    value = copy.deepcopy(dict(manifest))
    digest = compute_manifest_digest(value)
    identity = value.setdefault("manifest_identity", {})
    identity["manifest_content_sha256"] = digest
    value["preflight_evaluation"] = {
        "contract_id": PREFLIGHT_CONTRACT_ID,
        "status": "BLOCK",
        "checks": [
            {
                "check_id": "UNEVALUATED",
                "status": "BLOCK",
                "failure_code": "PF_UNEVALUATED",
                "evidence_refs": [],
            }
        ],
        "evaluated_manifest_sha256": digest,
    }
    return value


def _is_evidence_ref(value: Any) -> bool:
    return isinstance(value, Mapping) and {"repo", "path", "ref", "resolved_commit_sha", "evidence_class"}.issubset(value)


def _ref_key(ref: Mapping[str, Any]) -> str:
    return json.dumps(dict(ref), sort_keys=True, separators=(",", ":"))


def _iter_evidence_refs(value: Any) -> Iterable[Mapping[str, Any]]:
    if _is_evidence_ref(value):
        yield value
        return
    if isinstance(value, Mapping):
        for child in value.values():
            yield from _iter_evidence_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_evidence_refs(child)


def _same_ref_identity(ref: Any, expected: Mapping[str, Any]) -> bool:
    if not _is_evidence_ref(ref):
        return False
    return (
        ref.get("repo") == expected.get("repo", "maidiu/rawlsing")
        and ref.get("path") == expected.get("path")
        and ref.get("resolved_commit_sha") == expected.get("resolved_commit_sha")
    )


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _missingness_complete(value: Any) -> bool:
    node = _as_dict(value)
    flags = (
        "historical_authority_checked",
        "alternate_current_owner_checked",
        "disconnected_binding_checked",
        "superseded_implementation_checked",
        "intentional_deferral_checked",
    )
    return all(node.get(flag) is True for flag in flags) and bool(_as_list(node.get("search_evidence_refs")))


def _schema_errors(manifest: Mapping[str, Any]) -> list[str]:
    try:
        schema = _load_json(_SCHEMA_PATH)
        return _SchemaValidator(schema).validate(manifest)
    except Exception as exc:  # fail closed if the validator/schema cannot load
        return [f"schema validator unavailable: {exc}"]


def _validate_evidence_refs(
    manifest: Mapping[str, Any],
    lifecycle_context: Mapping[str, Any] | None,
    resolver: EvidenceResolver | None,
    acc: _Accumulator,
) -> set[str]:
    invalid: set[str] = set()
    all_refs = list(_iter_evidence_refs(manifest))
    if lifecycle_context is not None:
        all_refs.extend(_iter_evidence_refs(lifecycle_context))

    seen: set[str] = set()
    for ref in all_refs:
        key = _ref_key(ref)
        if key in seen:
            continue
        seen.add(key)
        supplied = str(ref.get("ref", ""))
        resolved = str(ref.get("resolved_commit_sha", ""))
        acc.evidence("P00", ref)

        # The current court admits only full immutable commit refs.  A branch,
        # HEAD/latest/default token, short SHA, or revision expression cannot
        # become exact merely because a resolved SHA is also written nearby.
        if not _RE_SHA40.fullmatch(supplied) or supplied != resolved:
            acc.fail("P00", "PF_FLOATING_OR_FUZZY_REF", ref)
            invalid.add(key)
            continue
        if ref.get("repo") != "maidiu/rawlsing" or not _RE_SHA40.fullmatch(resolved):
            acc.fail("P00", "PF_REF_UNRESOLVED", ref)
            invalid.add(key)
            continue
        if resolver is None:
            acc.fail("P00", "PF_REF_UNRESOLVED", ref)
            invalid.add(key)
            continue
        try:
            actual = resolver.resolve(ref)
        except Exception:
            acc.fail("P00", "PF_REF_UNRESOLVED", ref)
            invalid.add(key)
            continue
        if actual.commit_sha != resolved:
            acc.fail("P00", "PF_REF_UNRESOLVED", ref)
            invalid.add(key)
        declared_blob = ref.get("git_blob_sha")
        if declared_blob is not None and declared_blob != actual.blob_sha:
            acc.fail("P00", "PF_REF_CONTENT_MISMATCH", ref)
            invalid.add(key)
        declared_content = ref.get("content_sha256")
        if declared_content is not None and declared_content != actual.content_sha256:
            acc.fail("P00", "PF_REF_CONTENT_MISMATCH", ref)
            invalid.add(key)
    return invalid


def evaluate_manifest(
    manifest: Mapping[str, Any],
    *,
    resolver: EvidenceResolver | None,
    lifecycle_context: Mapping[str, Any] | None,
    profile: Mapping[str, Any] | None = None,
) -> PreflightResult:
    """Evaluate P00-P10 and return PASS only on complete closure."""

    governing = dict(profile) if profile is not None else load_governing_profile()
    digest = compute_manifest_digest(manifest)
    acc = _Accumulator(digest)

    # P00 — schema, freeze identity, exact refs/content.
    if _schema_errors(manifest):
        acc.fail("P00", "PF_SCHEMA_INVALID")
    identity = _as_dict(manifest.get("manifest_identity"))
    if identity.get("frozen_before_candidate_execution") is not True:
        acc.fail("P00", "PF_MANIFEST_NOT_PREOUTPUT_FROZEN")
    if identity.get("manifest_content_sha256") != digest:
        acc.fail("P00", "PF_REF_CONTENT_MISMATCH")
    prior_evaluation = _as_dict(manifest.get("preflight_evaluation"))
    if prior_evaluation.get("evaluated_manifest_sha256") != digest:
        acc.fail("P00", "PF_REF_CONTENT_MISMATCH")
    invalid_refs = _validate_evidence_refs(manifest, lifecycle_context, resolver, acc)
    head_bindings = _as_dict(manifest.get("current_head_bindings"))
    manifest_head = identity.get("generated_from_commit_sha")
    binding_head = head_bindings.get("generated_from_commit_sha")
    required_files = _as_dict(head_bindings.get("required_files"))
    if (
        not isinstance(manifest_head, str)
        or not _RE_SHA40.fullmatch(manifest_head)
        or binding_head != manifest_head
    ):
        acc.fail("P00", "PF_CURRENT_HEAD_BINDING_HEAD_MISMATCH")
    for path in REQUIRED_CURRENT_EXECUTION_PROVENANCE_PATHS:
        ref = required_files.get(path)
        if not _is_evidence_ref(ref):
            acc.fail("P00", "PF_CURRENT_HEAD_BINDING_MISSING")
            continue
        if (
            ref.get("path") != path
            or ref.get("ref") != manifest_head
            or ref.get("resolved_commit_sha") != manifest_head
            or ref.get("evidence_class") != "CURRENT_IMPLEMENTATION"
        ):
            acc.fail("P00", "PF_CURRENT_HEAD_BINDING_MISMATCH", ref)

    scope = _as_dict(manifest.get("court_scope"))
    terminal = _as_dict(manifest.get("comparison_terminal"))
    upstream = _as_dict(manifest.get("upstream_freeze"))
    chains = [item for item in _as_list(manifest.get("function_chains")) if isinstance(item, dict)]
    invariants = [item for item in _as_list(manifest.get("abc_invariants")) if isinstance(item, dict)]
    capabilities = [item for item in _as_list(manifest.get("source_candidate_capabilities")) if isinstance(item, dict)]

    profile_scope = _as_dict(governing.get("court_scope"))
    profile_terminal = _as_dict(governing.get("comparison_terminal"))
    profile_authority = _as_dict(governing.get("semantic_authority_closure"))
    boundary_ref = _as_dict(profile_terminal.get("boundary_adjudication_ref"))

    # P01 — exact comparison boundary and complete inherited-function map.
    if terminal.get("state") != "PROVED" or terminal.get("terminal_id") != profile_terminal.get("terminal_id"):
        acc.fail("P01", "PF_COMPARISON_TERMINAL_UNRESOLVED", terminal.get("resolution_evidence_ref"))
    if not _same_ref_identity(terminal.get("boundary_adjudication_ref"), boundary_ref):
        acc.fail("P01", "PF_COMPARISON_TERMINAL_UNRESOLVED", terminal.get("boundary_adjudication_ref"))
    else:
        acc.evidence("P01", terminal.get("boundary_adjudication_ref"))

    expected_sources = set(_as_list(profile_scope.get("sources")))
    expected_candidates = set(_as_list(profile_scope.get("candidates")))
    if set(_as_list(scope.get("sources"))) != expected_sources or set(_as_list(scope.get("candidates"))) != expected_candidates:
        acc.fail("P01", "PF_OBLIGATION_UNMAPPED", scope.get("workload_ref"))
    if scope.get("claim_scope_id") != profile_scope.get("claim_scope_id"):
        acc.fail("P01", "PF_OBLIGATION_UNMAPPED", scope.get("workload_ref"))
    if not _same_ref_identity(scope.get("workload_ref"), _as_dict(profile_scope.get("workload_ref"))):
        acc.fail("P01", "PF_OBLIGATION_UNMAPPED", scope.get("workload_ref"))

    boundary = _as_dict(governing.get("function_boundary"))
    all_functions = set(_as_list(boundary.get("all_functions")))
    required_functions = set(_as_list(boundary.get("required_before_terminal")))
    deferred_functions = set(_as_list(boundary.get("deferred_beyond_terminal")))
    chain_by_id: dict[str, dict[str, Any]] = {}
    duplicate_ids: set[str] = set()
    for chain in chains:
        function_id = chain.get("function_id")
        if not isinstance(function_id, str):
            continue
        if function_id in chain_by_id:
            duplicate_ids.add(function_id)
        chain_by_id[function_id] = chain
        obligation = _as_dict(chain.get("obligation"))
        if obligation.get("function_id") != function_id:
            acc.fail("P01", "PF_OBLIGATION_UNMAPPED", obligation.get("historical_evidence_ref"))
    if set(chain_by_id) != all_functions or duplicate_ids:
        acc.fail("P01", "PF_OBLIGATION_UNMAPPED")

    for function_id in required_functions:
        chain = chain_by_id.get(function_id, {})
        if chain.get("comparison_requirement") != "REQUIRED_BEFORE_TERMINAL":
            acc.fail("P01", "PF_DEFERMENT_UNPROVED", chain.get("deferment_authority_ref"))
        if chain.get("disposition") == "INTENTIONALLY_DEFERRED_BEYOND_COMPARISON_BOUNDARY":
            acc.fail("P01", "PF_DEFERMENT_UNPROVED", chain.get("deferment_authority_ref"))
    for function_id in deferred_functions:
        chain = chain_by_id.get(function_id, {})
        if chain.get("comparison_requirement") != "INTENTIONALLY_DEFERRED_BEYOND_TERMINAL":
            acc.fail("P01", "PF_DEFERMENT_UNPROVED", chain.get("deferment_authority_ref"))
        if chain.get("disposition") != "INTENTIONALLY_DEFERRED_BEYOND_COMPARISON_BOUNDARY":
            acc.fail("P01", "PF_DEFERMENT_UNPROVED", chain.get("deferment_authority_ref"))
        if not _same_ref_identity(chain.get("deferment_authority_ref"), boundary_ref):
            acc.fail("P01", "PF_DEFERMENT_UNPROVED", chain.get("deferment_authority_ref"))
    if any(chain.get("comparison_requirement") == "UNRESOLVED_BOUNDARY" for chain in chains):
        acc.fail("P01", "PF_COMPARISON_TERMINAL_UNRESOLVED")

    # P02 — exact semantic/manual authority; no binder/label inference.
    for function_id in required_functions:
        chain = chain_by_id.get(function_id, {})
        authorities = [item for item in _as_list(chain.get("accepted_authority")) if isinstance(item, dict)]
        if not authorities:
            acc.fail("P02", "PF_AUTHORITY_MISSING")
            continue
        jurisdiction_to_ids: dict[str, set[str]] = {}
        for authority in authorities:
            acc.evidence("P02", authority.get("authority_ref"), authority.get("resolution_evidence_ref"))
            if authority.get("state") != "PROVED":
                acc.fail("P02", "PF_AUTHORITY_MISSING", authority.get("resolution_evidence_ref"))
            if authority.get("scope_exact") is not True:
                acc.fail("P02", "PF_AUTHORITY_SCOPE_MISMATCH", authority.get("authority_ref"))
            authority_ref = _as_dict(authority.get("authority_ref"))
            if not authority_ref:
                acc.fail("P02", "PF_AUTHORITY_MISSING", authority.get("resolution_evidence_ref"))
            elif authority_ref.get("evidence_class") not in {"ACCEPTED_AUTHORITY", "COURT_ADJUDICATION"}:
                acc.fail("P02", "PF_SEMANTIC_INFERENCE_SUBSTITUTION", authority_ref)
            jurisdiction = str(authority.get("semantic_jurisdiction", ""))
            authority_id = str(authority.get("authority_id", ""))
            jurisdiction_to_ids.setdefault(jurisdiction, set()).add(authority_id)
        if any(len(ids) > 1 for ids in jurisdiction_to_ids.values()):
            acc.fail("P02", "PF_AUTHORITY_AMBIGUOUS")
        if chain.get("disposition") == "GENUINELY_MISSING" and not _missingness_complete(chain.get("missingness_search")):
            acc.fail("P02", "PF_MISSINGNESS_NOT_FALSIFIED_FIRST")

    # P03 — current owner and semantic-owner jurisdiction are separate from cost.
    for function_id in required_functions:
        chain = chain_by_id.get(function_id, {})
        owner = _as_dict(chain.get("current_owner"))
        authorities = [item for item in _as_list(chain.get("accepted_authority")) if isinstance(item, dict)]
        authority_ids = {str(item.get("authority_id")) for item in authorities if item.get("state") == "PROVED"}
        if owner.get("state") != "PROVED":
            acc.fail("P03", "PF_CURRENT_OWNER_UNRESOLVED", owner.get("resolution_evidence_ref"))
        if owner.get("owner_status") in {"SUPERSEDED", "HISTORICAL_ONLY"}:
            acc.fail("P03", "PF_OWNER_SUPERSEDED_OR_HISTORICAL", owner.get("implementation_ref"))
        elif owner.get("owner_status") != "CURRENT":
            acc.fail("P03", "PF_CURRENT_OWNER_UNRESOLVED", owner.get("resolution_evidence_ref"))
        implementation_ref = _as_dict(owner.get("implementation_ref"))
        if not implementation_ref or implementation_ref.get("evidence_class") != "CURRENT_IMPLEMENTATION":
            acc.fail("P03", "PF_CURRENT_OWNER_UNRESOLVED", implementation_ref)
        semantic_owner = str(owner.get("semantic_owner_id", ""))
        abc_class = _as_dict(chain.get("abc_class"))
        if semantic_owner not in authority_ids or abc_class.get("semantic_owner_id") != semantic_owner:
            acc.fail("P03", "PF_OWNER_AUTHORITY_JURISDICTION_MISMATCH", owner.get("resolution_evidence_ref"))
        acc.evidence("P03", implementation_ref, owner.get("currentness_ref"))

    # P04 — adopted code must actually bind the current owner to the live consumer.
    for function_id in required_functions:
        chain = chain_by_id.get(function_id, {})
        owner = _as_dict(chain.get("current_owner"))
        binding = _as_dict(chain.get("executable_binding"))
        consumer = _as_dict(chain.get("live_consumer"))
        binding_ref = _as_dict(binding.get("binding_ref"))
        if binding.get("state") != "PROVED":
            acc.fail("P04", "PF_EXECUTABLE_BINDING_MISSING", binding.get("resolution_evidence_ref"))
        if binding.get("producer_owner_id") != owner.get("owner_id") or binding.get("binding_identity_matches_owner") is not True:
            acc.fail("P04", "PF_BINDING_OWNER_MISMATCH", binding_ref)
            if binding.get("binding_identity_matches_owner") is not True:
                acc.fail("P04", "PF_WRAPPER_SHADOWS_CURRENT_OWNER", binding_ref)
        if binding.get("consumer_id") != consumer.get("consumer_id"):
            acc.fail("P04", "PF_PRODUCER_CONSUMER_CONTRACT_MISMATCH", binding.get("contract_receipt_ref"))
        if not binding_ref:
            acc.fail("P04", "PF_EXECUTABLE_BINDING_MISSING", binding.get("resolution_evidence_ref"))
        elif _ref_key(binding_ref) in invalid_refs:
            acc.fail("P04", "PF_BINDING_REF_STALE", binding_ref)
        contract_receipt = _as_dict(binding.get("contract_receipt_ref"))
        if not contract_receipt or contract_receipt.get("evidence_class") != "GOVERNED_EXECUTION_RECEIPT":
            acc.fail("P04", "PF_PRODUCER_CONSUMER_CONTRACT_MISMATCH", contract_receipt)
        acc.evidence("P04", binding_ref, contract_receipt)

    # P05 — static reachability never substitutes for a post-repair live receipt.
    for function_id in required_functions:
        consumer = _as_dict(chain_by_id.get(function_id, {}).get("live_consumer"))
        if consumer.get("state") != "LIVE":
            acc.fail("P05", "PF_LIVE_CONSUMER_DISCONNECTED", consumer.get("resolution_evidence_ref"))
            acc.fail("P05", "PF_LIVE_RECEIPT_MISSING", consumer.get("resolution_evidence_ref"))
        if not _is_evidence_ref(consumer.get("receipt_ref")):
            acc.fail("P05", "PF_LIVE_RECEIPT_MISSING", consumer.get("resolution_evidence_ref"))
        if consumer.get("receipt_code_commit_matches") is not True:
            acc.fail("P05", "PF_LIVE_RECEIPT_CODE_REF_MISMATCH", consumer.get("receipt_ref"))
        if consumer.get("receipt_after_required_repairs") is not True:
            acc.fail("P05", "PF_LIVE_RECEIPT_PREDATES_REQUIRED_REPAIR", consumer.get("receipt_ref"))
        acc.evidence("P05", consumer.get("receipt_ref"), consumer.get("execution_code_ref"))

    # P06 — typed negative states plus exact replay/provenance/authority closure.
    for function_id in required_functions:
        chain = chain_by_id.get(function_id, {})
        law = _as_dict(chain.get("negative_state_law"))
        distinctions = _as_list(law.get("required_distinctions"))
        if law.get("state") not in {"PROVED", "LIVE"}:
            acc.fail("P06", "PF_NEGATIVE_STATE_LAW_UNRESOLVED", law.get("resolution_evidence_ref"))
        if law.get("collapse_forbidden") is not True or not distinctions or len(distinctions) != len(set(map(str, distinctions))):
            acc.fail("P06", "PF_NEGATIVE_STATE_COLLAPSE", law.get("law_ref"))
        if not _is_evidence_ref(law.get("law_ref")) or not _is_evidence_ref(law.get("consumer_preservation_proof_ref")):
            acc.fail("P06", "PF_NEGATIVE_STATE_LAW_UNRESOLVED", law.get("resolution_evidence_ref"))
        provenance = [item for item in _as_list(chain.get("provenance_refs")) if _is_evidence_ref(item)]
        if not provenance:
            acc.fail("P06", "PF_REPLAY_PROVENANCE_UNCLOSED")
        acc.evidence("P06", law.get("law_ref"), law.get("consumer_preservation_proof_ref"), *provenance)

    authority_ref = _as_dict(upstream.get("semantic_authority_closure_ref"))
    if (
        upstream.get("state") != "PROVED"
        or upstream.get("candidate_neutral_work_frozen") is not True
        or not _same_ref_identity(authority_ref, _as_dict(profile_authority.get("closure_ref")))
    ):
        acc.fail("P06", "PF_AUTHORITY_CLOSURE_UNPROVED", authority_ref)
    if not _as_list(upstream.get("producer_outputs")):
        acc.fail("P06", "PF_REPLAY_PROVENANCE_UNCLOSED", upstream.get("resolution_evidence_ref"))
    else:
        acc.evidence("P06", authority_ref, upstream.get("resolution_evidence_ref"), *_as_list(upstream.get("producer_outputs")))

    # P07 — cross-candidate invariants and independent pre-output oracle.
    invariant_by_id = {item.get("invariant_id"): item for item in invariants if isinstance(item.get("invariant_id"), str)}
    for invariant in invariants:
        if invariant.get("state") != "PROVED":
            acc.fail("P07", "PF_ABC_INVARIANT_UNRESOLVED", invariant.get("resolution_evidence_ref"))
        if invariant.get("must_match_across_abc") is True and not _is_evidence_ref(invariant.get("proof_ref")):
            acc.fail("P07", "PF_ABC_INVARIANT_UNRESOLVED", invariant.get("resolution_evidence_ref"))
        acc.evidence("P07", invariant.get("authority_ref"), invariant.get("proof_ref"))
    for function_id in required_functions:
        abc_class = _as_dict(chain_by_id.get(function_id, {}).get("abc_class"))
        invariant_ids = _as_list(abc_class.get("invariant_ids"))
        if not invariant_ids or any(item not in invariant_by_id for item in invariant_ids):
            acc.fail("P07", "PF_ABC_INVARIANT_UNRESOLVED")
        if abc_class.get("must_match_semantically") is not True:
            acc.fail("P07", "PF_ABC_INVARIANT_UNRESOLVED")

    oracle = _as_dict(manifest.get("parity_oracle"))
    if oracle.get("state") != "PROVED":
        acc.fail("P07", "PF_ORACLE_NOT_PREOUTPUT_FROZEN", oracle.get("resolution_evidence_ref"))
        acc.fail("P07", "PF_FIXED_FRONTIER_UNRESOLVED", oracle.get("fixed_frontier_ref"))
    if oracle.get("frozen_before_candidate_output") is not True:
        acc.fail("P07", "PF_ORACLE_NOT_PREOUTPUT_FROZEN", oracle.get("oracle_material_ref"))
    if oracle.get("candidate_output_used_to_construct_expected_truth") is not False:
        acc.fail("P07", "PF_ORACLE_DERIVED_FROM_CANDIDATE_OUTPUT", oracle.get("oracle_material_ref"))
        acc.fail("P07", "PF_SELF_REPLAY_USED_AS_PARITY", oracle.get("oracle_material_ref"))
    oracle_material = _as_dict(oracle.get("oracle_material_ref"))
    if not oracle_material or oracle_material.get("evidence_class") == "GOVERNED_EXECUTION_RECEIPT":
        acc.fail("P07", "PF_ORACLE_DERIVED_FROM_CANDIDATE_OUTPUT", oracle_material)
    production_keys = {
        _ref_key(ref)
        for item in capabilities
        for ref in [_as_dict(item.get("production_realization_ref"))]
        if ref
    }
    if oracle_material and _ref_key(oracle_material) in production_keys:
        acc.fail("P07", "PF_ORACLE_DERIVED_FROM_CANDIDATE_OUTPUT", oracle_material)
        acc.fail("P07", "PF_SELF_REPLAY_USED_AS_PARITY", oracle_material)
    if not _is_evidence_ref(oracle.get("fixed_frontier_ref")):
        acc.fail("P07", "PF_FIXED_FRONTIER_UNRESOLVED", oracle.get("resolution_evidence_ref"))
    acc.evidence(
        "P07",
        oracle.get("resolution_evidence_ref"),
        oracle.get("oracle_contract_ref"),
        oracle.get("oracle_material_ref"),
        oracle.get("fixed_frontier_ref"),
        oracle.get("negative_state_expectation_ref"),
    )

    # P08 — every frozen source x candidate production cell is positively proved.
    expected_cells = {(source, candidate) for source in expected_sources for candidate in expected_candidates}
    cells: dict[tuple[str, str], dict[str, Any]] = {}
    duplicate_cells: set[tuple[str, str]] = set()
    for item in capabilities:
        key = (str(item.get("source_id", "")), str(item.get("candidate_id", "")))
        if key in cells:
            duplicate_cells.add(key)
        cells[key] = item
    if set(cells) != expected_cells or duplicate_cells:
        acc.fail("P08", "PF_SOURCE_CANDIDATE_CAPABILITY_MISSING")
    nonqualifying_dispositions = {
        "PRESERVED_BUT_DISCONNECTED",
        "AUTHORITY_EXISTS_RUNTIME_INTEGRATION_MISSING",
        "PARTIAL_SUCCESSION",
        "SUPERSEDED_IMPLEMENTATION_FUNCTION_PRESERVED",
        "GENUINELY_MISSING",
        "UNPROVED__DEEPER_ARCHAEOLOGY_REQUIRED",
    }
    for source, candidate in expected_cells:
        cell = cells.get((source, candidate), {})
        state = cell.get("state")
        disposition = cell.get("disposition")
        if state not in {"PROVED", "LIVE"} or disposition in nonqualifying_dispositions:
            acc.fail("P08", "PF_SOURCE_CANDIDATE_CAPABILITY_MISSING", cell.get("resolution_evidence_ref"))
            if source == "WVS7" and candidate == "C":
                acc.fail("P08", "PF_SOURCE_PORTABILITY_UNPROVED", cell.get("resolution_evidence_ref"))
        if state == "NOT_APPLICABLE":
            acc.fail("P08", "PF_UNAUTHORIZED_NOT_APPLICABLE_ESCAPE", cell.get("resolution_evidence_ref"))
        if not _is_evidence_ref(cell.get("production_realization_ref")):
            acc.fail("P08", "PF_PARTIAL_PREIMAGE_SET", cell.get("capability_contract_ref"))
        if cell.get("synthetic_fixture_substitution_forbidden") is not True:
            acc.fail("P08", "PF_SYNTHETIC_FIXTURE_SUBSTITUTION", cell.get("production_realization_ref"))
        if disposition == "GENUINELY_MISSING" and not _missingness_complete(cell.get("missingness_search")):
            acc.fail("P08", "PF_SOURCE_CANDIDATE_CAPABILITY_MISSING", cell.get("resolution_evidence_ref"))
        acc.evidence("P08", cell.get("capability_contract_ref"), cell.get("production_realization_ref"))

    # P09 — equal-work contract, immutable candidate-local metrics, owner separation.
    accounting = _as_dict(manifest.get("accounting_contract"))
    if accounting.get("state") != "PROVED":
        acc.fail("P09", "PF_EQUAL_WORK_ACCOUNTING_UNRESOLVED", accounting.get("resolution_evidence_ref"))
    if accounting.get("semantic_owner_cost_owner_separated") is not True:
        acc.fail("P09", "PF_SEMANTIC_COST_OWNERSHIP_CONFLATED", accounting.get("constitution_ref"))
    if not _is_evidence_ref(accounting.get("candidate_start_stop_ref")):
        acc.fail("P09", "PF_CANDIDATE_START_STOP_UNRESOLVED", accounting.get("resolution_evidence_ref"))
    if not _is_evidence_ref(accounting.get("preserved_work_treatment_ref")):
        acc.fail("P09", "PF_PRESERVED_WORK_ASYMMETRIC", accounting.get("resolution_evidence_ref"))
    if not _is_evidence_ref(accounting.get("candidate_process_isolation_ref")):
        acc.fail("P09", "PF_METRIC_NOT_CANDIDATE_LOCAL", accounting.get("resolution_evidence_ref"))

    metrics = [item for item in _as_list(accounting.get("metrics")) if isinstance(item, dict)]
    if not metrics:
        acc.fail("P09", "PF_EQUAL_WORK_ACCOUNTING_UNRESOLVED", accounting.get("resolution_evidence_ref"))
    metric_methods: dict[str, str] = {}
    for metric in metrics:
        metric_id = str(metric.get("metric_id", ""))
        method = str(metric.get("method_identity_across_candidates", ""))
        if metric.get("candidate_local") is not True:
            acc.fail("P09", "PF_METRIC_NOT_CANDIDATE_LOCAL", metric.get("definition_ref"))
        if metric.get("overwritten_before_terminal") is not False:
            acc.fail("P09", "PF_METRIC_OVERWRITTEN", metric.get("definition_ref"))
        if metric.get("accumulation_semantics") == "UNRESOLVED" or metric.get("measurement_kind") == "UNRESOLVED":
            acc.fail("P09", "PF_EQUAL_WORK_ACCOUNTING_UNRESOLVED", metric.get("definition_ref"))
        if metric.get("accumulation_semantics") == "DOCUMENTARY_ONLY" and metric.get("measurement_kind") == "OBSERVED":
            acc.fail("P09", "PF_DOCUMENTARY_VALUE_MISLABELED_OBSERVED", metric.get("definition_ref"))
        prior = metric_methods.get(metric_id)
        if prior is not None and prior != method:
            acc.fail("P09", "PF_METRIC_METHOD_MISMATCH", metric.get("definition_ref"))
        metric_methods[metric_id] = method
        acc.evidence("P09", metric.get("definition_ref"))
    candidate_cost_classes = {"CANDIDATE_OWNED_PHYSICAL_REALIZATION", "CANDIDATE_OWNED_EXECUTION"}
    for function_id in required_functions:
        abc_class = _as_dict(chain_by_id.get(function_id, {}).get("abc_class"))
        cost_class = abc_class.get("cost_class")
        if cost_class in {"UNRESOLVED", "EXCLUDED_DOWNSTREAM", None}:
            acc.fail("P09", "PF_EQUAL_WORK_ACCOUNTING_UNRESOLVED")
        if cost_class in candidate_cost_classes and abc_class.get("cost_owner_id") == abc_class.get("semantic_owner_id"):
            acc.fail("P09", "PF_SEMANTIC_COST_OWNERSHIP_CONFLATED")
    acc.evidence(
        "P09",
        accounting.get("constitution_ref"),
        accounting.get("candidate_start_stop_ref"),
        accounting.get("preserved_work_treatment_ref"),
        accounting.get("candidate_process_isolation_ref"),
    )

    # P10 — failure scope and lifecycle are a required external receipt context.
    lifecycle = _as_dict(lifecycle_context)
    if lifecycle.get("state") != "PROVED" or lifecycle.get("failure_scope_ambiguous") is not False:
        acc.fail("P10", "PF_FAILURE_SCOPE_AMBIGUOUS", *_as_list(lifecycle.get("evidence_refs")))
    if lifecycle.get("failure_scope_misclassified") is not False:
        acc.fail("P10", "PF_FAILURE_SCOPE_MISCLASSIFIED", *_as_list(lifecycle.get("evidence_refs")))
    if lifecycle.get("lifecycle_order_matches") is not True:
        acc.fail("P10", "PF_LIFECYCLE_ORDER_MISMATCH", *_as_list(lifecycle.get("evidence_refs")))
    if lifecycle.get("terminal_history_fresh_for_retry") is not True:
        acc.fail("P10", "PF_TERMINAL_HISTORY_STALE_FOR_RETRY", *_as_list(lifecycle.get("evidence_refs")))
    lifecycle_refs = [item for item in _as_list(lifecycle.get("evidence_refs")) if _is_evidence_ref(item)]
    if not lifecycle_refs:
        acc.fail("P10", "PF_FAILURE_SCOPE_AMBIGUOUS")
        acc.fail("P10", "PF_LIFECYCLE_ORDER_MISMATCH")
    else:
        acc.evidence("P10", *lifecycle_refs)

    return acc.build()


def require_preflight_pass(result: PreflightResult) -> None:
    """Raise unless the exact preflight result is PASS."""

    if result.status != "PASS":
        codes = ",".join(result.failure_codes) or "UNKNOWN_BLOCK"
        raise SuccessionPreflightBlocked(f"FIABC succession preflight BLOCK: {codes}")


_T = TypeVar("_T")


def run_only_after_preflight_pass(
    result: PreflightResult,
    action: Callable[..., _T],
    /,
    *args: Any,
    **kwargs: Any,
) -> _T:
    """Mechanical execution gate: BLOCK can never invoke the supplied action."""

    require_preflight_pass(result)
    return action(*args, **kwargs)


def _main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="RAWLSING FIABC mechanized succession preflight")
    parser.add_argument("--manifest", required=True, help="frozen succession manifest JSON")
    parser.add_argument("--lifecycle-context", required=True, help="governed P10 lifecycle/failure-scope receipt JSON")
    parser.add_argument("--repo-root", default=".", help="local maidiu/rawlsing checkout used only for exact evidence resolution")
    parser.add_argument("--output", help="optional path for deterministic evaluation JSON")
    args = parser.parse_args(argv)

    manifest = _load_json(Path(args.manifest))
    lifecycle = _load_json(Path(args.lifecycle_context))
    result = evaluate_manifest(
        manifest,
        resolver=GitEvidenceResolver(args.repo_root),
        lifecycle_context=lifecycle,
    )
    payload = json.dumps(result.as_dict(), sort_keys=True, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0 if result.status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(_main())
