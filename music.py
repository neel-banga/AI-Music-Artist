from random import randrange
from midiutil import MIDIFile
import os
import subprocess
import wave
import pyaudio

# Define Constants

track    = 0
channel  = 0
time     = 0   
duration = 0.3 # Will later be changed by AI
tempo    = 60 # Will later be changed by AI
volume   = 100

END_NOTE_NUM = 60 # expirementing with other vals like 12 n then *10

def convert_to_wav(filename):
    if os.path.isfile(filename):
      new_file = filename.replace('.mid', '.wav')
      # This command will convert the file to wav, the ">/dev/null 2>&1" part simply hides the output
      command = f'ffmpeg -i {filename} {new_file} >/dev/null 2>&1'
      subprocess.run(command, shell=True, input='y\n', text=True)
      os.remove(filename)

def create_music(notes):

    global time

    music = MIDIFile(1)

    music.addProgramChange(track, channel, time, 0)
    
    for note in notes:

        music.addNote(track, channel, note, time, duration, volume)
        time += duration

    # While this gives us less options there is a lot of sequances that can be made w 12 notes

    with open("music.mid", "wb") as output_file:
        music.writeFile(output_file)

    full_file = os.path.join(os.getcwd(), output_file.name)

    convert_to_wav(full_file)

def play_music(path = 'music.wav'):
    wav_file = wave.open(path, 'rb')
    audio = pyaudio.PyAudio()

    stream = audio.open(format=audio.get_format_from_width(wav_file.getsampwidth()),
                        channels=wav_file.getnchannels(),
                        rate=wav_file.getframerate(),
                        output=True)

    chunk_size = 1024
    data = wav_file.readframes(chunk_size)

    while data:
        stream.write(data)
        data = wav_file.readframes(chunk_size)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wav_file.close()