import pygame
import sys

# 定数
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)

EMPTY = 0
BLACK_STONE = 1
WHITE_STONE = 2

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1),  (1, 0), (1, 1)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")
font = pygame.font.SysFont(None, 48)

def init_board():
    board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
    board[3][3] = WHITE_STONE
    board[3][4] = BLACK_STONE
    board[4][3] = BLACK_STONE
    board[4][4] = WHITE_STONE
    return board

def draw_board(board):
    screen.fill(GREEN)
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, BLACK, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            center = (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2)
            if board[row][col] == BLACK_STONE:
                pygame.draw.circle(screen, BLACK, center, SQUARE_SIZE//2 - 5)
            elif board[row][col] == WHITE_STONE:
                pygame.draw.circle(screen, WHITE, center, SQUARE_SIZE//2 - 5)

def is_on_board(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

def valid_moves(board, color):
    moves = []
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == EMPTY and any(can_flip(board, row, col, color, dr, dc) for dr, dc in DIRECTIONS):
                moves.append((row, col))
    return moves

def can_flip(board, row, col, color, dr, dc):
    opponent = WHITE_STONE if color == BLACK_STONE else BLACK_STONE
    r, c = row + dr, col + dc
    has_opponent_between = False

    while is_on_board(r, c) and board[r][c] == opponent:
        has_opponent_between = True
        r += dr
        c += dc

    if not is_on_board(r, c) or board[r][c] != color:
        return False
    return has_opponent_between

def make_move(board, row, col, color):
    board[row][col] = color
    for dr, dc in DIRECTIONS:
        if can_flip(board, row, col, color, dr, dc):
            flip_stones(board, row, col, color, dr, dc)

def flip_stones(board, row, col, color, dr, dc):
    opponent = WHITE_STONE if color == BLACK_STONE else BLACK_STONE
    r, c = row + dr, col + dc
    while is_on_board(r, c) and board[r][c] == opponent:
        board[r][c] = color
        r += dr
        c += dc

def count_stones(board):
    blacks = sum(row.count(BLACK_STONE) for row in board)
    whites = sum(row.count(WHITE_STONE) for row in board)
    return blacks, whites

def show_result(winner_text):
    text = font.render(winner_text, True, WHITE, BLACK)
    rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    board = init_board()
    current_color = BLACK_STONE

    running = True
    while running:
        draw_board(board)
        pygame.display.flip()

        moves = valid_moves(board, current_color)
        if not moves:
            current_color = WHITE_STONE if current_color == BLACK_STONE else BLACK_STONE
            if not valid_moves(board, current_color):
                blacks, whites = count_stones(board)
                if blacks > whites:
                    show_result("Black won!")
                elif whites > blacks:
                    show_result("White won!")
                else:
                    show_result("Draw!")
                running = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                if (row, col) in moves:
                    make_move(board, row, col, current_color)
                    current_color = WHITE_STONE if current_color == BLACK_STONE else BLACK_STONE

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
