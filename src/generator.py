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


def generate_by_difficulty(difficulty):
    difficulty = difficulty.lower()

    difficulty_settings = {
        "easy": {
            "clues": 45,
            "min_attempts": 0,
            "min_backtracks": 0
        },
        "medium": {
            "clues": 40,
            "min_attempts": 45,
            "min_backtracks": 0
        },
        "hard": {
            "clues": 35,
            "min_attempts": 60,
            "min_backtracks": 5
        }
    }

    if difficulty not in difficulty_settings:
        raise ValueError("Difficulty must be easy, medium, or hard.")

    settings = difficulty_settings[difficulty]

    while True:
        puzzle = generate_puzzle(settings["clues"])
        stats = analyze_difficulty(puzzle)

        if difficulty == "hard":
            if stats["attempts"] >= 60 or stats["backtracks"] >= 5:
                return puzzle

        elif stats["attempts"] >= settings["min_attempts"]:
            return puzzle

def analyze_difficulty(board):
    test_board = [row[:] for row in board]

    stats = {
        "attempts": 0,
        "backtracks": 0
    }

    solve_mrv(test_board, stats)

    return stats