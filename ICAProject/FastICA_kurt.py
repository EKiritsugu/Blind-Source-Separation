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
    kurt01=np.mean(kurt01,axis=1)

    kurt02=np.power(zSignal2,2)
    kurt02=np.mean(kurt02,axis=1)
    kurt02=3*kurt02*kurt02
    
    kurt=(kurt01-kurt02)
    return kurt

def change_omega(zSignal,omega):
    zSignal2=np.dot(omega,zSignal)
    
    newOmega=np.power(zSignal2,3)
    newOmega=np.dot(zSignal,newOmega.T)
    newOmega=np.mean(newOmega,axis=0)
    newOmega-=3*omega

    squresum=np.sum((np.power(newOmega,2)))
    sum=np.sqrt(squresum)
    newOmega=newOmega/sum
    return newOmega
def getoneDimetion(steps,zSignal):#steps表示所需的迭代步数
    n,m=zSignal.shape
    omega=np.eye(n,dtype=float)
    omega=omega[0]
    
    n=0
    kurtPlot=[]
    while n<steps:
        print(omega)
        omega=change_omega(zSignal,omega)
        #print(str(n)+'last kurt'+str(Oldkurt)+'omega'+str(omega))
        kurtPlot.append(get_kurt(zSignal))
        n+=1
        
        
    y=kurtPlot[0]
    x=range(steps)
    plt.scatter(x,y)
    plt.show()

    return omega


def Normalize(W):
    u,s,v=np.linalg.svd(W@W.T)
    s=np.diag(np.sqrt(s**-1))
    W=np.dot(np.dot( np.dot(u,s) , v) , W)
    #第三部分，对W进行归一化
    w2=np.sqrt(np.sum(W**2,axis=1))
    W=(np.diag(w2**-1))@W
    return W.T


def fastICA(zSignal,steps,dimentions):
    omega=np.eye(zSignal.shape[0])

    for i in range(steps):
        print('this is'+str(i))
        for d in range(dimentions):
            omega[d]=get_EzwTz3(zSignal,omega[d])-3*omega[d]
        omega=Normalize(omega)
        print(omega)
    return omega
