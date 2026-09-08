import random

from src.solver import solve_mrv


def generate_full_board():
    board = [[0 for _ in range(9)] for _ in range(9)]

    solve_mrv(board, randomize=True)

    return board