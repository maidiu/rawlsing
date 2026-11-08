from dataclasses import FrozenInstanceError
import asyncio
import json

import pytest

from rawlsing_next.sorok_history.provider import (
    EndpointModelTransport,
    GRADE_NONE,
    GRADE_RATE_LIMITED,
    GRADE_TERMINAL,
    GRADE_TRANSIENT,
    HistoricalModelProvider,
    LIVE_PROVIDER_NOT_RUN,
    MODE_MOCK,
    MODE_UNAVAILABLE,
    ProviderConfig,
    ProviderPacketError,
    ProviderRateLimited,
    ProviderTerminalError,
    ProviderTransientError,
)


def packet(**overrides):
    value = {
        "schema": "SOROK_HISTORY_ADMISSION_PACKET@1",
        "request_id": "history-request-1",
        "root": "root", "branch": "branch", "time": 1,
        "target_ids": ["target"], "surface": {},
        "known_facts": [], "world_refs": [], "actor_refs": [], "event_refs": [],
        "authority": {}, "chronology": {}, "causal_closure": {},
        "world_readset": "readset", "source_limits": [],
    }
    value.update(overrides)
    return value


def candidate(**overrides):
    value = {
        "request_id": "history-request-1",
        "facts": [{"id": "fact-1", "text": "blue thread crosses the left strap"}],
        "occurrences": [{"id": "occ-1", "kind": "REPAIR"}],
        "links": [],
        "dependencies": [],
        "unknown": {},
    }
    value.update(overrides)
    return value


def run(coro):
    return asyncio.run(coro)


class FakeTransport:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.requests = []
        self.calls = 0

    async def __call__(self, request):
        self.calls += 1
        self.requests.append(request)
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        if callable(outcome):
            return await outcome(request)
        return outcome


def success(text, **extra):
    payload = {"text": text, "model": "actual-model", "usage": {
        "prompt_tokens": 11, "completion_tokens": 7, "total_tokens": 18,
    }}
    payload.update(extra)
    return payload


def test_missing_live_configuration_reports_not_run_without_calling_a_transport():
    provider = HistoricalModelProvider.from_environment({})
    result = run(provider.propose(packet()))

    assert result.ok is False
    assert result.candidate is None
    assert result.receipt.live is False
    assert result.receipt.mode == MODE_UNAVAILABLE
    assert result.receipt.failure_grade == LIVE_PROVIDER_NOT_RUN
    assert result.receipt.failure_code == LIVE_PROVIDER_NOT_RUN
    assert result.receipt.attempt == 0
    assert result.receipt.attempts == 0
    assert result.receipt.provider_identity["live"] is False


def test_injected_mock_success_has_separate_immutable_receipt_and_hashes():
    output = candidate()
    transport = FakeTransport([success(json.dumps(output))])
    provider = HistoricalModelProvider(
        transport=transport,
        endpoint="https://model.example.invalid/v1/chat/completions",
        model="requested-model",
        api_key="SECRET-CREDENTIAL",
        max_output_tokens=100,
    )
    result = run(provider.propose(packet()))

    assert result.ok is True
    assert result.candidate == output
    assert transport.calls == 1
    assert transport.requests[0]["prompt"].count("request_id") >= 1
    for field in ("facts", "occurrences", "links", "dependencies"):
        assert field in transport.requests[0]["prompt"]
    assert transport.requests[0]["max_output_tokens"] == 100
    assert "SECRET-CREDENTIAL" not in json.dumps(transport.requests[0])

    receipt = result.receipt
    assert receipt.live is False
    assert receipt.mode == MODE_MOCK
    assert receipt.failure_grade == GRADE_NONE
    assert receipt.failure_code is None
    assert receipt.status == "CANDIDATE"
    assert receipt.model == "actual-model"
    assert len(receipt.request_hash) == 64
    assert len(receipt.model_hash) == 64
    assert len(receipt.output_hash) == 64
    assert len(receipt.candidate_hash) == 64
    assert receipt.input_tokens == 11
    assert receipt.output_tokens == 7
    assert receipt.total_tokens == 18
    assert receipt.elapsed_ms >= 0
    assert receipt.attempt == 1
    assert receipt.attempts == 1
    assert receipt.writes_world is False
    assert receipt.issues_authority is False
    assert "SECRET-CREDENTIAL" not in json.dumps(receipt.as_dict())

    with pytest.raises(FrozenInstanceError):
        receipt.live = True


def test_packet_validation_refuses_user_text_profile_and_malformed_arrays():
    transport = FakeTransport([success(json.dumps(candidate()))])
    provider = HistoricalModelProvider(transport=transport)
    with pytest.raises(ProviderPacketError, match="user text or profile"):
        run(provider.propose(packet(user_text="private")))
    with pytest.raises(ProviderPacketError, match="unsupported packet fields"):
        run(provider.propose(packet(unexpected={"write": True})))
    with pytest.raises(ProviderPacketError, match="must be an array"):
        run(provider.propose(packet(known_facts={})))
    with pytest.raises(ProviderPacketError, match="missing packet fields"):
        run(provider.propose({"request_id": "history-request-1"}))
    assert transport.calls == 0


def test_strict_json_object_syntax_is_enforced_at_the_transport_boundary():
    fenced = FakeTransport([success("```json\n" + json.dumps(candidate()) + "\n```")])
    fenced_result = run(HistoricalModelProvider(transport=fenced).propose(packet()))
    assert fenced_result.ok is False
    assert fenced_result.receipt.failure_grade == GRADE_TERMINAL
    assert fenced_result.receipt.failure_code == "INVALID_JSON"

    list_result = run(
        HistoricalModelProvider(transport=FakeTransport([success("[]")])).propose(packet())
    )
    assert list_result.ok is False
    assert list_result.receipt.failure_code == "OUTPUT_NOT_OBJECT"

    nan_result = run(
        HistoricalModelProvider(
            transport=FakeTransport([
                success('{"request_id":"history-request-1","facts":[],"occurrences":[],"links":[],"dependencies":[],"x":NaN}')
            ])
        ).propose(packet())
    )
    assert nan_result.ok is False
    assert nan_result.receipt.failure_code == "INVALID_JSON"


def test_semantic_graph_completeness_is_not_owned_by_the_provider():
    minimal = {"request_id": "history-request-1"}
    result = run(
        HistoricalModelProvider(
            transport=FakeTransport([success(json.dumps(minimal))])
        ).propose(packet())
    )
    assert result.ok is True
    assert result.candidate == minimal


def test_rate_limit_and_transient_failures_retry_but_terminal_does_not():
    rate_then_success = FakeTransport([
        ProviderRateLimited("busy", code="HTTP_429"),
        success(json.dumps(candidate())),
    ])
    result = run(
        HistoricalModelProvider(
            transport=rate_then_success, max_attempts=3
        ).propose(packet())
    )
    assert result.ok is True
    assert result.receipt.attempt == 2
    assert result.receipt.attempts == 2
    assert len(rate_then_success.requests) == 2

    transient_then_terminal = FakeTransport([
        ProviderTransientError("temporary", code="HTTP_503"),
        ProviderTerminalError("bad request", code="HTTP_400"),
    ])
    failed = run(
        HistoricalModelProvider(
            transport=transient_then_terminal, max_attempts=3
        ).propose(packet())
    )
    assert failed.ok is False
    assert failed.receipt.failure_grade == GRADE_TERMINAL
    assert failed.receipt.failure_code == "HTTP_400"
    assert failed.receipt.attempt == 2
    assert len(transient_then_terminal.requests) == 2

    exhausted = FakeTransport([ProviderRateLimited("busy") for _ in range(3)])
    exhausted_result = run(
        HistoricalModelProvider(
            transport=exhausted, max_attempts=3
        ).propose(packet())
    )
    assert exhausted_result.ok is False
    assert exhausted_result.receipt.failure_grade == GRADE_RATE_LIMITED
    assert exhausted_result.receipt.attempts == 3
    assert len(exhausted.requests) == 3


def test_timeout_output_and_token_limits_fail_closed():
    async def slow(_request):
        await asyncio.sleep(0.2)
        return success(json.dumps(candidate()))

    timeout_result = run(
        HistoricalModelProvider(
            transport=FakeTransport([slow, slow]),
            timeout_s=0.02,
            max_attempts=2,
        ).propose(packet())
    )
    assert timeout_result.ok is False
    assert timeout_result.receipt.failure_grade == GRADE_TRANSIENT
    assert timeout_result.receipt.failure_code == "TIMEOUT"
    assert timeout_result.receipt.attempts == 2

    oversized = run(
        HistoricalModelProvider(
            transport=FakeTransport([success(json.dumps(candidate(facts=[{"text": "x" * 1000}])))]),
            max_output_chars=256,
        ).propose(packet())
    )
    assert oversized.ok is False
    assert oversized.receipt.failure_code == "OUTPUT_LIMIT_EXCEEDED"

    token_limited = run(
        HistoricalModelProvider(
            transport=FakeTransport([
                success(json.dumps(candidate()), usage={
                    "prompt_tokens": 1, "completion_tokens": 99, "total_tokens": 100,
                })
            ]),
            max_output_tokens=10,
        ).propose(packet())
    )
    assert token_limited.ok is False
    assert token_limited.receipt.failure_code == "OUTPUT_TOKEN_LIMIT_EXCEEDED"


def test_explicit_endpoint_adapter_and_environment_are_not_implicit_live_authority():
    assert EndpointModelTransport.from_environment({}) is None
    configured = EndpointModelTransport.from_environment({
        "SOROK_HISTORY_MODEL_ENDPOINT": "https://model.example.invalid/v1/chat/completions",
        "SOROK_HISTORY_MODEL": "configured-model",
        "SOROK_HISTORY_MODEL_API_KEY": "SECRET-CREDENTIAL",
    })
    assert configured is not None
    assert configured.is_live is True
    assert "SECRET-CREDENTIAL" not in repr(configured)

    provider = HistoricalModelProvider(config=ProviderConfig(
        endpoint="https://model.example.invalid/v1/chat/completions",
        model="configured-model",
        api_key="SECRET-CREDENTIAL",
    ))
    assert provider.live is True
    assert provider.provider_identity["live"] is True
    assert provider.provider_identity["endpoint"].startswith("https://")
    assert "SECRET-CREDENTIAL" not in json.dumps(provider.provider_identity)
    assert provider.config.api_key == "SECRET-CREDENTIAL"


def test_request_id_mismatch_is_terminal_and_does_not_return_the_candidate():
    result = run(
        HistoricalModelProvider(
            transport=FakeTransport([success(json.dumps(candidate(request_id="other")))])
        ).propose(packet())
    )
    assert result.ok is False
    assert result.candidate is None
    assert result.receipt.failure_code == "REQUEST_ID_MISMATCH"
    assert result.receipt.failure_grade == GRADE_TERMINAL


def test_endpoint_response_body_is_bounded_before_parsing(monkeypatch):
    from contextlib import nullcontext

    reads = []

    class Response:
        def read(self, length):
            reads.append(length)
            return b" " * length

    monkeypatch.setattr(
        "rawlsing_next.sorok_history.provider.urllib.request.urlopen",
        lambda *args, **kwargs: nullcontext(Response()),
    )
    provider = HistoricalModelProvider(config=ProviderConfig(
        endpoint="https://model.example.invalid/v1/chat/completions",
        model="configured-model", max_output_chars=100,
    ))

    result = run(provider.propose(packet()))

    assert reads == [6 * 100 + 65_536 + 1]
    assert result.candidate is None
    assert result.receipt.failure_code == "RESPONSE_LIMIT_EXCEEDED"
