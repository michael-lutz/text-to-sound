from midiutil.MidiFile import MIDIFile
import re

class Converter:
    note_dict = {
        'C' : 60,
        'C#' : 61,
        'D' : 62,
        'D#' : 63,
        'E' : 64,
        'F' : 65,
        'F#' : 66,
        'G' : 67,
        'G#' : 68,
        'A' : 69,
        'A#' : 70,
        'B' : 71
    }

    def __init__(self, prompt, sequence, volume=100, tempo=120):
        self.prompt = prompt
        self.sequence = sequence
        self.notes = []
        
        self.volume = volume

        self.mf = MIDIFile(1)     # only 1 track
        self.time = 0    # start at the beginning
        
        self.mf.addTrackName(0, self.time, "Sample Track")
        self.mf.addTempo(0, self.time, tempo)

        self.create_notes()
        
        for note in self.notes:
            self.add_note(note)

    # Clean the sequence and make a list
    def create_notes(self):
        self.notes = self.sequence[len(self.prompt):].split()

    # take in note and add mf
    def add_note(self, representation):
        match_object = re.match('n(A#|A|B|C|C#|D|D#|E|F|F#|G|G#)d([\d]+)t([\d]+)', representation)
        if match_object:
            note_t = match_object.groups()
            pitch = Converter.note_dict[note_t[0]]
            self.time += int(note_t[2]) / 48
            duration = int(note_t[1]) / 48
            self.mf.addNote(0, 0, pitch, self.time, duration, self.volume)

    # Write out
    def write(self):
        name = self.prompt + ".mid"
        print(name)
        with open(name, 'wb') as outf:
            self.mf.writeFile(outf)
