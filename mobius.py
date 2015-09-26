#!/bin/python3

import audioop
import random
import pyglet

# returns a list of lists of points in the song with similar frequencies
def loadConnections(song):
	return []

def main():
	# initialize variables
	song = pyglet.media.load("testmusic/funkychunk.mp3")
	song.play()
	pyglet.app.run()

	# load connections list with song links
	connections = loadConnections(song)

	# play song. We need to allow the song to randomly jump via connections[]
	print(connections)
	random.randint(0,2)

if __name__=="__main__":
	main()
