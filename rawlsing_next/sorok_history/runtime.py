"""Run one historical proposal through the authoritative world's durable outbox."""

from contextlib import nullcontext

from rawlsing_next.sorok_history.owner import HistoryRefusal
from rawlsing_next.sorok_history.provider import HistoricalModelProviderError


async def run_once(history, provider, *, lease_seconds=120, guard=nullcontext):
    """Resume a stored candidate first, or request and admit one new proposal."""
    with guard():
        ready_id = history.ready_candidate_id()
        if ready_id is not None:
            return history.commit_candidate(ready_id)
        if provider is None:
            return {"status": "LIVE_PROVIDER_NOT_RUN"}

        leased = history.lease(seconds=lease_seconds)
        if leased is None:
            return None

    job = leased["job"]
    job_id, token = job["id"], job["lease_token"]
    try:
        result = await provider.propose(leased["packet"])
    except HistoricalModelProviderError as exc:
        candidate = None
        receipt = {"failure_code": exc.code, "failure_grade": exc.failure_grade}
        retryable = exc.retryable
    else:
        candidate = result.candidate
        receipt = result.receipt.as_dict()
        retryable = receipt.get("failure_grade") in {"TRANSIENT", "RATE_LIMITED"}

    with guard():
        try:
            if candidate is None:
                status = history.record_failure(
                    job_id, token, receipt["failure_code"], receipt=receipt,
                    retryable=retryable,
                )
            else:
                status = history.record_candidate(job_id, token, candidate, receipt)
        except HistoryRefusal as exc:
            if str(exc) != "HISTORICAL_ATTEMPT_NOT_CURRENT":
                raise
            status = "ATTEMPT_SUPERSEDED"
        if status == "CANDIDATE_READY":
            return history.commit_candidate(job_id)
    return {"job_id": job_id, "status": status}
