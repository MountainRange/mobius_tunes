# Mobius Tunes
This is our submission for HackGT 2015. Mobius Tunes is inspired by [Infinite Jukebox](http://labs.echonest.com/Uploader/index.html), a site that continually and randomly loops a given song to other parts of the song that sound similar. Our goal is to recreate it as an open-source project, allowing for multiple songs within a playlist folder to link to one another as well as themselves.

### Dependencies
```
pip3 install wave
pip3 install pydub
pip3 install numpy
pip3 install scipy
pip3 install pyglet
```
Or equivalent with your package manager!

This project requires FFMPEG or avconv. [See this for help](https://ffmpeg.org/download.html)
In order to install avconv on linux, run sudo apt-get install libav-tools

This project also requires libav! Install with `apt-get install libavbin0 libavbin-dev`.

Does NOT support windows unless ffmpeg is compiled.
We recommend you run mobius-tunes run on linux! :smile:

### Usage

`./mobius.py`  Runs mobius.py w/ default settings looking for songs in the testmusic folder

`./mobius.py [-d directory] [-c chunksize] [-t threshold]`

Mobius Tunes will then remix the files in the folder specified, until you kill it with `^C`. We recommend you use the mp3 files we have provided in the testmusic folder with our project (use -d to specify the directory), but you are free to fill the with similar sounding songs of your choice. Be aware that one of the provided mp3 files is Rick Astley, so with this forewarning do not consider it a rick roll when it plays.

Enjoy!

