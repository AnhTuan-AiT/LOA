class Manager:
    '''Create manager that manages model and search process'''

    def __init__(self):
        self.__id_constraint = -1
        self.__constraints = []
        self.dvar = []
        self.__constraints_of_dvar = dict()
        self.__total_violation = 0
        self.__close = False
        self.obj_func = None

    def add_constraint (self, constraint):
        if not self.__close:
            self.__id_constraint += 1
            constraint.id = self.__id_constraint
            self.__constraints.append(constraint)

            for dvar in constraint.linear_expr.dvar:
                if dvar in self.__constraints_of_dvar:
                    self.__constraints_of_dvar[dvar].add(constraint.id)
                else:
                    self.__constraints_of_dvar[dvar] = {constraint.id}
        else:
            print(f"Can't add {constraint.name}, model closed!")

    def minimize(self, linear_expr):
        self.obj_func = linear_expr

    def set_value_violation(self, dvar):
        for id in self.__constraints_of_dvar[dvar]:
            if self.__constraints[id].violation > 0:
                return False

        return True

    @property
    def violation(self):
        self.__total_violation = 0

        for constraint in self.__constraints:
            self.__total_violation += constraint.violation

        return self.__total_violation

    def close(self):
        self.__close = True
        self.dvar = list(self.__constraints_of_dvar.keys())
