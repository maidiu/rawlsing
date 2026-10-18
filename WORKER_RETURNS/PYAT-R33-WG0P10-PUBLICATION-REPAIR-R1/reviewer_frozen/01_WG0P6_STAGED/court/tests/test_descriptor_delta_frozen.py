"""WG0M assertions frozen before WG0P5 read; adapter only supplies raw calls."""
import hashlib,importlib,json,os
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[1]
O=json.loads((R/'01_FROZEN_DESCRIPTOR_EXPECTATIONS.json').read_text())
@pytest.fixture(scope='module')
def court():
 for row in O['preserved_files']:assert hashlib.sha256((R/row['path']).read_bytes()).hexdigest()==row['sha256']
 return importlib.import_module(os.environ.get('WG0M_DESCRIPTOR_ADAPTER','descriptor_adapter_v1')).DescriptorCourt()
@pytest.mark.parametrize('control',O['controls'],ids=[x['group']+'/'+x['case'] for x in O['controls']])
def test_frozen_descriptor_source_integrity(court,control):
 e=court.execute_case(control['group'],control['case'])
 assert e['attempted'] and e['raw_path'] and e['physical_modules']
 assert e['exception_type'] in control['allowed_exceptions'] or e['typed_refusal'] in ('HELD','INADMISSIBLE','REVOKED','STALE','REFUSED','UNAVAILABLE')
 assert not e['served_positive']
 assert e['new_I03_calls']==0
