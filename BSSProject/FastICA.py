import numpy as np
import tool
def orthogonalGE(W,i):
    if i==0:
        return W
    
    else:
        w=W[:,i]
        for p in range(i):
            w-=(w.T@W[:,p])*W[:,p]
        w=w/(np.sqrt(np.sum(np.power(w,2))))
        W[:,i]=w
        return W

def g1(x,a=1.5):
    return (np.exp(x*a) - np.exp(-x*a)) / (np.exp(x*a) + np.exp(-x*a))
def g2(x):
    return np.exp(-x**2/2)*x
def g3(x):
    return x**3
def dg1(x,a=1.5):
    return a*(1-(g1(x))**2)
def dg2(x):
    return (1-x**2)*np.exp(-x**2/2)
def dg3(x):
    return 3*x**2

#更新w
def renew(sig,w):
    sig=tool.matToArray(sig)
    
    part1=np.zeros(sig.shape[0]).T
    
    for p in range(sig.shape[1]):
        m=np.dot(w.T,sig[:,p])
        k=g2(m)
        part1=part1+sig[:,p]*k

    part1=part1/sig.shape[1]
    

    part2=0
    for p in range(sig.shape[1]):
        part2+=dg2(w.T@(sig[:,p]))
    part2=part2/sig.shape[1]
    part2=part2*w

    w=part1-part2
    w2=(np.sqrt(np.sum(np.power(w,2))))
    
    return w/w2


#主迭代函数
def iteration(sig,W):
    
    for i in range(W.shape[1]):
        
        w=W[:,i]
        ww=renew(sig,w)
        W[:,i]=ww

    W=tool.orthogonal(W)
    W=tool.normalize(W)
        
    return W


def Judge(i,W0,W):#判定收敛条件，此处比较简略
    if i<1000:
        p= True
    else:
        p= False

    m=np.mean(np.power((W0-W),2))
    if m>0.0001:
        q=True
    else:
        q= False

    return p and q

def FastICAPO(sig,m):
    print('start')
    if m>sig.shape[0]:
        return 'ERROR,m should be less than sig.shape[0]'
    #随机初始化W
    W=np.random.rand(sig.shape[0],m)
    W=tool.normalize(W)
    
    W=tool.orthogonal(W)
    
    
    W0=np.ones((sig.shape[0],m))
    i=0
    while Judge(i,W0,W):
        W0=W
        W=iteration(sig,W)
        i+=1

    print("总共迭代次数:"+str(i))
    print(W)
        
    return W.T@sig
    
def FastICAGE(sig,m):
    print('start')
    if m>sig.shape[0]:
        return 'ERROR,m should be less than sig.shape[0]'
    #随机初始化W
    W=np.random.rand(sig.shape[0],m)
    W=tool.normalize(W)
    W=tool.orthogonal(W)
    
    
    for p in range(m):
        print('working')
        for _ in range(100):
            w=W[:,p]
            w=renew(sig,w)
            W[:,p]=w
            W=orthogonalGE(W,p)
            
        print(str(p)+'/4finished')
    print('This is W')
    print(W)
        
    return W.T@sig