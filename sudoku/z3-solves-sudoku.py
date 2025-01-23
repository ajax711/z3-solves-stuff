from z3 import *

X = []
for i in range(9):
    row = []
    for j in range(9):
        var = Int(f"x_{i+1}_{j+1}")
        row.append(var)
    X.append(row)

cells_c = []
for i in range(9):
    for j in range(9):
        cells_c.append(And(1 <= X[i][j], X[i][j] <= 9))

rows_c = []
for i in range(9):
    rows_c.append(Distinct(X[i]))

cols_c = []
for j in range(9):
    col = []
    for i in range(9):
        col.append(X[i][j])
    cols_c.append(Distinct(col))

sq_c = []
for i0 in range(3):
    for j0 in range(3):
        subgrid = []
        for i in range(3):
            for j in range(3):
                subgrid.append(X[3*i0 + i][3*j0 + j])
        sq_c.append(Distinct(subgrid))

sudoku_c = cells_c + rows_c + cols_c + sq_c

instance = [
    (0, 1, 3, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 5, 0, 0, 0, 0, 4),
    (5, 0, 0, 0, 2, 7, 0, 0, 3),
    (0, 5, 0, 0, 6, 0, 0, 0, 0),
    (7, 3, 0, 0, 0, 5, 0, 2, 0),
    (9, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 7, 0, 0, 9, 0, 8, 0, 2),
    (2, 0, 0, 0, 0, 0, 1, 9, 0),
    (0, 0, 0, 0, 1, 0, 0, 0, 0),
]

instance_c = []
for i in range(9):
    for j in range(9):
        if instance[i][j] != 0:
            instance_c.append(X[i][j] == instance[i][j])

s = Solver()
s.add(sudoku_c + instance_c)

if s.check() == sat:
    model = s.model()
    solved_grid = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(model.evaluate(X[i][j]).as_long())
        solved_grid.append(row)

    def print_sudoku(grid):
        for row in grid:
            print(row)

    print("Sudoku Solution:")
    print_sudoku(solved_grid)

else:
    print("No solution exists!")
