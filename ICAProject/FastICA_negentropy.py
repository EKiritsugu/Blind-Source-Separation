import math
import numpy as np
import whitening
import randomMixedSignal
import matplotlib.pyplot as plt

def get_negentropy(omega,zSignal):#返回一个n列的单行向量
    zSignal2=np.dot(omega,zSignal)
    part1=(np.mean(np.power(zSignal2,3)))**2/12
    
    kurt01=np.power(zSignal2,4)
    kurt01=np.mean(kurt01)

    kurt02=np.power(zSignal2,2)
    kurt02=np.mean(kurt02)
    kurt02=3*kurt02*kurt02
    
    part2=(kurt01-kurt02)**2/48
    return part1+part2
def g(y):
    return y*np.exp(-y**2/2)
def dg(y):
    return (1-y**2)*np.exp(-y**2/2)
def change_omega(zSignal,omega):
    zSignal2=np.dot(omega,zSignal)
    
    part1=(1/len(zSignal2.T))*(zSignal2@g(zSignal.T))

    part2=np.mean(dg(zSignal2))*omega

    omega=part1-part2

    squresum=np.sum((np.power(omega,2)))
    sum=np.sqrt(squresum)
    omega=omega/sum
    return omega



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
        kurtPlot.append(get_negentropy(omega,zSignal))
        n+=1
        
        
    y=kurtPlot
    x=range(steps)
    plt.scatter(x,y)
    plt.show()

    return omega

