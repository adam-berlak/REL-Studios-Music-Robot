from Configuration import *
from IOMidi.MidiToObjects import *
from mxm.midifile import *

class Sequencer():

    def __init__(self):
        self.notes = {}
        self.current_beat = 0

    def add(self, p_music_object, p_beat = None, p_channel = 0):
        current_beat = p_beat if p_beat is not None else self.getCurrentBeat()
        if p_channel not in self.getNotes().keys(): self.getNotes()[p_channel] = {}
        if current_beat not in self.getNotes()[p_channel].keys(): self.getNotes()[p_channel][p_beat] = []
        self.getNotes()[p_channel][current_beat] += toMidiData(p_music_object)
        self.updateCurrentBeat(current_beat + max([note.getDuration() for note in toMidiData(p_music_object)]))

    def updateCurrentBeat(self, p_current_beat):
        self.current_beat = p_current_beat

    def getNoteOnEvents(self):
        result = []

        for channel in self.getNotes().keys():
            for key in self.getNotes()[channel].keys():
                notes = self.getNotes()[channel][key]
                result += [{"event_action": 'note_on',
                            "data": (note.getKey().toDecimal(), note.getVelocity()), 
                            "absolute_position": key,
                            "channel": channel} for note in notes]

        return result

    def getNoteOffEvents(self):
        result = []

        for channel in self.getNotes().keys():
            for key in self.getNotes()[channel].keys():
                notes = self.getNotes()[channel][key]
                result += [{"event_action": 'note_off',
                            "data": (note.getKey().toDecimal(), note.getVelocity()), 
                            "absolute_position": key + int(4 / note.getDuration()),
                            "channel": channel} for note in notes]

        return result

    def getEvents(self):
        events = self.getNoteOnEvents() + self.getNoteOffEvents()
        events.sort(key=lambda x: x["absolute_position"])
        return events

    def fromMidi(self, p_file_name):
        event_handler = MidiToObjects()
        midi_in = MidiInFile(event_handler, p_file_name)
        midi_in.read()
        return self.setNotes(event_handler.getNotes())

    def toMidi(self, p_file_name = 'file-generated.mid'):
        out_file = open(p_file_name, 'wb')
        midi = MidiOutFile(out_file)

        midi.header(format=0, nTracks=1, division=int(1920/4))
        midi.start_of_track()

        previous_absolute_position = 0

        for event in self.getEvents():
            midi.update_time((int(1920/4) * event["absolute_position"]) - previous_absolute_position)
            midi.note_on(event["channel"], event["data"][0], event["data"][1]) if event["event_action"] == 'note_on' else midi.note_off(0, event["data"][0], event["data"][1])
            previous_absolute_position = (int(1920/4) * event["absolute_position"])

        midi.update_time(0)
        midi.end_of_track()

    def getNotes(self): return self.notes
    def getCurrentBeat(self): return self.current_beat

    def setNotes(self, p_notes): self.notes = p_notes
    def setCurrentBeat(self, p_current_beat): self.current_beat = p_current_beat