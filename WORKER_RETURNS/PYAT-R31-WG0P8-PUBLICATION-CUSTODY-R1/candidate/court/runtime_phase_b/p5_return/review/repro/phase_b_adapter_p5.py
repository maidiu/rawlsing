"""Explicit candidate identity transport; all frozen65 assertions unchanged."""
from phase_b_adapter_v1 import Adapter as OriginalAdapter
class Adapter(OriginalAdapter):
 candidate_sha='7499f32abd8d8027a37fe86f090ed3248ec71169'

 def register_committed(self):
  import pathlib,subprocess
  from phase_b_support_v1 import R
  path=R/'observations/phase_b/reviewer_second_frontier_register.json'
  root=pathlib.Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=R,text=True).strip())
  relative=path.relative_to(root).as_posix()
  actual=path.read_bytes()
  committed=subprocess.check_output(['git','show',self.candidate_sha+':'+relative],cwd=R)
  original=subprocess.check_output(['git','show','bec9a128922e4e431ce2ed862aa7802c902813ed:WORKER_RETURNS/PYAT-USERDIRECT-20261015-R10-WG0L-INDEPENDENT-FULL-ENGINE-COURT-R1/observations/phase_b/reviewer_second_frontier_register.json'],cwd=R)
  return actual==committed==original
