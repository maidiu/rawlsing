#!/usr/bin/env python3
"""Bounded Wave-1 metadata witness for the missing config->Q2 inventory link."""
from __future__ import annotations
import json, subprocess, tempfile
from pathlib import Path
ROOT=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117')
OWNER=ROOT/'OWNER'; IMP=ROOT/'IMPLEMENTER'
INDEX=OWNER/'WORKER_RETURNS/ANVIL_ALL35_R157_CONFIG_MATERIALIZATION_20261118/CONFIG_INDEX.json'
SNAP=Path('/tmp/anvil_all35_aee')

def main():
    import sys
    sys.path.insert(0,str(SNAP))
    from rawlsing_next.pre553_r157_projection_adapter import load_source_config, canonical_config_hash
    idx=json.loads(INDEX.read_text()); row=next(x for x in idx['rows'] if x['source_id']=='SRC01'); sc=row['source_config']
    raw=subprocess.check_output(['git','-C',str(IMP),'show',sc['revision_ref']])
    with tempfile.TemporaryDirectory(prefix='anvil-wave1-') as td:
        p=Path(td)/'SRC01.config.json';p.write_bytes(raw)
        config=load_source_config(p)
        doc=config.document
        out={
          'schema':'ANVIL_WAVE1_CONSTRUCTION_INPUT_WITNESS@1',
          'source_id':'SRC01','config_revision_ref':sc['revision_ref'],
          'config_file_sha256':sc['file_sha256'],'config_canonical_sha256':canonical_config_hash(config),
          'parsed':{'source_id':config.source_id,'identity_class':config.identity_class,'source_sha256':config.active_source_sha256},
          'metadata_shape':{'questions':len(doc.get('questions',[])),'physical_slots':len(doc.get('physical_slots',[])),'items':len(doc.get('items',[])),'response_slots':len(doc.get('response_slots',[])),'coordinate_slots':len(doc.get('coordinate_slots',[])),'weight_slots':len(doc.get('weight_slots',[])),'routing':len(doc.get('routing',[]))},
          'required_q2_preimages':{
            'occurrence_target_role': 'ABSENT_FROM_SOURCE_CONFIG__NOT_DERIVABLE_EXACTLY',
            'occurrence_conditioner_role': 'ABSENT_FROM_SOURCE_CONFIG__NOT_DERIVABLE_EXACTLY',
            'occurrence_forms_domain_administration': 'PARTIAL_OR_ABSENT__NO_EXACT_Q2_MAPPING',
            'measure_plans': 'ABSENT_FROM_SOURCE_CONFIG',
            'held_records': 'ABSENT_FROM_SOURCE_CONFIG',
            'grammar_policy': 'ABSENT_FROM_SOURCE_CONFIG',
            'scientific_frontier': 'ABSENT_FROM_SOURCE_CONFIG',
            'frozen_input_census': 'ABSENT_FROM_SOURCE_CONFIG'
          },
          'earliest_gate':{
            'symbol':'SourceInventory',
            'file':'rawlsing_next/universal_grammar/types.py:277',
            'reason':'SourceConfig carries source-native item/question/response metadata but not the exact occurrence roles, measure plans, held records, or grammar policy required by SourceInventory and ScientificFrontier. Constructing those would require a new owner-approved interpretation, not an exact preimage.',
            'existing_parser_validated':True,
            'source_config_validator':'rawlsing_next/pre553_r157_projection_adapter.py:load_source_config',
            'downstream_consumer':'rawlsing_next/pre553_source_i02_handoff.py:build_source_i02_handoff:987',
            'downstream_first_gate':'rawlsing_next/pre553_source_i02_handoff.py:_verify_census_before_source:218'
          },
          'verdict':'CONFIG_METADATA_PARSED__Q2_INVENTORY_PREIMAGE_ABSENT__STOP_BEFORE_SCIENCE_CONSTRUCTION',
          'no_source_body_access':True,
        }
        print(json.dumps(out,indent=2))
        return out
if __name__=='__main__':
    out=main();Path(__file__).resolve().parent.joinpath('WAVE1_WITNESS.json').write_text(json.dumps(out,indent=2)+'\n')
