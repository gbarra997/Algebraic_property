import os
import time
import numpy as np
import random 
import argparse
import multiprocessing


###### Checker for argparse - Dimension 
def positive_integer_checker(value):
    try:
        int_value = int(value)
        if int_value <= 0:
            raise argparse.ArgumentTypeError("Value must be a positive integer")
        elif int_value <= 1:
            raise argparse.ArgumentTypeError("A matrix must be at least 2x2, please provide an integer >= 2")
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid input. Please provide a positive integer as dimension parameter")

###### Checker for argparse - Scalar

def scalar_checker(scal):
    try:
        value = float(scal)
        if value.is_integer():
            return int(value)
        else:
            return value
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid input. Please provide an integer or float as scalar factor parameter")

###### Checker for argparse - Right path

def check_save_file(value):
    if value:
        if os.path.exists(value):
            return value
        else:
            raise argparse.ArgumentTypeError("Invalid path provided for saving file. Please provide a valid path.")
    else:
        return None




###### Functions for sequential process

##Create a random matrix
def create_random_matrix(rows, cols):
    matrix = [[random.randint(1, 100) for _ in range(cols)] for n in range(rows)]
    return matrix
##Multiply it for a scalar
def matrix_times_scalar(matrix, scalar):
    matrix = [[scalar * x for x in inner] for inner in matrix ]
    return matrix
##Computer the matrix multiplication
def mat_multiplication(matrix_1, matrix_2):
    result = []
    for i in range(len(matrix_1)):
        row = []
        for j in range(len(matrix_2[0])):
            value = 0
            for k in range(len(matrix_2)):
                value += matrix_1[i][k] * matrix_2[k][j]
            row.append(value)
        result.append(row)
    return result
# Test if they are equal or not 
def test(matrix_1, matrix_2):
    if len(matrix_1) != len(matrix_2) or len(matrix_1[0]) != len(matrix_2[0]):
        return False

    for i in range(len(matrix_1)):
        for j in range(len(matrix_1[0])):
            if matrix_1[i][j] != matrix_2[i][j]:
                return False
    return True

#General function for a sequential process
def fun_for_sequential(N,k,v):
    matA = create_random_matrix(N, N)
    matB = matrix_times_scalar(matA, k)
    start_time1 = time.time() 
    A_B = mat_multiplication(matA, matB)
    B_A = mat_multiplication(matB, matA)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1 

    if v == "y":
        if len(matA)<=10:
            print("A*B:\n")
            for elem in range(N):
                print( A_B[elem],'\n')
            print("B*A:\n")
            for elem in range(N):
                print(B_A[elem],'\n')
        else:
            print(f"A*B:\n[{A_B[0][0]}.........{A_B[0][N-1]}\n{A_B[N-1][0]} .........{A_B[N-1][N-1]}]")
            print(f"B*A:\n[{B_A[0][0]}.........{B_A[0][N-1]}\n{B_A[N-1][0]} .........{B_A[N-1][N-1]}]")    
            print("Are equal?:",test(A_B, B_A))    
    else:
        return elapsed_time1



#General function using only Numpy
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



#MULTIPROCESSING
#Split the matrix according the given processes 
def split_and_check(data):
    matA, matB = data
    A_B = np.matmul(matA, matB)
    B_A = np.matmul(matB, matA)
    return np.allclose(A_B, B_A)
#Function to perform multiprocessing 
def multi_process(N,k, p,v):
    if p:
        pass
    else:
        p = multiprocessing.cpu_count()-1
    matA = np.random.randint(1, 100, size=(10, N, N))
    matB = matA * k
    split_matA = np.array_split(matA, p)
    split_matB = np.array_split(matB, p)

    if v == "y":
        for A_B, B_A in zip(split_matA, split_matB):
            print(f"A*B=\n{np.matmul(A_B, B_A)}\nB*A=\n{np.matmul(B_A, A_B)}\n")

    test_data = list(zip(split_matA, split_matB))
    start_time = time.time()
    with multiprocessing.Pool(p) as pr:
        results = pr.map(split_and_check, test_data)
    end_time = time.time()
    elapsed_time = end_time - start_time 
    return elapsed_time





