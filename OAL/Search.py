import random
import math

class SASearch:

    def __init__(self, manager):
        self.__manager =  manager
        self.__objtive_function = self.__manager.obj_func
        self.__best_fitness = 0
        self.__curr_solution = [0 for i in range(len(self.__manager.dvar))]
        self.__T_init = 0
        self.__T_min = 1
        self.__T = 0
        self.best_solution = [0 for i in range(len(self.__manager.dvar))]
        self.fitnesses = []

    @property
    def obj_value(self):
        return self.__best_fitness

    def init_solution(self):
        while self.__manager.violation != 0:
            i_dvar = random.randint(0, len(self.__manager.dvar) - 1)
            new_value = random.randint(self.__manager.dvar[i_dvar].min_value, self.__manager.dvar[i_dvar].max_value)
            self.__manager.dvar[i_dvar].value = new_value

        for i in range(len(self.__manager.dvar)):
            self.__curr_solution[i] = self.__manager.dvar[i].value
            self.best_solution[i] = self.__manager.dvar[i].value

        self.__best_fitness = self.fitness()
        print(self.__best_fitness)
        '''
        for i in range(len(self.__curr_solution)):
            print(self.__manager.dvar[i].value)
        '''


    def move_to_neighbor(self):
        i_dvar = random.randint(0, len(self.__manager.dvar) - 1)
        curr_value = self.__manager.dvar[i_dvar].value
        feasible_value = []
        new_value = curr_value

        # find a new value for x[i_dvar] that doesn't cause violation.
        for value in range(self.__manager.dvar[i_dvar].min_value, self.__manager.dvar[i_dvar].max_value):
            self.__manager.dvar[i_dvar].value = value
            if (self.__manager.set_value_violation(self.__manager.dvar[i_dvar])):
                feasible_value.append(value)

        self.__manager.dvar[i_dvar].value = feasible_value[random.randint(0, len(feasible_value) - 1)]

        '''
        for i in range(len(self.__manager.dvar)):
            print(f'{self.__manager.dvar[i].value}, ', end = '')

        print()
        '''


    def fitness(self):
        return self.__objtive_function.curr_value

    def acceptance_probability(self, delta):
        return math.exp(-delta/self.__T)

    def geometrical_cooling_schedule(self, alpha, k):
        '''
        :param alpha: A constant betwwen 0 and 1. To have a slow decrease of temperature, it is necessary that the value of αlpha is closer to 1.
        :param k: Iteration number
        :return: None
        '''
        self.__T = self.__T*math.pow(alpha, k)

    def linear_cooling_schedule(self, n, k):
        '''
        :param n: Decay parameter
        :param k: Iteration number
        :return: None
        '''
        self.__T = self.__T_init - n*k

    def update_solution(self, solution):
        for i in range(len(solution)):
            solution[i] = self.__manager.dvar[i].value

    def go_back_previous_solution(self):
        for i in range(len(self.__curr_solution)):
            self.__manager.dvar[i].value = self.__curr_solution[i]

    def search(self, restart_const, max_iter, max_temp, min_temp = 1.0):
        self.__T = max_temp
        self.__T_init = max_temp
        self.__T_min = min_temp
        alpha = 0.99
        n_reduce_temp = 0
        old_fitness = 0
        new_fitness = 0
        delta = 0

        self.init_solution()

        while (self.__T > self.__T_min):
            for k in range(max_iter):
                old_fitness = self.fitness()
                self.move_to_neighbor()
                new_fitness = self.fitness()
                delta = new_fitness - old_fitness

                if delta <= 0:
                    self.update_solution(self.__curr_solution)
                    self.fitnesses.append(new_fitness)
                    if new_fitness < self.__best_fitness:
                        self.__best_fitness = new_fitness
                        self.update_solution(self.best_solution)
                elif random.random() < self.acceptance_probability(delta):
                    self.fitnesses.append(new_fitness)
                    self.update_solution(self.__curr_solution)
                else:
                    self.go_back_previous_solution()

                print(f"Iteration number = {k}, best fitness = {self.__best_fitness}")

            self.geometrical_cooling_schedule(alpha, 1)

            # Restart searching process.
            n_reduce_temp +=1
            if(n_reduce_temp % restart_const == 0):
                self.init_solution()




