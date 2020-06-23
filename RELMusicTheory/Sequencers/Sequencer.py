from Configuration import *

from mxm.midifile import MidiOutFile, MidiToCode

class Sequencer():

    def __init__(self):
        self.notes = {}

    def add(self, p_note, p_beats):
        self.getNotes()[p_beats] = self.getNotes()[p_beats] + toMidiData(p_note) if p_beats in self.getNotes().keys() else toMidiData(p_note)

    def getNoteOnEvents(self):
        result = []
        for key in self.getNotes().keys():
            notes = self.getNotes()[key]
            result += [{"event_action": 'note_on',"data": (note.getKey().toDecimal(), note.getVelocity()), "absolute_position": key} for note in notes]

        return result

    def getNoteOffEvents(self):
        result = []
        for key in self.getNotes().keys():
            notes = self.getNotes()[key]
            result += [{"event_action": 'note_off',"data": (note.getKey().toDecimal(), note.getVelocity()), "absolute_position": key + int(4 / note.getDuration())} for note in notes]

        return result

    def getEvents(self):
        events = self.getNoteOnEvents() + self.getNoteOffEvents()
        events.sort(key=lambda x: x["absolute_position"])
        return events

    def toMidi(self):
        out_file = open('file-generated.mid', 'wb')
        midi = MidiOutFile(out_file)

        midi.header(format=0, nTracks=1, division=int(1920/4))
        midi.start_of_track()

        previous_absolute_position = 0

        for event in self.getEvents():
            print(event)
            midi.update_time((int(1920/4) * event["absolute_position"]) - previous_absolute_position)
            midi.note_on(0, event["data"][0], event["data"][1]) if event["event_action"] == 'note_on' else midi.note_off(0, event["data"][0], event["data"][1])
            previous_absolute_position = (int(1920/4) * event["absolute_position"])

        midi.update_time(0)
        midi.end_of_track()

    def getNotes(self): return self.notes