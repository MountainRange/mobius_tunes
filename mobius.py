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
	i = 0
	while (i < len(connections)):
		i += 1
		fragments.append(song[:connections[i]])
		song = song[connections[i]:]
	return fragments

def main():
	# get songs
	song = AudioSegment.from_mp3("testmusic/funkychunk.mp3") #for each song

	folder = tempfile.mkdtemp()
	print(folder)

	filename = song.export(folder + "/filename.wav", format="wav")

	wavefile = wave.open(filename.name)
	wavefile.setpos(0)
	rawdata = wavefile.readframes(wavefile.getnframes())

	playList = []
	playList.append(song)

	# load connections list with song links
	connections = loadConnections(playList)
	sorted(connections, key = itemgetter(0))

	# play song. We need to allow the song to randomly jump via connections[]
	songFragments = fractureSong(song, connections)
	print(connections)
	play(songFragments[0])
	random.randint(0,2)

if __name__ == "__main__":
    main()
