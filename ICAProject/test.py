#使用规范：如果要对信号作测试，注意所有测试后的都要删除
import numpy as np 
import randomMixedSignal
import whitening
import matplotlib.pyplot as plt
import ICA_kurt
import FastICA_negentropy
import FastICA_kurt
import white3

#此处可以放置各个需要被调用的函数
def plotFourDimentions(mixedSigM):
    x=range(100)
    y1=mixedSigM[0][x]-15
    y2=mixedSigM[1][x]-5
    y3=mixedSigM[2][x]+5
    y4=mixedSigM[3][x]+15
    plt.plot(x,y1,color='red')
    plt.plot(x,y2,color='green')
    plt.plot(x,y3,color='blue')
    plt.plot(x,y4,color='skyblue')
    plt.show()


##############################
#此处用于放置用于不成熟的调试的测试函数
#对信号再次去均值以及归一
def normalizeSignal(signalMatrix):
    n,m=signalMatrix.shape
    mean=np.mean(signalMatrix,axis=1)
    mean=np.tile(mean,m)
    mean=np.reshape(mean,(m,n)).T
    zeroMeanSignal=signalMatrix-mean
    return zeroMeanSignal
def kurt(z,w):
    s = 0
    for i in range(z.shape[0]):
        s+=(np.dot(z[i:i+1,:],w))**4
    s/=z.shape[0]
#    w0.append(int(s-3))
    s = np.sign(s-3)
    return s

def ica_kurt(z,n,times,k=1,online = 'off'):#k是学习速率,n是独立成分个数,times是迭代次数
    if online =='off':
        w = np.random.random((z.shape[1],n))
        for ni in range(n):
            for stimes in range(times):#开始迭代，计算wi
                dw = np.zeros((w.shape[0],1))
                for i in range(z.shape[0]):#计算dw_i
                    dw += z[i:i+1,:].T*(np.dot(z[i:i+1,:],w[:,ni:ni+1]))**3
                s = kurt(z,w[:,ni:ni+1])
                dw /= z.shape[0]
                dw -= 3*w[:,ni:ni+1]
                w[:,ni:ni+1]+=k*s*dw
                for t in range(ni):#渐进正交化
                    w[:,ni:ni+1]-=np.dot(w[:,ni:ni+1].T,w[:,t:t+1])*w[:,t:t+1]
                w[:, ni:ni + 1] /= np.linalg.norm(w[:, ni:ni + 1])
        return w
########################


###下面是主要的测试部分

#待处理信号来源
data=np.asarray(randomMixedSignal.mixSignal(100))#后面填写信号源
plotFourDimentions(data)
#预处理过程
a = white3.down(data.T,4)
a = (white3.white(a)).T

#a=whitening.whiteningSignal(data,0.00000000001)


#对于单一维度的代码测试
#w1=ICA_kurt.getoneDimetion(25,0.01,a)
#w2=FastICA_negentropy.getoneDimetion(25,a)

#对于多维的代码测试
print('########################')
W=ICA_kurt.ica(a,0.1,200,4)
#W=ICA_kurt.getMoreDimetions(100,0.02,a,4)
print(W@W.T)


#展示效果
signal=np.dot(W,a)
plotFourDimentions(signal)