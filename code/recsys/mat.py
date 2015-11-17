import scipy.io as io

__author__ = 'Khaled Diab (kdiab@sfu.ca)'


def read(mat_file):
    return io.loadmat(mat_file)

