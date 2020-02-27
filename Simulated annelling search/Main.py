from LOA.Manager import Manager
from LOA.DVar import DVar
from LOA.LinearExpr import LinearExpr
from LOA.Constraint import Eq, Le, Ge
from LOA.Search import SASearch
import matplotlib.pyplot as plt


def model():
    mng = Manager()
    n = 5
    x = [DVar(mng, 0, 10, i) for i in range(n)]
    exprs = [LinearExpr() for i in range(3)]
    obj = LinearExpr()

    # x[0] + 2x[2] = 9
    exprs[0].add_term(1, x[0])
    exprs[0].add_term(2, x[2])
    mng.add_constraint(Eq(exprs[0], 9))

    # 2x[1] - x[3] <= 4
    exprs[1].add_term(2, x[1])
    exprs[1].add_term(-1, x[3])
    mng.add_constraint(Le(exprs[1], 4))

    # 2x[0] + 3x[1] + x[4] >= 10
    exprs[2].add_term(1, x[4])
    exprs[2].add_term(3, x[1])
    exprs[2].add_term(2, x[0])
    mng.add_constraint(Ge(exprs[2], 10))

    # obj = sum(x)
    for i in range(n):
        obj.add_term(1, x[i])

    mng.minimize(obj)

    mng.close()
    return mng


result = SASearch.parallel_search(model, 5, 200, 30)
best_fitnesses = [result[i].obj_value for i in range(len(result))]

print(f'\nMin = {min(best_fitnesses)}')