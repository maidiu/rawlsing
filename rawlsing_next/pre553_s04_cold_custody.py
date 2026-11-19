"""Sourcefree cold custody for one ALREADY EXECUTED I03 -> S04 research product.

This is a *secondary, private, content-addressed proof sidecar*, not C11
storage, source-native admission, scientific inference, an issuer signature or
a source grant. It stores original exact I03 query/fact semantic PREIMAGES,
not only their hashes, so they can be reconstituted after process exit without
reopening the respondent corpus or rerunning I03.

Replaying a fully self-rehashed counterfeit is possible without an
INDEPENDENTLY OBTAINED original fact root. Accordingly:
- inspection may check internal consistency but cannot feed FF01;
- the FF01 cold receiver REQUIRES a separately supplied query/fact/release
  pin, not stored in this archive; this checks equality, not who issued it;
- the caller is responsible for independent source custody and rights.
Only sourcefree test artefacts may be written by this version; the sidecar
contains potentially sensitive respondent-identity references.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads
from os import O_CREAT, O_EXCL, O_RDONLY, O_WRONLY, fdopen, fsync, link, open as os_open, unlink
from pathlib import Path
from secrets import token_hex
from stat import S_IMODE, S_ISREG
from typing import Any, Mapping

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact, EmpiricalQuerySpec, ExactRef, canonical_json, exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_s04_observed_research import (
    S04ObservedKnowledge, receive_s04_i03_research,
)

CONTRACT = "S04_SOURCEFREE_COLD_I03_PREIMAGE_R1"
MAX_BYTES = 64 * 1024 * 1024
FILE_SUFFIX = ".s04-sourcefree.json"
CLAIM = "INTERNAL_EXACT_PREIMAGE_REPLAY__EXTERNAL_SOURCE_RIGHTS_NOT_ISSUED"


class S04ColdCustodyError(ValueError):
    """Cold storage fails exact preimage, source root or safety checks."""


@dataclass(frozen=True)
class S04ColdBundle:
    payload_json: str
    digest: str

    def __post_init__(self) -> None:
        if type(self.payload_json) is not str or type(self.digest) is not str:
            raise S04ColdCustodyError("cold payload/hash must be exact strings")
        if len(self.payload_json.encode("utf-8")) > MAX_BYTES:
            raise S04ColdCustodyError("cold sidecar exceeds bounded sourcefree size")
        try:
            obj = loads(self.payload_json)
            if (type(obj) is not dict or obj.get("contract") != CONTRACT
                    or canonical_json(obj) != self.payload_json
                    or semantic_hash(obj) != self.digest):
                raise S04ColdCustodyError("cold semantic preimage/hash mismatch")
        except (TypeError, ValueError) as exc:
            raise S04ColdCustodyError("malformed cold bundle") from exc

    @property
    def ref(self) -> ExactRef:
        return ExactRef(CONTRACT, f"urn:rawlsing:s04:cold:sha256:{self.digest}", self.digest)

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


@dataclass(frozen=True)
class S04ExternalRootPin:
    """Externally obtained immutable roots, NEVER sourced from the cold file.

    A caller constructing this itself from an untrusted bundle obtains no
    authentication. Even a correct pin is NOT survey/source use authorization.
    """

    query_ref: ExactRef
    fact_ref: ExactRef
    release_ref: ExactRef

    def __post_init__(self) -> None:
        if any(type(x) is not ExactRef for x in (self.query_ref, self.fact_ref, self.release_ref)):
            raise S04ColdCustodyError("external root pin requires three exact refs")
        if (self.query_ref.kind != EmpiricalQuerySpec.FAMILY
                or self.fact_ref.kind != EmpiricalFact.FAMILY):
            raise S04ColdCustodyError("external root pin has wrong scientific object family")


@dataclass(frozen=True)
class S04ColdRead:
    query: EmpiricalQuerySpec
    execution: QueryExecutionResult
    knowledge: S04ObservedKnowledge
    integrity_grade: str
    pin_grade: str

    @property
    def ref(self) -> ExactRef:
        return self.knowledge.ref


def _preimage(obj: Any, family: type) -> Any:
    if type(obj) is not dict:
        raise S04ColdCustodyError("saved original is not a complete semantic object")
    keys = {
        "schema_id", "schema_version", "object_id", "content_hash",
        "typed_state", "authority_snapshot_refs", "dependency_refs",
        "producer_replay_locator_or_reference_root", "semantic_fields",
    }
    if set(obj) != keys or type(obj["semantic_fields"]) is not dict:
        raise S04ColdCustodyError("original I03 preimage missing or contains extra fields")
    try:
        answer = family(
            typed_state=obj["typed_state"],
            authority_snapshot_refs=obj["authority_snapshot_refs"],
            dependency_refs=obj["dependency_refs"],
            producer_replay_locator_or_reference_root=obj["producer_replay_locator_or_reference_root"],
            schema_id=obj["schema_id"], schema_version=obj["schema_version"],
            object_id=obj["object_id"], content_hash=obj["content_hash"],
            **obj["semantic_fields"],
        )
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise S04ColdCustodyError("cannot reconstruct original I03 semantic object") from exc
    # Native CanonicalSemanticObject may detach internal immutable tuples;
    # exact *canonical JSON* equality is the stable serialized ABI.
    if canonical_json(answer.as_dict()) != canonical_json(obj) or answer.ref != exact_ref(
        {"kind": answer.FAMILY, "object_id": obj["object_id"], "content_hash": obj["content_hash"]},
        "recreated original ref",
    ):
        raise S04ColdCustodyError("reconstructed original differs from exact semantic preimage")
    return answer


def freeze_s04_i03_sourcefree(
    *,
    query: EmpiricalQuerySpec,
    execution: QueryExecutionResult,
    knowledge: S04ObservedKnowledge,
) -> S04ColdBundle:
    """Seal the given exact I03 and S04 preimages; no source execution."""
    if (type(query) is not EmpiricalQuerySpec or type(execution) is not QueryExecutionResult
            or type(knowledge) is not S04ObservedKnowledge):
        raise S04ColdCustodyError("original I03 query/result and S04 knowledge required")
    independently_recomputed = receive_s04_i03_research(query=query, execution=execution)
    if independently_recomputed.ref != knowledge.ref:
        raise S04ColdCustodyError("S04 result does not match original I03 preimages")
    if len(execution.facts) != 1 or len(execution.release_refs) != 1:
        raise S04ColdCustodyError("cold sourcefree sidecar cannot contain pooled source")
    payload = {
        "contract": CONTRACT,
        "scope": "CALLER_DECLARED_SOURCEFREE_ONLY__NO_ORIGINAL_SOURCE_GRANT",
        "grade": CLAIM,
        "query_preimage": query.as_dict(),
        "fact_preimage": execution.facts[0].as_dict(),
        "execution": {
            "query_ref": execution.query_ref.as_dict(),
            "source_scope_mode": execution.source_scope_mode,
            "release_refs": [x.as_dict() for x in execution.release_refs],
        },
        "knowledge_payload_json": knowledge.payload_json,
        "knowledge_hash": knowledge.content_hash,
        "knowledge_ref": knowledge.ref.as_dict(),
        "external_source_root": "MUST_BE_SUPPLIED_SEPARATELY_AT_READ_TIME",
    }
    content = canonical_json(payload)
    return S04ColdBundle(content, semantic_hash(payload))


def read_s04_cold_preimages(
    bundle: S04ColdBundle,
    *,
    external_root: S04ExternalRootPin | None = None,
) -> S04ColdRead:
    """Rehydrate exact original query/fact and regenerate S04 WITHOUT I03.

    When external_root is absent, this is *inspection only*. A matching
    external pin checks identity but does not itself prove pin issuance.
    """
    if type(bundle) is not S04ColdBundle:
        raise S04ColdCustodyError("only exact cold-bundle type is readable")
    m = bundle.material()
    allowed = {
        "contract", "scope", "grade", "query_preimage", "fact_preimage",
        "execution", "knowledge_payload_json", "knowledge_hash", "knowledge_ref",
        "external_source_root",
    }
    if set(m) != allowed:
        raise S04ColdCustodyError("cold bundle fields do not match exact replay contract")
    if (m.get("scope") != "CALLER_DECLARED_SOURCEFREE_ONLY__NO_ORIGINAL_SOURCE_GRANT"
            or m.get("grade") != CLAIM
            or m.get("external_source_root") != "MUST_BE_SUPPLIED_SEPARATELY_AT_READ_TIME"):
        raise S04ColdCustodyError("sidecar scope or forbidden self-signed grant changed")
    query = _preimage(m["query_preimage"], EmpiricalQuerySpec)
    fact = _preimage(m["fact_preimage"], EmpiricalFact)
    envelope = m["execution"]
    if (type(envelope) is not dict or set(envelope) != {
        "query_ref", "source_scope_mode", "release_refs",
    } or type(envelope["release_refs"]) is not list
            or len(envelope["release_refs"]) != 1):
        raise S04ColdCustodyError("cold I03 envelope is invalid")
    try:
        execution = QueryExecutionResult(
            query_ref=exact_ref(envelope["query_ref"], "cold query"),
            facts=(fact,),
            source_scope_mode=envelope["source_scope_mode"],
            release_refs=tuple(exact_ref(x, "cold release") for x in envelope["release_refs"]),
        )
    except (TypeError, ValueError, AttributeError) as exc:
        raise S04ColdCustodyError("cold I03 execution envelope cannot be reconstructed") from exc
    regenerated = receive_s04_i03_research(query=query, execution=execution)
    if (regenerated.payload_json != m["knowledge_payload_json"]
            or regenerated.content_hash != m["knowledge_hash"]
            or regenerated.ref != exact_ref(m["knowledge_ref"], "cold S04 knowledge")):
        raise S04ColdCustodyError("replayed I03 source does not regenerate saved S04 knowledge")
    grade = "INSPECT_ONLY_UNPINNED__NO_FF01_COLD_ADMISSION"
    if external_root is not None:
        if type(external_root) is not S04ExternalRootPin:
            raise S04ColdCustodyError("independently supplied pin required; not a bundle-sourced dict")
        if (query.ref != external_root.query_ref
                or fact.ref != external_root.fact_ref
                or execution.release_refs[0] != external_root.release_ref):
            raise S04ColdCustodyError("EXTERNAL_ROOT_MISMATCH: cold source does not match pinned I03 custody")
        grade = "CALLER_SUPPLIED_EXACT_ROOTS_MATCH__ISSUER_AND_SOURCE_RIGHTS_UNVERIFIED"
    return S04ColdRead(
        query=query, execution=execution, knowledge=regenerated,
        integrity_grade=CLAIM, pin_grade=grade,
    )


def receive_ff01_from_pinned_cold(
    *,
    bundle: S04ColdBundle,
    external_root: S04ExternalRootPin,
    conditioner_index: int,
    producer_permission_ceiling: tuple[str, ...] = ("FF01_DESCRIPTIVE_SOURCEFREE",),
) -> Any:
    """Cold S04->original FF01 ABI; does not execute I03 or reopen C11.

    Source/custody actor must independently supply a trusted ORIGINAL fact
    root. No external pin, no FF01. This does not issue survey use rights.
    """
    from rawlsing_next.pre553_s04_ff01_consumer import receive_ff01_from_s04
    read = read_s04_cold_preimages(bundle, external_root=external_root)
    if not read.pin_grade.startswith("CALLER_SUPPLIED_EXACT_ROOTS_MATCH"):
        raise S04ColdCustodyError("cannot consume unpinned sourcefree cold product")
    return receive_ff01_from_s04(
        knowledge=read.knowledge, query=read.query, execution=read.execution,
        conditioner_index=conditioner_index,
        producer_permission_ceiling=producer_permission_ceiling,
    )


def write_s04_sourcefree_private(directory: str | Path, bundle: S04ColdBundle) -> Path:
    """Write private, content-addressed file by atomic hardlink without overwrite.

    A sensitive original-source/production C11 archive MUST NOT use this
    sourcefree sidecar or its caller-declared permissions.
    """
    if type(bundle) is not S04ColdBundle:
        raise S04ColdCustodyError("actual sourcefree bundle required")
    parent = Path(directory)
    if parent.is_symlink():
        raise S04ColdCustodyError("private sidecar directory cannot be a symlink")
    parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not parent.is_dir() or parent.is_symlink() or S_IMODE(parent.stat().st_mode) & 0o077:
        raise S04ColdCustodyError("private sidecar directory must exclude group/world access")
    final = parent / (bundle.digest + FILE_SUFFIX)
    if final.is_symlink():
        raise S04ColdCustodyError("existing cold sidecar path cannot be a symlink")
    raw = bundle.payload_json.encode("utf-8")
    temp = parent / ("." + bundle.digest + "." + token_hex(12) + ".tmp")
    fd = None
    try:
        fd = os_open(str(temp), O_WRONLY | O_CREAT | O_EXCL, 0o600)
        with fdopen(fd, "wb") as writer:
            fd = None
            writer.write(raw)
            writer.flush()
            fsync(writer.fileno())
        try:
            link(str(temp), str(final))
        except FileExistsError:
            if read_s04_sourcefree_private(final).payload_json != bundle.payload_json:
                raise S04ColdCustodyError("existing content-addressed name differs from preimage")
    finally:
        if fd is not None:
            from os import close
            close(fd)
        temp.unlink(missing_ok=True)
    return final


def read_s04_sourcefree_private(path: str | Path) -> S04ColdBundle:
    """Read bounded exact sidecar; refuse symlinks/nonregular/renamed digest."""
    import os
    import stat
    p = Path(path)
    if p.is_symlink():
        raise S04ColdCustodyError("symbolic link is not a trusted sidecar")
    try:
        flags = O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        fd = os_open(str(p), flags)
        with fdopen(fd, "rb") as reader:
            info = os.fstat(reader.fileno())
            if not S_ISREG(info.st_mode) or not 0 < info.st_size <= MAX_BYTES:
                raise S04ColdCustodyError("not a regular bounded cold sourcefree sidecar")
            raw = reader.read(MAX_BYTES + 1)
    except (OSError, ValueError) as exc:
        raise S04ColdCustodyError("sourcefree sidecar cannot be opened safely") from exc
    if len(raw) > MAX_BYTES:
        raise S04ColdCustodyError("cold sidecar exceeded byte budget")
    try:
        source = raw.decode("utf-8")
        material = loads(source)
    except (UnicodeError, ValueError) as exc:
        raise S04ColdCustodyError("invalid UTF8 or JSON in sourcefree sidecar") from exc
    bundle = S04ColdBundle(source, semantic_hash(material))
    if p.name != bundle.digest + FILE_SUFFIX:
        raise S04ColdCustodyError("content-addressed path does not match preimage")
    return bundle


__all__ = [
    "CONTRACT", "S04ColdCustodyError", "S04ColdBundle", "S04ExternalRootPin",
    "S04ColdRead", "freeze_s04_i03_sourcefree", "read_s04_cold_preimages",
    "receive_ff01_from_pinned_cold", "write_s04_sourcefree_private",
    "read_s04_sourcefree_private",
]
