import numpy as np

def flatten(a):
    if not isinstance(a, (list, )):
        return [a]
    else:
        b = []
        for item in a:
            b += flatten(item)
    return b

def orthogonal(W):#正交化,此处采用施密特渐进正交化法,假定列有效，因此如果是行的化，注意要输入转置
    
    mid=np.dot(W,W.T)
    u,s,v=np.linalg.svd(mid)
    s=np.sqrt(1/s)
    W=u@(np.diag(s))@v@W
    return W
     
def normalize(W):#假定列向量有效
    for i in range(W.shape[1]):
        w=W[:,i]
        w2=np.power(w,2)
        q=np.sqrt(np.sum(w2))
        for j in range(W.shape[0]):
            W[j,i]=W[j,i]/q
    return W

def matToArray(M):#对于所有的乱七八糟的都可以处理一下，将matrix格式转化为array格式
    try:
        M0=M.A
    except:
        M0=M
    finally:
        return M0
    
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

def tanh(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

