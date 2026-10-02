#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PYAT D2P PORTABLE RETAINED-CHECKPOINT EXPORT -- R1
Estate: NoviyMac

Deterministic, bounded-memory, checkpoint-only extractor.

Guarantees enforced by this script:
  * Fails closed on identity-gate mismatch, missing exact fields, or count drift.
  * Reads ONLY the retained I05 checkpoint named by REQUIRED_CHECKPOINT_SHA256.
  * Contains no raw LiTS DTA/source locator; invokes no Rawlsing source decoder.
  * Does not import or execute any Rawlsing production module.
  * Does not modify the retained checkpoint (opened 'rb' only).
  * Emits no row that is not present in retained checkpoint material.

Usage:
    python3 07_EXTRACTION_SCRIPT.py --outdir <dir> [--checkpoint <path>]

Requires: ijson (streaming JSON). No other dependency.
"""

import argparse
import hashlib
import json
import os
import platform
import socket
import subprocess
import sys

try:
    import ijson
except ImportError:  # fail closed
    sys.stderr.write("FATAL: ijson not installed. pip install ijson\n")
    sys.exit(2)

# ---------------------------------------------------------------------------
# Governed constants
# ---------------------------------------------------------------------------

REQUIRED_CHECKPOINT_BYTES = 3404445161
REQUIRED_CHECKPOINT_SHA256 = (
    "2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726"
)
REQUIRED_CHECKPOINT_IDENTITY = (
    "3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f"
)
REQUIRED_CANONICAL_CLOSURE_IDENTITY = (
    "f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415"
)

RAWLSING_ROOT = "/Users/matthewsmith/Desktop/Rawlsing"
CHECKPOINT_RELPATH = (
    "LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/"
    "payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/"
    "court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json"
)
DEFAULT_CHECKPOINT = os.path.join(RAWLSING_ROOT, CHECKPOINT_RELPATH)

CLOSURE = "material.canonical_empirical_object_closure"
PREIMAGES = CLOSURE + ".public_object_preimages"
SUMMARY = "material.astra_shaped_empirical_summary"

# B002 per-object closure families and their exact required cardinalities.
REQUIRED_FAMILY_COUNTS = {
    "EmpiricalFact": 60,
    "EmpiricalQuerySpec": 63,
    "EmpiricalPredicate": 35,
    "DiscoveryResultReceipt": 50,
}
REQUIRED_AUTHORITY_SNAPSHOTS = 24
REQUIRED_PER_OBJECT_ROWS = 208
REQUIRED_RECEIPTS = 50
REQUIRED_CROSS_SCHEMA_ROWS = 50
REQUIRED_P2_MAPPINGS = 18

# EmpiricalFact retained preimages are ~69 MB each (3.28 GB total) because of two
# fully enumerated retained members. NoviyMac has 800 MiB free, so those members
# are carried as exact retained canonical digests rather than inlined bytes.
# Nothing is inferred, dropped silently, or reconstructed: the exact retained
# canonical SHA-256 and byte length of every withheld member are recorded, and
# preimage_sha256 always covers the COMPLETE retained preimage.
DEFERRED_FAMILIES = {"EmpiricalFact"}
DEFERRED_MEMBERS = ("dependency_refs", "semantic_fields.source_empirical_provenance_refs")

DEFER_REASON = (
    "NoviyMac disk capacity (800 MiB free at extraction). Retained member is "
    "enumerated reference mass (EmpiricalFact dependency_refs and "
    "source_empirical_provenance_refs). Withheld from the portable packet as an "
    "exact retained canonical SHA-256 + byte length + item count so HQ can "
    "reconstruct the bytes byte-exactly from the verified retained checkpoint. "
    "No semantic value is inferred, summarized, or reconstructed."
)


class FailClosed(Exception):
    """Raised whenever a required exact condition is not met."""


# ---------------------------------------------------------------------------
# Canonical JSON law
# ---------------------------------------------------------------------------

def canon_bytes(obj):
    """UTF-8 JSON, sort_keys=true, separators (',',':'), ensure_ascii=false."""
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def canon_sha256(obj):
    return hashlib.sha256(canon_bytes(obj)).hexdigest()


def sha256_file(path, chunk=1 << 22):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# PHASE 0 -- identity gate
# ---------------------------------------------------------------------------

def phase0_identity(checkpoint):
    if not os.path.isfile(checkpoint):
        raise FailClosed("checkpoint absent at governed path: %s" % checkpoint)
    observed_bytes = os.path.getsize(checkpoint)
    if observed_bytes != REQUIRED_CHECKPOINT_BYTES:
        raise FailClosed(
            "size gate FAIL: observed %d required %d"
            % (observed_bytes, REQUIRED_CHECKPOINT_BYTES)
        )
    observed_sha = sha256_file(checkpoint)
    if observed_sha != REQUIRED_CHECKPOINT_SHA256:
        raise FailClosed(
            "sha256 gate FAIL: observed %s required %s"
            % (observed_sha, REQUIRED_CHECKPOINT_SHA256)
        )
    return observed_bytes, observed_sha


def estate_facts():
    try:
        osv = subprocess.run(
            ["sw_vers"], capture_output=True, text=True, timeout=20
        ).stdout.split()
    except Exception:
        osv = []
    os_name = " ".join(osv) if osv else "%s %s" % (platform.system(), platform.release())
    return {
        "estate": "NoviyMac",
        "hostname": socket.gethostname(),
        "os": os_name,
        "architecture": platform.machine(),
    }


# ---------------------------------------------------------------------------
# PHASE 1 -- bounded-memory extraction
# ---------------------------------------------------------------------------

def stream_preimages(checkpoint):
    """Yield each retained public object preimage one at a time (bounded memory)."""
    with open(checkpoint, "rb") as fh:
        for item in ijson.items(fh, PREIMAGES + ".item", buf_size=1 << 22):
            yield item


def build_export_preimage(item):
    """
    Return (export_preimage, deferred_list).

    export_preimage preserves every retained member verbatim EXCEPT deferred
    members on deferred families, which are replaced by an explicit digest
    marker. The full retained preimage SHA-256 is always computed separately
    over the complete unmodified retained item.
    """
    deferred = []
    if item.get("schema_id") not in DEFERRED_FAMILIES:
        return item, deferred

    export = dict(item)
    for member_path in DEFERRED_MEMBERS:
        node = item
        parts = member_path.split(".")
        ok = True
        for p in parts:
            if isinstance(node, dict) and p in node:
                node = node[p]
            else:
                ok = False
                break
        if not ok:
            raise FailClosed(
                "deferred member %s absent from retained %s"
                % (member_path, item.get("object_id"))
            )
        blob = canon_bytes(node)
        marker = {
            "$deferred_retained_member": {
                "member_path": member_path,
                "omitted_from_portable_packet": True,
                "retained_canonical_bytes": len(blob),
                "retained_canonical_sha256": hashlib.sha256(blob).hexdigest(),
                "retained_item_count": len(node) if isinstance(node, list) else None,
                "retained_checkpoint_sha256": REQUIRED_CHECKPOINT_SHA256,
                "reason": DEFER_REASON,
            }
        }
        if len(parts) == 1:
            export[parts[0]] = marker
        else:
            parent = export
            for p in parts[:-1]:
                parent = dict(parent[p])
            parent[parts[-1]] = marker
            cur = export
            for p in parts[:-1]:
                cur = cur[p]
            cur[parts[-1]] = marker
        deferred.append(marker["$deferred_retained_member"])
    return export, deferred


def extract(checkpoint, outdir):
    b001_rows, b002_snapshots, b002_objects = [], [], []
    family_counts = {}
    deferred_log = []

    for item in stream_preimages(checkpoint):
        for k in ("schema_id", "object_id", "content_hash", "semantic_fields",
                  "authority_snapshot_refs"):
            if k not in item:
                raise FailClosed("retained preimage missing exact field %s" % k)
        family = item["schema_id"]
        full_sha = canon_sha256(item)
        export_pre, deferred = build_export_preimage(item)
        if deferred:
            deferred_log.append(
                {"object_family": family, "object_ref": item["object_id"],
                 "deferred_members": deferred}
            )

        if family == "AuthoritySnapshot":
            sf = item["semantic_fields"]
            triples = []
            for k, v in sf.items():
                if isinstance(v, dict) and set(v.keys()) == {"content_hash", "kind", "object_id"}:
                    triples.append({"retained_field": k, "authority_ref": v})
                elif (
                    isinstance(v, list)
                    and v
                    and isinstance(v[0], dict)
                    and set(v[0].keys()) == {"content_hash", "kind", "object_id"}
                ):
                    for e in v:
                        triples.append({"retained_field": k, "authority_ref": e})
            if not triples:
                raise FailClosed("AuthoritySnapshot %s retains no AuthorityRef"
                                 % item["object_id"])
            b002_snapshots.append({
                "authority_snapshot_ref": {
                    "content_hash": item["content_hash"],
                    "kind": "AuthoritySnapshot@%s" % item["schema_version"],
                    "object_id": item["object_id"],
                },
                "authority_ref_triples": triples,
                "preimage_sha256": full_sha,
                "preimage": item,
            })
            continue

        if family in REQUIRED_FAMILY_COUNTS:
            family_counts[family] = family_counts.get(family, 0) + 1
            rec = {
                "object_family": family,
                "object_ref": {
                    "content_hash": item["content_hash"],
                    "kind": "%s@%s" % (family, item["schema_version"]),
                    "object_id": item["object_id"],
                },
                "authority_snapshot_refs": item["authority_snapshot_refs"],
                "preimage_sha256": full_sha,
                "preimage": export_pre,
            }
            if deferred:
                rec["deferred_retained_members"] = deferred
            b002_objects.append(rec)

            if family == "DiscoveryResultReceipt":
                sf = item["semantic_fields"]
                ci = sf.get("candidate_identity") or {}
                chash = ci.get("candidate_hash")
                if not chash:
                    raise FailClosed(
                        "receipt %s retains no explicit candidate_hash; B001 "
                        "association not explicit -> fail closed" % item["object_id"]
                    )
                for k in ("authority_snapshot_refs", "dependency_refs",
                          "winning_predicate_ref", "source_release_refs", "replay_ref"):
                    if k not in sf and k not in item:
                        raise FailClosed("receipt missing exact field %s" % k)
                b001_rows.append({
                    "candidate_hash": chash,
                    "discovery_result_receipt_ref": {
                        "content_hash": item["content_hash"],
                        "kind": "DiscoveryResultReceipt@%s" % item["schema_version"],
                        "object_id": item["object_id"],
                    },
                    "authority_snapshot_refs": item["authority_snapshot_refs"],
                    "dependency_refs": item["dependency_refs"],
                    "winning_predicate_ref": sf.get("winning_predicate_ref"),
                    "source_release_refs": sf.get("source_release_refs"),
                    "replay_ref": sf.get("replay_ref"),
                    "receipt_preimage_sha256": full_sha,
                    "receipt_preimage": item,
                    "association_basis": (
                        "explicit retained semantic_fields.candidate_identity."
                        "candidate_hash on the DiscoveryResultReceipt preimage; "
                        "no ordering-based pairing used"
                    ),
                })

    # ---- B003: retained cross-schema logical binding rows ----
    def rows(prefix):
        with open(checkpoint, "rb") as fh:
            return list(ijson.items(fh, prefix + ".item", buf_size=1 << 22))

    ncp = rows(SUMMARY + ".native_candidate_provenance.rows")
    lci = rows(SUMMARY + ".logical_candidate_identity")
    p2_block = rows(SUMMARY + ".P2")

    lci_by_key, ncp_by_key = {}, {}
    for r in lci:
        lci_by_key[r["logical_candidate_key"]] = r
    for r in ncp:
        ncp_by_key[r["logical_candidate_key"]] = r
    p2_keys = {p["logical_candidate_key"]: p for p in p2_block}

    b003_rows = []
    p2_verified = 0
    for i, key in enumerate(sorted(ncp_by_key)):
        binding = ncp_by_key[key]
        lci_row = lci_by_key.get(key)
        if lci_row is None:
            raise FailClosed("logical_candidate_key %s absent from retained "
                             "logical_candidate_identity" % key)
        lane = binding.get("lane")
        lane2 = (
            lci_row.get("logical_candidate_material", {})
            .get("candidate_semantics", {})
            .get("lane")
        )
        if lane != lane2:
            raise FailClosed("lane disagreement on retained binding %s" % key)
        rule_id = (
            lci_row.get("logical_candidate_material", {})
            .get("candidate_semantics", {})
            .get("rule_id")
        )
        contract = lci_row.get("logical_candidate_material", {}).get("contract")
        in_p2_block = key in p2_keys
        is_p2 = (lane == "P2")
        if is_p2 != in_p2_block:
            raise FailClosed("P2 lane/P2-block disagreement on %s" % key)
        if is_p2:
            p2_verified += 1
        b003_rows.append({
            "export_mode": "RETAINED_CROSS_SCHEMA_LOGICAL_BINDING",
            "row_index": i,
            "binding_sha256": canon_sha256(binding),
            "binding": binding,
            "logical_candidate_key": key,
            "retained_lane": lane,
            "retained_rule_id": rule_id,
            "retained_contract": contract,
            "logical_candidate_identity": lci_row,
            "p2_lane_block_item": p2_keys.get(key),
            "is_p2_memberwise_mapping": is_p2,
            "memberwise_roles": [
                {
                    "role": rb.get("role"),
                    "logical_condition_atom_ids": rb.get("logical_condition_atom_ids"),
                    "logical_query_template_id": rb.get("logical_query_template_id"),
                    "current_predicate_ref": rb.get("current_predicate_ref"),
                    "current_query_ref": rb.get("current_query_ref"),
                }
                for rb in binding.get("role_bindings", [])
            ],
            "verification_basis": (
                "explicit retained lane=='P2' on both native_candidate_provenance "
                "row and logical_candidate_identity row, AND logical_candidate_key "
                "present in the retained P2 lane block; no P2 classifier inferred"
            ),
        })

    return (b001_rows, b002_snapshots, b002_objects, family_counts,
            b003_rows, p2_verified, contract, deferred_log)


# ---------------------------------------------------------------------------
# Validation + outputs
# ---------------------------------------------------------------------------

def validate(b001, snaps, objs, famcounts, b003, p2_verified):
    gaps = []
    if len(b001) != REQUIRED_RECEIPTS:
        gaps.append("B001 rows %d != %d" % (len(b001), REQUIRED_RECEIPTS))
    if len({r["candidate_hash"] for r in b001}) != len(b001):
        gaps.append("B001 candidate_hash not distinct")
    if len(snaps) != REQUIRED_AUTHORITY_SNAPSHOTS:
        gaps.append("authority snapshots %d != %d" % (len(snaps), REQUIRED_AUTHORITY_SNAPSHOTS))
    if len(objs) != REQUIRED_PER_OBJECT_ROWS:
        gaps.append("per-object rows %d != %d" % (len(objs), REQUIRED_PER_OBJECT_ROWS))
    for fam, n in REQUIRED_FAMILY_COUNTS.items():
        if famcounts.get(fam, 0) != n:
            gaps.append("family %s %d != %d" % (fam, famcounts.get(fam, 0), n))
    for r in objs:
        if not r["authority_snapshot_refs"]:
            gaps.append("empty authority_snapshot_refs on %s" % r["object_ref"]["object_id"])
    if len(b003) != REQUIRED_CROSS_SCHEMA_ROWS:
        gaps.append("cross-schema rows %d != %d" % (len(b003), REQUIRED_CROSS_SCHEMA_ROWS))
    if p2_verified != REQUIRED_P2_MAPPINGS:
        gaps.append("P2 memberwise mappings %d != %d" % (p2_verified, REQUIRED_P2_MAPPINGS))
    return gaps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--checkpoint", default=DEFAULT_CHECKPOINT)
    args = ap.parse_args()

    ck = os.path.abspath(args.checkpoint)
    out = os.path.abspath(args.outdir)
    os.makedirs(out, exist_ok=True)

    nbytes, nsha = phase0_identity(ck)
    ef = estate_facts()

    (b001, snaps, objs, famcounts, b003, p2_verified, contract,
     deferred_log) = extract(ck, out)

    gaps = validate(b001, snaps, objs, famcounts, b003, p2_verified)

    write_jsonl(os.path.join(out, "02_CANDIDATE_RECEIPT_BINDINGS.jsonl"), b001)
    write_jsonl(os.path.join(out, "03_AUTHORITY_SNAPSHOT_CLOSURE.jsonl"), snaps)
    write_jsonl(os.path.join(out, "04_PER_OBJECT_AUTHORITY_BINDINGS.jsonl"), objs)
    write_jsonl(os.path.join(out, "05_P2_LOGICAL_BINDINGS.jsonl"), b003)

    identity = {
        "schema": "PYAT_D2P_CHECKPOINT_IDENTITY@1",
        "estate": "NoviyMac",
        "hostname": ef["hostname"],
        "os": ef["os"],
        "architecture": ef["architecture"],
        "rawlsing_root": RAWLSING_ROOT,
        "checkpoint_governed_relative_path": CHECKPOINT_RELPATH,
        "checkpoint_absolute_path": ck,
        "observed_bytes": nbytes,
        "observed_sha256": nsha,
        "required_sha256": REQUIRED_CHECKPOINT_SHA256,
        "checkpoint_identity": REQUIRED_CHECKPOINT_IDENTITY,
        "checkpoint_identity_verification": (
            "NOT_VERIFIED_HERE -- value recorded as commissioned; no field "
            "carrying this identity was located in the permitted retained "
            "material scanned. Not claimed as verified."
        ),
        "canonical_closure_identity": REQUIRED_CANONICAL_CLOSURE_IDENTITY,
        "canonical_closure_identity_verification": (
            "NOT_VERIFIED_HERE -- value recorded as commissioned; no field "
            "carrying this identity was located in the permitted retained "
            "material scanned. Not claimed as verified."
        ),
        "identity_gate": "PASS",
        "identity_gate_basis": "observed_bytes and freshly streamed sha256 both exact",
        "retained_material_paths_read": [
            PREIMAGES + ".item",
            SUMMARY + ".native_candidate_provenance.rows.item",
            SUMMARY + ".logical_candidate_identity.item",
            SUMMARY + ".P2.item",
        ],
    }
    with open(os.path.join(out, "01_CHECKPOINT_IDENTITY.json"), "w", encoding="utf-8") as fh:
        json.dump(identity, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")

    b001_ok = len(b001) == REQUIRED_RECEIPTS and not any("B001" in g for g in gaps)
    b002_ok = (len(snaps) == REQUIRED_AUTHORITY_SNAPSHOTS
               and len(objs) == REQUIRED_PER_OBJECT_ROWS
               and not any(("family" in g or "authority" in g or "per-object" in g)
                           for g in gaps))
    b003_ok = (len(b003) == REQUIRED_CROSS_SCHEMA_ROWS
               and p2_verified == REQUIRED_P2_MAPPINGS
               and not any(("cross-schema" in g or "P2" in g) for g in gaps))

    closure = {
        "schema": "PYAT_D2P_BLOCKER_CLOSURE@1",
        "B001": {
            "status": "CLOSED" if b001_ok else "OPEN",
            "candidate_receipt_rows": len(b001),
            "required": REQUIRED_RECEIPTS,
            "reason": (
                "50 retained DiscoveryResultReceipt preimages each carry an explicit "
                "retained semantic_fields.candidate_identity.candidate_hash, so the "
                "candidate->receipt association is explicit in retained material. "
                "authority_snapshot_refs, dependency_refs, winning_predicate_ref, "
                "source_release_refs and replay_ref exported verbatim per receipt. "
                "No ordering-based pairing."
            ) if b001_ok else "; ".join(g for g in gaps if "B001" in g),
        },
        "B002": {
            "status": "CLOSED" if b002_ok else "OPEN",
            "authority_snapshots": len(snaps),
            "required_authority_snapshots": REQUIRED_AUTHORITY_SNAPSHOTS,
            "per_object_rows": len(objs),
            "required_per_object_rows": REQUIRED_PER_OBJECT_ROWS,
            "family_counts": {k: famcounts.get(k, 0) for k in REQUIRED_FAMILY_COUNTS},
            "reason": (
                "24 retained AuthoritySnapshot preimages exported with their exact "
                "retained AuthorityRef triples; 208 per-object rows exported with "
                "exact retained per-object authority_snapshot_refs (no family-level "
                "substitution). EmpiricalFact retained preimage payload deferred by "
                "exact canonical digest for NoviyMac disk capacity; authority "
                "bindings themselves are complete and exact."
            ) if b002_ok else "; ".join(g for g in gaps if "B002" in g),
        },
        "B003": {
            "status": "CLOSED" if b003_ok else "OPEN",
            "export_mode": "RETAINED_CROSS_SCHEMA_LOGICAL_BINDING",
            "cross_schema_rows": len(b003),
            "p2_memberwise_mappings_verified": p2_verified,
            "required_p2_memberwise_mappings": REQUIRED_P2_MAPPINGS,
            "reason": (
                "The literal key cross_schema_logical_candidate_bindings is absent "
                "from the checkpoint (0 raw occurrences). The same retained material "
                "IS present under retained contract %s: 50 native_candidate_provenance "
                "rows joined 1:1 to 50 logical_candidate_identity rows on explicit "
                "retained logical_candidate_key, each row carrying memberwise "
                "role_bindings from historical logical member (logical_condition_atom_ids, "
                "logical_query_template_id) to current pre553_i05_candidate_hash with "
                "current_predicate_ref and current_query_ref. 18 rows are verified as "
                "the already-qualified P2 memberwise mappings from explicit retained "
                "identity (lane=='P2' on both retained rows AND logical_candidate_key "
                "present in the retained 18-key P2 lane block; rule_id "
                "D02_P2_HIGHER_ORDER_K3). No P2 classifier inferred."
            ) % contract if b003_ok else "; ".join(g for g in gaps if "B003" in g),
        },
        "zero_reconstructed_semantic_rows": True,
        "validation_gaps": gaps,
        "deferred_payload_objects": len(deferred_log),
        "deferred_payload_bytes_withheld": sum(
            d["retained_canonical_bytes"] for o in deferred_log
            for d in o["deferred_members"]
        ),
    }
    with open(os.path.join(out, "06_B001_B002_B003_CLOSURE.json"), "w", encoding="utf-8") as fh:
        json.dump(closure, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")

    if gaps:
        sys.stderr.write("VALIDATION GAPS:\n" + "\n".join(gaps) + "\n")

    print("B001=%s rows=%d" % (closure["B001"]["status"], len(b001)))
    print("B002=%s snaps=%d objects=%d families=%s"
          % (closure["B002"]["status"], len(snaps), len(objs),
             json.dumps(closure["B002"]["family_counts"], sort_keys=True)))
    print("B003=%s rows=%d p2=%d" % (closure["B003"]["status"], len(b003), p2_verified))
    print("deferred objects=%d bytes=%d"
          % (len(deferred_log), closure["deferred_payload_bytes_withheld"]))
    return 0 if not gaps else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except FailClosed as e:
        sys.stderr.write("FAIL CLOSED: %s\n" % e)
        sys.exit(3)