import os
from collections import defaultdict 
import numpy as np
from scipy.sparse import csr_matrix

def testCSR(matrix):
    spicy_matrix = csr_matrix((matrix.data, matrix.col, matrix.row), shape=(matrix.size['row'], matrix.size['col'])).toarray()
    print("testing dimensions")
    if matrix.size['row'] != len(spicy_matrix):
        print("shit")
        exit()
    if matrix.size['col'] != len(spicy_matrix[0]):
        print("shit")
        exit()
    print("OK")

    print("testing matrix times vector")
    vec = zeroMaker(matrix.size['row'])
    vec[0] = 1
    new_vec = matrix.multiply_vec(vec)

    spicy_matrix = csr_matrix((matrix.data, matrix.col, matrix.row), shape=(matrix.size['row'], matrix.size['col']))

    spicy_vec = spicy_matrix.dot(vec)
    print(vec)
    print(spicy_vec)

    #matrix.multiply_vec(matrix)
    print("I'm proud of you")   

# create toCSR
def readCSR(file):
    #Read in matrix from file adjecncy matrix or stuff provided from https://sparse.tamu.edu/
    with open ('/Users/brianallen/Desktop/Projects/GMRES/cage3.mtx') as fp:
        line = fp.readline()
        row_csr = []
        col_csr = []
        data_csr = []
        row_num = 1
        first_entry = False
        matrix_dict = {'size': {}}
        matrix = [[]]
        

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
                    matrix = [[0 for i in range(int(nums[0]))] for j in range(int(nums[1]))]   
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

        print("row: ", row_csr)  
        print("col: ", col_csr, " ", len(col_csr))
        print("data ", data_csr, " ", len(data_csr))

        print(matrix_dict)

        correct_matrix = csr_matrix((data_csr, col_csr, row_csr), shape=(int(matrix_dict['size']['row']), int(matrix_dict['size']['col']))).toarray()
        
        print("testing file versus created matrix with spicy")
        count = 0
        row = 0
        for row in range(0, matrix_dict['size']['row']):
            for col in range(0, matrix_dict['size']['col']):
                a = matrix[row][col]
                b = correct_matrix[row][col]
            if a != b:
                print('shit')
                exit()
        print("OK")
        return CSR_Matrix(str(file), row_csr, col_csr, data_csr, matrix_dict['size'])  

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
    def multiply_vec(self, vec):        
        result = zeroMaker(len(vec))
        
        for i in range(0, len(vec)):
            for k in range(self.row[i], self.row[i+1]):
                result[i] = result[i] + self.data[k] * vec[ self.col[k]]
        print(result)
        return result
        
# transpose
    def transpose(self):
        col_counter = 0
        new_row = []
        new_col = []
        new_data = []
        
        pre_data = defaultdict(list)

        #create dict of data to concat later

        for i in range(0, len(self.data)):
            pre_data[self.col[i]].append(self.data[i])

        print(pre_data)
# returnTranspose
    def returnTranspose(self):
        return 'not implemented'

# A * vector, A-transpose * vector

# CSR

# CSR Transpose with minimal ops

# A(CSR) * B(CSR) = C(CSR)

def zeroMaker(n):
            listOfZeros = [0] * n
            return listOfZeros

def main():
    matrix = readCSR('cage3')
    testCSR(matrix)

    


if __name__ == "__main__":
    main()