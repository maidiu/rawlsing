"""Run one historical proposal through the authoritative world's durable outbox."""


async def run_once(history, provider, *, lease_seconds=120):
    """Resume a stored candidate first, or request and admit one new proposal."""
    ready_id = history.ready_candidate_id()
    if ready_id is not None:
        return history.commit_candidate(ready_id)

    leased = history.lease(seconds=lease_seconds)
    if leased is None:
        return None

    job = leased["job"]
    job_id, token = job["id"], job["lease_token"]
    result = await provider.propose(leased["packet"])
    receipt = result.receipt.as_dict()
    if result.candidate is None:
        status = history.record_failure(
            job_id, token, receipt["failure_code"], receipt=receipt,
            retryable=receipt["failure_grade"] in {"TRANSIENT", "RATE_LIMITED"},
        )
    else:
        status = history.record_candidate(job_id, token, result.candidate, receipt)
        if status == "CANDIDATE_READY":
            return history.commit_candidate(job_id)
    return {"job_id": job_id, "status": status}
