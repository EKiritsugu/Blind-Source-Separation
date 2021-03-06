import numpy as np
from tqdm import tqdm
from numpy.linalg import inv
from scipy.signal import stft, istft

epsilon = 1e-6#这是一个小量


# suppose that the number of sources and microphones are equal.

# M : # of channels whose index is m
# K : # of frequency bins whose index is k
# T : # of time frames whose index is thaihai

class IVA:

    def __init__(self, x, sample_freq, win='hanning', nperseg=256, noverlap=128):
        '''
        @param(win):str, desired window to use.
        @param(nperseg): length of each segment.
        @param(noverlap): number of points to overlap between segments.
        '''
        self.max_iter = 1000
        self.eta = 2.5 * 10 ** (-2)  # is step size
        self.x = np.array(x)al array whose x
        self.sample_freq = sample_freq
        self.win = win
        self.nperseg = nperseg
        self.noverlap = noverlap

    def iva(self):
        '''
        X is complex64-type-3-dementionaxis is microphie , y axis is the segment times, z is frequency respectively.
        @output(x_prd): 2 dimensional array whose 1st axis is the source index, 2nd is data of them.
        '''

        f, _, X = stft(self.x, self.sample_freq, self.win, self.nperseg, self.noverlap)
        # X is (channel index, freq index, time segment index)短时傅里叶变换

        y = self.reconstruct(X)

        _, x_prd = istft(y, self.sample_freq, self.win, self.nperseg, self.noverlap)
        #逆傅里叶变换
        return x_prd

    def reconstruct(self, X):
        '''
        This func is the way of permutation.
        @param(f): frequency array.
        @param(X): stft of time series x.
        @output(y):y is 3 dementional array
                   whose 1st axis is source index 2nd axis is frequency index and 3rd is time segment index.
        '''

        w = self.__optimize(X)#得到解卷积矩阵
        y = np.empty(X.shape, dtype=np.complex64)#创建一个空数组,Y为最后得到的信号的存储空间
        for k in range(X.shape[1]):
            y[:,k,:] = np.dot(w[k,:,:], X[:,k,:])#用W处理一下

        return y

    def __alpha2(self, y):
        # y is (channel index, freq index, time segment index)
        M, K, T = y.shape
        alpha = np.zeros((K, M, M), dtype=np.complex64)#对每一个频带安排一个单独的混合举证

        ysq = np.sum(np.abs(y) ** 2, axis=1)
        ysq1 = 1 / np.sqrt(ysq)#每一个通道每一个频带的平方和的倒数
        for k in range(K):
            phi = ysq1*y[:,k,:]
            alpha[k,:,:] = np.dot(phi, np.conjugate(y[:,k,:].T))/T
        return alpha

    def __adjust(self, w):#正则化,我也不知道这个是在干嘛，莫名其妙的
        w = np.dot(np.diag(np.diag(inv(w))), w)
        return w

    def __optimize(self, X):
        M, K, T = X.shape
        w = np.zeros((K, M, M), dtype=np.complex64)
        y = np.empty((M, K, T), dtype=np.complex64)
        for k in range(K):
            w[k,:,:] += np.eye(M)#对针对每一个频率的分离矩阵初始化为I

        for _ in tqdm(range(self.max_iter)):#这就是个进度条模块
            for k in range(K):
                y[:,k,:] = np.dot(w[k,:,:], X[:,k,:])
            alpha = self.__alpha2(y)
            for k in range(K):
                w[k,:,:] += self.eta * np.dot((np.eye(M) - alpha[k,:,:]), w[k,:,:])

        for k in range(K):
            w[k,:,:] = self.__adjust(w[k,:,:])

        return w