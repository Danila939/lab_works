#Написать и выполнить параллельную программу, вычисляющую определенный интеграл методом Симпсона. 
#Подинтегральная функция f(x) = x*x, пределы интегрирования от a=0.0 до b=3.0.

#Выполнил Башлыков Данила, 4 курс 5 группа



from mpi4py import MPI

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
p = comm.Get_size()

L1 = open("simp.txt", "wt")
L2 = open("simp_parallel.txt", "wt")

print("p =", p, file=L2)

#function to be integrated
def f(x):
    return x*x

def simp(a, b, n, h):
	integral = (h/3)*(f(a) + f(b))
	x = a
	for i in range(1, int(2*n)):
		 x = x + h
		 if i % 2:
			 integral = integral + 4*h*f(x)/3
		 else:
			 integral = integral + 2*h*f(x)/3
	return integral
	

a = 0.0
b = 3.0
n = 600

if my_rank == 0:
	h = (b - a)/(2*n)
	print("a =", a, "   b =", b, "   h =", h, file=L1)
	res_serial = simp(a, b, n, h)
	#print("res_serial=", res_serial)
	print("res_serial=", res_serial, file=L1)

# Parallel calculations (MPI)
# a=0.0
# b=3.0
# n=600
dest=0
total=-1.0
h = (b-a)/(2*n)     
local_n = n/p 


local_a = a + my_rank*local_n*2*h
local_b = local_a + local_n*2*h
integral = simp(local_a, local_b, local_n, h)

if my_rank == 0:
	total = integral
	for source in range(1,p):
		print("source", source)
		integral = comm.recv(source=source)
		print("comm.recv: ", my_rank,"<-",source,",",integral)
		print("comm.recv: ", my_rank,"<-",source,",",integral, file=L2)
		total = total + integral
else:
	print("comm.send: ", my_rank,"->", dest, ",", integral)
	comm.send(integral, dest=0)
# Print the result
if (my_rank == 0):
	print("The integral from", a, "to", b, "=", total)
	print("The integral from", a, "to", b, "=", total, file=L2)
	
MPI.Finalize
L1.close
L2.close
