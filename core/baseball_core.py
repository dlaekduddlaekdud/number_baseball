import random


class BaseballCore:
    def __init__(self, digit_length=3):
        self.digit_length = digit_length
        self._answer = self._generate_answer()

    def _generate_answer(self):
        # 0~9 중 중복 없는 digit_length개
        return random.sample(range(10), self.digit_length)

    def reset_answer(self, digit_length=None):
        if digit_length is not None:
            self.digit_length = digit_length
        self._answer = self._generate_answer()

    def set_answer(self, answer_list):
        """싱글모드에서 룰을 만족하는 정답을 직접 세팅할 때 사용"""
        self._answer = answer_list

    def check_guess(self, answer, guess):
        """
        answer, guess: [int, int, ...]
        결과: (S, B, O)
        """
        s = 0
        b = 0
        for i, g in enumerate(guess):
            if g == answer[i]:
                s += 1
            elif g in answer:
                b += 1
        o = self.digit_length - (s + b)
        return (s, b, o)

    def get_answer(self):
        return self._answer
