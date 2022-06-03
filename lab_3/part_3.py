# в этой программе требуется определить что есть что
# анализировал и переводил студент 4 курса 5 группы факультета ПММ
# Воронежского государственного университета

#MPI - это стандарт на программный инструментарий для обеспечения связи между ветвями параллельного приложения


from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Создается несколько массивов np для каждого процесса:
# Для этой демонстрации массивы имеют только одну
# запись, которой присвоен ранг 

value = np.array(rank,'d')

print(' Rank: ',rank, ' value = ', value)

# инициализируйте массивы np, в которых будут храниться результаты:
value_sum = np.array(0.0,'d')
value_max = np.array(0.0,'d')

# выполяются сокращения и записываются операции max и sum
comm.Reduce(value, value_sum, op=MPI.SUM, root=0)
comm.Reduce(value, value_max, op=MPI.MAX, root=0)

if rank == 0:
    print(' Rank 0: value_sum =    ',value_sum)
    print(' Rank 0: value_max =    ',value_max)
