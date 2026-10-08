"""Bounded reproduction: does PyList_AsTuple steal its input list reference?

This is the independent check behind the HQ248 repair. Run standalone under the
governed interpreter; it touches no project module and mutates nothing.
"""
import ctypes
import sys


def probe(fname, build, label):
    f = getattr(ctypes.pythonapi, fname)
    f.restype = ctypes.py_object
    f.argtypes = [ctypes.py_object]
    obj = build()
    before = sys.getrefcount(obj)
    res = f(obj)
    after = sys.getrefcount(obj)
    delta = after - before
    steals = (delta == -1)
    print("%-22s refcount delta=%+d  -> %s" % (label, delta,
          "STEALS (caller must NOT decref)" if steals else "does NOT steal (caller OWNS it)"))
    return res, steals


print("interpreter:", sys.version.split()[0])
res1, steals1 = probe("PyList_AsTuple",   lambda: [1, 2, 3], "PyList_AsTuple(list3)")
res2, steals2 = probe("PyList_AsTuple",   lambda: [],       "PyList_AsTuple(empty)")
res3, steals3 = probe("PySequence_Tuple", lambda: [1, 2, 3], "PySequence_Tuple(list3)")
assert type(res1).__name__ == "tuple", res1
if steals1 or steals2 or steals3:
    print("RESULT: this interpreter's PyList_AsTuple DOES steal -- the HQ248 patch premise is WRONG")
    sys.exit(2)
print("RESULT: PyList_AsTuple does NOT steal. The R2 source comment asserting a steal, and")
print("        therefore the absence of a Py_DECREF(ordered), was a real ownership defect.")
sys.exit(0)
