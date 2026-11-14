from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_source_direct_parquet_estate import write_direct_estate

from fixture_1006 import ShapeSpec, build_context
from query_1006 import build_query_bundle, execute_bundle_oracle

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
scratch = HERE / ".local-data" / "representative"
shutil.rmtree(scratch, ignore_errors=True)
scratch.mkdir(parents=True, mode=0o700)
shape = ShapeSpec("representative", 64, include_weights=True, tag="PYAT1006-REPRESENTATIVE")
ctx = build_context(shape)
bundle = build_query_bundle(ctx)
receipt = write_direct_estate(ctx.direct_sections(), ctx.universe.ref, scratch, chunk_rows=16)
target = HERE / "evidence" / "representative-estate"
if target.exists():
    shutil.rmtree(target)
target.mkdir(mode=0o700)
release_name = Path(receipt.path).name
release_target = target / "releases" / release_name
release_target.parent.mkdir(mode=0o700)
shutil.copytree(Path(receipt.path), release_target)
for path in [target, target / "releases", release_target]:
    path.chmod(0o700)
for path in release_target.iterdir():
    path.chmod(0o600)
relative_exact_path = f"releases/{release_name}"
native_repo, native_release = ctx.native_oracle()
oracle = execute_bundle_oracle(
    native_repo, native_release, bundle,
    qa=bundle.catalog.authorities[-2], dauth=bundle.catalog.authorities[-1],
)
admission = SavedC11Admission.open(
    root=target, exact_path=target / relative_exact_path,
    independently_held_manifest_sha256=receipt.manifest_sha256,
    independently_held_i02=receipt.i02,
    release_ref=receipt.reconstructed_v1_release_ref,
    runtime_catalog=bundle.catalog, current_authorizer=lambda _r: True,
)
saved = {}
for name in ("selected", "f2_forward", "f2_reverse", "f4_three", "f4_four", "weighted", "repeated"):
    query, predicate = bundle.by_name(name)
    result = admission.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    saved[name] = {
        "query_ref": query.ref.as_dict(),
        "predicate_ref": predicate.ref.as_dict(),
        "fact_refs": [fact.ref.as_dict() for fact in result.facts],
        "fact_states": [fact.typed_state for fact in result.facts],
        "denominators": [fact.raw_denominator_support for fact in result.facts],
        "equal_native_oracle": (
            tuple(fact.ref for fact in result.facts)
            == tuple(fact.ref for fact in oracle[name].facts)
        ),
    }
i05 = admission.execute_i05(discovery_authority_ref=bundle.discovery_authority.ref)
i05_receipt = {
    "discovery_authority_ref": bundle.discovery_authority.ref.as_dict(),
    "candidate_count": i05.candidate_count,
    "covered_candidate_count": i05.covered_candidate_count,
    "fact_refs": [fact.ref.as_dict() for fact in i05.empirical_facts],
    "receipt_refs": [row.ref.as_dict() for row in i05.receipts],
    "equal_native_oracle": (
        tuple(row.ref for row in i05.receipts)
        == tuple(row.ref for row in oracle["i05"].receipts)
    ),
}
checksums = {
    path.name: hashlib.sha256(path.read_bytes()).hexdigest()
    for path in sorted(release_target.iterdir())
}
document = {
    "schema": "PYAT1006_REPRESENTATIVE_RECEIPT@1",
    "fixture": "sourcefree synthetic 64 respondents, weights, A/B/C/D/MR, typed missing B, routed D/MR",
    "root": "evidence/representative-estate",
    "exact_path": relative_exact_path,
    "manifest_sha256": receipt.manifest_sha256,
    "i02": {
        "logical": receipt.i02.logical,
        "physical": receipt.i02.physical,
        "release": receipt.i02.release,
        "source": receipt.i02.source,
        "replay": receipt.i02.replay,
        "universe": receipt.i02.universe,
        "schema": receipt.i02.schema,
    },
    "reconstructed_v1_release_ref": receipt.reconstructed_v1_release_ref.as_dict(),
    "family_counts": dict(receipt.family_counts),
    "members_sha256": checksums,
    "queries": saved,
    "i05": i05_receipt,
    "native_oracle_release": native_release.as_dict(),
    "permission_grade": "SOURCEFREE_TEST_ONLY",
}
(HERE / "evidence" / "representative_receipt.json").write_text(
    json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({
    "target": str(target),
    "manifest_sha256": receipt.manifest_sha256,
    "release": receipt.reconstructed_v1_release_ref.as_dict(),
    "saved_queries_equal": {k: v["equal_native_oracle"] for k, v in saved.items()},
    "i05_equal": i05_receipt["equal_native_oracle"],
    "bytes": sum(path.stat().st_size for path in release_target.iterdir()),
}, indent=2, sort_keys=True))
