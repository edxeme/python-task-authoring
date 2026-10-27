"""Verifier suite — RED until the ``search`` subcommand is implemented."""

from src.cli import build_parser, search_notes


def test_search_is_case_insensitive():
    notes = ["Deploy FastAPI", "fix flaky test", "FASTAPI retry"]
    assert search_notes(notes, "fastapi") == ["Deploy FastAPI", "FASTAPI retry"]


def test_search_matches_substring():
    notes = ["tune pgvector index", "clean garage"]
    assert search_notes(notes, "vector") == ["tune pgvector index"]


def test_search_no_match_returns_empty():
    assert search_notes(["a", "b"], "zzz") == []


def test_search_empty_term_matches_all():
    assert search_notes(["a", "b"], "") == ["a", "b"]


def test_search_preserves_storage_order():
    notes = ["b match", "a match"]
    assert search_notes(notes, "match") == ["b match", "a match"]


def test_parser_accepts_search_with_term():
    args = build_parser().parse_args(["search", "flaky"])
    assert args.command == "search"
    assert args.term == "flaky"
