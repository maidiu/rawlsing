"""Separately versioned integrated typed-refusal gate, frozen before execution.
Original reviewer tests remain unchanged. This supplements observed refusal
classification and does not modify S00V3 or I01R source.
"""
import json
import pytest
from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I

def test_forged_selection_key_requires_typed_product_refusal(tmp_path):
 p,_=I.build_product(tmp_path);path=tmp_path/'product_index.json';data=json.loads(path.read_text());data['selection_key_ref']=p.subject_ref.as_dict();I.save_json(path,data)
 with pytest.raises(I.I01Error):I.restore_product(tmp_path)
