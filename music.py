from midiutil import MIDIFile
import os
import subprocess
import subprocess
import pygame
from midi2audio import FluidSynth

# Define Constants

track    = 0
channel  = 0
time     = 0   
duration = 0.3 # Will later be changed by AI
tempo    = 60 # Will later be changed by AI
volume   = 100

END_NOTE_NUM = 112 # expirementing with other vals like 12 n then *10

def convert_to_wav(filename):
    if os.path.isfile(filename):
      new_file = filename.replace('.mid', '.wav')
      # This command will convert the file to wav, the ">/dev/null 2>&1" part simply hides the output
      command = f'ffmpeg -i {filename} {new_file} >/dev/null 2>&1'
      subprocess.run(command, shell=True, input='y\n', text=True)

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

def listen_midi(midi = 'music.mid'):

  pygame.init()
  pygame.mixer.music.load(midi)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
  return "Music's over"

def to_wav(filename):
  FluidSynth().play_midi(filename)
  fs = FluidSynth()
  fs.midi_to_audio(filename, 'output.wav')

def play_music(genome):
    create_music(genome)