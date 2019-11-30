import os
from collections import defaultdict 
import numpy as np
from scipy.sparse import csr_matrix
from itertools import chain 

# create toCSR
def readCSR(file):
    #Read in matrix from file adjecncy matrix or stuff provided from https://sparse.tamu.edu/
    with open ('/Users/brianallen/Desktop/Projects/GMRES/brian.mtx') as fp:
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
        
        print("\n \ntesting file versus created matrix with spicy")
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
        print(correct_matrix)
        return CSR_Matrix(str(file), row_csr, col_csr, data_csr, matrix_dict['size'])  



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

    print("testing matrix times too long vector")
    vec = zeroMaker(matrix.size['row']+ 1)
    vec[0] = 1
    new_vec = matrix.multiply_vec(vec)

    print("testing matrix times too short vector")
    vec = zeroMaker(matrix.size['row'] - 1)
    vec[0] = 1
    new_vec = matrix.multiply_vec(vec)

    print("testing matrix times vector")
    vec = zeroMaker(matrix.size['row'])
    vec[0] = 1
    new_vec = matrix.multiply_vec(vec)

    

    spicy_matrix = csr_matrix((matrix.data, matrix.col, matrix.row), shape=(matrix.size['row'], matrix.size['col']))

    spicy_vec = spicy_matrix.dot(vec)
    print(new_vec)
    print(spicy_vec)

    print('\n\n')
    tMatrix = matrix.transpose()

    if matrix.size['row'] != matrix.size['col']:
        print('Matrix is not nxn and will not work for GMRES')
        exit()

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
        result = zeroMaker(len(input))
        
        if isinstance(input, list):
            #ensure size(col(A)) = size(row(B))
            if(len(input) != self.size['row']):
                print('input is not correct size')
                return

            for i in range(0, len(input)):
                for k in range(self.row[i], self.row[i+1]):
                    result[i] = result[i] + self.data[k] * input[ self.col[k]]
            print(result)
        else:
            #ensure size(col(A)) = size(row(B))
            if(self.size['col'] != len(input)):
                print('input is not correct size')
                return

            #not implemented
                return
            '''
            for j in range(0, )
                for i in range(0, len(input)):
                    for k in range(self.row[i], self.row[i+1]):
                        result[i] = result[i] + self.data[k] * input[ self.col[k]]
                print(result)
            '''

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
        print(self.row)

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

        #to account for zero rows we may need to add the nnz on the end of row for spicy tests
        if len(new_row) < self.size['col'] + 1:
            new_row.append(self.size['non_zero'])

        print(pre_col)
        print(pre_data)
        print('new_col', new_col)
        print('new_data ', new_data)
        print('new_row', new_row)
        
        transposed = csr_matrix((new_data, new_col, new_row), shape=(self.size['col'], self.size['row'])).toarray()
        transposed_csr = csr_matrix((self.data, self.col, self.row), shape=(self.size['col'], self.size['row'])).transpose().toarray()

        print(transposed)
        print(transposed_csr)

        new_size = self.size
        new_size['col'] = self.size['row']
        new_size['row'] = self.size['col']

        return CSR_Matrix(self.name + ' tranposed', new_row, new_col, new_data, new_size)
        
# returnTranspose
    def returnTranspose(self):
        return 'not implemented'


# CSR

# CSR Transpose with minimal ops

# A(CSR) * B(CSR) = C(CSR)

def zeroMaker(n):
            listOfZeros = [0] * n
            return listOfZeros

def main():
    matrix = readCSR('cage3')
    testCSR(matrix)

    b = zeroMaker(matrix.size['row'])
    b[0] = 1
    tolerance = pow(10, -6)
    maxIter = 5
    maxSearch = 5
    x = []
    r = []
    pVectors = [[]]


if __name__ == "__main__":
    main()