import sys, json, os
import deployment as D
import pv2_original_scope_register as OLD

source_calls = []


def trace(frame, event, arg):
    if event == "call" and frame.f_code.co_name in {
        "execute_empirical_query",
        "execute_exact_bounded_discovery",
        "validate_c11_source_release",
    }:
        source_calls.append(frame.f_code.co_name)


sys.setprofile(trace)
try:
    result = D.api.read_current_consumer_material(
        OLD.author_sourcefree_original_scope_register(), json.load(open(sys.argv[1]))
    )
    raise AssertionError("FRESH_OFFLINE_HISTORY_WAS_SERVED")
except ValueError as e:
    print(
        json.dumps(
            {
                "pid": os.getpid(),
                "claim": str(e),
                "source_calls": len(source_calls),
                "servable": False,
            }
        )
    )
