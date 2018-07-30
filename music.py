"""
    This file deals with uploading music 
    It also converts the mp3 file into bit stream
"""
from pydub import AudioSegment
from pydub.playback import play
import os
import io



cwd = os.getcwd()
song_path = cwd+"/music/song.mp3"

def convert(song=song_path):
    sound = AudioSegment.from_mp3(song)

    # get the raw data
    raw_data = sound._data

    return raw_data


def convert_to_music(bytes):
    song = AudioSegment.from_file(io.BytesIO(bytes), format="mp3")
    print(song)
    #play(song)



if __name__ == "__main__":
    convert()



