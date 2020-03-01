from mxm.midifile.src import constants as c
from mxm.midifile.src.midi_events import MidiEvents

from Components.Note import Note

class MidiToObjects(MidiEvents):

    def note_on(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):

        if velocity == 0:
            print(Note(Key.decimalToKey(note), self.rel_time()))