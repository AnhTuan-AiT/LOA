import random
import math
import threading, multiprocessing


class SASearch:

    def __init__(self, manager):
        self.__manager =  manager
        self.__d_vars = manager.d_vars
        self.__obj_func = manager.obj_func
        self.__best_fitness = 32635
        self.__curr_solution = [0 for i in range(len(manager.d_vars))]
        self.__T_init = None
        self.__T_min = None
        self.__T = None
        self.best_solution = [0 for i in range(len(manager.d_vars))]
        self.list_fitnesses = []

    @property
    def obj_value(self):
        return self.__best_fitness

    def init_solution(self):
        while self.__manager.violation != 0:
            i = random.randint(0, len(self.__d_vars) - 1)
            new_value = random.randint(self.__d_vars[i].min_value, self.__d_vars[i].max_value)
            self.__d_vars[i].curr_value = new_value

        for i in range(len(self.__d_vars)):
            self.__curr_solution[i] = self.__d_vars[i].curr_value
            self.best_solution[i] = self.__d_vars[i].curr_value

        if self.fitness() < self.__best_fitness:
            self.__best_fitness = self.fitness()

        '''
        print(self.__best_fitness)
        for i in range(len(self.__curr_solution)):
            print(self.__manager.dvar[i].value)
        '''

    def move_to_neighbor(self):
        while True:
            i = random.randint(0, len(self.__d_vars) - 1)
            curr_value = self.__d_vars[i].curr_value
            feasible_value = []

            # find a new value for x[i] that doesn't cause violation.
            for value in range(self.__d_vars[i].min_value, self.__d_vars[i].max_value):
                self.__d_vars[i].curr_value = value
                if self.__manager.set_value_violation(self.__d_vars[i]):
                    feasible_value.append(value)

            if len(feasible_value) > 0:
                self.__d_vars[i].curr_value = feasible_value[random.randint(0, len(feasible_value) - 1)]
                break

        '''
        for i in range(len(self.__manager.dvar)):
            print(f'{self.__manager.dvar[i].value}, ', end = '')

        print()
        '''

    def fitness(self):
        return self.__obj_func.curr_value

    def acceptance_probability(self, delta):
        return math.exp(-delta/self.__T)

    def geometrical_cooling_schedule(self, alpha, k):
        """
        :param alpha: A constant betwwen 0 and 1. To have a slow decrease of temperature, it is necessary that the value of αlpha is closer to 1.
        :param k: Iteration number
        :return: None
        """
        self.__T = self.__T*math.pow(alpha, k)

    def linear_cooling_schedule(self, n, k):
        """
        :param n: Decay parameter
        :param k: Iteration number
        :return: None
        """
        self.__T = self.__T_init - n*k

    def update_solution(self, solution):
        for i in range(len(solution)):
            solution[i] = self.__d_vars[i].curr_value

    def go_back_previous_solution(self):
        for i in range(len(self.__curr_solution)):
            self.__d_vars[i].value = self.__curr_solution[i]

    def search(self, restart_const, max_iter, max_temp, min_temp = 1.0):
        print("Searching...   ", end='')
        self.__T = max_temp
        self.__T_init = max_temp
        self.__T_min = min_temp
        alpha = 0.99
        n_reduce_temp = 0
        old_fitness = 0
        new_fitness = 0
        delta = 0

        self.init_solution()

        while self.__T > self.__T_min:
            for k in range(max_iter):
                old_fitness = self.fitness()
                self.move_to_neighbor()
                new_fitness = self.fitness()
                delta = new_fitness - old_fitness

                if delta <= 0:
                    self.update_solution(self.__curr_solution)
                    self.list_fitnesses.append(new_fitness)

                    if new_fitness < self.__best_fitness:
                        self.list_fitnesses.append(new_fitness)
                        self.__best_fitness = new_fitness
                        self.update_solution(self.best_solution)
                elif random.random() < self.acceptance_probability(delta):
                    self.list_fitnesses.append(new_fitness)
                    self.update_solution(self.__curr_solution)
                else:
                    self.go_back_previous_solution()

                # print(f"Temperature = {self.__T}, Iteration number = {k}, best fitness = {self.__best_fitness}")

            self.geometrical_cooling_schedule(alpha, 1)

            # Restart searching process.
            n_reduce_temp +=1
            if n_reduce_temp % restart_const == 0:
                self.init_solution()

    @staticmethod
    def parallel_search(model_func, restart_const, max_iter, max_temp, min_temp = 1.0):
        """
        :param model_func: function's name that models the problem. It must create a Manager object, model with and return it
        :param restart_const: the number of times the temperature decreases before each restart of the searching process
        :param max_iter:
        :param max_temp:
        :param min_temp:
        :return: list of solvers corresponding to threads
        """
        n_threads = multiprocessing.cpu_count() - 1
        managers = [model_func() for i in range(n_threads)]
        solvers = [SASearch(managers[i]) for i in range(n_threads)]
        threads = [threading.Thread(target=solvers[i].search, args=(restart_const, max_iter, max_temp)) for i in range(n_threads)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return solvers







