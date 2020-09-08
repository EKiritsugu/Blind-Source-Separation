from gccNMF.gccNMFFunctions import *
from gccNMF.gccNMFPlotting import *

from IPython import display


#参数设定
windowSize = 1024
fftSize = windowSize
hopSize = 128
windowFunction = hanning

# TDOA params
numTDOAs = 128

# NMF params
dictionarySize = 128
numIterations = 100
sparsityAlpha = 0

# Input params    引用地址以后可以改变
mixtureFileNamePrefix = '../data/dev1_female3_liverec_130ms_1m'
microphoneSeparationInMetres = 1.0
numSources = 3