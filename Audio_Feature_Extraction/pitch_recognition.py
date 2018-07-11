import os
from pydub import AudioSegment
import speech_recognition as sr


sound = AudioSegment.from_file("./test2.m4a", format="mp4")

tenSecSlice = 10 * 1000

audioLength = len(sound)

q, r = divmod(audioLength, tenSecSlice)

totalSegments= q + int(bool(r))

def processAudio(WAV_FILE):
    r = sr.Recognizer()
    with sr.WavFile(WAV_FILE) as source:
        audio = r.record(source) # read the entire WAV file
    try:
        print(r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

segmentList = []
n=0
while n < totalSegments:
    firstPart = (tenSecSlice * n)
    secondPart =  (tenSecSlice * (n + 1))

    print ("Making slice  from %d to %d  (sec)" % (firstPart /1000 , secondPart /1000))
    print ("Recognizing words from  %d to %d " % (firstPart /1000 , secondPart /1000))
    tempObject = sound[ firstPart :secondPart ]
    myAudioFile = "slice" + str(n) +".wav"
    tempObject.export(myAudioFile , format="wav")
    n += 1
    # processAudio(tempObject)
    processAudio(myAudioFile)
    print ("")