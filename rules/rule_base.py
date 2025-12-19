from abc import ABC, abstractmethod


class GameRule(ABC):
    @abstractmethod
    def verify(self, numbers: list[int]) -> bool:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


class RuleManager:
    def __init__(self):
        self.rules = []

    def clear(self):
        self.rules = []

    def add_rule(self, rule: GameRule):
        self.rules.append(rule)

    def validate(self, numbers: list[int]):
        """
        모든 룰 통과하면 (True, "PASS")
        하나라도 위반하면 (False, 위반 룰 설명)
        """
        for rule in self.rules:
            if not rule.verify(numbers):
                return False, rule.get_description()
        return True, "PASS"

    def get_descriptions(self):
        return [r.get_description() for r in self.rules]
