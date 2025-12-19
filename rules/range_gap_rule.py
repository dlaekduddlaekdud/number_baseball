from rules.rule_base import GameRule


class RangeGapRule(GameRule):
    """
    max - min >= min_gap
    """
    def __init__(self, min_gap: int):
        self.min_gap = min_gap

    def verify(self, numbers: list[int]) -> bool:
        return (max(numbers) - min(numbers)) >= self.min_gap

    def get_description(self) -> str:
        return f"Max digit - Min digit ≥ {self.min_gap}"
