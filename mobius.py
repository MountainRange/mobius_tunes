#!/bin/python3

import wave
import audioop
from pydub import AudioSegment
from pydub.playback import play

song = AudioSegment.from_mp3("testmusic/funkychunk.mp3")
play(song)
