"""
Построить аналогичную гистограмму, используя идеи из
алгоритма деления отрезка пополам (Уикинсон, Райнш).
Сравнить полученные гистограммы (они должны быть идентичны)

Выполнил Башлыков Данила, 4 курс 5 группа
"""


import numpy as np
import matplotlib.pyplot as plt

n = 10
A = np.zeros((n,n))

for i in range(n-1):   #формирование матрицы Якоби
    if i % 2 == 0:
        A[i][i] = 5
    else:
        A[i][i] = 2

    A[i+1][i] = 1
    A[i][i+1] = 1

if A[n-2][n-2] == 5:
    A[n-1][n-1] = 2
else:
    A[n-1][n-1] = 5

print("Матрица Якоби:")
print(A, "\n")

L, v = np.linalg.eig(A)         #функция выявления собственных значений
print("Собственные значения матрицы A: ")
print(L, "\n")                    # и собственных векторов матрицы

h = 0.5  # выбор шага для построения гистограммы
z = int(n/h)
x = np.empty(z, dtype = float)
y = np.empty(z, dtype = float)     # формирование массивов x и y, по которым построим гистрограмму
x[0] = y[0] = 0

an = 0
E = 0.01   # для замены очень малого q(Lyam)
k = 0

for i in range(1,z):
    x[i] = i * h
    Lyam = i * h
    q_1_Lyam = A[0][0] - Lyam
    if q_1_Lyam < 0:
        k+=1                                  # метод BISECT в действии
    for j in range(1,n):
        if abs(q_1_Lyam) >= E:
            q_j_Lyam = (A[j][j] - Lyam) - (A[j-1][j]*A[j - 1][j]/q_1_Lyam)
            q_1_Lyam = q_j_Lyam
        else:
            q_j_Lyam = (A[j][j] - Lyam) - (A[j - 1][j]*A[j - 1][j] / E)
            q_1_Lyam = q_j_Lyam
        if q_1_Lyam < 0:
            k+=1
    y[i] = k - an
    an = k
    k = 0
    plt.vlines(x[i-1], y[i-1], y[i])
    plt.hlines(y[i], x[i-1], x[i])



print("Значения на оси абсцисс:\n",x, "\n")
print("Значения на оси ординат:\n",y, "\n")

#plt.bar(x,y)
plt.show()