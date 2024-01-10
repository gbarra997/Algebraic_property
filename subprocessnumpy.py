from os import environ
N_THREADS = '1'
environ['OMP_NUM_THREADS'] = N_THREADS
environ['OPENBLAS_NUM_THREADS'] = N_THREADS
environ['MKL_NUM_THREADS'] = N_THREADS
environ['VECLIB_MAXIMUM_THREADS'] = N_THREADS
environ['NUMEXPR_NUM_THREADS'] = N_THREADS
#For ensuring the fact the threads is only one I had to re define the function whole_numpy here, otherwise it would have imported the numpy module with respect to the file called functions.
import time
import numpy as np
from functions import whole_numpy
def whole_numpy(N,k,v):
    matA = np.random.randint(1, 100, size=(10, N, N))

    matB = matA * k
    start_time2 = time.time()
    A_B = np.matmul(matA, matB)
    B_A = np.matmul(matB, matA)
    end_time2 = time.time()
    elapsed_time2 = end_time2 - start_time2 
    if v == "y":
        print(f'A*B:\n{A_B}\n B*A:\n{B_A}\n They are the same: {np.allclose(A_B, B_A)}')

    return elapsed_time2



sizes = [200,400,800,1000,1200,1600,2000,2500,3000]
times_for_num_1 = []
k = 2
v = "n"
for elem in sizes:
    times_for_num_1.append(whole_numpy(elem, k, v))
print(times_for_num_1)

