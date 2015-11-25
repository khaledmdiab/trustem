# -*- coding: utf-8 -*-
"""
author: Tanveer
"""

import numpy as np
import os
from gen import DataGen, EP_RATING, EP_TRUST


def matrix_factorization(R, P, Q, K, steps=250, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in xrange(steps):
        # make sure we're running something
        if steps % 10 == 0:
            print 'MF: step %d out of %d' % (step, steps)
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


def run_rec(gen, k=100, steps=250, alpha=0.0002, beta=0.02):
    # merging two matrices
    uiu_matrix = np.hstack((gen.ui_matrix, gen.uu_matrix))

    N = len(uiu_matrix)
    M = len(uiu_matrix[0])
    W = len(gen.ui_matrix)
    X = len(gen.ui_matrix[0])
    P = np.random.rand(N, k)
    Q = np.random.rand(M, k)

    R = uiu_matrix
    nP, nQ = matrix_factorization(R, P, Q, k, steps=steps, alpha=alpha, beta=beta)
    mf_results = np.dot(nP, nQ.T)
    # trimming off the trust part of the matrix
    mf_user_item_matrix = mf_results[0:W, 0:X]
    return mf_user_item_matrix


if __name__ == '__main__':
    import recstats
    # current file directory, keep the mat files in the same place
    ip_dir = os.getcwd()
    rating_file = os.path.join(ip_dir, EP_RATING)
    trust_file = os.path.join(ip_dir, EP_TRUST)

    generator = DataGen(rating_file, trust_file)
    ui_matrix = run_rec(generator, 100)
    
    print "RMSE: %f  Coverage: %f " % (recstats.rmse(generator.ui_matrix, ui_matrix), recstats.coverage(ui_matrix, 1))
    
    
    




