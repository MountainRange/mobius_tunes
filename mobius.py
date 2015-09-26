#!/bin/python3

import wave
import audioop
import random
from pydub import AudioSegment
from pydub.playback import play
import tempfile

# returns a list of lists of points in the song with similar frequencies
def loadConnections(song):
	return []

def main():
	# initialize variables
	song = AudioSegment.from_mp3("testmusic/funkychunk.mp3")

	# load connections list with song links
	connections = loadConnections(song)
	folder = tempfile.mkdtemp()
	print(folder)

	# Write mp3 to wav
	filename = song.export(folder + "/filename.wav", format="wav")
	wavefile = wave.open(filename.name)
	wavedata = wavefile.getparams()
	wavefile.setpos(0)
	rawdata = wavefile.readframes(wavefile.getnframes())

	# PERFORM SOME CHANGES


	# Write changes
	tempWrite = wave.open(folder + "/temporaryOutput.wav", mode = 'wb')
	tempWrite.setnchannels(wavedata[0])
	tempWrite.setsampwidth(wavedata[1])
	tempWrite.setframerate(wavedata[2])
	tempWrite.setnframes(wavedata[3])
	tempWrite.writeframesraw(rawdata)

	# play song. We need to allow the song to randomly jump via connections[]
	#play(song)
	#print("hi")
	#random.randint(0,2)

if __name__=="__main__":
	main()
