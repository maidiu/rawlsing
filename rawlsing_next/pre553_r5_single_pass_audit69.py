"""Additive Authority-69 serial single-pass full audit."""
from __future__ import annotations

import gzip
import hashlib

from rawlsing_next import pre553_r5_compact_carrier as frozen


def single_pass_full_audit(reader, *, logical_wire=frozen._logical_wire):
    """Recompute the complete audit with one logical-wire serialization per row."""
    reader._require()
    global_digest = hashlib.sha256()
    rows = 0
    previous = None
    global_relations = {}

    for descriptor in reader.iter_inventory():
        path = reader.release_directory / "members" / descriptor["member"]
        member_digest = hashlib.sha256()
        member_rows = 0
        member_first = member_last = None
        member_relations = {}
        with reader._verified_spool(
            path, descriptor["sha256"], descriptor["byte_length"]
        ) as spool:
            try:
                gz = gzip.GzipFile(mode="rb", fileobj=spool)
                for line in gz:
                    row = frozen._decode_storage(line)
                    identity = row.identity_key
                    if previous is not None and identity <= previous:
                        reader._fail("single-pass audit found duplicate/noncanonical row order")
                    previous = identity
                    if member_first is None:
                        member_first = identity
                    member_last = identity
                    wire = logical_wire(row)
                    member_digest.update(wire)
                    global_digest.update(wire)
                    member_rows += 1
                    rows += 1
                    member_relations[row.relation] = member_relations.get(row.relation, 0) + 1
                    global_relations[row.relation] = global_relations.get(row.relation, 0) + 1
                gz.close()
            except frozen.R5IntegrityError:
                raise
            except Exception as exc:
                reader._fail(
                    f"single-pass compressed member decode failed {descriptor['member']}",
                    exc,
                )

        if (
            member_rows != descriptor["row_count"]
            or member_digest.hexdigest() != descriptor["logical_digest"]
        ):
            reader._fail(f"single-pass logical member digest/count mismatch {descriptor['member']}")
        if (
            list(member_first) != descriptor["first_identity"]
            or list(member_last) != descriptor["last_identity"]
            or dict(sorted(member_relations.items())) != descriptor["relation_counts"]
        ):
            reader._fail(f"single-pass member coverage descriptor mismatch {descriptor['member']}")

    if (
        rows != reader.root["canonical_row_count"]
        or global_digest.hexdigest() != reader.root["logical_stream_digest"]
    ):
        reader._fail("single-pass audit semantic stream digest/count mismatch")
    return {
        "physical_root_id": reader.root["physical_root_id"],
        "canonical_rows": rows,
        "logical_stream_digest": global_digest.hexdigest(),
        "relation_counts": dict(sorted(global_relations.items())),
    }


__all__ = ["single_pass_full_audit"]
