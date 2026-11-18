"""Review-only recomputation of ANVIL R2 aligned positive phases."""
from __future__ import annotations
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent / 'snapshot' / 'R2_PILOT'
def load(n): return json.loads((BASE/n).read_text())
b = load('baseline.json'); p = load('prepared.json'); r = load('FIRST_PAIR_RESULT.json')
neg = p['negative'] or {}
positive = {
 'baseline_wall_seconds': b['wall_seconds'],
 'prepared_total_wall_seconds': p['wall_seconds'],
 'prepared_negative_wall_seconds': neg.get('wall_seconds'),
 'prepared_aligned_positive_wall_seconds': p['wall_seconds'] - (neg.get('wall_seconds') or 0),
 'baseline_S_index_seconds': b['index_build_seconds'],
 'prepared_total_S_index_seconds': p['index_build_seconds'],
 'prepared_negative_S_index_seconds': neg.get('index_build_seconds'),
 'prepared_aligned_positive_S_index_seconds': p['index_build_seconds'] - (neg.get('index_build_seconds') or 0),
 'baseline_Q_seconds': b['evaluator_seconds_measured_operations'],
 'prepared_Q_seconds': p['evaluator_seconds_measured_operations'],
 'prepared_negative_Q_seconds': neg.get('evaluator_seconds'),
 'baseline_O_serialize_seconds': sum(row.get('serialize_seconds',0) for row in b['rows']),
 'prepared_O_serialize_seconds': sum(row.get('serialize_seconds',0) for row in p['rows']),
 'baseline_H_admission_seconds': b['admission']['seconds'],
 'prepared_H_admission_seconds': p['admission']['seconds'],
 'baseline_output_bytes': b['output_bytes'],
 'prepared_output_bytes': p['output_bytes'],
 'baseline_cpu_user_seconds': b['cpu_user_seconds'],
 'baseline_cpu_system_seconds': b['cpu_system_seconds'],
 'prepared_cpu_user_seconds': p['cpu_user_seconds'],
 'prepared_cpu_system_seconds': p['cpu_system_seconds'],
 'baseline_process_tree_peak_sampled': b['process_tree_rss_peak_observed_bytes'],
 'prepared_process_tree_peak_sampled': p['process_tree_rss_peak_observed_bytes'],
 'baseline_row_group_reads': b['row_group_reads'],
 'prepared_row_group_reads': p['row_group_reads'],
 'baseline_scratch_component_peak': b['scratch_peak_component_bytes'],
 'prepared_scratch_component_peak': p['scratch_peak_component_bytes'],
 'baseline_receipts': b['index_builds_measured_operations'],
 'prepared_receipts': p['index_builds_measured_operations'],
}
positive['derived_savings_wall_seconds'] = positive['baseline_wall_seconds'] - positive['prepared_aligned_positive_wall_seconds']
positive['derived_savings_S_seconds'] = positive['baseline_S_index_seconds'] - positive['prepared_aligned_positive_S_index_seconds']
positive['derived_savings_Q_seconds'] = positive['baseline_Q_seconds'] - positive['prepared_Q_seconds']
positive['aligned_positive_overhead_seconds'] = positive['prepared_aligned_positive_wall_seconds'] - (positive['prepared_aligned_positive_S_index_seconds'] + positive['prepared_Q_seconds'] + positive['prepared_O_serialize_seconds'])
positive['Q_fraction_baseline'] = positive['baseline_Q_seconds'] / positive['baseline_wall_seconds']
positive['Q_fraction_prepared_aligned'] = positive['prepared_Q_seconds'] / positive['prepared_aligned_positive_wall_seconds']
positive['S_fraction_baseline'] = positive['baseline_S_index_seconds'] / positive['baseline_wall_seconds']
positive['S_fraction_prepared_aligned'] = positive['prepared_aligned_positive_S_index_seconds'] / positive['prepared_aligned_positive_wall_seconds']
positive['phase_model'] = 'H admission is outside wall; S index build is outside Q timer because DirectEstateI03Session.__enter__ builds before execute_empirical_query; Q is native evaluator/fact construction; O is post-call serialization. Positive wall = total wall - separately measured negative/restore wall.'
positive['unmeasurable_aligned'] = ['CPU (negative phase has no CPU fields)', 'process-tree RSS (aggregate includes negative/restore)', 'row_group_reads (aggregate includes negative/restore)', 'peak staging (component only, no staging peak)', 'process-tree continuous peak (0.25 s samples + maxrss only)']
positive['parity'] = r.get('parity')
positive['negative'] = r.get('negative')
positive['supervision'] = r.get('supervision')
print(json.dumps(positive, indent=2, sort_keys=True))
Path(__file__).resolve().parent.joinpath('RECOMPUTED_PHASES.json').write_text(json.dumps(positive,indent=2,sort_keys=True)+'\n')
