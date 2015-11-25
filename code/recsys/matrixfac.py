# -*- coding: utf-8 -*-
"""
author: Tanveer
"""

import numpy as np
import os
from gen import DataGen
from math import sqrt

EP_RATING = 'rating.mat'
EP_TRUST = 'trustnetwork.mat'

def matrix_factorization(R, P, Q, K, steps=250, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in xrange(steps):
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        if e < 0.001:
            break
    return P, Q.T



def rmse(A,B):
    count=0 
    summ=0
    numrows = len(A)
    numcols = len(A[0])
    for x in xrange(0, numrows):
        for y in xrange(0, numcols):
            if A[x][y] >= 1:
                summ+= (A[x][y] - B[x][y])**2
                count=count+1
    
    return sqrt(summ/count)



def coverage(A,T):
    count=0
    numrows = len(A)
    numcols = len(A[0])
    for x in xrange(0, numrows):
        for y in xrange(0, numcols):
            if A[x][y] >= T:
                count=count+1
    
    return count/float(A.size)


if __name__ == '__main__':
    
    ip_dir = os.getcwd() #current file directory, keep the mat files in the same place
    rating_file = os.path.join(ip_dir, EP_RATING)
    trust_file = os.path.join(ip_dir, EP_TRUST)

    generator = DataGen(rating_file, trust_file)
    generator.generate()
    
    uiu_matrix = np.hstack((generator.ui_matrix, generator.uu_matrix)) #merging two matrices
    
   

    N = len(uiu_matrix)
    M = len(uiu_matrix[0])
    W = len(generator.ui_matrix)
    X = len(generator.ui_matrix[0])
    
    K = 100

    P = np.random.rand(N,K)
    Q = np.random.rand(M,K)

    R=uiu_matrix
    
    nP,nQ = matrix_factorization(R, P, Q, K)
  
    Y= np.dot(nP, nQ.T)
    Z = Y[0:W,0:X]  #trimming off the trust part of the matrix
    
    print "RMSE: %f  Coverage: %f " % (rmse(generator.ui_matrix,Z), coverage(Z,1)) 
    
    
    




