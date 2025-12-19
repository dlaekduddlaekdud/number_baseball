from core.attempt import Attempt
from core.turn_manager import TurnManager

class GameManager:
    def __init__(self, core, rule_manager):
        self._core = core
        self._rules = rule_manager
        self._players = []
        self._turn = None
        self._game_over = False
        self._winner = None
        self._digit_length = 3
        self._mode = "single"
    
    @property
    def rules(self):
        return self._rules

    @property
    def players(self):
        return self._players
    
    # ================================
    # Getter / Setter (캡슐화 핵심)
    # ================================
    def get_players(self):
        return self._players

    def get_rules(self):
        return self._rules

    def get_digit_length(self):
        return self._digit_length

    def get_winner(self):
        return self._winner

    def is_game_over(self):
        return self._game_over

    def current_player(self):
        return self._turn.current_player() if self._turn else None

    def defender_player(self):
        return self._turn.get_defender() if self._turn else None

    # ================================
    # 게임 설정 관련
    # ================================
    def start_new_game(self, players, mode, digit_length):
        self._players = players
        self._mode = mode
        self._digit_length = digit_length
        self._turn = TurnManager(players)
        self._game_over = False
        self._winner = None

        while True:
            self._core.reset_answer(self._digit_length)
            answer = self._core.get_answer()
            valid, _ = self._rules.validate(answer)
            if valid:
                break

        print("[DEBUG] SECRET ANSWER:", self._core.get_answer())

    def reset(self):
        self._players = []
        self._turn = None
        self._game_over = False
        self._winner = None

    # ================================
    # 플레이어 정답 설정
    # ================================
    def set_player_answer(self, player, answer_list):
        player.set_answer(answer_list)

    # ================================
    # 룰 관리 (캡슐화)
    # ================================
    def clear_rules(self):
        self._rules.clear()

    def add_rule(self, rule):
        self._rules.add_rule(rule)

    # ================================
    # 턴 진행
    # ================================
    def play_turn(self, guess_list):

        if self._game_over:
            return None, self._winner, None

        attacker = self._turn.current_player()
        defender = self._turn.get_defender()

        # 자리수 체크
        if len(guess_list) != self._digit_length:
            return None, None, f"Input {self._digit_length} digits."

        valid, msg = self._rules.validate(guess_list)
        if not valid:
            return None, None, f"Rule violated: {msg}"

        if self._mode == "single":
            answer = self._core.get_answer()
        else:
            answer = defender.get_answer()

        result = self._core.check_guess(answer, guess_list)
        s, b, o = result


        attacker.add_attempt(Attempt(guess_list, result))

        if s == self._digit_length:
            self._game_over = True
            self._winner = attacker.name
            return result, attacker.name, None

        self._turn.next_turn()
        return result, None, None
