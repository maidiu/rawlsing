from __future__ import annotations

import base64
import json
import lzma
from pathlib import Path

from rawlsing_next.n04_r3_carrier_specific_production_binding import build, sha256


def test_n04_r3_transient_export_only():
    accounting, _vector, vector_b64, frontier, summary = build()
    out = Path('.rabochii/n04r3_export')
    out.mkdir(parents=True, exist_ok=True)

    canonical = b''.join(
        (json.dumps(row, sort_keys=True, separators=(',', ':')) + '\n').encode()
        for row in accounting
    )
    assert len(canonical) == summary['accounting_canonical_jsonl_bytes']
    assert sha256(canonical) == summary['accounting_canonical_jsonl_sha256']

    packed = lzma.compress(canonical, format=lzma.FORMAT_XZ, preset=9 | lzma.PRESET_EXTREME)
    packed_b64 = base64.b64encode(packed)
    (out / '06_CURRENT_18276_BINDING_ACCOUNTING.jsonl.xz.b64').write_bytes(packed_b64 + b'\n')
    (out / '03_CURRENT_18276_BINDING_STATUS_VECTOR.zlib.b64').write_bytes(vector_b64 + b'\n')

    ids = [item['question_implementation_id'] for item in frontier]
    stream = ('\n'.join(ids) + '\n').encode()
    frontier_payload = {
        'schema': 'RAWLSING_N04_R3_CANDIDATE_KIND_FRONTIER@1.0.0',
        'count': len(frontier),
        'sorted_id_stream_sha256': sha256(stream),
        'records': frontier,
    }
    (out / '04_CANDIDATE_KIND_FRONTIER_42.json').write_text(
        json.dumps(frontier_payload, sort_keys=True, indent=2) + '\n', encoding='utf-8'
    )

    receipt = {
        'schema': 'RAWLSING_N04_R3_VALIDATION_RECEIPT@1.0.0',
        'terminal': 'PASS',
        'terminal_code': 'N04_R3_CARRIER_SPECIFIC_PRODUCTION_BINDING_AND_T03_RERELEASE_COMPLETE__RETURN_TO_HQ',
        'result': summary['terminal'],
        'rows': summary['rows'],
        'positive_t03_candidates': summary['positive_t03_candidates'],
        'accounting_canonical_jsonl_bytes': len(canonical),
        'accounting_canonical_jsonl_sha256': sha256(canonical),
        'accounting_xz_bytes': len(packed),
        'accounting_xz_sha256': sha256(packed),
        'accounting_xz_b64_bytes': len(packed_b64),
        'accounting_xz_b64_sha256': sha256(packed_b64),
        'status_vector_zlib_b64_sha256': summary['status_vector_zlib_b64_sha256'],
        'candidate_kind_frontier_sorted_id_stream_sha256': summary['candidate_kind_frontier_sorted_id_stream_sha256'],
        'compression': 'base64(xz(lzma FORMAT_XZ preset=9|PRESET_EXTREME)) over canonical JSONL',
    }
    (out / '05_VALIDATION_RECEIPT.json').write_text(
        json.dumps(receipt, sort_keys=True, indent=2) + '\n', encoding='utf-8'
    )
    (out / '07_SUMMARY.json').write_text(
        json.dumps(summary, sort_keys=True, indent=2) + '\n', encoding='utf-8'
    )
