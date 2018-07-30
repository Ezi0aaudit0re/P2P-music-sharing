"""
    This file deals with uploading music 
    It also converts the mp3 file into bit stream
"""
from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import mediainfo
import os
import io


sound = None
converted_sound = None

cwd = os.getcwd()
song_path = cwd+"/music/song.mp3"

def convert(song=song_path):
    sound = AudioSegment.from_mp3(song)

    # get the raw data
    raw_data = sound._data

    return raw_data


def convert_to_music(bytes):
    song = AudioSegment.from_file(io.BytesIO(bytes), format="mp3")
    output = io.StringIO()
    song.export(output, format="mp3", bitrate="192k")
    converted_sound = AudioSegment.from_mp3(cwd + "/music/copy.mp3")
    print("Done")



if __name__ == "__main__":
    music = convert()
    convert_to_music(music)
    if sound == converted_sound:
        print("They are the same")
    else:
        print("They are not the same")



