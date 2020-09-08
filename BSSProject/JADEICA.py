import numpy as np


def cum(x1,x2,x3,x4):#此处的x1x2x3x4都是一维向量的格式,使用的时候如果遇到报错注意采用reshape,同时,如果输入不是一维向量,这个def也不会检查
    result=np.mean(x1*x2*x3*x4)
    result=result-np.mean(x1*x2)*np.mean(x3*x4)-np.mean(x1*x3)*np.mean(x2*x4)-np.mean(x1*x4)*np.mean(x2*x3)
    return result

def FFF_ij(M,sig):#一般默认M为方阵
    F=np.zeros(sig.shape[0],sig.shape[1])

    for i in range(sig.shape[0]):
        for j in range(sig.shape[1]):
            #以下F_ij的计算
            for k in range(sig.shape[0]):
                for l in range(sig.shape[1]):
                    temp+=M[k,l]*cum(sig[i,:],sig[j,:],sig[k,:],sig[l,:])
            F[i,j]=temp
            temp=0
    
    return F

def J_JADE(sig):
    M=np.eyes(sig.shape[0])
    

