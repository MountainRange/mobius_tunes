#!/usr/bin/env python3

import wave
import audioop
import random
import tempfile
import file_manager
import numpy as np
import copy
from pydub import AudioSegment
from pydub.playback import play
from operator import itemgetter

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
		song = self.fileloader.load_from_mp3("testmusic/funkychunk.mp3") #for each song

		folder = tempfile.mkdtemp()
		print(folder)

		# Write mp3 to wav
		filename = self.fileloader.write_to_wav(folder + "/filename.wav", song)

		wavedata, rawdata = self.fileloader.get_raw_from_wav(filename.name)

		# PERFORM SOME CHANGES
		#
		# Test modification
		
		datalist = [rawdata[0:(int(len(rawdata)/self.parts))]]
		for i in range(1, self.parts):
			datalist += [rawdata[(int(len(rawdata)/self.parts)*(i)):(int(len(rawdata)/self.parts)*(i+1))]]

		rebultdata = b''
		for i in range(0, len(datalist)):
			d = np.frombuffer(datalist[i], np.int16)
			b = copy.deepcopy(d)
			a = 5
			for i in range(0, a):
				b[:] += np.mean(d, 0)
			rebultdata += bytes(b)

		playList = []
		playList.append(song)

		# load connections list with song links
		connections = self.loadConnections(playList)
		sorted(connections, key = itemgetter(0))

		# Write changes
		self.fileloader.write_raw_to_wav(folder + "/temporaryOutput.wav", wavedata, rebultdata)
		song = self.fileloader.load_from_wav(folder + "/temporaryOutput.wav")

		# play song. We need to allow the song to randomly jump via connections[]
		songFragments = self.fractureSong(song, connections)
		play(song)
		random.randint(0,2)

if __name__ == "__main__":
	mobius = mobius_py()
	mobius.main()
