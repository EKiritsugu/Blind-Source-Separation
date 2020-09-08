import math
import random

#signal1:random signal:
def signalOne(van):
    a=[]
    for i in range(van):
        a.append(random.uniform(-1,1))
    return a

#signal2:生成一个比较复杂的正弦信号的叠加
def signalTwo(van):
    n0=random.uniform(-1,+1)
    n1=random.uniform(-1,+1)
    n2=random.uniform(-1,+1)
    
    b=[]
    for s in range(van):
        p=n0*(math.cos(s/13))+n1*(math.sin(2*s/13))+n2*(math.cos(4*s/13))
        b.append(p)

    return b
    
def signalThree(dimention):
    c=[]
    for s in range(dimention):
        p=math.sin(s/17)
        c.append(p)
    return c

def signalFour(van):
    a=[]
    for i in range(van):
        a.append((i%7)/7)
    return a

def signal(dimention):
    a=signalOne(dimention)
    b=signalTwo(dimention)
    c=signalThree(dimention)
    d=signalFour(dimention)

    

    return [a,b,c,d]
