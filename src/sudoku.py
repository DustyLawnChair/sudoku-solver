import time

from src.solver import solve_mrv, is_valid_board
from src.generator import generate_by_difficulty


def main_menu():
    print("=" * 32)
    print("          SUDOKU SOLVER")
    print("=" * 32)
    print()
    print("1. Solve a puzzle")
    print("2. Generate a puzzle")
    print("3. Exit")
    print()

    return input("Choose an option: ").strip()


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


def solve_puzzle(board):
    if not is_valid_board(board):
        print("Invalid Sudoku puzzle.")
        return

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


def generate_puzzle_menu():
    print()
    print("Select difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print()

    difficulty_choice = input("Choose a difficulty: ").strip()

    difficulties = {
        "1": "easy",
        "2": "medium",
        "3": "hard"
    }

    if difficulty_choice not in difficulties:
        print("\nInvalid difficulty.")
        return

    difficulty = difficulties[difficulty_choice]

    print()
    print(f"Generating {difficulty} puzzle...")
    print()

    board = generate_by_difficulty(difficulty)

    print_board(board)
    print()

    print("Puzzle generated!")
    print()
    print("1. Solve this puzzle")
    print("2. Return to main menu")
    print()

    next_choice = input("Choose an option: ").strip()

    if next_choice == "1":
        print()
        solve_puzzle(board)

    elif next_choice == "2":
        print("\nReturning to main menu...")

    else:
        print("\nInvalid option.")


choice = main_menu()

if choice == "1":
    board = get_puzzle()

    print()
    solve_puzzle(board)

elif choice == "2":
    generate_puzzle_menu()

elif choice == "3":
    print("\nGoodbye!")

else:
    print("\nInvalid option.")