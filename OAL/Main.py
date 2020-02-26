from OAL.Manager import Manager
from OAL.DVar import DVar
from OAL.LinearExpr import LinearExpr
from OAL.Constraint import Eq, Le, Ge
from OAL.Search import SASearch
import matplotlib.pyplot as plt


mng = Manager()
x = [DVar(mng, 0, 10, i) for i in range(5)]
exprs = [LinearExpr() for i in range(3)]

exprs[0].add_term(1, x[0])
exprs[0].add_term(2, x[2])
mng.add_constraint(Eq(exprs[0], 9))

exprs[1].add_term(2, x[1])
exprs[1].add_term(-1, x[3])
mng.add_constraint(Le(exprs[1], 4))

exprs[2].add_term(1, x[4])
exprs[2].add_term(3, x[1])
exprs[2].add_term(2, x[0])
mng.add_constraint(Ge(exprs[2], 10))

obj = LinearExpr()
for i in range(5):
    obj.add_term(1, x[i])

mng.minimize(obj)

mng.close()
sa = SASearch(mng)
sa.search(500, 5)

plt.figure()
plt.subplot()
plt.axis([0, 12000, 0, 40])
plt.plot([i for i in range(len(sa.fitnesses))], sa.fitnesses, 'k')
plt.show()
