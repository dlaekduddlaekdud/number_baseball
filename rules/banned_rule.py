from rules.rule_base import GameRule

class BannedNumberRule(GameRule):
    def __init__(self, banned: list[int]):
        self.banned = set(banned)

    def verify(self, numbers: list[int]) -> bool:
        return len(self.banned & set(numbers)) == 0

    def get_description(self) -> str:
        return f"숫자 {sorted(list(self.banned))}은(는) 사용할 수 없습니다."
