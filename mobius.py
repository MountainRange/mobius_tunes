#!/bin/python3

import wave
import audioop
import random
from pydub import AudioSegment
from pydub.playback import play
from operator import itemgetter

# returns a list of lists of points in the song with similar frequencies
def loadConnections(playList[0]):
	return []

def fractureSong(song, connections):
	fragments = []
	for breakPoint in connections:
		fragments.append(song[:])
	return fragments

def main():
	# initialize variables
	playlist = []
	song = AudioSegment.from_mp3("testmusic/funkychunk.mp3") #for each song
	playList.append(song)

	# load connections list with song links
	connections = loadConnections(playList)
	sorted(connections, key = itemgetter(0))

	# play song. We need to allow the song to randomly jump via connections[]
	songFragments = fractureSong(song, connections)
	print(connections)
	play(song)
	random.randint(0,2)

if __name__ == "__main__":
    main()
