import wave
import shutil
import copy
import audioop
import random
import os
import tempfile
import glob
import pyglet
from operator import itemgetter
import time

#define stream chunk
chunk = 32
bitrate = "256k"

class file_manager(object):

	def __init__(self):
		self.temporaryfile = None
		self.pyglet_player = None

	def generate_tempfile(self):
		self.temporaryfile = tempfile.mkdtemp()
		self.temporaryfile = self.temporaryfile + "/"
		return copy.deepcopy(self.temporaryfile)

	def get_tempfile(self):
		return copy.deepcopy(self.temporaryfile)

	def delete_tempfile(self, path = None):
		if path == None:
			path = self.temporaryfile
		if path == None:
			print("Temp File was not created yet!")
			return
		shutil.rmtree(path)

	def set_tempfile(self, path):
		if path[-1:] != "/":
			path = path + "/"
		self.temporaryfile = path

	def __sanitize__(self, useTemp = True):
		if (useTemp == False) :
			return ""
		if self.temporaryfile == None:
			self.generate_tempfile()
		return self.temporaryfile


	def load_raw_from_mp3(self, path, useTemp = True):
		prefix = self.__sanitize__(useTemp)
		music = pyglet.media.load(prefix + path)
		byteList = []
		toAppend = music.get_audio_data('')

		if music == None:
			print("An empty file was found! This probably means avbin was incorrectly installed.")
			exit(1)

		wavedata = [music.audio_format.channels, int(music.audio_format.sample_size / 8),
				music.audio_format.sample_rate, None]

		while toAppend != None:
			if (toAppend.get_string_data() != None):
				byteList.append(toAppend.get_string_data())
			toAppend = music.get_audio_data('')

		toReturn = b''.join(byteList)
		wavedata[3] = int(len(toReturn) / 4)


		return wavedata, toReturn

	def load_raw_mp3_from_folder(self, path):
		toReturn = []
		for f in glob.glob(path + "/*.mp3"):
			toReturn.append(self.load_raw_from_mp3(f, useTemp = False))
		return toReturn


	def write_to_wav(self, path, toWrite, useTemp = True): #
		prefix = self.__sanitize__(useTemp)
		return toWrite.export(prefix + path, format="wav", bitrate = bitrate)

	def get_raw_from_wav(self, path, useTemp = True):
		prefix = self.__sanitize__(useTemp)
		toopen = wave.open(prefix +  path)
		toopen.setpos(0)

		return toopen.getparams(), toopen.readframes(toopen.getnframes())

	def write_raw_to_wav(self, path, waveparams, rawdata, useTemp = True):
		prefix = self.__sanitize__(useTemp)
		tempWrite = wave.open(prefix +  path, mode = 'wb')
		tempWrite.setnchannels(waveparams[0])
		# tempWrite.setsampwidth(waveparams[1])
		tempWrite.setsampwidth(2)
		tempWrite.setframerate(waveparams[2])
		tempWrite.setnframes(waveparams[3])
		tempWrite.writeframesraw(rawdata)

		return prefix + path

	def play_wav_file(self, path, useTemp = True):
		prefix = self.__sanitize__(useTemp)
		sound = pyglet.media.load(prefix + path, streaming=False)
		sound.play();

	def queue_wav_file(self, path, useTemp = True):
		print ("FRAGMENT ADDED TO QUEUE")
		if self.pyglet_player == None:
			self.pyglet_player = pyglet.media.Player()

		prefix = self.__sanitize__(useTemp)
		self.pyglet_player.queue(pyglet.media.load(prefix + path, streaming=False))
		self.pyglet_player.play()

	def play_raw_data(self, waveparams, rawdata, queue = False):
		filename = str(random.randint(0, 99999999))
		#open a wav format music
		self.write_raw_to_wav(self.get_tempfile() + filename, waveparams, rawdata, False)
		if queue:
			self.queue_wav_file(self.get_tempfile() + filename, False)
		else:
			self.play_wav_file(self.get_tempfile() + filename, False)
