import os
from collections import defaultdict 
import numpy as np
import random
import time
import math
from scipy.sparse import csr_matrix
from itertools import chain 
from pathlib import Path
import sys

# create toCSR
def readCSR(file):
    #Read in matrix from file adjecncy matrix or stuff provided from https://sparse.tamu.edu/
    path = Path(__file__).parent / str(file)
    with path.open() as fp:
        line = fp.readline()
        first_entry = False
        matrix_dict = {'size': {}}
        matrix = [[]]
        matrix_dict['name'] = file


        #Read in file. Skip non-essentail characters. Save information into a dict.
        while line:
            if line[0] == '%':
                line = fp.readline()
            else:
                if not first_entry:
                    first_entry = True
                    nums = line.split()
                    matrix_dict['size']['row'] = int(nums[0])
                    matrix_dict['size']['col'] = int(nums[1])
                    matrix_dict['size']['non_zero'] = int(nums[2])
                    matrix = [[0 for i in range(int(nums[1]))] for j in range(int(nums[0]))]   
                    line = fp.readline()
                else:
                    nums = line.split()
                    try:
                        matrix_dict[(int(nums[0]) -1, int(nums[1]) -1)] = float(nums[2])
                        matrix[int(nums[0]) -1][int(nums[1]) -1] = float(nums[2])
                    except:
                        matrix_dict[(int(nums[0]) -1, int(nums[1]) -1)] = 1
                        matrix[int(nums[0]) -1][int(nums[1]) -1] = 1
                    line = fp.readline()
    
    return matrix, matrix_dict
def generateCSR(matrix, matrix_dict):
    row_csr = []
    col_csr = []
    data_csr = []
    
    #From the dict, get csr values, col_csr, row_csr, data_csr
    row_csr = [0]* (int(matrix_dict['size']['row']) + 1)
    row_csr[int(matrix_dict['size']['row'])] = int(matrix_dict['size']['non_zero'])
    for row in range(0, int(matrix_dict['size']['row'])):
        for col in range(0, int(matrix_dict['size']['col'])):
            try:
                data_csr.append(matrix_dict[row,col])
                col_csr.append(col)
                if row != 0:
                    row_csr[row] = row_csr[row - 1] +  np.count_nonzero(matrix[row -1])
            except:
                continue

    correct_matrix = csr_matrix((data_csr, col_csr, row_csr), shape=(int(matrix_dict['size']['row']), int(matrix_dict['size']['col']))).toarray()
    
    print("\nMatrix Created from CSR (if small enough to print)")
    print(correct_matrix)
    
    return CSR_Matrix(matrix_dict['name'], row_csr, col_csr, data_csr, matrix_dict['size'])  
def testCSR(file, csrMatrix):
    
    matrix, matrix_dict = readCSR(file)
    
    scipy_matrix_array = csr_matrix((csrMatrix.data, csrMatrix.col, csrMatrix.row), shape=(csrMatrix.size['row'], csrMatrix.size['col'])).toarray()
    
    print("\ntesting dimensions")
    if csrMatrix.size['row'] != len(scipy_matrix_array):
        print("matrices row size do not match")
        exit()
    if csrMatrix.size['col'] != len(scipy_matrix_array[0]):
        print("matrices col size do not match")
        exit()
    print("OK")

    print("testing created CSR against scipy CSR")
    for row in range(0, matrix_dict['size']['row']):
        for col in range(0, matrix_dict['size']['col']):
            a = matrix[row][col]
            b = scipy_matrix_array[row][col]
        if a != b:
            print('mismatch in data')
            exit()
    print("OK")

    print("testing matrix times too long vector")
    vec = zeroMaker(csrMatrix.size['row']+ 1)
    vec[0] = 1
    new_vec = csrMatrix.multiply_vec(vec)
    print("OK")

    print("testing matrix times too short vector")
    vec = zeroMaker(csrMatrix.size['row'] - 1)
    vec[0] = 1
    new_vec = csrMatrix.multiply_vec(vec)
    print("OK")

    print("testing matrix times vector")
    vec = zeroMaker(csrMatrix.size['row'])
    vec[0] = 1
    new_vec = csrMatrix.multiply_vec(vec)
    print("OK")

    scipy_matrix = csr_matrix((csrMatrix.data, csrMatrix.col, csrMatrix.row), shape=(csrMatrix.size['row'], csrMatrix.size['col']))

    #need to finish this testing
    print("testing scipy dot equals result dot")
    scipy_vec = scipy_matrix.dot(vec)
    if(len(scipy_vec) != len(new_vec)):
        print('result vectors are not the same length')
        exit()
    for i in range(0, len(new_vec)):
        if new_vec[i] != scipy_vec[i]:
            print("dot products do not match!")
            exit()
    print("OK")

    #create transposed matrices
    tMatrix = csrMatrix.transpose()
    created_transpose = csr_matrix((tMatrix.data, tMatrix.col, tMatrix.row), shape=(tMatrix.size['row'], tMatrix.size['col'])).toarray()
    original_transpose = scipy_matrix.transpose().toarray()
    
    print('testing transposed dimensions')
    if tMatrix.size['row'] != len(scipy_matrix.transpose().toarray()) or tMatrix.size['col'] != len(scipy_matrix.transpose().toarray()[0]):
        print('tranposed dimensions are incorrect')
        exit()
    print("OK")

    print("Checking transposed scipy values against created transposed")
    for i in range(tMatrix.size['row']):
        for j in range(tMatrix.size['col']):
            if created_transpose[i][j] != original_transpose[i][j]:
                print("Transposed matrices are not the same!!")
                exit()
    print("OK")


    #matrix.multiply_vec(matrix)

# create matrix class
class CSR_Matrix:
    def __init__(self, name, row, col, data, size):
        self.name = name
        self.row = row
        self.col = col
        self.data = data
        self.size = size
    
    def print(self):
        print(self.name)
        print("row: ", self.row)
        print("col: ", self.col)
        print("data: ", self.data)
        print("size: ", self.size)

    # create matrix multiplication 
    # http://www.mathcs.emory.edu/~cheung/Courses/561/Syllabus/3-C/sparse.html <- Main idea taken from here
    #Still need to size check vector
    def multiply_vec(self, input):        
        result = np.zeros(len(input))
        
        if isinstance(input, list):
            
            #ensure size(col(A)) = size(row(B))
            if(len(input) != self.size['row']):
                print('input is not correct size')
                return

            for i in range(0, len(input)):
                for k in range(self.row[i], self.row[i+1]):
                    result[i] = result[i] + self.data[k] * input[ self.col[k]]
        else:
            print("input is not a vector")
            exit() 
            #ensure size(col(A)) = size(row(B))
            if(self.size['col'] != len(input)):
                print('input is not correct size')
                return

            #not implemented
                return
        return result
        
    # transpose
    def transpose(self):
        col_counter = 0
        new_row = []
        new_col = []
        new_data = []
        
        #create dict of lists
        pre_data = defaultdict(list)
        pre_col = defaultdict(list)

        for i in range(0, len(self.data)):
            pre_data[self.col[i]].append(self.data[i])
            pre_col[self.col[i]].append(i)

        new_row.append(0)
        for i in range(0, self.size['col']):
            new_data.append(pre_data[i])
            new_row.append((new_row[i] + len(pre_data[i])))
            new_col.append(pre_col[i])
        new_data = list(chain.from_iterable(new_data))
        new_col = list(chain.from_iterable(new_col))

        for i in range(0, len(new_col)):
            for j in range(0, len(self.row)):
                if new_col[i] < self.row[j+1]:
                    new_col[i] = j
                    break
                else:
                    continue

        #to account for zero rows we may need to add the nnz on the end of row for scipy tests
        if len(new_row) < self.size['col'] + 1:
            new_row.append(self.size['non_zero'])
        
        new_size = self.size
        new_size['col'] = self.size['row']
        new_size['row'] = self.size['col']

        return CSR_Matrix(self.name + ' tranposed', new_row, new_col, new_data, new_size)

def zeroMaker(n):
            listOfZeros = [0] * n
            return listOfZeros

def randomMaker(n):
    vec = zeroMaker(n)
    for i in range(0, len(vec)):
        vec[i] = random.randrange(0, 4)
    return vec

#Basis from http://mlwiki.org/index.php/Gram-Schmidt_Process#Python
def modified_qr_factorization(A, B):
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))
    print(B.ndim)

    if B.ndim == 1:
        Q[:,0] = B
    else:
        for i in range(B.shape[1]):
            Q[:,i] = B[:,i]

    for j in range(n):
        v = A[:, j]

        for i in range(j - 1):
            q = Q[:, i]
            R[i, j] = q.dot(v)
            v = v - R[i, j] * q

        norm = np.linalg.norm(v)
        Q[:, j] = v / norm
        R[j, j] = norm
    return Q, R

def main():
    file_name = sys.argv[1]
    print(file_name)
    matrix, matrix_dict = readCSR(file_name)
    A = generateCSR(matrix, matrix_dict)
    testCSR(file_name, A)

    b = zeroMaker(A.size['row'])
    b[0] = 1
    tolerance = pow(10, -6)
    maxIter = 5
    maxSearch = 15
    x = []
    r = zeroMaker(len(b))
    pVectors = np.zeros((A.size['row'], maxSearch))
    Q = np.zeros((A.size['row'], A.size['row']))
    R = np.zeros((A.size['row'], A.size['row']))
    alpha = [0 for i in range(maxSearch)]

    #initalize x
    x = zeroMaker(A.size['col'])
    
    print('x\n', x)
    #Compute r
    for i in range(0, len(b)):
        r[i] = b[i] - A.multiply_vec(x)[i]
    print("r: \n", r)

    #compute res_norm
    res_norm = np.linalg.norm(r)

    #1/||r|| * r
    pVectors[:,0] = np.multiply((1/res_norm), r)
    
    A_array = csr_matrix((A.data, A.col, A.row), shape=(A.size['row'], A.size['col'])).toarray()
    for i in range(maxIter):
        print('Restart ------------------------------')
        #restart
        #||r||
        r_norm = np.linalg.norm(r)

        #1/||r|| * r
        P = np.multiply((1/res_norm), r)

        #B = A(p1)
        B = (A.multiply_vec(list(P)))

        print("B\n", B)
        #loop
        print('P\n', P)
        for j in range(maxSearch-1):
            if B.ndim == 1:
                
                p_new = np.array(A.size['row']) 
                c = np.dot(np.transpose(P), r)
                p_new = np.subtract(r, np.multiply(c, P))
                p_new_norm = np.linalg.norm(p_new)

                P = np.transpose(np.vstack((P, np.multiply(1/p_new_norm, p_new))))
                B = np.transpose(np.vstack((B, A.multiply_vec(list(P[:,1])))))

                mu = np.linalg.norm(r)
                if mu < tolerance*res_norm:
                    exit()

            else:
                #Lease Squares
                Q, R = np.linalg.qr(B)
                Q_t = np.transpose(Q)
                beta = np.dot(Q_t, r)
                alpha = np.linalg.solve(R, beta)

                #compute next iterate 
                x = np.add(x, P@alpha)

                #compute next residual 
                r = np.subtract(r, B@alpha)

                #computer residual norm
                r_norm = np.linalg.norm(r)

                #check for convergence 
                if r_norm < res_norm*tolerance:
                    print('converged!')
                    exit()
                
                p_new = np.array(A.size['row'])                
                #compute next search direction
                for k in range(P.shape[1] if P.ndim > 1 else 1):
                    c = np.dot(np.transpose(P[:,k]), r)
                    p_new = np.subtract(r, np.multiply(c, P[:,k]))
                p_new_norm = np.linalg.norm(p_new)
                P = np.transpose(np.vstack((np.transpose(P),np.multiply(1/p_new_norm, p_new))))
                B = np.transpose(np.vstack((np.transpose(B),A.multiply_vec(list(P[:,k])))))
    
    
if __name__ == "__main__":
    main()