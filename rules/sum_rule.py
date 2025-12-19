from rules.rule_base import GameRule


class SumRule(GameRule):
    def __init__(self, min_total: int):
        self.min_total = min_total

    def verify(self, numbers: list[int]) -> bool:
        return sum(numbers) >= self.min_total

    def get_description(self) -> str:
        return f"Sum of digits >= {self.min_total}"
