import sys
import os
N_THREADS = str(os.cpu_count()-1)
os.environ['MAX_THREADS'] = N_THREADS
os.environ['OMP_NUM_THREADS'] = N_THREADS
os.environ['OPENBLAS_NUM_THREADS'] = N_THREADS
os.environ['MKL_NUM_THREADS'] = N_THREADS
os.environ['VECLIB_MAXIMUM_THREADS'] = N_THREADS
os.environ['NUMEXPR_NUM_THREADS'] = N_THREADS
#For ensuring the fact the threads is only one I had to re define the function whole_numpy here, otherwise it would have imported the numpy module with respect to the file called functions.
from functions import whole_numpy
if __name__ == "__main__":
    N = int(sys.argv[1])
    result = whole_numpy(N)
    print(result)
