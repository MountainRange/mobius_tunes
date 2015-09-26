#!/usr/bin/env python3

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

class mobius_py:

	def __init__(self, parts=500):
		self.fileloader = file_manager.file_manager()
		self.parts = parts


	# returns a list of lists of points in the song with similar frequencies
	def loadConnections(self, playList):
		return []

	def fractureSong(self, song, connections):
		fragments = []
		for breakPoint in connections:
			fragments.append(song[:])
		return fragments



		# load connections list with song links
		connections = self.loadConnections(song)

	def main(self):
		# get songs
		song = self.fileloader.load_from_mp3("testmusic/funkychunk.mp3", useTemp = False) #for each song

		self.fileloader.generate_tempfile()
		print(self.fileloader.get_tempfile())

		# Write mp3 to wav
		filename = self.fileloader.write_to_wav("filename.wav", song)

		# Get only last bit of filename. If this errors, no match!
		match = re.compile("[^/\\\\]*$").search(filename.name).group()


		wavedata, rawdata = self.fileloader.get_raw_from_wav(match)

		# PERFORM SOME CHANGES
		#
		# Test modification

		datalist = [rawdata[0:(int(len(rawdata)/self.parts))]]
		for i in range(1, self.parts):
			datalist += [rawdata[(int(len(rawdata)/self.parts)*(i)):(int(len(rawdata)/self.parts)*(i+1))]]

		rebuiltdata = b''
		for i in range(0, 1):
			a = np.frombuffer(datalist[i+4], np.int16)
			b = np.frombuffer(datalist[i+5], np.int16)
			
			a1 = copy.deepcopy(a[len(a)-100:]).astype(float)
			b1 = copy.deepcopy(b[:100]).astype(float)
			
			automax = np.max(np.correlate(a1, a1, mode='full'))
			
			compmax = np.max(np.correlate(a1, b1, mode='full'))

			similarity = compmax / automax

			print (automax)
			print (compmax)
			print (similarity)

			#plt.plot(npf.ifft(npf.fft(a1)) * npf.fft(a1))
			#plt.plot(npf.ifft(npf.fft(a1)) * npf.fft(b1))
			
			auto = np.correlate(a1, a1, mode='same')
			other = np.correlate(a1, b1, mode='same')

			plt.plot(auto)
			plt.plot(other)
			plt.show()
			
			rebuiltdata += bytes(a)

		playList = []
		playList.append(song)

		# load connections list with song links
		connections = self.loadConnections(playList)
		sorted(connections, key = itemgetter(0))

		# Write changes
		self.fileloader.write_raw_to_wav("temporaryOutput.wav", wavedata, rebuiltdata)
		song = self.fileloader.load_from_wav("temporaryOutput.wav")

		# play song. We need to allow the song to randomly jump via connections[]
		songFragments = self.fractureSong(song, connections)
		play(song)
		random.randint(0,2)

def rfft_xcorr(x, y):
	M = len(x) + len(y) - 1
	N = 2 ** int(np.ceil(np.log2(M)))
	X = np.fft.rfft(x, N)
	Y = np.fft.rfft(y, N)
	cxy = np.fft.irfft(X * np.conj(Y))
	cxy = np.hstack((cxy[:len(x)], cxy[N-len(y)+1:]))
	return cxy

if __name__ == "__main__":
	mobius = mobius_py()
	mobius.main()
