#!/usr/bin/env python3

from mobius.file_manager import file_manager
from mobius.command_line_flags import command_line_flags
from mobius.rawCompare import rawCompare

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
import time
import os
from operator import itemgetter

yes = set(['yes','y', 'ye', 'yah', 'ya'])
no = set(['no','n', 'nah', 'na'])
__version__ = '0.1.0'

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
		self.fileloader = file_manager()
		self.rawCompare = rawCompare()
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
		# initialize some variables
		cl = command_line_flags()
		chunksize = 500
		directory = "mobius/testmusic"
		threshold = 1.0
		opts = cl.get_arguments()
		for opt in opts:
			if opt[0] == '-d':
				directory = opt[1]
				print("Directory: " + directory)
			elif opt[0] == '-t':
				threshold = (float) (opt[1])
				print("Similarity threshold: " + (str) (threshold))
			elif opt[0] == '-c':
				chunksize = (int) (opt[1])
				print("Size of song chunks: " + (str) (chunksize))

		if not os.path.isdir(directory):
			print(directory + " was not found, specify a directory with -d <DIR>...")
			exit(2)

		# get songs
		songs = self.fileloader.load_raw_mp3_from_folder(directory) #for each song

		self.fileloader.generate_tempfile()
		print(self.fileloader.get_tempfile())

		# Write mp3 to wav
		filenames = []
		rawdatas = []
		wavedata = b''
		num = 0
		for song in songs:
			num += 1
			filename = self.fileloader.write_raw_to_wav("filename" + str(num) + ".wav", song[0], song[1])

			# Get only last bit of filename. If this errors, no match!
			match = re.compile("[^/\\\\]*$").search(filename).group()


			wavedata, rawdata = self.fileloader.get_raw_from_wav(match)
			rawdatas.append(rawdata)

		# PERFORM SOME CHANGES
		#
		# Test modification

		fragDict, datalist = self.rawCompare.compareAll(copy.deepcopy(rawdatas), self.parts, chunksize, threshold)

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
				if (random.randint(0, 4) == 1 and len(currentfrags) > 256000) or len(currentfrags) > 2560000:
					print ("JUMPED ADDED")
					self.fileloader.play_raw_data(wavedata, currentfrags, queue = True)
					time.sleep((len(currentfrags)/256000)-1)
					currentfrags = b''
					i = fragDict[i]
			i += 1

		playList = []
		#playList.append(song)

		# Write changes
		#self.fileloader.write_raw_to_wav("temporaryOutput.wav", wavedata, frags)
		#song = self.fileloader.load_from_wav("temporaryOutput.wav")

		# play song. We need to allow the song to randomly jump via connections[]
		#songFragments = self.fractureSong(song, connections)
		# play(song)

		# Do not remove unless debugging
		self.signal_handler(signal.SIGINT, None)

def main():
	try:
		mob = mobius_py()
		mob.main()
	except Exception:
		mob.fileloader.delete_tempfile()
		e = sys.exc_info()[0]
		write_to_page( "<p>Error: %s</p>" % e )

if __name__ == '__main__':
    main()

