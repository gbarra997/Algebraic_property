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
    matrix = [[random.random() for _ in range(cols)] for n in range(rows)]
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
    for i in range(len(matrix_1)):
        for j in range(len(matrix_1[0])):
            if float('{:f}'.format(matrix_1[i][j])) != float('{:f}'.format(matrix_2[i][j])):
                return False
    return True

#General function for a sequential process
def fun_for_sequential(N,k = 2,v = "n"):
    start_time1 = time.time() 
    for _ in range(1,11):        
        matA = create_random_matrix(N, N)
        matB = matrix_times_scalar(matA, k)
        A_B = mat_multiplication(matA, matB)
        B_A = mat_multiplication(matB, matA)

        if v == "y":
            if len(matA)<=10:
                print(f"Matrix n° {_}")
                print("A*B:\n")
                for elem in range(N):
                    print( A_B[elem],'\n')
                print("B*A:\n")
                for elem in range(N):
                    print(B_A[elem],'\n')
                print("Are equal?:",test(A_B, B_A), end="\n") 
            else:
                print(f"Matrix n° {_}")
                print(f"A*B:\n[{A_B[0][0]}.........{A_B[0][N-1]}\n{A_B[N-1][0]} .........{A_B[N-1][N-1]}]")
                print(f"B*A:\n[{B_A[0][0]}.........{B_A[0][N-1]}\n{B_A[N-1][0]} .........{B_A[N-1][N-1]}]")    
                print("Are equal?:",test(A_B, B_A))    

    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1 
    return elapsed_time1



#General function using only Numpy
def whole_numpy(N,k=2,v="n"):
    start_time2 = time.time()
    for elem in range(1,11):
        matA = np.random.random((N, N))
        matB = matA * k
        A_B = np.matmul(matA, matB)
        B_A = np.matmul(matB, matA)
        if v == "y":
            print(f'A*B:\n{A_B}\n B*A:\n{B_A}\n They are the same: {np.allclose(A_B, B_A)}')
    end_time2 = time.time()
    elapsed_time2 = end_time2 - start_time2 
    return elapsed_time2



#MULTIPROCESSING
#Split the matrix according the given processes 
def split_and_check(data):
    A_B = np.matmul(data[0], data[1])
    B_A = np.matmul(data[1], data[0])
    return np.allclose(A_B, B_A)
#Function to perform multiprocessing 

def multi_process(N,k=2, p=multiprocessing.cpu_count()-1,v="n"):
    matA = np.random.random(size=(10, N, N))
    matB = matA * k
    split_matA = np.array_split(matA, p)
    split_matB = np.array_split(matB, p)

    if v == "y":
        for A_B, B_A in zip(split_matA, split_matB):
            print(f"A*B=\n{np.matmul(A_B, B_A)}\nB*A=\n{np.matmul(B_A, A_B)}\nThese matrices are equal")

    test_data = list(zip(split_matA, split_matB))
    start_time = time.time()
    with multiprocessing.Pool(p) as pr:
        results = pr.map(split_and_check, test_data)
    end_time = time.time()
    elapsed_time = end_time - start_time 
    return elapsed_time





