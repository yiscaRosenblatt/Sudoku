import pygame
import sys
from settings import *
import time
from logic import Logic
import random


class Game:
    def __init__(self, difficulty):
        pygame.init()
        self.state = "playing"

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.difficulty = difficulty
        self.font = pygame.font.Font(None, MENE_FONT_SIZE)
        self.font_num = pygame.font.Font(None, 50)
        self.font_notes = pygame.font.Font(None, 25)
        self.font_top_title = pygame.font.Font(None, 25)
        self.font_top = pygame.font.Font(None, 20)
        self.big_font = pygame.font.Font(None, 70)
        self.small_font = pygame.font.Font(None, 30)

        self.mistake = 0
        self.score = 0
        self.elapsed_time = 0

        self.is_notes = False

        self.is_mistake = False

        self.history = []

        self.start_time = time.time()
        self.timer_font = pygame.font.Font(None, 40)

        self.undo = pygame.transform.scale(pygame.image.load(r"C:\Users\yisca\Desktop\Sudoku\pictures\60690.png"), (40, 40))
        self.erase = pygame.transform.scale(pygame.image.load(r"C:\Users\yisca\Desktop\Sudoku\pictures\erase.jpg"), (50, 50))
        self.notes = pygame.transform.scale(pygame.image.load(r"C:\Users\yisca\Desktop\Sudoku\pictures\nootes.png"), (50, 50))
        self.beck = pygame.transform.scale(pygame.image.load(r"C:\Users\yisca\Desktop\Sudoku\pictures\beck.png"), (30, 40))

        self.running = True

        self.cell_size = 60
        self.selected_cell = None

        self.cell_values = [[None for _ in range(9)] for _ in range(9)]
        self.notes_values = [[[] for _ in range(9)] for _ in range(9)]
        self.mistake_cells = [[False for _ in range(9)] for _ in range(9)]

        self.on_off = "off"
        self.color_on_off = GRAY

        self.rect = pygame.Rect(0, 0, self.cell_size, self.cell_size)

        self.given_cells = [[False for _ in range(9)] for _ in range(9)]

        self.logic = Logic()

        self.color = BLACK

        self.run()

    def draw_playing_board(self):
        self.screen.fill(WHITE)

        for row in range(9):
            for col in range(9):
                x = 5 + col * self.cell_size
                y = 110 + row * self.cell_size
                self.rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                if self.selected_cell == (row, col):
                    pygame.draw.rect(self.screen, (0, 255, 0), self.rect, 3)
                else:
                    pygame.draw.rect(self.screen, GRAY, self.rect, 1)

                value = self.cell_values[row][col]
                if value is not None and not self.notes_values[row][col]:
                    # self.check_num()
                    if self.given_cells[row][col]:
                        self.color = BLACK
                    elif self.mistake_cells[row][col]:
                        self.color = RED
                        # self.mistake_cells[row][col] = False
                    else:
                        self.color = BLUE

                    text_surface = self.font_num.render(str(value), True, self.color)
                    text_rect = text_surface.get_rect(center=self.rect.center)
                    self.screen.blit(text_surface, text_rect)

                if self.notes_values[row][col]:
                    for note in self.notes_values[row][col]:
                        note_x = x + ((note - 1) % 3) * 20 + 5
                        note_y = y + ((note - 1) // 3) * 20 + 5
                        note_surface = self.font_notes.render(str(note), True, GRAY)
                        self.screen.blit(note_surface, (note_x, note_y))

        for i in range(0, 10):
            width = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK, (5, 110 + i * self.cell_size), (545, 110 + i * self.cell_size), width)
            pygame.draw.line(self.screen, BLACK, (5 + i * self.cell_size, 110), (5 + i * self.cell_size, 650), width)

        # ציור כפתורים
        self.screen.blit(self.undo, (undo_x, undo_y))
        self.screen.blit(self.erase, (erase_x, erase_y))
        self.screen.blit(self.notes, (notes_x, notes_y))

        self.screen.blit(self.beck, (beck_x, beck_y))

        self.screen.blit(self.font.render("Undo", True, BLACK), (80, 720))
        self.screen.blit(self.font.render("Erase", True, BLACK), (240, 720))
        self.screen.blit(self.font.render("Notes", True, BLACK), (400, 720))

        self.screen.blit(self.font_top_title.render("Difficulty:", True, BLACK), (5, 50))
        self.screen.blit(self.font_top.render(self.difficulty, True, BLACK), (5, 70))

        self.screen.blit(self.font_top_title.render("Mistakes:", True, BLACK), (155, 50))
        self.screen.blit(self.font_top.render(f"{self.mistake}/3", True, BLACK), (155, 70))

        self.screen.blit(self.font_top_title.render("Score:", True, BLACK), (310, 50))
        self.screen.blit(self.font_top.render(f"{self.score}", True, BLACK), (310, 70))

        pygame.draw.rect(self.screen, self.color_on_off, (notes_x + notes_width - 10, notes_y, 30, 20), border_radius=20)
        text = self.font_top.render(self.on_off, True, WHITE)
        text_rect = text.get_rect(center=(notes_x + notes_width - 10 + 30 // 2, notes_y + 20 // 2))
        self.screen.blit(text, text_rect)

        if self.state == "playing":
            self.elapsed_time = int(time.time() - self.start_time)
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        time_string = f"{minutes:02d}:{seconds:02d}"

        self.screen.blit(self.font_top_title.render("Time:", True, BLACK), (460, 50))
        self.screen.blit(self.font_top.render(time_string, True, BLACK), (460, 70))

    def draw_gameover_screen(self):
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(180)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        self.screen.blit(self.big_font.render("Game Over", True, WHITE), (145, 200))
        pygame.draw.rect(self.screen, BLUE, (180, 300, 200, 50),border_radius=20)
        text = self.small_font.render("Back to the menu", True, WHITE)
        text_rect = text.get_rect(center=(180 + 200 // 2, 300 + 50 // 2))
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, BLUE, (180, 380, 200, 50), border_radius=20)
        text = self.small_font.render("Replay", True, WHITE)
        text_rect = text.get_rect(center=(180 + 200 // 2, 380 + 50 // 2))
        self.screen.blit(text, text_rect)

    def handle_mouse_click(self, pos):
        x, y = pos
        if 5 <= x <= 545 and 110 <= y <= 650:
            col = (x - 5) // self.cell_size
            row = (y - 110) // self.cell_size
            self.selected_cell = (row, col)

    def get_cell_color(self, row, col):
        if self.given_cells[row][col]:
            return BLACK
        elif self.mistake_cells[row][col]:
            return RED
        elif self.cell_values[row][col] is not None:
            return BLUE
        else:
            return GRAY

    def handle_keypress(self, event):
        if self.selected_cell and pygame.K_1 <= event.key <= pygame.K_9:
            row, col = self.selected_cell
            number = event.key - pygame.K_0

            if self.given_cells[row][col]:
                return

            if self.is_notes:
                if number in self.notes_values[row][col]:
                    self.notes_values[row][col].remove(number)
                else:
                    self.notes_values[row][col].append(number)
            else:

                # self.check_num()
                prev_value = self.cell_values[row][col]
                prev_color = self.get_cell_color(row, col)
                self.history.append((row, col, prev_value, prev_color))
                self.cell_values[row][col] = number
                self.notes_values[row][col] = []

    def undo_last_move(self):
        print("Current History:", self.history)
        if self.history:
            row, col, current_value, prev_color = self.history.pop()
            self.cell_values[row][col] = None
            if self.history:
                row2, col2, prev_value, prev_color = self.history[-1]
                print(f"Undo: ({row2}, {col2}) -> {prev_value}")
                self.cell_values[row2][col2] = prev_value
                self.mistake_cells[row][col] = (prev_color == RED)

    def erase_num(self):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cell_values[row][col] = None
            if self.given_cells[row][col]:
                return
            self.cell_values[row][col] = None

    def notes_on_off(self):
        self.is_notes = not self.is_notes
        if self.is_notes:
            self.on_off = "on"
            self.color_on_off = BLUE
        else:
            self.on_off = "off"
            self.color_on_off = GRAY

    def show_bord(self):
        logic = Logic()
        count = 0
        used_positions = set()
        numbers = 0
        if self.difficulty == "easy":
            numbers = 30
        if self.difficulty == "medium":
            numbers = 20
        if self.difficulty == "hard":
            numbers = 10

        while count < numbers:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if (row, col) in used_positions:
                continue
            value = logic.new_bord[row][col]
            if value is not None:
                self.cell_values[row][col] = self.logic.new_bord[row][col]
                # self.cell_values[row][col] = value
                self.given_cells[row][col] = True
                used_positions.add((row, col))
                count += 1

                x = 5 + col * self.cell_size
                y = 110 + row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                text_surface = self.font_num.render(str(value), True, BLACK)
                text_rect = text_surface.get_rect(center=rect.center)
                self.screen.blit(text_surface, text_rect)

    def check_num(self, event):
        if self.selected_cell and pygame.K_1 <= event.key <= pygame.K_9 and not self.is_notes:
            row, col = self.selected_cell
            number = event.key - pygame.K_0
            self.cell_values[row][col] = number

            if number == self.logic.new_bord[row][col]:
                self.mistake_cells[row][col] = False
                self.score += 20
            else:
                self.mistake_cells[row][col] = True
                self.mistake += 1
                if self.mistake == 3:
                    self.state = "gameover"
                    self.elapsed_time = int(time.time() - self.start_time)

    def run(self):
        self.show_bord()
        while self.running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if self.state == "gameover":
                    mouse_pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 180 <= mouse_pos[0] <= 380:
                            if 300 <= mouse_pos[1] <= 350:  # Back to the menu
                                from menu import Menu
                                Menu()
                                return
                            elif 380 <= mouse_pos[1] <= 430:  # Replay
                                self.__init__(self.difficulty)
                                return

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if beck_x <= mouse_pos[0] <= beck_x + beck_width and beck_y <= mouse_pos[1] <= beck_y + beck_height:
                        from menu import Menu
                        Menu()
                        return
                    if undo_x <= mouse_pos[0] <= undo_x + undo_width and undo_y <= mouse_pos[1] <= undo_y + undo_height:
                        self.undo_last_move()

                    if erase_x <= mouse_pos[0] <= erase_x + erase_width and erase_y <= mouse_pos[1] <= erase_y + erase_height:
                        self.erase_num()

                    if notes_x <= mouse_pos[0] <= notes_x + notes_width and notes_y <= mouse_pos[1] <= notes_y + notes_height:
                        self.notes_on_off()

                    self.handle_mouse_click(mouse_pos)

                elif event.type == pygame.KEYDOWN:
                    self.check_num(event)
                    self.handle_keypress(event)

            mouse_pos = pygame.mouse.get_pos()
            if self.state == "gameover":
                mouse_pos = pygame.mouse.get_pos()
                if 180 <= mouse_pos[0] <= 380 and (300 <= mouse_pos[1] <= 350 or 380 <= mouse_pos[1] <= 430):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            elif beck_x <= mouse_pos[0] <= beck_x + beck_width and beck_y <= mouse_pos[1] <= beck_y + beck_height or\
                    undo_x <= mouse_pos[0] <= undo_x + undo_width and undo_y <= mouse_pos[1] <= undo_y + undo_height or\
                    erase_x <= mouse_pos[0] <= erase_x + erase_width and erase_y <= mouse_pos[1] <= erase_y + erase_height\
                    or notes_x <= mouse_pos[0] <= notes_x + notes_width and notes_y <= mouse_pos[1] <= notes_y + notes_height:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            self.draw_playing_board()

            if self.state == "gameover":
                self.draw_gameover_screen()
            pygame.display.update()

        pygame.quit()
        sys.exit()
