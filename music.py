from midiutil import MIDIFile
import os
import subprocess
import subprocess
import pygame
import mido

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

    #full_file = os.path.join(os.getcwd(), output_file.name)

    #convert_to_wav(full_file)

def listen_midi(midi = 'music.mid'):

  pygame.init()
  pygame.mixer.music.load(midi)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
  return "Music's over"

def play_midi_file(midi_file = 'music.mid'):
    try:
        mid = mido.MidiFile(midi_file)

        for message in mid.play():
            if message.type == 'note_on':
                # Handle note_on messages, e.g., send them to a synthesizer or sound card
                print(f"Note On: {message.note}")
            elif message.type == 'note_off':
                # Handle note_off messages, e.g., stop playing the note
                print(f"Note Off: {message.note}")
            else:
                # Handle other MIDI messages as needed
                print(f"MIDI Message: {message}")

            time.sleep(message.time)

    except FileNotFoundError:
        print(f"File '{midi_file}' not found.")
    except mido.MidiFileError as e:
        print(f"Error loading MIDI file: {e}")

def play_music(genome):
    create_music(genome)
    listen_midi()

play_music([108, 79, 107, 96, 34, 93, 27, 2, 46, 89, 71, 104, 78, 79, 103, 21, 73, 98, 17, 107])