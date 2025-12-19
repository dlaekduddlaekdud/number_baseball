from rules.rule_base import GameRule

class AllEvenRule(GameRule):
    def verify(self, numbers):
        return all(n % 2 == 0 for n in numbers)

    def get_description(self) -> str:
        return "All digits % 2 == 0"
