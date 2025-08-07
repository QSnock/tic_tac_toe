import pygame
import sys

from gameparts import Board

pygame.init()

CELL_SIZE = 100
BOARD_SIZE = 3
WIDTH = HEIGHT = CELL_SIZE * BOARD_SIZE
LINE_WIDTH = 15
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
X_COLOR = (84, 84, 84)
O_COLOR = (242, 235, 211)
X_WIDTH = 15
O_WIDTH = 15
SPACE = CELL_SIZE // 4

# Цвета для текста
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (52, 152, 219)
BUTTON_HOVER_COLOR = (41, 128, 185)
BUTTON_TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Крестики-нолики')
screen.fill(BG_COLOR)

# Инициализация шрифта
try:
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
except Exception:
    font = pygame.font.SysFont('arial', 36)
    small_font = pygame.font.SysFont('arial', 24)


def draw_lines():
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (0, i * CELL_SIZE),
            (WIDTH, i * CELL_SIZE),
            LINE_WIDTH
        )

    for i in range(1, BOARD_SIZE):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, HEIGHT),
            LINE_WIDTH
        )


def draw_figures(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'X':
                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE),
                    (
                        col * CELL_SIZE + CELL_SIZE - SPACE,
                        row * CELL_SIZE + CELL_SIZE - SPACE
                    ),
                    X_WIDTH
                )
                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (
                        col * CELL_SIZE + SPACE,
                        row * CELL_SIZE + CELL_SIZE - SPACE
                    ),
                    (
                        col * CELL_SIZE + CELL_SIZE - SPACE,
                        row * CELL_SIZE + SPACE
                    ),
                    X_WIDTH
                )
            elif board[row][col] == 'O':
                pygame.draw.circle(
                    screen,
                    O_COLOR,
                    (
                        col * CELL_SIZE + CELL_SIZE // 2,
                        row * CELL_SIZE + CELL_SIZE // 2
                    ),
                    CELL_SIZE // 2 - SPACE,
                    O_WIDTH
                )


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def is_point_in_button(mouse_x, mouse_y, button_x, button_y, button_width,
                       button_height):
    """Проверяет, находится ли точка в пределах кнопки"""
    return (button_x <= mouse_x <= button_x + button_width and
            button_y <= mouse_y <= button_y + button_height)


def is_valid_move(row, col, board):
    """Проверяет, является ли ход валидным"""
    return (0 <= row < BOARD_SIZE and
            0 <= col < BOARD_SIZE and
            board[row][col] == ' ')


def draw_button(text, x, y, width, height, hover=False):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2)

    text_surface = small_font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)


def show_game_result(result):
    """Показывает результат игры и кнопку для новой игры"""
    screen.fill(BG_COLOR)

    draw_text(result, font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 30)

    button_x = WIDTH // 2 - 60
    button_y = HEIGHT // 2 + 20
    button_width = 120
    button_height = 40

    draw_button("Новая игра", button_x, button_y, button_width, button_height)

    pygame.display.update()

    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if is_point_in_button(
                    mouse_x,
                    mouse_y,
                    button_x,
                    button_y,
                    button_width,
                    button_height
                ):
                    waiting_for_click = False
                    return True

            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                hover = is_point_in_button(
                    mouse_x,
                    mouse_y,
                    button_x,
                    button_y,
                    button_width,
                    button_height
                )

                screen.fill(BG_COLOR)
                draw_text(
                    result, font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 30
                )
                draw_button(
                    "Новая игра",
                    button_x,
                    button_y,
                    button_width,
                    button_height,
                    hover
                )
                pygame.display.update()


def save_result(result):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(result + '\n')


def main():
    while True:
        game = Board()
        current_player = 'X'
        running = True
        screen.fill(BG_COLOR)
        draw_lines()
        pygame.display.update()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_y = event.pos[0]
                    mouse_x = event.pos[1]

                    clicked_row = mouse_x // CELL_SIZE
                    clicked_col = mouse_y // CELL_SIZE

                    if is_valid_move(clicked_row, clicked_col, game.board):
                        game.make_move(
                            clicked_row,
                            clicked_col,
                            current_player
                        )

                        if game.check_win(current_player):
                            result = f'Победили {current_player}!'
                            print(result)
                            save_result(result)
                            running = False
                        elif game.is_board_full():
                            result = 'Ничья!'
                            print(result)
                            save_result(result)
                            running = False
                        else:
                            current_player = 'O' if current_player == 'X' else 'X'

                        draw_figures(game.board)

            pygame.display.update()

        if not show_game_result(result):
            break


if __name__ == '__main__':
    main()
