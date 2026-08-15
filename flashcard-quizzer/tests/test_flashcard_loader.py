import json
import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.file_handler import load_flashcards


def _write_tmp(data):
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    )
    json.dump(data, f)
    f.close()
    return f.name


def test_load_valid_flashcards_array():
    cards = [
        {"question": "What is Python?", "answer": "A programming language"},
        {"question": "What is a list?", "answer": "An ordered collection"},
    ]
    path = _write_tmp(cards)
    try:
        result = load_flashcards(path)
        assert len(result) == 2
        assert result[0]["question"] == "What is Python?"
    finally:
        os.unlink(path)


def test_load_valid_flashcards_object_format():
    data = {
        "cards": [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
        ]
    }
    path = _write_tmp(data)
    try:
        result = load_flashcards(path)
        assert len(result) == 2
        assert result[1]["answer"] == "A2"
    finally:
        os.unlink(path)


def test_load_invalid_json():
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    )
    f.write("{ this is not valid json }")
    f.close()
    try:
        with pytest.raises(SystemExit):
            load_flashcards(f.name)
    finally:
        os.unlink(f.name)


def test_load_missing_required_field():
    cards = [
        {"question": "No answer field here"},
    ]
    path = _write_tmp(cards)
    try:
        with pytest.raises(SystemExit):
            load_flashcards(path)
    finally:
        os.unlink(path)


def test_load_file_not_found():
    with pytest.raises(SystemExit):
        load_flashcards("/nonexistent/path/cards.json")


def test_load_front_back_format():
    cards = [{"front": "Hello", "back": "World"}]
    path = _write_tmp(cards)
    try:
        result = load_flashcards(path)
        assert result[0]["front"] == "Hello"
    finally:
        os.unlink(path)
