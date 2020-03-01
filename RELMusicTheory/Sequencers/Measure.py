class Measure:

    def __init__(self, p_time_signature = (4, 4), p_current_beat = 0.0, p_contents = []):
        self.time_signature = p_time_signature
        self.current_beat = p_current_beat
        self.contents = p_contents

    def placeNotes(self, p_notes):
        self.placeNotesAt(p_notes, self.getCurrentBeat())
        self.setCurrentBeat(self.getCurrentBeat() + (p_notes.getDuration() * 4))

    def placeNotesAt(self, p_notes, p_beat): self.getContents()[p_beat] += p_notes

    def getTimeSignature(self): return self.time_signature
    def getCurrentBeat(self): return self.current_beat
    def getContents(self): return self.contents

    def setTimeSignature(self, p_time_signature): self.time_signature = p_time_signature
    def setCurrentBeat(self, p_current_beat): self.current_beat = p_current_beat
    def setContents(self, p_contents): self.contents = p_contents