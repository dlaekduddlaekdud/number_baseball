from player.player_base import Player


class HumanPlayer(Player):
    def set_answer(self, answer_list):
        self._answer = answer_list

    def make_guess(self, guess_list):
        return guess_list
