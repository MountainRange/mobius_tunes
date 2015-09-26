import wave
import audioop
import random
import tempfile
import file_manager
from pydub import AudioSegment
from pydub.playback import play
from operator import itemgetter


class file_manager(object):

	def load_from_mp3(self, path):
		return AudioSegment.from_mp3(path)

	def write_to_wav(self, path, toWrite):
		return toWrite.export(path, format="wav")

	def get_raw_from_wav(self, path):
		toopen = wave.open(path)
		toopen.setpos(0)

		return toopen.getparams(), toopen.readframes(toopen.getnframes())

	def load_from_wav(self, path):
		return AudioSegment.from_wav(path)

	def write_raw_to_wav(self, path, waveparams, rawdata):
		tempWrite = wave.open(path, mode = 'wb')
		tempWrite.setnchannels(waveparams[0])
		tempWrite.setsampwidth(waveparams[1])
		tempWrite.setframerate(waveparams[2])
		tempWrite.setnframes(waveparams[3])
		tempWrite.writeframesraw(rawdata)
