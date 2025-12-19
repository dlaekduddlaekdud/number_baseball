from rules.rule_base import GameRule

class EvenCountRule(GameRule):
    def __init__(self, count: int):
        self.count = count

    def verify(self, numbers: list[int]) -> bool:
        even_cnt = len([n for n in numbers if n % 2 == 0])
        return even_cnt == self.count

    def get_description(self) -> str:
        return f"짝수가 정확히 {self.count}개 포함되어야 합니다."
