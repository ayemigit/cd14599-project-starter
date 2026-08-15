import random
from abc import ABC, abstractmethod


class QuizMode(ABC):
    def __init__(self, cards):
        self.cards = cards
        self._index = 0

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass


class SequentialMode(QuizMode):
    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self.cards):
            raise StopIteration
        card = self.cards[self._index]
        self._index += 1
        return card


class RandomMode(QuizMode):
    def __iter__(self):
        self._shuffled = random.sample(self.cards, len(self.cards))
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self._shuffled):
            raise StopIteration
        card = self._shuffled[self._index]
        self._index += 1
        return card


class AdaptiveMode(QuizMode):
    def __init__(self, cards):
        super().__init__(cards)
        self._weights = {i: 1.0 for i in range(len(cards))}
        self._queue = list(range(len(cards)))
        self._results = {}

    def record_result(self, card, correct):
        idx = self.cards.index(card)
        if correct:
            self._weights[idx] = max(0.1, self._weights[idx] * 0.5)
        else:
            self._weights[idx] = min(5.0, self._weights[idx] * 2.0)

    def __iter__(self):
        self._queue = list(range(len(self.cards)))
        random.shuffle(self._queue)
        self._pos = 0
        return self

    def __next__(self):
        if self._pos >= len(self._queue):
            raise StopIteration
        indices = list(range(len(self.cards)))
        weights = [self._weights[i] for i in indices]
        chosen = random.choices(indices, weights=weights, k=1)[0]
        self._pos += 1
        return self.cards[chosen]


_REGISTRY = {
    "sequential": SequentialMode,
    "random": RandomMode,
    "adaptive": AdaptiveMode,
}


def quiz_mode_factory(mode_name, cards):
    if mode_name not in _REGISTRY:
        raise ValueError(
            f"Unknown mode '{mode_name}'. Choose from: {list(_REGISTRY.keys())}"
        )
    return _REGISTRY[mode_name](cards)
