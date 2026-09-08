import time
import tkinter as tk
from tkinter import ttk

from src.solver import solve_mrv, is_valid_board
from src.generator import generate_by_difficulty


class SudokuGUI:
    BG = "#111111"
    PANEL = "#1a1a1a"
    CELL = "#202020"
    CELL_HOVER = "#292929"
    BOX_BORDER = "#777777"

    ACCENT = "#00ff88"
    PURPLE = "#9b59ff"
    TEXT = "#eeeeee"
    MUTED = "#888888"
    ERROR = "#ff5c5c"

    def __init__(self, root):
        self.root = root

        self.root.title("Sudoku Solver")
        self.root.configure(bg=self.BG)
        self.root.resizable(False, False)

        self.cells = []
        self.original_cells = set()

        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(
            self.root,
            bg=self.BG
        )
        main_frame.pack(
            padx=30,
            pady=25
        )

        title = tk.Label(
            main_frame,
            text="SUDOKU SOLVER",
            bg=self.BG,
            fg=self.ACCENT,
            font=("Consolas", 24, "bold")
        )
        title.pack()

        subtitle = tk.Label(
            main_frame,
            text="MRV + BACKTRACKING ENGINE",
            bg=self.BG,
            fg=self.MUTED,
            font=("Consolas", 10)
        )
        subtitle.pack(pady=(2, 20))

        # Sudoku board
        board_frame = tk.Frame(
            main_frame,
            bg=self.BOX_BORDER
        )
        board_frame.pack()

        for box_row in range(3):
            box_row_frame = tk.Frame(
                board_frame,
                bg=self.BOX_BORDER
            )
            box_row_frame.grid(
                row=box_row,
                column=0,
                pady=(0 if box_row == 0 else 3)
            )

            for box_col in range(3):
                box_frame = tk.Frame(
                    box_row_frame,
                    bg=self.BOX_BORDER
                )
                box_frame.grid(
                    row=0,
                    column=box_col,
                    padx=(0 if box_col == 0 else 3)
                )

                for cell_row in range(3):
                    actual_row = box_row * 3 + cell_row

                    for cell_col in range(3):
                        actual_col = box_col * 3 + cell_col

                        validate_command = (
                            self.root.register(
                                self.validate_input
                            )
                        )

                        cell = tk.Entry(
                            box_frame,
                            width=2,
                            bg=self.CELL,
                            fg=self.TEXT,
                            insertbackground=self.ACCENT,
                            relief="flat",
                            bd=0,
                            font=("Consolas", 18, "bold"),
                            justify="center",
                            validate="key",
                            validatecommand=(
                                validate_command,
                                "%P",
                                str(actual_row),
                                str(actual_col)
                            )
                        )

                        cell.grid(
                            row=cell_row,
                            column=cell_col,
                            padx=2,
                            pady=2,
                            ipady=6
                        )

                        cell.bind(
                            "<Enter>",
                            lambda event, widget=cell:
                            self.cell_hover(widget, True)
                        )

                        cell.bind(
                            "<Leave>",
                            lambda event, widget=cell:
                            self.cell_hover(widget, False)
                        )

                        cell.bind(
                            "<KeyRelease>",
                            lambda event,
                            r=actual_row,
                            c=actual_col:
                            self.cell_changed(r, c)
                        )

                        while len(self.cells) <= actual_row:
                            self.cells.append([])

                        self.cells[actual_row].append(cell)

        # Difficulty selector
        difficulty_frame = tk.Frame(
            main_frame,
            bg=self.BG
        )
        difficulty_frame.pack(
            pady=(20, 10)
        )

        difficulty_label = tk.Label(
            difficulty_frame,
            text="DIFFICULTY",
            bg=self.BG,
            fg=self.MUTED,
            font=("Consolas", 10, "bold")
        )
        difficulty_label.pack(
            side="left",
            padx=(0, 10)
        )

        self.difficulty = tk.StringVar(
            value="medium"
        )

        difficulty_menu = ttk.Combobox(
            difficulty_frame,
            textvariable=self.difficulty,
            values=["easy", "medium", "hard"],
            state="readonly",
            width=10,
            font=("Consolas", 10)
        )
        difficulty_menu.pack(
            side="left"
        )

        # Buttons
        button_frame = tk.Frame(
            main_frame,
            bg=self.BG
        )
        button_frame.pack(
            pady=10
        )

        self.create_button(
            button_frame,
            "SOLVE",
            self.solve_puzzle,
            self.ACCENT
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        self.create_button(
            button_frame,
            "GENERATE",
            self.generate_puzzle,
            self.PURPLE
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        self.create_button(
            button_frame,
            "CLEAR",
            self.clear_board,
            self.MUTED
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        # Status
        self.status_label = tk.Label(
            main_frame,
            text="Enter a puzzle or generate one.",
            bg=self.BG,
            fg=self.TEXT,
            font=("Consolas", 10)
        )
        self.status_label.pack(
            pady=(15, 5)
        )

        # Stats
        stats_frame = tk.Frame(
            main_frame,
            bg=self.PANEL
        )
        stats_frame.pack(
            fill="x",
            pady=(5, 0)
        )

        self.stats_label = tk.Label(
            stats_frame,
            text="ATTEMPTS: --    BACKTRACKS: --    TIME: --",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Consolas", 9),
            padx=15,
            pady=10
        )
        self.stats_label.pack()

    def create_button(self, parent, text, command, color):
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=11,
            bg=self.PANEL,
            fg=color,
            activebackground=self.CELL_HOVER,
            activeforeground=color,
            relief="flat",
            bd=0,
            font=("Consolas", 10, "bold"),
            cursor="hand2",
            padx=8,
            pady=8
        )

    def validate_input(
        self,
        proposed_value,
        row,
        col
    ):
        row = int(row)
        col = int(col)

        # Fixed puzzle clues cannot be changed.
        if (row, col) in self.original_cells:
            return False

        # Allow clearing a cell.
        if proposed_value == "":
            return True

        # Only allow one digit.
        if len(proposed_value) != 1:
            return False

        # Only allow digits 1-9.
        if proposed_value not in "123456789":
            return False

        return True

    def cell_hover(self, cell, entering):
        if entering:
            cell.configure(
                bg=self.CELL_HOVER
            )
        else:
            cell.configure(
                bg=self.CELL
            )

    def cell_changed(self, row, col):
        if (row, col) in self.original_cells:
            return

        value = self.cells[row][col].get().strip()

        if value == "":
            self.cells[row][col].configure(
                fg=self.TEXT
            )

            return

        if not self.is_move_valid(
            row,
            col,
            int(value)
        ):
            cell = self.cells[row][col]

            cell.configure(
                fg=self.ERROR
            )

            self.status_label.configure(
                text="Invalid move.",
                fg=self.ERROR
            )

            self.root.after(
                250,
                lambda: self.clear_invalid_cell(
                    row,
                    col
                )
            )

        else:
            self.cells[row][col].configure(
                fg=self.ACCENT
            )

            self.status_label.configure(
                text="Valid move.",
                fg=self.ACCENT
            )

    def clear_invalid_cell(self, row, col):
        if (row, col) in self.original_cells:
            return

        cell = self.cells[row][col]

        cell.delete(
            0,
            tk.END
        )

        cell.configure(
            fg=self.TEXT
        )

        self.status_label.configure(
            text="Enter a valid number.",
            fg=self.TEXT
        )

    def is_move_valid(self, row, col, number):
        # Check row
        for current_col in range(9):
            if current_col != col:
                value = self.cells[row][current_col].get().strip()

                if value == str(number):
                    return False

        # Check column
        for current_row in range(9):
            if current_row != row:
                value = self.cells[current_row][col].get().strip()

                if value == str(number):
                    return False

        # Check 3x3 box
        box_start_row = (row // 3) * 3
        box_start_col = (col // 3) * 3

        for current_row in range(
            box_start_row,
            box_start_row + 3
        ):
            for current_col in range(
                box_start_col,
                box_start_col + 3
            ):
                if (
                    current_row == row
                    and current_col == col
                ):
                    continue

                value = self.cells[current_row][current_col].get().strip()

                if value == str(number):
                    return False

        return True

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
                cell = self.cells[row][col]

                # Disable validation while the application
                # populates the board.
                cell.configure(
                    validate="none"
                )

                cell.delete(
                    0,
                    tk.END
                )

                if board[row][col] != 0:
                    cell.insert(
                        0,
                        board[row][col]
                    )

                    if (row, col) in self.original_cells:
                        cell.configure(
                            fg=self.PURPLE
                        )
                    else:
                        cell.configure(
                            fg=self.ACCENT
                        )

                else:
                    cell.configure(
                        fg=self.TEXT
                    )

                # Re-enable validation for user input.
                cell.configure(
                    validate="key"
                )

    def set_original_cells(self, board):
        self.original_cells.clear()

        for row in range(9):
            for col in range(9):
                if board[row][col] != 0:
                    self.original_cells.add(
                        (row, col)
                    )

    def clear_board(self):
        for row in range(9):
            for col in range(9):
                cell = self.cells[row][col]

                cell.configure(
                    validate="none"
                )

                cell.delete(
                    0,
                    tk.END
                )

                cell.configure(
                    fg=self.TEXT
                )

                cell.configure(
                    validate="key"
                )

        self.original_cells.clear()

        self.status_label.configure(
            text="Board cleared.",
            fg=self.TEXT
        )

        self.stats_label.configure(
            text="ATTEMPTS: --    BACKTRACKS: --    TIME: --"
        )

    def solve_puzzle(self):
        board = self.get_board()

        if board is None:
            self.status_label.configure(
                text="Invalid input. Use numbers 1-9.",
                fg=self.ERROR
            )

            return

        if not is_valid_board(board):
            self.status_label.configure(
                text="Invalid Sudoku puzzle.",
                fg=self.ERROR
            )

            return

        # Remember the numbers that existed before solving.
        self.set_original_cells(board)

        stats = {
            "attempts": 0,
            "backtracks": 0
        }

        start_time = time.perf_counter()

        solved = solve_mrv(
            board,
            stats
        )

        end_time = time.perf_counter()

        if solved:
            self.display_board(board)

            self.status_label.configure(
                text="Puzzle solved successfully.",
                fg=self.ACCENT
            )

        else:
            self.status_label.configure(
                text="This puzzle has no solution.",
                fg=self.ERROR
            )

        self.stats_label.configure(
            text=(
                f"ATTEMPTS: {stats['attempts']}    "
                f"BACKTRACKS: {stats['backtracks']}    "
                f"TIME: {end_time - start_time:.6f}s"
            )
        )

    def generate_puzzle(self):
        difficulty = self.difficulty.get()

        self.status_label.configure(
            text=f"Generating {difficulty} puzzle...",
            fg=self.TEXT
        )

        self.root.update_idletasks()

        board = generate_by_difficulty(
            difficulty
        )

        self.set_original_cells(
            board
        )

        self.display_board(
            board
        )

        self.status_label.configure(
            text=f"{difficulty.upper()} puzzle generated.",
            fg=self.PURPLE
        )

        self.stats_label.configure(
            text="ATTEMPTS: --    BACKTRACKS: --    TIME: --"
        )


root = tk.Tk()

app = SudokuGUI(root)

root.mainloop()