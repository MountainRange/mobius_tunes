
from mobius.file_manager import file_manager
from mobius.progress_bar import progress_bar

import signal
import sys
import wave
import re
import audioop
import random
import tempfile
import numpy as np
import numpy.fft as npf
import copy
from operator import itemgetter
import warnings
from scipy import signal

class rawCompare:

	def compare(self, rawdata, parts, chunksize=200, threshold=1, maxStop=None):
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

				a = np.frombuffer(datalist[i], np.int16)
				b = np.frombuffer(datalist[j], np.int16)

				a1 = copy.deepcopy(a[len(a)-chunksize:]).astype(float)
				b1 = copy.deepcopy(b[:chunksize]).astype(float)

				automax = threshold * np.max(np.correlate(a1, a1, mode='full')[(chunksize/2):])

				compmax = np.max(np.correlate(a1, b1, mode='full')[(chunksize/2):])

				similarity = compmax / automax

				#print (automax)
				#print (compmax)
				#print (similarity)
				if similarity <= 1 and similarity > 0:
					simMat[i][j] = similarity
				else:
					simMat[i][j] = 0

			# Requires import of matplot lib as plt
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

	def compareAll(self, rawdatas, parts=100, chunksize=100, threshold=1.0, maxStop=None):
		if maxStop == None:
			maxStop = len(rawdatas)*500

		datalist = []
		for rawdata in rawdatas:
			datasize = int((int(len(rawdata)/parts))/2)*2
			datalist.append(rawdata[0:datasize])
			for i in range(1, parts):
				datalist.append(rawdata[(datasize*(i)):(datasize*(i+1))])

		rebuiltdata = b''
		simMat = np.zeros((len(datalist),len(datalist)))
		print ("CALCULATING")
		bar = progress_bar(50)
		for i in range(len(datalist)):
			bar.update_bar(bar.get_value())
			if i % 15 == 0 and i != 0:
				#print (str(i) + " parts processed.")
				bar.update_bar((i/chunksize/len(rawdatas))*50)
			for j in range(len(datalist)):
				chunki = chunksize * i
				if (j in range(i-10, i+10)) or (j > chunki and j < (chunki)+25) or (j > (chunki)+chunksize-25 and j < (chunki)+chunksize):
					simMat[i][j] = 0
					continue
				a = np.frombuffer(datalist[i], np.int16)
				b = np.frombuffer(datalist[j], np.int16)

				doublechunk = chunksize * 2
				halfchunk = chunksize/2

				with warnings.catch_warnings():
					warnings.simplefilter("ignore")
					apre = copy.deepcopy(a[len(a)-chunksize:]).astype(float)
					a1 = np.zeros(doublechunk)
					a1[halfchunk:halfchunk+chunksize] = apre
					bpre = copy.deepcopy(b[:chunksize]).astype(float)
					b1 = np.zeros(doublechunk)
					b1[halfchunk:halfchunk+chunksize] = bpre

					#automax = np.max(np.correlate(a1, a1, mode='full')[(chunksize/2):])
					c = signal.fftconvolve(b1, apre[::-1], mode='valid')
					automax = np.max(c)

					#compmax = np.max(np.correlate(a1, b1, mode='full')[(chunksize/2):])
					d = signal.fftconvolve(a1, apre[::-1], mode='valid')
					compmax = np.max(d)

					similarity = compmax / automax

				#print (automax)
				#print (compmax)
				#print (similarity)
				if similarity <= 1 and similarity > 0:
					simMat[i][j] = similarity
				else:
					simMat[i][j] = 0

			# Requires inport of matplot lib as plt
			#plt.plot(npf.ifft(npf.fft(a1)) * npf.fft(a1))
			#plt.plot(npf.ifft(npf.fft(a1)) * npf.fft(b1))

			auto = np.correlate(a1, a1, mode='same')
			other = np.correlate(a1, b1, mode='same')
			#plt.plot(auto)
			#plt.plot(other)
			#plt.show()

			#rebuiltdata += bytes(a)
		bar.complete()


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



