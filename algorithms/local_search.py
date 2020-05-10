import numpy as np
import copy
import matplotlib.pyplot as plt
# np.random.seed(42)

class LocalSearch:

    def __init__(self, n, D, F):
        self.n = n
        self.D = D
        self.F = F
        self.solution = None
        self.cost_fun = None
        self.plot_list = []

    def initial_solution(self, eye=False) -> np.array:
        if eye:
            return np.arange(self.n, dtype=int)
        return np.random.permutation(np.arange(self.n))

    def cost_function(self) -> int:
        fun_sum = 0
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    fun_sum += self.F[i,j] * self.D[self.solution[i],self.solution[j]]
        return fun_sum

    def delta_function(self, r, s) -> int:
        fun_sum = 0
        for k in range(self.n):
            if k != r and k != s:
                fun_sum += (self.F[k, r] + self.F[r, k]) * \
                           (self.D[self.solution[s], self.solution[k]] - self.D[self.solution[r], self.solution[k]]) + \
                           (self.F[k, s] + self.F[s, k]) * \
                           (self.D[self.solution[r], self.solution[k]] - self.D[self.solution[s], self.solution[k]])
        return fun_sum

    def run(self, method, dlb=True, eye=False, iters=100):
        method_name = copy.deepcopy(method)
        method = getattr(LocalSearch, method)
        self.solution = self.initial_solution(eye=eye)
        self.cost_fun = self.cost_function()
        except_fac = -1
        while True:
            if 'stochastic_2_opt' in method_name:
                result = method(self, iters)
            else:
                result = method(self, except_fac, dlb=dlb)
            if result is not None:
                r = result['r']
                s = result['s']
                self.solution[[r, s]] = self.solution[[s, r]]
                self.cost_fun += result['delta']
                self.plot_list.append(self.cost_fun)
                except_fac = result['r']
            else:
                return np.argsort(self.solution)

    def first_improvement(self, except_fac, dlb=False):
        if dlb:
            bits = np.zeros(self.n)
        for r in range(self.n):
            if r == except_fac:
                continue
            for s in range(self.n):
                if r != s:
                    if dlb and bits[s]:
                        continue
                    delta = self.delta_function(r, s)
                    if delta < 0:
                        return {'delta': delta, 'r': r, 's': s}
            bits[r] = 1
        return None

    def best_improvement(self, except_fac, dlb=False):
        min_delta = 0
        min_result = None
        if dlb:
            bits = np.zeros(self.n)
        for r in range(self.n):
            if r == except_fac:
                continue
            for s in range(self.n):
                if r != s:
                    if dlb and bits[s]:
                        continue
                    delta = self.delta_function(r, s)
                    if delta < min_delta:
                        min_delta = delta
                        min_result = {'delta': delta, 'r': r, 's': s}
            if min_result is not None:
                return min_result
            else:
                bits[r] = 1
        return None

    def stochastic_2_opt(self, iters):
        flag = 0
        for iter in range(iters):
            a = np.random.randint(low=0, high=self.n-1)
            b = np.random.randint(low=a+1, high=self.n)
            swap_part = np.arange(a, b+1)
            prev_cost = self.cost_fun
            prev_solution = self.solution
            self.plot_list.append(self.cost_fun)
            self.solution[swap_part] = self.solution[np.flip(swap_part)]
            self.cost_fun = self.cost_function()
            flag = 1
            if prev_cost < self.cost_fun:
                self.solution = prev_solution
                self.cost_fun = prev_cost
                flag = 0
        if flag:
            return {'delta': 0, 'r': 0, 's': 0}
        return None

    def plot(self, title='Algo'):
        plt.plot(list(range(len(self.plot_list))), self.plot_list)
        plt.grid()
        plt.title(title)
        plt.xlabel('iterations')
        plt.ylabel('cost')
        plt.show()



# n = 4
# D = np.array([[0, 22, 53, 53],
#               [22, 0, 40, 62],
#               [53, 40, 0, 55],
#               [53, 62, 55, 0]])
# F = np.array([[0, 3, 0, 2],
#               [3, 0, 0, 1],
#               [0, 0, 0, 4],
#               [2, 1, 4, 0]])
# test = LocalSearch(n, D, F)
# print('F is: \n', F)
# print('D is: \n', D)
# print(test.cost_fun)
# print('\n', test.run('stochastic_2_opt'))
# print(test.cost_fun)



n = 5
D = np.array([[0, 50, 50, 94, 50],
              [50, 0, 22, 50, 36],
              [50, 22, 0, 44, 14],
              [94, 50, 44, 0, 50],
              [50, 36, 14, 50, 0]])
F = np.array([[0, 0, 2, 0, 3],
              [0, 0, 0, 3, 0],
              [2, 0, 0, 0, 0],
              [0, 3, 0, 0, 1],
              [3, 0, 0, 1, 0]])
test = LocalSearch(n, D, F)
print('F is: \n', F)
print('D is: \n', D)
print('\n', test.run('stochastic_2_opt', iters=100))
print(test.cost_fun)
print(test.plot_list)
test.plot(title='So')

