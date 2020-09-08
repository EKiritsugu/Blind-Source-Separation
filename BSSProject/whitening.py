import numpy as np
import Signal
import matplotlib.pyplot as plt
import tool
def pca(X):
    # normalize the features
    C=np.mean(X,axis=1)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            X[i,j]=X[i,j]-C[i]
        
   
    # compute the covariance matrix
    X = np.matrix(X)
    cov = X*X.T/X.shape[1]
    # perform SVD
    U, S, V = np.linalg.svd(cov)
    return U, S, V

def PCAwhitening(sig,epsilon=0.000001):#epsilon为舍弃的方差
    
    u,s,_=pca(sig)
    a=0
    for k in range(sig.shape[0]):
        a+=s[k]
        if a/np.sum(s)>(1-epsilon):
            break
        
    U_reduced = u[:,:k+1]
    U_reduced=U_reduced.A
    
    sig=U_reduced.T@sig
    print(sig[:,0])
    D=np.sqrt(s)
    for i in range(k):
        sig[i,:]=sig[i,:]/D[i]

    for i in range(sig.shape[0]):
        std=np.std(sig[i,:])
        sig[i,:]=sig[i,:]/std

    return sig

def ZCAwhitening(sig,epsilon=0.000001):#比PCA多了一步还原数据
    
    u,s,_=pca(sig)
    a=0
    for k in range(sig.shape[0]):
        a+=s[k]
        if a/np.sum(s)>(1-epsilon):
            break
        
    U_reduced = u[:,:k]
    X=np.dot(U_reduced.T,sig)

    D=np.sqrt(s)
    for i in range(k):
        X[i,:]=X[i,:]/D[i]

    U_reduced = np.linalg.pinv(u[:,:k])
    sig=np.dot(U_reduced.T,X)

    for i in range(sig.shape[0]):
        std=np.std(sig[i,:])
        sig[i,:]=sig[i,:]/std

    return sig
'''
sig=ZCAwhitening(Signal.signal(1000),0.01)

plt.figure(figsize=(2,2))
plt.scatter(fuck.flatten(sig[0,:]),fuck.flatten(sig[1,:]))
plt.show()
'''