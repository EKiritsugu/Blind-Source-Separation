#!python3
#这部分为利用峭度进行ICA处理，主要分为两个部分，分别为梯度算法和快速不动点算法（FastICA）,还有，信号最好是array格式的。因为我测试的时候用的是array

#zSignal统一为白化后信号

import numpy as np
import random
import math
import whitening
import randomMixedSignal
import matplotlib.pyplot as plt
def get_EzwTz3(zSignal,omega):#此处Omega为一维
    wTz3=(omega@zSignal)**3
    b=0
    for i in range(zSignal.shape[1]):
        b+=zSignal[:,i]*wTz3[i]
    E=b/zSignal.shape[1]
    return E
def get_kurt(zSignal2):#返回一个n列的单行向量
    
    kurt01=np.power(zSignal2,4)
    kurt01=np.mean(kurt01)#,axis=1

    kurt02=np.power(zSignal2,2)
    kurt02=np.mean(kurt02)#,axis=1
    kurt02=3*kurt02*kurt02
    
    kurt=(kurt01-kurt02)
    return kurt

def gradient_kurt(zSignal,alpha,omega):#alpha指学习率，也即每次迭代的长度
    
    zSignal2=np.dot(omega,zSignal)
    kurt=get_kurt(zSignal2)
    
    gradient01=np.sign(kurt)
    gradient=omega
    for p in range(omega.shape[0]):
        dw=0
        wz=zSignal2[p]**3
        
        for i in range(zSignal.shape[1]):
            dw+=zSignal[:,i]*wz[i]
        dw/=zSignal.shape[1]
        dw-=3*omega[p]
        dw=dw*gradient01[p]
        gradient[p]=(alpha*dw)
    
    '''
    gradient02=np.power(zSignal2,3)
    gradient02=np.dot(gradient02,zSignal.T)
    gradient=np.dot(np.diag(gradient01),gradient02)
    gradient=alpha*gradient
    '''
    return gradient,kurt

def getoneDimetion(steps,alpha,zSignal):#steps表示所需的迭代步数
    n,m=zSignal.shape
    omega=np.eye(n,dtype=float)
    omega=omega[0]
    
    n=0
    kurtPlot=[]
    while n<steps:
        deltaOmega,Oldkurt=gradient_kurt(zSignal,alpha,omega)
        omega+=deltaOmega
        #归一化
        sum=np.sqrt(np.sum((np.power(omega,2))))
        omega=omega/sum
        #print(str(n)+'last kurt'+str(Oldkurt)+'omega'+str(omega))
        kurtPlot.append(Oldkurt)
        n+=1

    '''y=kurtPlot[0]
    x=range(steps)
    plt.scatter(x,y)
    plt.show()'''

    return omega

def getOneW1(alpha,zSignal,dimention,W):
    #第一部分，对每一个维度都进行变换
    
    deltaOmega,Oldkurt=gradient_kurt(zSignal,alpha,W)
    W+=deltaOmega
    #第二部分，对W进行正交化
    u,s,v=np.linalg.svd(W@W.T)
    s=np.diag(np.sqrt(s**-1))
    W=np.dot(np.dot( np.dot(u,s) , v) , W)
    #第三部分，对W进行归一化
    w2=np.sqrt(np.sum(W**2,axis=1))
    W=(np.diag(w2**-1))@W
    return W

def getMoreDimetions(steps,alpha,zSignal,dimention):
    n,m=zSignal.shape
    if n<dimention:
        print('ERROE,dimention is too large.')
        return 0
    W=np.eye(n,dtype=float)
    for p in range(steps):
        print('this is'+str(p))
        print(W)    
        W=getOneW1(alpha,zSignal,dimention,W)
    return W
    
    

def ica(zSignal,alpha,steps,dimentions):
    w=np.eye(zSignal.shape[0])
    for d in range(dimentions):
        for s in range(steps):
            print(str(d)+'###'+str(s))
            dw=np.zeros((1,zSignal.shape[0]))
            for p in range(zSignal.shape[1]):
                dw+=zSignal[:,p]*(w[d]@zSignal[:,p])**3
            dw=dw/zSignal.shape[1]
            dw-=3*w[d]
            sign=np.sign(get_kurt(w[d]@zSignal))
            
            w[d]=w[d]+alpha*sign*dw
            
            for di in range(d):
                w[d]-=(w[d]@w[di].T)*w[di]
            w[d]=w[d]/np.linalg.norm(w[d])
    return w


