import os
import sys
import time
import argparse
import functions
import subprocess
import multiprocessing
import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser(description="MATRIX EQUALITY TEST: Test the differences of speed in the alogritmhs")

parser.add_argument("-sv", "--save_file", type=functions.check_save_file,
                    default=os.getcwd(),
                    help="Directory path to save the results. A picture for each modality and a dataset will be saved in the current working directory or in a given one")




args = parser.parse_args()
save_directory = args.save_file  # Assuming args.save_file is the directory path

if __name__ == "__main__":
    v = "n"
    sizes = [200,400,800,1600,2400,2500,2800]
    size_seq = [10,50,100,150,200,250,300]
    times_for_seq = []
    times_for_num = []
    times_for_multi = {_ : [] for _ in range(1, multiprocessing.cpu_count())}  # Dictionary to store times for different number of processes
    k = 2
    #RUN SEQUENTIAL

    print("Sequential")
    for elem in size_seq:
        print(f'Testing with {elem} size')
        start_time1 = time.time() 
        for _ in range(1,11):
            functions.fun_for_sequential(elem,k,v)
            end_time1 = time.time()
            times_for_seq.append(end_time1 - start_time1 )


    #RUN NUMPY MULTI THREAD
    print("Normal Numpy")
    for elem in sizes:
        print(f'Testing with {elem} size')
        times_for_num.append(functions.whole_numpy(elem,k,v))

    #RUN NUMPY ONE THREAD
    print("Numpy with only 1 thread")
    python_executable = sys.executable
    processo = subprocess.Popen([python_executable, 'subprocessnumpy.py'], stdout=subprocess.PIPE, text=True)
    output, _ = processo.communicate()
    output = output.strip("[]\n").split(",")
    times_for_num_1 = [float(elem) for elem in output]


    #RUN MULTIPROCESS
    print("Multiprocess")
    for elem in sizes:
        print(f'Testing with {elem} size')
        for processi in range(1, multiprocessing.cpu_count()):
            times = functions.multi_process(elem, k, processi, v)
            times_for_multi[processi].append(times)


 # Plotting and saving the results for each list

    # Plot and save for Sequential

    plt.figure(figsize=(10, 6))
    plt.plot(size_seq,times_for_seq, label="Sequential", marker='o')
    plt.ticklabel_format(style='plain')    # to prevent scientific notation.
    plt.xlabel('Sizes')
    plt.ylabel('Time')
    plt.title('Sequential Algorithm Execution Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_directory, 'sequential_plot.png'))
    plt.close()

    # Plot and save for Numpy
       # Plotting and saving the results for Numpy and Numpy1 in a single plot
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times_for_num, label="Numpy", marker='o')
    plt.plot(sizes, times_for_num_1, label="Numpy1", marker='o')  # Aggiungi la seconda linea per Numpy1
    plt.ticklabel_format(style='plain')    # per evitare la notazione scientifica.
    plt.xlabel('Sizes')
    plt.ylabel('Time')
    plt.title('Numpy and Numpy1 Algorithm Execution Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_directory, 'numpy_combined.png'))
    plt.close()

    # Plotting and saving the results for Multiprocessing in a single plot
    plt.figure(figsize=(10, 6))
    num_colors = len(times_for_multi)
    colors = [plt.cm.jet(i / num_colors) for i in range(num_colors)]
    for i, (key, values) in enumerate(times_for_multi.items()): 
        plt.ticklabel_format(style='plain')    # to prevent scientific notation.
        plt.plot(sizes, values, label=key, color=colors[i])

    plt.xlabel('Sizes')
    plt.ylabel('Values')
    plt.title('Lines for Each Key with Sizes as X-axis (Different Colors)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_directory, 'multiprocessing.png'))
    plt.close()
     # Create a DataFrame
    data = {
        'Sequential': times_for_seq,
        'Numpy': times_for_num,
        'Numpy_1': times_for_num_1
    }
    for processi, times in times_for_multi.items():
        data[f'Multiprocessing_{processi}'] = times

    df = pd.DataFrame(data)
    df.to_csv(os.path.join(save_directory, 'execution_times.csv'), index=False)

