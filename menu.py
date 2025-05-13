import pygame
import sys
from settings import *
from game import Game

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sudoku Game")

        self.font = pygame.font.Font(None, FONT_SIZE)
        self.small_font = pygame.font.Font(None, SMALL_FONT_SIZE)

        self.button_x = 170
        self.button_width = 200
        self.button_height = 80
        self.button_y_easy = 410
        self.button_y_medium = 500
        self.button_y_hard = 590

        self.mode = 'menu'
        self.running = True

        self.run()

    def draw_menu(self):
        self.screen.fill(WHITE)
        title = self.font.render("Sudoku Game", True, BLACK)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
        # כפתורים
        pygame.draw.rect(self.screen, BLUE, (self.button_x, self.button_y_easy, self.button_width, self.button_height),border_radius=20)
        pygame.draw.rect(self.screen, BLUE,(self.button_x, self.button_y_medium, self.button_width, self.button_height), border_radius=20)
        pygame.draw.rect(self.screen, BLUE, (self.button_x, self.button_y_hard, self.button_width, self.button_height),border_radius=20)

        # טקסטים על הכפתורים
        text = self.small_font.render("Easy", True, WHITE)
        text_rect = text.get_rect(center=(self.button_x + self.button_width // 2, self.button_y_easy + self.button_height // 2))
        self.screen.blit(text, text_rect)

        text = self.small_font.render("Medium", True, WHITE)
        text_rect = text.get_rect(center=(self.button_x + self.button_width // 2, self.button_y_medium + self.button_height // 2))
        self.screen.blit(text, text_rect)

        text = self.small_font.render("Hard", True, WHITE)
        text_rect = text.get_rect(center=(self.button_x + self.button_width // 2, self.button_y_hard + self.button_height // 2))
        self.screen.blit(text, text_rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            if self.mode == 'menu':
                self.draw_menu()

                if self.button_x <= mouse_pos[0] <= self.button_x + self.button_width:
                    if self.button_y_easy <= mouse_pos[1] <= self.button_y_easy + self.button_height or \
                            self.button_y_medium <= mouse_pos[1] <= self.button_y_medium + self.button_height or \
                            self.button_y_hard <= mouse_pos[1] <= self.button_y_hard + self.button_height:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if mouse_click[0]:
                    difficulty = self.get_difficulty_clicked(mouse_pos)
                    if difficulty:
                        print(f"Starting {difficulty} game...")
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        Game(difficulty)

            pygame.display.update()

        pygame.quit()
        sys.exit()

    def get_difficulty_clicked(self, mouse_pos):
        if self.button_x <= mouse_pos[0] <= self.button_x + self.button_width:
            if self.button_y_easy <= mouse_pos[1] <= self.button_y_easy + self.button_height:
                return "easy"
            if self.button_y_medium <= mouse_pos[1] <= self.button_y_medium + self.button_height:
                return "medium"
            if self.button_y_hard <= mouse_pos[1] <= self.button_y_hard + self.button_height:
                return "hard"

        return None