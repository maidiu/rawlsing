"""Driver-facing FIABC process-isolation backend adapter.

The court driver may import this adapter in its long-lived orchestration process.
No candidate implementation is imported here. The actual P2X backend is loaded
only inside the sealed source×candidate child process created by the controller.
"""
from __future__ import annotations

import atexit
import os
from pathlib import Path

from rawlsing_next.ee_p2x_candidate_process_envelope import (
    BACKEND_CONTRACT,
    ProcessIsolationController,
)

INNER_BACKEND_DEFAULT = "rawlsing_next.ee_p2x_darwin_stage_backend"

_CONTROLLER: ProcessIsolationController | None = None


def _explicit_resume_cells() -> tuple[str, ...]:
    raw = os.environ.get("RAWLSING_EE_P2X_EXPLICIT_RESUME_CELLS", "")
    return tuple(sorted({item.strip() for item in raw.split(",") if item.strip()}))


def _warm_state_transitions() -> tuple[str, ...]:
    raw = os.environ.get("RAWLSING_EE_P2X_WARM_STATE_TRANSITIONS", "")
    return tuple(sorted({item.strip() for item in raw.split(",") if item.strip()}))


def _controller() -> ProcessIsolationController:
    global _CONTROLLER
    if _CONTROLLER is None:
        freeze = os.environ.get("RAWLSING_EE_P2X_FROZEN_UPSTREAM_RECEIPT")
        if not freeze:
            raise RuntimeError(
                "RAWLSING_EE_P2X_FROZEN_UPSTREAM_RECEIPT is required before "
                "candidate execution; it must name the already-frozen "
                "candidate-neutral source/authority/workload/oracle receipt"
            )
        inner = os.environ.get("RAWLSING_EE_P2X_INNER_BACKEND", INNER_BACKEND_DEFAULT)
        if inner == __name__:
            raise RuntimeError("process-isolation adapter may not wrap itself")
        _CONTROLLER = ProcessIsolationController(
            backend_spec=inner,
            freeze_receipt_path=Path(freeze),
            resume_cells=_explicit_resume_cells(),
            warm_state_transitions=_warm_state_transitions(),
            context_mode="DRIVER",
        )
    return _CONTROLLER


def run_stage(context, services):
    result = _controller().run_stage(context, services)
    return {
        "terminal_disposition": result.terminal_disposition,
        "receipt": dict(result.receipt),
        "output_artifacts": {str(k): str(v) for k, v in result.output_artifacts.items()},
        "verifier_complete": result.verifier_complete,
    }


def _close() -> None:
    global _CONTROLLER
    if _CONTROLLER is not None:
        _CONTROLLER.close()
        _CONTROLLER = None


atexit.register(_close)


__all__ = ["BACKEND_CONTRACT", "INNER_BACKEND_DEFAULT", "run_stage"]
