from Configuration import *
from IOMidi.Channel import *
from IOMidi.MidiToObjects import *

class Sequencer:

    def __init__(self, p_time_division = None, p_channels = {}):
        self.time_division = p_time_division if p_time_division is not None else TIME_DIVISION
        self.channels = [Channel(0)] if p_channels is not {} else Sequencer.fromDict(p_channels)

    def __getitem__(self, p_index):
        if p_index not in [channel.getNumber() for channel in self.getChannels()]: 
            self.getChannels().add(Channel(p_index))

        return self.getChannels()[p_index]

    def getNoteOnEvents(self):
        result = []

        for channel in self.getChannels():
            for key in Sequencer.toDict(channel).keys():
                notes = Sequencer.toDict(channel)[key]
                result += [{"event_action": 'note_on',
                            "data": (note.getKey().toDecimal(), note.getVelocity()), 
                            "time": key,
                            "channel": channel.getNumber()} for note in notes]

        return result

    def getNoteOffEvents(self):
        result = []

        for channel in self.getChannels():
            for key in Sequencer.toDict(channel).keys():
                notes = Sequencer.toDict(channel)[key]
                result += [{"event_action": 'note_off',
                            "data": (note.getKey().toDecimal(), note.getVelocity()), 
                            "time": key + int(4 / note.getDuration()),
                            "channel": channel.getNumber()} for note in notes]

        return result

    def getEvents(self):
        events = self.getNoteOnEvents() + self.getNoteOffEvents()
        events.sort(key=lambda x: x["time"])
        return events

    def flattenDict(p_dict):
        new_beats = {}

        for channel in p_dict.keys():
            new_beats += p_dict[channel]
        
        return new_beats

    @staticmethod
    def fromDict(p_dict):
        new_channels = []

        for channel in p_dict.keys():
            new_channel = Channel(channel, p_dict[channel])
            new_channels.append(new_channel)

        return new_channels

    @staticmethod
    def toDict(p_sequencer):
        new_channels = {}

        for channel in p_sequencer.getChannels():
            new_channels[channel.getNumber()] = Channel.toDict(channel)
        
        return new_channels

    def fromMidi(self, p_file_name):
        event_handler = MidiToObjects()
        midi_in = MidiInFile(event_handler, p_file_name)
        midi_in.read()
        self.setChannels(Sequencer.fromDict(event_handler.getNotes()))

    def toMidi(self, p_file_name = 'file-generated.mid'):
        out_file = open(p_file_name, 'wb')
        midi = MidiOutFile(out_file)

        midi.header(format=0, nTracks=1, division=self.getTimeDivision())
        midi.start_of_track()

        previous_time = 0

        for event in self.getEvents():
            midi.update_time((self.getTimeDivision() * event["time"]) - previous_time)
            midi.note_on(event["channel"], event["data"][0], event["data"][1]) if event["event_action"] == 'note_on' else midi.note_off(0, event["data"][0], event["data"][1])
            previous_time = (self.getTimeDivision() * event["time"])

        midi.update_time(0)
        midi.end_of_track()

    def getChannels(self): return self.channels
    def getTimeDivision(self): return self.time_division

    def setChannels(self, p_channels): self.channels = p_channels
    def setTimeDivision(self, p_time_divsion): self.time_division = p_time_divsion