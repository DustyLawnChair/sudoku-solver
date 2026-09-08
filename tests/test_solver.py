import unittest
import copy

from src.solver import (
    is_valid,
    is_valid_board,
    solve_mrv
)


class TestSudokuSolver(unittest.TestCase):

    def setUp(self):
        self.board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],

            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],

            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

    def test_valid_move(self):
        self.assertTrue(is_valid(self.board, 4, 0, 2))

    def test_invalid_move(self):
        self.assertFalse(is_valid(self.board, 5, 0, 2))

    def test_valid_board(self):
        self.assertTrue(is_valid_board(self.board))

    def test_invalid_board(self):
        invalid_board = copy.deepcopy(self.board)
        invalid_board[0][1] = 5

        self.assertFalse(is_valid_board(invalid_board))

    def test_solver(self):
        stats = {
            "attempts": 0,
            "backtracks": 0
        }

        solved = solve_mrv(self.board, stats)

        self.assertTrue(solved)

        for row in self.board:
            self.assertNotIn(0, row)


if __name__ == "__main__":
    unittest.main()