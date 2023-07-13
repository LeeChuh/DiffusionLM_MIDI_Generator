import os
import json
import argparse
import pretty_midi
import numpy as np
import scipy.io.wavfile as wav
import wave


from constant import DATA_PATH, MIN_NOTE_MULTIPLIER, MIDI_EXTENSIONS

class MidiHandler:
    MIN_NOTE_MULTIPLIER = 1/32
    def __init__(self, datapath, pitch_range=(30, 96), velocity_range=(32, 127, 4), fs=1000, tempo=120, augmentation=(1, 1, 1)):
        self.datapath = datapath
        self.pitch_range = pitch_range
        self.velocity_range = velocity_range
        self.fs = fs
        self.tempo = tempo
        self.augmentation = augmentation

    # Load function
    def load(self):
        if not os.path.exists(self.datapath):
            raise FileNotFoundError(f"The specified file does not exist: {self.datapath}")

        # Load a MIDI file into a PrettyMidi object
        midi_data = pretty_midi.PrettyMIDI(self.datapath)
        return midi_data


    # Function to load files from a directory
    def _load_dir(self, dirpath):
        vocab = set()

        for dir, _, files in os.walk(dirpath):
            for i, f in enumerate(files):
                filepath = os.path.join(dir, f)

                text = self._load_file(filepath)
                if text != '':
                    vocab = vocab | set(text.split(" "))

        return vocab

    # Function to load a file
    def _load_file(self, filepath):
        text = []

        # Check if it is a midi file
        filename, extension = os.path.splitext(filepath)
        if extension.lower() in MIDI_EXTENSIONS:
            print("Encoding file...", filepath)

            if os.path.isfile(filename + ".txt"):
                with open(filename + ".txt", "r") as midi_txt:
                    text = midi_txt.read().split(" ")
            else:
                try:
                    midi_data = pretty_midi.PrettyMIDI(filepath)
                except KeyboardInterrupt:
                    print("Exiting due to keyboard interrupt")
                    quit()
                except:
                    return " ".join(text)

                text = self._midi2text(midi_data)
                with open(filename + ".txt", "w") as midi_txt:
                    midi_txt.write(" ".join(text))

        return " ".join(text)

    def midi2text(self, midi_data, pitch_range=(30, 96), velocity_range=(32, 127, 4), fs=1000, tempo=120, augmentation=(1, 1, 1)):
        text = []

        # Parse notes and tempo changes from the midi data
        midi_notes = self.parse_notes_from_midi(midi_data)


        transpose, time_stretch, velo_stretch = augmentation
        transpose_range    = (-transpose//2 + 1, transpose//2 + 1)
        time_stretch_range = (-time_stretch//2 + 1, time_stretch//2 + 1)
        velo_stretch_range = (-velo_stretch//2 + 1, velo_stretch//2 + 1)

        for i in range(transpose_range[0], transpose_range[1]):
            for j in range(time_stretch_range[0], time_stretch_range[1]):
                for k in range(velo_stretch_range[0], velo_stretch_range[1]):
                    last_start = last_duration = last_velocity = 0

                    for start, time_step_notes in sorted(midi_notes.items()):
                        wait_duration = self.get_note_duration((start - last_start)/fs, tempo, stretch=j)
                        if wait_duration > 0:
                            if wait_duration != last_duration:
                                text.append("d_" + str(wait_duration))
                                last_duration = wait_duration

                            text.append("a")

                        for note in time_step_notes:
                            note_pitch  = self.clamp_pitch(note["pitch"] + i, pitch_range)
                            note_velocity = self.clamp_velocity(note["velocity"] + k * 8 * velocity_range[2], velocity_range)
                            note_duration = self.get_note_duration(note["duration"]/fs, tempo, stretch=j)

                            if note_velocity > 0 and note_duration > 0:
                                if note_velocity != last_velocity:
                                    text.append("v_" + str(note_velocity))
                                    last_velocity = note_velocity

                                if note_duration != last_duration:
                                    text.append("d_" + str(note_duration))
                                    last_duration = note_duration

                                text.append("n_" + str(note_pitch))

                        last_start = start

                    text.append("\n")

        return text


    def parse_notes_from_midi(self, midi_data):
        notes = {}

        for instrument in midi_data.instruments:
            for note in instrument.notes:
                start, end = int(self.fs * note.start), int(self.fs * note.end)

                if start not in notes:
                    notes[start] = []

                notes[start].append({
                    "pitch": note.pitch,
                 "duration": end - start,
                 "velocity": note.velocity})

        return notes
    
    def text2midi(self, text, tempo):
        notes = self.parse_notes_from_text(text, tempo)

        # Create a PrettyMIDI object
        midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)

        # Create an Instrument instance for a piano instrument
        piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
        piano = pretty_midi.Instrument(program=piano_program)

        # Add notes
        for n in notes:
            piano.notes.append(n)

        midi.instruments.append(piano)

        return midi
    
    def parse_total_duration_from_text(self, text, tempo=120):
        duration, total_duration = 0, 0
        for token in text.split(" "):
            if token[0] == "a":
                total_duration += duration

            elif token[0] == "d":
                duration = int(token.split("_")[1])

        # Compute duration of shortest note
        min_duration = MIN_NOTE_MULTIPLIER * 60/tempo

        return total_duration * min_duration
    
    def parse_notes_from_text(self, text, tempo):
        notes = []

        # If text is a list, convert it to a single string
        if isinstance(text, list):
            text = " ".join(text)

        # Set default velocity
        velocity = 100

        # Set default duration
        duration = 8

        # Compute duration of shortest note
        min_duration = self.MIN_NOTE_MULTIPLIER * 60/tempo

        i = 0
        for token in text.split(" "):
            if token[0] == "a":
                i += duration

            elif token[0] == "n":
                pitch = int(token.split("_")[1])
                note = pretty_midi.Note(velocity, pitch, start=i * min_duration, end=(i + duration) * min_duration)
                notes.append(note)

            elif token[0] == "d":
                duration = int(token.split("_")[1])

            elif token[0] == "v":
                velocity = int(token.split("_")[1])

        return notes


    def clamp_velocity(self, velocity, velocity_range):
        min_velocity, max_velocity, step = velocity_range

        velocity = max(min(velocity, max_velocity), min_velocity)
        velocity = (velocity//step) * step

        return velocity

    def clamp_pitch(self, pitch, pitch_range):
        min, max = pitch_range

        while pitch < min:
            pitch += 12
        while pitch >= max:
            pitch -= 12

        return pitch

    def get_note_duration(self, dt, tempo, stretch=0, max_duration=56, percentage=0.15):
        min_duration = MIN_NOTE_MULTIPLIER * 60/tempo

        dt += dt * percentage * stretch

        # Compute how many 32th notes fit inside the given note
        note_duration = round(dt/min_duration)

        # Clamp note duration
        note_duration = min(note_duration, max_duration)

        return note_duration

    def save_vocab(self, vocab, vocab_path):
        # Create dict to support char to index conversion
        char2idx = { char:i for i,char in enumerate(sorted(vocab)) }

        # Save char2idx encoding as a json file for generate midi later
        with open(vocab_path, "w") as f:
            json.dump(char2idx, f)



    def write(self, text, path, synthesize=False, tempo=120):
        SF2_PATH = "soundfonts/SalC5Light2.sf2"
        WAV_32INT_MAX = 2147483647

        # Convert the text into a MIDI object
        midi = self.text2midi(text, tempo)

        # Write the MIDI object to a file
        midi.write(path + ".mid")

        # Check if audio synthesis is requested
        if synthesize:
            # Use fluidsynth to convert MIDI to audio
            audio = midi.fluidsynth(fs=44100, sf2_path=SF2_PATH)

            # Normalize the audio data
            audio = np.int32(audio/np.max(np.abs(audio)) * WAV_32INT_MAX)

            # Save the audio data to a .wav file
            wav.write(path + ".wav", 44100, audio)





# if __name__ == '__main__':
#     midi_handler = MidiHandler(datapath=DATA_PATH)
#     midi_data = midi_handler.load()
#     text = midi_handler.midi2text(midi_data)
#     print(text)
#     midi = midi_handler.text2midi(text, tempo=120) 

#     a = midi_handler.write(text, '../samp', synthesize=False)  