import numpy as np
import tobeImported
import scipy
import matplotlib
import wave
from scipy.signal import stft, istft
#import IVA
'''
#导入信号
Sig=np.empty((4,100000))
for i in range(4):
    f=wave.open('mixedSig'+str(i)+'.wav','rb')
    str_data=f.readframes(100000)
    f.close
    wave_data=np.fromstring(str_data,dtype=np.short)
    wave_data.shape=-1,2
    wave_data=wave_data.T
    Sig[i,:]=wave_data

Sig=IVA.bss_iva(Sig)

for i in range(4):
    # 配置声道数、量化位数和取样频率
    wave_data=Sig[i]
    wave_data=wave_data.astype(np.short)

    f = wave.open('Sig'+str(i)+'.wav', "wb")
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)
    # 将wav_data转换为二进制数据写入文件
    f.writeframes(wave_data.tostring())
    f.close()


'''
f=wave.open('mixedSig0'+'.wav','rb')
str_data=f.readframes(100000)
f.close
wave_data=np.fromstring(str_data,dtype=np.short)
wave_data.shape=-1,1
wave_data=wave_data.T
Sig=wave_data
print(np.shape(Sig))
f, t, X = scipy.signal.stft(Sig, fs=1.0, window='hann', nperseg=256,return_onesided=True)
print(np.shape(f))
print(np.shape(t))
print(np.shape(X))
print(X)
