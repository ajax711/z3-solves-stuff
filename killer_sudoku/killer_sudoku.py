from z3 import * 

X = []
for i in range(9):
    row=[]
    for j in range(9):
        var = Int(f"x_{i+1}_{j+1}")
        row.append(var) 
    X.append(row)

print(X)

constraints = []
# Cell + Row + Column + Subgrid + Cage(hardest) constrains 

for i in range(9):
    for j in range(9):
        constraints.append(And(1 <= X[i][j], X[i][j] <= 9))

for i in range(9):
    constraints.append(Distinct X[i])

for i in range(9):
    col=[]
    for j in range(9):
        col.append(X[i][j])
    constraints.append(Distinct(col))
        
for i0 in range(3):
    for j0 in range(3):
        subgrid = []
        for i in range(3):
            for j in range(3):
                subgrid.append(X[3*i0 + i][3*j0 + j])
        constraints.append(Distinct(subgrid))



# Somehow code killer sudoku constraints 



