"""Exact sourcefree deserialization of retained LiTS catalog preimages.

No respondent decoding, query generation, authority issuance, I03 rerun or
Fact reconstruction. Deferred Fact members are never synthesized.
"""
import gzip
import json
from pathlib import Path

from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog, materialize_public_object

HERE = Path(__file__).resolve().parent


def retained_documents():
    return json.loads(gzip.decompress((HERE / 'evidence/retained_native_catalog_preimages.json.gz').read_bytes()))


def materialize_retained_objects():
    documents = sorted(retained_documents(), key=lambda d: d['content_hash'])
    return tuple(materialize_public_object(d) for d in documents)


def build_retained_catalog():
    """Preserved full-packet diagnostic: expected to reject authority collisions.

    Individually valid retained snapshots are not necessarily one valid registry.
    No envelope is selected or replaced here.
    """
    documents = retained_documents()
    authorities = [d for d in documents if d['schema_id'] == 'AuthoritySnapshot']
    predicates = [d for d in documents if d['schema_id'] == 'EmpiricalPredicate']
    query_documents = sorted([d for d in documents if d['schema_id'] == 'EmpiricalQuerySpec'], key=lambda d: d['content_hash'])
    return RuntimeObjectCatalog.from_documents(
        authority_documents=authorities,
        predicate_documents=predicates,
        query_documents=query_documents,
    )


def build_original_scoped_catalog():
    """Use exact original public snapshot pins, never flatten the whole archive.

    Extra query/predicate authority keys must have exactly one retained snapshot.
    This is sourcefree packet binding, not a new source/operation use grant.
    """
    documents = retained_documents()
    frozen = json.loads((HERE / 'evidence/RETAINED_NATIVE_CATALOG_FREEZE.json').read_text())
    original = {r['content_hash'] for r in frozen['expected_refs'] if r['kind'] == 'AuthoritySnapshot@1.0.0'}
    all_authorities = [d for d in documents if d['schema_id'] == 'AuthoritySnapshot']
    authorities = [d for d in all_authorities if d['content_hash'] in original]
    if {d['content_hash'] for d in authorities} != original:
        raise ValueError('original exact public snapshot preimage missing')
    def key(fields):
        return tuple(fields[n] for n in ('authority_id', 'authority_version', 'authority_content_hash'))
    bound = {key(d['semantic_fields']) for d in authorities}
    predicates = [d for d in documents if d['schema_id'] == 'EmpiricalPredicate']
    queries = sorted([d for d in documents if d['schema_id'] == 'EmpiricalQuerySpec'], key=lambda d: d['content_hash'])
    required = {key(ref) for d in [*predicates, *queries] for ref in d['authority_snapshot_refs']}
    for missing in sorted(required - bound):
        candidates = [d for d in all_authorities if key(d['semantic_fields']) == missing]
        if len(candidates) != 1:
            raise ValueError('required authority triple has absent or ambiguous retained envelope')
        authorities.append(candidates[0])
    return RuntimeObjectCatalog.from_documents(
        authority_documents=authorities, predicate_documents=predicates,
        query_documents=queries,
    )
