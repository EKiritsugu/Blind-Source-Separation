import numpy as np
import tobeImported
import scipy
import matplotlib
import wave

'''
IVA相关地笔记：
IVA信号分离由多个步骤构成
1.对多个输入信号进行短时傅里叶变换，需要参数：信号，时域采样率，窗函数，窗函数的长度，窗函数重叠数，fft长度（？），return_outside（返回复数或者实部）
  我看的案例中采用的返回实部的处理方法
2.对短时傅里叶变换后的结果进行白化处理，
3.对于每个信号的频率段进行方差归一化（那这以后怎么还原？）
4.
'''

def whiten(x):
  K,N,T = x.shape
  z = np.zeros((K,N,T))
  V = np.zeros((K,N,N))
  U = np.zeros((K,N,N))
  for k in range(0, K):
      xk = x[k,:,:] - np.mean(x[k,:,:],axis=1).reshape(np.mean(x[k,:,:],1).size, axis=1)
      covar= np.matmul(xk, np.matrix(xk).getH())/T
      [eigval, eigvec] = np.linalg.eig(covar)
      V[k,:,:] = np.linalg.lstsq(np.sqrt(np.diag(eigval)), eigvec)[0]
      U[k,:,:] = np.matmul(eigvec, np.sqrt(eigval))
      z[k,:,:] = np.matmul(V[k,:,:], xk)

  return [z, V, U]

def __adjust(W):#不知道在干嘛
  W = np.dot(np.diag(np.diag(inv(W))), W)
  return W

def countKL(y):
  return 0 

def deltaW(y,W):
  [K,N,T]=y.shape
  alpha = np.zeros((N, K, K))#对每一个频带安排一个单独的混合矩阵

  ysq = np.sum(np.abs(y) ** 2, axis=1)
  ysq1 = 1 / np.sqrt(ysq)

  for n in range(N):
    phi = ysq1*y[:,n,:]
    deltaW[n,:,:] = np.dot(phi, np.conjugate(y[:,n,:].T))/T
  return deltaW

def UpdateW(X,W):
  step=0.01

  [K,N,T]=X.shape
  y = np.empty((K, N, T))
  for n in range(N):
    y[:,n,:] = np.dot(W[n,:,:], X[:,n,:])
  delta = deltaW(y)
  for k in range(K):
    W[k,:,:] += step * np.dot((np.eye(K) - delta[k,:,:]), W[k,:,:])

  KL=countKL(y)
  return [W,KL]

def bss_iva(Sig,ifwhiten=False):#self为时域的音频信号，格式为行数组，array格式
  #初始化迭代次数（后续可以采用步长逐渐收敛的方式来，但是这儿默认通过多次计算
  countTimes=1000
  KLlist=np.empty((1,countTimes))
  
  #将self转化为array格式方便进一步操作
  Sig=tobeImported.matToArray(Sig)

  #对信号进行短时傅里叶变换
  f, _, X = scipy.signal.stft(Sig, fs=1.0, window='hann', nperseg=256)
  #这一块消化得还是不行
  [K,N,T]=X.shape
  
  #对信号进行白化处理(如有必要)
  if ifwhiten:
    [X,V,U]=whiten(X)
  #随机初始化W
  W = np.random.randn(K, N, N)

  #这一段为主要的IVA程序
  #更新W函数
  for turn in range(countTimes):
    [W,KL[turn]]=UpdateW(X,W)
    W=__adjust(W)

  #主要IVA程序结束，得到W

  for k in range(X.shape[1]):
    y[:,k,:] = np.dot(W[k,:,:], X[:,k,:])#用W处理一下


  _, Sig= istft(y)
        #逆傅里叶变换
  return Sig


  

  


  

  
