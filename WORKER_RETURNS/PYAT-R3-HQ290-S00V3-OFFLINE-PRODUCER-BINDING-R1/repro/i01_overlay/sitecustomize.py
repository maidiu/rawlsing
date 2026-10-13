"""Load only the S00V2 candidate seam over the exact retained I01 tree."""
import importlib.util,os,sys
sys.path.insert(0, os.environ["S00V2_I01_ROOT"])
import rawlsing_next
rawlsing_next.__path__ = [os.path.join(os.environ["S00V2_I01_ROOT"], "rawlsing_next")]
path=os.environ['S00V2_SEAM_PATH']
name='rawlsing_next.r3_s02_seam_witness'
spec=importlib.util.spec_from_file_location(name,path)
module=importlib.util.module_from_spec(spec)
sys.modules[name]=module
spec.loader.exec_module(module)
rawlsing_next.r3_s02_seam_witness=module
