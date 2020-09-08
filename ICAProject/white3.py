import matplotlib.pyplot as plt
import numpy as np

#用来降维，去掉冗余信号
def down(x,k):#k表示剩下的信号个数
    x -= np.mean(x, axis=0)
    cov = np.dot(x.T, x) / x.shape[0]
    U, S, V = np.linalg.svd(cov)
    xReduce = np.dot(x,U[:,0:k])
    return xReduce

def white(x):#白化
    cov = np.dot(x.T, x) / x.shape[0]
    U, S, V = np.linalg.svd(cov)
    e = 1e-6
    v = np.dot(np.dot(U,(np.diag(1. / np.sqrt(S+e)))),V)
    xPCAwhite = np.dot(x,v.T)
    return xPCAwhite

if __name__ == '__main__':
    file_add = 'C:\\Users\\one for all\\Desktop\\python练习\\white\\test_date.txt'
    dt =0.5
    x = np.loadtxt(file_add)
    x = down(x,2)
    x = white(x)
    t = np.arange(0,dt*x.shape[0],dt)
    plt.scatter(t,x[:,1])
    plt.scatter(t,x[:,0])
    plt.show()


