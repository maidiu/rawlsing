"""Classify exception types for frozen reviewer index hostiles without altering courts."""
import json,pathlib,tempfile
from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I
rows=[]
for field in ['release_ref','selection_key_ref','selected_receipt']:
 with tempfile.TemporaryDirectory() as d:
  root=pathlib.Path(d);p,_=I.build_product(root);path=root/'product_index.json';data=json.loads(path.read_text())
  if field=='selected_receipt':data[field]['selected_release_ref']=p.subject_ref.as_dict()
  else:data[field]=p.subject_ref.as_dict()
  I.save_json(path,data)
  try:q=I.restore_product(root);I.serve(q)
  except Exception as e:rows.append(dict(field=field,exception=type(e).__name__,message=str(e),typed=isinstance(e,ValueError)))
  else:rows.append(dict(field=field,accepted=True))
print(json.dumps(rows,indent=2))
