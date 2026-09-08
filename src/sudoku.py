import time

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



# test code
start_time = time.perf_counter()

if solve(board):
    end_time = time.perf_counter()

    print("Solved!")
    print_board(board)

    print()
    print(f"Attempts: {stats['attempts']}")
    print(f"Backtracks: {stats['backtracks']}")
    print(f"Time: {end_time - start_time:.6f} seconds")
else:
    print("No solution exists.")