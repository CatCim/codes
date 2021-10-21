#import wave, struct, math, random
#sampleRate = 44100.0 # hertz
#duration = 1.0 # seconds
#frequency = 440.0 # hertz
#obj = wave.open('sound.wav','w')
#obj.setnchannels(1) # mono
#obj.setsampwidth(2)
#obj.setframerate(sampleRate)
#for i in range(99999):
#   value = random.randint(-32767, 32767)
#   data = struct.pack('<h', value)
#   obj.writeframesraw( data )
#obj.close()

##########
#from scipy.io.wavfile import write
#import numpy as np
#samplerate = 44100; fs = 100
#t = np.linspace(0., 1., samplerate)
#amplitude = 1#np.iinfo(np.int16).max
#data = amplitude * np.sin(2. * np.pi * fs * t)
#print(data)
#write("example.wav", samplerate, data.astype(np.int16))

#########
## https://pythonaudiosynthesisbasics.com
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt, scipy

sample_rate = 44100

def soundGene(sr,duration,fq,amp):
	x = np.linspace(0,duration*2*np.pi,int(sr*duration))
	sinewave_data = np.sin(fq*x)
	sinewave_data = sinewave_data*amp
	sd.play(sinewave_data,sr)
	sd.wait()
	sd.stop()
def soundGene2(sr,duration,fq,amp):
	x = np.linspace(0,duration*2*np.pi,int(sr*duration))
	sinewave_data = np.sin(fq*x)
	sinewave_data = sinewave_data*amp

	envelop_start=(np.linspace(0,.5,1000))
	envelop_end=(np.linspace(.5,0,1000))
	envelop_mid=np.repeat(.5,(len(sinewave_data)-len(envelop_start)-len(envelop_end)))
	envelop = np.concatenate((envelop_start,envelop_mid,envelop_end),axis=None)

	sinewave_data=sinewave_data*envelop

	return sinewave_data
	#plot_data = sinewave_data[:500] # slicing 500 samples off of your wavfile should show about 5 cycles
	#fig,ax = plt.subplots()
	#ax.plot(plot_data,linewidth=3)
	#ax.plot(plot_data,linewidth=3)
	#plt.xlabel("Sample Number")
	#plt.ylabel("Amplitude")
	#plt.title("Sine Wave")
	#plt.show()
	#plt.close()

#tone=soundGene2(44100,1,440,.5)
#sd.play(tone,44100)
#sd.wait()
#envelop_start=(np.linspace(0,.5,1000))
#envelop_end=(np.linspace(.5,0,1000))
#envelop_mid=np.repeat(.5,(len(tone)-len(envelop_start)-len(envelop_end)))
#envelop = np.concatenate((envelop_start,envelop_mid,envelop_end),axis=None)
#sd.play(tone*envelop,44100)
#sd.wait()

