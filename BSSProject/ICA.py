import numpy as np
import whitening
import tool
import FastICA
import Signal
import matplotlib.pyplot as plt
import likehoodICA
#导入信号
import Signal
sig,M=Signal.signal(1000)
sig=sig[:2,:]
print(np.linalg.pinv(M).T)
print('############################')
#规范化输入数据
if sig.shape[0]>sig.shape[1]:
    sig=sig.T

#预处理程序
#
sig=whitening.PCAwhitening(sig)


#ICA程序
sig=likehoodICA.likehoodICA_nature(sig,-0.2,-0.2)#m为所需的信号的数量

x=range(100)
y1=sig[0,:100].reshape(100,-1)
y2=sig[1,:100].reshape(100,-1)
#y3=sig[2,:100].reshape(100,-1)
#y4=sig[3,:100].reshape(100,-1)
plt.plot(x,y1+10,color='red')
plt.plot(x,y2-10,color='blue')
#plt.plot(x,y3,color='green')
#plt.plot(x,y4-20,color='black')
plt.show()


