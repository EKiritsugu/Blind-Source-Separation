import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

filename = 'test_date.txt'
T = 5
dt = 0.01
t_list = np.arange(0,T,dt)

Sin = lambda t: np.sin(1.2*t+0.1)
Cos = lambda t: np.cos(5*t)
def la(miu,lam):
    a = []
    for t in t_list:
        a.append(1/(2*lam)*np.exp(-abs(t-miu)/lam))
    return a

def date(fun):
    a = []
    for t in t_list:
        a.append(fun(t))
    return a


def rect_wave(k=1,T=1):
    a = []
    for i in t_list:
        y = k*(abs(i)%T)
        a.append(y)
    return a

line1 = np.array(rect_wave())
line2 = np.array(date(Cos))
mix1 = 5*line1+3*line2
mix2 = 1.2*line1+9*line2
mix3 = 8*line1+4*line2
#plt.plot(t_list,mix1)
#plt.plot(t_list,mix2)
#plt.plot(t_list,mix3)
plt.plot(t_list,line1)
plt.plot(t_list,line2)
#plt.plot(mix1,mix2)
plt.show()
fig = plt.figure()
ax1 = plt.axes(projection='3d')
ax1.scatter3D(mix1,mix2,mix3, cmap='Blues')  #绘制散点图
ax1.plot3D(mix1,mix2,mix3,'gray')    #绘制空间曲线
plt.show()

with open(filename, 'w') as file_object:
    for i in range(int(T/dt)):
        file_object.write(str(mix1[i])+' '+str(mix2[i])+' '+str(mix3[i])+'\n')