import time

from solver import solve_mrv, is_valid_board


def get_puzzle():
    print("Enter your Sudoku puzzle.")
    print("Use 0 for empty cells.")
    print("Enter 9 digits per row.")
    print()

    puzzle = []

    for row in range(9):
        while True:
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

    return puzzle


def print_board(board):
    for row in range(9):
        if row == 3 or row == 6:
            print("------+-------+------")

        for col in range(9):
            if col == 3 or col == 6:
                print("|", end=" ")

            print(board[row][col], end=" ")

        print()


board = get_puzzle()

print()

if not is_valid_board(board):
    print("Invalid Sudoku puzzle.")
else:
    stats = {
        "attempts": 0,
        "backtracks": 0
    }

    start_time = time.perf_counter()

    if solve_mrv(board, stats):
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