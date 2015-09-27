#!/usr/bin/env python3

import signal
import sys
import wave
import re
import audioop
import random
import tempfile
import file_manager
import command_line_flags
import numpy as np
import numpy.fft as npf
import copy
import time
from pydub import AudioSegment
from pydub.playback import play
from operator import itemgetter
import matplotlib.pyplot as plt
import rawCompare


yes = set(['yes','y', 'ye', 'yah', 'ya'])
no = set(['no','n', 'nah', 'na'])

class mobius_py:

	def signal_handler(self, signal=signal.SIGINT, frame=None):
		choice = input('Would you like to keep your tmp files [yN]: ').lower()
		if choice in yes:
			print("Find your tmp files at: " + self.fileloader.get_tempfile())
		elif choice in no:
			self.fileloader.delete_tempfile()
		else:
			self.fileloader.delete_tempfile()
		exit(0)

	def __init__(self, parts=100):
		self.fileloader = file_manager.file_manager()
		self.rawCompare = rawCompare.rawCompare()
		self.parts = parts
		signal.signal(signal.SIGINT, self.signal_handler)


	# returns a list of lists of points in the song with similar frequencies
	def loadConnections(self, playList):
		return []

	def fractureSong(self, song, connections):
		fragments = []
		i = 0
		while (i < len(connections)):
			i += 1
			fragments.append(song[:connections[i][0]])
			song = song[connections[i]:]
		return fragments

	def main(self):
		# get songs
		songs = self.fileloader.load_mp3_from_folder("testmusic") #for each song
		if not cl.get_directory() == 0:
			songs = self.fileloader.load_mp3_from_folder(cl.get_directory())
			print("Directory: " + cl.get_directory())

		self.fileloader.generate_tempfile()
		print(self.fileloader.get_tempfile())

		# Write mp3 to wav
		filenames = []
		rawdatas = []
		wavedata = b''
		num = 0
		for song in songs:
			num += 1
			filename = self.fileloader.write_to_wav("filename" + str(num) + ".wav", song)

			# Get only last bit of filename. If this errors, no match!
			match = re.compile("[^/\\\\]*$").search(filename.name).group()


			wavedata, rawdata = self.fileloader.get_raw_from_wav(match)
			rawdatas.append(rawdata)

		# PERFORM SOME CHANGES
		#
		# Test modification

		fragDict, datalist = self.rawCompare.compareAll(copy.deepcopy(rawdatas), self.parts)

		currentfrags = datalist[0]
		i = 1
		stopNum = 0
		maxStop = 100000
		print ("CALCULATING JUMPS")
		while i < len(datalist):
			stopNum += 1
			if stopNum == int(maxStop / 2):
				print ("50% DONE")
			if stopNum >= maxStop:
				break
			currentfrags += datalist[i]
			if i % self.parts == self.parts-1:
				i -= self.parts-1
			if i in fragDict:
				if (random.randint(0, 4) == 1 and len(currentfrags) > 256000) or len(currengfrags) > 2560000:
					print ("JUMPED ADDED")
					self.fileloader.play_raw_data(wavedata, currentfrags, queue = True)
					time.sleep((len(currentfrags)/256000)-1)
					currentfrags = b''
					i = fragDict[i]
			i += 1

		playList = []
		#playList.append(song)

		# load connections list with song links
		connections = self.loadConnections(playList)
		sorted(connections, key = itemgetter(0))

		# Write changes
		#self.fileloader.write_raw_to_wav("temporaryOutput.wav", wavedata, frags)
		#song = self.fileloader.load_from_wav("temporaryOutput.wav")

		# play song. We need to allow the song to randomly jump via connections[]
		#songFragments = self.fractureSong(song, connections)
		# play(song)

		# Do not remove unless debugging
		self.signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
	try:
		cl = command_line_flags.command_line_flags()
		mobius = mobius_py()
		mobius.main()
	except Exception:
		mobius.fileloader.delete_tempfile()
		e = sys.exc_info()[0]
		write_to_page( "<p>Error: %s</p>" % e )
