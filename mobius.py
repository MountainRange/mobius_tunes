#!/bin/python3

import wave
import audioop
import random
import tempfile
from pydub import AudioSegment
from pydub.playback import play
from operator import itemgetter

# returns a list of lists of points in the song with similar frequencies
def loadConnections(playList):
	return []

def fractureSong(song, connections):
	fragments = []
	for breakPoint in connections:
		fragments.append(song[:])
	return fragments

	# load connections list with song links
	connections = loadConnections(song)

def main():
	# get songs
	song = AudioSegment.from_mp3("testmusic/funkychunk.mp3") #for each song

	folder = tempfile.mkdtemp()
	print(folder)

	# Write mp3 to wav
	filename = song.export(folder + "/filename.wav", format="wav")
	wavefile = wave.open(filename.name)
	wavedata = wavefile.getparams()
	wavefile.setpos(0)
	rawdata = wavefile.readframes(wavefile.getnframes())

	# PERFORM SOME CHANGES

	playList = []
	playList.append(song)

	# load connections list with song links
	connections = loadConnections(playList)
	sorted(connections, key = itemgetter(0))



	# Write changes
	tempWrite = wave.open(folder + "/temporaryOutput.wav", mode = 'wb')
	tempWrite.setnchannels(wavedata[0])
	tempWrite.setsampwidth(wavedata[1])
	tempWrite.setframerate(wavedata[2])
	tempWrite.setnframes(wavedata[3])
	tempWrite.writeframesraw(rawdata)

	# play song. We need to allow the song to randomly jump via connections[]
	songFragments = fractureSong(song, connections)
	print(connections)
	play(song)
	random.randint(0,2)

if __name__ == "__main__":
    main()
