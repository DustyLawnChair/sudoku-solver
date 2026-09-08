import tkinter as tk
from tkinter import ttk
import time

from src.solver import solve_mrv, is_valid_board
from src.generator import generate_by_difficulty


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.resizable(False, False)

        self.cells = []

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="SUDOKU SOLVER",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(15, 10))

        grid_frame = tk.Frame(self.root)
        grid_frame.pack(padx=15, pady=5)

        for row in range(9):
            row_cells = []

            for col in range(9):
                cell = tk.Entry(
                    grid_frame,
                    width=2,
                    font=("Arial", 18),
                    justify="center"
                )

                padx = (2, 8) if col in (2, 5) else (2, 2)
                pady = (2, 8) if row in (2, 5) else (2, 2)

                cell.grid(
                    row=row,
                    column=col,
                    padx=padx,
                    pady=pady,
                    ipady=5
                )

                row_cells.append(cell)

            self.cells.append(row_cells)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        solve_button = tk.Button(
            button_frame,
            text="Solve",
            width=10,
            command=self.solve_puzzle
        )
        solve_button.grid(row=0, column=0, padx=5)

        generate_button = tk.Button(
            button_frame,
            text="Generate",
            width=10,
            command=self.generate_puzzle
        )
        generate_button.grid(row=0, column=1, padx=5)

        clear_button = tk.Button(
            button_frame,
            text="Clear",
            width=10,
            command=self.clear_board
        )
        clear_button.grid(row=0, column=2, padx=5)

        self.status_label = tk.Label(
            self.root,
            text="Enter a puzzle or generate one.",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=(0, 5))

        self.stats_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 9)
        )
        self.stats_label.pack(pady=(0, 15))

    def get_board(self):
        board = []

        for row in range(9):
            board_row = []

            for col in range(9):
                value = self.cells[row][col].get().strip()

                if value == "":
                    board_row.append(0)

                elif value.isdigit() and 1 <= int(value) <= 9:
                    board_row.append(int(value))

                else:
                    return None

            board.append(board_row)

        return board

    def display_board(self, board):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].delete(0, tk.END)

                if board[row][col] != 0:
                    self.cells[row][col].insert(0, board[row][col])

    def clear_board(self):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].delete(0, tk.END)

        self.status_label.config(text="Board cleared.")
        self.stats_label.config(text="")

    def solve_puzzle(self):
        board = self.get_board()

        if board is None:
            self.status_label.config(
                text="Invalid input. Use numbers 1-9."
            )
            return

        if not is_valid_board(board):
            self.status_label.config(
                text="Invalid Sudoku puzzle."
            )
            return

        stats = {
            "attempts": 0,
            "backtracks": 0
        }

        start_time = time.perf_counter()

        solved = solve_mrv(board, stats)

        end_time = time.perf_counter()

        if solved:
            self.display_board(board)

            self.status_label.config(
                text="Solved!"
            )

            self.stats_label.config(
                text=(
                    f"Attempts: {stats['attempts']}    "
                    f"Backtracks: {stats['backtracks']}    "
                    f"Time: {end_time - start_time:.6f} seconds"
                )
            )

        else:
            self.status_label.config(
                text="This Sudoku puzzle has no solution."
            )

            self.stats_label.config(
                text=(
                    f"Attempts: {stats['attempts']}    "
                    f"Backtracks: {stats['backtracks']}    "
                    f"Time: {end_time - start_time:.6f} seconds"
                )
            )

    def generate_puzzle(self):
        difficulty = "hard"

        self.status_label.config(
            text=f"Generating {difficulty} puzzle..."
        )

        self.root.update_idletasks()

        board = generate_by_difficulty(difficulty)

        self.display_board(board)

        self.status_label.config(
            text=f"{difficulty.capitalize()} puzzle generated."
        )

        self.stats_label.config(text="")


root = tk.Tk()
app = SudokuGUI(root)
root.mainloop()