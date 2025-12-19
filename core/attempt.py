class Attempt:
    def __init__(self, guess, result):
        """
        guess : [int, int, ...]
        result: (S, B, O)
        """
        self.guess = guess
        self.result = result

    def __repr__(self):
        s, b, o = self.result
        return f"{self.guess} -> {s}S {b}B {o}O"
