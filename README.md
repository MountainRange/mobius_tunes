# Mobius Tunes
This is our submission for HackGT 2015. Mobius Tunes is inspired by [Infinite Jukebox](http://labs.echonest.com/Uploader/index.html), a site that continually and randomly loops a given song to other parts of the song that sound similar. Our goal is to recreate it as an open-source project, allowing for multiple songs within a playlist folder to link to one another as well as themselves.

### Dependencies
```
pip3 install numpy
pip3 install scipy
pip3 install pyglet
pip3 install mutagen
```
Or equivalent with your package manager!

This project requires avbin! Please install the [lastest version here](https://avbin.github.io/AVbin/Download.html)

Any Platform that supports python3 and avbin will probably work, but we recommend you run mobius-tunes run on linux! :smile:

Install this package with
`pip3 install mobius-tunes`

### Usage

`mobius-tunes`  Runs mobius.py w/ default settings looking for songs in the testmusic folder

`mobius-tunes [-d directory] [-c chunksize] [-t threshold]`

`./runner.py` Runs from source repository

Mobius Tunes will then remix the files in the folder specified, until you kill it with `^C`. If you don't know what songs you want our project to run with, we recommend trying Ain't No Mountain High Enough, Eye of the Tiger, and Never Gonna Give You Up together. These three songs interact nicely in Mobius Tunes.

Enjoy!


