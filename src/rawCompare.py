import signal
import sys
import wave
import re
import audioop
import random
import tempfile
import file_manager
import numpy as np
import numpy.fft as npf
import copy
from pydub import AudioSegment
from pydub.playback import play
from operator import itemgetter
import matplotlib.pyplot as plt

class rawCompare:
	
	def compare(self, rawdata, parts):
			datalist = [rawdata[0:(int(len(rawdata)/parts))]]
			for i in range(1, parts):
				datalist += [rawdata[(int(len(rawdata)/parts)*(i)):(int(len(rawdata)/parts)*(i+1))]]

			rebuiltdata = b''
			simMat = np.zeros((len(datalist),len(datalist)))
			for i in range(len(datalist)):
				for j in range(len(datalist)):
					if j == i:
						simMat[i][j] = 0
						continue
					a = np.frombuffer(datalist[i], np.int16)
					b = np.frombuffer(datalist[j], np.int16)

					a1 = copy.deepcopy(a[len(a)-100:]).astype(float)
					b1 = copy.deepcopy(b[:100]).astype(float)

					automax = np.max(np.correlate(a1, a1, mode='full')[50:])

					compmax = np.max(np.correlate(a1, b1, mode='full')[50:])

					similarity = compmax / automax

					#print (automax)
					#print (compmax)
					#print (similarity)
					if similarity <= 1 and similarity > 0:
						simMat[i][j] = similarity
					else:
						simMat[i][j] = 0

				#plt.plot(npf.ifft(npf.fft(a1)) * npf.fft(a1))
				#plt.plot(npf.ifft(npf.fft(a1)) * npf.fft(b1))

				auto = np.correlate(a1, a1, mode='same')
				other = np.correlate(a1, b1, mode='same')
				#plt.plot(auto)
				#plt.plot(other)
				#plt.show()

				#rebuiltdata += bytes(a)

			print (simMat)

			maxIndices = np.argpartition(simMat, -4)[-4:]

			simMat = simMat.ravel()
			simMat.sort()
			simMat = simMat[::-1]


			return simMat[:10]
