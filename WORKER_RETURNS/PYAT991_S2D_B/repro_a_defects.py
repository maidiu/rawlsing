"""A-cut RED vs B-cut GREEN for the S2-D corrective findings.

A's original adapter is loaded from the immutable startup commit via `git show`;
it is not edited.  B's repaired adapter is imported from the working tree.
Synthetic sourcefree fixtures only.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
TMP = Path("/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T")

import rawlsing_next.tests.test_pre553_direct_estate_i03 as s2c
import rawlsing_next.tests.test_pre553_empirical_query as native
from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor,
    RuntimeObjectCatalog,
)
from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec, exact_ref
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission as BAdmission,
    SavedC11AdmissionError as BAdmissionError,
)
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
from rawlsing_next.tests.test_pyat991_s2d_saved_admission import (
    _i03_parts,
    _i05_parts,
    _source_with_candidate,
)


def load_a_module():
    source = subprocess.check_output(
        ["git", "-C", str(ROOT), "show",
         "e399c48d576f5b2ae501dac569fb729e95bd968e:"
         "rawlsing_next/pre553_saved_c11_admission.py"],
        text=True,
    )
    path = Path(tempfile.mkdtemp(prefix="s2d-a-orig-", dir=TMP)) / "a_saved_c11_admission.py"
    path.write_text(source, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("a_saved_c11_admission_orig", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _combine(*catalogs):
    return RuntimeObjectCatalog(
        authorities=tuple(sorted({
            obj.authority_ref.key: obj
            for catalog in catalogs for obj in catalog.authorities
        }.values(), key=lambda obj: obj.authority_ref.key)),
        predicates=tuple(sorted({
            obj.ref.key: obj
            for catalog in catalogs for obj in catalog.predicates
        }.values(), key=lambda obj: obj.ref.key)),
        queries=tuple(sorted({
            obj.ref.key: obj
            for catalog in catalogs for obj in catalog.queries
        }.values(), key=lambda obj: obj.ref.key)),
        discovery_authorities=tuple(sorted({
            obj.ref.key: obj
            for catalog in catalogs for obj in catalog.discovery_authorities
        }.values(), key=lambda obj: obj.ref.key)),
    )


class MonkeyPatch:
    def __init__(self):
        self._undo = []
    def context(self):
        from contextlib import contextmanager
        @contextmanager
        def _ctx():
            yield self
        return _ctx()
    def setattr(self, obj, name, value):
        old = getattr(obj, name)
        self._undo.append((obj, name, old))
        setattr(obj, name, value)
    def undo(self):
        for obj, name, old in reversed(self._undo):
            setattr(obj, name, old)


def main():
    a_mod = load_a_module()
    patch = MonkeyPatch()
    try:
        base_source, base_candidate = _source_with_candidate(
            patch, "S2D-B-RED",
            [{"id": "R1", "responses": {"X": 1, "Y": 1}},
             {"id": "R2", "responses": {"X": 0, "Y": 0}}],
        )
        foreign_source, _ = _source_with_candidate(
            patch, "S2D-B-RED-FOREIGN",
            [{"id": "Q1", "responses": {"X": 1, "Y": 0}},
             {"id": "Q2", "responses": {"X": 0, "Y": 1}}],
        )
        changed_source, changed_candidate = _source_with_candidate(
            patch, "S2D-B-RED",
            [{"id": "R1", "responses": {"X": 1, "Y": 1}},
             {"id": "R2", "responses": {"X": 0, "Y": 1}}],
        )
        tmp = Path(tempfile.mkdtemp(prefix="s2d-b-red-", dir=TMP))
        qa, pred, query, base_catalog = _i03_parts(base_source, "S2D-B-RED")
        _, _, _, foreign_catalog = _i03_parts(
            foreign_source, "S2D-B-RED-FOREIGN"
        )
        root, receipt = s2c._cold(
            tmp, base_candidate, base_source["universe"].ref, "base"
        )
        changed_root, changed_receipt = s2c._cold(
            tmp, changed_candidate, changed_source["universe"].ref, "changed"
        )

        # Mixed-scope query: estate empirical universe plus a foreign scope.
        fields = dict(query.semantic_fields)
        fields["scope_refs"] = tuple(sorted({
            *(exact_ref(dict(v)) for v in fields["scope_refs"]),
            foreign_source["universe"].ref,
        }, key=lambda ref: ref.key))
        mixed_scope_query = EmpiricalQuerySpec(
            typed_state=query.typed_state,
            authority_snapshot_refs=query.authority_snapshot_refs,
            dependency_refs=query.dependency_refs,
            producer_replay_locator_or_reference_root=query.producer_replay_locator_or_reference_root,
            **fields,
        )
        mixed_catalog = _combine(
            base_catalog,
            foreign_catalog,
            RuntimeObjectCatalog(
                authorities=base_catalog.authorities,
                predicates=(pred,),
                queries=(query, mixed_scope_query),
                discovery_authorities=(),
            ),
        )
        native_state = native._run(
            base_source, qa, pred, mixed_scope_query
        ).facts[0].typed_state

        a_estate = VerifiedDirectEstate(
            root, exact_path=receipt.path,
            independently_held_manifest_sha256=receipt.manifest_sha256,
            independently_held_i02=receipt.i02,
            current_authorizer=lambda _roots: True,
        )
        a_adm = a_mod.SavedC11Admission(
            estate=a_estate, release_ref=base_source["release_ref"],
            runtime_catalog=mixed_catalog,
        )
        a_mixed = a_adm.execute_i03(
            query_ref=mixed_scope_query.ref, predicate_ref=pred.ref
        )
        b_adm = BAdmission(
            estate=VerifiedDirectEstate(
                root, exact_path=receipt.path,
                independently_held_manifest_sha256=receipt.manifest_sha256,
                independently_held_i02=receipt.i02,
                current_authorizer=lambda _roots: True,
            ),
            release_ref=base_source["release_ref"],
            runtime_catalog=mixed_catalog,
        )
        b_mixed_refused = None
        try:
            b_adm.execute_i03(
                query_ref=mixed_scope_query.ref, predicate_ref=pred.ref
            )
            b_mixed_refused = False
        except BAdmissionError as exc:
            b_mixed_refused = str(exc)

        # Mutable admission: A accepts a post-construction retarget; B refuses.
        a_mutable_estate = VerifiedDirectEstate(
            changed_root, exact_path=changed_receipt.path,
            independently_held_manifest_sha256=changed_receipt.manifest_sha256,
            independently_held_i02=changed_receipt.i02,
            current_authorizer=lambda _roots: True,
        )
        a_adm2 = a_mod.SavedC11Admission(
            estate=VerifiedDirectEstate(
                root, exact_path=receipt.path,
                independently_held_manifest_sha256=receipt.manifest_sha256,
                independently_held_i02=receipt.i02,
                current_authorizer=lambda _roots: True,
            ),
            release_ref=base_source["release_ref"],
            runtime_catalog=base_catalog,
        )
        base_fact = a_adm2.execute_i03(
            query_ref=query.ref, predicate_ref=pred.ref
        ).facts[0].ref
        a_adm2.estate = a_mutable_estate
        a_adm2.release_ref = changed_source["release_ref"]
        a_adm2._executor = CarrierNeutralResearchExecutor(
            repository=a_mutable_estate,
            release_refs=(changed_source["release_ref"],),
            runtime_catalog=base_catalog,
        )
        a_changed_fact = a_adm2.execute_i03(
            query_ref=query.ref, predicate_ref=pred.ref
        ).facts[0].ref
        b_adm2 = BAdmission(
            estate=VerifiedDirectEstate(
                root, exact_path=receipt.path,
                independently_held_manifest_sha256=receipt.manifest_sha256,
                independently_held_i02=receipt.i02,
                current_authorizer=lambda _roots: True,
            ),
            release_ref=base_source["release_ref"],
            runtime_catalog=base_catalog,
        )
        try:
            b_adm2.release_ref = changed_source["release_ref"]
            b_mutation_refused = False
        except BAdmissionError as exc:
            b_mutation_refused = str(exc)
        b_base_fact = b_adm2.execute_i03(
            query_ref=query.ref, predicate_ref=pred.ref
        ).facts[0].ref

        # I05 mixed universe: A returns a typed negative; B hard-refuses.
        qa5, dauth, all_p, x1, yq, auth, base_i05 = _i05_parts(
            base_source, "S2D-B-RED-I05"
        )
        _, _, _, _, _, foreign_auth, foreign_i05 = _i05_parts(
            foreign_source, "S2D-B-RED-FOREIGN-I05"
        )
        combined5 = _combine(base_i05, foreign_i05)
        a_adm5 = a_mod.SavedC11Admission(
            estate=VerifiedDirectEstate(
                root, exact_path=receipt.path,
                independently_held_manifest_sha256=receipt.manifest_sha256,
                independently_held_i02=receipt.i02,
                current_authorizer=lambda _roots: True,
            ),
            release_ref=base_source["release_ref"],
            runtime_catalog=combined5,
        )
        a_i05 = a_adm5.execute_i05(discovery_authority_ref=foreign_auth.ref)
        b_adm5 = BAdmission(
            estate=VerifiedDirectEstate(
                root, exact_path=receipt.path,
                independently_held_manifest_sha256=receipt.manifest_sha256,
                independently_held_i02=receipt.i02,
                current_authorizer=lambda _roots: True,
            ),
            release_ref=base_source["release_ref"],
            runtime_catalog=combined5,
        )
        try:
            b_adm5.execute_i05(discovery_authority_ref=foreign_auth.ref)
            b_i05_refused = False
        except BAdmissionError as exc:
            b_i05_refused = str(exc)
        b_i05_base = b_adm5.execute_i05(
            discovery_authority_ref=auth.ref
        )

        out = {
            "schema": "PYAT991_S2D_B_RED_GREEN@1",
            "a_code_cut": "e399c48d576f5b2ae501dac569fb729e95bd968e",
            "mixed_scope_i03": {
                "native_oracle_state": native_state,
                "a_state": a_mixed.facts[0].typed_state,
                "a_accepted": a_mixed.facts[0].typed_state == "SUPPORTED",
                "b_refused": b_mixed_refused,
            },
            "mutable_admission_i03": {
                "a_base_fact": base_fact.content_hash,
                "a_retargeted_fact": a_changed_fact.content_hash,
                "a_accepted_retarget": a_changed_fact != base_fact,
                "b_refused": b_mutation_refused,
                "b_restored_fact": b_base_fact.content_hash,
            },
            "mixed_universe_i05": {
                "a_candidate_count": a_i05.candidate_count,
                "a_covered_count": a_i05.covered_candidate_count,
                "a_receipt_states": [r.typed_state for r in a_i05.receipts],
                "a_fact_states": [f.typed_state for f in a_i05.empirical_facts],
                "b_refused": b_i05_refused,
                "b_base_receipts": [r.ref.as_dict() for r in b_i05_base.receipts],
            },
        }
        out_path = Path(__file__).with_name("a_red_b_green.json")
        out_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(out, indent=2, sort_keys=True))
    finally:
        patch.undo()


if __name__ == "__main__":
    main()
