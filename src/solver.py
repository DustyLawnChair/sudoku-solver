def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col

    return None


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

            if num == 0:
                continue

            board[row][col] = 0

            if not is_valid(board, num, row, col):
                board[row][col] = num
                return False

            board[row][col] = num

    return True


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

                    if len(best_candidates) == 1:
                        break

        if best_candidates is not None and len(best_candidates) == 1:
            break

    return best_cell, best_candidates


def solve(board, stats):
    empty = find_empty(board)

    if empty is None:
        return True

    row, col = empty

    for num in range(1, 10):
        stats["attempts"] += 1

        if is_valid(board, num, row, col):
            board[row][col] = num

            if solve(board, stats):
                return True

            board[row][col] = 0
            stats["backtracks"] += 1

    return False


def solve_mrv(board, stats):
    cell, candidates = find_best_empty(board)

    if cell is None:
        return True

    row, col = cell

    for num in candidates:
        stats["attempts"] += 1

        board[row][col] = num

        if solve_mrv(board, stats):
            return True

        board[row][col] = 0
        stats["backtracks"] += 1

    return False