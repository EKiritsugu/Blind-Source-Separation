import numpy as np
import tool
import Signal

A=np.array([[0.1,0.2,0.3,0.4],[2,3,4,5]])
W=tool.normalize(A)
print(W)


sig=Signal.signal(1000)
print(sig[:,2])