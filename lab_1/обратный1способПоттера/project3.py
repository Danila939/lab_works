import random
import numpy as np


print('Введите размерность матрицы: ')
n = int(input())
p = 6

A = np.zeros((n,n))

for i in range(n):
        for j in range(n):
                if i > j:
                        A[i][j] = A[j][i]
                else:
                        A[i][j] = random.randint(1,9)

print('Инициализация симметричной матрицы A размером n*n: ')
print(A, "\n")

v0 = np.empty(n, dtype=float)

for i in range(n):
        v0[i] = random.randrange(-10, 10)
        v0[i] /= 10

print('Инициализация вектора v0:')
print(v0, "\n")

vp = np.empty(n, dtype=float)

Lyamp1 = 0
E = 0.01

while (p > E):
        vp = np.linalg.solve(A, v0)
        Lyamp2 = (np.dot(vp, np.dot(A, vp))) / (np.dot(vp, vp))
        max = 0
        for i in range(n):
                if abs(vp[i]) > abs(max):
                        max = vp[i]
        vp /= max
        v0 = vp
        p = abs(Lyamp1 - Lyamp2)
        Lyamp1 = Lyamp2

print("Минимальное собственное значение: ", Lyamp2)

print("\n\n")
res = np.linalg.eig(A)
print(res)