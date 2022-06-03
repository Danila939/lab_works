"""
МАТРИЧНОЕ УМНОЖЕНИЕ
"""
import numpy as np
from numba import jit, njit, prange
from datetime import datetime

L = open("Listing.txt", "wt")

def matel(i, j):
    if i==j:
        return 3.0
    elif i > j:
        return 2*abs(i-j)
    else:
        return 2.0/abs(i-j)

def mult_1(A, B):
    res = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            res[i,j] += A[i,j] * B[j,i]
    return res

@jit
def mult_2(A, B):
    res = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            res[i, j] += A[i, j] * B[j, i]
    return res

@jit("float64[:,:](float64[:,:], float64[:,:])")
def mult_3(A, B):
    res = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            res[i, j] += A[i, j] * B[j, i]
    return res

@njit(parallel=True)
def mult_4(A, B):
    res = np.zeros((A.shape[0], B.shape[1]))
    for i in prange(A.shape[0]):
        for j in range(B.shape[1]):
            res[i, j] += A[i, j] * B[j, i]
    return res

@njit("float64[:,:](float64[:,:], float64[:,:])", parallel=True)
def mult_5(A, B):
    res = np.zeros((A.shape[0], B.shape[1]))
    for i in prange(A.shape[0]):
        for j in range(B.shape[1]):
            res[i, j] += A[i, j] * B[j, i]
    return res

@njit("float64[:,:](float64[:,:], float64[:,:])", parallel=True)
def mult_6(A, B):
    res = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for j in prange(B.shape[1]):
            res[i, j] += A[i, j] * B[j, i]
    return res



n = 2000
A = np.array([[matel(i, j) for i in range(n)] for j in range(n)])
B = np.array([[matel(i, j) for i in range(n)] for j in range(n)])

t7_start = datetime.now()
res7 = np.dot(A, B)
t7_stop = datetime.now()

print("n= ", n)

t1_start = datetime.now()
res1 = mult_1(A, B)
t1_stop = datetime.now()
print('Duration mult_1: {}'.format(t1_stop-t1_start))
print('Duration mult_1: {}'.format(t1_stop-t1_start), file=L)

t2_start = datetime.now()
res2 = mult_2(A, B)
t2_stop = datetime.now()
print('Duration mult_2: {}'.format(t2_stop-t2_start))
print('Duration mult_2: {}'.format(t2_stop-t2_start), file=L)

t3_start = datetime.now()
res3 = mult_3(A, B)
t3_stop = datetime.now()
print('Duration mult_3: {}'.format(t3_stop-t3_start))
print('Duration mult_3: {}'.format(t3_stop-t3_start), file=L)

t4_start = datetime.now()
res4 = mult_4(A, B)
t4_stop = datetime.now()
print('Duration mult_4: {}'.format(t4_stop-t4_start))
print('Duration mult_4: {}'.format(t4_stop-t4_start), file=L)

t5_start = datetime.now()
res5 = mult_5(A, B)
t5_stop = datetime.now()
print('Duration mult_5: {}'.format(t5_stop-t5_start))
print('Duration mult_5: {}'.format(t5_stop-t5_start), file=L)

t6_start = datetime.now()
res6 = mult_6(A, B)
t6_stop = datetime.now()
print('Duration mult_6: {}'.format(t6_stop-t6_start))
print('Duration mult_6: {}'.format(t6_stop-t6_start), file=L)

print('Duration mult_7: {}'.format(t7_stop-t7_start))
print('Duration mult_7: {}'.format(t7_stop-t7_start), file=L)

print("")
print("", file=L)


print("\nres1: \n", res1, file=L)
print("res2: \n", res2, file=L)
print("res3: \n", res3, file=L)
print("res4: \n", res4, file=L)
print("res5: \n", res5, file=L)
print("res6: \n", res6, file=L)
print("res7: \n", res7, file=L)

