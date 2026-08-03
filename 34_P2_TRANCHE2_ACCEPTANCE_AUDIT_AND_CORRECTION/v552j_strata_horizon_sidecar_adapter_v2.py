#!/usr/bin/env python3
"""Read-only V552→V552J strata/horizon sidecar adapter v2.1.

Not installed into the live pipeline. It performs cardinality-checked,
blank-key-safe pass-through and preserves packet row identity.
"""
from __future__ import annotations
import json
from typing import Any
import pandas as pd
from pandas.api.types import is_scalar

FIELDS = ['stratum_id', 'stratum_label', 'strata_relevance', 'strata_path', 'conditional_strata_weights', 'horizon_affordance', 'horizon_type', 'horizon_scope', 'horizon_openness', 'horizon_reach', 'horizon_valence', 'horizon_sustaining_power']
KEY_PREFERENCES = [('question_implementation_id',), ('source','wave','question_id'), ('source','wave','source_variable_code')]
STATUS_COLUMN = 'strata_horizon_sidecar_status'
KEY_COLUMN = 'strata_horizon_sidecar_join_key'
_HELPER_PREFIX = '__rawlsing_sidecar_join_'


def _is_missing(v: Any) -> bool:
    if v is None:
        return True
    if not is_scalar(v):
        return False
    try:
        return bool(pd.isna(v))
    except Exception:
        return False


def _clean(v: Any) -> str:
    if _is_missing(v):
        return ''
    if isinstance(v, (dict, list, tuple)):
        return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return str(v).strip()


def _canonical(v: Any) -> str:
    if _is_missing(v):
        return ''
    if isinstance(v, (dict, list, tuple, bool, int, float)):
        return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    s = str(v).strip()
    if not s:
        return ''
    try:
        obj = json.loads(s)
    except Exception:
        return s
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def _complete_mask(df: pd.DataFrame, keys: list[str]) -> pd.Series:
    mask = pd.Series(True, index=df.index, dtype=bool)
    for k in keys:
        mask &= df[k].map(_clean).ne('')
    return mask


def select_join_key(packet: pd.DataFrame, sidecar: pd.DataFrame) -> list[str]:
    candidates = []
    for pref in KEY_PREFERENCES:
        keys = list(pref)
        if not all(k in packet.columns and k in sidecar.columns for k in keys):
            continue
        side_complete = _complete_mask(sidecar, keys)
        packet_complete = _complete_mask(packet, keys)
        candidates.append({'keys': keys, 'sidecar_complete': int(side_complete.sum()), 'sidecar_rows': len(sidecar), 'packet_complete': int(packet_complete.sum())})
        if side_complete.all() and packet_complete.any():
            return keys
    raise ValueError('no safe supported join key: ' + repr(candidates))


def validate_sidecar_schema(sidecar: pd.DataFrame) -> None:
    missing = [f for f in FIELDS if f not in sidecar.columns]
    if missing:
        raise ValueError('missing required sidecar fields: ' + repr(missing))


def enrich_with_report(packet: pd.DataFrame, sidecar: pd.DataFrame):
    validate_sidecar_schema(sidecar)
    keys = select_join_key(packet, sidecar)
    p = packet.copy()
    s = sidecar.copy()
    reserved = [c for c in list(p.columns) + list(s.columns) if c.startswith(_HELPER_PREFIX)]
    if reserved:
        raise ValueError('reserved internal join columns already exist: ' + repr(sorted(set(reserved))))

    p['__packet_row_order__'] = range(len(p))
    helper_keys = []
    for i, key in enumerate(keys):
        helper = f'{_HELPER_PREFIX}{i}__'
        helper_keys.append(helper)
        p[helper] = p[key].map(_clean)
        s[helper] = s[key].map(_clean)

    packet_complete = _complete_mask(p, helper_keys)
    side_complete = _complete_mask(s, helper_keys)
    if not side_complete.all():
        raise ValueError('selected sidecar join key contains blank components')
    dup = s.duplicated(helper_keys, keep=False)
    if dup.any():
        sample_cols = keys + helper_keys
        raise ValueError('duplicate sidecar join keys after canonical trimming: ' + repr(s.loc[dup, sample_cols].to_dict('records')[:10]))

    # Never expose blank packet keys to the merge; they remain explicit unmatched rows.
    mergeable = p.loc[packet_complete].copy()
    missing_key = p.loc[~packet_complete].copy()
    side_field_columns = {f: f + '__sidecar' for f in FIELDS}
    side_merge = s[helper_keys + FIELDS].rename(columns=side_field_columns)
    out = mergeable.merge(side_merge, how='left', on=helper_keys, validate='many_to_one', indicator='__sidecar_merge__')
    matched = out['__sidecar_merge__'].eq('both')

    # Status reflects whether the authoritative sidecar itself supplied any value,
    # not whether the packet happened to carry a pre-existing value.
    sidecar_nonempty = pd.Series(False, index=out.index, dtype=bool)
    for sf in side_field_columns.values():
        sidecar_nonempty |= out[sf].map(_clean).ne('')

    for f in FIELDS:
        sf = side_field_columns[f]
        if f not in packet.columns:
            out[f] = out[sf]
        else:
            left = out[f].map(_canonical)
            right = out[sf].map(_canonical)
            conflict = left.ne('') & right.ne('') & left.ne(right)
            if conflict.any():
                sample = out.loc[conflict, keys + [f, sf]].head(10).to_dict('records')
                raise ValueError(f'conflicting non-empty values for {f}: {sample!r}')
            out[f] = out[f].where(left.ne(''), out[sf])
        out.drop(columns=[sf], inplace=True)

    out[STATUS_COLUMN] = 'NO_V552_SIDECAR_MATCH'
    out.loc[matched & sidecar_nonempty, STATUS_COLUMN] = 'V552_AUTHORITATIVE_PASS_THROUGH_MATCHED'
    out.loc[matched & ~sidecar_nonempty, STATUS_COLUMN] = 'V552_SIDECAR_MATCHED_NO_AUTHORITATIVE_VALUES'
    out[KEY_COLUMN] = '|'.join(keys)
    out.drop(columns=['__sidecar_merge__'], inplace=True)

    # Missing-key packet rows receive no sidecar values and cannot collide with blank sidecar keys.
    for f in FIELDS:
        if f not in missing_key.columns:
            missing_key[f] = pd.NA
    missing_key[STATUS_COLUMN] = 'PACKET_JOIN_KEY_MISSING'
    missing_key[KEY_COLUMN] = '|'.join(keys)

    combined = pd.concat([out, missing_key], ignore_index=True, sort=False).sort_values('__packet_row_order__', kind='stable')
    combined.drop(columns=['__packet_row_order__'] + helper_keys, inplace=True)
    combined.reset_index(drop=True, inplace=True)
    if len(combined) != len(packet):
        raise AssertionError('packet row count changed')

    side_keys = {tuple(row[k] for k in helper_keys) for _, row in s.iterrows()}
    packet_keys = {tuple(row[k] for k in helper_keys) for _, row in p.loc[packet_complete].iterrows()}
    report = {
        'join_keys': keys,
        'key_normalization': 'TRIMMED_STRING_OR_CANONICAL_STRUCTURED_VALUE',
        'packet_rows': len(packet),
        'packet_complete_key_rows': int(packet_complete.sum()),
        'packet_missing_key_rows': int((~packet_complete).sum()),
        'sidecar_rows': len(sidecar),
        'matched_packet_rows': int(combined[STATUS_COLUMN].isin(['V552_AUTHORITATIVE_PASS_THROUGH_MATCHED', 'V552_SIDECAR_MATCHED_NO_AUTHORITATIVE_VALUES']).sum()),
        'unmatched_complete_packet_rows': int(combined[STATUS_COLUMN].eq('NO_V552_SIDECAR_MATCH').sum()),
        'orphan_sidecar_keys': len(side_keys - packet_keys),
        'status_counts': combined[STATUS_COLUMN].value_counts(dropna=False).to_dict(),
    }
    return combined, report


def enrich(packet: pd.DataFrame, sidecar: pd.DataFrame) -> pd.DataFrame:
    return enrich_with_report(packet, sidecar)[0]
