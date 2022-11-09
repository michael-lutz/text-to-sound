"""""""""""""""""""""""""""""""""""""""
Author: Michael Lutz                
                                    
Overview: Processes and formats midi
files into a CSV file for training.

"""""""""""""""""""""""""""""""""""""""

from mido import MidiFile
import pandas as pd
import os

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

directory = "data/raw-adl-piano-midi/"


def create_note_sequence(track):
    globalTime = 0
    mapping = dict()
    noteSequence = []
    for message in track:
        note, time = message.note, message.time
        if note in mapping:
            start = mapping.pop(note)
            noteSequence.append((note, time + globalTime - start, start))
        else:
            mapping[note] = globalTime + time
        globalTime += time

    noteSequence.sort(key = lambda item: item[2])
    for i in range(len(noteSequence)):
        nextItem = -1
        for j in range(i, len(noteSequence)):
            if noteSequence[j][2] != noteSequence[i][2]:
                nextItem = j
                break
        noteSequence[i] = [number_to_note(noteSequence[i][0]), noteSequence[i][1], noteSequence[i][2], noteSequence[nextItem][2] - noteSequence[i][2]]

    return stringify_sequence(noteSequence)

def stringify_sequence(seq):
    result = ''
    for line in seq:
        result += 'n' + str(line[0]) + 'd' + str(line[1]) + 't' + str(line[3]) + ' '
    return result

def number_to_note(number: int) -> tuple:
    octave = number // NOTES_IN_OCTAVE
    assert octave in OCTAVES, 'Error with octaves'
    assert 0 <= number <= 127, 'Error with notes'
    note = NOTES[number % NOTES_IN_OCTAVE]
    return note

def return_roots(directory):
    file_list = []
    for folder in os.scandir(directory):
        print(folder)
        if folder.is_dir():
            file_list += return_roots(folder.path)
        elif folder.path.endswith('.mid'):
            file_list.append(folder.path)
    return file_list


data_list = []

"""mid = MidiFile('data/adl-piano-midi/Rap/Chicago Rap/Kanye West/Diamonds From Sierra Leone.mid')
for track in mid.tracks:
    track = list(filter((lambda x: 'note_on' in str(x)), track))
    if len(track) != 0:
        x = 'Rap song in the style of Kanye West'
        data_list.append([x, create_note_sequence(track)])"""



for song_path in return_roots(directory):
    song_path_list = song_path.split('/')
    artist_name = song_path_list[-2]
    genre_name = song_path_list[-3]
    x = genre_name + ' song in the style of ' + artist_name

    try:
        mid = MidiFile(song_path)
        for track in mid.tracks:
            track = list(filter((lambda x: 'note_on' in str(x)), track))
            if len(track) != 0:
                data_list.append([x, create_note_sequence(track)])
        print('saved')
    except:
        print('failed to decode, skipping')



df = pd.DataFrame(data_list, columns=['input', 'sequence'])
df.to_csv('data/converted_sequences/sequence-adl-piano-midi.csv')
