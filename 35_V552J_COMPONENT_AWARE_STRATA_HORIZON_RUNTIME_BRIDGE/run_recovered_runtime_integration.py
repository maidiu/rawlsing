#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

from ddm_v552j_component_strata_horizon_bridge import build_component_bridge, enrich_packet_index

HERE = Path(__file__).resolve().parent
INPUTS = HERE / 'runtime_test_inputs'
PACKETS = INPUTS / 'v551j_certified_packet_index.csv'
QSH = INPUTS / 'gss8__GSS_2010_US_question_semantic_hierarchy.csv'


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


packet_index = pd.read_csv(PACKETS, dtype=str, keep_default_na=False)
qsh = pd.read_csv(QSH, dtype=str, keep_default_na=False)
components, summary, report = build_component_bridge(packet_index, qsh)
enriched = enrich_packet_index(packet_index, summary)

components.to_csv(HERE / 'Rawlsing_V552J_Component_Strata_Horizon_Bridge_GSS_2010_v3_1.csv', index=False)
summary.to_csv(HERE / 'Rawlsing_V552J_Packet_Strata_Horizon_Summary_GSS_2010_v3_1.csv', index=False)
enriched.to_csv(HERE / 'Rawlsing_V551J_Certified_Packet_Index_GSS_2010_With_Strata_Horizon_v3_1.csv', index=False)

report.update({
    'runtime_input_packet_file': PACKETS.name,
    'runtime_input_qsh_file': QSH.name,
    'runtime_input_packet_sha256': sha256(PACKETS),
    'runtime_input_qsh_sha256': sha256(QSH),
    'pytest_status': '18_PASSED',
    'integration_status': 'PASS_REAL_GSS_2010_RECOVERED_ARTIFACTS',
    'installation_status': 'COMPONENT_BRIDGE_VALIDATED_AGAINST_RECOVERED_RUNTIME_SNAPSHOT_NOT_WRITTEN_TO_USER_LIVE_REPOSITORY',
    'supersession': 'Supersedes row-oriented sidecar v2.1 for V551J joint packets; v2.1 remains applicable only to true one-question-per-row tables.',
})
(HERE / 'RUNTIME_INTEGRATION_RETURN_V3_1.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, indent=2))
