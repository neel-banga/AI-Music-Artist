from music21 import note, stream, configure

# Configure the music21 environment
#configure.run()

# Create a stream object to hold the music
stream_obj = stream.Stream()

# Define a series of pitch numbers (MIDI note numbers) for the melody
melody_pitches = [60, 62, 64, 65, 67, 69, 71, 72]

# Convert pitch numbers to Note objects and add them to the stream
for pitch in melody_pitches:
    note_obj = note.Note()
    note_obj.pitch.midi = pitch
    stream_obj.append(note_obj)

# Show the sheet music representation
stream_obj.write('midi', fp='piano_music.mid')