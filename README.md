# Algebraic_property
This is project evaluate how different type of process can deal with matrix multiplication.
Mathematically speaking, the product of two matrices is not alway commutative. In few specific case it can be known in advance, but as for the nature of the matrix multiplication (row*colum) itself, it cannot be taken for granted that A*B == B*A.
One specific case is when B = A * k, i.e. when B is the result of matrix A multiplied by a scalar, then the product of A,B and B,A is the same. 

The "Test_algebraic_properties" is a code in which the user can provide several input:
* Dimension of the matrix you want to test. It will generate a D*D matrix. It can be every positive number ≥ 2. 
* Scalar: Any number
* Modality: The script can run three different modalities:
  1. Fully **sequential**: It employes only loops and simple operations. Therefore is very slow. Don't provide dimension greater than 200 unless you don't want to spend ages waiting
  2. **Numpy**: It only uses numpy function. It's known that numpy employ itself multithreading strategies managing to release the GIL, therefore it can handle easely big matrices
  3. **Multiprocessing**: It will create a number of paraller and indipendent processes equal to your the number you provide. Each matrix will be splitted in several parts and each will be
    * If you select this mode you can also insert the p (process) parameter to select the number you
      want. If none, the max available will be used. 
* The last parameter is "verbose", wether you can print the output of the process or just the time.


