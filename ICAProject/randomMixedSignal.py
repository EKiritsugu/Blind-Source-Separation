#!python3
#使用的时候直接调用mixSignal(时间长度)，默认生成一个四维的格式为array的混合信号，例如mixSignal(1000)
# 对于原信号，一信号为随机信号，二信号为角频率为1/13,2/13,4/13的多个三角函数的叠加，三信号为周期为17的扫描信号，四信号为周期为7的扫描信号
import numpy as np
import math
import matplotlib.pyplot as plt
import random


def signalOne(van):
    a=[]
    for i in range(van):
        a.append(0.0)
    return a

#signal2:生成一个比较复杂的正弦信号的叠加
def signalTwo(van):
    n0=random.uniform(-1,+1)
    n1=random.uniform(-1,+1)
    n2=random.uniform(-1,+1)
    
    b=[]
    for s in range(van):
        p=n0*(math.cos(s/13))+n1*(math.sin(2*s/13))+n2*(math.cos(4*s/13))
        b.append(p)

    return b
    
def signalThree(dimention):
    c=[]
    for s in range(dimention):
        if (s%23)<13:
            p=1
        else:
            p=0
        c.append(p)
    return c

def signalFour(van):
    a=[]
    for i in range(van):
        a.append((i%7)/7)
    return a

def signal(dimention):
    a=signalOne(dimention)
    b=signalTwo(dimention)
    c=signalThree(dimention)
    d=signalFour(dimention)

    

    return [a,b,c,d]
#以上部分为生成一个四个独立的信号

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
#以上部分为生成一个混合矩阵
def mixSignal(time):
    ssgnal=signal(time)
    sig1=np.array(ssgnal[0])
    sig2=np.array(ssgnal[1])
    sig3=np.array(ssgnal[2])
    sig4=np.array(ssgnal[3])

    sig=[sig1,sig2,sig3,sig4]
    sigM=np.array(sig)
    mixM=mixMatrix(4)
    mixedSigM=np.dot(mixM,sigM)
    return mixedSigM
'''    x=range(100)
    y1=mixedSigM[0][x]
    y2=mixedSigM[1][x]
    y3=mixedSigM[2][x]
    y4=mixedSigM[3][x]
    plt.plot(x,y1,color='red')
    plt.plot(x,y2,color='green')
    plt.plot(x,y3,color='blue')
    plt.plot(x,y4,color='skyblue')
    plt.show()'''
    #return mixedSigM
