Author: Giuseppe Barranco
ID: 985853 
# This is a project written in Python for the course "Scientific Programming". Master's degree in Bioinformatics for computational genomics



# Test_algebraic_properties.py


This project evaluates how different types of processes can deal with matrix multiplication.
Mathematically speaking, the product of two matrices is not always commutative. In a few specific cases, it can be known in advance, but as for the nature of the matrix multiplication (row*colum) itself, it cannot be taken for granted that A*B == B*A.
One specific case is when B = A * k, i.e. when B is the result of matrix A multiplied by a scalar, then the product of A, B and B, A is the same. 

The "Test_algebraic_properties.py" is a code that aims to test this algebraic property and verify it in different modalities. Generally it creates 10 random squared matrices of the given dimension, multiply them for a scalar and then test if are the same. 
The user can provide several inputs:
* -d Dimension of the matrix you want to test. It will generate a D*D matrix. It can be every positive number ≥ 2. 
* -k Scalar: Any number
* -m Modality: The script can run three different modalities:
  1. -s Fully **sequential**: It employs only loops and simple operations. Therefore, it is very slow. Don't provide a dimension greater than 200 unless you don't want to spend ages waiting
  2. -n **Numpy**: It only uses the numpy function. It's known that numpy employs multithreading/multiprocessing strategies managing to release the GIL, therefore it can easily handle big matrices
  3. -m **Multiprocessing**: It will create parallel and independent processes equal to the number you would provide. Each matrix will be split and each piece tested in a different process. These processes will share the available CPU. Since it employs numpy, if you provide, for example, 7 processes, then each process will have one thread so all the CPU will likely be involved. 
    * -p If you select this mode you can also insert the p (process) parameter to select the number you
      want. If none, the max available will be used. 
* -v The last parameter is "verbose", whether you can print the output of the process or just the time.

# Test_performance.py



The "Test_performance.py" is an additional code that aims to test how different implementations work with matrix multiplications. The process is the same as above, 10 random squared matrix of given dimensions: Sequential 50,100,200,400 and for the rest 500,1000,2000,4000. In the end, the code will provide one plot with several lines, one for each modality. The x axis represents the dimensions and the y axis the time in second. A data frame with the recorded time is also produced.
Normally python cannot go for multithreading or multiprocessing unless specific packages are used. So it uses only one thread.
There are 4 main implementations: 
1. Sequential: Only loops. For this mode, the size of the matrix will be smaller due to the extremely "trivial" and time-consuming code.
2. Numpy with only one thread: Since the constraint is defined at the beginning of the code, numpy cannot use multiplethreads so it has to work with one only. 
3. Numpy with multi-threads: This will create one different and independent process and Numpy will use all the available resources.
4. Multiprocessing aims to find the best number of processes to speed up this calculation. It is not easy to state whether more or less processes are better. It usually depends on the computational complexity, in this case, the dimension of the matrix. Employing 10 processes for a 2*2 matrix is not the best strategy, since it would overhead.

The user can provide:
* -sv The directory where to save the picture. If not, the files will be saved in the script folder. 




# Outcome

What we would expect is: 
1. the sequential is terribly slow.
2. The numpy with one thread and the 1 thread parallel multiprocessing should have a similar time since they have the same resource in terms of CPU so they cannot parallelize the process.
3. Given that in this setting Numpy would always be the fastest also for the further hidden implementation, we would expect that the parallel methods with the higher number should be the faster, at least like numpy. That is indeed true but not always. For smaller matrices, it is not worth it to create more than x processes because the time to create and manage them would be probably more than what is required for the computation itself.


# Notes
To work with only one thread, that is,  forcing the libraries (BLAS, Openblas,..) numpy depends on, I had to define an additional script file (subprocessnumpy.py). In this script, I invoke the very same function ("numpy_only") but with a different name of threads, otherwise, as a child process, it would have used the same setting as the parent process.

