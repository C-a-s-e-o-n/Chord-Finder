from pydub import AudioSegment
from pydub.playback import play

def convert_note(note):
    # Load AIFF file
    aiff_file_path = (f"app/static/notes/Piano.ff.{note}.aiff")
    audio = AudioSegment.from_file(aiff_file_path, format="aiff")

    # Export as WAV
    wav_file_path = (f"app/static/notes/{note}_unedited.wav")
    audio.export(wav_file_path, format="wav")

    print(f"Conversion completed. WAV file saved at: {wav_file_path}")

def shorten_and_fadeout(note):
    # Load WAV file
    wav_file = AudioSegment.from_file(file= (f"app/static/notes/{note}_unedited.wav"), format= "wav")

    # start 1 second in, end at 2.5 seconds
    start_time = 1000
    end_time = 2500

    # Fade the entire time
    fadeout_duration = 2500

    # Apply correct timing
    wav_short = wav_file[start_time:start_time+end_time]
    # Apply fadeout
    wav = wav_short.fade_out(fadeout_duration)
    
    wav_file_path = (f"app/static/notes/{note}.wav")
    wav.export(wav_file_path, format="wav")
    #play(wav)


def play_note(note):
    wav_file = AudioSegment.from_file(file= (f"app/static/notes/{note}.wav"), format= "wav")
    play(wav_file)


def play_notes_quickly(note_paths):
    for note_path in note_paths:
        # Load the note as an AudioSegment
        note = AudioSegment.from_file(note_path, format="wav")

        # Apply a quick fade-out effect
        note_fadeout = note.fade_out(100)

        play(note_fadeout)


#play_notes_quickly(note_paths)


def overlay_block_chord(note_paths):
    overlayed = AudioSegment.silent(duration=0)

    for note_path in note_paths:
        note = AudioSegment.from_file(note_path, format="wav")
        overlayed = note.overlay(overlayed, position=0)

    #play(overlayed)
    return overlayed

# Test the function with note_paths
note_paths = ["app/static/notes/C3.wav", "app/static/notes/E3.wav", "app/static/notes/G3.wav"]

def overlay_slow_arpeggiated(note_paths):
    note1 = AudioSegment.from_file(note_paths[0])
    note2 = AudioSegment.from_file(note_paths[1])
    note3 = AudioSegment.from_file(note_paths[2])

    overlayed = note1.overlay(note2, position=180).overlay(note3, position=350)

    #play(overlayed)

#overlay_slow_arpeggiated(note_paths)

#overlay_slow_arpeggiated(note_paths)
#overlay_block_chord(note_paths)