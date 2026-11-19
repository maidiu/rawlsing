#!/usr/bin/env python3
import json,sys,shutil,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import witness_caller as w
assert w.STARTUP_FREE_FLOOR == 26907826727, w.STARTUP_FREE_FLOOR
assert w.IN_FLIGHT_FREE_FLOOR == 8*1024**3, w.IN_FLIGHT_FREE_FLOOR
assert w.RAM_CAP == 6*1024**3, w.RAM_CAP
root=HERE/'DISK_GUARD_TEST';root.mkdir(mode=0o700,exist_ok=True)
s=[];abort=w._sample(__import__('os').getpid(),root,s)
out={'startup_free_floor':w.STARTUP_FREE_FLOOR,'in_flight_free_floor':w.IN_FLIGHT_FREE_FLOOR,'rss_cap':w.RAM_CAP,'current_free':shutil.disk_usage(root).free,'sample_abort':abort}
(HERE/'DISK_GUARD_TEST.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out))
