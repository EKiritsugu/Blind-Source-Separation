
#!python3
# 使用方法：mixMatrix(4)
import random
import numpy as np
def mixMatrix(dimention):
    while True:
        A=np.array(np.random.rand(dimention,dimention))
        if np.linalg.matrix_rank(A)==dimention:
            break  
    A=normalizedMatrix(A,dimention)
    return A
    
def normalizedMatrix(Matrix,N):
    for n in range(N):
        squreSum=0.0
        for p in range(N):
            b=Matrix[p,n]
            squreSum+=b*b
        
        for p in range(N):
            Matrix[p,n]=Matrix[p,n]/squreSum   
    return Matrix
