import pygame
import sys
import random
import os

from player.human_player import HumanPlayer
from rules.sum_rule import SumRule
from rules.range_limit_rule import RangeLimitRule
from rules.no_consecutive_rule import NoConsecutiveRule
from rules.range_gap_rule import RangeGapRule
from .menu_ui import MainMenuUI


class BaseballGUI:
    def __init__(self, game_manager):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 650))
        pygame.display.set_caption("Number Baseball - OOP & Pygame")
        self.clock = pygame.time.Clock()

        self.gm = game_manager

        self.mode = "single"
        self.rule_mode = "normal"
        self.digit_length = 3

        self.state = "MENU"
        self.input_text = ""
        self.message = ""
        self.winner = ""
        self.answer_setting_player_index = 0

        font_path = os.path.join("fonts", "BlackHanSans-Regular.ttf")
        H = self.screen.get_height()

        self.font_big = pygame.font.Font(font_path, int(H * 0.09))
        self.font_mid = pygame.font.Font(font_path, int(H * 0.055))
        self.font_small = pygame.font.Font(font_path, int(H * 0.035))

        self.font_rule = self.font_small

        pret_path = os.path.join("fonts", "PretendardStd-Regular.otf")
        self.font_rule_symbol = pygame.font.Font(pret_path, int(H * 0.04))

        

        self.NAVY = (10, 42, 102)
        self.RED = (180, 58, 58)
        self.BG = (246, 241, 231)
        self.PINSTRIPE = (230, 223, 210)
        self.WHITE = (255, 255, 255)

        ball_img_path = os.path.join("images", "baseball_watermark.png")
        raw_ball = pygame.image.load(ball_img_path).convert_alpha()

        ball_diameter = int(self.screen.get_height() * 0.70)
        ball_radius = ball_diameter // 2
        self.ball_image = pygame.transform.smoothscale(
            raw_ball, (ball_diameter, ball_diameter)
        )

        ball_center_x = self.screen.get_width() // 2
        ball_center_y = int(self.screen.get_height() * 0.25)
        self.ball_pos = (ball_center_x - ball_radius, ball_center_y - ball_radius)

        self.menu = MainMenuUI(self.screen, self.start_game_from_menu)

    def draw_center(self, text, y, font=None, color=None):
        if font is None:
            font = self.font_mid
        if color is None:
            color = self.Navy
        surf = font.render(text, True, color)
        center_x = self.screen.get_width() // 2
        rect = surf.get_rect(center=(center_x, y))
        self.screen.blit(surf, rect)

    def draw_rule_line(self, text: str, y: int):
        
        tokens = text.split()

        parts = []
        total_width = 0

        space_width = self.font_rule.size(" ")[0]

        for token in tokens:
            if not token:
                continue

            if token in ("<", ">", "<=", ">="):
                font = self.font_rule_symbol
                color = self.RED
            else:
                font = self.font_rule
                color = (40, 40, 40)

            surf = font.render(token, True, color)
            parts.append((surf, font))
            total_width += surf.get_width()

        if len(parts) > 1:
            total_width += space_width * (len(parts) - 1)

        center_x = self.screen.get_width() // 2
        start_x = center_x - total_width // 2

        x = start_x
        for surf, font in parts:
            rect = surf.get_rect(midleft=(x, y))
            self.screen.blit(surf, rect)
            x += surf.get_width() + space_width



    def draw_digit_boxes(self, top_y: int, display_text: str):
        box_w = 70      
        box_h = 80      
        gap   = 12      

        center_x = self.screen.get_width() // 2
        total_w = self.digit_length * box_w + (self.digit_length - 1) * gap
        start_x = center_x - total_w // 2

        for i in range(self.digit_length):
            x = start_x + i * (box_w + gap)
            rect = pygame.Rect(x, top_y, box_w, box_h)

            pygame.draw.rect(self.screen, self.WHITE, rect, border_radius=18)
            pygame.draw.rect(self.screen, self.NAVY, rect, 3, border_radius=18)

            if i < len(display_text):
                ch = display_text[i]
                surf = self.font_big.render(ch, True, self.RED)
                surf_rect = surf.get_rect(center=rect.center)
                self.screen.blit(surf, surf_rect)


    def draw_background(self):
        
        self.screen.fill(self.BG)

        gap = 35
        for x in range(0, self.screen.get_width(), gap):
            pygame.draw.line(
                self.screen,
                self.PINSTRIPE,
                (x, 0),
                (x, self.screen.get_height()),
                1,
            )

        self.screen.blit(self.ball_image, self.ball_pos)

    def draw_set_answer(self):
        
        self.draw_background()

        p = self.answer_setting_player_index + 1
        title = f"PLAYER {p} · SET SECRET NUMBER"
        self.draw_center(title, 90, self.font_mid, self.NAVY)

        sub = f"Enter {self.digit_length}-digit unique number (no duplicate digits)"
        self.draw_center(sub, 140, self.font_small, self.RED)

        if self.input_text:
            masked = "*" * len(self.input_text)
        else:
            masked = ""   

        self.draw_digit_boxes(top_y=185, display_text=masked)

        if self.rule_mode == "rule":
            self.draw_center("ACTIVE RULE", 310, self.font_small, self.NAVY)
            y = 345
            for desc in self.gm.rules.get_descriptions():
                self.draw_rule_line(desc,y)
                y += 26

        if self.message:
            self.draw_center(self.message, 540, self.font_small, (200, 60, 60))

        self.draw_center("Press ENTER to confirm", 600, self.font_small, self.NAVY)



    def draw_game(self):
        
        self.draw_background()

        cur = self.gm.current_player()
        name = cur.name if cur else "?"
        header = f"{name}'s TURN"
        self.draw_center(header, 70, self.font_mid, self.NAVY)

        self.draw_center("CURRENT GUESS", 130, self.font_small, self.NAVY)

        guess_text = self.input_text
        self.draw_digit_boxes(top_y=165, display_text=guess_text)

        if self.message:
            self.draw_center(self.message, 270, self.font_small, (200, 60, 60))

        if self.rule_mode == "rule":
            self.draw_center("ACTIVE RULE", 320, self.font_small, self.NAVY)
            y = 355
            for desc in self.gm.rules.get_descriptions():
                if hasattr(self, "draw_rule_line"):
                    self.draw_rule_line(desc, y)
                else:
                    self.draw_center(desc, y, self.font_small, (40, 40, 40))
                y += 24
            base_y = y + 20
        else:
            base_y = 315

        if self.mode == "single":
            self.draw_center("LAST ATTEMPTS", base_y, self.font_small, self.NAVY)

            panel_w = self.screen.get_width() - 300   
            panel_h = 26 * 5 + 40                     
            panel_x = 150
            panel_y = base_y + 20

            panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            panel_surf.fill((255, 255, 255, 220))
            pygame.draw.rect(panel_surf, self.NAVY, panel_surf.get_rect(),
                             3, border_radius=20)
            self.screen.blit(panel_surf, (panel_x, panel_y))

            y = panel_y + 25
            if cur:
                for att in cur.get_attempts()[-5:]:
                    s, b, o = att.result
                    t = f"{att.guess}  →  {s}S  {b}B  {o}O"
                    self.draw_center(t, y, self.font_small, (0, 0, 0))
                    y += 26

        else:
            players = self.gm.players
            p1 = players[0] if len(players) > 0 else None
            p2 = players[1] if len(players) > 1 else None

            screen_w = self.screen.get_width()

            left_center_x = screen_w * 0.25
            right_center_x = screen_w * 0.75
            title_y = base_y

            txt1 = "PLAYER 1'S LAST ATTEMPTS"
            surf1 = self.font_small.render(txt1, True, self.NAVY)
            rect1 = surf1.get_rect(center=(left_center_x, title_y))
            self.screen.blit(surf1, rect1)

            txt2 = "PLAYER 2'S LAST ATTEMPTS"
            surf2 = self.font_small.render(txt2, True, self.NAVY)
            rect2 = surf2.get_rect(center=(right_center_x, title_y))
            self.screen.blit(surf2, rect2)

            panel_w = int(screen_w * 0.36)
            panel_h = 26 * 5 + 40
            panel_y = base_y + 20

            left_x = int(screen_w * 0.07)
            right_x = screen_w - panel_w - left_x

            left_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            left_surf.fill((255, 255, 255, 220))
            pygame.draw.rect(left_surf, self.NAVY,
                             left_surf.get_rect(), 3, border_radius=20)
            self.screen.blit(left_surf, (left_x, panel_y))

            right_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            right_surf.fill((255, 255, 255, 220))
            pygame.draw.rect(right_surf, self.NAVY,
                             right_surf.get_rect(), 3, border_radius=20)
            self.screen.blit(right_surf, (right_x, panel_y))

            y1 = panel_y + 25
            if p1:
                for att in p1.get_attempts()[-5:]:
                    s, b, o = att.result
                    t = f"{att.guess}  →  {s}S  {b}B  {o}O"
                    center_x = left_x + panel_w // 2
                    surf = self.font_small.render(t, True, (0, 0, 0))
                    rect = surf.get_rect(center=(center_x, y1))
                    self.screen.blit(surf, rect)
                    y1 += 26

            y2 = panel_y + 25
            if p2:
                for att in p2.get_attempts()[-5:]:
                    s, b, o = att.result
                    t = f"{att.guess}  →  {s}S  {b}B  {o}O"
                    center_x = right_x + panel_w // 2
                    surf = self.font_small.render(t, True, (0, 0, 0))
                    rect = surf.get_rect(center=(center_x, y2))
                    self.screen.blit(surf, rect)
                    y2 += 26

        self.draw_center("Type your guess and press ENTER", 610,
                         self.font_small, self.NAVY)






    def draw_result(self):
       
        self.draw_background()

        self.draw_center(f"{self.winner} WINS!", 220, self.font_big, self.RED)

        self.draw_center("Press R to Restart", 340, self.font_small, self.NAVY)
        self.draw_center("Press ESC to Quit", 380, self.font_small, self.NAVY)



    def handle_number_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                return True
            elif event.unicode.isdigit() and len(self.input_text) < self.digit_length:
                self.input_text += event.unicode
        return False

    def run(self):
        while True:
            self.screen.fill(self.BG)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                self.process_state_event(event)

            self.draw_current_screen()
            pygame.display.flip()
            self.clock.tick(60)

    def process_state_event(self, event):
        if self.state == "MENU":
            self.menu.handle_event(event)
        elif self.state in ("SET_P1", "SET_P2"):
            self.process_set_answer_event(event)
        elif self.state == "GAME":
            self.process_game_event(event)
        elif self.state == "RESULT":
            self.process_result_event(event)

    def process_set_answer_event(self, event):
        if self.handle_number_input(event):
            txt = self.input_text

            if not (len(txt) == self.digit_length and txt.isdigit() and len(set(txt)) == self.digit_length):
                self.message = "Invalid number."
                self.input_text = ""
                return

            nums = [int(c) for c in txt]

            if self.rule_mode == "rule":
                valid, msg = self.gm.rules.validate(nums)
                if not valid:
                    self.message = f"Rule violated: {msg}"
                    self.input_text = ""
                    return

            player = self.gm.players[self.answer_setting_player_index]
            self.gm.set_player_answer(player, nums)

            if self.state == "SET_P1":
                self.state = "SET_P2"
                self.answer_setting_player_index = 1
            else:
                self.state = "GAME"

            self.message = ""
            self.input_text = ""

    def process_game_event(self, event):
        if self.handle_number_input(event):
            txt = self.input_text
            if not (len(txt) == self.digit_length and txt.isdigit() and len(set(txt)) == self.digit_length):
                self.message = "Invalid number."
                self.input_text = ""
                return

            guess = [int(c) for c in txt]
            result, winner, error = self.gm.play_turn(guess)

            if error:
                self.message = error
            else:
                s, b, o = result
                self.message = f"{s}S {b}B {o}O"
                if winner:
                    self.winner = winner
                    self.state = "RESULT"

            self.input_text = ""

    def process_result_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.restart_game()

    def draw_current_screen(self):
        if self.state == "MENU":
            self.menu.draw()
        elif self.state in ("SET_P1", "SET_P2"):
            self.draw_set_answer()
        elif self.state == "GAME":
            self.draw_game()
        elif self.state == "RESULT":
            self.draw_result()

    def start_game(self):
        self.gm.rules.clear()

        if self.rule_mode == "rule":
            candidates = [
                SumRule(12 if self.digit_length == 3 else 18),
                RangeLimitRule(min_value=2),
                RangeLimitRule(max_value=7),
                NoConsecutiveRule(),
                RangeGapRule(3),
            ]
            self.gm.rules.add_rule(random.choice(candidates))

        players = [HumanPlayer("Player 1")]
        if self.mode == "multi":
            players.append(HumanPlayer("Player 2"))

        self.gm.start_new_game(players, self.mode, self.digit_length)

        self.input_text = ""
        self.message = ""

        if self.mode == "single":
            self.state = "GAME"
        else:
            self.state = "SET_P1"
            self.answer_setting_player_index = 0

    def start_game_from_menu(self, mode, rule, diff):
        self.mode = "single" if mode == "SINGLE" else "multi"
        self.rule_mode = "normal" if rule == "NORMAL" else "rule"
        self.digit_length = 3 if diff == "EASY" else 4
        self.start_game()

    def restart_game(self):
        self.gm.reset()
        self.state = "MENU"
        self.input_text = ""
        self.message = ""
        self.winner = ""
        self.mode = "single"
        self.rule_mode = "normal"
        self.digit_length = 3

