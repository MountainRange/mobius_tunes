#!/bin/python3

import wave
import audioop
from pydub import AudioSegment
from pydub.playback import play

def main():

	song = AudioSegment.from_mp3("testmusic/funkychunk.mp3")
	counter = 1
	while counter > 0:
		counter -= 1
		play(song)

if __name__=="__main__":
    main()
