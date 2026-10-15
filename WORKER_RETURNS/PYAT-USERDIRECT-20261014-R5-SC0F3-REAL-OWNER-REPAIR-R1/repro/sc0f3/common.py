import dataclasses
import hashlib
import json
from collections.abc import Mapping
from port.contracts import PortContractError


class Hold(PortContractError):
    pass


def material(x):
    if x is None or isinstance(x, (str, int, float, bool)):
        return x
    if isinstance(x, Mapping):
        return {str(k): material(v) for k, v in sorted(x.items(), key=lambda kv: str(kv[0]))}
    if isinstance(x, (tuple, list)):
        return [material(v) for v in x]
    if isinstance(x, (set, frozenset)):
        return sorted((material(v) for v in x), key=lambda v: json.dumps(v, sort_keys=True))
    for method in ('material', 'as_dict'):
        if callable(getattr(x, method, None)):
            return material(getattr(x, method)())
    if hasattr(x, 'release_refs') and hasattr(x, '_objects'):
        return {'type': type(x).__name__, 'release_refs': material(x.release_refs),
                'objects': {k: material(v) for k, v in sorted(x._objects.items())}}
    if hasattr(x, '_by_key'):
        return {'type': type(x).__name__, 'snapshots': material(x._by_key)}
    if dataclasses.is_dataclass(x):
        return {f.name: material(getattr(x, f.name)) for f in dataclasses.fields(x)
                if not f.name.startswith('_')}
    if type(x).__name__ == 'ConditionValueBindingWitness':
        return material(vars(x))
    raise TypeError('No auditable material for '+type(x).__name__)


def digest(x):
    return hashlib.sha256(json.dumps(material(x), sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def require(condition, code, detail):
    if not condition:
        raise Hold(code, detail)


PHYSICAL_FIELDS = frozenset(('physical_provider_id', 'physical_storage_locator',
                             'physical_serialization', 'physical_lineage_blob', 'nonsemantic_cache_ids'))


def semantic_selection(selection):
    # Only the five frozen physical provenance fields are excluded. All other
    # fields, including unknown future semantic extensions, participate.
    result = material(selection)
    result['provider'] = {k: v for k, v in result['provider'].items() if k not in PHYSICAL_FIELDS}
    return result
