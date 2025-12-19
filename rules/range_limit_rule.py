from rules.rule_base import GameRule


class RangeLimitRule(GameRule):
    """
    예)
    min_value=2 → 최소값이 2 이상
    max_value=7 → 최대값이 7 이하
    둘 다 넣으면 둘 다 만족해야 함
    """
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def verify(self, numbers: list[int]) -> bool:
        if self.min_value is not None and min(numbers) < self.min_value:
            return False
        if self.max_value is not None and max(numbers) > self.max_value:
            return False
        return True

    def get_description(self) -> str:
        parts = []
        if self.min_value is not None:
            parts.append(f"Min digit ≥ {self.min_value}")
        if self.max_value is not None:
            parts.append(f"Max digit ≤ {self.max_value}")
        return " / ".join(parts) if parts else "Range limit rule"
