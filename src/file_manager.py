import wave
import shutil
import copy
import audioop
import random
import os
import tempfile
import file_manager
from pydub import AudioSegment
from pydub.playback import play
from operator import itemgetter


class file_manager(object):

	def __init__(self):
		self.temporaryfile = None

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


	def load_from_mp3(self, path, useTemp = True):
		prefix = self.__sanitize__(useTemp)
		return AudioSegment.from_mp3(prefix + path)

	def write_to_wav(self, path, toWrite, useTemp = True): #
		prefix = self.__sanitize__(useTemp)
		return toWrite.export(prefix + path, format="wav")

	def get_raw_from_wav(self, path, useTemp = True):
		prefix = self.__sanitize__(useTemp)
		toopen = wave.open(prefix +  path)
		toopen.setpos(0)

		return toopen.getparams(), toopen.readframes(toopen.getnframes())

	def load_from_wav(self, path, useTemp = True):
		prefix = self.__sanitize__(useTemp)
		return AudioSegment.from_wav(prefix +  path)

	def write_raw_to_wav(self, path, waveparams, rawdata, useTemp = True):
		prefix = self.__sanitize__(useTemp)
		tempWrite = wave.open(prefix +  path, mode = 'wb')
		tempWrite.setnchannels(waveparams[0])
		tempWrite.setsampwidth(waveparams[1])
		tempWrite.setframerate(waveparams[2])
		tempWrite.setnframes(waveparams[3])
		tempWrite.writeframesraw(rawdata)
