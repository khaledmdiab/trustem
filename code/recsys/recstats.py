from math import sqrt

__author__ = 'Khaled Diab (kdiab@sfu.ca)'


def rmse(mat1, mat2):
    count = 0
    summ = 0
    num_rows = len(mat1)
    num_cols = len(mat1[0])
    for x in xrange(0, num_rows):
        for y in xrange(0, num_cols):
            if mat1[x][y] >= 1:
                summ += (mat1[x][y] - mat2[x][y])**2
                count += 1
    return sqrt(summ/count)


def coverage(mat1, threshold=1):
    count = 0
    num_rows = len(mat1)
    num_cols = len(mat1[0])
    for x in xrange(0, num_rows):
        for y in xrange(0, num_cols):
            if mat1[x][y] >= threshold:
                count += 1
    return count/float(mat1.size)
