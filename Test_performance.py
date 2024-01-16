



#####################################################################
#                       Performance Tester                          #
# This script conducts a performance test by computing the matrix   #
# product of ten random matrices. The goal is to evaluate the       #
# performance of the following approaches:                          #
#   - "One-threaded" sequential (basic Python commands)             #
#   - Multithreaded (utilizing NumPy, that relies on an accelerated #
#     linear algebra library, typically Intel MKL or OpenBLAS)      #
#   - Parallelized mono and multithreaded (leveraging NumPy's       #
#     capability to send parallelized processes to multiple cores)  #
#####################################################################





#IMPORT MODULES 
#To force the enviroment to work with only one thread we have to set these variable before calling the necessary functions
import os
N_THREADS = '1'
os.environ['MAX_THREADS'] = N_THREADS               
os.environ['OMP_NUM_THREADS'] = N_THREADS           # Since it would be more complex to get the actual version you are using,
os.environ['OPENBLAS_NUM_THREADS'] = N_THREADS      # I set the variable for all the possibilities       
os.environ['MKL_NUM_THREADS'] = N_THREADS          
os.environ['VECLIB_MAXIMUM_THREADS'] = N_THREADS
os.environ['NUMEXPR_NUM_THREADS'] = N_THREADS
import sys
import time
import argparse
import functions 
import subprocess
import multiprocessing
import matplotlib.pyplot as plt
import pandas as pd


#IMPORT INPUT
#Using argparser the user can set the input, the directory to save the results

parser = argparse.ArgumentParser(description="MATRIX EQUALITY TEST: Test the differences of speed in the alogritmhs") 

parser.add_argument("-sv", "--save_file", type=functions.check_save_file,
                    help="Directory path to save the results. A picture for each modality and a dataset will be saved in the current working directory or in a given one")


args = parser.parse_args()
save_directory = args.save_file

args = parser.parse_args()
save_directory = args.save_file

if save_directory is not None:
    pass
else:
    save_directory = os.path.join(os.getcwd(), "results")
    os.makedirs(save_directory, exist_ok=True)

if __name__ == "__main__":                                            #To run the py file
    SET_OF_DIMENSION = [[50,100,200,400],[500,1000,2000,4000]]        #Dimensions to test
    
    RECORDS_FOR_SEQUENTIAL = []                                       #Lists/dict to save the results of the test
    RECORDS_FOR_NUMPY_1THREAD = []
    RECORDS_FOR_NUMPY_MULTI_THREAD = []
    RECORDS_FOR_NUMPY_PARALLELIZED = {_ : [] for _ in range(1, multiprocessing.cpu_count())}  
    python_executable = sys.executable

    #RUN SEQUENTIAL
    print("Sequential")
    for elem in SET_OF_DIMENSION[0]:
        print(f'Testing with {elem} size')
        rec = functions.fun_for_sequential(elem)                                        #The fun_for_sequential that is in functions module create ten matrix and verify the algebraic properties
        RECORDS_FOR_SEQUENTIAL.append(rec)
    

    #RUN NUMPY ONE THREAD
    print("Numpy with one threads")
    for elem in SET_OF_DIMENSION[1]:
        print(f'Testing with {elem} size')
        RECORDS_FOR_NUMPY_1THREAD.append(functions.whole_numpy(elem))


    #NUMPY MULTI
    print("Numpy with multiple threads")
    for elem in SET_OF_DIMENSION[1]:
        print(f'Testing with {elem} size')
        processo = subprocess.Popen([python_executable, 'subprocessnumpy.py',str(elem)], stdout=subprocess.PIPE, text=True)
        output, _ = processo.communicate()
        RECORDS_FOR_NUMPY_MULTI_THREAD.append(float(output))
        processo.terminate()
        processo.wait()

    #RUN REAL PARALLELIZED MULTIPROCESS
    print("Multiprocess")

    for elem in SET_OF_DIMENSION[1]:
        print(f'Testing with {elem} size')
        for processi in range(1, multiprocessing.cpu_count()):
            print(f'Testing with {processi} number of process')
            times = functions.multi_process(N=elem, p=processi)
            RECORDS_FOR_NUMPY_PARALLELIZED[processi].append(times)

    # Plot and save for Sequential, Numpy, Numpy1, and Multiprocessing
    plt.figure(figsize=(15, 10))
    # Sequential
    plt.plot(SET_OF_DIMENSION[0], RECORDS_FOR_SEQUENTIAL, label="Sequential", marker='o')
    # Numpy and Numpy1
    plt.plot(SET_OF_DIMENSION[1], RECORDS_FOR_NUMPY_1THREAD, label="Numpy one threads", marker='o')
    plt.plot(SET_OF_DIMENSION[1], RECORDS_FOR_NUMPY_MULTI_THREAD, label="Numpy multiple threads", marker='o')
    # Multiprocessing
    num_colors = len(RECORDS_FOR_NUMPY_PARALLELIZED)
    colors = [plt.cm.jet(i / num_colors) for i in range(num_colors)]
    for i, (key, values) in enumerate(RECORDS_FOR_NUMPY_PARALLELIZED.items()):
        plt.plot(SET_OF_DIMENSION[1], values, label=f"Multiprocessing ({key} processes)", color=colors[i], linestyle='dashed')

    plt.ticklabel_format(style='plain')  # to prevent scie]]ntific notation.
    plt.xlabel('Dimension')
    plt.ylabel('Time (s)')
    plt.title('Algorithm Execution Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_directory, 'combined_plot.png'))
    plt.close()
    # Create a DataFrame

    data = {
        'Sequential':RECORDS_FOR_SEQUENTIAL,
        'Numpy': RECORDS_FOR_NUMPY_1THREAD,
        'Numpy_1': RECORDS_FOR_NUMPY_MULTI_THREAD        }

    for processi, times in RECORDS_FOR_NUMPY_PARALLELIZED.items():
        data[f'Multiprocessing_{processi}'] = times

    df = pd.DataFrame(data)
    df.to_csv(os.path.join(save_directory, 'execution_times.csv'), index=False)
