import time
import copy

board = [
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

stats = {
    "attempts": 0,
    "backtracks": 0
}


def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col

    return None


empty = find_empty(board)

def is_valid(board, num, row, col):
    # Check the row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check the column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check the 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False

    return True

def is_valid_board(board):
    for row in range(9):
        for col in range(9):
            num = board[row][col]

            # Empty cells are fine
            if num == 0:
                continue

            # Temporarily remove the number
            board[row][col] = 0

            # Check whether that number could legally exist here
            if not is_valid(board, num, row, col):
                board[row][col] = num
                return False

            # Restore the number
            board[row][col] = num

    return True

def get_puzzle():
    print("Enter your Sudoku puzzle.")
    print("Use 0 for empty cells.")
    print("Enter 9 digits per row.")
    print()

    puzzle = []

    for row in range(9):
        while True:
            try:
                values = input(f"Row {row + 1}: ").strip()

                # Allow either "530070000" or "5 3 0 0 7 0 0 0 0"
                values = values.replace(" ", "")

                if len(values) != 9:
                    print("Please enter exactly 9 digits.")
                    continue

                if not values.isdigit():
                    print("Please enter numbers only.")
                    continue

                values = [int(value) for value in values]

                puzzle.append(values)
                break

            except ValueError:
                print("Please enter numbers only.")

    return puzzle


def get_candidates(board, row, col):
    candidates = []

    for num in range(1, 10):
        if is_valid(board, num, row, col):
            candidates.append(num)

    return candidates

def find_best_empty(board):
    best_cell = None
    best_candidates = None

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                candidates = get_candidates(board, row, col)

                if best_candidates is None or len(candidates) < len(best_candidates):
                    best_cell = (row, col)
                    best_candidates = candidates

                    # Can't do better than one candidate
                    if len(best_candidates) == 1:
                        break

        if best_candidates is not None and len(best_candidates) == 1:
            break

    return best_cell, best_candidates

def print_board(board):
    for row in range(9):
        if row == 3 or row == 6:
            print("------+-------+------")

        for col in range(9):
            if col == 3 or col == 6:
                print("|", end=" ")

            print(board[row][col], end=" ")

        print()

def solve(board):
    empty = find_empty(board)

    # No empty cells means the puzzle is solved
    if empty is None:
        return True

    row, col = empty

    # Try numbers 1 through 9
    for num in range(1, 10):
        stats["attempts"] += 1

        if is_valid(board, num, row, col):
            board[row][col] = num

            # Recursively try to solve the rest of the board
            if solve(board):
                return True

            # If it didn't work, undo the move
            board[row][col] = 0
            stats["backtracks"] += 1

    return False

def solve_mrv(board):
    cell, candidates = find_best_empty(board)

    # No empty cells means the puzzle is solved
    if cell is None:
        return True

    row, col = cell

    for num in candidates:
        stats["attempts"] += 1

        board[row][col] = num

        if solve_mrv(board):
            return True

        board[row][col] = 0
        stats["backtracks"] += 1

    return False



board = [
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

# Create a valid-looking but unsolvable puzzle
board[0][2] = 4
board[0][3] = 6
board[0][5] = 8

if not is_valid_board(board):
    print("Invalid Sudoku puzzle.")
else:
    stats["attempts"] = 0
    stats["backtracks"] = 0

    start_time = time.perf_counter()

    if solve_mrv(board):
        end_time = time.perf_counter()

        print("Solved!")
        print_board(board)

        print()
        print(f"Attempts: {stats['attempts']}")
        print(f"Backtracks: {stats['backtracks']}")
        print(f"Time: {end_time - start_time:.6f} seconds")
    else:
        end_time = time.perf_counter()

        print("This Sudoku puzzle has no solution.")

        print()
        print(f"Attempts: {stats['attempts']}")
        print(f"Backtracks: {stats['backtracks']}")
        print(f"Time: {end_time - start_time:.6f} seconds")