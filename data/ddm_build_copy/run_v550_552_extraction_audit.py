"""Standalone runner for the V550–V552 extraction audit sidecar."""
from __future__ import annotations
import argparse
from dataclasses import dataclass
import json
import sys
import time
from pathlib import Path
from typing import Any
import pandas as pd
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from data.ddm_build_copy.v550_552_extraction_audit import build_v550_552_extraction_audit_package

@dataclass(frozen=True)
class ArtifactLoadResult:
    artifact_name: str
    path: Path
    frame: pd.DataFrame
    load_status: str
    error: str = ''

    def diagnostic_row(self, *, stage: str) -> dict[str, Any]:
        return {'stage': stage, 'artifact_name': self.artifact_name, 'path': str(self.path), 'load_status': self.load_status, 'row_count': int(len(self.frame)), 'error': self.error}

def _load_parquet_result(path: Path, *, label: str='', verbose: bool=False) -> ArtifactLoadResult:
    artifact_name = label or path.stem
    if not path.exists():
        if verbose:
            print(f'  [{artifact_name}] not found: {path}', flush=True)
        return ArtifactLoadResult(artifact_name, path, pd.DataFrame(), 'MISSING')
    try:
        frame = pd.read_parquet(path)
    except Exception as exc:
        if verbose:
            print(f'  [{artifact_name}] error loading {path}: {exc}', flush=True)
        return ArtifactLoadResult(artifact_name, path, pd.DataFrame(), 'READ_ERROR', type(exc).__name__)
    status = 'VALID_EMPTY' if frame.empty else 'LOADED'
    if verbose:
        print(f'  [{artifact_name}] {status.lower()} {len(frame)} rows from {path}', flush=True)
    return ArtifactLoadResult(artifact_name, path, frame, status)

def _load_parquet(path: Path, *, label: str='', verbose: bool=False) -> pd.DataFrame:
    """Compatibility wrapper.  Callers needing integrity must use the result form."""
    return _load_parquet_result(path, label=label, verbose=verbose).frame

def _load_json_result(path: Path, *, label: str='', verbose: bool=False) -> tuple[dict[str, Any], dict[str, Any]]:
    artifact_name = label or path.stem
    if not path.exists():
        return ({}, {'stage': 'v551', 'artifact_name': artifact_name, 'path': str(path), 'load_status': 'MISSING', 'row_count': None, 'error': ''})
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(payload, dict):
            raise TypeError('manifest root is not an object')
    except Exception as exc:
        if verbose:
            print(f'  [{artifact_name}] error loading {path}: {exc}', flush=True)
        return ({}, {'stage': 'v551', 'artifact_name': artifact_name, 'path': str(path), 'load_status': 'READ_ERROR', 'row_count': None, 'error': type(exc).__name__})
    return (payload, {'stage': 'v551', 'artifact_name': artifact_name, 'path': str(path), 'load_status': 'LOADED', 'row_count': 1, 'error': ''})

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Cross-stage extraction audit for V550/V551/V552/V550J.')
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--source', required=True)
    parser.add_argument('--wave', required=True)
    parser.add_argument('--canonical-wave', default=None, help='Defaults to --wave if not set.')
    parser.add_argument('--country-code', default=None, help='Defaults to --country if not set.')
    parser.add_argument('--country', default=None, help='Alias for --country-code.')
    parser.add_argument('--v550-root', default=str(ROOT / 'data' / 'ddm_repository_copy' / 'v550'))
    parser.add_argument('--v551-root', default=str(ROOT / 'data' / 'ddm_repository_copy' / 'v551' / 'runs'))
    parser.add_argument('--v552-root', default=str(ROOT / 'data' / 'ddm_repository_copy' / 'v552' / 'runs'))
    parser.add_argument('--v550j-root', default=str(ROOT / 'data' / 'ddm_repository_copy' / 'v550j'))
    parser.add_argument('--output-root', default=None, help='Defaults to <v550-root>/extraction_audit if not set.')
    parser.add_argument('--write-csv', action='store_true', default=False)
    parser.add_argument('--write-parquet', action='store_true', default=True)
    parser.add_argument('--verbose', action='store_true')
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    progress_started = time.monotonic()
    run_id = args.run_id
    source = args.source
    wave = args.wave
    canonical_wave = args.canonical_wave or wave
    country_code = args.country_code or args.country or ''
    v550_root = Path(args.v550_root)
    v551_root = Path(args.v551_root)
    v552_root = Path(args.v552_root)
    v550j_root = Path(args.v550j_root)
    output_root = Path(args.output_root or str(v550_root / 'extraction_audit'))
    out_dir = output_root / 'runs' / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    verbose = args.verbose
    load_diagnostics: list[dict[str, Any]] = []
    if verbose:
        print(f'[audit] Loading stage outputs for {source} / {wave} / {country_code}', flush=True)

    def load(stage: str, path: Path, name: str) -> pd.DataFrame:
        result = _load_parquet_result(path, label=f'{stage}_{name}', verbose=verbose)
        load_diagnostics.append(result.diagnostic_row(stage=stage))
        return result.frame
    v550_run_dir = v550_root / 'runs' / run_id
    v550_outputs: dict[str, pd.DataFrame] = {}
    v550_outputs['question_carry_forward_summary'] = load('v550', v550_run_dir / 'core' / 'question_carry_forward_summary.parquet', 'question_carry_forward_summary')
    v550_outputs['question_response_attitude_cloud'] = load('v550', v550_run_dir / 'clouds' / 'question_response_attitude_cloud.parquet', 'question_response_attitude_cloud')
    v551_run_dir = v551_root / run_id
    v551_outputs: dict[str, pd.DataFrame] = {}
    for table_name in ('numeric_wrapper_audit', 'directional_candidate_adjudication', 'relation_evidence_atoms', 'directional_distribution_coverage', 'relation_review_surface', 'blocked_signal_audit', 'certification_candidate_bridge'):
        v551_outputs[table_name] = load('v551', v551_run_dir / f'{table_name}.parquet', table_name)
    v551_outputs['bridge'] = v551_outputs['certification_candidate_bridge']
    v551_manifest, manifest_diag = _load_json_result(v551_run_dir / 'manifest.json', label='manifest', verbose=verbose)
    load_diagnostics.append(manifest_diag)
    v552_run_dir = v552_root / run_id
    v552_outputs = {'v552_directionality_gap_surface': load('v552', v552_run_dir / 'audits' / 'v552_directionality_gap_surface.parquet', 'directionality_gap_surface'), 'v552_status_pressure_review_surface': load('v552', v552_run_dir / 'audits' / 'v552_status_pressure_review_surface.parquet', 'status_pressure_review_surface')}
    shard_id = f'{source}__{canonical_wave}'
    v550j_pattern_dir = v550j_root / 'runs' / run_id / shard_id / 'joint_patterns'
    v550j_outputs = {'joint_pattern_association_review_surface': load('v550j', v550j_pattern_dir / 'joint_pattern_association_review_surface.parquet', 'joint_pattern_association_review_surface')}
    if verbose:
        print('[audit] Building extraction audit package...', flush=True)
    load_audit = pd.DataFrame(load_diagnostics)
    package = build_v550_552_extraction_audit_package(run_id=run_id, source=source, wave=wave, canonical_wave=canonical_wave, country_code=country_code, v550_outputs=v550_outputs, v551_outputs=v551_outputs, v552_outputs=v552_outputs, v550j_outputs=v550j_outputs, v551_manifest=v551_manifest, artifact_load_diagnostics=load_audit)
    written: list[dict[str, Any]] = []
    for table_name, frame in package.items():
        if frame is None or frame.empty:
            continue
        parquet_path = out_dir / f'{table_name}.parquet'
        csv_path = out_dir / f'{table_name}.csv'
        if args.write_parquet:
            frame.to_parquet(parquet_path, index=False)
        if args.write_csv:
            frame.to_csv(csv_path, index=False)
        written.append({'table_name': table_name, 'rows': int(len(frame)), 'parquet': str(parquet_path) if args.write_parquet else '', 'csv': str(csv_path) if args.write_csv else ''})
        if verbose:
            print(f'  [audit] wrote {table_name}: {len(frame)} rows', flush=True)
    elapsed = time.monotonic() - progress_started
    readiness_row = package.get('readiness_report', pd.DataFrame())
    state: dict[str, Any] = {}
    if isinstance(readiness_row, pd.DataFrame) and (not readiness_row.empty):
        for key in ('run_integrity_status', 'evidence_status', 'downstream_permission_status', 'coverage_status', 'candidate_count', 'directionally_applicable_count', 'promotable_count', 'nonpromotable_count', 'not_applicable_count', 'overall_status'):
            if key in readiness_row.columns:
                value = readiness_row.iloc[0][key]
                state[key] = value.item() if hasattr(value, 'item') else value
    manifest = {'run_id': run_id, 'source': source, 'wave': wave, 'canonical_wave': canonical_wave, 'country_code': country_code, **state, 'written_tables': written, 'elapsed_seconds': round(elapsed, 2)}
    manifest_path = out_dir / 'v550_552_extraction_audit_manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    profile = {'run_id': run_id, 'compiler_name': 'v550_552_extraction_audit', 'elapsed_seconds': round(elapsed, 2), 'source': source, 'wave': wave, 'canonical_wave': canonical_wave, 'country_code': country_code, 'output_tables': [entry['table_name'] for entry in written], 'total_output_rows': int(sum((entry['rows'] for entry in written)))}
    profile_path = out_dir / 'v550_552_extraction_audit_performance_profile.json'
    profile_path.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding='utf-8')
    if verbose:
        print(f'[audit] Done in {elapsed:.1f}s — {len(written)} tables, manifest at {manifest_path}', flush=True)
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
