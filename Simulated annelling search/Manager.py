class Manager:
    '''Create manager that manages model and search process'''

    def __init__(self):
        self.__id_constraint = -1
        self.__constraints = []
        self.__constraints_d_var = dict()
        self.__total_violation = 0
        self.__close = False
        self.d_vars = None
        self.obj_func = None

    @property
    def violation(self):
        if self.__close:
            self.__total_violation = 0

            for constraint in self.__constraints:
                self.__total_violation += constraint.violation

            return self.__total_violation

        raise Exception("Model is still open, close the model and try again!")

    def add_constraint (self, constraint):
        if not self.__close:
            self.__id_constraint += 1
            constraint.id = self.__id_constraint
            self.__constraints.append(constraint)

            for d_var in constraint.expr.d_vars:
                if d_var in self.__constraints_d_var:
                    self.__constraints_d_var[d_var].add(constraint.id)
                else:
                    self.__constraints_d_var[d_var] = {constraint.id}
        else:
            print(f"Can't add {constraint.name}, model closed!")

    def minimize(self, expr):
        self.obj_func = expr

    def set_value_violation(self, dvar):
        for id in self.__constraints_d_var[dvar]:
            if self.__constraints[id].violation > 0:
                return False

        return True

    def close(self):
        self.__close = True
        self.d_vars = list(self.__constraints_d_var.keys())

