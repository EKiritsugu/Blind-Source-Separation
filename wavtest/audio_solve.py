import numpy as np
import pyaudio
import wave
from tqdm import tqdm
import matplotlib.pyplot as plt
import sys

def date_get(file_path,time):#time是要剪辑的时间
    with wave.open(file_path) as f:
        # 读取格式信息
        params = f.getparams()
        nchannels,sampwidth,framerate,nframes = params[:4]
        # 读取波形数据
        str_data = f.readframes(time*framerate)
    data = np.frombuffer(str_data,dtype = np.short)
    return data,nchannels,sampwidth,framerate,nframes

def save_wav(file_name,nchannels,sampwidth,framerate,data):
    # 打开WAV文档
    f = wave.open(file_name, "wb")
    # 配置声道数、量化位数和取样频率
    f.setnchannels(nchannels)
    f.setsampwidth(sampwidth)
    f.setframerate(framerate)
    # 将wav_data转换为二进制数据写入文件
    f.writeframes(data.tostring())
    f.close()

def audio_solve(f_path1,f_path2,time):

    wave_data1,nchannels1,sampwidth1,framerate1,nframes1 = date_get(f_path1,time)
    wave_data2,nchannels2,sampwidth2,framerate2,nframes2 = date_get(f_path2,time)

    if sampwidth1!=sampwidth2 or framerate1!=framerate2 or nchannels1!=nchannels2:
        print("error,your audio can't be mixed")
        sys.exit()
    #线性混合

    data1 = 0.1*wave_data1+0.5*wave_data2
    data2 = 0.3*wave_data1+0.4*wave_data2
    # 将两个音频分别放在左右声道，实验人耳能不能分离
    data3 = np.zeros(data1.shape[0]*2)
    a = 0
    for i in range(data1.shape[0]):
        data3[a] = data1[i]
        data3[a+1] = data2[i]
        a+=2

    #查看波形
    #t = np.arange(0, time*framerate1*nchannels1)/framerate1
    #plt.plot(t,wave_data)
    #plt.show()

    #打开txt文件
    data1 = data1.astype(np.short)
    data2 = data2.astype(np.short)
    data3 = data3.astype(np.short)

    #存储数据
    f = open(r'C://Users//one for all//Desktop//盲源分离文件//test.txt', "w")
    for i in range( time*framerate1*nchannels1):
        f.write(str(data1[i])+' '+str(data2[i])+'\n')
    f.close()

    #存储音频
    save_wav('C://Users//one for all//Desktop//盲源分离文件//try1.wav',2,2,framerate1,data1)
    save_wav('C://Users//one for all//Desktop//盲源分离文件//try2.wav',2,2,framerate1,data2)
    save_wav('C://Users//one for all//Desktop//盲源分离文件//try3.wav',2,2,2*framerate1,data3)#这个只是用来实验的，不是用来分离的
    return nchannels1,nframes1,framerate1

if __name__ == '__main__':
    file_path1 = 'C://Users//one for all//Desktop//盲源分离文件//千本桜.wav'
    file_path2 = 'C://Users//one for all//Desktop//盲源分离文件//唯一人.wav'
    time = 2
    audio_solve(file_path1,file_path2,time)
