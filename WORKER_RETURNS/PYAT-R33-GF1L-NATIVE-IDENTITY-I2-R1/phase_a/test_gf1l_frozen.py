"""Independent GF1L falsifiers. Freeze remotely before inspecting GF1K repair.
Full native GF1G fixture required; never a synthetic adapter.
"""
from copy import deepcopy
import importlib.util
import os
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location('gf1l_native_fixture', os.environ['GF1J_GF1G_TEST'])
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def fields():
    f = deepcopy(h._template().__dict__)
    f.pop('content_hash'); f.pop('object_id')
    return f


def make(f):
    digest = h.G.semantic_hash(h.G._projection(f))
    return h.G.GenericNativePairRelation(**f, content_hash=digest,
        object_id='urn:rawlsing:gf1:generic-pair-relation:sha256:' + digest)


def refused(f):
    # Native construction may reject a malformed projection before consumption.
    try:
        rel = make(f)
    except h.G.GenericNativePairError:
        return
    got = h.CONS(rel)
    assert got['decision_state'] == 'CONSUMER_RELATION_INTEGRITY_REJECTED', got
    assert got['separation_class'] is None and got['downstream_value_produced'] is False


@pytest.mark.parametrize('role', ['condition', 'target'])
@pytest.mark.parametrize('alias', [0, False, 0.0])
def test_native_string_zero_never_aliases(role, alias):
    f = fields()
    if role == 'condition':
        assert type(f['conditioner_domain'][0]) is str
        f['conditional_count_profile'][0]['condition_state'] = alias
    else:
        assert type(f['target_domain'][0]) is str
        f['conditional_count_profile'][0]['target_counts'][0]['target_state'] = alias
    refused(f)


@pytest.mark.parametrize('role', ['condition', 'target'])
def test_integer_domain_bool_alias_is_not_equal(role):
    f = fields()
    domain = 'conditioner_domain' if role == 'condition' else 'target_domain'
    f[domain] = (0, 1)
    for row in f['conditional_count_profile']:
        if role == 'condition':
            row['condition_state'] = int(row['condition_state'])
        else:
            for cell in row['target_counts']:
                cell['target_state'] = int(cell['target_state'])
    if role == 'condition':
        f['conditional_count_profile'][0]['condition_state'] = False
    else:
        f['conditional_count_profile'][0]['target_counts'][0]['target_state'] = False
    refused(f)


@pytest.mark.parametrize('role', ['condition', 'target'])
def test_duplicate_or_foreign_native_category(role):
    for state in ('foreign', '1'):
        f = fields()
        if role == 'condition':
            f['conditional_count_profile'][0]['condition_state'] = state
        else:
            f['conditional_count_profile'][0]['target_counts'][0]['target_state'] = state
        refused(f)


@pytest.mark.parametrize('order', ['native', 'reverse_both'])
def test_legitimate_source_native_positive_and_order(order):
    f = fields()
    if order == 'reverse_both':
        f['conditioner_domain'] = tuple(reversed(f['conditioner_domain']))
        f['target_domain'] = tuple(reversed(f['target_domain']))
        rows = list(reversed(f['conditional_count_profile']))
        for row in rows:
            row['target_counts'] = tuple(reversed(row['target_counts']))
        f['conditional_count_profile'] = tuple(rows)
    r = make(f)
    for c, row in zip(r.conditioner_domain, r.conditional_count_profile):
        assert type(c) is type(row['condition_state']) and c == row['condition_state']
        for t, cell in zip(r.target_domain, row['target_counts']):
            assert type(t) is type(cell['target_state']) and t == cell['target_state']
    got = h.CONS(r)
    assert got['separation_class'] == 'EXACT_PAIR_SEPARATION', got
    assert got['joint_support_total'] == 2
    assert got['production_owner_commit'] is False


def test_original_full_native_import_required():
    assert h.GB.REATTESTED == 74
    assert Path(h.G.__file__).resolve().is_relative_to(h.RT.resolve())
    h.GB.reattest()


def test_semantic_projection_retains_native_python_identity():
    for role in ('condition', 'target'):
        f = fields()
        original = h.G.semantic_hash(h.G._projection(f))
        if role == 'condition':
            f['conditional_count_profile'][0]['condition_state'] = 0
        else:
            f['conditional_count_profile'][0]['target_counts'][0]['target_state'] = 0
        assert h.G.semantic_hash(h.G._projection(f)) != original
        refused(f)
