"""Authority-67 independent trailing full audit for frozen V4 output."""
from __future__ import annotations

import gzip, hashlib, json, multiprocessing as mp, os, queue, resource, shutil, time
from pathlib import Path

from rawlsing_next import pre553_r5_compact_carrier as compact
from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.pre553_r5_compact_density_court import WVS_ROWS, WVS_SHA256, WVS_VARIABLES, _release_identity
from rawlsing_next.pre553_r5_serial_turbo66 import SerialTurboBuilder, TurboConfig
from rawlsing_next.pre553_r5_serial_turbo66_court import source_rows

V4 = TurboConfig("V4", 65536, 67108864, 64, 1, False, 16384, 16777216, 6, True)
QUEUE_MAX = 8


class ReadinessTelemetry:
    """Shared exact state for Authority-67 bounded readiness admission."""
    def __init__(self):
        self.lock = mp.RLock()
        self.pending = mp.Value("i", 0, lock=False)
        self.inflight = mp.Value("i", 0, lock=False)
        self.pending_peak = mp.Value("i", 0, lock=False)
        self.inflight_peak = mp.Value("i", 0, lock=False)
        self.outstanding_peak = mp.Value("i", 0, lock=False)

    def _check(self):
        if not (0 <= self.pending.value <= QUEUE_MAX):
            raise compact.R5IntegrityError("Authority-67 pending readiness queue bound violated")
        if not (0 <= self.inflight.value <= 1):
            raise compact.R5IntegrityError("Authority-67 auditor inflight bound violated")

    def admit(self):
        with self.lock:
            self.pending.value += 1; self._check()
            self.pending_peak.value = max(self.pending_peak.value, self.pending.value)
            self.outstanding_peak.value = max(self.outstanding_peak.value, self.pending.value + self.inflight.value)

    def begin_audit(self):
        with self.lock:
            self.pending.value -= 1; self.inflight.value += 1; self._check()
            self.inflight_peak.value = max(self.inflight_peak.value, self.inflight.value)
            self.outstanding_peak.value = max(self.outstanding_peak.value, self.pending.value + self.inflight.value)

    def finish_audit(self):
        with self.lock:
            self.inflight.value -= 1; self._check()

    def snapshot(self):
        with self.lock:
            self._check()
            return {"pending_queue_peak": self.pending_peak.value, "auditor_inflight_peak": self.inflight_peak.value, "outstanding_closed_members_peak": self.outstanding_peak.value, "pending_queue_depth": self.pending.value, "auditor_inflight": self.inflight.value}


def _audit_member(path: Path):
    sha, length = compact._sha256_file(path)
    digest = hashlib.sha256(); rows = 0; first = last = None; relations = {}
    with path.open("rb") as raw:
        with gzip.GzipFile(mode="rb", fileobj=raw) as gz:
            for line in gz:
                row = compact._decode_storage(line)
                digest.update(compact._logical_wire(row)); rows += 1
                if first is None: first = row.identity_key
                last = row.identity_key
                relations[row.relation] = relations.get(row.relation, 0) + 1
    if first is None:
        raise compact.R5IntegrityError("closed final member is empty")
    return {"member": path.name, "byte_length": length, "sha256": sha,
            "logical_digest": digest.hexdigest(), "row_count": rows,
            "first_identity": list(first), "last_identity": list(last),
            "relation_counts": dict(sorted(relations.items()))}


def _auditor(target_s, ready, result, telemetry, slots):
    """Process target: derives all member facts from bytes, never builder truth."""
    target = Path(target_s); expected = 0; buffered = {}; derived = []; previous = None
    global_digest = hashlib.sha256(); global_rows = 0; global_relations = {}
    try:
        while True:
            item = ready.get()
            kind = item[0]
            if kind == "closed":
                ordinal, name = item[1], item[2]
                telemetry.begin_audit(); slots.release()
                if ordinal < expected or ordinal in buffered:
                    raise compact.R5IntegrityError("duplicate readiness ordinal")
                buffered[ordinal] = name
                if len(buffered) > QUEUE_MAX:
                    raise compact.R5IntegrityError("readiness buffer exceeded bounded protocol")
                while expected in buffered:
                    name = buffered.pop(expected)
                    try:
                        d = _audit_member(target / "members" / name)
                    finally:
                        telemetry.finish_audit()
                    first = tuple(d["first_identity"]); last = tuple(d["last_identity"])
                    if previous is not None and first <= previous:
                        raise compact.R5IntegrityError("trailing audit found duplicate/noncanonical row order")
                    previous = last
                    # Re-open only the audited member to form the global exact wire.
                    with gzip.open(target / "members" / name, "rb") as gz:
                        for line in gz:
                            row = compact._decode_storage(line)
                            global_digest.update(compact._logical_wire(row)); global_rows += 1
                            global_relations[row.relation] = global_relations.get(row.relation, 0) + 1
                    derived.append(d); expected += 1
            elif kind == "sealed":
                if buffered:
                    raise compact.R5IntegrityError("missing readiness ordinal before root reconciliation")
                reader = compact.R5CompactLongShardedReader(target)
                inventory = list(reader.iter_inventory())
                if len(inventory) != len(derived):
                    raise compact.R5IntegrityError("readiness/member inventory cardinality mismatch")
                fields = ("member", "byte_length", "sha256", "logical_digest", "row_count", "first_identity", "last_identity", "relation_counts")
                for independent, sealed in zip(derived, inventory):
                    if any(independent[k] != sealed[k] for k in fields):
                        raise compact.R5IntegrityError("trailing audit inventory reconciliation mismatch")
                if global_rows != reader.root["canonical_row_count"] or global_digest.hexdigest() != reader.root["logical_stream_digest"]:
                    raise compact.R5IntegrityError("trailing audit global reconciliation mismatch")
                result.put({"ok": True, "audit": {"physical_root_id": reader.root["physical_root_id"], "canonical_rows": global_rows, "logical_stream_digest": global_digest.hexdigest(), "relation_counts": dict(sorted(global_relations.items()))}, "members": derived})
                return
            else:
                raise compact.R5IntegrityError("unknown trailing-audit notification")
    except BaseException as exc:
        result.put({"ok": False, "error": f"{type(exc).__name__}: {exc}"})


def run_overlap(source: Path, checkpoint: int, work: Path):
    """Build frozen V4 once while a single independent auditor trails it."""
    if hashlib.sha256(source.read_bytes()).hexdigest() != WVS_SHA256:
        raise RuntimeError("source hash mismatch")
    shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
    incidence = decode_sav(source)
    if incidence.row_count != WVS_ROWS or len(incidence.variables) != WVS_VARIABLES:
        raise RuntimeError("source shape mismatch")
    ready = mp.Queue(maxsize=QUEUE_MAX); results = mp.Queue(maxsize=1); target = work / "sealed"
    telemetry_state = ReadinessTelemetry(); slots = mp.BoundedSemaphore(QUEUE_MAX)
    auditor = mp.Process(target=_auditor, args=(str(target), ready, results, telemetry_state, slots), daemon=True)
    start = time.perf_counter(); auditor.start(); audit_started = time.perf_counter()
    blocked = 0.0
    def notify(ordinal, name):
        nonlocal blocked
        t = time.perf_counter(); slots.acquire(); blocked += time.perf_counter() - t
        telemetry_state.admit(); ready.put(("closed", ordinal, name))
    progress = {"cells_done": 0}
    try:
        telemetry = SerialTurboBuilder(V4, member_ready_hook=notify).build(source_rows(incidence, checkpoint, progress), release_identity=_release_identity(checkpoint), target_directory=target)
        root_sealed = time.perf_counter(); ready.put(("sealed",)); auditor.join(timeout=3600)
        if auditor.is_alive(): auditor.terminate(); auditor.join(); raise RuntimeError("trailing auditor timeout")
        outcome = results.get_nowait()
        if not outcome["ok"]: raise RuntimeError(outcome["error"])
    except BaseException:
        if auditor.is_alive(): auditor.terminate(); auditor.join()
        raise
    finished = time.perf_counter(); ordinary = compact.R5CompactLongShardedReader(target, expected_physical_root_id=telemetry["physical_root_id"]).full_audit()
    if ordinary != outcome["audit"]:
        raise compact.R5IntegrityError("trailing audit result differs from ordinary full_audit")
    return {"target": str(target), "telemetry": telemetry, "audit": outcome["audit"], "ordinary_audit": ordinary,
            "overlap_wall_seconds": finished-start, "auditor_start_seconds": audit_started-start,
            "auditor_finish_lag_after_root_seal_seconds": finished-root_sealed, **telemetry_state.snapshot(),
            "builder_blocked_seconds": blocked, "audit_rows_per_second": outcome["audit"]["canonical_rows"]/(finished-audit_started)}
