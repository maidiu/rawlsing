"""Real retained original LiTS objects -> native catalog, bounded before I03."""
import json
from pathlib import Path
import sys
import subprocess

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))
import retained_catalog
from rawlsing_next.pre553_carrier_execution import materialize_public_object, CarrierExecutionBindingError
from rawlsing_next.pre553_empirical_authority import Pre553AuthorityConflict
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_batch_runner import BatchUnitSpec, BatchManifest, BatchExecutionRunner, BatchIntegrityError


def frozen_refs(family):
    freeze = json.loads((HERE / 'evidence/RETAINED_NATIVE_CATALOG_FREEZE.json').read_text())
    return {tuple(sorted(r.items())) for r in freeze['expected_refs'] if r['kind'] == family + '@1.0.0'}


def test_retained_original_query_consumer_preimages_no_drop():
    objects = retained_catalog.materialize_retained_objects()
    actual = {tuple(sorted(o.ref.as_dict().items())) for o in objects if o.schema_id == 'EmpiricalQuerySpec'}
    expected = frozen_refs('EmpiricalQuerySpec')
    assert expected - actual == set()
    assert actual - expected == set()
    assert len(actual) == 63


def test_retained_native_predicate_and_snapshot_preimages():
    objects = retained_catalog.materialize_retained_objects()
    actual_predicates = {tuple(sorted(o.ref.as_dict().items())) for o in objects if o.schema_id == 'EmpiricalPredicate'}
    actual_authorities = {tuple(sorted(o.ref.as_dict().items())) for o in objects if o.schema_id == 'AuthoritySnapshot'}
    assert actual_predicates == frozen_refs('EmpiricalPredicate')
    assert frozen_refs('AuthoritySnapshot') <= actual_authorities
    assert len(actual_authorities) == 24
    assert len(actual_predicates) == 35
    assert len(objects) == 122


def test_full_retained_catalog_rejects_conflicting_snapshot_envelopes():
    with pytest.raises(Pre553AuthorityConflict, match='duplicate exact authority ref has conflicting snapshots'):
        retained_catalog.build_retained_catalog()


def test_original_scoped_catalog_consumer_no_drop():
    catalog = retained_catalog.build_original_scoped_catalog()
    actual = {tuple(sorted(r.as_dict().items())) for r in catalog.query_refs}
    expected = frozen_refs('EmpiricalQuerySpec')
    assert expected - actual == set()
    assert actual - expected == set()
    projection = json.loads((HERE / 'evidence/RETAINED_SCOPED_CATALOG_FREEZE.json').read_text())
    independent_ref = dict(sorted(expected)[0])
    assert catalog.resolve_query_exact(independent_ref).content_hash == independent_ref['content_hash']
    expected_authorities = {tuple(sorted(r.items())) for r in projection['independently_predetermined_authority_public_refs']}
    assert {tuple(sorted(a.ref.as_dict().items())) for a in catalog.authorities} == expected_authorities
    assert {tuple(sorted(r.as_dict().items())) for r in catalog.predicate_refs} == frozen_refs('EmpiricalPredicate')
    assert len(catalog.authorities) == 13


def test_deferred_original_fact_is_not_an_exact_native_fact():
    partial = json.loads((HERE / 'evidence/retained_DEFERRED_fact_negative_only.json').read_text())
    assert '$deferred_retained_member' in partial['preimage']['dependency_refs']
    with pytest.raises(CarrierExecutionBindingError, match='preimage'):
        materialize_public_object(partial['preimage'])


def test_original_query_reaches_batch_but_exact_release_is_missing():
    catalog = retained_catalog.build_original_scoped_catalog()
    freeze = json.loads((HERE / 'evidence/RETAINED_NATIVE_CATALOG_FREEZE.json').read_text())
    source = freeze['independent_expected_source']
    oracle = json.loads(subprocess.check_output(['git', 'show', source['commit'] + ':' + source['path']], cwd=HERE.parents[1]))
    release = ExactRef(**oracle['projection_and_release_refs']['release_refs'][0])
    unit = BatchUnitSpec(job_kind='QUERY', job_ref=catalog.query_refs[0], release_refs=(release,))
    manifest = BatchManifest(units=(unit,))
    with pytest.raises(BatchIntegrityError, match='exact C11 release unavailable'):
        BatchExecutionRunner(manifest=manifest, repository=C11Repository())
