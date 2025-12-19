class RuleManager:
    def __init__(self):
        self._rules = []   
    def clear(self):
        self._rules = []

    def add_rule(self, rule):
        self._rules.append(rule)

    def validate(self, numbers):
        for rule in self._rules:
            if not rule.verify(numbers):
                return False, rule.get_description()
        return True, "PASS"

    def get_descriptions(self):
        return [rule.get_description() for rule in self._rules]