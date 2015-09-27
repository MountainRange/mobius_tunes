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
	
	def compare(self, rawdata, parts=100, chunksize=200, maxStop=None):
		if maxStop == None:
			maxStop = 500
		datalist = [rawdata[0:(int(len(rawdata)/parts))]]
		for i in range(1, parts):
			datalist += [rawdata[(int(len(rawdata)/parts)*(i)):(int(len(rawdata)/parts)*(i+1))]]

		rebuiltdata = b''
		simMat = np.zeros((len(datalist),len(datalist)))
		for i in range(len(datalist)):
			if i % 100 == 0 and i != 0:
				print (str(i) + " parts processed.")
			for j in range(len(datalist)):
				if j in range(i-10, i+10):
					simMat[i][j] = 0
					continue

				a = np.frombuffer(datalist[i], np.int8)
				b = np.frombuffer(datalist[j], np.int8)

				a1 = copy.deepcopy(a[len(a)-chunksize:]).astype(float)
				b1 = copy.deepcopy(b[:chunksize]).astype(float)

				automax = np.max(np.correlate(a1, a1, mode='full')[(chunksize/2):])

				compmax = np.max(np.correlate(a1, b1, mode='full')[(chunksize/2):])

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

		#print (simMat)

		indexArr = copy.deepcopy(simMat)

		maxIndices = np.argpartition(simMat, -4)[-4:]

		simMat = simMat.ravel()
		simMat.sort()
		simMat = simMat[::-1]
		
		top = simMat[:100]

		test = []

		for i in range(len(top)):
			test.append(np.asarray(np.where(indexArr == top[i])).T[0].tolist())

		fragList = []
	
		fragDict = {test[0][0]: test[0][1]}

		for i in range(len(test)):
			fragList.append(datalist[test[i][0]] + datalist[test[i][1]])
			fragDict[test[i][0]] = test[i][1]

		print ("TEST")

		test2 = datalist[0]
		i = 1
		stopNum = 0;
		while i < len(datalist):
			stopNum += 1
			if stopNum == int(maxStop / 2):
				print ("50% DONE")
			if stopNum >= maxStop:
				break
			test2 += datalist[i]
			print (i)
			if i % 500 == 499:
				i -= 499
			if i in fragDict:
				if random.randint(0, 4) == 1:
					print ("YES")
					i = fragDict[i]
			i += 1
		print ("TEST2")

		return test2

	def compareAll(self, rawdatas, parts=100, chunksize=200, maxStop=None):
		if maxStop == None:
			maxStop = len(rawdatas)*500
		datalist = []
		for rawdata in rawdatas:
			datalist.append(rawdata[0:(int(len(rawdata)/parts))])
			for i in range(1, parts):
				datalist.append(rawdata[(int(len(rawdata)/parts)*(i)):(int(len(rawdata)/parts)*(i+1))])

		rebuiltdata = b''
		simMat = np.zeros((len(datalist),len(datalist)))
		print ("CALCULATING")
		for i in range(len(datalist)):
			if i % 100 == 0 and i != 0:
				print (str(i) + " parts processed.")
			for j in range(len(datalist)):
				if j in range(i-10, i+10):
					simMat[i][j] = 0
					continue
				a = np.frombuffer(datalist[i], np.int8)
				b = np.frombuffer(datalist[j], np.int8)

				a1 = copy.deepcopy(a[len(a)-chunksize:]).astype(float)
				b1 = copy.deepcopy(b[:chunksize]).astype(float)

				automax = np.max(np.correlate(a1, a1, mode='full')[(chunksize/2):])

				compmax = np.max(np.correlate(a1, b1, mode='full')[(chunksize/2):])

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
		print ("CALCULATED")

		#print (simMat)

		indexArr = copy.deepcopy(simMat)

		maxIndices = np.argpartition(simMat, -4)[-4:]

		simMat = simMat.ravel()
		simMat.sort()
		simMat = simMat[::-1]
		
		top = simMat[:(100*len(rawdatas))]

		test = []

		for i in range(len(top)):
			test.append(np.asarray(np.where(indexArr == top[i])).T[0].tolist())
		fragList = []
	
		fragDict = {test[0][0]: test[0][1]}

		for i in range(len(test)):
			fragList.append(datalist[test[i][0]] + datalist[test[i][1]])
			fragDict[test[i][0]] = test[i][1]
		
		return fragDict, datalist



