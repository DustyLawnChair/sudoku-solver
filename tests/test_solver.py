import unittest
import copy

from src.solver import (
    is_valid,
    is_valid_board,
    solve_mrv,
    count_solutions
)

from src.generator import (
    generate_puzzle,
    generate_by_difficulty,
    analyze_difficulty
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

    def test_unique_solution(self):
        board = copy.deepcopy(self.board)

        solutions = count_solutions(board)

        self.assertEqual(solutions, 1)

    def test_generated_puzzle_has_unique_solution(self):
        puzzle = generate_puzzle(40)

        solutions = count_solutions(copy.deepcopy(puzzle))

        self.assertEqual(solutions, 1)

    def test_generated_puzzle_has_correct_clue_count(self):
        puzzle = generate_puzzle(40)

        clues = sum(
            1
            for row in puzzle
            for value in row
            if value != 0
        )

        self.assertEqual(clues, 40)

    def test_easy_puzzle(self):
        puzzle = generate_by_difficulty("easy")

        clues = sum(
            1
            for row in puzzle
            for value in row
            if value != 0
        )

        self.assertEqual(clues, 45)


    def test_medium_puzzle(self):
        puzzle = generate_by_difficulty("medium")
        stats = analyze_difficulty(puzzle)

        self.assertGreaterEqual(stats["attempts"], 45)


    def test_hard_puzzle(self):
        puzzle = generate_by_difficulty("hard")
        stats = analyze_difficulty(puzzle)

        self.assertTrue(
            stats["attempts"] >= 60
            or stats["backtracks"] >= 5
        )


if __name__ == "__main__":
    unittest.main()

