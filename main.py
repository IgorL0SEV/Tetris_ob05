# Tetris
import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Определение размеров сетки
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
GREY = (155, 155, 155)

clock = pygame.time.Clock()
fps = 60

# Класс для представления фигур Тетриса
class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.rotation = 0
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0

    def image(self):
        return self.shape[self.rotation % len(self.shape)]

    def rotate(self):
        self.rotation += 1

# Класс для игры
class TetrisGame:
    def __init__(self, screen):
        self.screen = screen
        self.locked_positions = {}
        self.grid = self.create_grid(self.locked_positions)
        self.current_piece = self.get_shape()
        self.next_piece = self.get_shape()
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.score = 0
        self.max_score = 0
        self.change_piece = False
        self.run = True

    def create_grid(self, locked_positions={}):
        grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if (x, y) in locked_positions:
                    color = locked_positions[(x, y)]
                    grid[y][x] = color
        return grid

    def valid_space(self, shape):
        accepted_positions = [(j, i) for i in range(GRID_HEIGHT) for j in range(GRID_WIDTH) if self.grid[i][j] == BLACK]
        formatted_shape = self.convert_shape_format(shape)
        for pos in formatted_shape:
            if pos not in accepted_positions:
                if pos[1] > -1:
                    return False
        return True

    def convert_shape_format(self, shape):
        positions = []
        shape_format = shape.image()
        for i, line in enumerate(shape_format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
        return positions

    def clear_rows(self):
        increment = 0
        for i in range(len(self.grid) - 1, -1, -1):
            row = self.grid[i]
            if BLACK not in row:
                increment += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del self.locked_positions[(j, i)]
                    except:
                        continue
        if increment > 0:
            for key in sorted(list(self.locked_positions), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + increment)
                    self.locked_positions[newKey] = self.locked_positions.pop(key)
        return increment

    def get_shape(self):
        shapes = [
            [['.....', '.....', '..00.', '.00..', '.....'],
             ['.....', '..0..', '..00.', '...0.', '.....']],
            [['.....', '.....', '.00..', '..00.', '.....'],
             ['.....', '..0..', '.00..', '.0...', '.....']],
            [['.....', '..0..', '..0..', '..0..', '..0..'],
             ['.....', '0000.', '.....', '.....', '.....']],
            [['.....', '.....', '.00..', '.00..', '.....']],
            [['.....', '..0..', '.000.', '.....', '.....'],
             ['.....', '..0..', '..00.', '..0..', '.....'],
             ['.....', '.....', '.000.', '..0..', '.....'],
             ['.....', '..0..', '.00..', '..0..', '.....']],
            [['.....', '.0...', '.000.', '.....', '.....'],
             ['.....', '..00.', '..0..', '..0..', '.....'],
             ['.....', '.....', '.000.', '...0.', '.....'],
             ['.....', '..0..', '..0..', '.00..', '.....']],
            [['.....', '...0.', '.000.', '.....', '.....'],
             ['.....', '..0..', '..0..', '..00.', '.....'],
             ['.....', '.....', '.000.', '.0...', '.....'],
             ['.....', '.00..', '..0..', '..0..', '.....']]
        ]
        colors = [CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, MAGENTA]
        return Tetromino(random.choice(shapes), random.choice(colors))

    def draw_window(self):
        self.screen.fill(BLACK)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        pygame.draw.rect(self.screen, RED, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)
        font = pygame.font.SysFont('Arial', 20)
        label = font.render(f'Score: {self.score}', 1, GREEN)
        max_label = font.render(f'Max Score: {self.max_score}', 1, BLUE)
        # Отображение счета
        self.screen.blit(label, (SCREEN_WIDTH - label.get_width() - 10, 10))
        self.screen.blit(max_label, (10, 10))
        pygame.display.update()

    def run_game(self):
        while self.run:
            self.grid = self.create_grid(self.locked_positions)
            fall_speed = 0.27
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            if self.fall_time / 1000 >= fall_speed:
                self.fall_time = 0
                self.current_piece.y += 1
                if not self.valid_space(self.current_piece) and self.current_piece.y > 0:
                    self.current_piece.y -= 1
                    self.change_piece = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece.x -= 1
                        if not self.valid_space(self.current_piece):
                            self.current_piece.x += 1
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece.x += 1
                        if not self.valid_space(self.current_piece):
                            self.current_piece.x -= 1
                    elif event.key == pygame.K_DOWN:
                        self.current_piece.y += 3
                        if not self.valid_space(self.current_piece):
                            self.current_piece.y -= 3
                    elif event.key == pygame.K_UP:
                        self.current_piece.rotate()
                        if not self.valid_space(self.current_piece):
                            self.current_piece.rotation -= 1
                    elif event.key == pygame.K_q:  # Выход из игры
                        pygame.quit()
                        exit()  # Завершение программы

            shape_pos = self.convert_shape_format(self.current_piece)

            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    self.grid[y][x] = self.current_piece.color

            if self.change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    self.locked_positions[p] = self.current_piece.color
                self.current_piece = self.next_piece
                self.next_piece = self.get_shape()
                self.change_piece = False

                self.score += self.clear_rows() * 10

            self.draw_window()  # Обновление окна с текущим счетом

            for pos in self.locked_positions:
                x, y = pos
                if y < 1:
                    self.run = False
                    break

            if self.score > self.max_score:
                self.max_score = self.score

        self.show_game_over()

    def show_game_over(self):
        self.screen.fill(BLACK)
        font = pygame.font.SysFont('Arial bold', 40)
        game_over_label = font.render("Game Over", 1, WHITE)
        font = pygame.font.SysFont('Arial bold', 30)
        score_label = font.render(f'Your Score: {self.score}', 1, GREEN)
        max_score_label = font.render(f'Max Score: {self.max_score}', 1, BLUE)
        font = pygame.font.SysFont('Arial', 20)
        restart_label = font.render("Press R to Restart or Q to Quit", 1, GREY)

        # Центрирование текста
        game_over_rect = game_over_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        score_rect = score_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        max_score_rect = max_score_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        restart_rect = restart_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))

        self.screen.blit(game_over_label, game_over_rect)
        self.screen.blit(score_label, score_rect)
        self.screen.blit(max_score_label, max_score_rect)
        self.screen.blit(restart_label, restart_rect)
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        waiting = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()  # Завершение программы

    def reset_game(self):
        self.locked_positions = {}
        self.grid = self.create_grid(self.locked_positions)
        self.current_piece = self.get_shape()
        self.next_piece = self.get_shape()
        self.score = 0
        self.run = True
        self.run_game()

# Класс для управления меню
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

    def draw_start_menu(self):
        self.screen.fill(BLACK)
        font = pygame.font.SysFont('Arial bold', 60)
        title = font.render("Tetris", 1, WHITE)
        font = pygame.font.SysFont('Arial', 20)
        start_label = font.render("Press SPACE to Start", 1, GREY)

        # Центрирование текста
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        start_rect = start_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.screen.blit(title, title_rect)
        self.screen.blit(start_label, start_rect)
        pygame.display.update()

    def run(self):
        while self.running:
            self.draw_start_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game = TetrisGame(self.screen)
                        game.run_game()

# Запуск игры
if __name__ == '__main__':
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    menu = Menu(screen)
    menu.run()
    pygame.quit()
    clock.tick(fps)
