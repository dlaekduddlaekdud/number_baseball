class TurnManager:
    def __init__(self, players):
        self.players = players
        self.index = 0  # 현재 공격수 인덱스

    def current_player(self):
        return self.players[self.index]

    def get_defender(self):
        defender_idx = (self.index + 1) % len(self.players)
        return self.players[defender_idx]

    def next_turn(self):
        self.index = (self.index + 1) % len(self.players)
