#!/bin/python3

import wave
import audioop
import random
from pydub import AudioSegment
from pydub.playback import play

# returns a list of lists of points in the song with similar frequencies
def loadConnections(song):
	return []

def main():
	# initialize variables
	song = AudioSegment.from_mp3("testmusic/funkychunk.mp3")

	# load connections list with song links
	connections = loadConnections(song)

	# play song. We need to allow the song to randomly jump via connections[]
	print("hi")
	random.randint(0,2)

if __name__=="__main__":
    main()
