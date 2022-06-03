# в этой программе требуется определить что есть что
# анализировал и переводил студент 4 курса 5 группы факультета ПММ
# Воронежского государственного университета

#MPI - это стандарт на программный инструментарий для обеспечения связи между ветвями параллельного приложения

from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()   

numDataPerRank = 10    # присваиваем переменной этой значение 10
sendbuf = np.linspace(rank*numDataPerRank+1,(rank+1)*numDataPerRank,numDataPerRank)
                # здесь мы задаем массивы взависимости от того какой rank получатся массивы [1..10], [11..20], [21..30], [31,40]
print('Rank: ',rank, ', sendbuf: ',sendbuf) # печатаем на экране

recvbuf = None   # задаем пустой объект recvbuf
if rank == 0:
    recvbuf = np.empty(numDataPerRank*size, dtype='d')  # и делаем пустой массив размером 40

comm.Gather(sendbuf, recvbuf, root=0)  # с помощью этого метода собираем все sendbufs в recvbufs

if rank == 0:
    print('Rank: ',rank, ', recvbuf received: ',recvbuf) # выводим получившийся приемный буфер
