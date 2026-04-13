"""Unit tests for the fast-path service."""

from __future__ import annotations

from app.services.fast_path import check_fast_path


def test_fast_path_greetings(sample_greeting_queries: list[str]) -> None:
    for query in sample_greeting_queries:
        result = check_fast_path(query)
        assert result is not None
        assert result.matched is True
        assert result.category == "greeting"
        assert "Hello!" in result.response


def test_fast_path_gratitude(sample_gratitude_queries: list[str]) -> None:
    for query in sample_gratitude_queries:
        result = check_fast_path(query)
        assert result is not None
        assert result.matched is True
        assert result.category == "gratitude"
        assert "welcome" in result.response.lower()


def test_fast_path_farewell(sample_farewell_queries: list[str]) -> None:
    for query in sample_farewell_queries:
        result = check_fast_path(query)
        assert result is not None
        assert result.matched is True
        assert result.category == "farewell"
        assert "Goodbye" in result.response


def test_fast_path_normal_queries(sample_normal_queries: list[str]) -> None:
    for query in sample_normal_queries:
        result = check_fast_path(query)
        assert result is None


def test_fast_path_empty_query() -> None:
    assert check_fast_path("") is None
    assert check_fast_path("   ") is None
    assert check_fast_path("\t\n") is None
