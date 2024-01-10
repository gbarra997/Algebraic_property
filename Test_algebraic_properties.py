
import argparse
import multiprocessing
import time
import functions
parser = argparse.ArgumentParser(description="MATRIX EQUALITY: This program verifies whether, given two matrices A and B where B = k*A for some scalar k, the matrix multiplication is commutative. This can be demonstrated by exploiting the associative property of matrix multiplication. Given B = k*A we can express the matrix multiplication as follows: A * A * k = A * A * k. Using the associative property, we rearrange this expression to (A**2) * k = (A**2) * k. This demonstrates that in this specific case, the matrix multiplication indeed satisfies the commutative property. ")
parser.add_argument("-d", "--dimension", type=functions.positive_integer_checker, required=True, help="Size of the square matrices. Any integer >=2")

parser.add_argument("-k", "--scalar_factor", type=functions.scalar_checker, required=True, help="Scalar factor. Any number, integer, float, positive or negative")

parser.add_argument("-m","--modality",choices=['n','numpy','s', 'sequential', 'm', 'multi'], type=str, required=True, help="Type 's' or 'sequential' for sequential. Type 'n' or 'numpy' for using only numpy. Type 'm' or 'multi' for multiprocessing")

parser.add_argument("-p","--process", nargs='?', const='0', type=int, choices=list(range(1,multiprocessing.cpu_count())), help="Number of process to run on multiprocess way")

parser.add_argument("-v","--verbose", nargs='?', const='n', choices=['y', 'n'], type=str, help="Insert y or n. Do you want to print the matrix multiplication. Default set to: n")
args = parser.parse_args()
N = args.dimension
k = args.scalar_factor
path = args.save_file
m = args.modality
v = args.verbose
p = args.process

if p != None and m in ["s","sequential","n","numpy"]:
     parser.error("-p/--process argument cannot be used with sequential or numpy modes.")



if __name__ == "__main__":



    
    ############################################################
    ### Sequential i.e. only using loop and bultin functions ###
    ############################################################
    if m == "sequential" or m == "s":
        start_time1 = time.time() 
        for _ in range(1,11):
            print("\n\nMatrix number:", _)
            functions.fun_for_sequential(N,k,v)
        end_time1 = time.time()
        print("These matrix are equal")
        elapsed_time1 = end_time1 - start_time1 
        print(f'The entire process using sequential code only (no external modules) took: {elapsed_time1}')
        
    ################################################################
    ### Using Numpy only i.e. exploiting built in "multithreads" ###
    ################################################################
    if m == "numpy" or m == "n":
        print(f'The entire process using numpy took: {functions.whole_numpy(N,k,v)}')
 
#Multithreading is used by the numpy library by default to speed up matrix operations. While not all functions have multiple threads, those that compute matrices do. The fact that numpy is able to release the GIL is the cause. To get more specific, we can state that numpy uses libraries for algebraic comutational processes, such as BLAS and LAPACK. They are typically developed in programming languages that have the ability to release the GIL and handle multithreading properly. As our goal is essentially to do two matrix calculations, we can show how multithreading expedites the procedure.
#As stated before, Numpy can bypass the GIL but we could have tested the difference reloading the numpy module after running these lines below. They force to use the specified number of threads. Checking on the task-manager we would see that setting N_THREADS = '1' let python run, numpy tasks in only one threads, while normally we would expect an higher number. We can set even 1000 the os would manage a reasonable number according to the resources. 
#import environ from os
#del numpy
#N_THREADS = '10'
#environ['OMP_NUM_THREADS'] = N_THREADS
#environ['OPENBLAS_NUM_THREADS'] = N_THREADS
#environ['MKL_NUM_THREADS'] = N_THREADS
#environ['VECLIB_MAXIMUM_THREADS'] = N_THREADS
#environ['NUMEXPR_NUM_THREADS'] = N_THREADS
# import numpy
#Quelle: https://scipy-cookbook.readthedocs.io/items/ParallelProgramming.html
#https://superfastpython.com/numpy-number-blas-threads/

#########################################################################################
### Multiprocessing: As the number of threads is > 10, assigning each pair of matrices###
### to a single process is not a valid solution, as some processes will be unused.    ###
### Therefore we need to split out tasks in multiple subtasks such that we can employ ###  
### all process                                                                       ###
#########################################################################################
    if m == "multi" or m == "m":
            functions.multi_process(N,k,p,v)