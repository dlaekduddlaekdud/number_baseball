from core.baseball_core import BaseballCore
from rules.rule_base import RuleManager
from game_manager import GameManager
from ui.pygame_gui import BaseballGUI


if __name__ == "__main__":
    core = BaseballCore(digit_length=3)
    rule_manager = RuleManager()
    gm = GameManager(core, rule_manager)

    app = BaseballGUI(gm)
    app.run()
