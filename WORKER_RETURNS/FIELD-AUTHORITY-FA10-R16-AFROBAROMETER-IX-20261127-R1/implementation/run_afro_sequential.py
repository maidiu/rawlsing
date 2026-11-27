"""Resume the frozen Afro core serially. Prior accepted stages are never regenerated."""
import contextlib
import fcntl
from pathlib import Path
import shlex
from subprocess import SubprocessError
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT / "frozen"))
import fa10

WORK = ROOT / "core"
ATTEMPT = "attempt-afro-sequential"
BRIDGE = ROOT / "opencode_provider_sequential.py"


def refresh_status():
    status = {}
    for arm, plan in fa10.PLAN["arms"].items():
        status[arm] = next(
            (role for role in plan["stages"]
             if not (fa10.stage_path(WORK, arm, role) / "accepted.json").is_file()),
            "PROJECTED" if (WORK / arm / "projection.json").is_file() else "PROJECTION_REQUIRED",
        )
    fa10.r9.save(WORK / "CORE_STATUS.json", status)
    return status


def execute():
    # Preserve the already-banked random arm order within each pair. The
    # user's Afro-only direction prioritizes closing the specialized chains.
    prior_order = fa10.r9.read(WORK / "CONTROLLER_ONLY_ORDER.json")
    arm_order = sorted(prior_order, key=lambda arm: arm in {"A","B"})
    for arm in arm_order:
        for role in fa10.PLAN["arms"][arm]["stages"]:
            packet = fa10.prepare_stage(arm,role,WORK)
            stage = fa10.stage_path(WORK,arm,role)
            if (stage/"accepted.json").exists():
                fa10.validate(packet,fa10.r9.read(stage/"response.json"))
                continue
            if (stage/ATTEMPT).exists():
                print(arm,role,"PREVIOUS_SERIAL_ATTEMPT_HELD",flush=True)
                break
            cap = fa10.PLAN["budget_proposal"]["stage_caps"][role]
            command = shlex.join([sys.executable,str(BRIDGE),"--cap",str(cap)])
            started = datetime.now(timezone.utc).isoformat()
            print(started,arm,role,"START",flush=True)
            try:
                result,_ = fa10.transport.call(packet,command,ATTEMPT,stage)
                fa10.accept(arm,role,WORK,result)
            except (ValueError,KeyError,SubprocessError) as error:
                fa10.r9.save(stage/(ATTEMPT+"-rejection.json"),
                            {"error":type(error).__name__,"reason":str(error),"start_utc":started})
                print(arm,role,"HELD",type(error).__name__,str(error),flush=True)
                break
            else:
                print(arm,role,"ACCEPTED_STRUCTURALLY",flush=True)
                refresh_status()
        else:
            fa10.project(arm,WORK)
            print(arm,"PROJECTED",flush=True)
    status = refresh_status()
    if all(x=="PROJECTED" for x in status.values()) and not (WORK/"blinded").exists():
        fa10.blind(WORK)
    print(status,flush=True)


if __name__=="__main__":
    with (WORK/".sequential.lock").open("a") as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        execute()
