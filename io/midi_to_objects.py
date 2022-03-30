from theory.key import *
from theory.note import *
from mxm.midifile import *

class MidiToObjects(MidiToCode):

    def __init__(self):
        self.notes = {}
        self.active_notes = []

    def header(self, format=0, nTracks=1, time_division=480):
        super().header(format, nTracks, time_division)
        self.setDivision(time_division)

    def note_on(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        super().note_on(channel, note, velocity, use_running_status)
        active_notes = self.getActiveNotes() + [{"key": Key.decimalToKey(note), 
                        "velocity": velocity,
                        "absolute_time": self.abs_time(), 
                        "channel": channel}]

        self.setActiveNotes(active_notes)
        
    def note_off(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        super().note_off(channel, note, velocity, use_running_status)
        active_notes = [item for item in self.getActiveNotes() if item["key"] == Key.decimalToKey(note)]

        if len(active_notes) > 0:
            while True:
                active_note = max(active_notes, key=lambda x: x["absolute_time"])
                duration = (self.abs_time() - active_note["absolute_time"]) / self.getDivision()
                active_notes.remove(active_note)
                if duration != 0 or len(active_notes) == 0: break

            if active_note["channel"] not in self.getNotes().keys(): self.getNotes()[active_note["channel"]] = {}
            if active_note["absolute_time"] not in self.getNotes()[active_note["channel"]].keys(): self.getNotes()[active_note["channel"]][active_note["absolute_time"]] = []
            
            notes = self.getNotes()
            notes[active_note["channel"]][active_note["absolute_time"]] += [Note(active_note["key"], duration, active_note["velocity"])]
            new_active_notes = self.getActiveNotes()[:]
            new_active_notes.remove(active_note)
            
            self.setActiveNotes(new_active_notes)
            self.setNotes(notes)

    def getNotes(self): return self.notes
    def getActiveNotes(self): return self.active_notes
    def getDivision(self): return self.time_division

    def setNotes(self, p_notes): self.notes = p_notes
    def setActiveNotes(self, p_active_notes): self.active_notes = p_active_notes
    def setDivision(self, p_time_division): self.time_division = p_time_division
