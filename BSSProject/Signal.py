import math
import random
import numpy as np
#signal1:random signal:
def mixMatrix(dimention):
    while True:
        A=np.array(np.random.rand(dimention,dimention))
        if np.linalg.matrix_rank(A)==dimention:
            break  
    A=normalizedMatrix(A,dimention)
    return A
    
def normalizedMatrix(Matrix,N):
    if np.linalg.matrix_rank(Matrix) !=4:
        print('FUCK!')
    return Matrix

''' 
    for n in range(N):
        squreSum=0.0
        for p in range(N):
            b=Matrix[p,n]
            squreSum+=b*b
        
        for p in range(N):
            Matrix[p,n]=Matrix[p,n]/squreSum   
'''
    

def signal(dimention):
    signal=np.random.rand(4,dimention)
    n0=random.uniform(-1,+1)
    n1=random.uniform(-1,+1)
    n2=random.uniform(-1,+1)





    for i in range(dimention):
        signal[0,i]=np.exp(i%13)/10000-1
        signal[1,i]=n0*(math.cos(i/13))+n1*(math.sin(2*i/13))+n2*(math.cos(4*i/13))
        signal[2,i]=math.sin(i/5)
        signal[3,i]=(i%7)/7
    mixM=mixMatrix(4).T
    
    signal=mixM@signal
    return signal,mixM

