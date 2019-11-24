import os
'''
#Read in matrix from file adjecncy matrix or stuff provided from https://sparse.tamu.edu/
with open ('/Users/brianallen/Desktop/Projects/Math/ash85.mtx') as fp:
    line = fp.readline()
    row_csr = []
    col_csr = []
    data_csr = []
    row_num = 1
    first_entry = False
    matrix_dict = {}

    #Read in file. Skip non-essentail characters. Save information into a dict.
    while line:
        if line[0] == '%':
            line = fp.readline()
        else:
            if not first_entry:
                first_entry = True
                nums = line.split()
                matrix_dict['size'] = nums
                line = fp.readline()
            else:
                nums = line.split()
                try:
                    matrix_dict[(int(nums[0]), int(nums[1]))] = float(nums[2])
                except:
                    matrix_dict[(int(nums[0]), int(nums[1]))] = 1
                line = fp.readline()

    #From the dict, get csr values, col_csr, row_csr, data_csr
    new_row = True
    for row in range(1, int(matrix_dict['size'][0]) +1):
        new_row = True
        for col in range(1, int(matrix_dict['size'][1]) +1):
            try:
                data_csr.append(float(matrix_dict[row,col]))
                col_csr.append(col)
                if new_row:
                    row_csr.append(row_num)
                    new_row = False
                row_num += 1
            except:
                continue

    print(matrix_dict)
    print("col: ", col_csr, " ", len(col_csr))
    print("data ", data_csr, " ", len(data_csr))
    print("row: ", row_csr)
    
    #Ensure we can get back to the original dictionary
    count = 0
    row = 0
    for i in range(0, len(data_csr)):
        print(row+1, col_csr[i], data_csr[i])
        try:
            out_data = matrix_dict[(row+1,int(col_csr[i]))]
            count += 1
            if out_data != data_csr[i]:
                print("miss matching data")
            try:
                if count +1 == row_csr[row+1]:
                    row +=1
            except:
                continue
        except:
            print("test failed!! i: ", i, " row: ", row)
            continue
 
    print("Number non zero entries recovered: ", count)          
'''   

def testCSR(dict, data_csr, row_csr, col_csr):
    #Ensure we can get back to the original dictionary
    count = 0
    row = 0
    for i in range(0, len(data_csr)):
        print(row+1, col_csr[i], data_csr[i])
        try:
            out_data = matrix_dict[(row+1,int(col_csr[i]))]
            count += 1
            if out_data != data_csr[i]:
                print("miss matching data")
            try:
                if count +1 == row_csr[row+1]:
                    row +=1
            except:
                continue
        except:
            print("test failed!! i: ", i, " row: ", row)
            continue
 
    print("Number non zero entries recovered: ", count)     

def readCSR(file):
    #Read in matrix from file adjecncy matrix or stuff provided from https://sparse.tamu.edu/
    with open ('/Users/brianallen/Desktop/Projects/Math/cage3.mtx') as fp:
        line = fp.readline()
        row_csr = []
        col_csr = []
        data_csr = []
        row_num = 1
        first_entry = False
        matrix_dict = {}

        #Read in file. Skip non-essentail characters. Save information into a dict.
        while line:
            if line[0] == '%':
                line = fp.readline()
            else:
                if not first_entry:
                    first_entry = True
                    nums = line.split()
                    matrix_dict['size'] = nums
                    line = fp.readline()
                else:
                    nums = line.split()
                    try:
                        matrix_dict[(int(nums[0]), int(nums[1]))] = float(nums[2])
                    except:
                        matrix_dict[(int(nums[0]), int(nums[1]))] = 1
                    line = fp.readline()

        #From the dict, get csr values, col_csr, row_csr, data_csr
        new_row = True
        for row in range(1, int(matrix_dict['size'][0]) +1):
            new_row = True
            for col in range(1, int(matrix_dict['size'][1]) +1):
                try:
                    data_csr.append(float(matrix_dict[row,col]))
                    col_csr.append(col)
                    if new_row:
                        row_csr.append(row_num)
                        new_row = False
                    row_num += 1
                except:
                    continue

        print(matrix_dict)
        print("col: ", col_csr, " ", len(col_csr))
        print("data ", data_csr, " ", len(data_csr))
        print("row: ", row_csr)    

        #testCSR(matrix_dict, data_csr, row_csr, col_csr) fix this later

        print('Ensureing we can get back to the original dictionary')
        count = 0
        row = 0
        for i in range(0, len(data_csr)):
            print(row+1, col_csr[i], data_csr[i])
            try:
                out_data = matrix_dict[(row+1,int(col_csr[i]))]
                count += 1
                if out_data != data_csr[i]:
                    print("miss matching data")
                try:
                    if count +1 == row_csr[row+1]:
                        row +=1
                except:
                    continue
            except:
                print("test failed!! i: ", i, " row: ", row)
                continue
    
        print("Number non zero entries recovered: ", count) 
        print("mtx file to CSR successfull!!!!", '\n', '\n')

        return CSR_Matrix(str(file), row_csr, col_csr, data_csr)      
           



# create matrix class
class CSR_Matrix:
    def __init__(self, name, row, col, data):
        self.name = name
        self.row = row
        self.col = col
        self.data = data
    
    def print(self):
        print(self.name)
        print(self.row)
        print(self.col)
        print(self.data)

# create matrix multiplication 
# create toCSR
# transpose
# returnTranspose

        
        



# A * vector, A-transpose * vector

# CSR

# CSR Transpose with minimal ops

# A(CSR) * B(CSR) = C(CSR)

def main():
    matrix = readCSR('cage3')
    matrix.print()
    


if __name__ == "__main__":
    main()