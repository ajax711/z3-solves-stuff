from z3 import *

X = [[Bool(f"x_{i+1}_{j+1}") for j in range(8)] for i in range(8)]

solver = Solver()

#rwo contraints 

for i in range(8):
    solver.add(Or([X[i][j] for j in range(8)]))  # At least one queen
    for j in range(8):
        for k in range(j + 1, 8):
            solver.add(Implies(X[i][j], Not(X[i][k])))  # No two queens in the same row

#col constraints 
for j in range(8):
    solver.add(Or([X[i][j] for i in range(8)]))  # At least one queen
    for i in range(8):
        for k in range(i + 1, 8):
            solver.add(Implies(X[i][j], Not(X[k][j])))  # No two queens in the same column

#diagonal constraints 
for i in range(8):
    for j in range(8):
        for k in range(8):
            for l in range(8):
                if i != k and j != l and abs(i - k) == abs(j - l):
                    solver.add(Implies(X[i][j], Not(X[k][l])))

# Check if the solution exists and print it
if solver.check() == sat:
    model = solver.model()
    board = [["." for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            if model.evaluate(X[i][j]):
                board[i][j] = "Q"
    for row in board:
        print(" ".join(row))
else:
    print("No solution found")
