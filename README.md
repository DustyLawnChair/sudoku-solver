# Sudoku Solver

A Python-based Sudoku solver and puzzle generator using backtracking, MRV (Minimum Remaining Values), and solution-counting to generate unique puzzles with adjustable difficulty.

## Features

- Solve standard 9×9 Sudoku puzzles
- Backtracking search algorithm
- MRV (Minimum Remaining Values) optimization
- Puzzle validation
- Unique-solution verification
- Randomized complete-board generation
- Automatic puzzle generation
- Easy, Medium, and Hard difficulty levels
- Solver statistics including attempts and backtracks
- Automated unit tests

## How It Works

### Backtracking

The solver uses recursive backtracking to fill empty cells.

For each empty cell, the solver:

1. Selects a value that is valid in the current row, column, and 3×3 box.
2. Places the value.
3. Recursively continues solving.
4. If the choice leads to a dead end, the solver removes the value and tries another.

### MRV Optimization

The solver improves traditional backtracking with the **Minimum Remaining Values (MRV)** heuristic.

Instead of choosing the first empty cell it finds, the solver selects the empty cell with the fewest possible candidates.

This reduces the search space and allows the solver to reach contradictions earlier.

### Unique Puzzle Generation

Generated puzzles are checked with a solution-counting algorithm.

A number is only permanently removed from the completed board if the resulting puzzle still has exactly one solution.

This guarantees that generated puzzles have a unique solution.

## Difficulty Generation

The generator uses different clue counts and solver-complexity thresholds:

| Difficulty | Clues | Complexity |
|------------|-------|------------|
| Easy | 45 | Lower search complexity |
| Medium | 40 | Moderate search complexity |
| Hard | 35 | Higher search complexity |

Hard puzzles are generated repeatedly until they meet a minimum solver complexity threshold based on attempts and backtracking.

## Example

```text
================================
          SUDOKU SOLVER
================================

1. Solve a puzzle
2. Generate a puzzle
3. Exit

Choose an option: 2

Select difficulty:
1. Easy
2. Medium
3. Hard

Choose a difficulty: 3

Generating hard puzzle...

0 7 0 | 0 0 0 | 8 0 0
3 0 1 | 0 0 0 | 4 2 6
8 0 0 | 0 0 1 | 0 0 5
------+-------+------
0 0 7 | 0 0 0 | 0 5 4
1 2 0 | 7 4 0 | 6 8 0
0 4 0 | 2 0 9 | 1 0 3
------+-------+------
0 8 0 | 9 1 0 | 0 6 0
0 0 6 | 0 7 0 | 0 0 2
7 0 0 | 0 6 0 | 9 0 8

Puzzle generated!

1. Solve this puzzle
2. Return to main menu

Choose an option: 1

Solved!

Attempts: 142
Backtracks: 96
Time: 0.005074 seconds