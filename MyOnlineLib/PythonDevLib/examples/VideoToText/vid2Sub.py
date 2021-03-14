#pip install SpeechRecognition
#pip install ffmpeg moviepy
#pip install googletrans==3.1.0a0
#usage\

#install C:\Program Files\mp3splt\mp3splt_doc as cmd line interface
#install -ffmpeg-on-windows for mp3 support
#C:\Users\ndhavalikar\Desktop\VideoToText>python.exe vid2Sub.py C:\Users\ndhavalikar\Desktop\VideoToText\vid\japVid.mp4
import subprocess
import io
import os
import wave
import re
import sys

from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import make_chunks
from googletrans import Translator
import speech_recognition as sr
import noisereduce as nr

import moviepy.editor as mp
from moviepy import *

import numpy
import scipy.io.wavfile as wf
from pydub import AudioSegment, effects  
'''
#########Audio Nomalize
CHECK:https://stackoverflow.com/questions/42492246/how-to-normalize-the-volume-of-an-audio-file-in-python-any-packages-currently-a
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

sound = AudioSegment.from_file("yourAudio.m4a", "m4a")
normalized_sound = match_target_amplitude(sound, -20.0)
normalized_sound.export("nomrmalizedAudio.m4a", format="mp4")
from pydub import AudioSegment, effects  

rawsound = AudioSegment.from_file("./input.m4a", "m4a")  
normalizedsound = effects.normalize(rawsound)  
normalizedsound.export("./output.wav", format="wav")
'''
logFlg = 0 # set this to create log file
debugFlg = 0 # set this for debug prints
logTxt=""
srtTxt=""
subs = ""
subidx = 1
linesIdx = 1
def splitter(s, n):
    a = [] 
    if(not s):
        return(a)
    else:
        pieces = s.split()
        return (" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n))

def srtEnd(tmpPth):
    global subs
    f = open(tmpPth+"_Sub.srt", "w",encoding='utf8')
    f.write(subs)
    f.close()
def srtDataUpdate(txt,t1,total): #t1 t2 in min
    global subidx
    global linesIdx
    global subs
    tmpTim = 0
    #print(subidx,total)
    if(linesIdx >= total):
        wordPer10sec = len(txt.split())
    else:
        wordPer10sec = int((len(txt.split())/60)*12) #wordper10 sec = (wordperSec*10)
    #print(txt)
    if(wordPer10sec<15):
        wordPer10sec = 15
    listTmp = splitter(txt,wordPer10sec)# 15 words in 10 sec
    
    for lineTmp in listTmp:
        subs += str(subidx)+"\n" +'{:02d}:{:02d}'.format(*divmod(t1, 60))+":"+str((tmpTim)*10).zfill(2)+",000"+" --> "+'{:02d}:{:02d}'.format(*divmod(t1, 60))+":"+str((tmpTim+1)*10).zfill(2)+",000"+"\n"+lineTmp+"\n\n"
        tmpTim = tmpTim + 1
        subidx = subidx + 1
    linesIdx = linesIdx +1
def logWrite(tmpPth):
    global logTxt
    global logFlg
    if(logFlg==1):
        f = open(tmpPth+"_Log.txt", "w",encoding='utf8')
        f.write(logTxt)
        f.close()
def logData(txt,force = 0):
    global logTxt
    global debugFlg
    if(debugFlg==1 or (force == 1)):
        print(txt)
    logTxt += txt + "\n"
def normalizeSound(AudFilePath):
    logData("Normalizing")
    rawsound = AudioSegment.from_file(AudFilePath, AudFilePath.split(".")[1])  
    normalizedsound = effects.normalize(rawsound)  
    normalizedsound.export(AudFilePath, format=AudFilePath.split(".")[1])
def wavVolumeAmpli(fileIn,fileOut,VolumeDb):
    logData("Amplifing")
    wavData = AudioSegment.from_wav(fileIn)
    # boost volume by 5 dB
    more_volume = wavData + VolumeDb
    more_volume.export(fileOut, format="wav")

def mp3VolumeAmpli(fileIn,fileOut,VolumeDb):
    logData("Amplifing")
    mp3Data = AudioSegment.from_mp3(fileIn)
    # boost volume by 5 dB
    more_volume = mp3Data + VolumeDb
    more_volume.export(fileOut, format="mp3")

def wavNoiceReduce(fileIn,FileOut):
    logData("wav file noice Reduction")
    # load data
    rate, wavData = wf.read(fileIn)
    # select section of data that is noise
    #noisy_part = data[10000:15000]
    noisy_part = wavData
    # perform noise reduction
    reduced_noise = nr.reduce_noise(audio_clip=wavData, noise_clip=noisy_part, verbose=True)
    wavData.write(fileOut)
    
def mp3NoiceReduce(fileIn):
    logData("mp3 file noice Reduction")
    mp3towav(fileIn)
    fileIn = fileIn.split(".")[0]+".wav"
    wavNoiceReduce(fileIn,fileIn)
    wavtomp3(fileIn)
    os.remove(fileIn)
class VoiceActivityDetection:

    def __init__(self):
        self.__step = 8000
        self.__buffer_size = 8000 
        self.__buffer = numpy.array([],dtype=numpy.int16)
        self.__out_buffer = numpy.array([],dtype=numpy.int16)
        self.__n = 0
        self.__VADthd = 0.
        self.__VADn = 0.
        self.__silence_counter = 0

    # Voice Activity Detection
    # Adaptive threshold
    def vad(self, _frame):
        frame = numpy.array(_frame) ** 2.
        result = True
        threshold = 0.1
        thd = numpy.min(frame) + numpy.ptp(frame) * threshold
        self.__VADthd = (self.__VADn * self.__VADthd + thd) / float(self.__VADn + 1.)
        self.__VADn += 1.

        if numpy.mean(frame) <= self.__VADthd:
            self.__silence_counter += 1
        else:
            self.__silence_counter = 0

        if self.__silence_counter > 20:
            result = False
        return result

    # Push new audio samples into the buffer.
    def add_samples(self, data):
        self.__buffer = numpy.append(self.__buffer, data)
        result = len(self.__buffer) >= self.__buffer_size
        # print('__buffer size %i'%self.__buffer.size)
        return result

    # Pull a portion of the buffer to process
    # (pulled samples are deleted after being
    # processed
    def get_frame(self):
        window = self.__buffer[:self.__buffer_size]
        self.__buffer = self.__buffer[self.__step:]
        # print('__buffer size %i'%self.__buffer.size)
        return window

    # Adds new audio samples to the internal
    # buffer and process them
    def process(self, data):
        if self.add_samples(data):
            tot= (len(self.__buffer))
            i = 0
            while len(self.__buffer) >= self.__buffer_size:
                # Framing
                i += self.__buffer_size
                DisplayBar("Silence Remove",i+1,tot)
                window = self.get_frame()
                # print('window size %i'%window.size)
                if self.vad(window):  # speech frame
                    self.__out_buffer = numpy.append(self.__out_buffer, window)
                # print('__out_buffer size %i'%self.__out_buffer.size)

    def get_voice_samples(self):
        return self.__out_buffer

def DisplayBar(Heading,Per,max):# display persentage   
    global debugFlg
    if(debugFlg==1):
        tmp = Heading + ": "+"#"*(int((Per/max)*20)) +" [" +str(int((Per/max)*100)) +"%]"
        sys.stdout.write("\r"+tmp)
        sys.stdout.flush()

def Speech2TxtLarge(audioFilePath,audioLang):
    logData("Converting Audio To Text")
    ListTxt = [] 
    txt =""
    tmpFormat = audioFilePath.split(".")[1]
    # split mp3 file
    a = os.system("mp3splt -Q -t 1.0 "+audioFilePath+" -o @n_@t") # split file in 1min each
    index = 1
    wkspFldr = os.path.dirname(audioFilePath) +"\\"
    flag = 1 # mp3spli append file name 0 if total files > 9
    fileMp3 = wkspFldr +"00"+str(index)+"_.mp3"
    fileMp3_tmp = wkspFldr +"0"+str(index)+"_.mp3"
    if(os.path.exists(fileMp3)):
        flag = 3
    elif(os.path.exists(fileMp3_tmp)):
        flag = 2
        fileMp3 = fileMp3_tmp
    else:
        fileMp3 = wkspFldr + str(index)+"_.mp3"
    if(not os.path.exists(fileMp3)):
        logData("Error no file Found")
        exit()
    while(os.path.exists(fileMp3)):
        mp3VolumeAmpli(fileMp3,fileMp3,10) #10 db file
        normalizeSound(fileMp3)
        mp3towav(fileMp3)
        os.remove(fileMp3)
        fileWav = fileMp3.split(".")[0]+".wav"

        # we only take .wav file fom here
        fileSource = sr.AudioFile(fileWav)#'harvard.wav'
        r = sr.Recognizer()
        with fileSource as source:
            try:
                r.adjust_for_ambient_noise(source)
                audio = r.record(source)
                tmpTxt = r.recognize_google(audio,language=audioLang)
                #print(tmpTxt)
                #tmpTxt = str(index-1) + ":" + tmpTxt
                txt += tmpTxt +"\n\n"
                ListTxt.append(tmpTxt +"\n\n")
                logData(tmpTxt,0)
            except sr.RequestError:
                tmpTxt = str(index-1) + ":"
                txt += tmpTxt +"\n\n"
                ListTxt.append(tmpTxt +"\n\n")
                logData(str(index-1) + ": unresponsive",0)
            except sr.UnknownValueError:
                tmpTxt = str(index-1) + ":"
                txt += tmpTxt +"\n\n"
                ListTxt.append(tmpTxt +"\n\n")
                logData(str(index-1) + ": unintelligible",0)
        DisplayBar("Sph2Txt: ",index,100)
        os.remove(fileWav)
        index = index + 1
        fileMp3 = wkspFldr + str(index).zfill(flag)+"_.mp3"
        #print(fileMp3)
    DisplayBar("Sph2Txt: ",index,index)
    return(ListTxt)


def Speech2TxtStream(audioFilePath,audioLang):
    txt =""
    with open(audioFilePath, 'rb') as fh:
        contents = io.BytesIO(fh.read())
    
    fileSource = sr.AudioFile(contents)#'harvard.wav'

    r = sr.Recognizer()
    with fileSource as source:
        try:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
            tmpTxt = r.recognize_google(audio,language=audioLang)
            print(tmpTxt)
            txt += tmpTxt
        except sr.RequestError:
            print("API was unreachable or unresponsive")
        except sr.UnknownValueError:
            print("speech was unintelligible")
    print("Text in Input :")
    print(txt) # creates subtitles
    return(txt)
'''
def video2audio1(vidPath,audPath):
    #vidPath = C:/test.mp4 , audPath =audio.wav
    command = "ffmpeg -i " + vidPath + " -ab 160k -ac 2 -ar 44100 -vn "+audPath
    subprocess.call(command, shell=True)
'''
def Traslate(txtLst,SrcLng,DestLng):
    # traslate api by google have max limit of 2k , so we send traslate request in chunk
    logData("Translating to Language ( " + DestLng + "):")
    translator = Translator() #dest='en' dest='ja'
    tmpTxt = ""
    idx = 0
    for txt in txtLst:
        translation = translator.translate(txt, dest=DestLng , src=SrcLng)
        tmpTxt = formatText(translation.text) + "\n"
        srtDataUpdate(tmpTxt,idx,len(txtLst)) # assuming one munit for srt
        idx = idx +1
        logData (tmpTxt)
    return(translation.text)
def formatText(text):
    pat = ('(?<!Dr)(?<!Esq)\. +(?=[A-Z])')
    return(re.sub(pat,'.\n',text))
def wrap_by_word(s, n):
    '''returns a string where \\n is inserted between every n words'''
    a = s.split()
    ret = ''
    for i in range(0, len(a), n):
        ret += ' '.join(a[i:i+n]) + '\n'

    return ret
# extrect audio from video file
def AmplifyAudioInVidioFile(VidfilePath,factor):
    logData("Amplifying Audio in Audio")
    my_clip = mp.VideoFileClip(VidfilePath)
    return(my_clip.volumex(factor))
def AmplifyAudioInAudioFile(AudioPath,factor):
    logData("Amplifying Audio")
    my_clip = mp.AudioFileClip(AudioPath)
    return(my_clip.volumex(factor))
def video2audioLarge(vidPath,audPath): #https://ffmpeg.org/ffmpeg.html is one cli tool for all video audio processing
    os.system("ffmpeg -i "+vidPath+" -loglevel fatal -f mp3 -ab 192000 -y -vn "+'-af "highpass=f=200, lowpass=f=3000" '+audPath)
def video2audio2(vidPath,audPath):    # this support vidio file up to 30 min 
    my_clip = mp.VideoFileClip(vidPath)
    #amplify volume
    my_clip.audio.write_audiofile(audPath)
def mp3towav(mp3Path):
    # convert wav to mp3
    dst = mp3Path.split(".")[0] + ".wav"
    sound = AudioSegment.from_mp3(mp3Path)
    sound.export(dst, format="wav")
def wavtomp3(mp3Path):
    # convert wav to mp3
    dst = mp3Path.split(".")[0] + ".mp3"
    sound = AudioSegment.from_wav(mp3Path)
    sound.export(dst, format="mp3")
print("\n-------Video to Subtitle Tool----------")
print("\n---------Tool Need Internet------------")
print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))
#print ("\n-------------------------------\n")
if(len(sys.argv) >= 2):
    vidPathTest = sys.argv[1]#video file path  , "vid\japVid.mp4" #"vid\engVid.mp4"
    #vidPathTest = "vid\engVid.mp4"
    tmpPth = vidPathTest.split(".")[0]
    audPathTest =  tmpPth+"_Audio.mp3"#"out\VidTest.wav" # can also convert to .mp3 or other format
    #audNoSiPathTest ="out/NoSilence.wav"
    audNoSiPathTest = tmpPth+"_compAudio.mp3"
    fromLng = "ja"#"ja" #'en-US'
    toLng = "en"#"en"  #"'en-US' #methods accept a BCP-47 language tag, such as 'en-US' for American English, or 'fr-FR' for French.
    if(len(sys.argv) != 3):#its a vidio file
        print("converting Video to Audio")
        video2audioLarge(vidPathTest,audPathTest)
        #mp3VolumeAmpli(audPathTest,audPathTest,10) #10 db file
        #normalizeSound(audPathTest)
        
    else: #its a audio file
        #clip = AmplifyAudioInAudioFile(vidPathTest,10)
        #newApliAud = vidPathTest.split(".")[0]+"Amp." + vidPathTest.split(".")[1]
        #clip.write_audiofile(newApliAud)
        audPathTest = vidPathTest
    if(0):
        print("Removing Silence from Audio")
        removeSilence(audPathTest,audNoSiPathTest)
    else:
        audNoSiPathTest = audPathTest
    print("converting Audio to Text")
    txtLst = Speech2TxtLarge(audNoSiPathTest,fromLng)
    #if(len(sys.argv) != 3):#its a vidio file input so delete .mp3 file generated
    #os.remove(audNoSiPathTest)
    print("Translating")
    trTxt = Traslate(txtLst,fromLng,toLng)
    logWrite(tmpPth)
    srtEnd(tmpPth)
    #Traslate(trTxt,fromLng) #test purpose
'''
LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
  '''