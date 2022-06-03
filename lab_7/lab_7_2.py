"""
Создать параллельный код с использованием функций пакета mpi4py.
Следует построить гистограмму распределения собственных значений 
действительной симметричной трехдиагональной матрицы размером N x N
(N не менее 1000) с использованием алгоритма деления отрезка пополам 
(Уикинсон, Райнш). Главную диагональ заполнить последовательно 
чередующимися числами 5.0 и 2.0. Наддиагональ и поддиагональ заполнить 
единицами. График гистограммы распределения собственных значений матрицы 
с построить с постоянным шагом h без использования функций для создания 
гистограмм из matplotlib.pyplot (типа hist). Гистограмма должна содержать 
несколько десятков шагов. Код для построения гистограммы - последовательный.


Выполнил Башлыков Данила, 4 курс 5 группа
"""

from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
p = comm.Get_size()


def func(dawn, dusk, h, A, x, n):
	E = 0.01
	k = 0
	for i in range(dawn, dusk):
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
		summ = 0
		for z in range(i):
			summ += y[z]
		y[i] = k - summ
		k = 0
	
	return x
		
		

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

h = 0.5  # выбор шага для построения гистограммы
z = int(n/h) + 1


if rank == 0:
	print("Yakobi Matrix:")
	print(A, "\n")

	L, v = np.linalg.eig(A)         #функция выявления собственных значений
	#print("Own values of Matrix A: ")
	#print(L, "\n")                    # и собственных векторов матрицы
	
	
	
x = np.empty(z, dtype = float)
y = np.empty(z, dtype = float)      # формирование массивов x и y, по которым построим гистрограмму
x[0] = y[0] = 0
	
dest = 0 
dawn = 1 + rank * 5
dusk = dawn + 5
x = func(dawn, dusk, h, A, x, n)
#print(y)

f = np.empty(dusk-dawn, dtype = float)
for i in range(dusk - dawn):
	f[i] = y[dawn]
	dawn = dawn + 1

y1 = None   # задаем пустой объект recvbuf
if rank == 0:
    y1 = np.empty(z-1, dtype='d')

comm.Gather(f, y1, root=0)


if rank == 0:
	x1 = np.empty(z, dtype = float)
	for i in range(dusk):
		if x[i] > 0.1:
			x1[i] = x[i]

if rank == 0:
	for source in range(1,p):
		print("source", source)
		x = comm.recv(source=source)
		print("comm.recv: ", rank,"<-",source)
		for i in range(z):
			if x[i] > 0.1:
				x1[i] = x[i]
		
	
else:
	print("comm.send: ", rank,"->", dest)
	comm.send(x, dest=0)
	



if rank == 0:
	y2 = np.empty(z, dtype = float)
	y2[0] = 0
	for i in range(1, z):
		y2[i] = y1[i-1]
	
	kol = (z-1) / p

	sum1 = 0.0
	for i in range(1, int(kol+1)):
		sum1 += y2[i]

	sum2 = 0
	for i in range(1, p):
		kol2 = (i+1)*5 + 1
		for j in range(int(kol), int(kol2)):
			sum2 += y2[j]
		if (sum2 == sum1):
			for j in range(int(kol), int(kol2)):
				y2[j] = 0
		else:
			y2[kol] = y2[kol] - sum1
			
		kol = kol2
		sum1 = sum2		
		sum2 = 0	
		
	print("Values on X axes:\n",x1, "\n")
	print("Values on Y axes:\n",y2, "\n")
		 
	
	
	for i in range(z):
		plt.vlines(x1[i-1], y2[i-1], y2[i])
		plt.hlines(y2[i], x1[i-1], x1[i])

	#plt.bar(x,y)
	plt.show()
