from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, name):
        self._name = name
        self._answer = []
        self._attempts = []

    @property
    def name(self):
        return self._name

    def get_answer(self):
        return self._answer

    def get_attempts(self):
        return self._attempts

    def add_attempt(self, attempt):
        self._attempts.append(attempt)

    @abstractmethod
    def set_answer(self, answer_list):
        pass

    @abstractmethod
    def make_guess(self, guess_list):
        pass
