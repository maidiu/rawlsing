#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

FIXED_CREATED_AT = '2026-07-31T00:00:00+00:00'


def main() -> None:
    parser = argparse.ArgumentParser(description='Regenerate recovered V552 question-semantic hierarchy evidence deterministically.')
    parser.add_argument('--output-dir', default=str(Path(__file__).resolve().parent / 'generated_question_semantic_hierarchy'))
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    repo = here / 'runtime_reproducibility_code'
    sys.path.insert(0, str(repo))
    from data.ddm_build_copy.ddm_v552_structural import build_question_semantic_hierarchy

    inputs = here / 'runtime_reproducibility_inputs' / 'v551_atoms'
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    records = []
    for source_type in ('crosssurvey', 'gss8'):
        base = inputs / source_type
        for atom_path in sorted(base.glob('*/relation_evidence_atoms.csv')):
            scope = atom_path.parent.name
            atoms = pd.read_csv(atom_path, dtype=str, keep_default_na=False)
            hierarchy = build_question_semantic_hierarchy(atoms)
            if 'created_at' in hierarchy.columns:
                hierarchy['created_at'] = FIXED_CREATED_AT
            filename = f'{source_type}__{scope}_question_semantic_hierarchy.csv'
            hierarchy.to_csv(output / filename, index=False)
            records.append({'source_type': source_type, 'scope': scope, 'input_rows': int(len(atoms)), 'output_rows': int(len(hierarchy)), 'output_file': filename})
    print(json.dumps({'scope_files': len(records), 'total_output_rows': sum(r['output_rows'] for r in records), 'records': records}, indent=2))


if __name__ == '__main__':
    main()
