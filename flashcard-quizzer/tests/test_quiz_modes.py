import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from quiz_engine import (
    quiz_mode_factory,
    SequentialMode,
    RandomMode,
    AdaptiveMode,
)

SAMPLE_CARDS = [
    {"question": f"Q{i}", "answer": f"A{i}"} for i in range(5)
]


def test_quiz_mode_factory_sequential():
    mode = quiz_mode_factory("sequential", SAMPLE_CARDS)
    assert isinstance(mode, SequentialMode)


def test_quiz_mode_factory_random():
    mode = quiz_mode_factory("random", SAMPLE_CARDS)
    assert isinstance(mode, RandomMode)


def test_quiz_mode_factory_adaptive():
    mode = quiz_mode_factory("adaptive", SAMPLE_CARDS)
    assert isinstance(mode, AdaptiveMode)


def test_quiz_mode_factory_invalid():
    with pytest.raises(ValueError):
        quiz_mode_factory("nonexistent", SAMPLE_CARDS)


def test_sequential_mode_order():
    mode = quiz_mode_factory("sequential", SAMPLE_CARDS)
    results = list(mode)
    assert results == SAMPLE_CARDS


def test_random_mode_returns_all_cards():
    mode = quiz_mode_factory("random", SAMPLE_CARDS)
    results = list(mode)
    assert len(results) == len(SAMPLE_CARDS)
    assert set(c["question"] for c in results) == set(
        c["question"] for c in SAMPLE_CARDS
    )


def test_adaptive_mode_behavior():
    cards = [{"question": f"Q{i}", "answer": f"A{i}"} for i in range(3)]
    mode = quiz_mode_factory("adaptive", cards)

    initial_weight = mode._weights[0]
    mode.record_result(cards[0], correct=False)
    assert mode._weights[0] > initial_weight

    mode.record_result(cards[0], correct=True)
    assert mode._weights[0] < mode._weights[0] * 2


def test_adaptive_mode_weight_bounds():
    cards = [{"question": "Q", "answer": "A"}]
    mode = quiz_mode_factory("adaptive", cards)
    for _ in range(20):
        mode.record_result(cards[0], correct=False)
    assert mode._weights[0] <= 5.0

    for _ in range(20):
        mode.record_result(cards[0], correct=True)
    assert mode._weights[0] >= 0.1


def test_adaptive_mode_iterates():
    mode = quiz_mode_factory("adaptive", SAMPLE_CARDS)
    results = list(mode)
    assert len(results) == len(SAMPLE_CARDS)
