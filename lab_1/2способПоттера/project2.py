import random
import numpy as np
import math

print('Введите размерность матрицы: ')
n = int(input())
p = 6


A = np.zeros((n,n))

for i in range(n):
        for j in range(n):
                if i > j:
                        A[i][j] = A[j][i]
                else:
                        A[i][j] = random.randint(-9,5)

print("\n", 'Инициализация симметричной матрицы A размером n*n: ')
print(A, "\n")

res, values = np.linalg.eig(A)

print("Введите наперед заданное число E:")
E = float(input())

v0 = np.empty(n, dtype=float)

for i in range(n):
        v0[i] = random.randrange(-10, 10)
        v0[i] /= 10

print('Инициализация вектора v0:')
print(v0, "\n")

A2 = A
for i in range(n):
        A2[i][i] = A2[i][i] - E

print('Матрица вида (A-IE): ')
print(A2, "\n")


Lyamp1 = 0
l = 0.001

while(p > l):
    vp =np.linalg.solve(A2, v0)
    c = 0
    for i in range(n):
        c += (vp[i] * vp[i])
    for i in range(n):
        vp[i] = (1/math.sqrt(c))*vp[i]
    Lyamp2 = E+(np.dot(vp, np.dot(A2, vp))) / (np.dot(vp, vp))

    v0 = vp
    p = abs(Lyamp1 - Lyamp2)
    Lyamp1 = Lyamp2

print("Найденное собственное значение при E =", E, ": ", Lyamp2, "\n")

print("Собственные значения, найденные с помощью функции eig: ")
print(res)





