import json
import os
import sys
import tempfile
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.file_handler import load_flashcards
from quiz_engine import quiz_mode_factory


def _write_tmp(data):
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    )
    json.dump(data, f)
    f.close()
    return f.name


CARDS = [
    {"question": "Capital of France?", "answer": "Paris"},
    {"question": "2 + 2?", "answer": "4"},
    {"question": "Color of sky?", "answer": "Blue"},
]


def test_full_session():
    path = _write_tmp(CARDS)
    try:
        cards = load_flashcards(path)
        assert len(cards) == 3

        mode = quiz_mode_factory("sequential", cards)
        results = list(mode)
        assert len(results) == 3
        assert results[0]["answer"] == "Paris"
    finally:
        os.unlink(path)


def test_full_session_random_mode():
    path = _write_tmp(CARDS)
    try:
        cards = load_flashcards(path)
        mode = quiz_mode_factory("random", cards)
        results = list(mode)
        assert len(results) == len(CARDS)
        assert {c["question"] for c in results} == {c["question"] for c in CARDS}
    finally:
        os.unlink(path)


def test_full_session_adaptive_mode():
    path = _write_tmp(CARDS)
    try:
        cards = load_flashcards(path)
        mode = quiz_mode_factory("adaptive", cards)
        results = list(mode)
        assert len(results) == len(CARDS)
    finally:
        os.unlink(path)


def test_full_session_object_format():
    data = {"cards": CARDS}
    path = _write_tmp(data)
    try:
        cards = load_flashcards(path)
        assert len(cards) == 3
        mode = quiz_mode_factory("sequential", cards)
        results = list(mode)
        assert results[1]["answer"] == "4"
    finally:
        os.unlink(path)


def test_full_session_with_data_files():
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    python_file = os.path.join(base, "python_basics.json")
    server_file = os.path.join(base, "server_acronyms.json")

    py_cards = load_flashcards(python_file)
    assert len(py_cards) == 8

    sv_cards = load_flashcards(server_file)
    assert len(sv_cards) == 5
