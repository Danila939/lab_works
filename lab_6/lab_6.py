# Определить максимальное и минимальное собственные значение
# при использовании пакета NUMBA (njit, prange)

# Выполнил Башлыков Данила, 4 курс 5 группа


import random
import numpy as np
from numba import njit, prange

@njit(parallel=True)
def create_matrix(A):
        for i in prange(n):
                for j in range(n):
                    if i > j:
                        A[i][j] = A[j][i]
                    else:
                        A[i][j] = random.randint(-9,2)
        return A

@njit(parallel=True)
def v0_create(v0):
        for i in prange(n):
                v0[i] = random.randrange(-10, 10)
                v0[i] /= 10
        return v0


def potter_max(A, ksi):
        A2 = A
        for i in range(n):
                A2[i][i] = A2[i][i] - ksi
        v0 = np.empty(n, dtype=float)

        for i in range(n):
                v0[i] = random.randrange(-10, 10)
                v0[i] /= 10

        vp = np.empty(n, dtype=float)

        Lyamp1 = 0
        E = 0.0001
        p = 6
        while (p > E):
                vp = np.dot(A2, v0)
                Lyamp2 = (np.dot(vp, np.dot(A2, vp))) / (np.dot(vp, vp))
                max = 0
                for i in range(n):
                        if abs(vp[i]) > abs(max):
                                max = vp[i]
                vp /= max
                v0 = vp
                p = abs(Lyamp1 - Lyamp2)
                Lyamp1 = Lyamp2

        return Lyamp2

print('Введите размерность матрицы: ')
n = int(input())
p = 6

A = np.zeros((n,n))

A = create_matrix(A)

print('Инициализация симметричной матрицы A размером n*n: ')
print(A, "\n")

v0 = np.empty(n, dtype=float)

v0 = v0_create(v0)

print('Инициализация вектора v0:')
print(v0, "\n")

vp = np.empty(n, dtype=float)

Lyamp1 = 0
E = 0.01

while(p > E):
        vp = np.dot(A, v0)
        Lyamp2 = (np.dot(vp, np.dot(A, vp))) / (np.dot(vp, vp))
        max = 0
        for i in range(n):
                if abs(vp[i]) > abs(max):
                        max = vp[i]
        vp /= max
        v0 = vp
        p = abs(Lyamp1 - Lyamp2)
        Lyamp1 = Lyamp2


value, res = np.linalg.eig(A)



if Lyamp2 < 0:
        print("Максимальное собственное значение: ", potter_max(A, Lyamp2) + Lyamp2)
        print("Минимальное собственное значение: ", Lyamp2)
else:
        print("Максимальное собственное значение: ", Lyamp2)



print("Собственные значения с помощью функции eig: ")
print(value)




