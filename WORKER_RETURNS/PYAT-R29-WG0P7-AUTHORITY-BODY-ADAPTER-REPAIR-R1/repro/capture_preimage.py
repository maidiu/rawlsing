"""WG0P7 — capture the full authority-snapshot preimage and the three negatives.

Reads the repaired candidate module, builds the three genuine releases, and
records the complete constructed authority body that the repair now binds into
the owner-registered release material.  Also folds in the executed A2/A3/A4
outcomes from observations/frozen14_execution.json (never regenerated or
relabelled here).
"""
import hashlib
import json
import pathlib
import sys

RET = pathlib.Path(__file__).resolve().parents[1]
CAND = RET / "candidate" / "court" / "runtime_phase_b" / "p5_return" / "review" / "runtime_phase_b" / "candidate"
sys.path[:0] = [str(CAND / "repro"), str(CAND / "pinned")]

import wg0p4_workload as w  # noqa: E402


def _body(a):
    return dict(ref=a.authority_ref.as_dict(),
                constructed_content_hash=a.content_hash,
                semantic_projection=a.semantic_projection())


releases = w.build_all_releases()
authority_bodies = {}
for tag, rel in releases.items():
    authority_bodies[tag] = {
        "qauth": _body(rel.qauth),
        "authorities": [_body(a) for a in rel.authorities],
        "material_authority_bodies": w._release_material(rel)["authority_bodies"],
        "qauth_operations": list(rel.qauth.governed_operations),
    }

module = pathlib.Path(w.__file__).resolve()
data = module.read_bytes()
frozen14 = json.loads((RET / "observations" / "frozen14_execution.json").read_text())
by_case = {c["case"]: c for c in frozen14["cases"]}

record = dict(
    schema="WG0P7_FULL_AUTHORITY_SNAPSHOT_PREIMAGE_AND_THREE_NEGATIVES@1",
    candidate_module=str(module),
    candidate_module_sha256=hashlib.sha256(data).hexdigest(),
    candidate_module_git_blob_sha1=hashlib.sha1(
        b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
    version=w.VERSION,
    binding_contract=(
        "Each release's owner-registered material now carries, for every "
        "(*rel.authorities, rel.qauth): the claimed authority_ref triple, the "
        "CONSTRUCTED AuthoritySnapshot.content_hash (constructed semantic body), and "
        "the full semantic projection. The digest of that material is registered by "
        "the fixture owner at ingestion and rechecked at compile, every I03 boundary, "
        "consumer publication and cold restore."),
    authority_bodies=authority_bodies,
    three_negatives={k: by_case[k] for k in
                     ("A2_stale_issuer_epoch_same_identity",
                      "A3_same_hash_foreign_signed_body",
                      "A4_foreign_governed_operations_same_hash")},
    three_positives={k: by_case[k] for k in
                     ("P1_unmodified_owner_serves",
                      "P2_own_authority_identity_rebind_serves",
                      "P3_replay_identical_consumer")},
)
(RET / "01_FULL_AUTHORITY_SNAPSHOT_PREIMAGE_AND_THREE_NEGATIVES.json").write_text(
    json.dumps(record, indent=1, sort_keys=True, default=str) + "\n")
print("authority preimage recorded for", list(authority_bodies))
for k in ("A2_stale_issuer_epoch_same_identity", "A3_same_hash_foreign_signed_body",
          "A4_foreign_governed_operations_same_hash"):
    c = by_case[k]
    print(" ", k, "->", c.get("exception_type"), c.get("typed_refusal"),
          "served", c.get("served_supported_original_fact"), "i03", c.get("new_I03_calls"))
