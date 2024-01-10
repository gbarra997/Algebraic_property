# Algebraic_property
This project evaluates how different types of processes can deal with matrix multiplication.
Mathematically speaking, the product of two matrices is not always commutative. In a few specific case, it can be known in advance, but as for the nature of the matrix multiplication (row*colum) itself, it cannot be taken for granted that A*B == B*A.
One specific case is when B = A * k, i.e. when B is the result of matrix A multiplied by a scalar, then the product of A, B and B, A is the same. 

The "Test_algebraic_properties.py" is a code that aims to test this algebraic properties and also verify it in different modalities. The user can provide several inputs:
* Dimension of the matrix you want to test. It will generate a D*D matrix. It can be every positive number ≥ 2. 
* Scalar: Any number
* Modality: The script can run three different modalities:
  1. Fully **sequential**: It employs only loops and simple operations. Therefore, it is very slow. Don't provide a dimension greater than 200 unless you don't want to spend ages waiting
  2. **Numpy**: It only uses numpy function. It's known that numpy employs multithreading strategies managing to release the GIL, therefore it can handle easily big matrices
  3. **Multiprocessing**: It will create several parallel and independent processes equal to the number you provide. Each matrix will be split into several parts and each will be
    * If you select this mode you can also insert the p (process) parameter to select the number you
      want. If none, the max available will be used. 
* The last parameter is "verbose", whether you can print the output of the process or just the time.


The "Test_performance.py" is a code that aims to test how different implementations work with matrix multiplications. At the end, the code will provide three plots, one for each modality, and a data frame with the recorded time. There are 4 main implementations: 
1. Parallel: Only loops. For this mode, the size of the matrix will be smaller due to the extremely low and time-consuming code.
2. Numpy with multi-threads
3. Numpy with only one thread
4. Multiprocessing aims to find the best number of processes that can speed up this calculation. It is not easy to state wether more or less processes are better. It usually depends on the computational complexity, in this case, the dimension of the matrix. Employing 10 processes for a 2*2 matrix is not the best strategy, since it would take more to create them instead of performing these multiplications. 
The user can provide:
* The directory where to save the picture. If not, the files will be saved in the script folder
