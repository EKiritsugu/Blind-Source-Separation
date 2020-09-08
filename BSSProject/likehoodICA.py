import numpy as np
import tool
import matplotlib.pyplot as plt
#本书中提到的最大似然度的估计算法似乎比较适用于适定情况，虽然可能仅对少数的信号有作用，但是必须对与输入信号数量相同的信号进行估计
#我也不知道为啥这个算法的FastICA就是跑不起来
#我检查了半天和书上基本都是一致的，实在想不通哪儿有问题，而且此处的梯度算法虽然看起来好像能用，但是和书上的其实也是不一样的，学习率和书上的正负正好相反

def gP(y):
    return -2*tool.tanh(y)
def gN(y):
    return tool.tanh(y)-y

def g(y):
    return tool.tanh(y)
def dg(y):
    return 1-np.power(tool.tanh(y),2)

def renewGamma(y,gamma,mugamma):
    gamma=tool.matToArray(gamma)
    k=float(1-mugamma)
    part1=gamma*k
    
    part2=np.mean(np.multiply(-tool.tanh(y),y)+1-np.power(tool.tanh(y),2),axis=1)
    #part2=np.mean(np.multiply(-tool.tanh(y),y)+1-tool.tanh(np.power(y,2)),axis=1)
    part2=part2*mugamma
    part2=part2.reshape(y.shape[0],1)
    
    gamma=part1+part2
    return gamma

def renewB(B,signg,y,mu):
    part=np.eye(y.shape[0])

    #for i in range(y.shape[1]):
    signg=signg.ravel()
    signg.astype(int)
    GY=np.zeros((y.shape[0],y.shape[1]))
    for j in range(y.shape[0]):
        if signg[j]==1:
            GY[j,:]=gP(y[j,:])
            
        else:
            GY[j,:]=gN(y[j,:])
        
    part+=GY@y.T
        
        
        #part+=(signg*gP(y[:,i])+(1-signg)*gN(y[:,i]))@y[:,i].T

    #part=part/y.shape[1]
    
    B=B+mu*part@B
    return B

def likehoodICA_nature(sig,mu,mugamma):#此处sig必须经过白化处理，不然结果会很难看，sig默认是横过来的，在非ICA程序中调用务必注意
    #随机初始化gamma
    gamma=np.random.rand(sig.shape[0],1)
    gamma-=np.mean(gamma)
    
    #随机初始化B
    B=np.random.rand(sig.shape[0],sig.shape[0])

    #PPPPP=np.zeros((2,500))

    for h in range(500):
        y=B@sig
        
        #for i in range(y.shape[0]):
        #    y[i,:]=y[i,:]/np.var(y[i,:])
            
        
        gamma=renewGamma(y,gamma,mugamma)
        signg=(np.sign(gamma)+1)/2
        
        
        
        #如果gamma为正，那么设为1采用gp，如果为负设为0，采用gn，那么设为0，因此公式为(gamma*gp+(1-gamma)gn)

        B=renewB(B,signg,y,mu)

        B=tool.orthogonal(B)
        B=tool.normalize(B.T)
        B=B.T

        #PPPPP[:,h]=B[1,:]
        
    sig=B@sig


    #plt.scatter(PPPPP[0,:],PPPPP[1,:])
    #plt.show()

    return sig

def FastRenewB(B,alpha,beta,y,C):
    E=np.zeros((y.shape[0],y.shape[0]))
    for i in range(y.shape[1]):
        E+=g(y[:,i])@y[:,i].T
    E=E/y.shape[1]

    E+=np.diag(beta)
    B=B+np.diag(alpha)@E@B

    #接下来一大块都是给B正交归一化(BCB)^-1/2 B

    core=B@C@B.T
    u,s,v=np.linalg.svd(core)
    s=np.sqrt(1/s)
    B=u@(np.diag(s))@v.T@B

    return B

def likehoodFastICA(sig):
    B=np.random.rand(sig.shape[0],sig.shape[0])
    C=np.dot(sig,sig.T)/sig.shape[1]
    #beta=np.zeros(sig.shape[0]).T
    #alpha=np.zeros(sig.shape[0]).T
    PPPPP=np.zeros((2,500))
    for h in range(500):
        y=B@sig

        for i in range(y.shape[0]):
            y[i,:]=y[i,:]/np.var(y[i,:])

        beta=-np.mean(np.multiply(y,g(y)),axis=1)
        alpha=-1/(beta+np.mean(dg(y),axis=1))

        beta=beta.ravel()
        alpha=alpha.ravel()

        B=FastRenewB(B,alpha,beta,y,C)

        PPPPP[:,h]=B[1,:]
    
    plt.scatter(PPPPP[0,:],PPPPP[1,:])
    plt.show()

    x=range(500)
    y1=PPPPP[0,:500]
    y2=PPPPP[1,:500]
    plt.plot(x,y1)
    plt.plot(x,y2)
    plt.show()
    sig=B@sig

    return sig