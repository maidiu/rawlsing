"""Opt-in runtime context for adopted PRE553 successor contracts.

Legacy PRE553 callers never create this context and therefore retain the
accepted execution path. Runtime-authorized callers bind one exact immutable
authority set for the duration of one synchronous evaluation.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Iterator

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import AuthorityRef
from rawlsing_next.pre553_runtime_authority import Pre553RuntimeAuthoritySet


@dataclass(frozen=True)
class RuntimeBinding:
    authorities: Pre553RuntimeAuthoritySet
    repository: C11Repository | None
    predicate_grammar_authority_ref: AuthorityRef | None
    runtime_catalog_identity: str | None


_CURRENT: ContextVar[RuntimeBinding | None] = ContextVar(
    "pre553_runtime_binding", default=None
)


@contextmanager
def bind_runtime(
    authorities: Pre553RuntimeAuthoritySet,
    *,
    repository: C11Repository | None = None,
    predicate_grammar_authority_ref: AuthorityRef | None = None,
    runtime_catalog_identity: str | None = None,
) -> Iterator[RuntimeBinding]:
    if not isinstance(authorities, Pre553RuntimeAuthoritySet):
        raise TypeError("authorities must be exact Pre553RuntimeAuthoritySet")
    if repository is not None and not isinstance(repository, C11Repository):
        raise TypeError("repository must be exact C11Repository")
    if runtime_catalog_identity is not None:
        if (
            not isinstance(runtime_catalog_identity, str)
            or len(runtime_catalog_identity) != 64
            or any(ch not in "0123456789abcdef" for ch in runtime_catalog_identity)
        ):
            raise TypeError("runtime_catalog_identity must be an exact lowercase sha256")
    binding = RuntimeBinding(
        authorities=authorities,
        repository=repository,
        predicate_grammar_authority_ref=predicate_grammar_authority_ref,
        runtime_catalog_identity=runtime_catalog_identity,
    )
    token = _CURRENT.set(binding)
    try:
        yield binding
    finally:
        _CURRENT.reset(token)


def current_runtime_binding() -> RuntimeBinding | None:
    return _CURRENT.get()


def current_runtime_authorities() -> Pre553RuntimeAuthoritySet | None:
    binding = _CURRENT.get()
    return None if binding is None else binding.authorities


def execute_empirical_query_runtime(
    *,
    runtime_authorities,
    runtime_catalog_identity: str | None = None,
    **kwargs,
):
    from rawlsing_next.pre553_empirical_query import execute_empirical_query

    predicate = kwargs.get("predicate")
    repository = kwargs.get("repository")
    grammar_ref = None if predicate is None else predicate.grammar_authority_ref
    with bind_runtime(
        runtime_authorities,
        repository=repository,
        predicate_grammar_authority_ref=grammar_ref,
        runtime_catalog_identity=runtime_catalog_identity,
    ):
        return execute_empirical_query(**kwargs)


def execute_empirical_query_current_runtime(**kwargs):
    binding = current_runtime_binding()
    if binding is None:
        from rawlsing_next.pre553_empirical_query import execute_empirical_query
        return execute_empirical_query(**kwargs)
    return execute_empirical_query_runtime(
        runtime_authorities=binding.authorities,
        runtime_catalog_identity=binding.runtime_catalog_identity,
        **kwargs,
    )


def execute_exact_bounded_discovery_runtime(
    *,
    runtime_authorities,
    runtime_catalog_identity: str | None = None,
    **kwargs,
):
    from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery

    with bind_runtime(
        runtime_authorities,
        repository=kwargs.get("repository"),
        runtime_catalog_identity=runtime_catalog_identity,
    ):
        return execute_exact_bounded_discovery(**kwargs)


__all__ = [
    "RuntimeBinding",
    "bind_runtime",
    "current_runtime_authorities",
    "current_runtime_binding",
    "execute_empirical_query_current_runtime",
    "execute_empirical_query_runtime",
    "execute_exact_bounded_discovery_runtime",
]
