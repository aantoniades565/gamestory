from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
[Fs, x] = audioBasicIO.readAudioFile("p11-d2-7.wav")
Fs = 48000

F0 = audioFeatureExtraction.stFeatureExtraction(x, Fs, Fs, Fs)
print(len(F0[0]))
with open('energy2.csv','a') as file:
    for m in F0:
        for data in m:
            file.write(str(data))
            file.write('\n')
