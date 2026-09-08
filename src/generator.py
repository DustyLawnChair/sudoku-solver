import random

from src.solver import solve_mrv, count_solutions


def generate_full_board():
    board = [[0 for _ in range(9)] for _ in range(9)]

    solve_mrv(board, randomize=True)

    return board


def generate_puzzle(clues=40):
    board = generate_full_board()

    cells = [(row, col) for row in range(9) for col in range(9)]
    random.shuffle(cells)

    current_clues = 81

    for row, col in cells:
        if current_clues <= clues:
            break

        original = board[row][col]

        board[row][col] = 0

        test_board = [row[:] for row in board]

        if count_solutions(test_board) == 1:
            current_clues -= 1
        else:
            board[row][col] = original

    return board