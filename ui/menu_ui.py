import pygame
import os


class MainMenuUI:
    def __init__(self, screen, start_callback):
        self.screen = screen
        self.start_callback = start_callback

        self.WIDTH, self.HEIGHT = self.screen.get_size()
        self.FPS = 60

        self.NAVY = (10, 42, 102)
        self.RED = (180, 58, 58)
        self.BG = (246, 241, 231)
        self.PINSTRIPE = (230, 223, 210)
        self.WHITE = (255, 255, 255)
        self.DARK_RED = (150, 40, 40)

        self.font_title = self.load_font(int(self.HEIGHT * 0.17))
        self.font_sub = self.load_font(int(self.HEIGHT * 0.038))
        self.font_label = self.load_font(int(self.HEIGHT * 0.04))
        self.font_btn = self.load_font(int(self.HEIGHT * 0.045))

        self.ball_image, self.ball_pos = self.load_ball_image()

        self.selected_mode = "SINGLE"
        self.selected_rule = "NORMAL"
        self.selected_diff = "EASY"

        self.init_buttons()

    def load_font(self, size: int) -> pygame.font.Font:
        
        font_path = os.path.join("fonts", "BlackHanSans-Regular.ttf")
        return pygame.font.Font(font_path, size)

    def load_ball_image(self):
        
        img_path = os.path.join("images", "baseball_watermark.png")
        raw_ball = pygame.image.load(img_path).convert_alpha()

        ball_diameter = int(self.HEIGHT * 0.70)
        ball_radius = ball_diameter // 2
        ball_image = pygame.transform.smoothscale(raw_ball, (ball_diameter, ball_diameter))

        ball_center_x = self.WIDTH // 2
        ball_center_y = int(self.HEIGHT * 0.25)
        ball_pos = (ball_center_x - ball_radius, ball_center_y - ball_radius)

        return ball_image, ball_pos

    def init_buttons(self):
        
        self.BUTTON_W = 180
        self.BUTTON_H = 62
        self.BUTTON_GAP_X = 70

        self.left_x1 = 80
        self.left_x2 = self.left_x1 + self.BUTTON_W + self.BUTTON_GAP_X

        label_gap = 6

        self.row_mode_y = int(self.HEIGHT * 0.50)
        self.row_rule_y = int(self.HEIGHT * 0.67)
        self.row_diff_y = int(self.HEIGHT * 0.86)

        self.rect_mode_single = pygame.Rect(
            self.left_x1, self.row_mode_y + label_gap, self.BUTTON_W, self.BUTTON_H
        )
        self.rect_mode_multi = pygame.Rect(
            self.left_x2, self.row_mode_y + label_gap, self.BUTTON_W, self.BUTTON_H
        )

        self.rect_rule_normal = pygame.Rect(
            self.left_x1, self.row_rule_y + label_gap, self.BUTTON_W, self.BUTTON_H
        )
        self.rect_rule_rulecard = pygame.Rect(
            self.left_x2, self.row_rule_y + label_gap, self.BUTTON_W, self.BUTTON_H
        )

        self.rect_diff_easy = pygame.Rect(
            self.left_x1, self.row_diff_y + label_gap, self.BUTTON_W, self.BUTTON_H
        )
        self.rect_diff_hard = pygame.Rect(
            self.left_x2, self.row_diff_y + label_gap, self.BUTTON_W, self.BUTTON_H
        )

        start_w, start_h = 220, 90
        self.rect_start = pygame.Rect(
            self.WIDTH - start_w - 70,
            int(self.HEIGHT * 0.64),
            start_w,
            start_h,
        )

    def draw_pinstripes(self):
        
        self.screen.fill(self.BG)
        gap = 35
        for x in range(0, self.WIDTH, gap):
            pygame.draw.line(self.screen, self.PINSTRIPE, (x, 0), (x, self.HEIGHT), 1)

    def draw_option_button(self, rect, text, selected, mouse_pos):
        
        is_hover = rect.collidepoint(mouse_pos)

        if selected:
            body = self.NAVY
            border = self.DARK_RED
            text_color = self.WHITE
        else:
            body = self.WHITE
            border = self.NAVY
            text_color = self.NAVY

        if is_hover and not selected:
            body = (235, 235, 235)

        pygame.draw.rect(self.screen, body, rect, border_radius=20)
        pygame.draw.rect(self.screen, border, rect, 3, border_radius=20)

        label = self.font_btn.render(text, True, text_color)
        self.screen.blit(label, label.get_rect(center=rect.center))

    def draw_start_button(self, mouse_pos):
        
        is_hover = self.rect_start.collidepoint(mouse_pos)
        body = self.NAVY if not is_hover else (20, 60, 130)

        pygame.draw.rect(self.screen, body, self.rect_start, border_radius=25)
        pygame.draw.rect(self.screen, self.RED, self.rect_start, 4, border_radius=25)

        label1 = self.font_btn.render("START", True, self.WHITE)
        label2 = self.font_btn.render("GAME", True, self.WHITE)

        label1_rect = label1.get_rect(
            center=(self.rect_start.centerx, self.rect_start.centery - 12)
        )
        label2_rect = label2.get_rect(
            center=(self.rect_start.centerx, self.rect_start.centery + 16)
        )
        self.screen.blit(label1, label1_rect)
        self.screen.blit(label2, label2_rect)

    def draw(self):
        
        mouse_pos = pygame.mouse.get_pos()

        self.draw_pinstripes()
        self.screen.blit(self.ball_image, self.ball_pos)

        title1 = self.font_title.render("NUMBER", True, self.NAVY)
        title2 = self.font_title.render("BASEBALL", True, self.NAVY)
        self.screen.blit(
            title1,
            title1.get_rect(center=(self.WIDTH / 2, self.HEIGHT * 0.17)),
        )
        self.screen.blit(
            title2,
            title2.get_rect(center=(self.WIDTH / 2, self.HEIGHT * 0.32)),
        )

        sub = self.font_sub.render("Guess the random digit number!", True, self.RED)
        self.screen.blit(
            sub,
            sub.get_rect(center=(self.WIDTH / 2, self.HEIGHT * 0.40)),
        )

        mode_label = self.font_label.render("MODE", True, self.NAVY)
        rule_label = self.font_label.render("RULE", True, self.NAVY)
        diff_label = self.font_label.render("DIFFICULTY", True, self.NAVY)

        mode_center_x = (self.rect_mode_single.right + self.rect_mode_multi.left) // 2
        rule_center_x = (self.rect_rule_normal.right + self.rect_rule_rulecard.left) // 2
        diff_center_x = (self.rect_diff_easy.right + self.rect_diff_hard.left) // 2

        self.screen.blit(
            mode_label,
            mode_label.get_rect(center=(mode_center_x, self.row_mode_y - 13)),
        )
        self.screen.blit(
            rule_label,
            rule_label.get_rect(center=(rule_center_x, self.row_rule_y - 13)),
        )
        self.screen.blit(
            diff_label,
            diff_label.get_rect(center=(diff_center_x, self.row_diff_y - 13)),
        )

        self.draw_option_button(
            self.rect_mode_single, "SINGLE", self.selected_mode == "SINGLE", mouse_pos
        )
        self.draw_option_button(
            self.rect_mode_multi, "MULTI", self.selected_mode == "MULTI", mouse_pos
        )

        self.draw_option_button(
            self.rect_rule_normal,
            "NORMAL",
            self.selected_rule == "NORMAL",
            mouse_pos,
        )
        self.draw_option_button(
            self.rect_rule_rulecard,
            "RULE CARD",
            self.selected_rule == "RULE CARD",
            mouse_pos,
        )

        self.draw_option_button(
            self.rect_diff_easy, "EASY", self.selected_diff == "EASY", mouse_pos
        )
        self.draw_option_button(
            self.rect_diff_hard, "HARD", self.selected_diff == "HARD", mouse_pos
        )

        # START 버튼
        self.draw_start_button(mouse_pos)

    def handle_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect_mode_single.collidepoint(event.pos):
                self.selected_mode = "SINGLE"

            elif self.rect_mode_multi.collidepoint(event.pos):
                self.selected_mode = "MULTI"

            elif self.rect_rule_normal.collidepoint(event.pos):
                self.selected_rule = "NORMAL"

            elif self.rect_rule_rulecard.collidepoint(event.pos):
                self.selected_rule = "RULE CARD"

            elif self.rect_diff_easy.collidepoint(event.pos):
                self.selected_diff = "EASY"

            elif self.rect_diff_hard.collidepoint(event.pos):
                self.selected_diff = "HARD"

            elif self.rect_start.collidepoint(event.pos):
                self.start_callback(
                    self.selected_mode, 
                    self.selected_rule, 
                    self.selected_diff,)
