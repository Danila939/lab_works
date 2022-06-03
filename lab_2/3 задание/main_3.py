"""
Модифицировать матрицу: главную диагональ заполнить последовательно чередующимися числами
5.0 и 2.0; затем одно из чисел 5.0 заменить на 10.0. Наддиагональ и поддиагональ заполнить
единицами. Найти максимальное собственное значение с точностью 0.001,
используя алгоритм деления отрезка пополам (Уикинсон, Райнш).

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
A[int(n/2)][int(n/2)] = 10   #замена одного элемента главной диагонали на число 10

print("Матрица Якоби:")
print(A)

L, v = np.linalg.eig(A)     #функция выявления собственных значений
print(L)                    # и собственных векторов матрицы

max = L[0]
for i in range(1,n):
    if L[i] > max:    #Узнаем где лежит наше максимальное собственное значение
        max = L[i]

h = 1 # шаг
for i in range(2*n):   #Понимаем какой отрезок мы рассматриваем для нахождения max
    if i*h < max and (i+1)*h > max:                # собственного значения до 0.001
        a = i*h
        b = (i + 1)*h
        break

c = 1
E = 0.001

while(abs(max - c) > E):
    c = (a+b)/2
    if(c > max):
        b = c   # находим наибольшее собственное значение методом
    else:        # отрезка пополам с точностью до 0.001
        a = c

print("\nНайденное наибольшее собственное значение: ", c)
print("Разница между искомым собственным значением и получнным функцией eig: ", abs(max-c))