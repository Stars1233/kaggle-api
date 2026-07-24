# coding=utf-8
import pytest


def test_search_parser_default_succeeds(parser):
    func, kwargs = parser.dispatch(["search", "weather"])
    assert func.__name__ == "search_cli"
    assert kwargs["query"] == "weather"
    assert kwargs.get("document_type") is None
    assert kwargs.get("mine") is False
    assert kwargs.get("sort_by") is None
    assert kwargs.get("page_size") == 20
    assert kwargs.get("page_token") is None
    assert kwargs.get("csv_display") is False
    assert kwargs.get("output_format") is None


def test_search_parser_with_flags_succeeds(parser):
    func, kwargs = parser.dispatch(
        [
            "search",
            "llm",
            "--type",
            "dataset,model",
            "--mine",
            "--sort-by",
            "votes",
            "--page-size",
            "50",
            "--page-token",
            "tok123",
            "--csv",
        ]
    )
    assert func.__name__ == "search_cli"
    assert kwargs["query"] == "llm"
    assert kwargs["document_type"] == "dataset,model"
    assert kwargs["mine"] is True
    assert kwargs["sort_by"] == "votes"
    assert kwargs["page_size"] == 50
    assert kwargs["page_token"] == "tok123"
    assert kwargs["csv_display"] is True


def test_search_parser_short_flags_succeeds(parser):
    func, kwargs = parser.dispatch(["search", "gemma", "-t", "model", "-m"])
    assert func.__name__ == "search_cli"
    assert kwargs["document_type"] == "model"
    assert kwargs["mine"] is True


def test_search_parser_format_json_succeeds(parser):
    func, kwargs = parser.dispatch(["search", "x", "--format", "json"])
    assert kwargs["output_format"] == "json"


def test_search_parser_requires_query(parser):
    with pytest.raises(SystemExit):
        parser.dispatch(["search"])


def test_search_parser_csv_and_format_mutually_exclusive(parser):
    with pytest.raises(SystemExit):
        parser.dispatch(["search", "x", "--csv", "--format", "json"])
