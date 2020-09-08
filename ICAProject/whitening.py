#!这一部分用来白化矩阵用
#要求其信号矩阵为n行m列，即有n个不同的混合后的信号，时间为m
import numpy as np

#epsilon表示一个小量，retainVarPercent表示所需保留的
def whiteningSignal(signalMatrix,epsilon):
    n,m=signalMatrix.shape
#将信号0均值化
    mean=np.mean(signalMatrix,axis=1)
    mean=np.tile(mean,m)
    mean=np.reshape(mean,(m,n)).T
    zeroMeanSignal=signalMatrix-mean
#得到协方差矩阵,u为特征向量， s为排好序由大到小的特征值
    covMatrix=np.dot(zeroMeanSignal,zeroMeanSignal.T)/m#此处存疑，py内置的协方差矩阵为除以m-1，此处除以m，不确定哪种好，
    u, s, v = np.linalg.svd(covMatrix)

    if True:    #retainVarPercent==1.0:
        pcaSignal=np.dot(u.T,signalMatrix)
        s=s
        whitenedSignal=np.dot(np.diag(1.0 / np.sqrt(s + epsilon)),pcaSignal)
    #归一化
        s2=np.sqrt(np.sum(whitenedSignal**2/m,axis=1))
        whitenedSignal=(np.diag(s2**-1))@whitenedSignal
        return whitenedSignal
        #,(np.diag(s2**-1))@np.dot(np.diag(1.0 / np.sqrt(s + epsilon)),u.T)
    '''else:#如果要启用的话，主函数里添加一个参量，把上面的if函数后面的改一下
         k = 0 #选取的特征的数目
        for i in range(n):
            if (np.sum(s[0:(i+1)]) / np.sum(s)) >= retainVarPercent:
                k = (i + 1)
                break
        print ('Optimal k to retain '+str(retainVarPercent) +' variance is:', k)
        simplifedSignal = np.dot((u[:, 0: k].T),signalMatrix)
        simplifedOriginalSignal = u[:, 0: k].dot(signalMatrix) #将降维后的数据还原，会有一部分损失
        return simplifedOriginalSignal #返回还原后的数据
        '''









