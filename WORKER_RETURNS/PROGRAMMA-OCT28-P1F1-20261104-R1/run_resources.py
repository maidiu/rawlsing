from hashlib import sha256
import json, lzma, os, pathlib, subprocess
root = pathlib.Path('/tmp/rawlsing-oct28-p1f1')
candidate = pathlib.Path('/Users/matthewsmith/.codex/worktrees/60ed/Rawlsing')
baseline = pathlib.Path('/Users/matthewsmith/.codex/worktrees/oct28-p1r1-baseline/Rawlsing')
python = '/tmp/rawlsing-oct28-p1r1/venv/bin/python'
packet = root / 'packet'
resources = root / 'resources'
resources.mkdir(exist_ok=True)
for name, target in [('base', baseline), ('p1', candidate)]:
    path = resources / name
    if not path.exists(): path.symlink_to(target, target_is_directory=True)
env = dict(os.environ, PATH='/tmp/rawlsing-oct28-p1r1/venv/bin:' + os.environ['PATH'], PYTHONPATH='.', PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1', LC_ALL='C')
results = []
def run(label, argv, cwd=candidate, extra=None):
    active = dict(env, **(extra or {}))
    with (root / (label + '.log')).open('w') as out:
        result = subprocess.run(argv, cwd=cwd, env=active, stdout=out, stderr=subprocess.STDOUT)
    results.append(dict(label=label, argv=argv, exit_code=result.returncode))
    (root / 'resources-status.json').write_text(json.dumps(results, indent=2))
    print(label, result.returncode, flush=True)
    if result.returncode: raise SystemExit(result.returncode)
# Original probe asks for an exploit. The fixed counterpart keeps every fault,
# native lookup and restoration but requires that neither loop changes any fact.
p = packet / 'probe_selector_ref_alias.py'
body = p.read_text().replace('    if changed:', '    assert not changed, "selector descendant changed downstream exact facts"\n    if changed:')
body = body.replace('raise AssertionError("no exercised selector changed a downstream fact")', 'print("PASS: all event-ref faults preserve exact supported facts and sealed native lookup")')
body = body.replace('raise AssertionError("no question ref alias changed a downstream fact")', 'print("PASS: all shared question-ref faults preserve exact facts across respondents and restoration")')
fixed_probe = packet / 'probe_selector_ref_alias_fixed.py'
fixed_probe.write_text(body)
run('selector-alias-fixed-GREEN', [python, str(fixed_probe)])
run('native-ref-control', [python, str(packet / 'probe_native_ref_baseline.py')], cwd=baseline)
for label, cwd, cache in [('base', baseline, ''), ('fixed', candidate, str(root / 'native-cache'))]:
    destination = root / ('native-' + label)
    destination.mkdir(exist_ok=True)
    run('native-' + label, [python, str(root / 'inputs/capture_native.py'), str(root / 'inputs/same-source.sav'), str(destination)], cwd=cwd, extra={'RAWLSING_C11_ACCELERATOR_DIR': cache})
parity = {}
for path in sorted((root / 'native-base').iterdir()):
    other = root / 'native-fixed' / path.name
    assert path.read_bytes() == other.read_bytes(), path.name
    parity[path.name] = dict(equal=True, bytes=path.stat().st_size, sha256=sha256(path.read_bytes()).hexdigest())
    if path.name == 'native.json':
        (root / 'native.json.xz').write_bytes(lzma.compress(path.read_bytes()))
(root / 'native-parity.json').write_text(json.dumps(parity, indent=2))
print('native and checkpoints byte-exact', flush=True)
# Reuse the reviewer resource script with only the exact candidate pin changed.
original = packet / 'run_pairs.sh'
pin = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=candidate, text=True).strip()
script = original.read_text().replace('0a63e7c90cabcfd01dbb169d477f2d0ead5be22c', pin)
adapted = packet / 'run_pairs_fixed.sh'
adapted.write_text(script)
run('resource-pairs', ['bash', str(adapted), str(resources), str(root / 'inputs')])
with (root / 'MEASUREMENTS.json').open('w') as out:
    result = subprocess.run([python, str(packet / 'compare.py'), str(resources / 'evidence')], cwd=candidate, env=env, stdout=out, stderr=subprocess.STDOUT)
assert result.returncode == 0
print('resource parity and cache assertions PASS', flush=True)
